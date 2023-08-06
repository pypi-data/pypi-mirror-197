from enum import Enum
from typing import List


class FailedToLoadPlugin(Exception):
    @classmethod
    def none_found(cls, plugin_group: str, plugin_name: str):
        return cls(f"No plugins found with name '{plugin_name}' in group '{plugin_group}'")

    @classmethod
    def multiple_found(cls, plugin_group: str, plugin_name: str):
        return cls(f"Multiple plugins found with name '{plugin_name}' in group '{plugin_group}'")


class GroupExists(Exception):
    pass


class GroupNotFound(Exception):
    pass


class FailedToAddBucket(Exception):
    pass


class BucketNotFound(Exception):
    pass


class AbTestNotFound(Exception):
    pass


class AbTestExists(Exception):
    pass


class SubjectAlreadyInGroup(Exception):
    def __init__(self, sub_id: int, group_name: str):
        super().__init__(f"Subject with id {sub_id} is already in group '{group_name}'")


class SubjectNotInGroup(Exception):
    def __init__(self, sub_id: int, group_name: str):
        super().__init__(f"Subject with id {sub_id} is not in group '{group_name}'")


class SubjectNotFound(Exception):
    pass


class SubjectExists(Exception):
    pass


class FeatureExists(Exception):
    pass


class FeatureNotFound(Exception):
    pass


class FeatureHasChildren(Exception):
    def __init__(self, feature_name: str, variant_names: List[str]):
        super().__init__(
            f"Cannot remove feature '{feature_name}' with child variant(s) "
            + ", ".join([f"'{v}'" for v in variant_names])
        )


class VariantExists(Exception):
    pass


class VariantNotFound(Exception):
    def __init__(self, variant_name: str, feature_name: str):
        super().__init__(f"No variant named '{variant_name}' for feature '{feature_name}'")


class VariantIsUsed(Exception):
    class Reason(Enum):
        ROLLOUT = 1
        AB_TEST = 2
        DEFAULT = 3
        GROUP = 4

    def __init__(self, message: str, reason: Reason):
        self.reason = reason
        super().__init__(message)

    @classmethod
    def in_abtest(cls, variant: str, feature: str, test: str):
        return cls(
            f"Cannot remove variant '{variant}' of feature '{feature}' used in the ab-test '{test}'", cls.Reason.AB_TEST
        )

    @classmethod
    def as_default(cls, variant: str, feature: str):
        return cls(f"Cannot remove default variant '{variant}' of feature '{feature}'", cls.Reason.DEFAULT)

    @classmethod
    def in_group(cls, variant: str, feature: str, group: str):
        return cls(
            f"Cannot remove variant '{variant}' of feature '{feature}' set as override in group '{group}'",
            cls.Reason.GROUP,
        )

    @classmethod
    def in_rollout(cls, variant: str, feature: str):
        return cls(f"Cannot remove rolled-out variant '{variant}' of feature '{feature}'", cls.Reason.ROLLOUT)


class RolloutExists(Exception):
    pass


class RolloutNotFound(Exception):
    def __init__(self, feature_name: str):
        super().__init__(f"No rollout found for feature '{feature_name}'")


class InvalidRolloutProportion(Exception):
    class Reason(Enum):
        RANGE = 1
        EQUAL = 2
        PRECISION = 3

    def __init__(self, message: str, reason: Reason):
        self.reason = reason
        super().__init__(message)

    @classmethod
    def range(cls, proportion: float):
        return cls(f"Rollout proportion must be between 0 and 1. Got {proportion}", cls.Reason.RANGE)

    @classmethod
    def equal(cls, proportion: float, feat_name: str):
        return cls(f"Rollout of feature '{feat_name}' is already at {round(proportion * 100)}%", cls.Reason.EQUAL)

    @classmethod
    def precision(cls, proportion: float):
        return cls(f"Rollout proportion must be a multiple of 5%. Got {proportion}", cls.Reason.PRECISION)


class NoBuckets(Exception):
    pass


class ValidationError(Exception):
    pass
