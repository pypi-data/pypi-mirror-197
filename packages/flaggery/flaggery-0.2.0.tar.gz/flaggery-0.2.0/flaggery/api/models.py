from datetime import date
from typing import List, Dict, Optional

from pydantic import BaseModel, Field  # pylint: disable=E0611


class Ok(BaseModel):
    success: bool = True


class GetGroupResponse(BaseModel):
    group_name: str
    subjects: List[int]
    overrides: Dict[str, str]


class GetSubjectResponse(BaseModel):
    id: int
    weight: int
    bucket: int
    groups: List[str]


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


class AbTestGroup(BaseModel):
    name: str
    proportion: float
    variants: Dict[str, str] = Field(default_factory=dict)
    buckets: List[int] = Field(default_factory=list)
    effective_weight: Optional[int] = None


class AbTest(BaseModel):
    name: str
    start: date
    end: date
    groups: List[AbTestGroup]


class AddAbTestRequest(BaseModel):
    test: AbTest


class GetAbTestResponse(BaseModel):
    test: AbTest


class GetSubjectFlagsResponse(BaseModel):
    flags: Dict[str, str]
