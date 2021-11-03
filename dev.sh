#!/bin/sh

while true; do
	PYTHONPATH=.. python3 -m ${PWD##*/}
	printf '\r\e[K\e[2mPress ^C to exit now:\e[0m '
	sleep 1s || break  # allow for ^C
	printf '\r\e[K'
done
