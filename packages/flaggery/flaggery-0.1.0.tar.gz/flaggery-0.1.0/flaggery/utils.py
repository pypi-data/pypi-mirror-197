import math
import os
import random
import sys
from collections import defaultdict
from importlib.metadata import entry_points
from queue import Queue, LifoQueue
from typing import Tuple, List, Callable, Any

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine


def partition_exact(total: float, n_partitions: int) -> List[float]:
    parts = [total / n_partitions] * n_partitions
    if sum(parts) != total:
        parts[-1] += total - sum(parts)
    return parts


def append_dicts(*dicts: dict):
    final = {}
    for d in dicts:
        final.update(d)
    return final


def shuffle(_list: list) -> list:
    random.shuffle(_list)
    return _list


def shuffled_queue(_list: list, lifo: bool = False) -> Queue:
    if lifo:
        queue = LifoQueue(len(_list))
    else:
        queue = Queue(len(_list))
    for x in shuffle(_list):
        queue.put(x)
    return queue


def shuffled_stack(_list: list) -> Queue:
    return shuffled_queue(_list, lifo=True)


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def partition_by_amount(partition_proportions: List[float], elements: List[Any]) -> List[List[Any]]:
    num_partitions = len(partition_proportions)
    assert num_partitions >= 2
    assert sum(partition_proportions) == 1.0
    total_amount = len(elements)
    target_amounts = [math.floor(total_amount * proportion) for proportion in partition_proportions]
    diff = total_amount - sum(target_amounts)
    target_amounts[-1] += diff
    assignments = [list() for _ in range(num_partitions)]
    pointer = 0
    for idx, tgt in enumerate(target_amounts):
        assignments[idx] = elements[pointer:pointer + tgt]
        pointer += tgt
    return assignments


def partition_by_weight(partition_proportions: List[float], weighed_elements: List[Tuple[Any, int]]) -> List[List[Any]]:
    num_partitions = len(partition_proportions)
    assert num_partitions >= 2
    assert sum(partition_proportions) == 1.0
    total_weight = sum(e_wg for _, e_wg in weighed_elements)
    curr_weights = [0] * num_partitions
    target_weights = [math.floor(total_weight * proportion) for proportion in partition_proportions]
    assignments = [list() for _ in range(num_partitions)]
    stack = LifoQueue(len(weighed_elements))
    for e in sorted(weighed_elements, key=lambda kv: kv[1]):
        stack.put(e)
    while stack.qsize() > 0:
        stuck = True
        for part_idx in range(num_partitions):
            element_id, element_weight = stack.get()
            if curr_weights[part_idx] + element_weight <= target_weights[part_idx]:
                assignments[part_idx].append(element_id)
                curr_weights[part_idx] += element_weight
                stuck = False
            else:
                stack.put((element_id, element_weight))
            if stack.qsize() <= 0:
                break
        if stuck and stack.qsize() >= 0:
            element_id, element_weight = stack.get()
            min_error = sys.maxsize
            chosen_part = None
            for part_idx in range(num_partitions):
                error = curr_weights[part_idx] + element_weight - target_weights[part_idx]
                if error < min_error:
                    min_error = error
                    chosen_part = part_idx
            assignments[chosen_part].append(element_id)
            curr_weights[chosen_part] += element_weight
    return assignments


def find_plugin(
    group: str,
    name: str,
    exc_factory_none: Callable[[str, str], Exception],
    exc_factory_multi: Callable[[str, str], Exception]
):
    found = entry_points(group=group, name=name)
    if len(found) == 0:
        raise exc_factory_none(group, name)
    if len(found) > 1:
        raise exc_factory_multi(group, name)
    return found[0].load()


def get_alembic_config(db_url, entity: str):
    alembic_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), entity)
    # Escape any '%' that appears in a db_url. This could be in a password,
    # url, or anything that is part of a potentially complex database url
    db_url = db_url.replace("%", "%%")
    config = Config(os.path.join(alembic_dir, "alembic.ini"))
    config.set_main_option("script_location", alembic_dir)
    config.set_main_option("sqlalchemy.url", db_url)
    return config


def upgrade_db(engine: Engine, entity: str):
    db_url = str(engine.url)
    config = get_alembic_config(db_url, entity)
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")
