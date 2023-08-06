from datetime import date
from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class Ok(BaseModel):
    success: bool = True


class GetFeatureResponse(BaseModel):
    feature_name: str
    variants: List[str]
    default_variant: Optional[str] = None


class GetRolloutResponse(BaseModel):
    feature: str
    variant: str
    proportion: float
    effective_weight: int
    buckets: List[int]


class GetFeaturesResponse(BaseModel):
    features: List[str]


class IncreaseBucketsResponse(BaseModel):
    bucket_ids: List[int]


class AddSubjectResponse(BaseModel):
    subject_id: int
    weight: int
    bucket_id: int


class AbTestGroupSpec(BaseModel):
    name: str
    proportion: float
    variants: Dict[str, str] = Field(default_factory=lambda: dict())


class AddAbTestRequest(BaseModel):
    name: str
    start: date
    end: date
    groups: List[AbTestGroupSpec]


class GetSubjectFlagsResponse(BaseModel):
    flags: Dict[str, str]
