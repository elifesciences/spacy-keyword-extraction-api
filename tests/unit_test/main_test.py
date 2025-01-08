from fastapi.testclient import TestClient

from spacy_keyword_extraction_api.main import create_app, get_app_meta


class TestGetAppMeta:
    def test_should_return_language_model(self):
        meta = get_app_meta(
            spacy_language_model_name='model_1'
        )
        assert meta['spacy_language_model_name'] == 'model_1'


def test_read_main():
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200


def test_extract_keywords_endpoint_is_available():
    client = TestClient(create_app())
    response = client.get("/v1/extract-keywords", params={'text': 'some text'})
    assert response.status_code == 200
