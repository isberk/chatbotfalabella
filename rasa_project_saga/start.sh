#!/usr/bin/env bash
rasa run --enable-api --cors "*" --interface 0.0.0.0 --port $PORT
