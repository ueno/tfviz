#! /usr/bin/env python

import sys
from os import path
from tfviz.visualizer import Visualizer
import __main__

script_path = sys.argv[1]
REPO_ROOT_DIR = path.dirname(path.dirname(script_path))
sys.path[:0] = [REPO_ROOT_DIR]

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
        """Link conversation with runner"""
        self.visualizer = Visualizer(conversation)

    def run(self):
        """Execute conversation"""
        print("-" * 60)
        print(self.visualizer.generate())
        print("-" * 60)

sys.modules['tlsfuzzer.runner'] = __main__

cli_app_module = __import__(
    entry_point_importable_path,
    fromlist=(entry_points_importable_namespace,),
)

cli_app_module.main()
