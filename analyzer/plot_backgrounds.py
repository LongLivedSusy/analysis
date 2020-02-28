#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import collections
import glob
import os

def plot_validation(variable, root_file, header, pdffile, lumi = 1.0, label):
    
    histos = collections.OrderedDict()

    # load histograms:
    
    fin = TFile(root_file, "read")

    # get nonprompt CR and nonprompt prediction
    for zone in ["_fakecr_short", "_fakecr_long", "_fakeprediction_short", "_fakeprediction_long", "_sr_short", "_sr_long", "_srgenfakes_short", "_srgenfakes_long", "_srgenprompt_short", "_srgenprompt_long"]: 
        histos[label + "_fakecr_short"] = fin.Get(label + zone)

    for label in histos:
        histos[label].SetDirectory(0)
        histos[label].Scale(lumi)
    fin.Close()
    
    fin = TFile(prediction_folder + "/prediction_Run2016_%s.root" % dataset, "read")
    histos["data_CR"] = fin.Get("%s_nonpromptcontrol_%s_%s" % (variable, category, cr) )
    histos["data_signal"] = fin.Get("%s_signal_%s_%s" % (variable, category, cr) )
    histos["data_prediction"] = fin.Get("%s_nonpromptprediction_%s_%s" % (variable, category, cr) )    

    for label in histos:
        histos[label].SetDirectory(0)
        histos[label].SetLineWidth(2)
        shared_utils.histoStyler(histos[label])

        if label == "mc_signalprompt":
            histos[label].SetTitle("Prompt bg. (MC Truth)")       
        elif label == "data_prediction":
            histos[label].SetTitle("Fake bg. (from Data)")
        elif label == "data_signal":
            histos[label].SetTitle("Data")
        else:
            histos[label].SetTitle(label)
    fin.Close()

    # plot:

    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    legend.SetHeader(header)

    canvas = shared_utils.mkcanvas()
    canvas.SetFillStyle(4000)    
    colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]
    
    histos["data_prediction"].SetFillColor(216)
    histos["mc_signalprompt"].SetFillColor(207)
   
    stacked_histograms = [histos["data_prediction"], histos["mc_signalprompt"]]

    lumi = float("%.2f" % (lumi/1e3))

    hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histos["data_signal"], stacked_histograms, lumi = lumi, datamc = 'Data')

    for i_label, label in enumerate(histos):
    #    color = colors.pop(0)
    #    histos[label].SetLineColor(color)
        histos[label].GetYaxis().SetRangeUser(1e-4, 1e4)
           
    hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
    hratio.GetYaxis().SetTitle('Events/bin')
    hratio.GetXaxis().SetTitle(variable)

    #histos["mc_signalprompt"].SetLineColor(kBlack)
    #histos["mc_signalprompt"].Draw("same")
    #histos["mc_signalfake"].SetLineColor(kOrange)
    #histos["mc_signalfake"].Draw("same")
    histos["mc_CR"].SetLineColor(kTeal)
    histos["mc_CR"].Draw("same")
    legend.AddEntry(histos["mc_CR"], "nonprompt fake CR")

    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)
    canvas.SaveAs(pdffile)


if __name__ == "__main__":

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

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

    # do validation plots:
    

