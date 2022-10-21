
from fastapi import Body, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from v2api.types.vmess import VMessAccount
from v2api import errors as v2errors
from . import app, database as db
from .v2ray import client as v2client
from .utils import share_vmess, validate_username


class User(BaseModel):
    username: str
    id: UUID = Field(default_factory=uuid4)


class UserModify(BaseModel):
    id: UUID = Field(default_factory=uuid4)


class UserResponse(BaseModel):
    username: str
    id: UUID
    plans: list
    link: str
    qr: str


class Plan(BaseModel):
    data: int
    ttl: int


@app.post("/user", tags=['User'], response_model=UserResponse)
def add_user(user: User):
    """
    Add a new user

    - **id** must be an UUID. if not specified, a random UUID will be generated for user.
    """

    if not validate_username(user.username):
        raise HTTPException(
            status_code=400,
            detail="Username only can be 3 to 12 characters and contain a-z, 0-9, and underscores in between.")

    added = db.add_user(user.username, user.id)
    if not added:
        raise HTTPException(status_code=409, detail="User already exists.")

    link, qr = share_vmess(user.id, user.username)
    return UserResponse(id=user.id, username=user.username, plans=[], link=link, qr=qr)


@app.get("/user/{username}", tags=['User'], response_model=UserResponse)
def get_user(username: str):
    """
    Get users information and active plans
    """
    if user := db.get_user(username):
        link, qr = share_vmess(user['id'], user['username'])
        return UserResponse(id=user['id'], username=user['username'], plans=user['plans'], link=link, qr=qr)

    raise HTTPException(status_code=404, detail="User not found")


@app.put("/user/{username}", tags=['User'], response_model=UserResponse)
def modify_user(username: str, modify: UserModify):
    """
    Change user id
    """
    modified = db.modify_user(username, modify.id)
    if not modified:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        v2client.remove_user(email=username, inbound_tag="VMESS_INBOUND")
        v2client.add_user(email=username,
                          inbound_tag='VMESS_INBOUND',
                          account=VMessAccount(modify.id))
    except v2errors.EmailNotFoundError:
        pass

    user = db.get_user(username)
    link, qr = share_vmess(modify.id, username)
    return UserResponse(id=user['id'], user=user['username'], plans=user['plans'], link=link, qr=qr)


@app.delete("/user/{username}", tags=['User'])
def remove_user(username: str):
    """
    Remove a user
    """
    removed = db.remove_user(username)
    if not removed:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        v2client.remove_user(email=username, inbound_tag="VMESS_INBOUND")
    except v2errors.EmailNotFoundError:
        pass
    return {}


@app.get("/users", tags=['User'])
def get_users(only_active_users: bool):
    """
    Get all users

    -  **only_active_users**: returns only users who have at least one active plan
    """
    return db.get_users(only_active_users)


@app.post("/plan", tags=['Plan'])
def add_plan(plan: Plan, username: str = Body(..., embed=True)):
    """
    Add a new plan for the user

    - **data**: must be in bytes, e.g. 1073741824B = 1GB
    - **ttl**: time to live, must be in seconds
    """
    ok = db.add_plan(username, plan.data, plan.ttl)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")

    dbuser = db.get_user(username)
    try:
        v2client.add_user(email=dbuser['username'],
                          inbound_tag='VMESS_INBOUND',
                          account=VMessAccount(dbuser['id']))
    except v2errors.EmailExistsError:
        pass

    return dbuser
