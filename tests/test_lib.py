import json

from fractions import Fraction
from os import path

import pytest

from trustthedice import exceptions, lib


def test_outcome_serialise():
    _assert_serialisable(
        lib.ProbableOutcome(name="outcomo", probability=Fraction(1, 7))
    )


def test_event_serialise():
    _assert_serialisable(
        lib.RandomEvent(
            name="evento",
            outcomes=[
                lib.ProbableOutcome(name="Safety", probability=Fraction(1, 2)),
                lib.ProbableOutcome(
                    name="Woodpeckero loco", probability=Fraction(1, 2)
                ),
            ],
        )
    )


def _assert_serialisable(original):
    simple_list = original.to_simple_list()
    # The whole point is to produce something that can be JSON serialised:
    # thus this shouldn't throw an erroe.
    json.dumps(simple_list)
    reconstructed = original.__class__.from_simple_list(simple_list)
    assert reconstructed == original


def test_bad_serialisable_input_for_outcome():
    for bad_input in [
        [],
        ["has a name and numerator", "but not a denominator"],
        "not a list",
    ]:
        with pytest.raises(exceptions.SerialisationError):
            lib.ProbableOutcome.from_simple_list(bad_input)


def test_cumulative_outcomes_generates_remainder():
    t1 = lib.ProbableOutcome(name="t1", probability=Fraction(4, 7))
    t2 = lib.ProbableOutcome(name="t1", probability=Fraction(2, 7))
    outcomes = lib.calculate_cumulative_probabilities([t1, t2], remainder_name="rest")

    assert len(outcomes) == 3
    [new_t1, new_t2, rest] = outcomes

    assert new_t1.probability == Fraction(4, 7)
    assert new_t2.probability == Fraction(6, 7)  # t1 + t2

    # And a remainder to bring us back up to 1
    assert rest.probability == Fraction(1, 1)


def test_cumulative_outcomes_without_remainder():
    t1 = lib.ProbableOutcome(name="t1", probability=Fraction(4, 7))
    t2 = lib.ProbableOutcome(name="t1", probability=Fraction(3, 7))

    outcomes = lib.calculate_cumulative_probabilities([t1, t2])

    assert len(outcomes) == 2
    assert outcomes[0].probability == Fraction(4, 7)
    assert outcomes[1].probability == Fraction(7, 7)


def test_cumulative_outcomes_cant_go_past_one():
    t1 = lib.ProbableOutcome(name="t1", probability=Fraction(4, 7))
    t2 = lib.ProbableOutcome(name="t1", probability=Fraction(4, 7))

    with pytest.raises(exceptions.TotalProbabilityMoreThanOneError):
        lib.calculate_cumulative_probabilities([t1, t2])


def test_cumulative_outcomes_cant_be_under_one():
    t1 = lib.ProbableOutcome(name="t1", probability=Fraction(3, 7))
    t2 = lib.ProbableOutcome(name="t1", probability=Fraction(3, 7))

    with pytest.raises(exceptions.TotalProbabilityLessThanOneError):
        lib.calculate_cumulative_probabilities([t1, t2], remainder_name=None)


def test_cumulative_outcomes_rejects_redundant_remainder():
    t1 = lib.ProbableOutcome(name="t1", probability=Fraction(4, 7))
    t2 = lib.ProbableOutcome(name="t1", probability=Fraction(3, 7))

    # The probabilities already add up to 1, so a remainder is bad.
    with pytest.raises(exceptions.RedundantRemainderError):
        lib.calculate_cumulative_probabilities([t1, t2], remainder_name="try")


def test_initialise(tmp_path):
    project_dir = path.join(tmp_path, ".trustthedice")
    assert not path.exists(project_dir)

    lib.initialise(project_dir)

    assert path.isdir(project_dir)
    assert path.isfile(path.join(project_dir, "random_events"))

    with pytest.raises(exceptions.ProjectAlreadyExistsError):
        lib.initialise(project_dir)

    lib.initialise(project_dir, ignore_existing=True)


def test_saving_a_random_event(tmp_path):
    with open(path.join(tmp_path, "random_events"), "w") as out:
        out.write("")

    random_event = lib.RandomEvent(
        name="sure thing",
        outcomes=[
            lib.ProbableOutcome(name="win", probability=Fraction(99, 100)),
            lib.ProbableOutcome(name="lose", probability=Fraction(1, 100)),
        ],
    )

    assert lib.load_random_events(tmp_path) == []

    # First write the event...
    lib.save_random_event(tmp_path, random_event)

    assert lib.load_random_events(tmp_path) == [random_event]

    # Now, attempting to rewrite it is bad!
    with pytest.raises(exceptions.RandomEventExistsError):
        lib.save_random_event(tmp_path, random_event)

    # now let's modify it
    new_random_event = lib.RandomEvent(
        name="sure thing",
        outcomes=[lib.ProbableOutcome(name="win", probability=Fraction(100, 100))],
    )
    lib.save_random_event(tmp_path, new_random_event, overwrite=True)

    assert lib.load_random_events(tmp_path) == [new_random_event]


def test_loading_a_specific_event(tmp_path):
    with open(path.join(tmp_path, "random_events"), "w") as out:
        out.write("")

    random_event = lib.RandomEvent(
        name="sure thing",
        outcomes=[lib.ProbableOutcome(name="win", probability=Fraction(100, 100))],
    )
    lib.save_random_event(tmp_path, random_event)

    assert lib.load_random_event(tmp_path, "sure thing") == random_event

    with pytest.raises(exceptions.RandomEventDoesntExistError):
        lib.load_random_event(tmp_path, "this won't exist")
