#! /usr/bin/env bash

{ printf 'files=(\n'; ls -1 *.sh; printf ')\n'; } | sed '2,$s/.*/  "&"/'

