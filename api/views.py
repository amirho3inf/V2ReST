from fastapi import Body, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from v2api.types.vmess import VMessAccount
from v2api import errors as v2errors
from . import app, database as db
from .v2ray import client as v2client


class User:
    class new(BaseModel):
        id: UUID = Field(default_factory=uuid4)
        username: str

    class modify(BaseModel):
        username: str  # unchangeable
        id: UUID


class Plan(BaseModel):
    data: int
    ttl: int


@app.get("/user/{username}", tags=['User'])
def get_user(username: str):
    """
    Get users information and active plans
    """
    if user := db.get_user(username):
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user", tags=['User'])
def add_user(user: User.new):
    """
    Add a new user

    - **id** must be an UUID. if not specified, a random UUID will be generated for user.
    """

    # TODO
    # if not user.username.isalpha():
    #     raise HTTPException(status_code=400,
    #                         detail="Username can only contain alpha characters")

    added = db.add_user(user.username, user.id)
    if not added:
        raise HTTPException(status_code=409, detail="User already exists.")

    return user


@app.put("/user", tags=['User'])
def modify_user(user: User.modify):
    """
    Modify users information

    - **username** is unchangeable
    """
    modified = db.modify_user(user.username, user.id)
    if not modified:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        v2client.remove_user(email=user.username)
        v2client.add_user(email=user.username,
                          inbound_tag='VMESS_INBOUND',
                          account=VMessAccount(user.id))
    except v2errors.EmailNotFoundError:
        pass

    return user


@app.delete("/user", tags=['User'])
def remove_user(username: str = Body(..., embed=True)):
    """
    Remove a user
    """
    removed = db.remove_user(username)
    if not removed:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        v2client.remove_user(email=username)
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

    - **data**: must be in bytes, e.g. 1000000B = 1MB
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
