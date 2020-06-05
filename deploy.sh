#!/bin/bash -eu

SCRIPT_DIR=$(cd $(dirname $0); pwd)

echo "Script dir is ${SCRIPT_DIR}"

cd ${SCRIPT_DIR}

rm -rf ${SCRIPT_DIR}/build/*
pip install --target ./build -r requirements.txt

rsync -a -exclude=.git --exclude=package --exclude=deploy.sh --exclude=requirements.txt --exclude=function.zip --exclude=build ${SCRIPT_DIR}/. ${SCRIPT_DIR}/build/

read -p "Deploy to AWS Lambda ? (y/N): " yn
case "$yn" in [yY]*) ;; *) echo "Abort." ; exit ;; esac

echo "Deploy to lambda using lambroll"

cd ${SCRIPT_DIR}/build
lambroll deploy --region us-west-2