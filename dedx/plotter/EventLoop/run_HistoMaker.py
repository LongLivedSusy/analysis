#!/usr/bin/env python
import os, sys
import subprocess
from glob import glob
from ROOT import *
from GridEngineTools import runParallel

Recompile=True
#Recompile=False

OUTDIR = "./histos"

def Make_samplelist(samplename,selected_sample):
    
    # Folder
    path = "../../skimmer/python/output_skim_Summer16MC_merged"
    file_names = glob(path+"/*.root")
    
    samples = []
    for file_name in file_names:
	if "merged" not in path:
            identifier = "_".join(file_name.split("_")[:-3])
        else:
            #identifier = file_name.replace(".root", "") 
            identifier = file_name 
    
        selectors = selected_sample.split("*")
        count = 0 
        for selector in selectors:
    
            if "|" in selector:
                for or_selector in selector.split("|"):
                    if or_selector in identifier:
                        count += 1
                        break
            elif selector in identifier:
                count += 1
        if count == len(selectors):
            samples.append(identifier)
    
    samples = list(set(samples))
    print "selected_sample:", selected_sample
    print "Found samples matching ''%s'':" % selected_sample, samples

    with open("list_"+samplename+".txt","w") as flist:
	flist.write('\n'.join(sorted(samples)))


if __name__ == '__main__' :

    if Recompile : 
	print ("============Recompiling HistoMaker...==============")
	subprocess.call("./compile_HistoMaker.sh", stdin=None, stdout=None, stderr=None, shell=True)
    
    if not os.path.exists(OUTDIR):
	#subprocess.Popen("mkdir -p %s"%OUTDIR,stdin=None, stdout=None, stderr=None, shell=True)
	os.system("mkdir -p %s"%OUTDIR)

    # Samples
    samples = {
	#"Run2016":	{"select": "Run2016*MET", "type": "data", "color": kBlack, "lumi": 7188.570159},
        "DYJetsToLL":	{"select": "Summer16.DYJetsToLL|RunIIFall17MiniAODv2.DYJetsToLL", "type": "bg", "color": 62},
        "TT":		{"select": "Summer16.TTJets_TuneCUETP8M1|RunIIFall17MiniAODv2.TTJets_HT|RunIIFall17MiniAODv2.TTJets_TuneCP5", "type": "bg", "color": 8}, 
        "ZJetsToNuNu":	{"select": "Summer16.ZJetsToNuNu", "type": "bg", "color": 67},
        "QCD":		{"select": "Summer16.QCD|RunIIFall17MiniAODv2.QCD", "type": "bg", "color": 97},
        "WJetsToLNu":	{"select": "Summer16.WJetsToLNu|RunIIFall17MiniAODv2.WJetsToLNu", "type": "bg", "color": 85},
        "Diboson":	{"select": "Summer16.WW_TuneCUETP8M1|Summer16.WZ_TuneCUETP8M1|Summer16.ZZ_TuneCUETP8M1", "type": "bg", "color": 51},
        "rare":		{"select": "Summer16.ST|Summer16.GJets|RunIIFall17MiniAODv2.ST", "type": "bg", "color": 15},
        "g1800_chi1400_ctau10": {"select": "Summer16.g1800_chi1400_27_200970_step4_10AODSIM", "type": "sg", "color": kBlue},
        "g1800_chi1400_ctau30": {"select": "Summer16.g1800_chi1400_27_200970_step4_30AODSIM", "type": "sg", "color": kGreen},
        "g1800_chi1400_ctau50": {"select": "Summer16.g1800_chi1400_27_200970_step4_50AODSIM", "type": "sg", "color": kRed},
        "g1800_chi1400_ctau100": {"select": "Summer16.g1800_chi1400_27_200970_step4_100AODSIM", "type": "sg", "color": kMagenta},
        #"Autumn18.g1800_chi1400_ctau10": {"select": "Autumn18.g1800_chi1400_27_200970_step4_10AODSIM", "type": "sg", "color": kBlue},
        #"Autumn18.g1800_chi1400_ctau30": {"select": "Autumn18.g1800_chi1400_27_200970_step4_30AODSIM", "type": "sg", "color": kGreen},
        #"Autumn18.g1800_chi1400_ctau50": {"select": "Autumn18.g1800_chi1400_27_200970_step4_50AODSIM", "type": "sg", "color": kRed},
        #"Autumn18.g1800_chi1400_ctau100": {"select": "Autumn18.g1800_chi1400_27_200970_step4_100AODSIM", "type": "sg", "color": kMagenta},
              }
  
    commands =[]
    for label in samples :
	print "Making Sample list"
	Make_samplelist(label,samples[label]["select"])

	if samples[label]["type"] == "data" :
	    is_data = True
	else : 
	    is_data = False
	
	#subprocess.call(("./HistoMaker list_%s.txt %s %s.root %s"%(label,OUTDIR,label,is_data)),stdin=None, stdout=None, stderr=None, shell=True)
	command = "./HistoMaker list_%s.txt %s %s.root"%(label,OUTDIR,label)
	commands.append(command)
    
    raw_input("Submit condor : continue?")
    runParallel(commands, "grid", condorDir="condor", dontCheckOnJobs=True)
    #runParallel(commands, "multi", condorDir="condor", dontCheckOnJobs=True)
