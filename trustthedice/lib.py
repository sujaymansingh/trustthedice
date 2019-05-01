from fractions import Fraction

from attr import attrs, attrib


@attrs
class ProbableOutcome:
    """A probable outcome has a name and a probability.
    """
    name: str = attrib()
    probability: Fraction = attrib()
