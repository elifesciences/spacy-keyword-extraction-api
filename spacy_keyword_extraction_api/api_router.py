import logging

from fastapi import APIRouter


LOGGER = logging.getLogger(__name__)


def create_api_router() -> APIRouter:
    router = APIRouter()

    @router.get("/v1/extract-keywords")
    def extract_keywords(text: str):
        return text.split()

    return router
