#!/usr/bin/env bash
set -e
docker build -t pull-reminder .
docker run \
    -it \
    -e GITHUB_API_TOKEN=$1 \
    -e GITHUB_INGORE_LABELS=hold \
    -e GITHUB_IGNORE_TITLE_WORDS=WIP \
    -e GITHUB_ORGANIZATION=piratestudios \
    -e SLACK_API_TOKEN=$2 \
    -e SLACK_CHANNEL=\#dev-chat \
    pull-reminder
