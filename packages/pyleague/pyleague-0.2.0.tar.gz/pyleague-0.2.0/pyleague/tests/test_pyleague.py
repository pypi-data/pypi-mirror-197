from pyleague.domain.groups_per_day import generate_groups_per_day


def test_generate_groups_per_day_works_correctly_for_4_participants():
    participants = ["a", "b", "c", "d"]
    groups_per_day = generate_groups_per_day(participants)
    expected_groups_per_day = [
        ['a', 'b', 'c', 'd'],
        ['a', 'd', 'b', 'c'],
        ['a', 'c', 'd', 'b'],
    ]
    assert groups_per_day == expected_groups_per_day


def test_generate_groups_per_day_works_correctly_for_6_participants():
    participants = ["a", "b", "c", "d", "e", "f"]
    groups_per_day = generate_groups_per_day(participants)
    expected_groups_per_day = [['a', 'b', 'c', 'd', 'e', 'f'],
                               ['a', 'f', 'b', 'c', 'd', 'e'],
                               ['a', 'e', 'f', 'b', 'c', 'd'],
                               ['a', 'd', 'e', 'f', 'b', 'c'],
                               ['a', 'c', 'd', 'e', 'f', 'b']]
    assert groups_per_day == expected_groups_per_day
