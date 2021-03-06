"""
Imports from a URL and saves a new temp file for import

Custom arguments:
id -- the import scene identifier
url -- the url to the import file
"""

import sys

from argparse import ArgumentParser
from os import chdir, path

elmyra_root = path.dirname(path.realpath(__file__))

# Make elmyra's root dir the current working directory (could be anything else)
chdir(elmyra_root)

# Add elmyra's root dir to sys.path (this script runs from blender context)
sys.path.append(elmyra_root)

import common
import update


def parse_custom_args():
    parser = ArgumentParser(prog="Elmyra Import Params")

    parser.add_argument("--id", required=True)
    parser.add_argument("--url", required=True)

    custom_args = sys.argv[sys.argv.index("--") + 1:]

    return parser.parse_args(custom_args)

args = parse_custom_args()

common.empty_scene()
update.import_model(args.url, args.id)
