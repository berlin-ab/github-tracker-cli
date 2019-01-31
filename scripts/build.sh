#!/usr/bin/env bash

set -e

pip install -r requirements.txt
pip install -r requirements-development.txt

./scripts/unit-test.sh
./scripts/code-quality-check.bash

./scripts/integration-test.sh

./scripts/example-missing-stories.bash
./scripts/example-missing-stories-csv.bash
./scripts/example-closed-issues.bash
