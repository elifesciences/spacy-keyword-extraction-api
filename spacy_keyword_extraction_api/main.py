import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


LOGGER = logging.getLogger(__name__)


def create_app():
    app = FastAPI()

    app = FastAPI(docs_url=None, redoc_url=None)
    app.mount('/', StaticFiles(directory='static', html=True), name='static')

    return app