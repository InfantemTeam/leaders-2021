#!/bin/sh

exec env PYTHONPATH=.. hypercorn ${PWD##*/}.app:app
