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


def get_ddbg_histograms(variable, basecuts, label, folder, globstrings, output_root_file):

    histos = collections.OrderedDict()

    input_files = []
    for globstring in globstrings:
       input_files += glob.glob(folder + "/" + globstring + "*.root")
    
    def get_histo(additional_cuts, scaling = ""):
        print "Getting", variable, label, additional_cuts, scaling
        return plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=additional_cuts, scaling=scaling, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2])

    dEdxLower = 0
    dEdxLow = 2.1
    dEdxMid = 4.0

    # get nonprompt CR and nonprompt prediction
    histos[label + "_fakecr_short"] = get_histo(basecuts + " && tracks_CR_short==1")
    histos[label + "_fakecr_long"] = get_histo(basecuts + " && tracks_CR_long==1")
    histos[label + "_fakeprediction_short"] = get_histo(basecuts + " && tracks_CR_short==1", scaling="fakerate_short")
    histos[label + "_fakeprediction_long"] = get_histo(basecuts + " && tracks_CR_long==1", scaling="fakerate_long")

    # get MC Truth histograms for closure
    histos[label + "_sr_short"] = get_histo(basecuts + " && tracks_SR_short==1")
    histos[label + "_sr_long"] = get_histo(basecuts + " && tracks_SR_long==1")
    histos[label + "_srHighDeDx_short"] = get_histo(basecuts + " && tracks_SR_short==1 && tracks_deDxHarmonic2pixel>%s" % dEdxLow)
    histos[label + "_srHighDeDx_long"] = get_histo(basecuts + " && tracks_SR_long==1 && tracks_deDxHarmonic2pixel>%s" % dEdxLow)
    histos[label + "_srgenfakes_short"] = get_histo(basecuts + " && tracks_SR_short==1 && tracks_fake==1")
    histos[label + "_srgenfakes_long"] = get_histo(basecuts + " && tracks_SR_long==1 && tracks_fake==1")
    histos[label + "_srgenprompt_short"] = get_histo(basecuts + " && tracks_SR_short==1 && tracks_fake==0")
    histos[label + "_srgenprompt_long"] = get_histo(basecuts + " && tracks_SR_long==1 && tracks_fake==0")

    # get prompt background ABCD histograms:
    histos[label + "_lowDeDxPromptElectron"] = get_histo(" && n_SR_short=0 && n_SR_long=0 && n_goodelectrons==1 && n_goodmuons==0 && leptons_dedx>%s && leptons_dedx<%s" % (dEdxLower, dEdxLow))
    histos[label + "_highDeDxPromptElectron"] = get_histo(" && n_SR_short=0 && n_SR_long=0 && n_goodelectrons==1 && n_goodmuons==0 && leptons_dedx>%s" % dEdxLow)
    histos[label + "_lowDeDxDTnoLep"] = get_histo(basecuts + " && ((n_SR_short+n_SR_long)==1) && n_goodleptons==0 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxLower, dEdxLow))
    histos[label + "_highDeDxDTnoLep"] = get_histo(basecuts + " && ((n_SR_short+n_SR_long)==1) && n_goodleptons==0 && tracks_deDxHarmonic2pixel>%s" % dEdxLow)
    
    # ABCD method to get prompt contribution in SR:
    histos[label + "_promptprediction"] = histos[label + "_highDeDxPromptElectron"].Clone()
    histos[label + "_promptprediction"].Multiply(histos[label + "_lowDeDxDTnoLep"])
    histos[label + "_promptprediction"].Divide(histos[label + "_lowDeDxPromptElectron"])
    
    # combine short and long tracks:
    for h_name in histos:
        if "_short" in h_name:
            histos[h_name.replace("_short", "")] = histos[h_name].Clone()
            histos[h_name.replace("_short", "")].Add(histos[h_name.replace("_short", "_long")])
     
    fout = TFile(output_root_file, "update")
    for h_name in histos:            
        histos[h_name].SetName(h_name)
        histos[h_name].SetTitle(h_name)
        histos[h_name].Write()
    fout.Close()


if __name__ == "__main__":

    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/tools/skim_69_merged"
    #folder = "../skims/tools/skim_01"

    print "OK"
    
    event_selections = {
                "Baseline":               "(n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0",
                "BaselineNoLeptons":      "n_goodleptons==0",
                "BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110 && leadinglepton_mt>90",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leptons_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leptons_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leptons_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leptons_mt<70",
                      }

    variables = ["HT", "MHT", "tracks_invmass", "leptons_mt"]
    regions = ["Baseline", "SElValidationZLL", "SMuValidationZLL", "SElValidationMT", "SMuValidationMT"]
    
    variables = ["leptons_mt"]
    regions = ["SElValidationMT"]

    # get histograms and save them to a file:
    os.system("rm ddbg.root")
    for variable in variables:
        for region in regions:
            get_ddbg_histograms(variable, event_selections[region], region + "_Summer16", folder, ["Summer16"], "ddbg.root")
            if not "Validation" in region:
                get_ddbg_histograms(variable, event_selections[region], region + "_Summer16QCDZJets", folder, ["Summer16.QCD", "Summer16.ZJets"], "ddbg.root")
            if not "SMu" in region:
                get_ddbg_histograms(variable, event_selections[region], region + "_Run2016SingleElectron", folder, ["Run2016*SingleElectron"], "ddbg.root")
            if not "SEl" in region:
                get_ddbg_histograms(variable, event_selections[region], region + "_Run2016SingleMuon", folder, ["Run2016*SingleMuon"], "ddbg.root")


