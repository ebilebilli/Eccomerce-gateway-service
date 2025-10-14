from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ShopListItem(BaseModel):
    id: str
    name: str
    slug: Optional[str]
    profile_url: Optional[str]
    is_verified: bool
    about: Optional[str]


class ShopBranch(BaseModel):
    id: int
    name: str
    slug: Optional[str]
    about: Optional[str]
    phone_number: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    is_active: Optional[bool]


class ShopMedia(BaseModel):
    id: int
    image_url: str
    alt_text: Optional[str]
    created_at: Optional[datetime]


class ShopSocialMedia(BaseModel):
    id: int
    media_name: str
    media_url: str


class ShopComment(BaseModel):
    id: int
    user_id: Optional[str]
    text: Optional[str]
    rating: Optional[int]
    created_at: Optional[datetime]


class ShopDetail(ShopListItem):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    branches: Optional[List[ShopBranch]] = None
    media: Optional[List[ShopMedia]] = None
    social_medias: Optional[List[ShopSocialMedia]] = None


class ShopCreateRequest(BaseModel):
    name: str
    about: Optional[str]


class ShopUpdateRequest(BaseModel):
    name: Optional[str]
    about: Optional[str]


class BranchCreateRequest(BaseModel):
    name: str
    about: Optional[str]
    phone_number: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


class CommentCreateRequest(BaseModel):
    text: Optional[str]
    rating: Optional[int]


class SocialMediaCreateRequest(BaseModel):
    media_name: str
    media_url: str
