#!/bin/sh

source .venv/bin/activate

exec env PYTHONPATH=.. hypercorn ${PWD##*/}.app:app
