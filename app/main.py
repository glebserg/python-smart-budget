import uvicorn
from fastapi import FastAPI
from routes import users
from config import settings

app = FastAPI()
app.include_router(users.route)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)
