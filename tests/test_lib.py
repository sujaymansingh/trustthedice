from fractions import Fraction

import pytest

from trustthedice import lib


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

    with pytest.raises(lib.TotalProbabilityMoreThanOneError):
        lib.calculate_cumulative_probabilities([t1, t2])


def test_cumulative_outcomes_cant_be_under_one():
    t1 = lib.ProbableOutcome(name="t1", probability=Fraction(3, 7))
    t2 = lib.ProbableOutcome(name="t1", probability=Fraction(3, 7))

    with pytest.raises(lib.TotalProbabilityLessThanOneError):
        lib.calculate_cumulative_probabilities([t1, t2], remainder_name=None)


def test_cumulative_outcomes_rejects_redundant_remainder():
    t1 = lib.ProbableOutcome(name="t1", probability=Fraction(4, 7))
    t2 = lib.ProbableOutcome(name="t1", probability=Fraction(3, 7))

    # The probabilities already add up to 1, so a remainder is bad.
    with pytest.raises(lib.RedundantRemainderError):
        lib.calculate_cumulative_probabilities([t1, t2], remainder_name="try")
