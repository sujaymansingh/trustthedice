from textwrap import dedent

import click


class BaseError(click.ClickException):
    def __init__(self):
        pass

    def show(self):
        click.secho("Error: ", fg="red", nl=False)
        click.echo(self.title() or self.__class__.__name__)

        description = self.description() or ""
        if description:
            click.echo(dedent(description))

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


class SerialisationError(BaseError):
    def __init__(self, message):
        self.message = message

    def title(self):
        return "Couldn't load object from disk"

    def description(self):
        return self.message
