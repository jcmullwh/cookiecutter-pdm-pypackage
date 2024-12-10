#! /bin/bash

set -e

pip install pdm

pdm install

pdm add --dev --editable .
