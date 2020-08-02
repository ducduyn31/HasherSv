#!/usr/bin/env bash

find . -depth -execdir bash -c 'mv "$0" "${0// /_}"' {} \;
