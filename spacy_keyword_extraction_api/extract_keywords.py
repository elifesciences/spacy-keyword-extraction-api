import logging
from abc import ABC, abstractmethod
import re
from typing import Iterable, List, Sequence

from spacy.language import Language

from spacy_keyword_extraction_api.spacy_keyword import SpacyKeywordDocumentParser

LOGGER = logging.getLogger(__name__)


class KeywordExtractor(ABC):
    @abstractmethod
    def iter_extract_keywords(self, text_list: Iterable[str]) -> Iterable[List[str]]:
        pass

    def get_extracted_keywords_for_text(self, text: str) -> Sequence[str]:
        return list(self.iter_extract_keywords(text_list=[text]))[0]


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


class SpacyKeywordExtractor(KeywordExtractor):
    def __init__(self, language: Language):
        self.parser = SpacyKeywordDocumentParser(language)

    def iter_extract_keywords(
            self, text_list: Iterable[str]) -> Iterable[List[str]]:
        return (
            document.get_keyword_str_list()
            for document in self.parser.iter_parse_text_list(text_list)
        )
