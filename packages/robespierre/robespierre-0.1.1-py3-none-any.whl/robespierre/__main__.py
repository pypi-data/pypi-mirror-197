import logging
import click
import coloredlogs
import os

import robespierre
import robespierre.runner as runner

from importlib.metadata import version, PackageNotFoundError


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    if debug:
        coloredlogs.install(level=logging.DEBUG)
        robespierre.DEBUG = True
    else:
        coloredlogs.install(level=logging.INFO)

    logging.debug("Debug active")


@cli.command()
@click.option("--config", default=os.path.join(os.path.dirname(__file__), '../../config.toml'), help="Configuration file to use.")
@click.option('--show-out/--no-show-out', default=False, help="show the output of the scorch instructions")
def run(config, show_out):
    logging.info("Using config file {}".format(str(config)))
    if show_out:
        robespierre.SHOW_OUT = True
    else:
        robespierre.SHOW_OUT = False
    runner.run(config=config)


def main():
    try:
        __version__ = version("robespierre")
        logging.info("Robespierre v{}".format(__version__))
    except PackageNotFoundError:
        # package is not installed
        logging.warning("Robespierre (unknown version). Is the package installed ?")

    cli()


if __name__ == '__main__':
    main()
