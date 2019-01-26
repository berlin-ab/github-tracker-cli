#!/usr/bin/env bash

set -e

pip install -r requirements.txt

./scripts/unit-test.sh

./scripts/integration-test.sh
