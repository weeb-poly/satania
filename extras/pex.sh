#!/bin/sh

pip freeze > requirements.txt

pex \
  --requirement=requirements.txt \
  -e app.loop \
  --sources-directory=. \
  --output-file=satania-loop.pex

pex \
  --requirement=requirements.txt \
  -e app.main \
  --sources-directory=. \
  --output-file=satania-main.pex

rm requirements.txt
