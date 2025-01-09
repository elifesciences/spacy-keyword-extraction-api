from fastapi.testclient import TestClient

from spacy_keyword_extraction_api.main import EnvironmentVariables, create_app, get_app_meta


class TestGetAppMeta:
    def test_should_return_language_model(self):
        meta = get_app_meta(
            spacy_language_model_name='model_1'
        )
        assert meta['spacy_language_model_name'] == 'model_1'

    def test_should_not_return_revision_if_unknown(self, mock_env: dict):
        assert EnvironmentVariables.VCS_REF not in mock_env
        meta = get_app_meta(
            spacy_language_model_name='model_1'
        )
        assert 'revision' not in meta

    def test_should_return_revision(self, mock_env: dict):
        mock_env[EnvironmentVariables.VCS_REF] = 'commit_1'
        meta = get_app_meta(
            spacy_language_model_name='model_1'
        )
        assert meta['revision'] == 'commit_1'


def test_read_main():
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200
