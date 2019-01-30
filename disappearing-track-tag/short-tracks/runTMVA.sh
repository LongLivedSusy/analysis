#!/bin/sh
echo "running TMVA..."

g++ -w -g -Wall -Wextra -lTMVA -lTMVAGui `root-config --cflags --libs` tmva.cxx -o tmva

./tmva /nfs/dust/cms/user/kutznerv/DisappTrksNtupleSidecarI7d/tracks-short/signal.root output.root /nfs/dust/cms/user/kutznerv/DisappTrksNtupleSidecarI7d/tracks-short -1
