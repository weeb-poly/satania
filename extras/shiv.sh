#!/usr/bin/env bash

shiv_build () {
  local PYZ_FILE=$1
  local PY_ENTRY=$2

  [ ! -e "${PYZ_FILE}" ] || rm "${PYZ_FILE}"

  shiv \
    --site-packages dist \
    --uncompressed \
    --reproducible \
    -p '/usr/bin/env python3' \
    -o "${PYZ_FILE}" \
    -e "${PY_ENTRY}"
}


pip install -r <(pipenv lock -r) --target dist/

cp -r -t dist app

shiv_build "satania-loop.pyz" "app.loop:cli"
shiv_build "satania-once.pyz" "app.once:cli"

rm -r dist
