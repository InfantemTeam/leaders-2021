#!/bin/sh

set -e

[ -e '.venv' ] || python3 -m venv '.venv'

source .venv/bin/activate

exec pip3 install --disable-pip-version-check -Uqr requirements.txt
