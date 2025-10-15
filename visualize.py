#! /usr/bin/env python

import sys
import argparse
from os import path
from tfviz.visualizer import Visualizer
import __main__


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Generate Mermaid sequence diagrams from TLS conversation trees',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  %(prog)s tlsfuzzer/scripts/test-tls13-obsolete-curves.py "sanity - HRR support"
        """
    )
    parser.add_argument(
        'script_path',
        help='Path to the tlsfuzzer test script'
    )
    parser.add_argument(
        'test_name',
        nargs='?',
        help='Name of the specific test to visualize (optional)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file for the diagram (default: stdout)'
    )

    return parser.parse_args()


args = parse_args()
script_path = args.script_path
OUTPUT_FILE = args.output  # Store output file for Runner to access
REPO_ROOT_DIR = path.dirname(path.dirname(script_path))
sys.path[:0] = [REPO_ROOT_DIR]

# Rebuild sys.argv with only the script path and test_name (if provided)
# This prevents visualizer arguments from interfering with tlsfuzzer script's getopt
new_argv = [sys.argv[0], script_path]
if args.test_name:
    new_argv.append(args.test_name)
sys.argv = new_argv

normalized_app_importable_base_name = path.splitext(
    path.basename(script_path),
)[0].replace('-', '_')
entry_points_importable_namespace = '.'.join(
    (
        'tlsfuzzer',
        '_apps',
    ),
)
entry_point_importable_path = '.'.join(
    (
        entry_points_importable_namespace,
        normalized_app_importable_base_name,
    ),
)

class Runner(object):
    """Test if sending a set of commands returns expected values"""

    def __init__(self, conversation):
        """Link conversation with runner

        Args:
            conversation: The conversation tree to visualize
        """
        self.visualizer = Visualizer(conversation)

    def run(self):
        """Execute conversation"""
        diagram = self.visualizer.generate()

        if OUTPUT_FILE:
            with open(OUTPUT_FILE, 'w') as f:
                f.write(diagram)
                f.write('\n')
            print(f"Diagram written to {OUTPUT_FILE}")
        else:
            print("-" * 60)
            print(diagram)
            print("-" * 60)

sys.modules['tlsfuzzer.runner'] = __main__

cli_app_module = __import__(
    entry_point_importable_path,
    fromlist=(entry_points_importable_namespace,),
)

cli_app_module.main()
