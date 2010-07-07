#!/bin/bash
# vim: set sw=4 sts=4 et foldmethod=indent :
#This script run the all test suites just by 
#hitting enter on the window console.
while true;do 
    python3.1 src/mpdclient/all_tests.py
    read
done

