#!/usr/bin/env bash

input=$1
intepreter=$2
from=$3
to=$4
sub_to=$((to - 1))

if [ $UID != 0 ]; then

  for N in $(seq $from $sub_to); do
    sudo $intepreter multiprocess_runner.py -i "$input" -n "$N"
  done

  sudo $intepreter multiprocess_runner.py -i "$input" -n $to
fi
