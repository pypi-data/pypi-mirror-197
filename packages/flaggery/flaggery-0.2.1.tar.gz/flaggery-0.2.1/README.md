# Flaggery

Feature flag management framework for serving rollouts, ab-tests and feature groups.

**Table of contents:**
 - [Installation](#installation)
 - [Starting the API Server](#starting-the-api-server)
 - [Rest API Reference](#rest-api-reference)
 - [Configuring the API Server](#configuring-the-api-server)
 - [Quickstart Guide](#quickstart-guide)
 - [Entities Guide](#entities-guide)
   - [Subjects](#subjects)
   - [Buckets](#buckets)
   - [Features and Variants](#features-and-variants)
   - [Rollouts](#rollouts)
   - [AB Tests](#ab-tests)
   - [Groups and Overrides](#groups-and-overrides)

## Installation

```bash
pip install flaggery
```

## Starting the API Server

```bash
flaggery --host <host> --port <port>
```

<a id="rest-reference"></a>
## Rest API Reference

To access the API documentation,
first start the API server and then open
[http://{hostname}:{port}/docs](http://localhost/docs)
in your browser.

<a id="configuration"></a>
## Configuring the API server

The API server can be configured by setting the following environment variables:

| Variable                     | Required | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                                              |
|------------------------------|----------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `FLAGGERY_DB_URL`            | Yes      | None    | SQLAlchemy compatible connection URL for an existing database.<br><br>Depending on which database you use, you might also need to install database-specific Python clients (e.g.: psycopg2 for PostgreSQL)                                                                                                                                                                                                                               |
| `FLAGGERY_DB_AUTO_UPGRADE`   | No       | False   | If True, database will be migrated to the latest schema on server startup.                                                                                                                                                                                                                                                                                                                                                               |
| `FLAGGERY_ADMIN_MODE`        | No       | False   | If True, all endpoints are available. <br> <br> If false, the server goes on a limited read-only mode, in which all endpoints are locked except for `GET /v1/subject/flags` <br> <br> For both security and performance reasons, it is recommended to deploy a single replica of the server in admin mode, which can only be accessed by admins, and many replicas in limited read-only mode, which can be accessed by clients at scale. |
| `FLAGGERY_ENABLE_PROMETHEUS` | No       | False   | If True, prometheus metrics route is exposed at `/metrics`                                                                                                                                                                                                                                                                                                                                                                               |

<a id="quickstart"></a>
## Quickstart Guide

A basic workflow with Flaggery Python API (same operations also available in the Rest API)

```python
from flaggery.core import Flaggery

# Create connection
flaggery = Flaggery.from_db_url("postgresql+psycopg2://<user>:<pswd>@<host>:<port>/<db>")

# Migrate database to the latest schema
flaggery.upgrade_db()

# Allocate buckets (i.e.: partitions of subjects) 
flaggery.increase_buckets(10)

# Add subjects (i.e.: could be users/accounts/clients)
for _id in range(100):
    # Subjects have weight (i.e.: estimate of traffic/workload/demand/contract size)
    flaggery.add_subject(_id, weight=random.randint(1, 10))
# Subjects are automatically allocated into buckets by a weight balancing algorithm

# Create a feature flag
flaggery.add_feature("foobar")

# Create some variants of this feature
flaggery.add_variant("A", "foobar")
flaggery.add_variant("B", "foobar")

# Make the feature disabled by default
flaggery.add_disabling_variant("foobar", make_default=True)

# Set up a rollout of variant A
flaggery.add_rollout("A", "foobar")

# Push the rollout proportion to 10% (it starts at 0%)
flaggery.set_rollout_proportion("foobar", proportion=0.1)

# Now, the subjects getting variant 'A' of feature 'foobar'
# amount to approximately 10% of all subjects' weight
total_weight, weight_of_A = 0, 0
for subject_id in range(100):
    with flaggery.get_subject(subject_id) as subject:
        total_weight += subject.weight
        if flaggery.get_subject_variants(subject_id)["foobar"] == "A":
            weight_of_A += subject.weight
print("Weight of variant 'A': %.2f%%" % (100 * weight_of_A / total_weight))
            
# Create a user group
flaggery.add_group("friends")

# Add a subject to the group
flaggery.add_subject_to_group(42, "friends")

# Configure a group override
flaggery.add_group_override("friends", "foobar", "B")

# Now, subject 42 gets variant 'B' of feature 'foobar', regardless of rollout or default behaviour
assert flaggery.get_subject_variants(42) == {"foobar": "B"}

# Set up an AB-test on feature 'foobar'
flaggery.add_abtest(
    test_name="my_test",
    start=datetime(2024, 4, 1),
    end=datetime(2024, 4, 12),
    groups={
        "control": {"foobar": "__DISABLE__"},
        "experiment": {"foobar": "B"},
    },
    proportions=[0.8, 0.2]  # 80% control, 20% experiment
)
# Because the proportions sum up to 1, every bucket will be allocated to either one group or the other.
# This means that during the test period, the rollout of 10% of 'A' will have no effect.
# As always, group overrides have precedence, so subject 42 will still get 'B' regardless of its assigned test group.
```

<a id="entities-guide"></a>
## Entities Guide

### Subjects
Subjects may represent users, accounts, clients or something else.
Each subject has a weight,
which represents an estimate of the expected traffic,
demand or workload expected from that subject.

For an application with thousands of individual users,
it makes sense to treat each user as a subject with weight 1.
On the other hand, for a B2B application where each user is an employee of
a client company, it makes sense to treat each client as a subject
with weight proportional to the contract size or number of purchased licenses.

### Buckets
Buckets contain subjects and can be assigned to rollouts or ab-tests.
All subjects inside the same bucket have access to the same feature variants.
We try to distribute subjects in a way that all buckets have roughly the same weight.

The system starts with zero buckets, so buckets must be increased before subjects are added.
As a rule of thumb, 10 buckets are good if you have a few hundreds of unit-weight subjects,
while 100 buckets should be enough if you have more than that.

### Features and Variants
A feature is a named functionality of your application.
A variant of that feature is a named implementation of the respective functionality
(e.g.: if "sorting" is a feature, then "bubble-sort" and "quick-sort" are variants of it).

A feature may have a default variant, which may also be a disabling variant.

A disabling variant is a special type of variant that tells your application that
no implementation of that feature is to be used.
The name `__DISABLE__` is reserved for this type of variant.

When determining which variant of a feature a subject should get,
the order of resolution is:
1. **None**
2. **Default variant:** If that feature has a default variant
3. **Rolled-out variant:** If a rollout of that feature exists and the subject's bucket was assigned
4. **Variant in AB-testing group:** If a test of that feature is currently live
5. **Variant overrides:** If the subject is in a group that overrides that feature 

### Rollouts
A rollout is the serving of a feature variant to a proportion (i.e.: percentage) of the application traffic.

A feature can only have one rollout at a time,
although the chosen variant for that feature's rollout can be changed at any time.

When a rollout is created, its proportion is always 0%.
When its increased, more buckets are assigned to it.
When its decreased, previously assigned bucket are unassigned.

The effective weight of a rollout is the sum of the weights of the assigned buckets.
It might deviate a bit from `proportion * total_weight` because of eventual bucket imbalances,
although a rollout of 100% will always cover all buckets, as will a rollout of 0% cover zero buckets.

Rollouts take precedence over default variants in the subject's variants resolution,
if the subject is in one of the assigned buckets.

### AB Tests
An AB test is a structured, time-bound experiment
in which certain features are affected differently for each test-group.
Usually, a control group gets the stable or baseline variants of each feature
(the ones which have been previously validated),
while one or more experimental groups get each a different combination of feature variants.

Each test-group has a proportion (i.e.: desired percentage of traffic weight).
All proportions must sum up to 1, so that every bucket is assigned to one of the groups.

Concurrent tests affecting the same feature(s) are forbidden.

AB-tests are considered after rollouts and default variants
in the subject's variants resolution,
so they take precedence over everything else except for group overrides.

### Groups and Overrides
A group is an arbitrary, custom-defined collection of subjects.
It may be configured to override certain features with certain variants.

This is useful when an under-development feature variant must be exposed only
to a certain group of users, like the product designers, developers or beta testers.

The group override is the last step in the subject variant's resolution,
so a subject will get the overriden variant regardless of defaults, rollouts and ab-tests.
