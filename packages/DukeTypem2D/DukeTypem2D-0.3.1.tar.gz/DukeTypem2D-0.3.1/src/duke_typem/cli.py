import logging
import sys

import click

from . import __version__

logger = logging.getLogger("dukeTypem.cli")
verbose_level = 2


def config_logger(verbose: int) -> None:
    # TODO: put in __init__, provide logger, ditch global var
    if verbose == 0:
        logger.setLevel(logging.ERROR)
    elif verbose == 1:
        logger.setLevel(logging.WARNING)
    elif verbose == 2:
        logger.setLevel(logging.INFO)
    elif verbose > 2:
        logger.setLevel(logging.DEBUG)
    global verbose_level
    verbose_level = verbose
    logging.basicConfig(format="%(message)s")  # reduce internals


@click.group(context_settings={"help_option_names": ["-h", "--help"], "obj": {}})
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="4 Levels [0..3](Error, Warning, Info, Debug)",
)
@click.pass_context
def cli(ctx: click.Context, verbose: int) -> None:
    """Duke Typem 2D: Improve readability, spelling and expression of your text documents

    Args:
        ctx:
        verbose:
    """
    config_logger(verbose)
    click.echo("Program v%s", __version__)
    logger.debug("Python v%s", sys.version)
    logger.debug("Click v%s", click.__version__)
    if not ctx.invoked_subcommand:
        click.echo("Please specify a valid command")
