#! /bin/bash

echo "Installing npm & serverless dependencies"
npm init -y
# Make sure serverless is installed first
# npm i -g serverless
# npm i -g serverless
serverless plugin install -n serverless-python-requirements@4.1.1 serverless-wsgi


# echo "###Replacing plugin section in serverless"

# sed -i  "" "s/\##plugin_name_1/\- serverless-python-requirements/g" serverless.yml
# sed -i "" "s/\#service_name/service: iot-basic-\$\{env\:LINKER_NAME\}/g" serverless.yml