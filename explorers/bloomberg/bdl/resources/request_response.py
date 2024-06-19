from typing import List

from pydantic import BaseModel


class ContentMember(BaseModel):
    key: str
    headers: dict
    metadata: dict


class ContentPaginatedView(BaseModel):
    next: str


class RequestResponseView(BaseModel):
    contains: List[ContentMember]
    view: ContentPaginatedView
