#!/bin/env python
import os, glob

# use this script to get a file of unique sample names for a large folder full of ntuples:

#folder = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub"
folder = "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v2"

samples = []
for item in glob.glob(folder + "/*root"):
    sample_name = "_".join( item.split("/")[-1].split(".root")[0].split("_")[:-2] )
    samples.append(sample_name)

samples = list(set(samples))

for item in sorted(samples):
    print '"' + item + '",'
