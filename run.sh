#!/bin/bash

source ./.venv/bin/activate
python3 ./src/App.py 2>error.log &
deactivate
