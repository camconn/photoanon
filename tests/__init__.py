#!/usr/bin/env python3

import unittest

if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader()
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover('.')
    test_runner.run(test_suite)
