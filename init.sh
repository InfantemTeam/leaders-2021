#!/bin/sh

set -e

[ -e '.venv' ] || python -m venv '.venv'

source .venv/bin/activate

exec pip install --disable-pip-version-check -Uqr requirements.txt
