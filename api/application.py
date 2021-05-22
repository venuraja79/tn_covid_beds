import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from api.controller.http_error import http_error_handler
from api.controller.router import router as api_router

from config import (LOG_LEVEL)

logging.basicConfig(format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(LOG_LEVEL)

def get_application() -> FastAPI:
    application = FastAPI(title="TN Covid Beds Data", debug=True, version="0.1")

    application.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)

    application.include_router(api_router)

    return application

# gunicorn api.application:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -t 300
app = get_application()

logger.info("Open http://127.0.0.1:8000/docs to see Swagger API Documentation.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)