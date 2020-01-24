#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *
import collections
import shared_utils

def plot_run_periods(variable, prediction_folder, header):
    
    histos = collections.OrderedDict()
    
    for period in ["Run2016B", "Run2016C", "Run2016D", "Run2016E", "Run2016F", "Run2016G", "Run2016H"]:
        iFile = prediction_folder + "/closure_%s_MET.root" % period
        print iFile
        fin = TFile(iFile, "read")
        
        histos[period] = fin.Get(variable)
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

        color = colors.pop(0)
        histos[label].SetLineColor(color)
        histos[label].SetFillColor(0)
        #histos[label].SetLineWidth(2)
        histos[label].SetMarkerSize(0)
        histos[label].Scale(1.0/histos[label].Integral())        
        histos[label].GetXaxis().SetRangeUser(0,7.5)
        histos[label].GetYaxis().SetRangeUser(1e-3,1e-1)
        
        legend.AddEntry(histos[label], label + " MET")
        
    legend.Draw()
    shared_utils.stamp()
    canvas.SaveAs("fake-bg-prediction-periods-%s.pdf" % variable)
    

plot_run_periods("hFkBaseline_DeDxAverageMethod", "prediction31", "non-prompt prediction")
plot_run_periods("hFkBaseline_DeDxAverageMethod_CR", "prediction31", "non-prompt control region")
