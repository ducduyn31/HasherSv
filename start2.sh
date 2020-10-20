#!/usr/bin/env bash

input=$1
intepreter=$2

if [ $UID != 0 ]; then

  while IFS= read -r line; do
    for N in {1..999}; do
      sudo $intepreter multiprocess_runner.py -i "$line" -n "$N"
    done

    sudo $intepreter multiprocess_runner.py -i "$line" -n 1000
  done <"$input"
fi