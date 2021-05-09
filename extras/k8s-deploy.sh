#!/bin/sh

kubectl create \
  secret generic satania-secret \
  --namespace="satania" \
  --from-file=google-key=./secret/creds.json \
  --from-literal=discord-webhook="${WEBHOOK_URL}"

kubectl label \
  secret satania-secret \
  "app.kubernetes.io/part-of=satania" \
  --namespace="satania"
