import logging
from typing import Optional, Sequence
from typing_extensions import TypedDict

from fastapi import APIRouter, Body

from spacy_keyword_extraction_api.api_router_typing import (
    BatchExtractKeywordsRequestTypedDict,
    BatchKeywordsResponseTypedDict,
    KeywordsRequestDataTypedDict,
    KeywordsResponseDataTypedDict,
    KeywordsResponseKeywordTypedDict,
    KeywordsResponseMetaTypedDict
)
from spacy_keyword_extraction_api.extract_keywords import KeywordExtractor


LOGGER = logging.getLogger(__name__)


class KeywordsResponseTypedDict(TypedDict):
    keywords: Sequence[str]


def get_keyword_response_dict_list(
    keywords: Sequence[str]
) -> Sequence[KeywordsResponseKeywordTypedDict]:
    return [
        {
            'keyword': keyword
        }
        for keyword in keywords
    ]


def get_keyword_response_data(
    keywords: Sequence[str],
    extract_keyword_request: KeywordsRequestDataTypedDict
) -> KeywordsResponseDataTypedDict:
    result: KeywordsResponseDataTypedDict = {
        'type': 'extract-keyword-result',
        'attributes': {
            'keywords': get_keyword_response_dict_list(keywords)
        }
    }
    if extract_keyword_request.get('id'):
        result['id'] = extract_keyword_request['id']
    if extract_keyword_request.get('meta'):
        result['meta'] = extract_keyword_request['meta']
    return result


def create_api_router(
    keyword_extractor: KeywordExtractor,
    meta: Optional[KeywordsResponseMetaTypedDict] = None
) -> APIRouter:
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
        extract_keywords_request_list = batch_extract_keywords_request['data']
        text_list = [
            extract_keywords_request['attributes']['content']
            for extract_keywords_request in extract_keywords_request_list
        ]
        keywords_list = list(keyword_extractor.iter_extract_keywords(text_list=text_list))
        assert len(text_list) == len(extract_keywords_request_list)
        extraction_result_data_list: Sequence[KeywordsResponseDataTypedDict] = [
            get_keyword_response_data(
                keywords=keywords,
                extract_keyword_request=extract_keywords_request
            )
            for keywords, extract_keywords_request in zip(
                keywords_list, extract_keywords_request_list
            )
        ]
        response_json: BatchKeywordsResponseTypedDict = {
            'data': extraction_result_data_list
        }
        if meta:
            response_json['meta'] = meta
        return response_json

    return router
