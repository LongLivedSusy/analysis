#!/bin/sh
echo "running TMVA..."

g++ -w -g -Wall -Wextra -lTMVA -lTMVAGui `root-config --cflags --libs` tmva.cxx -o tmva

./tmva /nfs/dust/cms/user/kutznerv/shorttrack/analysis/disappearing-track-tag/training-phase0/tracks-long/signal.root output.root /nfs/dust/cms/user/kutznerv/shorttrack/analysis/disappearing-track-tag/training-phase0/tracks-long -1
