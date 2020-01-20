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
    
    print "Found samples matching :" 
    for process, sample_found in samples_found.items():
	print process, sample_found
	if not sample_found : 
	    print 'Samples for [%s] process empty!!'%process
	    sys.exit()
    
    for variable in variables:
	histos = {}
	
	print "=================Variable:%s=================="%variable
	for sample_process, sample_found in samples_found.iteritems() :
	    h_combined = 0
	    for eachsample in sample_found : 
		f = TFile(eachsample,"r")
		histo = f.Get(variable)
		try : 
		    histo.SetDirectory(0)
		except : 
		    print "no histogram for variable %s in %s"%(variable,eachsample)
		    sys.exit()
	    	if h_combined == 0 : h_combined = histo
	    	else : h_combined.Add(histo)
	    	f.Close()
	    histos[sample_process]=h_combined

	stack_histograms(histos, outputdir, samples, variable, variable, "Events", logx=logx, logy=logy, suffix=suffix, outformat=outformat, save_shape=save_shape)
    
    
if __name__=="__main__":
    
    # Samples
    samples = {
	"Run2016":	{"select": "Run2016*MET", "type": "data", "color": kBlack, "lumi": 35348.5695},
        "DYJetsToLL":	{"select": "Summer16.DYJetsToLL|RunIIFall17MiniAODv2.DYJetsToLL", "type": "bg", "color": 62},
        "WJetsToLNu":	{"select": "Summer16.WJetsToLNu", "type": "bg", "color": 62},
        "TT":		{"select": "Summer16.TT|RunIIFall17MiniAODv2.TTJets_HT|RunIIFall17MiniAODv2.TTJets_TuneCP5", "type": "bg", "color": 8}, 
        "QCD":		{"select": "Summer16.QCD|RunIIFall17MiniAODv2.QCD", "type": "bg", "color": 97},
        "ZJetsToNuNu":	{"select": "Summer16.ZJetsToNuNu", "type": "bg", "color": 67},
        "WJetsToLNu":	{"select": "Summer16.WJetsToLNu|RunIIFall17MiniAODv2.WJetsToLNu", "type": "bg", "color": 85},
        "Diboson":	{"select": "Summer16.WW_TuneCUETP8M1|Summer16.WZ_TuneCUETP8M1|Summer16.ZZ_TuneCUETP8M1", "type": "bg", "color": 51},
        #"rare":		{"select": "Summer16.ST|Summer16.GJets|RunIIFall17MiniAODv2.ST", "type": "bg", "color": 15},
        #"g1800_chi1400_ctau10": {"select": "Summer16.g1800_chi1400_27_200970_step4_10AODSIM", "type": "sg", "color": kBlue},
        #"g1800_chi1400_ctau30": {"select": "Summer16.g1800_chi1400_27_200970_step4_30AODSIM", "type": "sg", "color": kGreen},
        #"g1800_chi1400_ctau50": {"select": "Summer16.g1800_chi1400_27_200970_step4_50AODSIM", "type": "sg", "color": kRed},
        #"g1800_chi1400_ctau100": {"select": "Summer16.g1800_chi1400_27_200970_step4_100AODSIM", "type": "sg", "color": kMagenta},
	#"SMS-T2bt-mLSP150": {"select": "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "type": "sg", "color": kBlue, "xsec":304.0},
	#"SMS-T2bt-mLSP400": {"select": "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "type": "sg", "color": kMagenta, "xsec":2.15},
	#"SMS-T2bt-mLSP1000": {"select": "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "type": "sg", "color": kGreen, "xsec":0.00683},
	#"SMS-T2bt-mLSP2000": {"select": "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "type": "sg", "color": kRed, "xsec":0.0000148},
              }
    
    # Variables to draw
    variables =	[
	    "muonPt",
	    "muonEta",
	    "muonPhi",
	    "electronPt",
	    "electronEta",
	    "electronPhi",
	    
	    "muonPt_CR1muon",
	    "MET_CR1muon",
	    "MHT_CR1muon",
	    "HT_CR1muon",
	    "n_jets_CR1muon",
	    
	    "electronPt_CR1electron",
	    "MET_CR1electron",
	    "MHT_CR1electron",
	    "HT_CR1electron",
	    "n_jets_CR1electron",
	    
	    #"MET_orig",
	    #"MET",
	    #"MHT",
	    #"n_jets",
	    #"n_leptons",
	    #"n_DT",
	    #"TrackDedx_pixel", 
	    #"TrackDedx_strips", 
	    #"TrackP_pixel",
	    #"TrackP_pixel_GenChi",
	    #"TrackP_pixel_GenMatch",
	    #"TrackPt_pixel",
	    #"TrackPt_pixel_GenChi",
	    #"TrackPt_pixel_GenMatch", 
	    #"TrackDedx_pixel", 
	    #"TrackDedx_pixel_GenChi", 
	    #"TrackMass_pixel",
	    #"TrackMass_pixel_GenChiMomentum",
	    #"TrackMass_pixel_GenMatch",
	    #"TrackP_strips",
	    #"TrackP_strips_GenChi",
	    #"TrackP_strips_GenMatch",
	    #"TrackPt_strips",
	    #"TrackPt_strips_GenChi",
	    #"TrackPt_strips_GenMatch",
	    #"TrackDedx_strips", 
	    #"TrackDedx_strips_GenChi", 
	    #"TrackMass_strips", 
	    #"TrackMass_strips_GenChiMomentum",
	    #"TrackMass_strips_GenMatch",
	    #"Track_deltaR_with_GenChi_pixel",
	    #"Track_deltaR_with_GenChi_strips" 
	    
	    #"MET_CR_noDT",
	    #"MHT_CR_noDT",
	    #"n_jets_CR_noDT",
	    #"n_leptons_CR_noDT",
	    #"n_DT_CR_noDT",
	    #"TrackP_CR_noDT",
	    #"TrackPt_CR_noDT",
	    #"TrackDedx_pixel_CR_noDT",
	    #"TrackDedx_strips_CR_noDT",
	    
	    #"MET_CR2",
	    #"MHT_CR2",
	    #"n_jets_CR2",
	    #"n_leptons_CR2",
	    #"n_DT_CR2",
	    #"TrackDedx_pixel_CR2", 
	    #"TrackDedx_strips_CR2", 
	    ]

    # Draw plots
    makePlots(histodir, plotdir, samples, variables, logx=False, logy=True, suffix="", outformat="png", save_shape=False)
