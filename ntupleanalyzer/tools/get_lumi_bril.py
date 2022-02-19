#!/bin/env python3
import glob
import os
import subprocess

# https://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html
# install brilws on lxplus:
# mv ~/.local ~/.local.bak
# export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda3/bin:$PATH
# pip3 install --user brilws
# 
# then copy your merged json files to lxplus and run this script
#
# comments @ Viktor

json_folder = "smallstay2"
get_lumis =   1
get_summary = 1

if get_lumis:

    for json in glob.glob("%s/*.json" % json_folder):
        
        with open(json, "r") as fin:
            contents = fin.read()
            if contents == "{}":
                print("Ignoring empty json: %s" % json)
                continue
                    
        os.system("export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda3/bin:$PATH; brilcalc lumi -u /fb -i %s --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json > %s 2>&1 &" % (json, json.replace(".json", ".briloutput")))   

    os.system("htop")
    input("continue...?")

if get_summary:

    lumis = {}

    for briloutput in glob.glob("%s/*.briloutput" % json_folder):
    
        os.system("grep totrecorded %s -A 2 | grep '|' | tail -n1 > lumi" % briloutput)
        
        with open("lumi", "r") as fin:
            label = briloutput.split("/")[-1].replace(".briloutput", "")
            try:
                output = fin.read()
                lumi = float(output.split("|")[-2])
                print(label, "\t\t", lumi)
                lumis[label] = lumi
            except:
                lumis[label] = 0
            
    for datastream in ["MET", "SingleElectron", "SingleMuon", "JetHT", "EGamma"]:
        total = 0.0
        for label in lumis:
            if datastream in label:
                total += lumis[label]
        print(datastream, "\t\t", total)
