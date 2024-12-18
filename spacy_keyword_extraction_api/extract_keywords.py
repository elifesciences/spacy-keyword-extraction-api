import logging
from abc import ABC, abstractmethod
from typing import Iterable, List

LOGGER = logging.getLogger(__name__)


class KeywordExtractor(ABC):
    @abstractmethod
    def iter_extract_keywords(self, text_list: Iterable[str]) -> Iterable[List[str]]:
        pass


class SimpleKeywordExtractor(KeywordExtractor):
    def iter_extract_keywords(self, text_list: Iterable[str]) -> Iterable[List[str]]:
        return (
            text.split()
            for text in text_list
        )
