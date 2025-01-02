import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import spacy

from spacy_keyword_extraction_api.api_router import create_api_router
from spacy_keyword_extraction_api.extract_keywords import SpacyKeywordExtractor
from spacy_keyword_extraction_api.spacy_keyword import (
    DEFAULT_SPACY_LANGUAGE_MODEL_NAME,
    load_spacy_model
)


LOGGER = logging.getLogger(__name__)


def create_app():
    app = FastAPI()

    spacy_language_model_name = DEFAULT_SPACY_LANGUAGE_MODEL_NAME

    app.include_router(create_api_router(
        keyword_extractor=SpacyKeywordExtractor(
            language=load_spacy_model(spacy_language_model_name)
        ),
        meta={
            'spacy_version': spacy.__version__,
            'spacy_language_model_name': spacy_language_model_name
        }
    ))

    app.mount('/', StaticFiles(directory='static', html=True), name='static')

    return app
