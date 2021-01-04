#!/bin/sh

podman build -t ghcr.io/weeb-poly/satania .

# TODO: Add Cred Volume

podman create \
    --env "GCAL_ID=${GCAL_ID}" \
    --env "WEBHOOK_URL=${WEBHOOK_URL}" \
    --env "PING_ROLE=${PING_ROLE}" \
#    --mount "type=bind,source=${SYNCPLAY_TLS_PATH}/privkey.pem,target=/app/cert/privkey.pem,ro=true" \
    --name satania \
    ghcr.io/weeb-poly/satania

podman start satania
