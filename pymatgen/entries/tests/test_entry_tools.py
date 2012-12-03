#!/usr/bin/env python

"""
FIXME: Proper module docstring
"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyue@mit.edu"
__date__ = "Nov 9, 2012"

import unittest
import os
import json

from pymatgen.serializers.json_coders import PMGJSONDecoder
from pymatgen.entries.entry_tools import group_entries_by_structure

test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                        'test_files')


class FuncTest(unittest.TestCase):

    def test_group_entries_by_structure(self):
        with open(os.path.join(test_dir, "TiO2_entries.json"), "r") as f:
            entries = json.load(f, cls=PMGJSONDecoder)
        groups = group_entries_by_structure(entries, symmetry_tol=0.1)
        self.assertEqual(sorted([len(g) for g in groups]),
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4])
        self.assertLess(len(groups), len(entries))
        #Make sure no entries are left behind
        self.assertEqual(sum([len(g) for g in groups]), len(entries))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
