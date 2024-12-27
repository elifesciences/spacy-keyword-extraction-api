import logging
from typing import Sequence
from typing_extensions import TypedDict

from fastapi import APIRouter, Body

from spacy_keyword_extraction_api.api_router_typing import (
    BatchExtractKeywordsRequestTypedDict,
    BatchKeywordsResponseTypedDict,
    KeywordsResponseDataTypedDict
)
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

    @router.post("/v1/batch-extract-keywords")
    def batch_extract_keywords(
        batch_extract_keywords_request: BatchExtractKeywordsRequestTypedDict = Body()
    ) -> BatchKeywordsResponseTypedDict:
        text_list = [
            extract_keywords_request['attributes']['content']
            for extract_keywords_request in batch_extract_keywords_request['data']
        ]
        extraction_result_data_list: Sequence[KeywordsResponseDataTypedDict] = [
            {
                'type': 'extract-keyword-result',
                'attributes': {
                    'keywords': [
                        {
                            'keyword': keyword
                        }
                        for keyword in keywords
                    ]
                }
            }
            for keywords in keyword_extractor.iter_extract_keywords(text_list=text_list)
        ]
        return {
            'data': extraction_result_data_list
        }

    return router
