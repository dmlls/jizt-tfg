#!/bin/bash

# Absolute path to the setup script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# If user interrupts installation, make sure we leave
# everything consistent.
trap tidy_up SIGINT  
tidy_up() {
    echo -e "\nInstallation aborted."
    echo -e "WARNING: Some components might have already been created."
    exit 1
}

print_welcome() {
    echo "THANK YOU for installing JIZT."
    echo "The installation process will take some time... But hey! Rome wasn't built"
    echo "in a day. We recommend that you go get a coffee and come visit later :)"
}

print_help() {
    echo    "Usage: setup [options]"
    echo -e "    JIZT Kubernetes installer.\n"
    echo    "    If no options are specified, a complete installation will be performed."
    echo -e "    That is, both Strimzi Kafka Operator and JIZT will be installed.\n"
    echo    "    Options:"
    echo    "      -p, --partial            install only JIZT components"
}

if [[ "$1" == "-h" || "$1" == "--help"  ]]; then
    print_help
    exit 0
fi

if [[ $# == 0 ]]; then
    print_welcome
    ./_install_strimzi_operator.sh
    ./_install_jizt.sh
else
    while [[ $# > 0 ]]; do
        key="$1"
        case $key in
            -p|--partial)
            print_welcome
            ./_install_jizt.sh
            shift # past argument
            shift # past value
            ;;
            *)    # unknown option
            echo "setup: invalid option '$1'"
            echo "See 'setup --help' for usage."
            exit 1
            ;;
        esac
    done
fi

echo -e "\n> Everything ready, done installing!"
