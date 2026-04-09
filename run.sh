#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
source venv/bin/activate
cd backend
python manage.py runserver 0.0.0.0:8000
