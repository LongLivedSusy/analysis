#! /usr/bin/env python

import os,sys
from stackedplot import *
from ROOT import *
from glob import glob

# Folder for histograms and plots
histodir = "histos"
plotdir = "plots"
##############################


def makePlots(histodir, outputdir, samples, variables, logx=False, logy=True, suffix="", outformat="", save_shape=False):
   
    file_names = glob(histodir+"/h_*.root")
    samples_found = {}
    for process, sample in samples.iteritems():
	sample_files = []
        selectors = sample['select'].split("*")
        for file_name in file_names :
	    identifier = file_name
	    for selector in selectors :
	        if "|" in selector:
		    for or_selector in selector.split("|"):
			if or_selector in identifier:
			    sample_files.append(identifier)
	        	    break
	        elif selector in identifier:
		    sample_files.append(identifier)
	samples_found[process] = list(set(sample_files))
    
    print "Found samples matching :",samples_found 
    
    for variable in variables:
	histos = {}
	
	print "=================Variable:%s=================="%variable
	for sample_process, sample_found in samples_found.iteritems() :
	    h_combined = 0
	    for eachsample in sample_found : 
		f = TFile(eachsample,"r")
		histo = f.Get(variable)
	    	histo.SetDirectory(0)
	    	if h_combined == 0 : h_combined = histo
	    	else : h_combined.Add(histo)
	    	f.Close()
	    histos[sample_process]=h_combined

	stack_histograms(histos, outputdir, samples, variable, variable, "Events", logx=logx, logy=logy, suffix=suffix, outformat=outformat, save_shape=save_shape)
    
    
if __name__=="__main__":
    
    # Samples
    samples = {
	#"Run2016":	{"select": "Run2016*MET", "type": "data", "color": kBlack, "lumi": 35348.5695},
        "WJetsToLNu":	{"select": "Summer16.WJetsToLNu", "type": "bg", "color": 62},
        "DYJetsToLL":	{"select": "Summer16.DYJetsToLL|RunIIFall17MiniAODv2.DYJetsToLL", "type": "bg", "color": 62},
        "TT":		{"select": "Summer16.TT_|RunIIFall17MiniAODv2.TTJets_HT|RunIIFall17MiniAODv2.TTJets_TuneCP5", "type": "bg", "color": 8}, 
        "ZJetsToNuNu":	{"select": "Summer16.ZJetsToNuNu", "type": "bg", "color": 67},
        "QCD":		{"select": "Summer16.QCD|RunIIFall17MiniAODv2.QCD", "type": "bg", "color": 97},
        "WJetsToLNu":	{"select": "Summer16.WJetsToLNu|RunIIFall17MiniAODv2.WJetsToLNu", "type": "bg", "color": 85},
        "Diboson":	{"select": "Summer16.WW_TuneCUETP8M1|Summer16.WZ_TuneCUETP8M1|Summer16.ZZ_TuneCUETP8M1", "type": "bg", "color": 51},
        "rare":		{"select": "Summer16.ST|Summer16.GJets|RunIIFall17MiniAODv2.ST", "type": "bg", "color": 15},
        "g1800_chi1400_ctau10": {"select": "Summer16.g1800_chi1400_27_200970_step4_10AODSIM", "type": "sg", "color": kBlue},
        "g1800_chi1400_ctau30": {"select": "Summer16.g1800_chi1400_27_200970_step4_30AODSIM", "type": "sg", "color": kGreen},
        "g1800_chi1400_ctau50": {"select": "Summer16.g1800_chi1400_27_200970_step4_50AODSIM", "type": "sg", "color": kRed},
        "g1800_chi1400_ctau100": {"select": "Summer16.g1800_chi1400_27_200970_step4_100AODSIM", "type": "sg", "color": kMagenta},
              }
    
    # Variables to draw
    #variables =	["MET","MHT","HT","n_leptons_CR1","TrackPt_pixel","TrackPt_strips","TrackMass_pixel","TrackMass_strips","TrackMass_weightedPixelStripsMass","MET_CR1","MHT_CR1", "HT_CR1","TrackPt_pixel_CR1","TrackPt_strips_CR1", "TrackMass_pixel_CR1", "TrackMass_strips_CR1", "TrackMass_weightedPixelStripsMass_CR1"]
    variables =	[
	    #"TrackP_pixel",
	    #"TrackP_pixel_GenChi",
	    #"TrackP_pixel_GenMatch",
	    #"TrackPt_pixel",
	    #"TrackPt_pixel_GenChi",
	    #"TrackPt_pixel_GenMatch", 
	    "TrackDedx_pixel", 
	    "TrackDedx_pixel_GenChi", 
	    #"TrackMass_pixel",
	    #"TrackMass_pixel_GenChiMomentum",
	    #"TrackMass_pixel_GenMatch",
	    #"TrackP_strips",
	    #"TrackP_strips_GenChi",
	    #"TrackP_strips_GenMatch",
	    #"TrackPt_strips",
	    #"TrackPt_strips_GenChi",
	    #"TrackPt_strips_GenMatch",
	    "TrackDedx_strips", 
	    "TrackDedx_strips_GenChi", 
	    #"TrackMass_strips", 
	    #"TrackMass_strips_GenChiMomentum",
	    #"TrackMass_strips_GenMatch",
	    #"Track_deltaR_with_GenChi_pixel",
	    #"Track_deltaR_with_GenChi_strips" 
	    ]

    # Draw plots
    makePlots(histodir, plotdir, samples, variables, logx=False, logy=True, suffix="", outformat="png", save_shape=True)
