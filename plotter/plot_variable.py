#! /usr/bin/env python
from plotting import *
from stackedplot import *
from ROOT import *

# Data blind
blind=True 

# Remake histos
#remakeHistos=True
remakeHistos=False

# Folder histogram and plots
histodir = "histos"
plotdir = "plots"

# FIXME : use TEventList for later use
#def makeEventList(folder, samples, cuts, variables):
#    for cutname, cut in cuts.items() : 
#        for variable in variables:
#	    print cutname, cut, variable

def makeHistos(folder, samples, cuts, variables):
    for cutname, cut in cuts.items() : 
	
	if not os.path.exists("./%s/%s"%(histodir,cutname)):
    	    os.system("mkdir -p %s/%s"%(histodir,cutname))
        
	for variable in variables:
    	    histos = get_histograms_from_folder(folder, samples, variables[variable][0], cut, variables[variable][1], variables[variable][2], variables[variable][3])
	    
	    f_hout = TFile("./%s/%s/histo_%s.root"%(histodir,cutname,variable),"RECREATE")
    	    for key, value in histos.items():
    	        hout = value.Clone()
    	        hout.SetName(key+"_"+variable)
    	        hout.SetTitle(key+"_"+variable)
    	        hout.SetDirectory(0)
    	        hout.Write()
    	    f_hout.Close()
    
def makePlots(histodir, outputdir, samples, cuts, variables, logx=False, logy=True, blind=True, suffix="", outformat="", fit_bkg=False, fit_sig=False, fit_data=False):
    histos = {}
    for cutname in cuts:
	for variable in variables:
	    if os.path.exists(histodir+"/"+cutname+"/histo_"+variable+".root"):
		f = TFile(histodir+"/"+cutname+"/histo_"+variable+".root")
	    	for sample in samples:
	    	    histo = f.Get(sample+"_"+variable)
	    	    histos[sample]=histo
		stack_histograms(histos, outputdir, samples, cutname, variable, variable, "Events", logx=logx, logy=logy, blind=blind, suffix=suffix, outformat=outformat, fit_bkg=fit_bkg, fit_sig=fit_sig, fit_data=fit_data)
	    
	    else :
		print histodir+"/"+cutname+"/histo_"+variable+".root does not exist"


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
        "All_signal_ctau": {"select": "Summer16.g1800_chi1400|Autumn18.g1800_chi1400", "type": "sg", "color": kBlue},
        #"Summer16.g1800_chi1400_ctau10": {"select": "Summer16.g1800_chi1400_27_200970_step4_10AODSIM", "type": "sg", "color": kBlue},
        #"Summer16.g1800_chi1400_ctau30": {"select": "Summer16.g1800_chi1400_27_200970_step4_30AODSIM", "type": "sg", "color": kGreen},
        #"Summer16.g1800_chi1400_ctau50": {"select": "Summer16.g1800_chi1400_27_200970_step4_50AODSIM", "type": "sg", "color": kRed},
        #"Summer16.g1800_chi1400_ctau100": {"select": "Summer16.g1800_chi1400_27_200970_step4_100AODSIM", "type": "sg", "color": kMagenta},
        #"Autumn18.g1800_chi1400_ctau10": {"select": "Autumn18.g1800_chi1400_27_200970_step4_10AODSIM", "type": "sg", "color": kBlue},
        #"Autumn18.g1800_chi1400_ctau30": {"select": "Autumn18.g1800_chi1400_27_200970_step4_30AODSIM", "type": "sg", "color": kGreen},
        #"Autumn18.g1800_chi1400_ctau50": {"select": "Autumn18.g1800_chi1400_27_200970_step4_50AODSIM", "type": "sg", "color": kRed},
        #"Autumn18.g1800_chi1400_ctau100": {"select": "Autumn18.g1800_chi1400_27_200970_step4_100AODSIM", "type": "sg", "color": kMagenta},
              }
    
    if not blind: 
        if "dilepton_invmass" in variable:
	    samples["data"] = {"select": "Run2016*MET", "type": "data", "color": kBlack, "lumi": 17330}
	    #samples["data"] = {"select": "Run2016B-17Jul2018_ver2-v1.METAOD", "type": "data", "color": kBlack, "lumi": 17330}
    
    # Cuts 
    cuts =  {
	    #"FullMhtNJet" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && n_DT>0",
	    #"FullMhtNJet_short" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && n_DT==1 && tracks_is_disappearing_track==1 && tracks_is_pixel_track==1 && tracks_mass_Pixel<10000",
	    #"FullMhtNJet_long" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && n_DT==1 && tracks_is_disappearing_track==1 && tracks_is_pixel_track==0 && tracks_mass_WeightedByValidHits<10000",
	    #"CR_FullMhtNJet_short" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && tracks_tagged_bdt==0 && tracks_is_pixel_track==1",
	    "CR_FullMhtNJet_long" : "passesUniversalSelection==1 && HT>100 && MHT>180 && n_jets>0 && tracks_tagged_bdt==0 && tracks_is_pixel_track==0",
	    }
    
    # Variables
    variables =	{
	    #"Track_Pt":["tracks_pt",100, 3000, 10000, cuts],
	    #"Track_P":["tracks_P",100, 0, 3000, cuts],
	    #"Track_LogMassFromDedxPixel":["TMath::Log10(tracks_massfromdeDxPixel)",20, 1.5, 5.5, cuts],
	    "Track_LogMassFromDedxWeightedDeDx":["TMath::Log10(tracks_massfromdeDx_weightedDeDx)",20, 1.5, 5.5, cuts],
	    "Track_LogMassFromDedxWeightedStripsMass":["TMath::Log10(tracks_massfromdeDx_weightedPixelStripsMass)",20, 1.5, 5.5, cuts],
		}

    #FIXME : Use TEventList for each cut(no need to loop in each variable)
    #makeEventList(folder, samples, cuts, variables)

    # Make histogram and save
    if remakeHistos:
	makeHistos(folder, samples, cuts, variables)
   
    # Draw plots
    makePlots(histodir, plotdir, samples, cuts.keys(), variables.keys(), logx=False, logy=True, blind=blind, suffix="", outformat="png", fit_bkg=False, fit_sig=False, fit_data=False)
