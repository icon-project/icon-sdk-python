#!/bin/bash
set -e

PYVER=$(python -c 'import sys; print(sys.version_info[0])')
if [ $PYVER -ne 3 ]
then
    echo "The script should be run on python3"
    exit 1
fi

if [ $# -eq 1 ]
then
    echo $1 > ./VERSION
fi

pip install wheel
rm -rf build dist *.egg-info
python setup.py sdist bdist_wheel