#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import collections
import glob
import os

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

binnings = {}
binnings["LepMT"] = [16, 0, 160]
binnings["leptons_mt"] = binnings["LepMT"]
binnings["leadinglepton_mt"] = binnings["LepMT"]
binnings["InvMass"] = [50, 0, 200]
binnings["tracks_invmass"] = binnings["InvMass"]
binnings["Ht"] = [35 , 0, 700]
binnings["HT"] = binnings["Ht"]
binnings["Met"] = [35 , 0, 700]
binnings["MET"] = binnings["Met"]
binnings["Mht"] = [35 , 0, 700]
binnings["MHT"] = binnings["Mht"]
binnings["DeDxAverage"] = [60, 0, 6]
binnings["tracks_massfromdeDxPixel"] = binnings["DeDxAverage"]
binnings["DeDxAverageCorrected"] = [60, 0, 6]
binnings["BinNumber"] = [ 88, 1, 89]
binnings["region"] = binnings["BinNumber"]
binnings["n_tags"] = [ 3, 0, 3]
binnings["n_goodjets"] = [ 10, 0, 10]
binnings["n_goodelectrons"] = [ 5, 0, 5]
binnings["n_goodmuons"] = [ 5, 0, 5]
binnings["MinDeltaPhiMhtJets"] = [ 16, 0, 3.2]
binnings["BTags"] = [ 4, 0, 4]
binnings["Track1MassFromDedx"] = [ 25, 0, 1000]
binnings["Log10DedxMass"] = [10, 0, 5]


def get_fkbg_histograms(variable, basecuts, label, folder, globstrings, output_root_file):


    histos = collections.OrderedDict()

    input_files = []
    for globstring in globstrings:
       input_files += glob.glob(folder + "/" + globstring + "*.root")
    
    def get_histo(additional_cuts, scaling = ""):
        print "getting", additional_cuts, scaling
        return plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=basecuts + additional_cuts, scaling=scaling, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2])

    # get nonprompt CR and nonprompt prediction
    histos[label + "_fakecr_short"] = get_histo(" && tracks_CR_short==1")
    histos[label + "_fakecr_long"] = get_histo(" && tracks_CR_long==1")
    histos[label + "_fakeprediction_short"] = get_histo(" && tracks_CR_short==1", scaling="fakerate_short")
    histos[label + "_fakeprediction_long"] = get_histo(" && tracks_CR_long==1", scaling="fakerate_long")

    # get MC Truth histograms for nonprompt closure
    histos[label + "_sr_short"] = get_histo(" && tracks_SR_short==1")
    histos[label + "_sr_long"] = get_histo(" && tracks_SR_long==1")
    histos[label + "_srgenfakes_short"] = get_histo(" && tracks_SR_short==1 && tracks_fake==1")
    histos[label + "_srgenfakes_long"] = get_histo(" && tracks_SR_long==1 && tracks_fake==1")
    histos[label + "_srgenprompt_short"] = get_histo(" && tracks_SR_short==1 && tracks_fake==0")
    histos[label + "_srgenprompt_long"] = get_histo(" && tracks_SR_long==1 && tracks_fake==0")
     
    fout = TFile(output_root_file, "update")
    for h_name in histos:
        histos[h_name].SetName(h_name)
        histos[h_name].SetTitle(h_name)
        histos[h_name].Write()
    fout.Close()


if __name__ == "__main__":

    folder = "../skims/current"
    
    event_selections = {
                "Baseline":               "(n_goodleptons==0 || tracks_invmass>110)",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0",
                "BaselineNoLeptons":      "n_goodleptons==0",
                "BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110",
                "BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || tracks_invmass>110)",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leptons_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leptons_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leptons_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leptons_mt<70",
                      }

    # get histograms and save them to a file:
    os.system("rm ddbg.root")
    for variable in ["MHT", "tracks_invmass", "leptons_mt"]:
        #for region in ["Baseline", "SElValidationZLL", "SMuValidationZLL", "SElValidationMT", "SMuValidationMT"]:
        for region in ["SElValidationMT"]:
            get_fkbg_histograms(variable, event_selections[region], region + "_Summer16QCDZJets", folder, ["Summer16.QCD", "Summer16.ZJets"], "ddbg.root")
            #get_fkbg_histograms(variable, event_selections[region], region + "_Run2016MET", folder, ["Run2016*MET"], "ddbg.root")
            get_fkbg_histograms(variable, event_selections[region], region + "_Run2016SingleElectron", folder, ["Run2016*SingleElectron"], "ddbg.root")
            #get_fkbg_histograms(variable, event_selections[region], region + "_Run2016SingleMuon", folder, ["Run2016*Muon"], "ddbg.root")

    
