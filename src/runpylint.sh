#!/bin/bash
# vim: set sw=4 sts=4 et foldmethod=indent :

# Specify which files to ignore when checking them with pylint, delimiter is the semicolon
# Caution don't leave a semicolon at the end because it will break the script after
IGNORED="main_window.py"



IGNORED=$(echo $IGNORED | tr ";" "|")

FILES=$(find . | grep -v -E $IGNORED | grep -E py$)

pylint $FILES
