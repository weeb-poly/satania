#!/usr/bin/env bash

rm satania-loop.pyz satania-once.pyz

pip install -r <(pipenv lock -r) --target dist/

cp -r -t dist app

shiv \
  --site-packages dist \
  --uncompressed \
  --reproducible \
  -p '/usr/bin/env python3' \
  -o satania-loop.pyz \
  -e app.loop:cli

shiv \
  --site-packages dist \
  --uncompressed \
  --reproducible \
  -p '/usr/bin/env python3' \
  -o satania-once.pyz \
  -e app.once:cli

rm -r dist
