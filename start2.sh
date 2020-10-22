#!/usr/bin/env bash

input=$1
intepreter=$2

if [ $UID != 0 ]; then

  for N in {1..999}; do
    sudo $intepreter multiprocess_runner.py -i "$input" -n "$N"
  done

  sudo $intepreter multiprocess_runner.py -i "$input" -n 1000
fi
