from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest

from spacy_keyword_extraction_api.api_router import create_api_router
from spacy_keyword_extraction_api.extract_keywords import KeywordExtractor, SimpleKeywordExtractor


TEXT_1 = 'Some Text'


@pytest.fixture(name='keyword_extractor')
def _keyword_extractor():
    return SimpleKeywordExtractor()


def create_test_client(keyword_extractor: KeywordExtractor):
    app = FastAPI()
    app.include_router(create_api_router(keyword_extractor=keyword_extractor))
    client = TestClient(app)
    return client


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
