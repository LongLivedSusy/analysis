#! /usr/bin/env python

import os,sys
from stackedplot import *
from ROOT import *
from glob import glob

# Folder for histograms and plots
suffix=""
#histodir = "output_mediumchunks/"
histodir = sys.argv[1]
plotdir = "plots"+suffix
##############################


def makePlots(histodir, outputdir, samples, variables, logx=False, logy=True, suffix="", outformat="", save_shape=False):
   
    file_names = glob(histodir+"/*.root")
    samples_found = {}
    for process, sample in samples.iteritems():
	sample_files = []
        selectors = sample['select'].split("*")
	print "selectors:",selectors
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
	print "[PROCESS : %s]\n"%process, sample_found
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
	"MET"	    :	{"select": "Run2016B_MET|Run2016C_MET|Run2016D_MET|Run2016E_MET|Run2016F_MET|Run2016G_MET|Run2016H_MET", "type": "data", "color": kBlack, "lumi": 35729.573401},
	#"SingleMuon":	{"select": "SingleMuon", "type": "data", "color": kBlack, "lumi": 32189.463371},
	#"SingleElectron":	{"select": "SingleElectron", "type": "data", "color": kBlack, "lumi": 30668.889085999997},
        "WJetsToLNu":	{"select": "WJetsToLNu_HT", "type": "bg", "color": 85},
        "DYJetsToLL":	{"select": "DYJetsToLL_M-50_HT", "type": "bg", "color": 62},
        "TT":		{"select": "TTJets", "type": "bg", "color": 8}, 
        "QCD":		{"select": "QCD_HT", "type": "bg", "color": 97},
        "ZJetsToNuNu":	{"select": "ZJetsToNuNu_HT", "type": "bg", "color": 67},
        "Diboson":	{"select": "WW|WZ|ZZ", "type": "bg", "color": 51},
        #"rare":		{"select": "Summer16.ST|Summer16.GJets|RunIIFall17MiniAODv2.ST", "type": "bg", "color": 15},
	#"SMS-T2bt-mLSP150": {"select": "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "type": "sg", "color": kBlue},
	#"SMS-T2bt-mLSP400": {"select": "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "type": "sg", "color": kMagenta},
	#"SMS-T2bt-mLSP1000": {"select": "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "type": "sg", "color": kGreen},
	#"SMS-T2bt-mLSP2000": {"select": "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", "type": "sg", "color": kRed},
              }
    
    # Variables to draw
    variables =	[
	    "hMET",
	    "hMHT",
	    "hHT",
	    "hHT_unweighted",
	    
	    "hMuPt",
	    "hMuEta",
	    "hMuPhi",
	    
	    "hTrkPt",
	    "hTrkPt_mumatch",
	    "hTrkDedx_mumatch",
	    
	    #"electronPt",
	    #"electronEta",
	    #"electronPhi",
	    #"electronPt_noMu",
	    
	    ]

    # Draw plots
    makePlots(histodir, plotdir, samples, variables, logx=False, logy=True, suffix="", outformat="png", save_shape=False)
