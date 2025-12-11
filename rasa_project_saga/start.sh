#!/usr/bin/env bash
set -e

echo "PORT=$PORT"

rasa run \
  --enable-api \
  --cors "*" \
  --interface 0.0.0.0 \
  --port $PORT
