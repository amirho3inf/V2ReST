from . import redis
from typing import Union, Iterator
from uuid import UUID


global _REDIS_CURSOR
_REDIS_CURSOR = 0


def _get_user_plan_keys(username: str) -> list:
    """
    Get the redis key of user active plans

    :param username:
    :return: List of redis keys
    """
    global _REDIS_CURSOR
    _REDIS_CURSOR, plan_keys = redis.scan(
        cursor=_REDIS_CURSOR,
        match=f'vmess:user:{username}:*')
    return plan_keys


def add_user(username: str, id: Union[str, UUID]) -> bool:
    """
    Add a vmess user to redis

    :param username:
    :param id:
    :return:
    """
    if user_exists(username):
        return False
    redis.hset("vmess:users", username, str(id))
    return True


def modify_user(username: str, id: Union[str, UUID]) -> bool:
    """
    Modify a vmess user ID with it's username

    :param username:
    :param id:
    :return:
    """
    if not user_exists(username):
        return False
    redis.hset("vmess:users", username, str(id))
    return True


def remove_user(username: str) -> bool:
    """
    Remove a vmess user

    :param username:
    :return:
    """
    if not user_exists(username):
        return False
    redis.hdel("vmess:users", username)
    # remove user activate plans
    for k in _get_user_plan_keys(username):
        redis.delete(k)
    return True


def get_user(username: str) -> Union[dict, None]:
    """
    Get a vmess user data

    :param username:
    :return:
    :rtype: Union[dict, None]
    """
    if not (id := redis.hget("vmess:users", username)):
        return

    plans = []
    for k in _get_user_plan_keys(username):
        n = int(k[-1].split(":")[-1])
        ttl = redis.ttl(k)
        data = int(redis.get(k) or 0)
        plans.append({
            "pid": n,
            "data": data if data > 0 else 0,
            "ttl": ttl if ttl > 0 else 0
        })

    return {
        "username": username,
        "id": id,
        "plans": plans
    }


def user_has_active_plan(username: str) -> bool:
    """
    Check if user has a active plan or not

    :param username:
    :return:
    """
    return bool(_get_user_plan_keys(username))


def user_exists(username: str) -> bool:
    """
    Check if user exists or not

    :param username:
    :return:
    """
    return bool(redis.hget("vmess:users", username))


def get_users(only_active_users=False) -> Iterator[dict]:
    """
    Get all vmess users

    :param username:
    :param only_active_users: Filter users who don't have active plan
    :return: All users username and id
    :rtype: Iterator[dict]
    """
    for username, id in redis.hgetall("vmess:users").items():
        if not only_active_users or user_has_active_plan(username):
            yield {
                "username": username,
                "id": id
            }


def decr_user_data(username: str, by: int) -> int:
    """
    Decrease the remaining data of the user current active plan 

    :param username:
    :param by: The amount of decrease
    :return: The remaining data of active plan
    """
    plan_keys = sorted(_get_user_plan_keys(username),
                       key=lambda i: int(i.rsplit(":", 1)[-1]))

    # just do on first plan
    for p in plan_keys:
        n = redis.decrby(p, by)
        if n > 0:
            return n
        else:
            redis.delete(p)
            return 1

    # there's no plan
    return 0


def add_plan(username: str, data: int, ttl: int) -> bool:
    """
    Add a new plan for a vmess user

    :param username:
    :param data: The amount of plan data in bytes
    :param ttl: Time to live in seconds
    :return: False if user doesn't exist else True
    """
    if not redis.hget("vmess:users", username):
        return False

    if k := _get_user_plan_keys(username):
        plan_n = int(k[-1].split(":")[-1]) + 1
    else:
        plan_n = 0
    redis.setex(f"vmess:user:{username}:{plan_n}", value=data, time=ttl)
    return True
