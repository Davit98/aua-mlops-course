#!/bin/bash

set -e

exec python prepare_db.py &  # Creates a table in the database (runs in the background).
exec python openapi_main.py  # Runs the API.