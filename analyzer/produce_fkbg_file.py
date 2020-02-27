#!/bin/env python
from __future__ import division
import os
from ROOT import *
import collections

def main(root_file, output_root_file, variable, category, cr, canvas_label, lumi = 137000):

    if "Run201" in output_root_file:
        is_data = True
    else:
        is_data = False
       
    histos = collections.OrderedDict()
    tfile = TFile(root_file, "open")      
    histos["mc_CR"] = tfile.Get("%s_nonpromptcontrol_%s_%s" % (variable, category, cr) )
    histos["mc_prediction"] = tfile.Get("%s_nonpromptprediction_%s_%s" % (variable, category, cr) )
    
    for label in histos:                
        if not is_data:
            histos[label].Scale(lumi)

    fout = TFile(output_root_file, "update")
    if is_data:
        histos["mc_prediction"].SetName("%sMethod" % (canvas_label))
    else:
        histos["mc_prediction"].SetName("%sTruth" % (canvas_label))
    histos["mc_prediction"].Write()

    if is_data:
        histos["mc_CR"].SetName("%sMethod_CR" % (canvas_label))
    else:
        histos["mc_CR"].SetName("%sTruth_CR" % (canvas_label))
    histos["mc_CR"].Write()

    fout.Close()
    

if __name__ == "__main__":

    prediction_folder = "prediction7"
   
    variables = ['BTags', 'Met', 'Mht', 'BinNumber', 'InvMass', 'DeDxAverageCorrected', 'LepMT', 'Ht', 'DeDxAverage']
    data_periods = ["Summer16_all", "Run2016_all", "Run2016_SingleElectron", "Run2016_SingleMuon", "Run2016_MET"]
    
    event_selections_from_analyzer = {
                "Baseline":               "n_goodleptons==0 || tracks_invmass>110",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0",
                #"BaselineNoLeptons":      "n_goodleptons==0",
                #"BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110",
                #"BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || tracks_invmass>110)",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leptons_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leptons_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leptons_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leptons_mt<70",
                      }

    # add zones:
    event_selections = []
    for event_selection in event_selections_from_analyzer.keys():
        for zone in ["", "ZoneDeDx1p6to2p1", "ZoneDeDx0p0to2p1", "ZoneDeDx2p1to4p0", "ZoneDeDx4p0toInf"]:
            event_selections.append(event_selection + zone)

    for data_period in data_periods:

        os.system("rm %s/fakebg_%s.root" % (prediction_folder, data_period))
        root_file = "%s/prediction_%s.root" % (prediction_folder, data_period)

        for variable in variables:
            for event_selection in event_selections:
                print data_period, variable, event_selection
                canvas_label = "%s_%s" % (event_selection, variable)
                main(root_file, prediction_folder + "/fakebg_%s.root" % (data_period), variable, "combined", event_selection, canvas_label)

