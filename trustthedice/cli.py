import click


@click.group()
def main():
    pass


@main.command()
def generate():
    click.echo("TODO")
