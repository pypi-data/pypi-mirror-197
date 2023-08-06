"""
This is a main file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = dragtooth.main:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

from dragtooth import __version__

from . import lib

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

package = __name__.split(".")[0]


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from dragtooth.main import fib`,
# when using this Python module as a library.

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--version",
        action="version",
        version="dragtooth {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-d",
        "--prevent-crash-delay",
        default="0s",
        required=False,
        help="delay fetches to prevent sls crash (eg, 2m, 60s, 1h)",
    )
    parser.add_argument(
        "-c",
        "--session-count",
        type=int,
        default=5,
        required=False,
        metavar="INT",
        help="how many session do you want to create or fetch?",
    )
    parser.add_argument(
        "-l",
        "--session-lifetime",
        type=str,
        default="60s",
        required=False,
        help="session lifetime in units like this, eg 10s, 1m, 1d, 1h30s, ...",
    )
    parser.add_argument(
        "-g",
        "--update-geolocation",
        action="store_true",
        help="map ip address to region",
        default=False,
        required=False,
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "{%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(
        level=loglevel,
        format=logformat,
        handlers=[
            # logging.FileHandler(f"{package}.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting script...")
    lib.main(args)
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m dragtooth.main 42
    #
    run()
