import uvicorn
from fastapi import FastAPI

from auth.routers import router as auth_router
from config import Settings


app = FastAPI(title="FastapiAuth",
              docs_url=f"/{Settings.config_url}/docs",
              redoc_url=f"/{Settings.config_url}/redoc")


app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=Settings.HOST, port=Settings.PORT)
