from fractions import Fraction

from attr import attrs, attrib


@attrs
class ProbableOutcome:
    """A probable outcome has a name and a probability.
    """
    name: str = attrib()
    probability: Fraction = attrib()


def calculate_cumulative_probabilities(outcomes, remainder_name=None):
    """Return a new set of outcomes, but with probabilities made cumulative.

    I.e. if we have a list of outcomes, and each has its own individual
    probability, return a new list of outcomes where the probabilities are:
    [prob0, prob0 + prob1, prob0 + prob1 + prob2, ...]

    This way, selecting a random value is as simple as choosing a number
    between 0 and 1, then finding the first outcome whose (cumulative)
    probability is greater than our value.

    If a remainder_name is given, then a probable-outcome is added at the end
    that has a probability of 1 (to catch any values beyond the final probable
    outcome)
    """
    result = []

    one = Fraction(1, 1)
    current_total = Fraction(0, 1)
    for outcome in outcomes:
        current_total += outcome.probability
        if current_total > one:
            raise TotalProbabilityMoreThanOneError()
        result.append(ProbableOutcome(name=outcome.name, probability=current_total))

    if current_total == one:
        if remainder_name:
            raise RedundantRemainderError()
    else:
        if remainder_name:
            result.append(ProbableOutcome(name=remainder_name, probability=one))
        else:
            # We have a gap between our current total and 1.0
            # Any values within there will have no probabilities, and that's bad.
            raise TotalProbabilityLessThanOneError()

    return result


class BaseError(Exception):
    pass


class TotalProbabilityMoreThanOneError(BaseError):
    pass


class TotalProbabilityLessThanOneError(BaseError):
    pass


class RedundantRemainderError(BaseError):
    pass
