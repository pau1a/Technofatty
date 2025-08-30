#!/usr/bin/env bash
set -e

CSS_FILE="node_modules/bootstrap/dist/css/bootstrap.min.css"
JS_FILE="node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"

CSS_SIZE=$(stat -c%s "$CSS_FILE")
JS_SIZE=$(stat -c%s "$JS_FILE")

MAX_CSS=$((250 * 1024))
MAX_JS=$((90 * 1024))

if [ "$CSS_SIZE" -gt "$MAX_CSS" ]; then
  echo "::warning file=$CSS_FILE::CSS bundle size exceeds budget (${CSS_SIZE} bytes > ${MAX_CSS} bytes)"
fi

if [ "$JS_SIZE" -gt "$MAX_JS" ]; then
  echo "::warning file=$JS_FILE::JS bundle size exceeds budget (${JS_SIZE} bytes > ${MAX_JS} bytes)"
fi
