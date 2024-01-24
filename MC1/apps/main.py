from fastapi import FastAPI

from routers import router

app = FastAPI(
    title="MC1"
)

app.include_router(router)
