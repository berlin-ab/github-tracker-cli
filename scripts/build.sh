 #!/usr/bin/env bash


set -e


print_python_version() {
    python --version
}


log() {
    echo
    echo $1
    echo
}


run_example() {
    local example_script=$1;

    $example_script >> $LOG_FILE && \
	(echo "Passed $example_script") || \
        (echo "Failed $example_script" && false);
}


setup_log_file() {
    log "clean before running suite"
    LOG_FILE=/tmp/github-tracker-cli-build.log
    rm -f $LOG_FILE # cleanup previous run
    find . -name *.pyc | xargs --no-run-if-empty rm;
    find . -name __pycache__ | xargs --no-run-if-empty rm -rf;
}


install_production_dependencies() {
    pip install -r requirements.txt >> $LOG_FILE && \
	(echo "Success.") || \
        (echo "Failed to install dependencies" && false);
}


install_development_dependencies() {
    pip install -r requirements-development.txt >> $LOG_FILE && \
	(echo "Success.") || \
	(echo "Failed to install dev dependencies" && false);    
}


install_dependencies() {
    install_production_dependencies
    install_development_dependencies
}


run_unit_tests() {
    ./scripts/unit-test.sh
}


run_code_quality_check() {
    ./scripts/code-quality-check.bash
}


run_integration_tests() {
    ./scripts/integration-test.sh
}


run_examples() {
    run_example "./examples/example-missing-stories.bash"
    run_example "./examples/example-missing-stories-csv.bash"
    run_example "./examples/example-closed-issues.bash"
    run_example "./examples/example-pull-requests.bash"
    run_example "./examples/example-tracker-story-history.bash"
    run_example "./examples/example-github-issues.bash"
}


main() {
    export PYTHONIOENCODING=utf_8
    setup_log_file
    print_python_version

    log "install dependencies"
    install_dependencies

    log "run code quality check"
    run_code_quality_check
    
    log "run test suites"
    run_unit_tests
    run_integration_tests
    run_examples
}


main "$@"
