#!/bin/sh

g++ -w -g -Wall -Wextra `root-config --cflags --glibs` HistoMaker.cxx -o HistoMaker
