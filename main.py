import os
import aioredis
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware
from dependency_injector.wiring import inject

from core.redis.containers import Container
from core.db import database
from user.schemas import UserLogin, TokenSchema
from user import services
from utils.jwt.auth_handler import signJWT

app = FastAPI()
app.state.database = database

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    """The function is executed when turned on server"""
    # Redis create connection
    redis_host = os.environ.get('REDIS_HOST')
    redis_pass = os.environ.get('REDIS_PASSWORD')
    redis = await aioredis.create_redis(f"redis://{redis_host}", password=redis_pass)
    await FastAPILimiter.init(redis)
    # Postgres database connect
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    """The function is executed when switched off server"""
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    """Redirect from '/' path to '/docs'"""
    return RedirectResponse(url='/docs')


@app.post('/signin',
          dependencies=[Depends(RateLimiter(times=3, seconds=60))],
          summary="Create access and refresh tokens for user",
          response_model=TokenSchema
          )
@inject
async def login(data: UserLogin):
    """
    Login user

    :param data: class 'user.schemas.UserLogin', parameters: phone: str, password: str
    :return: object
    """
    user = await services.check_user(data)
    if user:
        return {'status': 'success', 'token': signJWT(user.phone), 'data': user}


container = Container()
container.config.redis_host.from_env("REDIS_HOST", "redis")
container.config.redis_password.from_env("REDIS_PASSWORD", "password")
container.wire(modules=[__name__])
