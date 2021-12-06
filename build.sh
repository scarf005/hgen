#!/bin/bash

rm dist/*

python3 semver.py Minor

python3 -m build
python3 -m twine upload dist/*
python3 -m twine upload --repository testpypi dist/*
pip3 install --upgrade hgen