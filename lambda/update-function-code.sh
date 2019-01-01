#!/usr/bin/env bash

pip3 install awscli --upgrade
mkdir package
cd package
pip3 install paramiko -t .
zip -r ../function.zip .
cd ..
zip -g function.zip function.py
aws lambda update-function-code --function-name startNetkeibaPipeline --zip-file fileb://function.zip
