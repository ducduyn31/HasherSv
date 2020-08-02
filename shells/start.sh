#!/usr/bin/env bash

input=$1

while IFS= read -r line; do
  for N in 1 2 3 4 5 6 7 8 9; do
    python runner.py -i "$line" -n "$N"
  done

  python runner.py -i "$line" -n 10 -r
done <"$input"
