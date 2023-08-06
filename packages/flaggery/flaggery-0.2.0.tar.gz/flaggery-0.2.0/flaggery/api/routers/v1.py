from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from starlette import status

from flaggery.api import models
from flaggery.api.common import admin_route
from flaggery.api.dependencies import get_flaggery
from flaggery.api.settings import Settings
from flaggery.core import Flaggery

config = Settings()

router = APIRouter(prefix="/v1", tags=["v1"])


@router.get(
    "/subjects/{subject_id}/flags", response_model=models.GetSubjectFlagsResponse, status_code=status.HTTP_200_OK
)
def get_subject_flags(subject_id: int, flaggery: Flaggery = Depends(get_flaggery)):
    return {"flags": flaggery.get_subject_variants(subject_id)}


@router.get("/subjects/{subject_id}", response_model=models.GetSubjectResponse, status_code=status.HTTP_200_OK)
def get_subject(subject_id: int, flaggery: Flaggery = Depends(get_flaggery)):
    with flaggery.get_subject(subject_id) as sub:
        return models.GetSubjectResponse(
            id=sub.id, weight=sub.weight, bucket=sub.bucket_id, groups=[grp.name for grp in sub.groups]
        )


@admin_route(router)
@router.put("/buckets", response_model=models.IncreaseBucketsResponse, status_code=status.HTTP_200_OK)
def increase_buckets(amount: int, flaggery: Flaggery = Depends(get_flaggery)):
    ids = flaggery.increase_buckets(amount)
    return models.IncreaseBucketsResponse(bucket_ids=ids)


@admin_route(router)
@router.post("/subjects/{subject_id}", response_model=models.AddSubjectResponse, status_code=status.HTTP_201_CREATED)
def add_subject(subject_id: int, weight: int, flaggery: Flaggery = Depends(get_flaggery)):
    buck_id = flaggery.add_subject(subject_id, weight)
    return models.AddSubjectResponse(subject_id=subject_id, weight=weight, bucket_id=buck_id)


@admin_route(router)
@router.delete("/subjects/{subject_id}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def delete_subject(subject_id: int, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.rm_subject(subject_id)
    return models.Ok()


@admin_route(router)
@router.put("/subjects/{subject_id}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def set_subject_weight(subject_id: int, weight: int, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.set_subject_weight(subject_id, weight)
    return models.Ok()


@admin_route(router)
@router.post("/features/{feature}", response_model=models.Ok, status_code=status.HTTP_201_CREATED)
def add_feature(feature: str, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.add_feature(feature)
    return models.Ok()


@admin_route(router)
@router.delete("/features/{feature}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def delete_feature(feature: str, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.rm_feature(feature)
    return models.Ok()


@admin_route(router)
@router.post("/features/{feature}/disabling_variant", response_model=models.Ok, status_code=status.HTTP_201_CREATED)
def add_disabling_variant(feature: str, make_default: bool = False, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.add_disabling_variant(feature, make_default=make_default)
    return models.Ok()


@admin_route(router)
@router.post("/features/{feature}/variants/{variant}", response_model=models.Ok, status_code=status.HTTP_201_CREATED)
def add_variant(feature: str, variant: str, make_default: bool = False, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.add_variant(variant, feature, make_default=make_default)
    return models.Ok()


@admin_route(router)
@router.delete("/features/{feature}/variants/{variant}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def add_variant(feature: str, variant: str, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.rm_variant(variant, feature)
    return models.Ok()


@admin_route(router)
@router.get("/features/{feature}", response_model=models.GetFeatureResponse, status_code=status.HTTP_200_OK)
def get_feature(feature: str, flaggery: Flaggery = Depends(get_flaggery)):
    with flaggery.get_feature(feature) as feat:
        response = models.GetFeatureResponse(feature_name=feat.name, variants=[v.name for v in feat.variants])
        if feat.default_variant:
            response.default_variant = feat.default_variant.name
        return response


@admin_route(router)
@router.get("/features", response_model=models.GetFeaturesResponse, status_code=status.HTTP_200_OK)
def get_features(flaggery: Flaggery = Depends(get_flaggery)):
    return models.GetFeaturesResponse(features=flaggery.list_features())


@admin_route(router)
@router.put("/features/{feature}/default_variant/{variant}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def set_default_variant(feature: str, variant: str, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.set_default_feature_variant(feature, variant)
    return models.Ok()


@admin_route(router)
@router.post("/features/{feature}/rollout", response_model=models.Ok, status_code=status.HTTP_201_CREATED)
def add_rollout(feature: str, variant: str, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.add_rollout(variant, feature)
    return models.Ok()


@admin_route(router)
@router.get("/features/{feature}/rollout", response_model=models.GetRolloutResponse, status_code=status.HTTP_200_OK)
def get_rollout(feature: str, flaggery: Flaggery = Depends(get_flaggery)):
    with flaggery.get_rollout(feature) as roll:
        return models.GetRolloutResponse(
            feature=roll.feature.name,
            variant=roll.variant.name,
            proportion=roll.proportion,
            effective_weight=roll.weight,
            buckets=[b.id for b in roll.buckets],
        )


@admin_route(router)
@router.put("/features/{feature}/rollout", response_model=models.Ok, status_code=status.HTTP_200_OK)
def update_rollout(
    feature: str,
    proportion: Optional[float] = None,
    variant: Optional[str] = None,
    flaggery: Flaggery = Depends(get_flaggery),
):
    if variant:
        flaggery.set_rollout_variant(variant, feature)
    if proportion:
        flaggery.set_rollout_proportion(feature, proportion)
    return models.Ok()


@admin_route(router)
@router.get("/groups/{group}", response_model=models.GetGroupResponse, status_code=status.HTTP_200_OK)
def get_group(group: str, flaggery: Flaggery = Depends(get_flaggery)):
    with flaggery.get_group(group) as grp:
        return models.GetGroupResponse(
            group_name=grp.name,
            subjects=[sub.id for sub in grp.subjects],
            overrides={feat.name: var.name for feat, var in grp.variant_map.items()},
        )


@admin_route(router)
@router.post("/groups/{group}", response_model=models.Ok, status_code=status.HTTP_201_CREATED)
def add_group(group: str, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.add_group(group)
    return models.Ok()


@admin_route(router)
@router.post("/groups/{group}/subjects/{subject_id}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def add_subject_to_group(group: str, subject_id: int, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.add_subject_to_group(subject_id, group)
    return models.Ok()


@admin_route(router)
@router.delete("/groups/{group}/subjects/{subject_id}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def remove_subject_from_group(group: str, subject_id: int, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.rm_subject_from_group(subject_id, group)
    return models.Ok()


@admin_route(router)
@router.post("/groups/{group}/overrides/{feature}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def add_group_override(group: str, feature: str, variant: str, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.add_group_override(group, feature, variant)
    return models.Ok()


@admin_route(router)
@router.delete("/groups/{group}/overrides/{feature}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def remove_group_override(group: str, feature: str, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.rm_group_override(group, feature)
    return models.Ok()


@admin_route(router)
@router.delete("/groups/{group}", response_model=models.Ok, status_code=status.HTTP_200_OK)
def remove_group(group: str, flaggery: Flaggery = Depends(get_flaggery)):
    flaggery.rm_group(group)
    return models.Ok()


@admin_route(router)
@router.post(
    "/abtests",
    response_model=models.Ok,
    status_code=status.HTTP_201_CREATED,
    description="The field 'variants' is a mapping of feature names to respective variants.\n"
    "It determines which variant the group will adopt for each feature.\n"
    "To guarantee consistency throughout the test, all groups must affect the same features.",
)
def add_ab_test(add_abtest_req: models.AddAbTestRequest, flaggery: Flaggery = Depends(get_flaggery)):
    test = add_abtest_req.test
    flaggery.add_abtest(
        test_name=test.name,
        start=datetime.combine(test.start, datetime.min.time()),
        end=datetime.combine(test.end, datetime.min.time()),
        proportions=[grp.proportion for grp in test.groups],
        groups={grp.name: grp.variants for grp in test.groups},
    )
    return models.Ok()


@admin_route(router)
@router.get("/abtests/{test_name}", response_model=models.GetAbTestResponse, status_code=status.HTTP_200_OK)
def get_ab_test(test_name: str, flaggery: Flaggery = Depends(get_flaggery)):
    with flaggery.get_abtest(test_name) as test:
        return models.GetAbTestResponse(
            test=models.AbTest(
                name=test.name,
                start=test.start,
                end=test.end,
                groups=[
                    models.AbTestGroup(
                        name=group.name,
                        proportion=group.proportion,
                        variants={feat.name: var.name for feat, var in group.variant_map.items()},
                        buckets=[buck.id for buck in group.buckets],
                        effective_weight=group.weight,
                    )
                    for group in test.groups
                ],
            )
        )
