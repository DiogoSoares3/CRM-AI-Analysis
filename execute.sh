#!/bin/bash

streamlit run ${PROJECT_PATH}/app/ui/home.py --server.port 8210 --logger.level=debug --server.runOnSave true --theme.base dark &
uvicorn main:app --host 0.0.0.0 --port 8200 --reload --log-level info &

while ! nc -z localhost 8200; do
    echo "Waiting API start up"
    sleep 1
done
echo "API successfully initialized!"
curl -s -X POST "http://localhost:8200/api/insert-init-data/"
curl -s -X GET "http://localhost:8200/api/serve-dbt-docs/"

tail -f /dev/null
