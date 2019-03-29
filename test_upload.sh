#!/usr/bin/env bash
rm -rf dist/*
python3 setup.py sdist bdist_egg
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
