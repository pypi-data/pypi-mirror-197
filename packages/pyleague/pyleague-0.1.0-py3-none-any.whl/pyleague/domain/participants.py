import json
import logging

from pyleague.infrastructure.path_utils import get_project_root_path


def ask_for_participants():
    participants = list()
    i = 0
    while True:
        participant = input(f"Insert participant {i} or type 'done' to continue: ")
        if participant == "":
            break
        if participant == "done":
            break
        else:
            participants.append(participant)
            i += 1

    number_of_participants = len(participants)
    if number_of_participants % 2 != 0:
        participants.append("No one")

    return participants


def store_participants(participants):
    logging.debug("Storing participants ...")
    root = get_project_root_path()
    participants_file_path = root / "files" / "participants.json"
    with open(participants_file_path, "w") as participants_file:
        json.dump(participants, participants_file)


def read_participants():
    logging.debug("Reading participants ...")
    root = get_project_root_path()
    participants_file_path = root / "files" / "participants.json"
    with open(participants_file_path, "r") as participants_file:
        participants = json.load(participants_file)
    return participants


def n_of_participants():
    return len(read_participants())


def print_participants(participants):
    print("Participants: ")
    for participant in participants:
        print(participant)
