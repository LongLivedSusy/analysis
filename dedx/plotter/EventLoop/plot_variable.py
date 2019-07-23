#! /usr/bin/env python

import os,sys
from stackedplot import *
from ROOT import *

# Folder for histograms and plots
histodir = "histos"
plotdir = "plots"
##############################

def makePlots(histodir, outputdir, samples, variables, logx=False, logy=True, unblind=False, suffix="", outformat="", fit_bkg=False, fit_sig=False, fit_data=False):
    histos = {} 
    for variable in variables:
	for sample in samples:
	    if os.path.exists("./%s/%s.root"%(histodir,sample)):
		f = TFile("./%s/%s.root"%(histodir,sample),"r")
    	    	histo = f.Get(variable)
    	    	histo.SetDirectory(0)
    	    	histos[sample]=histo
    	    	f.Close
	    else :
		print "./%s/%s.root does not exist"%(histodir,sample)
    	    	sys.exit()
	    
	stack_histograms(histos, outputdir, samples, variable, variable, "Events", logx=logx, logy=logy, unblind=unblind, suffix=suffix, outformat=outformat, fit_bkg=fit_bkg, fit_sig=fit_sig, fit_data=fit_data)
	
    
if __name__=="__main__":
    
    # Samples
    samples = {
	#"Run2016":	{"select": "Run2016*MET", "type": "data", "color": kBlack, "lumi": 7188.570159},
        "WJetsToLNu":	{"select": "Summer16.WJetsToLNu", "type": "bg", "color": 62},
        "DYJetsToLL":	{"select": "Summer16.DYJetsToLL|RunIIFall17MiniAODv2.DYJetsToLL", "type": "bg", "color": 62},
        "TT":		{"select": "Summer16.TTJets_TuneCUETP8M1|RunIIFall17MiniAODv2.TTJets_HT|RunIIFall17MiniAODv2.TTJets_TuneCP5", "type": "bg", "color": 8}, 
        "ZJetsToNuNu":	{"select": "Summer16.ZJetsToNuNu", "type": "bg", "color": 67},
        #"QCD":		{"select": "Summer16.QCD|RunIIFall17MiniAODv2.QCD", "type": "bg", "color": 97},
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
    
    # Variables
    variables =	["MET","MHT","HT","TrackMass_short","TrackMass_long_strips","TrackMass_long_weightedPixelStripsMass"]
    #variables =	["MET","MHT","HT"]

    # Draw plots
    makePlots(histodir, plotdir, samples, variables, logx=False, logy=True, unblind=False, suffix="", outformat="png", fit_bkg=False, fit_sig=False, fit_data=False)
