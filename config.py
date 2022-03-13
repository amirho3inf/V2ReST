from decouple import config


# Redis server settings
# Redis is used as the main database, make sure redis auto save is enabled
# And don't forget to take backup from dump file
# https://redis.io/topics/persistence
REDIS_URL = config('REDIS_URL', default='redis://localhost/0')

# V2ray server settings
V2RAY_HOST = config('V2RAY_HOST', default='0.0.0.0')
V2RAY_PORT = config('V2RAY_PORT', default=10086, cast=int)
V2RAY_LOCATION_BIN = config('V2RAY_LOCATION_BIN', default='/usr/bin/v2ray')
V2RAY_LOCATION_ASSET = config('V2RAY_LOCATION_ASSET', default='/usr/share/v2ray')
V2RAY_API_HOST = config('V2RAY_API_HOST', default='127.0.0.1')
V2RAY_API_PORT = config('V2RAY_API_PORT', default=12121, cast=int)

# Jobs settings
# Set SYNC_USER_USAGE_PERIOD_SEC in seconds
# For a job that syncs v2ray stats with redis server
SYNC_USER_USAGE_PERIOD_SEC = config('SYNC_USER_USAGE_PERIOD_SEC', default=30, cast=int)
# Set an hour to RESET_V2RAY_HOUR_DAILY between [0-23]
# For a job that restarts v2ray server at the hour
# Default: 04:00 AM, when users are sleeping!
RESET_V2RAY_HOUR_DAILY = config('RESET_V2RAY_HOUR_DAILY', default=4, cast=int)
SCHEDULER_TIMEZONE = config('SCHEDULER_TIMEZONE', default='Asia/Tehran')
