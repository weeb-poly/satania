#!/bin/sh

pip freeze > requirements.txt

pex \
  --requirement=requirements.txt \
  -e app.loop \
  --sources-directory=. \
  --output-file=satania-loop.pex

pex \
  --requirement=requirements.txt \
  -e app.once \
  --sources-directory=. \
  --output-file=satania-once.pex

rm requirements.txt
