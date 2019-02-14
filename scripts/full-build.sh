#!/usr/bin/env bash

for version in 2.7.15 3.6.8; do
    echo "Running tests for python version: $version"
    pyenv local $version
    ./scripts/build.sh;
done;
