#!/usr/bin/env python3
"""
Test runner for AWS Cost Explorer package.
Run with: python run_tests.py
"""

import unittest
import sys


if __name__ == "__main__":
    # Discover and run all tests
    test_suite = unittest.defaultTestLoader.discover('aws_cost_explorer/tests')
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return non-zero exit code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)