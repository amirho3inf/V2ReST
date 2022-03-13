from fastapi import FastAPI
from fastapi_responses import custom_openapi
from apscheduler.schedulers.background import BackgroundScheduler
from redis import StrictRedis
import config


app = FastAPI()
app.openapi = custom_openapi(app)
scheduler = BackgroundScheduler()
redis = StrictRedis.from_url(config.REDIS_URL, decode_responses=True)

from . import views, jobs  # noqa

scheduler.start()
