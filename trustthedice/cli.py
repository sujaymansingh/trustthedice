import random

from functools import wraps

import click

from . import exceptions, lib


# TODO: make this configurable?
PROJECT_DIR = ".trustthedice"


class ProbableOutcomeParamType(click.ParamType):
    name = "ProbableOutcome"

    def convert(self, value, param, ctx):
        try:
            return lib.parse_probable_outcome(value)
        except exceptions.BaseError as e:
            self.fail(e.title(), param, ctx)


def handle_errors_nicely(func):
    """This attempts to run some code, and deal (nicely) with any exception

    In particular, for our own exceptions, we can print a suggestion that helps
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except click.ClickException as e:
            # Let click handle this, it'll show the relevant erroe message and
            # exit with a non-zero code.
            raise
        except:
            click.echo("unknown error")
            # TODO: don't just blindly raise! Deal with it better
            raise

    return wrapped


@click.group()
def main():
    pass


@main.group()
def events():
    pass


@events.command("save")
@click.argument("name", type=str)
@click.option(
    "--outcome", "-oc", "outcomes", multiple=True, type=ProbableOutcomeParamType()
)
@click.option("--otherwise", type=str, default="")
@click.option("--overwrite/--no-overwrite", default=False)
@handle_errors_nicely
def save_random_event(name, outcomes, otherwise, overwrite):
    project_dir = PROJECT_DIR

    all_outcomes = lib.calculate_cumulative_probabilities(
        outcomes, remainder_name=otherwise
    )
    random_event = lib.RandomEvent(name=name, outcomes=all_outcomes)
    lib.save_random_event(project_dir, random_event, overwrite)


@main.command("random")
@click.option(
    "--outcome", "-oc", "outcomes", multiple=True, type=ProbableOutcomeParamType()
)
@click.option("--otherwise", type=str, default="")
@click.option("--from-saved", "saved_event_name", type=str, default="")
@handle_errors_nicely
def pick_random_outcome(outcomes, otherwise, saved_event_name):
    if saved_event_name:
        if outcomes or otherwise:
            raise exceptions.CantHaveOutcomesAndSavedEventError()

        project_dir = PROJECT_DIR
        event = lib.load_random_event(project_dir, saved_event_name)
        outcomes = event.outcomes
    else:
        outcomes = lib.calculate_cumulative_probabilities(
            outcomes, remainder_name=otherwise
        )
    value = random.random()
    chosen_outcome = lib.pick_outcome(value, outcomes)

    click.echo(chosen_outcome.name)
