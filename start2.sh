#!/usr/bin/env bash

input=$1

if [ $UID != 0 ]; then

  while IFS= read -r line; do
    for N in {1..999}; do
      sudo python3 multiprocess_runner.py -i "$line" -n "$N"
    done

    sudo python3 multiprocess_runner.py -i "$line" -n 1000
  done <"$input"
fi