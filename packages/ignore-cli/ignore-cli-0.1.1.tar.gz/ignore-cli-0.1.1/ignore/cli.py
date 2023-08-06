# -*- coding: utf-8 -*-

"""Console script for ignoreCLI."""
import sys
import argparse
from .ignore import IgnoreCLI

def main():
    parser = argparse.ArgumentParser(
        description='Create and update .gitignore.')
    parser.add_argument('templates', type=str, nargs='+',
                        help='a template name.')
    args = parser.parse_args()

    templates = args.templates
    gitignore = IgnoreCLI()

    if len(templates) > 0:
        if not gitignore.gitignore_existed():
            print('Creating .gitignore file.')
            gitignore.create_gitignore()
            print('.gitignore file created.')

        for template in templates:
            gitignore.update_gitignore(template)
        print('Done.')

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
