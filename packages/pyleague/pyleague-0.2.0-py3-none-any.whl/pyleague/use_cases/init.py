from typing import List

from pyleague.domain.day_pointer import generate_day_pointer, store_day_pointer
from pyleague.domain.groups_per_day import generate_groups_per_day, store_groups_per_day
from pyleague.domain.participants import ask_for_participants, store_participants


def init_():
    # ask for participants
    participants = ask_for_participants()
    # store participants
    do_init(participants)


def do_init(participants: List[str]):
    store_participants(participants)
    # generate groups per day
    groups_per_day = generate_groups_per_day(participants)
    # store groups per day
    store_groups_per_day(groups_per_day)
    # generate day pointer
    day_pointer = generate_day_pointer(participants)
    # store day pointer
    store_day_pointer(day_pointer)
