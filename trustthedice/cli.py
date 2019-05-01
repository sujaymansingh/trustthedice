import random

from functools import wraps
from textwrap import dedent

import click

from . import lib


class ProbableOutcomeParamType(click.ParamType):
    name = "ProbableOutcome"

    def convert(self, value, _param, _ctx):
        return lib.parse_probable_outcome(value)


def handle_errors_nicely(func):
    """This attempts to run some code, and deal (nicely) with any exception

    In particular, for our own exceptions, we can print a suggestion that helps
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except lib.BaseError as e:
            click.secho("Error: ", fg="red", nl=False)
            click.echo(e.title() or e.__class__.__name__)
            description = e.description() or ""
            if description:
                click.echo(dedent(description))
        except:
            click.echo("unknown error")
            # TODO: don't just blindly raise! Deal with it better
            raise

    return wrapped


@click.group()
def main():
    pass


@main.command("random")
@click.option(
    "--outcome", "-oc", "outcomes", multiple=True, type=ProbableOutcomeParamType()
)
@click.option("--otherwise", type=str, default="n/a")
def pick_random_outcome(outcomes, otherwise):
    outcomes = lib.calculate_cumulative_probabilities(
        outcomes, remainder_name=otherwise
    )
    value = random.random()
    chosen_outcome = lib.pick_outcome(value, outcomes)

    click.echo(chosen_outcome.name)
