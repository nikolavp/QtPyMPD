#!/usr/bin/env python3.1
# vim: set sw=4 sts=4 et foldmethod=indent :

import unittest

modules_to_test = {
    "gui_test"
}


def suite():
    alltests = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
