#!/usr/bin/python

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import subprocess

import i3sub.i3sub as app

HERE = os.path.dirname(__file__)

def make_readme_text():
    parser = app.build_parser()
    help_text = parser.format_help()
    with open('README.md.template') as stream:
        return '<!-- This is generated by make-readme.py do not edit -->\n' + stream.read().format(
            usage=help_text,
        )

def backticks(command, stdin=None, shell=False):
    stdin_arg = subprocess.PIPE if stdin is not None else None
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=stdin_arg, shell=shell)
    result, _ = process.communicate(stdin)
    if process.returncode != 0:
        raise Exception('{!r} returned non-zero return code {!r}'.format(command, process.returncode))
    result = result.decode('utf8')
    return result

def main():
    PARSER = argparse.ArgumentParser(description='Write readme.md')
    PARSER.add_argument('--stdout', action='store_true', help='Write to standard out rather than README.md')
    options = PARSER.parse_args()
    output = make_readme_text()
    if options.stdout:
        print(output, end='')
    else:
        with open('README.md', 'w') as out_stream:
            out_stream.write(output)

if __name__ == '__main__':
	main()
