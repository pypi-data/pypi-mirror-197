import typer

from pyleague.domain.day_pointer import generate_day_pointer, store_day_pointer, read_day_pointer, modify_day_pointer
from pyleague.domain.groups_per_day import generate_groups_per_day, store_groups_per_day, read_group
from pyleague.domain.participants import ask_for_participants, store_participants, read_participants, print_participants

app = typer.Typer()


@app.command()
def init():
    # ask for participants
    participants = ask_for_participants()
    # store participants
    store_participants(participants)
    # generate groups per day
    groups_per_day = generate_groups_per_day(participants)
    # store groups per day
    store_groups_per_day(groups_per_day)
    # generate day pointer
    day_pointer = generate_day_pointer(participants)
    # store day pointer
    store_day_pointer(day_pointer)


def print_day_and_group(day_pointer, group):
    number_of_participants = len(group)

    pairs = list()
    for i in range(int(number_of_participants / 2)):
        pairs.append(f"{group[i]} VS {group[-i - 1]}")

    print(f"Day: {day_pointer[0]}")
    print("")
    for pair in pairs:
        print(pair)


@app.command()
def previous():
    # read day pointer
    day_pointer = read_day_pointer()
    # modify day pointer
    day_pointer = modify_day_pointer(day_pointer, next_=False)
    # store modified day pointer
    store_day_pointer(day_pointer)
    # read corresponding group
    group = read_group(day_pointer)
    # print corresponding day and group
    print_day_and_group(day_pointer, group)


@app.command()
def today():
    # read day pointer
    day_pointer = read_day_pointer()
    # read corresponding group
    group = read_group(day_pointer)
    # print corresponding day and group
    print_day_and_group(day_pointer, group)


@app.command()
def next():
    # read day pointer
    day_pointer = read_day_pointer()
    # modify day pointer
    day_pointer = modify_day_pointer(day_pointer, next_=True)
    # store modified day pointer
    store_day_pointer(day_pointer)
    # read corresponding group
    group = read_group(day_pointer)
    # print corresponding day and group
    print_day_and_group(day_pointer, group)


@app.command()
def participants():
    # read participants
    my_participants = read_participants()
    # print participants
    print_participants(my_participants)


if __name__ == "__main__":
    app()
