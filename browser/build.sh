#!/usr/bin/env sh
set -eu
destination=${1:?Usage: sh browser/build.sh OUTPUT_DIRECTORY}
mkdir -p "$destination"
destination=$(cd "$destination" && pwd)
cd "$(dirname "$0")/.."
mkdir -p "$destination"/src/signature "$destination"/demo "$destination"/docs
cp browser/index.html browser/dashboard.js app.py "$destination"/
cp src/__init__.py "$destination"/src/
cp src/signature/__init__.py src/signature/rules.py "$destination"/src/signature/
cp demo/sample_flows.csv "$destination"/demo/
cp docs/week*.png "$destination"/docs/
