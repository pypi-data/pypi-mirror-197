import math
from contextlib import contextmanager
from datetime import datetime
from typing import List, Dict, Optional

from sqlalchemy import Engine
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, Session

from flaggery import exceptions as exc
from flaggery import utils
from flaggery.db.models import Bucket, Subject, Rollout, Feature, Variant, Group, AbTestGroup, AbTest


class Flaggery:

    def __init__(self, engine: Engine):
        self.engine = engine
        self.Session = sessionmaker(engine)

    @contextmanager
    def _get_or_create_session(self, session: Optional[Session]) -> Session:
        if session:
            yield session
        else:
            with self.Session.begin() as session:
                yield session

    @contextmanager
    def get_subject(self, sub_id: int, session: Optional[Session] = None) -> Subject:
        with self._get_or_create_session(session) as s:
            if sub := s.query(Subject).filter(Subject.id == sub_id).first():
                yield sub
            else:
                raise exc.SubjectNotFound(sub_id)

    @contextmanager
    def get_group(self, group_name: str, session: Optional[Session] = None) -> Group:
        with self._get_or_create_session(session) as s:
            if grp := s.query(Group).filter(Group.name == group_name).first():
                yield grp
            else:
                raise exc.GroupNotFound(group_name)

    @contextmanager
    def get_bucket(self, buck_id: int, session: Optional[Session] = None) -> Bucket:
        with self._get_or_create_session(session) as s:
            if buck := s.query(Bucket).filter(Bucket.id == buck_id).first():
                yield buck
            else:
                raise exc.BucketNotFound(buck_id)

    @contextmanager
    def get_feature(self, feature_name: str, session: Optional[Session] = None) -> Feature:
        with self._get_or_create_session(session) as s:
            if feat := s.query(Feature).filter(Feature.name == feature_name).first():
                yield feat
            else:
                raise exc.FeatureNotFound(feature_name)

    @contextmanager
    def get_variant(self, variant_name: str, feature_name: str, session: Optional[Session] = None) -> Variant:
        with self._get_or_create_session(session) as s:
            if var := s.query(Variant) \
                    .filter(Variant.name == variant_name) \
                    .filter(Variant.feature.has(name=feature_name)) \
                    .first():
                yield var
            elif s.query(Feature).filter(Feature.name == feature_name).first():
                raise exc.VariantNotFound(variant_name, feature_name)
            else:
                raise exc.FeatureNotFound(feature_name)

    @contextmanager
    def get_rollout(self, feature_name: str, session: Optional[Session] = None) -> Rollout:
        with self._get_or_create_session(session) as s:
            if roll := s.query(Rollout).filter(Rollout.feature.has(name=feature_name)).first():
                yield roll
            elif s.query(Feature).filter(Feature.name == feature_name).first():
                raise exc.RolloutNotFound(feature_name)
            else:
                raise exc.FeatureNotFound(feature_name)

    @contextmanager
    def get_abtest(self, test_name: str, session: Optional[Session] = None) -> Feature:
        with self._get_or_create_session(session) as s:
            if feat := s.query(AbTest).filter(AbTest.name == test_name).first():
                yield feat
            else:
                raise exc.AbTestNotFound(test_name)

    def get_subject_variants(self, sub_id: int) -> Dict[str, str]:
        with self.Session.begin() as session:
            with self.get_subject(sub_id, session) as sub:
                defaults = session.query(Feature).filter(Feature.default_variant_id.is_not(None)).all()
                return utils.append_dicts(
                    {feat.name: feat.default_variant.name for feat in defaults},
                    {feat.name: var.name for feat, var in sub.variant_map.items()}
                )

    def add_subject(self, sub_id: int, weight: int) -> int:
        try:
            with self.Session.begin() as session:
                buk = session.query(Bucket).order_by(Bucket.weight).first()
                if buk:
                    sub = Subject(id=sub_id, weight=weight, bucket_id=buk.id)
                    session.add(sub)
                    return buk.id
                else:
                    raise exc.NoBuckets("Please increase buckets before adding new subjects")
        except IntegrityError:
            raise exc.SubjectExists(sub_id)

    def increase_buckets(self, amount: int = 2) -> List[int]:
        if amount % 2 != 0:
            raise exc.ValidationError("Buckets must be increased in even amounts")
        with self.Session.begin() as session:
            next_id = session.query(func.max(Bucket.id) + 1).first()[0] or 1
            buckets = [Bucket(id=i) for i in range(next_id, next_id + amount)]
            for roll in session.query(Rollout).all():
                active = buckets if roll.proportion >= 1.0 else buckets[:math.floor(roll.proportion * amount)]
                roll.buckets += active
            session.add_all(buckets)
            return [b.id for b in buckets]

    def add_feature(self, name: str):
        try:
            with self.Session.begin() as session:
                feat = Feature(name=name)
                session.add(feat)
        except IntegrityError:
            raise exc.FeatureExists(name)

    def add_disabling_variant(self, feature_name: str, make_default: bool = False):
        self.add_variant("__DISABLE__", feature_name, make_default, disable=True)

    def add_variant(self, variant_name: str, feature_name: str, make_default: bool = False, disable: bool = False):
        try:
            with self.Session.begin() as session:
                with self.get_feature(feature_name, session) as feat:
                    var = Variant(disable=disable, name=variant_name, feature_id=feat.id)
                    session.add(var)
                    if make_default:
                        feat.default_variant = var
        except IntegrityError:
            raise exc.VariantExists(f"Feature '{feature_name}' already has a variant named '{variant_name}'")

    def list_features(self) -> List[str]:
        with self.Session.begin() as session:
            return [f.name for f in session.query(Feature).all()]

    def set_default_feature_variant(self, feature_name: str, variant_name: str):
        with self.Session.begin() as session:
            with self.get_feature(feature_name, session) as feat:
                with self.get_variant(variant_name, feature_name, session) as var:
                    feat.default_variant = var

    def add_rollout(self, variant_name: str, feature_name: str):
        try:
            with self.Session.begin() as session:
                with self.get_variant(variant_name, feature_name, session) as var:
                    roll = Rollout(variant_id=var.id, feature_id=var.feature_id)
                    session.add(roll)
        except IntegrityError:
            raise exc.RolloutExists(f"A rollout of feature '{feature_name}' already exists")

    def set_rollout_variant(self, variant_name: str, feature_name: str):
        with self.Session.begin() as session:
            with self.get_rollout(feature_name, session) as roll:
                with self.get_variant(variant_name, feature_name, session) as var:
                    roll.variant = var

    def set_rollout_proportion(self, feature_name: str, proportion: float):
        with self.Session.begin() as session:
            with self.get_rollout(feature_name, session) as roll:
                prev = roll.proportion
                roll.proportion = proportion
                bucks = session.query(Bucket).all()
                total_weight = sum([b.weight for b in bucks])
                tgt_weight = math.floor(proportion * total_weight)
                if proportion >= 1.0:
                    roll.buckets = bucks
                elif proportion <= 0.0:
                    roll.buckets = []
                else:
                    null_bucks_in, null_bucks_out = [], []
                    for b in bucks:
                        if b.weight == 0.0:
                            (null_bucks_in if b in roll.buckets else null_bucks_out).append(b)
                            continue
                        if proportion > prev and b not in roll.buckets and roll.weight + b.weight <= tgt_weight:
                            roll.buckets.append(b)
                        if proportion < prev and b in roll.buckets and roll.weight - b.weight >= tgt_weight:
                            roll.buckets.remove(b)
                    total_null_bucks = len(null_bucks_in) + len(null_bucks_out)
                    tgt_null_bucks = math.floor(proportion * total_null_bucks)
                    diff_null_bucks = tgt_null_bucks - len(null_bucks_in)
                    if diff_null_bucks > 0:
                        roll.buckets += null_bucks_out[:diff_null_bucks]
                    if diff_null_bucks < 0:
                        [roll.buckets.remove(b) for b in null_bucks_in[:abs(diff_null_bucks)]]

    def add_group(self, group_name: str):
        try:
            with self.Session.begin() as session:
                grp = Group(name=group_name)
                session.add(grp)
        except IntegrityError:
            raise exc.GroupExists(group_name)

    def add_subject_to_group(self, sub_id: int, group_name: str):
        with self.Session.begin() as session:
            with self.get_group(group_name, session) as grp:
                with self.get_subject(sub_id, session) as sub:
                    if sub in grp.subjects:
                        raise exc.SubjectAlreadyInGroup(sub_id, group_name)
                    else:
                        grp.subjects.append(sub)

    # TODO: rm_subject_from_group
    # TODO: rm_group_override

    def add_group_override(self, group_name: str, feature_name: str, variant_name: str):
        with self.Session.begin() as session:
            with self.get_group(group_name, session) as grp:
                with self.get_variant(variant_name, feature_name, session) as var:
                    grp.add_override(var)

    def rm_group(self, group_name: str):
        with self.Session.begin() as session:
            with self.get_group(group_name, session) as grp:
                session.delete(grp)

    def add_abtest(
        self,
        test_name: str,
        start: datetime,
        end: datetime,
        groups: Dict[str, Dict[str, str]],
        proportions: Optional[List[float]] = None
    ):
        if len(groups) < 2:
            raise exc.ValidationError(f"AbTest requires at least 2 groups")
        if proportions is None:
            proportions = utils.partition_exact(1.0, len(groups))
        if len(proportions) != len(groups):
            raise exc.ValidationError(f"Got {len(proportions)} proportions for {len(groups)} test groups")
        if sum(proportions) != 1.0:
            raise exc.ValidationError(f"Test group proportions must sum up to 1.0")
        try:
            with self.Session.begin() as session:
                test = AbTest(name=test_name, start=start, end=end)

                # Build groups
                for (grp_name, variants), proportion in zip(groups.items(), proportions):
                    grp = AbTestGroup(name=grp_name, test=test, proportion=proportion)
                    for feat_name, var_name in variants.items():
                        with self.get_variant(var_name, feat_name, session) as var:
                            grp.variants.append(var)
                session.add_all(test.groups)

                # Assert all groups affect the same features
                for grp in test.groups:
                    if missing := test.affected_features.difference(grp.affected_features):
                        raise exc.ValidationError(
                            f"Some features of the ab-test are not configured for "
                            f"the group '{grp.name}': {[f.name for f in missing]}"
                        )

                # Assert no overlapping tests affect the same features
                other_tests = set()
                for feat in test.affected_features:
                    for grp in session.query(AbTestGroup).filter(AbTestGroup.variants.any(feature_id=feat.id)).all():
                        other_tests.add(grp.test)
                other_tests.discard(test)
                for other_test in other_tests:
                    if overlap := test.dates_intersection(other_test):
                        start, end = overlap
                        feats = [f.name for f in test.feature_intersection(other_test)]
                        raise exc.ValidationError(
                            f"Cannot create test '{test_name}' because other test '{other_test.name}' "
                            f"also affects the features {feats} "
                            f"during the overlapping period between {start.isoformat()} and {end.isoformat()}. "
                            "Please review test end/start dates and/or affected features."
                        )

                # Assign weighed buckets
                bucks = session.query(Bucket).filter(Bucket.weight > 0.0).order_by(Bucket.weight).all()
                assignments = utils.partition_by_weight(
                    partition_proportions=[grp.proportion for grp in test.groups],
                    weighed_elements=[(b, b.weight) for b in bucks]
                )
                for grp, assigned_buckets in zip(test.groups, assignments):
                    grp.buckets = assigned_buckets

                # Assign empty buckets
                null_bucks = session.query(Bucket).filter(Bucket.weight == 0.0).all()
                null_assignments = utils.partition_by_amount(
                    partition_proportions=[grp.proportion for grp in test.groups],
                    elements=null_bucks
                )
                for grp, assigned_null_buckets in zip(test.groups, null_assignments):
                    grp.buckets += assigned_null_buckets

                session.add(test)
        except IntegrityError as e:
            if len(e.params) >= 1 and e.params[0] == test_name:
                raise exc.AbTestExists(test_name)
            else:
                raise e
