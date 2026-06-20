#!/bin/bash
set -e
cd frontend
npm install
npm run build
npx serve -s build -l "$PORT"
