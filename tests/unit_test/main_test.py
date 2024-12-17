from fastapi.testclient import TestClient

from spacy_keyword_extraction_api.main import create_app


def test_read_main():
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200


def test_extract_keywords_endpoint_is_available():
    client = TestClient(create_app())
    response = client.get("/v1/extract-keywords", params={'text': 'some text'})
    assert response.status_code == 200
