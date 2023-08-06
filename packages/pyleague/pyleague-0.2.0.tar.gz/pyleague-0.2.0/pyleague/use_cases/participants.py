from typing import List

from pyleague.domain.participants import read_participants, print_participants


def participants_():
    # read participants
    my_participants = get_participants()
    # print participants
    print_participants(my_participants)


def get_participants() -> List[str]:
    my_participants = read_participants()
    return my_participants
