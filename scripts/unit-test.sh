#!/usr/bin/env bash

find . -name *.pyc | xargs rm
nosetests --rednose -s test/**/*.py
