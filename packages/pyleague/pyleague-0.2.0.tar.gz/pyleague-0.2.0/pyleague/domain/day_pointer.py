import json
import logging

from pyleague.domain.participants import n_of_participants
from pyleague.infrastructure.path_utils import get_project_root_path


def generate_day_pointer(participants):
    logging.debug("Generating day pointer")
    number_of_participants = len(participants)
    number_of_days = number_of_participants - 1
    day_pointer = (0, number_of_days)
    return day_pointer


def store_day_pointer(day_pointer):
    logging.debug("Storing day pointer")
    root = get_project_root_path()
    day_pointer_path = root / "files" / "day_pointer.json"
    with open(day_pointer_path, "w") as day_pointer_file:
        json.dump(day_pointer, day_pointer_file)


def read_day_pointer():
    logging.debug("Reading day pointer")
    root = get_project_root_path()
    day_pointer_path = root / "files" / "day_pointer.json"
    with open(day_pointer_path, "r") as day_pointer_file:
        day_pointer = json.load(day_pointer_file)
    return day_pointer


def modify_day_pointer(day_pointer, next_):
    logging.debug("Modifying day pointer")
    if next_:
        day_pointer[0] += 1
        day_pointer[0] %= n_of_participants() - 1
    else:
        day_pointer[0] -= 1
        day_pointer[0] %= n_of_participants() - 1
    return day_pointer


def print_day(day_pointer):
    print(f"Day: {day_pointer[0]}")
