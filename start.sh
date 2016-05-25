#!/usr/bin/env bash
cd $( dirname $0 )
if [[ ! -d ./venv ]];then
    rm -f ./venv
    mkdir ./venv
    virtualenv ./venv > /dev/null 2>&1
fi
if [[ ! -d ./logs ]];then
    mkdir ./logs
fi
if [[ ! -f ./logs/blogservice.log ]];then
    touch ./logs/blogservice.log
fi
. venv/bin/activate
[[ -f ./requirements.txt ]] && pip install -r ./requirements.txt >/dev/null 2>&1
python manage.py runserver &
