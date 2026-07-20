#!/usr/bin/python3
# test-lp-fetch.py - manually test fetching a pruned source version from
# Launchpad
#
# This is a standalone diagnostic script, not part of the daily cron
# pipeline. Run it directly on the merges server to check whether
# fetch_source_from_launchpad() can retrieve a specific package version
# that is no longer present in the local pool / archive mirror, e.g.:
#
#   ./test-lp-fetch.py publicfile 0.52-14
#   ./test-lp-fetch.py --distro debian publicfile 0.52-14

import logging

from momlib import fetch_source_from_launchpad, get_pool_source, run


def options(parser):
    parser.add_option(
        "--distro",
        type="string",
        metavar="DISTRO",
        default="debian",
        help="Distribution to fetch the source from (default: debian)",
    )


def main(options, args):
    if len(args) != 2:
        raise SystemExit("Usage: test-lp-fetch.py [--distro DISTRO] PACKAGE VERSION")

    package, version = args

    logging.info("Fetching %s %s from Launchpad (%s)", package, version, options.distro)
    fetch_source_from_launchpad(options.distro, package, version)

    source = get_pool_source(options.distro, package, version)
    logging.info("Success, pool now has: %s", source)


if __name__ == "__main__":
    run(
        main,
        options,
        usage="%prog [--distro DISTRO] PACKAGE VERSION",
        description="test fetching a source package version from Launchpad",
    )
