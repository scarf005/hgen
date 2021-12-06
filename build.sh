#!/bin/bash

rm dist/*

python3 semver.py Patch

python3 -m build
python3 -m twine upload --repository testpypi dist/*
