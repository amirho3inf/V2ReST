# interval and scheduled jobs

from . import v2ray, scheduler, redis, database as db
from v2api import errors as v2errors
import traceback
import config


SYNC_USAGE_P = config.SYNC_USER_USAGE_PERIOD_SEC
RESET_HOUR = config.RESET_V2RAY_HOUR_DAILY
TZ = config.SCHEDULER_TIMEZONE


def _deactive_user(username: str) -> None:
    """
    Remove user from v2ray server
    It will call by an interval jobs that checks users usage when doesn't have an active plan

    :param username:
    """
    if redis.get(f"deactivate_try:{username}"):
        return
    try:
        v2ray.client.remove_user(email=username, inbound_tag="VMESS_INBOUND")
    except v2errors.EmailNotFoundError:
        pass
    except Exception:
        traceback.print_exc()
    redis.setex(f"deactivate_try:{username}", time=60, value=1)


def record_users_usage():
    """
    An interval job that checks users data usage and record that to the database
    """
    for data in v2ray.client.get_all_traffic_stats(reset=True):
        username = data['email']
        by = data['value']
        if by == 0:
            continue
        if db.decr_user_data(username, by) <= 0:
            # User data is over
            _deactive_user(username)


scheduler.add_job(record_users_usage, 'interval', seconds=SYNC_USAGE_P)


def restart_v2ray():
    """
    An interval job that restarts v2ray server every day at an exact hour
    """
    v2ray.process.stop()
    v2ray.process.start(v2ray.generate_db_config())


scheduler.add_job(restart_v2ray, 'cron', hour=RESET_HOUR, timezone=TZ)
