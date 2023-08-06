# -*- coding: utf-8 -*-

"""Spatial analysis feature.

"""

from logging import getLogger


logger = getLogger(__name__)


def setup(parser):
    """Configure the parser for the module.

    Parameters
    ----------
    parser : ArgumentParser
        Parser dedicated to the module.

    """
    logger.debug("defining command-line arguments")
    parser.set_defaults(
        func=main,
    )


def main(**kwargs):
    """Analize.

    """
    _ = kwargs
