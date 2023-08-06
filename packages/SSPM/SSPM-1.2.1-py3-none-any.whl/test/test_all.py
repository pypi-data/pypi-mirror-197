import sys
import os
import unittest
from pathlib import Path
from . import test_plugin_manager

# set correct loading path for test files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

MainTestSuite = unittest.TestSuite(
    [  # add the tests suites below
        test_plugin_manager.suite
    ])
