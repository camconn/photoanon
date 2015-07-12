#!/usr/bin/env python3

import unittest

def test_suite():
    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover('.')
    return test_suite
