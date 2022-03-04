#!/bin/bash

TYPE=$1

cleanup() {
  rm dist/* 2> /dev/null
}

setup_semver () {
  TYPE=$1
  python3 semver.py $TYPE
}

build () {
  python3 -m build
}

upload () {
  python3 -m twine upload dist/*
  # python3 -m twine upload --repository testpypi dist/*
}

refresh () {
  sleep 1
  pip3 install --upgrade hgen
  asdf reshim
}

push () {
  git commit -am "release@$VER"
  git tag -a $VER -m "release@$VER"
  git push
}


cleanup
VER="v$(setup_semver $TYPE)"
build
upload
refresh
push