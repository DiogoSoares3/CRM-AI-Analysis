#!/bin/bash

streamlit run ${PROJECT_PATH}/app/ui/home.py --server.port 8210 --logger.level=debug --server.runOnSave true --theme.base dark &
# mkdocs serve -a 0.0.0.0:8220 &
uvicorn main:app --host 0.0.0.0 --port 8200 --reload --log-level info &

while ! nc -z localhost 8200; do
    echo "Waiting API start up"
    sleep 1
done
echo "API successfully initialized!"
curl -s -X POST "http://localhost:8200/api/insert-init-data/"

tail -f /dev/null
