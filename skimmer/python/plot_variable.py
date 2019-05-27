#! /usr/bin/env python
from stackedplot import *
from ROOT import *

# Data blind
blind=True 

# Remake histos
remakeHistos=True
#remakeHistos=False
   
def saveHistos(histos,cutname,variable):
    if not os.path.exists("./histos/%s"%cutname):
        os.system("mkdir -p histos/%s"%cutname)
    
    f_hout = TFile("./histos/%s/histo_%s.root"%(cutname,variable),"RECREATE")
    for key, value in histos.items():
        hout = value.Clone()
        hout.SetName(key+"_"+variable)
        hout.SetTitle(key+"_"+variable)
        hout.SetDirectory(0)
        hout.Write()
    f_hout.Close()

def makeHistos(folder, samples, cuts, variables):
    for cutname, cut in cuts.items() : 
        for variable in variables:
	   if remakeHistos:
    	       histos = get_histograms_from_folder(folder, samples, variables[variable][0], cut, variables[variable][1], variables[variable][2], variables[variable][3])
    	       saveHistos(histos,cutname,variable)

def makePlots(histodir, outputdir, samples, cuts, variables, logx=False, logy=True, blind=True, suffix=""):
    histos = {}
    for cutname in cuts:
	for variable in variables:
	    f = TFile(histodir+"/"+cutname+"/histo_"+variable+".root")
	    for sample in samples:
		histo = f.Get(sample+"_"+variable)
		histos[sample]=histo

	    stack_histograms(histos, outputdir, samples, cutname, variable, variable, "Events", logx=logx, logy=logy, blind=blind, suffix=suffix)

if __name__=="__main__":
    
    # Folder
    #folder = "output_skim_merged"
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/background-estimation/non-prompt/output_skim_5_loose_merged"
    
    # Samples
    samples = {
        "DYJetsToLL": {"select": "Summer16.DYJetsToLL", "type": "bg", "color": 62},
        "QCD": {"select": "Summer16.QCD", "type": "bg", "color": 97},
        "WJetsToLNu": {"select": "Summer16.WJetsToLNu", "type": "bg", "color": 85},
        "ZJetsToNuNu": {"select": "Summer16.ZJetsToNuNu", "type": "bg", "color": 67},
        "Diboson": {"select": "Summer16.WW_TuneCUETP8M1|Summer16.WZ_TuneCUETP8M1|Summer16.ZZ_TuneCUETP8M1", "type": "bg", "color": 51},
        "TT": {"select": "Summer16.TTJets_TuneCUETP8M1", "type": "bg", "color": 8}, 
        "rare": {"select": "Summer16.ST|Summer16.GJets", "type": "bg", "color": 15},
        "signal": {"select": "Summer16.g1800_chi1400", "type": "sg", "color": kBlue},
              }
    if not blind: 
        if "dilepton_invmass" in variable:
	    samples["data"] = {"select": "Run2016*SingleMuon", "type": "data", "color": kBlack, "lumi": 13801}
	    #samples["data"] = {"select": "Run2016*SingleElectron", "type": "data", "color": kBlack, "lumi": 6212}
	    
	    #samples["data"] = {"select": "Run2016*MET", "type": "data", "color": kBlack, "lumi": 17330}
	    samples["data"] = {"select": "Run2016B-17Jul2018_ver2-v1.METAOD", "type": "data", "color": kBlack, "lumi": 17330}
    
    # Cuts 
    cuts =  {
	    "FullMhtNJet" : "passesUniversalSelection==1 && HT>100 && MHT>250 && n_jets>0 && n_DT>0 && tracks_dxyVtx < 0.02",
	    #"Mhtgt250_Njet1" : "passesUniversalSelection==1 && HT>100 && MHT>250 && n_jets==1 && n_DT>0",
	    #"Mhtgt250_Njet2to5" : "passesUniversalSelection==1 && HT>100 && MHT>250 && n_jets>=2 && n_jets<=5 && n_DT>0",
	    #"Mhtgt250_Njet6toInf" : "passesUniversalSelection==1 && HT>100 && MHT>250 && n_jets>=6 && n_DT>0",
	    }
    
    # Variables
    variables =	{
	    #"TrackMassFromDedxPixel":["TMath::Sqrt((tracks_deDxHarmonic2pixel-2.557)*TMath::Power(tracks_P,2)/2.579)",50, 0, 2000, cuts],
	    #"TrackMassFromDedxStrips":["TMath::Sqrt((tracks_deDxHarmonic2strips-2.557)*TMath::Power(tracks_P,2)/2.579)",50, 0, 2000, cuts],
	    "Log_TrackMassFromDedxPixel":["TMath::Log10(TMath::Sqrt((tracks_deDxHarmonic2pixel-2.557)*TMath::Power(tracks_P,2)/2.579))",15, 1.5, 4.5, cuts],
	    "Log_TrackMassFromDedxStrips":["TMath::Log10(TMath::Sqrt((tracks_deDxHarmonic2strips-2.557)*TMath::Power(tracks_P,2)/2.579))",15, 1.5, 4.5, cuts],
		}

    # Make histogram and save
    if remakeHistos:
	makeHistos(folder, samples, cuts, variables)
   
    # Draw plots
    makePlots("./histos/", "./plots/", samples, cuts.keys(), variables.keys(), logx=False, logy=True, blind=blind, suffix="")
