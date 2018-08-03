#!/bin/bash

# Project specific properties
export DJANGO_SETTINGS_MODULE=django_multi_factor_authentication.settings.test

feedback_loop(){
    cmd=$*
    if which inotifywait; then
        while true; do
            clear;
            sh -c "$cmd";
            echo "Waiting for file changes";
            inotifywait --exclude='.*\.log' -qre modify *;
            sleep 1;
        done;
    else
        export LC_NUMERIC="en_US.UTF-8"
        watch -c -n 0.1 -- "$cmd"
    fi;
}

verbosity=0
parallel="--parallel"

while getopts "1h" opt; do
  case $opt in
    1) RUN_ONCE=1;;
    h) usage;;
  esac
done

shift $((OPTIND-1))

if [ -z "$VIRTUAL_ENV" ]; then
	if [ -e "../bin/activate" ]; then
		echo "Activating your environment for you"
		. ../bin/activate
	else
		echo "Please activate your environment first!"
		exit 1
	fi
fi

cmd="
set -e
python manage.py test $parallel --verbosity=$verbosity $*
echo"

if [ -z $RUN_ONCE ]; then
    feedback_loop "$cmd"
else
    sh -c "$cmd"
fi
