from pyleague.domain.day_pointer import read_day_pointer, modify_day_pointer, store_day_pointer, print_day
from pyleague.domain.groups_per_day import read_group, print_group_pairs, get_group_pairs


def next_():
    day_pointer, group_pairs = set_next_day()
    # print corresponding day and group
    print_day(day_pointer)
    print_group_pairs(group_pairs)


def set_next_day():
    # read day pointer
    day_pointer = read_day_pointer()
    # modify day pointer
    day_pointer = modify_day_pointer(day_pointer, next_=True)
    # store modified day pointer
    store_day_pointer(day_pointer)
    # read corresponding group
    group = read_group(day_pointer)
    group_pairs = get_group_pairs(group)
    return day_pointer, group_pairs
