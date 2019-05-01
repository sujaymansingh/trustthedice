import random

import click

from . import lib


class ProbableOutcomeParamType(click.ParamType):
    name = "ProbableOutcome"

    def convert(self, value, _param, _ctx):
        return lib.parse_probable_outcome(value)


@contextmanager
def catch_errors():
    try:
        yield
    except lib.BaseError as e:
        click.echo("Encountered an error:")
        click.echo(dedent(e.explanation()))
    except:
        click.echo("unknown error")
        raise


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
