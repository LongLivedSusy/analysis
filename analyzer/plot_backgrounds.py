#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import collections
import glob
import os
import shared_utils

def plot_validation(variable, root_file, mclabel, datalabel, category, pdffile, lumi, header):
    
    # get histograms:
    histos = collections.OrderedDict()
    fin = TFile(root_file, "read")
    for zone in ["_fakecr_short",
                 "_fakecr_long",
                 "_fakeprediction_short",
                 "_fakeprediction_long",
                 "_sr_short", "_sr_long",
                 "_srgenfakes_short",
                 "_srgenfakes_long",
                 "_srgenprompt_short",
                 "_srgenprompt_long"]:
        histos[mclabel + zone] = fin.Get(label + zone)
        histos[datalabel + zone] = fin.Get(label + zone)

    for label in histos:
        histos[label].SetDirectory(0)
        histos[label].SetLineWidth(2)
        if "Run201" not in label:
            histos[label].Scale(lumi)
        shared_utils.histoStyler(histos[label])
    fin.Close()
    
    for label in histos:
        histos[label].SetDirectory(0)

    # plot:
    canvas = shared_utils.mkcanvas()
    canvas.SetFillStyle(4000)    
    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    legend.SetHeader(header)
    colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]
    
    histos[datalabel + "_fakeprediction_" + category].SetFillColor(216)
  
    stacked_histograms = [
                           histos[datalabel + "_fakeprediction_" + category],
                         ]

    lumi = float("%.2f" % (lumi/1e3))

    hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histos[datalabel + "_sr_" + category]], stacked_histograms, lumi = lumi, datamc = 'Data')

    for i_label, label in enumerate(histos):
        histos[label].GetYaxis().SetRangeUser(1e-4, 1e4)
           
    hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
    hratio.GetYaxis().SetTitle('Events/bin')
    hratio.GetXaxis().SetTitle(variable)

    histos[datalabel + "_fakecr_" + category].SetLineColor(kTeal)
    histos[datalabel + "_fakecr_" + category].Draw("same")
    legend.AddEntry(histos[datalabel + "_fakecr_" + category], "Fake CR")

    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)
    canvas.SaveAs(pdffile)


if __name__ == "__main__":

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
   
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/current"
    with open(folder + "/luminosity.py") as fin:
        lumis = eval(fin.read())

    for variable in ["MHT", "tracks_invmass", "leptons_mt"]:
        for region in ["SElValidationMT"]:
            plot_validation(variable, "ddbg.root", "Summer16", "Run2016SingleElectron", "short", "validation_" + variable + "_" + region, lumis["Run2016_SingleElectron"] * 1e3, region)

    

