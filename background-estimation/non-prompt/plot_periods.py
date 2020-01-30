#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *
import collections
import shared_utils
from optparse import OptionParser

def plot_run_periods(variable, prediction_folder, header):
    
    histos = collections.OrderedDict()
    
    for period in ["Summer16", "Run2016B_MET", "Run2016C_MET", "Run2016D_MET", "Run2016E_MET", "Run2016F_MET", "Run2016G_MET", "Run2016H_MET"]:
        iFile = prediction_folder + "/prediction_%s.root" % period
        print iFile
        fin = TFile(iFile, "read")
        
        histos[period] = fin.Get(variable)
        print histos[period].GetEntries()
        histos[period].SetDirectory(0)
        fin.Close()
    
    canvas = shared_utils.mkcanvas()
    canvas.SetLogy(True)
    
    legend = TLegend(0.6, 0.6, 0.88, 0.88)
    legend.SetHeader(header)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)    
    
    colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]
    
    for i_label, label in enumerate(histos):
        
        if i_label == 0:
            histos[label].Draw("h")
        else:
            histos[label].Draw("h same")
    
        shared_utils.histoStyler(histos[label])

        xlabel = variable.split("_")[0]
        if "DeDx" in xlabel:
            xlabel += " (Mev/cm)"

        color = colors.pop(0)
        histos[label].SetLineColor(color)
        histos[label].SetFillColor(0)
        histos[label].SetMarkerSize(0)
        if histos[label].Integral()>0:
            histos[label].Scale(1.0/histos[label].Integral())
        histos[label].SetTitle(";%s;Events" % xlabel)
        histos[label].GetXaxis().SetRangeUser(0,7.5)
        histos[label].GetYaxis().SetRangeUser(5e-4,1e-1)
        
        # fit histograms:

        if "DeDx_" in variable:
            if "Summer16" in label:
                fit_x = TF1("fit_x", "gaus", 2.5, 3.5)
            else:
                fit_x = TF1("fit_x", "gaus", 1.6, 2.8)
            fit_x.SetLineColor(kRed)
            fit_x.SetLineWidth(2)
            histos[label].Fit("fit_x", "r")

            legend.AddEntry(histos[label], label + ", (#mu=%1.2f)" % fit_x.GetParameter(1))

        else:

            legend.AddEntry(histos[label], label)


    legend.Draw()
    shared_utils.stamp()
    canvas.SaveAs("fakebg_%s.pdf" % variable)
              


folder = "prediction38"
for variable in ["DeDx", "DeDxCorrected"]:
    for region in ["control", "prediction"]:
        for category in ["short", "long"]:
            for event_selection in ["baseline", "baseline_simplecuts"]:
                header = "non-prompt " + region + " reg., " + category + " tr."
                plot_run_periods("%s_%s_%s_%s" % (variable, region, category, event_selection), folder, header)


