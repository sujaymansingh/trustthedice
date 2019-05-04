import json

from fractions import Fraction

import pytest

from trustthedice import exceptions, lib


def test_outcome_serialise():
    _assert_serialisable(
        lib.ProbableOutcome(name="outcomo", probability=Fraction(1, 7))
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
