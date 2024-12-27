import logging
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest

from spacy_keyword_extraction_api.api_router import (
    create_api_router,
    get_keyword_response_dict_list
)
from spacy_keyword_extraction_api.api_router_typing import (
    BatchExtractKeywordsRequestTypedDict,
    BatchKeywordsResponseTypedDict
)
from spacy_keyword_extraction_api.extract_keywords import KeywordExtractor, SimpleKeywordExtractor


LOGGER = logging.getLogger(__name__)


TEXT_1 = 'Some Text'


@pytest.fixture(name='keyword_extractor')
def _keyword_extractor():
    return SimpleKeywordExtractor()


def create_test_client(keyword_extractor: KeywordExtractor):
    app = FastAPI()
    app.include_router(create_api_router(keyword_extractor=keyword_extractor))
    client = TestClient(app)
    return client


class TestGetKeywordResponseDictList:
    def test_should_return_dict_list(self):
        assert (
            get_keyword_response_dict_list(['keyword_1', 'keyword_2'])
            == [{
                'keyword': 'keyword_1'
            }, {
                'keyword': 'keyword_2'
            }]
        )


class TestExtractKeyword:
    def test_should_return_extracted_keywords(
        self,
        keyword_extractor: KeywordExtractor
    ):
        client = create_test_client(keyword_extractor=keyword_extractor)
        response = client.get('/v1/extract-keywords', params={'text': TEXT_1})
        assert response.json() == {
            'keywords': keyword_extractor.get_extracted_keywords_for_text(TEXT_1)
        }

    def test_should_return_batch_extracted_keywords(
        self,
        keyword_extractor: KeywordExtractor
    ):
        request_json: BatchExtractKeywordsRequestTypedDict = {
            'data': [{
                'type': 'extract-keyword-request',
                'attributes': {
                    'content': TEXT_1
                }
            }]
        }
        expected_response_json: BatchKeywordsResponseTypedDict = {
            'data': [{
                'type': 'extract-keyword-result',
                'attributes': {
                    'keywords': get_keyword_response_dict_list(
                        keyword_extractor.get_extracted_keywords_for_text(TEXT_1)
                    )
                }
            }]
        }
        client = create_test_client(keyword_extractor=keyword_extractor)
        response = client.post('/v1/batch-extract-keywords', json=request_json)
        response.raise_for_status()
        actual_response_json = response.json()
        LOGGER.debug('actual_response_json: %r', actual_response_json)
        assert actual_response_json == expected_response_json

    def test_should_return_passed_in_id(
        self,
        keyword_extractor: KeywordExtractor
    ):
        request_json: BatchExtractKeywordsRequestTypedDict = {
            'data': [{
                'type': 'extract-keyword-request',
                'id': 'doc-1',
                'attributes': {
                    'content': TEXT_1
                }
            }]
        }
        expected_response_json: BatchKeywordsResponseTypedDict = {
            'data': [{
                'type': 'extract-keyword-result',
                'id': 'doc-1',
                'attributes': {
                    'keywords': get_keyword_response_dict_list(
                        keyword_extractor.get_extracted_keywords_for_text(TEXT_1)
                    )
                }
            }]
        }
        client = create_test_client(keyword_extractor=keyword_extractor)
        response = client.post('/v1/batch-extract-keywords', json=request_json)
        response.raise_for_status()
        actual_response_json = response.json()
        LOGGER.debug('actual_response_json: %r', actual_response_json)
        assert actual_response_json == expected_response_json

    def test_should_return_meta_from_request(
        self,
        keyword_extractor: KeywordExtractor
    ):
        request_json: BatchExtractKeywordsRequestTypedDict = {
            'data': [{
                'type': 'extract-keyword-request',
                'id': 'doc-1',
                'attributes': {
                    'content': TEXT_1
                },
                'meta': {
                    'version_id': 'v1'
                }
            }]
        }
        expected_response_json: BatchKeywordsResponseTypedDict = {
            'data': [{
                'type': 'extract-keyword-result',
                'id': 'doc-1',
                'attributes': {
                    'keywords': get_keyword_response_dict_list(
                        keyword_extractor.get_extracted_keywords_for_text(TEXT_1)
                    )
                },
                'meta': {
                    'version_id': 'v1'
                }
            }]
        }
        client = create_test_client(keyword_extractor=keyword_extractor)
        response = client.post('/v1/batch-extract-keywords', json=request_json)
        response.raise_for_status()
        actual_response_json = response.json()
        LOGGER.debug('actual_response_json: %r', actual_response_json)
        assert actual_response_json == expected_response_json
