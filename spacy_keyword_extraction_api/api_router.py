import logging
from typing import Sequence
from typing_extensions import TypedDict

from fastapi import APIRouter

from spacy_keyword_extraction_api.extract_keywords import KeywordExtractor


LOGGER = logging.getLogger(__name__)


class KeywordsResponseTypedDict(TypedDict):
    keywords: Sequence[str]


def create_api_router(keyword_extractor: KeywordExtractor) -> APIRouter:
    router = APIRouter()

    @router.get("/v1/extract-keywords")
    def extract_keywords(text: str) -> KeywordsResponseTypedDict:
        return {
            'keywords': keyword_extractor.get_extracted_keywords_for_text(text)
        }

    return router
