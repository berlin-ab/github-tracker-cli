 #!/usr/bin/env bash


set -e

log() {
    echo
    echo $1
    echo
}


log "clean before running suite"
LOG_FILE=/tmp/github-tracker-cli-build.log
rm -f $LOG_FILE # cleanup previous run


log "install dependencies"
pip install -r requirements.txt
pip install -r requirements-development.txt


log "run test suites"
./scripts/unit-test.sh
./scripts/code-quality-check.bash
./scripts/integration-test.sh


log "run examples"
./scripts/example-missing-stories.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed.' && false)
./scripts/example-missing-stories-csv.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed.' && false)
./scripts/example-closed-issues.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed' && false)
./scripts/example-pull-requests.bash >> $LOG_FILE && echo "Passed." || (echo 'Failed' && false)

