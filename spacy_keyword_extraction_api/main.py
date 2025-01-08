import logging
import os
import platform
from typing import Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import spacy

from spacy_keyword_extraction_api.api_router import create_api_router
from spacy_keyword_extraction_api.api_router_typing import KeywordsResponseMetaTypedDict
from spacy_keyword_extraction_api.extract_keywords import SpacyKeywordExtractor
from spacy_keyword_extraction_api.spacy_keyword import (
    DEFAULT_SPACY_LANGUAGE_MODEL_NAME,
    load_spacy_model
)


LOGGER = logging.getLogger(__name__)


class EnvironmentVariables:
    VCS_REF = 'VCS_REF'


def get_vcs_ref() -> Optional[str]:
    return os.getenv(EnvironmentVariables.VCS_REF)


def get_app_meta(
    spacy_language_model_name: str
) -> KeywordsResponseMetaTypedDict:
    meta: KeywordsResponseMetaTypedDict = {
        'spacy_version': spacy.__version__,
        'spacy_language_model_name': spacy_language_model_name,
        'python_version': platform.python_version()
    }
    vcf_ref = get_vcs_ref()
    if vcf_ref:
        meta['revision'] = vcf_ref
    return meta


def create_app():
    app = FastAPI()

    spacy_language_model_name = DEFAULT_SPACY_LANGUAGE_MODEL_NAME

    app.include_router(create_api_router(
        keyword_extractor=SpacyKeywordExtractor(
            language=load_spacy_model(spacy_language_model_name)
        ),
        meta=get_app_meta(
            spacy_language_model_name=spacy_language_model_name
        )
    ))

    app.mount('/', StaticFiles(directory='static', html=True), name='static')

    return app
