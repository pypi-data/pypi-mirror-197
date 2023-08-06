from datetime import datetime
from typing import Dict, Set, Tuple, Optional

from sqlalchemy import Column, Integer, String, Float, UniqueConstraint, ForeignKeyConstraint, Boolean
from sqlalchemy import ForeignKey, Table
from sqlalchemy import select, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import validates, relationship
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.sqltypes import DateTime

from flaggery import utils
from flaggery.exceptions import ValidationError, InvalidRolloutProportion

Base = declarative_base()

BucketRollout = Table(
    'bucket_rollouts', Base.metadata,
    Column('bucket_id', Integer, ForeignKey('buckets.id')),
    Column('rollout_id', Integer, ForeignKey('rollouts.id'))
)

BucketTest = Table(
    'bucket_tests', Base.metadata,
    Column('bucket_id', Integer, ForeignKey('buckets.id')),
    Column('group_id', Integer),
    Column('test_id', Integer),
    ForeignKeyConstraint(['group_id', 'test_id'], ['abtest_groups.id', 'abtest_groups.test_id']),
    UniqueConstraint('bucket_id', 'test_id', name='_bucket_has_only_one_group_in_each_test', info={'FOO': 'BAR'}),
)

SubjectGroup = Table(
    'subject_groups', Base.metadata,
    Column('subject_id', Integer, ForeignKey('subjects.id')),
    Column('group_id', Integer, ForeignKey('groups.id')),
)

GroupOverrides = Table(
    'group_overrides', Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('feature_id', Integer),
    Column('variant_id', Integer),
    ForeignKeyConstraint(['feature_id', 'variant_id'], ['variants.feature_id', 'variants.id']),
    UniqueConstraint('group_id', 'feature_id', name='_group_override_feature_unique'),
)

AbTestGroupOverrides = Table(
    'abtest_group_overrides', Base.metadata,
    Column('group_id', Integer, ForeignKey("abtest_groups.id")),
    Column('feature_id', Integer, nullable=False),
    Column('variant_id', Integer, nullable=False),
    ForeignKeyConstraint(['feature_id', 'variant_id'], ['variants.feature_id', 'variants.id']),
    UniqueConstraint('group_id', 'feature_id', name='_test_group_unique_feature_override'),
)


class Variant(Base):
    __tablename__ = 'variants'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    feature_id = Column(Integer, ForeignKey('features.id'), nullable=False)
    feature = relationship("Feature", back_populates="variants", foreign_keys=[feature_id])#, remote_side=[Feature.id])
    disable = Column(Boolean, default=False, nullable=False)
    test_groups = relationship("AbTestGroup", uselist=True, secondary=AbTestGroupOverrides, viewonly=True)
    __table_args__ = (
        UniqueConstraint('feature_id', 'name', name='_feature_variant_unique'),
        UniqueConstraint('id', 'feature_id', name='_feature_variant_unique_ids'),
    )

    @validates("name")
    def validate_name(self, _, value):
        if self.disable and value != '__DISABLE__':
            raise ValidationError("Disabling variant must be named '__DISABLE__'")
        elif not self.disable and value == '__DISABLE__':
            raise ValidationError(f"Variant name is reserved: {value}")
        else:
            return value

    @validates('feature_id')
    def validate_feature_id(self, key, value):
        if self.feature_id and self.feature_id != value:
            raise ValidationError("Parent feature of variant cannot be changed")
        return value

    @validates('disable')
    def validate_disable(self, key, value):
        if self.disable and not value:
            raise ValidationError(
                f"Cannot turn disabling variant of feature '{self.feature.name}' into a common variant"
            )
        if self.disable is not None and not self.disable and value:
            raise ValidationError(
                f"Cannot turn non-disabling variant '{self.name}' of feature '{self.feature.name}' "
                "into a disabling variant"
            )
        return value

    def __repr__(self):
        return f"Variant({self.name}, of_feature={self.feature})"


class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, unique=True, nullable=False)
    default_variant_id = Column(Integer, ForeignKey('variants.id'), nullable=True)
    default_variant = relationship("Variant", foreign_keys=[default_variant_id], post_update=True)
    variants = relationship("Variant", back_populates="feature", foreign_keys=[Variant.feature_id])
    __table_args__ = (
        ForeignKeyConstraint(['id', 'default_variant_id'], ['variants.feature_id', 'variants.id']),
    )

    def __repr__(self):
        return f"Feature({self.name}, "\
               f"default_variant={None if self.default_variant_id is None else self.default_variant.name})"


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, unique=True)
    weight = Column(Integer, nullable=False, default=1)
    bucket_id = Column(Integer, ForeignKey('buckets.id'), nullable=False)
    bucket = relationship("Bucket", back_populates="subjects")
    groups = relationship("Group", secondary=SubjectGroup, back_populates='subjects')

    @validates("weight")
    def validate_weight(self, key, value):
        if value < 1:
            raise ValidationError("Weight must be at least 1")
        return value

    @property
    def variant_map(self) -> Dict[Feature, Variant]:
        return utils.append_dicts(
            self.bucket.variant_map,
            *[grp.variant_map for grp in self.groups]
        )

    def __repr__(self):
        return f"Subject({self.id}, weight={self.weight})"


class Bucket(Base):
    __tablename__ = 'buckets'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    rollouts = relationship("Rollout", secondary=BucketRollout, back_populates='buckets')
    abgroups = relationship("AbTestGroup", secondary=BucketTest, back_populates='buckets')
    subjects = relationship("Subject", back_populates="bucket")
    weights = association_proxy("subjects", "weight")

    @hybrid_property
    def weight(self) -> int:
        return sum(self.weights)

    @classmethod
    @weight.inplace.expression
    def _weight_expr(cls):
        return select(func.coalesce(func.sum(Subject.weight), 0))\
            .where(Subject.bucket_id == cls.id).scalar_subquery()

    @property
    def variant_map(self) -> Dict[Feature, Variant]:
        d = {roll.feature: roll.variant for roll in self.rollouts}
        for grp in self.abgroups:
            d.update(grp.variant_map)
        return d

    def __repr__(self):
        return f"Bucket({self.id}, weight={self.weight})"


class Rollout(Base):
    __tablename__ = 'rollouts'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    feature_id = Column(Integer, ForeignKey('features.id'), unique=True, nullable=False)
    feature = relationship("Feature", viewonly=True)
    variant_id = Column(Integer, nullable=False)
    variant = relationship("Variant")
    proportion = Column(Float, nullable=False, default=0.0)
    buckets = relationship("Bucket", secondary=BucketRollout, back_populates='rollouts')
    __table_args__ = (
        ForeignKeyConstraint(['feature_id', 'variant_id'], ['variants.feature_id', 'variants.id']),
        UniqueConstraint('feature_id', name="_only_one_rollout_per_feature")
    )

    @validates("proportion")
    def validate_proportion(self, _, value):
        if not (0.0 <= value <= 1.0):
            raise InvalidRolloutProportion.range(value)
        elif self.proportion == value:
            raise InvalidRolloutProportion.equal(value, self.feature.name)
        elif 100 * value % 5 != 0.0:
            raise InvalidRolloutProportion.precision(value)
        else:
            return value

    @property
    def weight(self) -> int:
        return sum([b.weight for b in self.buckets])

    @property
    def variant_map(self) -> Dict[Feature, Variant]:
        return {self.variant.feature: self.variant}

    def __repr__(self):
        return f"Rollout(feature={self.feature.name}, variant={self.variant.name}, proportion={100 * self.proportion}%)"


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, unique=True, nullable=False)
    subjects = relationship("Subject", secondary=SubjectGroup, back_populates='groups')
    variants = relationship("Variant", secondary=GroupOverrides)

    @property
    def variant_map(self) -> Dict[Feature, Variant]:
        return {variant.feature: variant for variant in self.variants}

    def add_override(self, var: Variant):
        self.variants = [v for v in self.variants if v.feature != var.feature] + [var]

    def rm_variant(self, feat: Feature):
        self.variants = [v for v in self.variants if v.feature != feat]

    def __repr__(self):
        return f"Group({self.name})"


class AbTestGroup(Base):
    __tablename__ = 'abtest_groups'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    proportion = Column(Float, nullable=False)
    test_id = Column(Integer, ForeignKey('abtests.id'), nullable=False)
    test = relationship("AbTest", back_populates='groups')
    variants = relationship("Variant", secondary=AbTestGroupOverrides)
    buckets = relationship("Bucket", secondary=BucketTest, back_populates='abgroups')

    __table_args__ = (
        UniqueConstraint('test_id', 'name', name='_group_name_in_test_unique'),
        UniqueConstraint('id', 'test_id', name='_test_group_unique_ids'),
    )

    @property
    def weight(self) -> int:
        return sum([b.weight for b in self.buckets])

    @property
    def variant_map(self) -> Dict[Feature, Variant]:
        return {v.feature: v for v in self.variants}

    @property
    def affected_features(self) -> Set[Feature]:
        return set([var.feature for var in self.variants])

    def __repr__(self):
        return f"AbTestGroup({self.name}, of_test={self.test.name})"


class AbTest(Base):
    __tablename__ = 'abtests'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, unique=True, nullable=False)
    groups = relationship("AbTestGroup", back_populates='test')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    @validates("start")
    def validate_start(self, _, start: datetime):
        if start <= datetime.now():
            raise ValidationError("AbTest start must be in the future")
        return start

    @validates("end")
    def validate_end(self, _, end):
        if end <= self.start:
            raise ValidationError("End date must be after the start date")
        return end

    @hybrid_property
    def live(self):
        return self.start <= datetime.now() <= self.end

    @classmethod
    @live.inplace.expression
    def _live_expr(cls):
        return select(and_(
            cls.start <= func.now(),
            func.now() <= cls.end
        )).scalar_subquery()

    @property
    def affected_features(self) -> Set[Feature]:
        s = set()
        for grp in self.groups:
            s.update(grp.affected_features)
        return s

    def feature_intersection(self, other_test) -> Set[Feature]:
        return self.affected_features.intersection(other_test.affected_features)

    def dates_intersection(self, other_test) -> Optional[Tuple[datetime, datetime]]:
        start, end = max(self.start, other_test.start), min(self.end, other_test.end)
        if start < end:
            return start, end
        else:
            return None

    def __repr__(self):
        return f"AbTest({self.name})"
