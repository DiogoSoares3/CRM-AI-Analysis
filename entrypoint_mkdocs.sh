#!/bin/sh

if [ -z "${GITHUB_TOKEN}" ]; then
    echo "GITHUB_TOKEN not found. Aborting..."
    exit 1
fi

git remote set-url origin https://${GITHUB_TOKEN}@github.com/DiogoSoares3/CRM-AI-Analysis.git

exec "$@"