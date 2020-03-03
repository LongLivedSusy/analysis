#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *
import collections
import shared_utils
from optparse import OptionParser

def plot_run_periods(variable, prediction_folder, header, pdffile, lumi = 1.0, category = "combined", cr = "Baseline", dataset = "MET"):
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    histos = collections.OrderedDict()

    # load histograms:
    
    fin = TFile(prediction_folder + "/prediction_Summer16_all.root", "read")
    histos["mc_CR"] = fin.Get("%s_nonpromptcontrol_%s_%s" % (variable, category, cr) )
    histos["mc_nonpromptprediction"] = fin.Get("%s_nonpromptprediction_%s_%s" % (variable, category, cr) )    
    histos["mc_signalprompt"] = fin.Get("%s_signalprompt_%s_%s" % (variable, category, cr) )    
    histos["mc_signalfake"] = fin.Get("%s_signalfake_%s_%s" % (variable, category, cr) )    

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
    

folder = "../skims/current"
with open(folder + "/luminosity.py") as fin:
    lumis = eval(fin.read())

pred_folder = "prediction7"

for variable in ["LepMT", "Ht", "Mht", "InvMass"]:
    for dataset in ["SingleElectron", "SingleMuon"]:
        lumi = lumis["Run2016_%s" % dataset] * 1e3

        if "Electron" in dataset:
            crs = ["SElValidationMT", "SElValidationZLL"]
        if "SingleMuon" in dataset:
            crs = ["SMuValidationMT", "SMuValidationZLL"]

        for cr in crs:
            plot_run_periods(variable, pred_folder, "%s region" % cr, "validation_%s_%s.pdf" % (variable, cr), cr = cr, dataset = dataset, lumi = lumi)



