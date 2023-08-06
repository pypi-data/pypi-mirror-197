from typing import Tuple

from pyleague.domain.day_pointer import read_day_pointer, print_day
from pyleague.domain.groups_per_day import read_group, print_group_pairs, get_group_pairs


def today_():
    day_pointer, group_pairs = get_today()
    # print corresponding day and group
    print_day(day_pointer)
    print_group_pairs(group_pairs)


def get_today() -> Tuple:
    # read day pointer
    day_pointer = read_day_pointer()
    # read corresponding group
    group = read_group(day_pointer)
    group_pairs = get_group_pairs(group)
    return day_pointer, group_pairs
