#!/bin/bash

set -e  # Exit on error

RUN_ONLY=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    -r|--run)
      RUN_ONLY=true
      shift
      ;;
  esac
done

if [ "$RUN_ONLY" = true ]; then
  echo "Starting development server only..."
  uv run python manage.py runserver
  exit 0
fi

echo "Running makemigrations..."
uv run python manage.py makemigrations

echo "Running migrate..."
uv run python manage.py migrate

echo "Starting development server..."
uv run python manage.py runserver