import math
import sys
from importlib.metadata import entry_points
from queue import LifoQueue
from typing import Tuple, List, Callable, Any


def partition_exact(total: float, n_partitions: int) -> List[float]:
    parts = [total / n_partitions] * n_partitions
    if sum(parts) != total:
        parts[-1] += total - sum(parts)
    return parts


def append_dicts(*dicts: dict):
    final = {}
    for _dict in dicts:
        final.update(_dict)
    return final


def partition_by_amount(partition_proportions: List[float], elements: List[Any]) -> List[List[Any]]:
    num_partitions = len(partition_proportions)
    assert num_partitions >= 2
    assert sum(partition_proportions) == 1.0
    total_amount = len(elements)
    target_amounts = [math.floor(total_amount * proportion) for proportion in partition_proportions]
    diff = total_amount - sum(target_amounts)
    target_amounts[-1] += diff
    assignments = [[] for _ in range(num_partitions)]
    pointer = 0
    for idx, tgt in enumerate(target_amounts):
        assignments[idx] = elements[pointer : pointer + tgt]
        pointer += tgt
    return assignments


def partition_by_weight(partition_proportions: List[float], weighed_elements: List[Tuple[Any, int]]) -> List[List[Any]]:
    # pylint: disable=R0914
    num_partitions = len(partition_proportions)
    assert num_partitions >= 2
    assert sum(partition_proportions) == 1.0
    total_weight = sum(e_wg for _, e_wg in weighed_elements)
    curr_weights = [0] * num_partitions
    target_weights = [math.floor(total_weight * proportion) for proportion in partition_proportions]
    assignments = [[] for _ in range(num_partitions)]
    stack = LifoQueue(len(weighed_elements))
    for element in sorted(weighed_elements, key=lambda kv: kv[1]):
        stack.put(element)
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
    exc_factory_multi: Callable[[str, str], Exception],
):
    found = entry_points(group=group, name=name)
    if len(found) == 0:
        raise exc_factory_none(group, name)
    if len(found) > 1:
        raise exc_factory_multi(group, name)
    return found[0].load()
