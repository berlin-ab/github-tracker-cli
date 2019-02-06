 #!/usr/bin/env bash


set -e


LOG_FILE=/tmp/github-tracker-cli-build.log
rm -f $LOG_FILE # cleanup previous run


# install dependencies
pip install -r requirements.txt
pip install -r requirements-development.txt


# run test suites
./scripts/unit-test.sh
./scripts/code-quality-check.bash
./scripts/integration-test.sh


# run examples
./scripts/example-missing-stories.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed.' && false)
./scripts/example-missing-stories-csv.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed.' && false)
./scripts/example-closed-issues.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed' && false)
./scripts/example-pull-requests.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed' && false)
