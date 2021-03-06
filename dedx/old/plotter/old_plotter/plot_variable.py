#! /usr/bin/env python

import os,sys
from plotting import *
from stackedplot import *
from ROOT import *

####### GLOBAL SETTINGS ########
# Data unblind
#unblind=True 
unblind=False 

# Remake histos
#remakeHistos=True
remakeHistos=False

# Remake plots
remakePlots=True
#remakePlots=False

# Folder for histograms and plots
histodir = "histos"
plotdir = "plots"
##############################

def makeHistos(folder, samples, cuts, variables):
    for cutname, cut in cuts.items() : 
        if not os.path.exists("./%s/%s"%(histodir,cutname)):
    	    os.system("mkdir -p %s/%s"%(histodir,cutname))
        
	for variable in variables:
    	    histos = get_histograms_from_folder(folder, samples, variables[variable][0], cut, variables[variable][1], variables[variable][2], variables[variable][3])
	
	    for sample, histo in histos.items():
	        f_hout = TFile("./%s/%s/histo_%s_%s.root"%(histodir,cutname,variable,sample),"RECREATE")
    	        hout = histo.Clone()
    	        hout.SetName(sample+"_"+variable)
    	        hout.SetTitle(sample+"_"+variable)
    	        hout.SetDirectory(0)
    	        hout.Write()
	        f_hout.Close()
    
def makePlots(histodir, outputdir, samples, cuts, variables, logx=False, logy=True, unblind=False, suffix="", outformat="", fit_bkg=False, fit_sig=False, fit_data=False):
   for cutname in cuts:
       for variable in variables:
	    histos = {}
	    for sample in samples:
		if os.path.exists("./%s/%s/histo_%s_%s.root"%(histodir,cutname,variable,sample)):
		    f = TFile("./%s/%s/histo_%s_%s.root"%(histodir,cutname,variable,sample),"r")
		    histo = f.Get(sample+"_"+variable)
		    histo.SetDirectory(0)
		    histos[sample]=histo
		    f.Close
		else :
		    print "./%s/%s/histo_%s_%s.root does not exist"%(histodir,cutname,variable,sample)
		    sys.exit()
	    
	    stack_histograms(histos, outputdir, samples, cutname, variable, variable, "Events", logx=logx, logy=logy, unblind=unblind, suffix=suffix, outformat=outformat, fit_bkg=fit_bkg, fit_sig=fit_sig, fit_data=fit_data)
	
    
if __name__=="__main__":
    
    # Folder
    folder = "../skimmer/python/output_skim_Summer16MC_merged"
    
    # Samples
    samples = {
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
    
    if unblind: 
	samples["data"] = {"select": "Run2016*MET", "type": "data", "color": kBlack, "lumi": 7188.570159}
	pass
    
    # Cuts 
    cuts =  {
	    "SR_FullMhtNJet_short" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && n_leptons==0 && tracks_pt>30 && tracks_mva_bdt>0.1 && tracks_is_pixel_track==1",
	    #"SR_FullMhtNJet_long" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && n_leptons==0 && tracks_pt>30 && tracks_mva_bdt>0.25 && tracks_is_pixel_track==0",
	    #"CR_FullMhtNJet_short" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && n_leptons==0 && tracks_pt>30 && tracks_mva_bdt<0.1 && tracks_is_pixel_track==1",
	    #"CR_FullMhtNJet_long" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && n_leptons==0 && tracks_pt>30 && tracks_mva_bdt<0.25 && tracks_is_pixel_track==0",
	    #"CR_FullMhtNJet_long_loose" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && n_leptons==0 && tracks_pt>30 && tracks_mva_bdt_loose<0 && tracks_is_pixel_track==0",
	    }
    
    # Variables
    variables =	{
	    #"MET":["MET",100, 0, 1000, cuts],
	    #"Track_Pt":["tracks_pt",100, 0, 1000, cuts],
	    #"Track_P":["tracks_P",100, 0, 3000, cuts],
	    "Track_LogMassFromDedxPixel":["TMath::Log10(tracks_massfromdeDxPixel)",50, 0, 5.5, cuts],
	    #"Track_LogMassFromDedxWeightedDeDx":["TMath::Log10(tracks_massfromdeDx_weightedDeDx)",50, 0, 5.5, cuts],
	    #"Track_LogMassFromDedxWeightedPixelStripsMass":["TMath::Log10(tracks_massfromdeDx_weightedPixelStripsMass)",50, 0, 5.5, cuts],
		}

    # Make histogram and save
    if remakeHistos:
	print 'Are you going to remake Histos? Enter to continue'
	raw_input()
	makeHistos(folder, samples, cuts, variables)
   
    # Draw plots
    if remakePlots:
	makePlots(histodir, plotdir, samples, cuts.keys(), variables.keys(), logx=False, logy=True, unblind=unblind, suffix="", outformat="png", fit_bkg=False, fit_sig=False, fit_data=False)
