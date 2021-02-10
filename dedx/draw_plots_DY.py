#! /usr/bin/env python

import os,sys
from stackedplot import *
from ROOT import *
from glob import glob

def makePlots(histodir, outputdir, samples, variable, logx=False, logy=True, suffix="", outformat="", save_shape=False):
   
    file_names = glob(histodir+"/*.root")
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
	#print "[PROCESS : %s]\n"%process, sample_found
	if not sample_found : 
	    print 'Samples for [%s] process empty!!'%process
	    sys.exit()
    
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
    
    stack_histograms(histos, outputdir, samples, variable, variable, "Events", logx=logx, logy=logy, suffix=suffix, outformat=outformat)
    
if __name__=="__main__":
    
    # Folder for histograms and plots
    #histodir = "output_mediumchunks/"
    histodir = "output_mediumchunks_MIH/"
    #plotdir = "plots_2016_DY"
    plotdir = "plots_2016_DY_MIH"
    #plotdir = "plots_2017_DY_MIH"
    #plotdir = "plots_2018_DY"
    ##############################

    # Samples
    samples = {
        "WJetsToLNu":	{"select": "Summer16.WJetsToLNu", "type": "bg", "color": 85},
        "DYJetsToLL":	{"select": "Summer16.DYJetsToLL", "type": "bg", "color": 62},
        "TT":		{"select": "Summer16.TTJets", "type": "bg", "color": 8}, 
        "Diboson":	{"select": "Summer16.WW_Tune|Summer16.WZ_Tune|Summer16.ZZ_Tune", "type": "bg", "color": 51},
        "QCD":		{"select": "Summer16.QCD", "type": "bg", "color": 97},
        "ZJetsToNuNu":	{"select": "Summer16.ZJetsToNuNu", "type": "bg", "color": 67},
        "Triboson":	{"select": "Summer16.WWW|Summer16.WZZ|Summer16.ZZZ", "type": "bg", "color": 46},
        "SingleTop":	{"select": "Summer16.ST", "type": "bg", "color": 15},
              }
    
    # Variables to draw
    variables_mu =	[
	    "hMET",
	    "hMHT",
	    "hHT",
	    "hHT_unweighted",
	    "hMuP_fromZ",
	    "hMuPt_fromZ",
	    "hMuEta_fromZ",
	    "hMuPhi_fromZ",
	    "hMuGamma_fromZ",
	    "hMuBetaGamma_fromZ",
	    "hMuMu2InvMass",
	    "hMuMu2InvMass_ZmassWindow",
	    "hTrkMuInvMass",
	    "hTrkMuInvMass_ZmassWindow",
	    "hTrkP_fromZ",
	    "hTrkPt_fromZ",
	    "hTrkEta_fromZ",
	    "hTrkPhi_fromZ",
	    "hTrkPixelDedx_fromZ",
	    "hTrkPixelDedx_fromZ_barrel",
	    "hTrkPixelDedxScale_fromZ_barrel",
	    "hTrkPixelDedxScaleSmear_fromZ_barrel",
	    "hTrkPixelDedx_fromZ_endcap",
	    "hTrkPixelDedxScale_fromZ_endcap",
	    "hTrkPixelDedxScaleSmear_fromZ_endcap",
	    "hTrkStripsDedx_fromZ",
	    "hTrkStripsDedx_fromZ_barrel",
	    "hTrkStripsDedx_fromZ_endcap",
	    ]
    
    
    # Draw plots
    for variable in variables_mu:
	samples["Run2016_SingleMuon"]={"select": "Run2016B-SingleMuon|Run2016C-SingleMuon|Run2016D-SingleMuon|Run2016E-SingleMuon|Run2016F-SingleMuon|Run2016G-SingleMuon|Run2016H-SingleMuon", "type": "data", "color": kBlack, "lumi": 35900}
	#samples["Run2017_SingleMuon"]={"select": "Run2017B-SingleMuon|Run2017C-SingleMuon|Run2017D-SingleMuon|Run2017E-SingleMuon|Run2017F-SingleMuon", "type": "data", "color": kBlack, "lumi": 41470}
	#samples["Run2018_SingleMuon"]={"select": "Run2018A-SingleMuon|Run2018B-SingleMuon|Run2018C-SingleMuon|Run2018D-SingleMuon", "type": "data", "color": kBlack, "lumi": 55550}
	#makePlots(histodir, plotdir, samples, variable, logx=False, logy=False, suffix="", outformat="png")
	makePlots(histodir, plotdir, samples, variable, logx=False, logy=True, suffix="", outformat="png")
	del samples["Run2016_SingleMuon"]
	#del samples["Run2017_SingleMuon"]
	#del samples["Run2018_SingleMuon"]
    
