#!/bin/env python
import glob, os, commands

with open("prediction3.condor/args", "r") as fin:
    args = fin.read()

args = args.split("\n")
outputfiles = [] 
missing = []
newargs = ""
newcmds = []

for line in args:
    outputfile = line.split("--output")[-1].split("--")[0].replace(";", "").replace(" ", "")
    outputfiles.append(outputfile)

    if not os.path.exists(outputfile):
        print outputfile
        newcmds.append(line + "\n")

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

print len(newcmds)

with open("prediction3.condor/args.new", "w") as fin:
    #for chunk in chunks(newcmds, 2):
    for chunk in newcmds:
        #fin.write("\n".join(chunk))
        fin.write(chunk)

#os.system("mkdir skim_03.condor/done")
#os.system("mv skim_03.condor/*log skim_03.condor/done/")
#os.system("mv skim_03.condor/*sh.e skim_03.condor/done/")
#os.system("mv skim_03.condor/*sh.o skim_03.condor/done/")
