from module.SINGLETONE import MainInstance
#
from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# Fast 서버 구동
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

# Main Instance 생성
Main_Instance = MainInstance.get_instance()

# Lazy Import Router
from controller.route import router

app.include_router(router, prefix='', tags=['search'])