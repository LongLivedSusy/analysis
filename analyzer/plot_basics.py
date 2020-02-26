#!/bin/env python
from __future__ import division
import os
from ROOT import *
import plotting
import collections
import shared_utils
import glob

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def plot(variable, histos, lumi, pdffile):

    contains_data = False
    for label in histos:
        if not "Run201" in label:
            contains_data = True
            histos[label].Scale(lumi)
    
    for label in histos:
        histos[label].SetLineWidth(2)
        shared_utils.histoStyler(histos[label])

    histolist = [histos[histos.keys()[0]]]
    for label in histos:
        if not "Run201" in label and not "SMS" in label and not "g1800" in label:
            histolist.append(histos[label])

    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)

    canvas = shared_utils.mkcanvas()
    canvas.SetFillStyle(4000)    
      
    lumi = float("%.2f" % (lumi/1e3))

    if contains_data:
        hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histolist[0], histolist[1:], lumi = lumi, datamc = 'Data')
    else:
        hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histolist[0], histolist, lumi = lumi, datamc = 'Data')

    for i_label, label in enumerate(histos):
        histos[label].GetYaxis().SetRangeUser(1e-1, 1e10)

    for label in histos:
        if "SMS" in label or "g1800" in label:
            histos[label].Draw("same")
            legend.AddEntry(histos[label], label)

       
    hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
    hratio.GetYaxis().SetTitle('Data/MC')
    hratio.GetXaxis().SetTitle(variable)
    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)
    canvas.SaveAs(pdffile)
    

def do_plots(variables, cutstring, thisbatchname, folder, labels):

    with open(folder + "/luminosity.py") as fin:
        lumis = eval(fin.read())

    lumi = 1.0
    binnings = {}
    binnings["MHT"] = [20, 0, 1000]
    binnings["tracks_invmass"] = [50, 0, 200]

    for variable in variables:
        histos = collections.OrderedDict()
        for label in labels:
            input_files = glob.glob(folder + "/" + label + "*.root")
            histos[label] = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cutstring, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2])
            if "Run201" in label:
                lumi = lumis[label.replace("*", "_")] * 1e3

            title = labels[label][0]
            color = labels[label][1]

            histos[label].SetTitle(title)
            if not "SMS" in label and not "g1800" in label:
                histos[label].SetFillColor(color)
            else:
                histos[label].SetLineColor(color)

        plot(variable, histos, lumi, "%s_%s.pdf" % (thisbatchname, variable))
        plot(variable, histos, lumi, "%s_%s.root" % (thisbatchname, variable))


if __name__ == "__main__":

    folder = "../skims/current"
    
    labels = collections.OrderedDict()
    labels["Run2016*MET"] =         ["Run2016 MET", kBlack]
    labels["Summer16.WJetsToLNu"] = ["WJets", 85]
    labels["Summer16.DYJetsToLL"] = ["DY Jets", 67]
    labels["Summer16.QCD"] =        ["QCD", 97]
    labels["Summer16.TTJets"] =     ["TT Jets", 8]
    labels["Summer16.??_Tune"] =    ["Diboson", 62]
    labels["*g1800_chi1400*"] =     ["Signal", kBlue]

    event_selections = {
                "Baseline":               "n_goodleptons==0 || tracks_invmass>110",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0",
                "BaselineNoLeptons":      "n_goodleptons==0",
                "BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110",
                "BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110",
                "PromptDeterminationEl":  "n_goodelectrons==1 && n_goodmuons==0",
                "PromptDeterminationMu":  "n_goodelectrons==0 && n_goodmuons==1",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || tracks_invmass>110)",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leptons_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leptons_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leptons_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leptons_mt<70",
                      }

    do_plots(["tracks_invmass"], event_selections["SElValidationZLL"], "hello", folder, labels)

