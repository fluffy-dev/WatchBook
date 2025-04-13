from fastapi import FastAPI

from src.api.routes import router


def get_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router)

    @app.get("/")
    def root():
        return {"message": "Hello World"}

    @app.get("/health")
    def health():
        return {"message": "healthy"}

    return app