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
	print "[PROCESS : %s]\n"%process, sample_found
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
    
    stack_histograms(histos, outputdir, samples, variable, variable, "Events", logx=logx, logy=logy, suffix=suffix, outformat=outformat, save_shape=save_shape)
    
if __name__=="__main__":
    
    # Samples
    samples = {
        "WJetsToLNu":	{"select": "Summer16.WJetsToLNu_Tune|Summer16.WJetsToLNu_HT", "type": "bg", "color": 85},
        "DYJetsToLL":	{"select": "Summer16.DYJetsToLL_M-50_Tune|Summer16.DYJetsToLL_M-50_HT", "type": "bg", "color": 62},
        "TT":		{"select": "Summer16.TTJets", "type": "bg", "color": 8}, 
        "QCD":		{"select": "Summer16.QCD_HT", "type": "bg", "color": 97},
        "ZJetsToNuNu":	{"select": "Summer16.ZJetsToNuNu_HT", "type": "bg", "color": 67},
        "Diboson":	{"select": "Summer16.WW_Tune|Summer16.WZ_Tune|Summer16.ZZ_Tune", "type": "bg", "color": 51},
        "Triboson":	{"select": "Summer16.WWW|Summer16.WZZ|Summer16.ZZZ", "type": "bg", "color": 46},
        "rare":		{"select": "Summer16.ST", "type": "bg", "color": 15},
	
	## Fall17 Bkgs
	#"WJetsToLNu":	{"select": "RunIIFall17MiniAODv2.WJetsToLNu_HT", "type": "bg", "color": 85},
        #"DYJetsToLL":	{"select": "RunIIFall17MiniAODv2.DYJetsToLL_M-50_Tune|RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT", "type": "bg", "color": 62},
        #"TT":		{"select": "RunIIFall17MiniAODv2.TTJets_Tune|RunIIFall17MiniAODv2.TTJets_HT", "type": "bg", "color": 8}, 
        #"QCD":		{"select": "RunIIFall17MiniAODv2.QCD_HT", "type": "bg", "color": 97},
        #"ZJetsToNuNu":	{"select": "RunIIFall17MiniAODv2.ZJetsToNuNu_HT", "type": "bg", "color": 67},
        #"Diboson":	{"select": "RunIIFall17MiniAODv2.WW|RunIIFall17MiniAODv2.WZ|RunIIFall17MiniAODv2.ZZ", "type": "bg", "color": 51},
	
	## signals
	#"SMS-T2bt-mLSP1": {"select": "SMS-T2bt-LLChipm_ctau-200_mLSP-1_", "type": "sg", "color": kYellow},
	#"SMS-T2bt-mLSP150": {"select": "SMS-T2bt-LLChipm_ctau-200_mLSP-150_", "type": "sg", "color": kBlue},
	#"SMS-T2bt-mLSP400": {"select": "SMS-T2bt-LLChipm_ctau-200_mLSP-400_", "type": "sg", "color": kMagenta},
	#"SMS-T2bt-mLSP1000": {"select": "SMS-T2bt-LLChipm_ctau-200_mLSP-1000_", "type": "sg", "color": kGreen},
	#"SMS-T2bt-mLSP2000": {"select": "SMS-T2bt-LLChipm_ctau-200_mLSP-2000_", "type": "sg", "color": kRed},
              }
    
    # Variables to draw
    variables_mu =	[
	    "hMuP",
	    "hMuPt",
	    "hMuEta",
	    "hMuPhi",
	    "hMuGamma",
	    "hMuBetaGamma",

	    "hMuP_genmatch",
	    "hMuPt_genmatch",
	    "hMuEta_genmatch",
	    "hMuPhi_genmatch",
	    "hMuGamma_genmatch",
	    "hMuBetaGamma_genmatch",
	    
	    "hTrkPt_tightmumatch",
	    "hTrkPt_tightgenmumatch",

	    "hTrkPt_tightgenmumatch_barrel",
	    "hTrkPt_tightgenmumatch_endcap",
	    
	    "hTrkPixelDedx_tightmumatch",
	    "hTrkPixelDedx_tightmumatch_barrel",
	    "hTrkPixelDedx_tightmumatch_endcap",
	    "hTrkPixelDedx_tightgenmumatch",
	    "hTrkPixelDedx_tightgenmumatch_barrel",
	    "hTrkPixelDedx_tightgenmumatch_endcap",
	    "hTrkPixelDedxCalib_tightmumatch",
	    "hTrkPixelDedxCalib_tightmumatch_barrel",
	    "hTrkPixelDedxCalib_tightmumatch_endcap",
	    
	    "hTrkStripsDedx_tightmumatch",
	    "hTrkStripsDedx_tightmumatch_barrel",
	    "hTrkStripsDedx_tightmumatch_endcap",
	    "hTrkStripsDedx_tightgenmumatch",
	    "hTrkStripsDedx_tightgenmumatch_barrel",
	    "hTrkStripsDedx_tightgenmumatch_endcap",
	    "hTrkStripsDedxCalib_tightmumatch",
	    "hTrkStripsDedxCalib_tightmumatch_barrel",
	    "hTrkStripsDedxCalib_tightmumatch_endcap",
	    ]
    
    variables_ele =	[
	    "hElePt",
	    "hElePt_fromZ_leading",
	    "hElePt_fromZ_trailing",
	    "hElePt_genmatch",
	    "hEleEta",
	    "hElePhi",
	    "hGamma_ele",
	    
	    "hTrkPt_tightelematch",
	    "hTrkPt_tightelematch_fromZ",
	    "hTrkPt_tightgenelematch",
	    "hTrkPt_tightgenelematch_barrel",
	    "hTrkPt_tightgenelematch_endcap",
	    
	    "hTrkPixelDedx_tightelematch",
	    "hTrkPixelDedx_tightelematch_fromZ",
	    "hTrkPixelDedx_tightelematch_barrel",
	    "hTrkPixelDedx_tightelematch_fromZ_barrel",
	    "hTrkPixelDedx_tightelematch_endcap",
	    "hTrkPixelDedx_tightelematch_fromZ_endcap",
	    "hTrkPixelDedx_tightgenelematch",
	    "hTrkPixelDedx_tightgenelematch_barrel",
	    "hTrkPixelDedx_tightgenelematch_endcap",
	    "hTrkPixelDedxCalib_tightelematch",
	    "hTrkPixelDedxCalib_tightelematch_barrel",
	    "hTrkPixelDedxCalib_tightelematch_endcap",
	    
	    "hTrkStripsDedx_tightelematch",
	    "hTrkStripsDedx_tightelematch_fromZ",
	    "hTrkStripsDedx_tightelematch_barrel",
	    "hTrkStripsDedx_tightelematch_fromZ_barrel",
	    "hTrkStripsDedx_tightelematch_endcap",
	    "hTrkStripsDedx_tightelematch_fromZ_endcap",
	    "hTrkStripsDedx_tightgenelematch",
	    "hTrkStripsDedx_tightgenelematch_barrel",
	    "hTrkStripsDedx_tightgenelematch_endcap",
	    "hTrkStripsDedxCalib_tightelematch",
	    "hTrkStripsDedxCalib_tightelematch_barrel",
	    "hTrkStripsDedxCalib_tightelematch_endcap",
	    ]
    
    variables_met = [
	    "hMET",
	    "hMHT",
	    "hHT",
	    "hHT_unweighted",
	    ]
    
    # Folder for histograms and plots
    histodir = "output_mediumchunks/"
    plotdir = "plots_2016"
    #plotdir = "plots_2017"
    #plotdir = "plots_2018"
    ##############################

    # Draw plots
    for variable in variables_mu:
	samples["Run2016_SingleMuon"]={"select": "Run2016B-SingleMuon|Run2016C-SingleMuon|Run2016D-SingleMuon|Run2016E-SingleMuon|Run2016F-SingleMuon|Run2016G-SingleMuon|Run2016H-SingleMuon", "type": "data", "color": kBlack, "lumi": 35200.41639}
	#samples["Run2017_SingleMuon"]={"select": "Run2017B-SingleMuon|Run2017C-SingleMuon|Run2017D-SingleMuon|Run2017E-SingleMuon|Run2017F-SingleMuon", "type": "data", "color": kBlack, "lumi": 41470}
	#samples["Run2018_SingleMuon"]={"select": "Run2018A-SingleMuon|Run2018B-SingleMuon|Run2018C-SingleMuon|Run2018D-SingleMuon", "type": "data", "color": kBlack, "lumi": 55550}
	makePlots(histodir, plotdir, samples, variable, logx=False, logy=True, suffix="", outformat="png", save_shape=False)
	del samples["Run2016_SingleMuon"]
	#del samples["Run2017_SingleMuon"]
	#del samples["Run2018_SingleMuon"]
    
#    for variable in variables_ele:
#	samples["SingleElectron"]={"select": "Run2016B-SingleElectron|Run2016C-SingleElectron|Run2016D-SingleElectron|Run2016E-SingleElectron|Run2016F-SingleElectron|Run2016G-SingleElectron|Run2016H-SingleElectron", "type": "data", "color": kBlack, "lumi": 34331.72766}
#	#samples["SingleElectron"]={"select": "Run2017B-SingleElectron|Run2017C-SingleElectron|Run2017D-SingleElectron|Run2017E-SingleElectron|Run2017F-SingleElectron", "type": "data", "color": kBlack, "lumi": 40805.1454}
#	makePlots(histodir, plotdir, samples, variable, logx=False, logy=True, suffix="", outformat="png", save_shape=False)
#	del samples["SingleElectron"]
    
#    for variable in variables_met:
#	samples["MET"]={"select": "Run2016B_MET|Run2016C_MET|Run2016D_MET|Run2016E_MET|Run2016F_MET|Run2016G_MET|Run2016H_MET", "type": "data", "color": kBlack, "lumi": 35767.77446}
#	makePlots(histodir, plotdir, samples, variable, logx=False, logy=True, suffix="", outformat="pdf", save_shape=False)
#	del samples["MET"]
