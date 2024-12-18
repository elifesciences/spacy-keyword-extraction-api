import logging
from typing import Sequence

from fastapi import APIRouter

from spacy_keyword_extraction_api.extract_keywords import KeywordExtractor


LOGGER = logging.getLogger(__name__)


def create_api_router(keyword_extractor: KeywordExtractor) -> APIRouter:
    router = APIRouter()

    @router.get("/v1/extract-keywords")
    def extract_keywords(text: str) -> Sequence[str]:
        return list(keyword_extractor.iter_extract_keywords(text_list=[text]))[0]

    return router
