from typing import Any, Literal, Mapping, Sequence
from typing_extensions import NotRequired, TypedDict


class KeywordsRequestAttributesTypedDict(TypedDict):
    content: str


class KeywordsRequestDataTypedDict(TypedDict):
    type: Literal['extract-keyword-request']
    attributes: KeywordsRequestAttributesTypedDict
    id: NotRequired[str]
    meta: NotRequired[Mapping[str, Any]]


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
    meta: NotRequired[Mapping[str, Any]]


class KeywordsResponseMetaTypedDict(TypedDict):
    spacy_version: NotRequired[str]
    spacy_language_model_name: NotRequired[str]


class BatchKeywordsResponseTypedDict(TypedDict):
    data: Sequence[KeywordsResponseDataTypedDict]
    meta: NotRequired[KeywordsResponseMetaTypedDict]
