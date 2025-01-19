import uvicorn
import fastapi
from src.api.auth import auth_router
from src.api.lessons import lessons_router

app = fastapi.FastAPI()
app.include_router(auth_router)
app.include_router(lessons_router)



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
