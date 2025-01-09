from collections import Counter
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


EXAMPLE_BATCH_EXTRACT_KEYWORDS_REQUEST: BatchExtractKeywordsRequestTypedDict = {
    'data': [{
        'type': 'extract-keyword-request',
        'id': 'doc-1',
        'attributes': {
            'content': 'I am interested in biochemistry and neuroscience.'
        },
        'meta': {
            'extra_id': 'doc-1/v1'
        }
    }]
}

EXAMPLE_BATCH_KEYWORDS_RESPONSE: BatchKeywordsResponseTypedDict = {
    'data': [{
        'type': 'extract-keyword-result',
        'attributes': {
            'keywords': [{
                'keyword': 'biochemistry',
                'count': 1
            }, {
                'keyword': 'neuroscience',
                'count': 1
            }]
        },
        'id': 'doc-1',
        'meta': {
            'extra_id': 'doc-1/v1'
        }
    }],
    'meta': {
        'spacy_version': '2.2.4',
        'spacy_language_model_name': 'en_core_web_lg'
    }
}

EXAMPLE_BATCH_KEYWORDS_RESPONSES_BY_STATUS_CODE_DICT: dict = {
    200: {
        'description': 'Successful keyword extraction',
        'content': {
            'application/json': {
                'example': EXAMPLE_BATCH_KEYWORDS_RESPONSE
            }
        }
    }
}


class KeywordsResponseTypedDict(TypedDict):
    keywords: Sequence[str]


def get_keyword_response_dict_list(
    keywords: Sequence[str]
) -> Sequence[KeywordsResponseKeywordTypedDict]:
    return [
        {
            'keyword': keyword,
            'count': count
        }
        for keyword, count in Counter(keywords).items()
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

    @router.post(
        '/v1/batch-extract-keywords',
        responses=EXAMPLE_BATCH_KEYWORDS_RESPONSES_BY_STATUS_CODE_DICT
    )
    def batch_extract_keywords(
        batch_extract_keywords_request: BatchExtractKeywordsRequestTypedDict = Body(
            examples=[EXAMPLE_BATCH_EXTRACT_KEYWORDS_REQUEST]
        )
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
