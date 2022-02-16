#!/bin/bash

VER=$1

cleanup() {
  rm dist/*
}

setup_semver () {
  VER=$1
  python3 semver.py $VER
}

build () {
  python3 -m build
}

upload () {
  python3 -m twine upload dist/*
  python3 -m twine upload --repository testpypi dist/*
}

refresh () {
  pip3 install --upgrade hgen
  asdf reshim
}

cleanup
setup_semver $VER
build
upload
refresh