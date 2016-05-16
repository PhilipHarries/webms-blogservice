#!/usr/bin/env bash

echo "Setting up tests..."

cd $( dirname $0 )

export PYTHONPATH='../../'

if [[ ! -d ./venv ]];then
    rm -f ./venv
    mkdir ./venv
    virtualenv ./venv
fi

. venv/bin/activate

[[ -f ./requirements.txt ]] && pip install -r ./requirements.txt > /tmp/testsetup.out.$$ 2>&1
[[ -f ./requirements_gunicorn.txt ]] && pip install -r ./requirements_gunicorn.txt > /tmp/testsetup.out.$$ 2>&1
[[ -f ./requirements_tests.txt ]] && pip install -r ./requirements_tests.txt > /tmp/testsetup.out.$$ 2>&1

echo "Starting test instance of webserver..."

./start.sh >/tmp/testserver.out.$$ 2>&1

sleep 2

netstat -na | grep 5434

cd tests

echo "Starting test suite..."

py.test

cd ..

echo "stopping test instance of webserver..."

./stop.sh

echo "Tests complete"
