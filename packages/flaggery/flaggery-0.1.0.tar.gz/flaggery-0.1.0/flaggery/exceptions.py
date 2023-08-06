from enum import Enum


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


class SubjectNotFound(Exception):
    pass


class SubjectExists(Exception):
    pass


class FeatureExists(Exception):
    pass


class FeatureNotFound(Exception):
    pass


class VariantExists(Exception):
    pass


class VariantNotFound(Exception):
    def __init__(self, variant_name: str, feature_name: str):
        super().__init__(f"No variant named '{variant_name}' for feature '{feature_name}'")


class RolloutExists(Exception):
    pass


class RolloutNotFound(Exception):

    def __init__(self, feature_name: str):
        super().__init__(f"No rollout found for feature '{feature_name}'")


class InvalidRolloutProportion(Exception):

    class Reason(Enum):
        RANGE = 1
        EQUAL = 1
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
