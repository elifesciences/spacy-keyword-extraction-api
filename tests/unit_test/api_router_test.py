from fastapi.testclient import TestClient
from fastapi import FastAPI

from spacy_keyword_extraction_api.api_router import create_api_router
from spacy_keyword_extraction_api.extract_keywords import SimpleKeywordExtractor


def create_test_client():
    app = FastAPI()
    app.include_router(create_api_router(keyword_extractor=SimpleKeywordExtractor()))
    client = TestClient(app)
    return client


class TestExtractKeyword:
    def test_should_return_keywords_in_lower_case(self):
        client = create_test_client()
        response = client.get('/v1/extract-keywords', params={'text': 'Some Text'})
        assert response.json() == ['some', 'text']
