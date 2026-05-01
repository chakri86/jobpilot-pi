#!/usr/bin/env sh
set -eu

cd backend
ruff check app tests
pytest
cd ../frontend
npm install
npm run build
