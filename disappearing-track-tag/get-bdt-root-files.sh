#!/bin/env bash

echo "Getting BDT output.root files..."

COPYFROM=/afs/desy.de/user/k/kutznerv/dust/shorttrack/analysis/disappearing-track-tag/

for D in `find . -maxdepth 1 -type d`
do
	if [[ $D == *"201"* ]]; then
      echo $D
	  cp $COPYFROM/$D/output.root $D/output.root
    fi
done