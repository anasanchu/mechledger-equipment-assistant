"""FastAPI application entrypoint for MECHLEDGER.

Configures middleware, registers routes, and starts the server via Uvicorn.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from config.settings import API_HOST, API_PORT


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    app = FastAPI(title="MECHLEDGER API", description="Industrial knowledge and evidence-led diagnostics")

    # Enable CORS for the React frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
