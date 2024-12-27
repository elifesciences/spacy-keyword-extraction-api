from typing import Literal, Sequence
from typing_extensions import NotRequired, TypedDict


class KeywordsRequestAttributesTypedDict(TypedDict):
    content: str


class KeywordsRequestDataTypedDict(TypedDict):
    type: Literal['extract-keyword-request']
    attributes: KeywordsRequestAttributesTypedDict
    id: NotRequired[str]


class BatchExtractKeywordsRequestTypedDict(TypedDict):
    data: Sequence[KeywordsRequestDataTypedDict]


class KeywordsResponseKeywordTypedDict(TypedDict):
    keyword: str


class KeywordsResponseAttributesTypedDict(TypedDict):
    keywords: Sequence[KeywordsResponseKeywordTypedDict]


class KeywordsResponseDataTypedDict(TypedDict):
    type: Literal['extract-keyword-result']
    attributes: KeywordsResponseAttributesTypedDict
    id: NotRequired[str]


class BatchKeywordsResponseTypedDict(TypedDict):
    data: Sequence[KeywordsResponseDataTypedDict]
