from module.SINGLETONE import MainInstance
#
from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# Fast 서버 구동
app = FastAPI()



@app.on_event('startup')
async def startup_event():
    app.mount('/static', StaticFiles(directory='static'), name='static')

    global templates
    templates = Jinja2Templates(directory='templates')

    # Main Instance 생성
    global Main_Instance
    Main_Instance = MainInstance.get_instance()

    # Lazy Import Router
    from controller.route import router
    app.include_router(router, prefix='', tags=['search'])

# 서버 시작 시 이벤트 핸들러 호출
app.add_event_handler('startup', startup_event)

# 서버 실행 코드
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)