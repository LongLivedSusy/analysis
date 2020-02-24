#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *
import collections
import shared_utils
from optparse import OptionParser

def plot_run_periods(mc_root_input, variable, header, pdffile, ymin=1e-5, ymax=1e5, lumi = 37000, category = "combined", cr = "Baseline"):
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    histos = collections.OrderedDict()

    # load histograms:
    
    fin = TFile(mc_root_input, "read")
    histos["mc_CR"] = fin.Get("%s_nonpromptcontrol_%s_%s" % (variable, category, cr) )
    histos["mc_CR_promptcontamination"] = fin.Get("%s_nonpromptcontrolprompt_%s_%s" % (variable, category, cr) )
    histos["mc_nonpromptprediction"] = fin.Get("%s_nonpromptprediction_%s_%s" % (variable, category, cr) )    
    histos["mc_signal"] = fin.Get("%s_signal_%s_%s" % (variable, category, cr) )    
    histos["mc_signalprompt"] = fin.Get("%s_signalprompt_%s_%s" % (variable, category, cr) )    
    histos["mc_signalfake"] = fin.Get("%s_signalfake_%s_%s" % (variable, category, cr) )    

    for label in histos:
        histos[label].SetDirectory(0)
        histos[label].Scale(lumi)
    fin.Close()
    
    for label in histos:
        histos[label].SetDirectory(0)
        histos[label].SetLineWidth(2)
        shared_utils.histoStyler(histos[label])

        if label == "mc_nonpromptprediction":
            histos[label].SetTitle("Fake prediction")       
        elif label == "mc_signalprompt":
            histos[label].SetTitle("Prompt background SR (MC Truth)")       
        elif label == "mc_signalfake":
            histos[label].SetTitle("Fake background SR (MC Truth)")       
        else:
            histos[label].SetTitle(label)
    fin.Close()


    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    legend.SetHeader(header)

    canvas = shared_utils.mkcanvas()
    canvas.SetFillStyle(4000)    
    colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]
    
    histos["mc_signalprompt"].SetFillColor(216)
    histos["mc_signalfake"].SetFillColor(207)
   
    stacked_histograms = [histos["mc_signalprompt"], histos["mc_signalfake"]]
    
    histos["combined_truth"] = histos["mc_signalprompt"].Clone()
    histos["combined_truth"].Add(histos["mc_signalfake"])
    #legend.AddEntry(histos["combined_truth"], "MC Truth everything")
    histos["combined_truth"].SetTitle("MC Truth everything")
    
    lumi = float("%.2f" % (lumi/1e3))

    hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histos["combined_truth"], stacked_histograms, lumi = lumi, datamc = 'Data')
    for i_label, label in enumerate(histos):
        histos[label].GetYaxis().SetRangeUser(ymin, ymax)
       
    hratio.GetYaxis().SetTitle('Truth/Pred.')
    hratio.GetXaxis().SetTitle(variable)

    new_ratio = stacked_histograms[-1].Clone()
    new_ratio.Divide(histos["mc_nonpromptprediction"])
    hratio.Multiply(new_ratio)

    histos["mc_nonpromptprediction"].SetLineColor(kBlue)
    histos["mc_nonpromptprediction"].Draw("same")
    legend.AddEntry(histos["mc_nonpromptprediction"], "Fake prediction")
        
    histos["mc_CR"].SetLineColor(kTeal)
    histos["mc_CR"].Draw("same")
    legend.AddEntry(histos["mc_CR"], "Fake CR")

    legend.Draw()

    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
            
    hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
    hratio.GetYaxis().SetLimits(-0.1,2.6)    
    
            
    hratio.SetMarkerColor(kBlack)
    canvas.SaveAs(pdffile)
    

for variable in ["Ht", "Mht"]:
    
    cr = "Baseline"
    
    if variable == "Ht":
        ymin = 1
        ymax = 1e8
    if variable == "Mht":
        ymin = 1e-4
        ymax = 1e7    
    
    plot_run_periods("prediction/prediction_Summer16_QCDZJets.root", variable, "%s region, QCD/ZJets-only" % cr, "fakeclosure_%s_%s_QCDZJets.pdf" % (variable, cr), ymin = ymin, ymax = ymax, cr = cr)
    plot_run_periods("prediction/prediction_Summer16_all.root", variable, "%s region" % cr, "fakeclosure_%s_%s.pdf" % (variable, cr), ymin = ymin, ymax = ymax, cr = cr)


