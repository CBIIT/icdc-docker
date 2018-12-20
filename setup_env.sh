#!/bin/bash
# Script to setup all configuration file

file="./apis_configs/env.properties" 

if [ -f "$file" ]
then
  echo "$file found."

  while IFS='=' read -r key value
  do
    key=$(echo $key | tr '.' '_')
    eval ${key}=\${value}
  done < "$file"
  echo "${ICDCHOST}"
  if [ -f ./apis_configs/fence_creds.json ]
  then
    cp ./apis_configs/fence_creds.json ./apis_configs/fence_creds.json.bak
  fi
  cp ./apis_configs/fence_creds.json.template ./apis_configs/fence_creds.json
  sed -i -e "s/ICDCHOST/${ICDCHOST}/g" ./apis_configs/fence_creds.json
  sed -i -e "s/GOOGLE_C_SECRET/${GOOGLE_C_SECRET}/g" ./apis_configs/fence_creds.json
  sed -i -e "s/GOOGLE_C_ID/${GOOGLE_C_ID}/g" ./apis_configs/fence_creds.json

  if [ -f ./apis_configs/fence_credentials.json ]
  then
    cp ./apis_configs/fence_credentials.json ./apis_configs/fence_credentials.json.bak
  fi
  cp ./apis_configs/fence_credentials.json.template ./apis_configs/fence_credentials.json
  sed -i -e "s/AWS_ACCESS_KEY_ID/${AWS_ACCESS_KEY_ID}/g" ./apis_configs/fence_credentials.json
  sed -i -e "s/AWS_SECRET_ACCESS_KEY/${AWS_SECRET_ACCESS_KEY}/g" ./apis_configs/fence_credentials.json
  sed -i -e "s/S3_BUCKET_NAME/${S3_BUCKET_NAME}/g" ./apis_configs/fence_credentials.json
  sed -i -e "s/AWS_ROLE_ARN/${AWS_ROLE_ARN}/g" ./apis_configs/fence_credentials.json

  if [ -f ./apis_configs/fence_settings.py ]
  then
    cp ./apis_configs/fence_settings.py ./apis_configs/fence_settings.py.bak
  fi
  cp ./apis_configs/fence_settings.py.template ./apis_configs/fence_settings.py
  sed -i -e "s/INDEXD_HOST/${INDEXD_HOST}/g" ./apis_configs/fence_settings.py

  if [ -f ./apis_configs/sheepdog_settings.py ]
  then
    cp ./apis_configs/sheepdog_settings.py ./apis_configs/sheepdog_settings.py.bak
  fi
  cp ./apis_configs/sheepdog_settings.py.template ./apis_configs/sheepdog_settings.py
  sed -i -e "s/INDEXD_HOST/${INDEXD_HOST}/g" ./apis_configs/sheepdog_settings.py

  if [ -f ./apis_configs/peregrine_settings.py ]
  then
    cp ./apis_configs/peregrine_settings.py ./apis_configs/peregrine_settings.py.bak
  fi
  cp ./apis_configs/peregrine_settings.py.template ./apis_configs/peregrine_settings.py
  sed -i -e "s/INDEXD_HOST/${INDEXD_HOST}/g" ./apis_configs/peregrine_settings.py

  if [ -f ./apis_configs/sheepdog_creds.json ]
  then
    cp ./apis_configs/sheepdog_creds.json ./apis_configs/sheepdog_creds.json.bak
  fi
  cp ./apis_configs/sheepdog_creds.json.template ./apis_configs/sheepdog_creds.json
  sed -i -e "s/ICDCHOST/${ICDCHOST}/g" ./apis_configs/sheepdog_creds.json

  if [ -f ./apis_configs/peregrine_creds.json ]
  then
    cp ./apis_configs/peregrine_creds.json ./apis_configs/peregrine_creds.json.bak
  fi
  cp ./apis_configs/peregrine_creds.json.template ./apis_configs/peregrine_creds.json
  sed -i -e "s/ICDCHOST/${ICDCHOST}/g" ./apis_configs/peregrine_creds.json
else
  echo "$file not found."
fi
