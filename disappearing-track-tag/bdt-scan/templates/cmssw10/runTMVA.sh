#!/bin/sh
echo "running TMVA..."

g++ -w -g -Wall -Wextra -lTMVA -lTMVAGui `root-config --cflags --libs` tmva.cxx -o tmva

./tmva $TREEPATH/signal.root output.root $TREEPATH -1
