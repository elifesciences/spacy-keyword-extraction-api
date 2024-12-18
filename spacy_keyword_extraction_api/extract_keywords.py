import logging
from abc import ABC, abstractmethod
import re
from typing import Iterable, List

LOGGER = logging.getLogger(__name__)


class KeywordExtractor(ABC):
    @abstractmethod
    def iter_extract_keywords(self, text_list: Iterable[str]) -> Iterable[List[str]]:
        pass


def simple_regex_keyword_extraction(
        text: str,
        regex_pattern=r"([a-z](?:\w|-)+)"
):
    return re.findall(regex_pattern, text.lower())


class SimpleKeywordExtractor(KeywordExtractor):
    def iter_extract_keywords(self, text_list: Iterable[str]) -> Iterable[List[str]]:
        return (
            simple_regex_keyword_extraction(text)
            for text in text_list
        )
