import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from spacy_keyword_extraction_api.api_router import create_api_router
from spacy_keyword_extraction_api.extract_keywords import SimpleKeywordExtractor


LOGGER = logging.getLogger(__name__)


def create_app():
    app = FastAPI()

    app.include_router(create_api_router(keyword_extractor=SimpleKeywordExtractor()))

    app.mount('/', StaticFiles(directory='static', html=True), name='static')

    return app
