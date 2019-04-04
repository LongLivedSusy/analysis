#!/bin/env python
import os, glob
from optparse import OptionParser

parser = OptionParser()
(options, args) = parser.parse_args()
folders = []
if len(args) > 0:
    for folder in args:
        folders.append(folder)


for folder in folders:

    samples = []
    for item in glob.glob(folder + "/*root"):
        sample_name = "_".join( item.split("/")[-1].split(".root")[0].split("_")[:-2] )
        samples.append(sample_name)

    samples = list(set(samples))

    for item in sorted(samples):
        print '"' + item + '",'

