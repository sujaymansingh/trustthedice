from fractions import Fraction

from attr import attrs, attrib


@attrs
class ProbableOutcome:
    """A probable outcome has a name and a probability.
    """

    name: str = attrib()
    probability: Fraction = attrib()


def parse_probable_outcome(outcome_string):
    """Parse a probable outcome from a string.

    >>> parse_probable_outcome("Win: 1 in 10")
    ProbableOutcome(name='Win', probability=Fraction(1, 10))
    """
    parts = [part.strip() for part in outcome_string.split(":")]
    if len(parts) != 2:
        raise InvalidProbableOutcomeStringError()
    name = parts[0]

    number_parts = [part.strip() for part in parts[1].split("in")]
    if len(parts) != 2:
        raise InvalidProbableOutcomeStringError()

    try:
        numbers = [int(part) for part in number_parts]
    except (TypeError, ValueError) as e:
        raise InvalidProbableOutcomeStringError(e)

    probability = Fraction(numbers[0], numbers[1])

    return ProbableOutcome(name=name, probability=probability)


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


def pick_outcome(value, outcomes):
    """Pick the first outcome that has a probability that is greater than the given value.

    >>> o1 = ProbableOutcome(name="a", probability=Fraction(1, 3))
    >>> o2 = ProbableOutcome(name="b", probability=Fraction(2, 3))
    >>> o3 = ProbableOutcome(name="c", probability=Fraction(3, 3))
    >>> outcomes = [o1, o2, o3]

    Anything less than (or equal to) 1/3 will give us a...
    >>> pick_outcome(0.001, outcomes).name
    'a'
    >>> pick_outcome(0.333, outcomes).name
    'a'
    >>> pick_outcome(Fraction(1, 3), outcomes).name
    'a'

    Between 1/3 and 2/3 gives us 'b'
    >>> pick_outcome(0.4, outcomes).name
    'b'
    """
    for outcome in outcomes:
        if value <= outcome.probability:
            return outcome
    raise CouldntPickOutcomeError()


class BaseError(Exception):
    def title(self):
        """Return a short, one line description
        """
        pass

    def description(self):
        """Return a longer, multiline description
        """
        pass


class InvalidProbableOutcomeStringError(BaseError):
    def title(self):
        return (
            "Invalid probable outcome value (must be 'Win the lottery: 1 in 1000000')"
        )


class TotalProbabilityMoreThanOneError(BaseError):
    def title(self):
        return "Total probability can't be more than one"

    def description(self):
        return """
            The total of all the probabilities is more than 1.
            Make sure that the total doesn't exceed 1!
        """


class TotalProbabilityLessThanOneError(BaseError):
    def title(self):
        return "Total probability can't be less than one"

    def description(self):
        return """
            The total of the all the probabilities is less than 1.
            Either fix the probabilities so that they add up to 1, or use
            the --otherwise flag to catch the rest
        """


class CouldntPickOutcomeError(BaseError):
    pass


class RedundantRemainderError(BaseError):
    def title(self):
        return "--otherwise passed in but not needed"

    def description(self):
        return """
            The total of the all the probabilities already is 1.
            There is no need for the --otherwise option: remove it.
        """
