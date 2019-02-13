 #!/usr/bin/env bash


set -e


python --version


log() {
    echo
    echo $1
    echo
}


export PYTHONIOENCODING=utf_8


log "clean before running suite"
LOG_FILE=/tmp/github-tracker-cli-build.log
rm -f $LOG_FILE # cleanup previous run
find . -name *.pyc | xargs --no-run-if-empty rm;
find . -name __pycache__ | xargs --no-run-if-empty rm -rf;



log "install dependencies"
pip install -r requirements.txt >> $LOG_FILE && echo "Success." || (echo "Failed to install dependencies" && false)
pip install -r requirements-development.txt >> $LOG_FILE && echo "Success." || (echo "Failed to install dev dependencies" && false)


log "run test suites"
./scripts/unit-test.sh
./scripts/code-quality-check.bash
./scripts/integration-test.sh


log "run examples"
./scripts/example-missing-stories.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed.' && false)
./scripts/example-missing-stories-csv.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed.' && false)
./scripts/example-closed-issues.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed' && false)
./scripts/example-pull-requests.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed' && false)

