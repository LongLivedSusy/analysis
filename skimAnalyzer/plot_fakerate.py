#!/bin/env python
from __future__ import division
from ROOT import *
import os
import collections
import shared_utils
import glob

if __name__ == "__main__":

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    variables = [
                 "HT",
                 "n_goodjets",
                 "n_allvertices",
                 "n_btags",
                 "MinDeltaPhiMhtJets",
                 "HT:n_allvertices",
                ]
   
    histos = collections.OrderedDict()
   
    fin = TFile("fakerate.root", "read")
    region = "FakeRateDet"
    fakeratetype = "fakerate"
    
    for variable in variables:
        for category in ["short", "long"]:
            for dataset in ["Summer16", "Run2016"]:

                label = "%s_%s_%s_%s_%s" % (variable.replace(":", "_"), region, dataset, fakeratetype, category)

                print label

                histos[label] = fin.Get(label)
                histos[label].SetDirectory(0)

                histos[label].SetLineWidth(2)
                shared_utils.histoStyler(histos[label])                

                if ":" in variable:
                    
                    myvariable = variable
                    myvariable = myvariable.replace("HT", "H_{T} (GeV)")
                    myvariable = myvariable.replace("n_allvertices", "n_{vertices}")
                    
                    size = 0.059
                    font = 132
                    histos[label].GetZaxis().SetLabelFont(font)
                    histos[label].GetZaxis().SetTitleFont(font)
                    histos[label].GetZaxis().SetTitleSize(size)
                    histos[label].GetZaxis().SetLabelSize(size)
                    histos[label].GetZaxis().SetRangeUser(3e-3, 2e-1)
                    histos[label].GetZaxis().SetTitleOffset(1.2)
                    histos[label].SetTitle(";%s;%s;Events" % (myvariable.split(":")[1], myvariable.split(":")[0]))

                    canvas = shared_utils.mkcanvas()
                    canvas.SetRightMargin(0.2)
                    histos[label].Draw("colz")
                    canvas.SetLogz(True)
                    shared_utils.stamp()
                    
                    text = TLatex()
                    text.SetTextFont(132)
                    text.SetTextSize(0.05)
                    text.SetNDC()
                    text.DrawLatex(0.175, 0.825, "%s, %s tracks" % (dataset, category))
                    
                    canvas.SaveAs("frplots/" + label + ".pdf")
    
    
        if ":" not in variable:
            
            legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
            canvas = shared_utils.mkcanvas()
            
            mc_histograms = []
            data_histograms = []
            
            for i, dataset in enumerate(["Run2016", "Summer16"]):
            
                for category in ["long", "short"]:
                
                    if category == "short":
                        color = kRed
                    else:
                        color = kBlue
                    
                    label = "%s_%s_%s_%s_%s" % (variable, region, dataset, fakeratetype, category)
                    histos[label].SetLineStyle(i+1)
                    histos[label].SetLineColor(color)
                    histos[label].SetTitle(category + " tracks, " + dataset.replace("Summer16", "MC").replace("Run2016", "Data"))
                    if "Run201" in dataset:
                        data_histograms.append(histos[label])
                    else:
                        mc_histograms.append(histos[label])

            hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, data_histograms[0], mc_histograms, lumi = 36.0, datamc = 'Data')

            hratio.SetMarkerColor(hratio.GetLineColor())            
            
            hratio.GetYaxis().SetRangeUser(1e-3,1e3)
            mc_histograms[0].GetYaxis().SetTitle('Fake rate')

            data_histograms[0].SetMarkerStyle(20)
            data_histograms[0].SetMarkerColor(data_histograms[0].GetLineColor())            
            data_histograms[1].SetMarkerStyle(20)
            data_histograms[1].SetMarkerColor(data_histograms[1].GetLineColor())
            data_histograms[1].Draw("same p")
            legend.AddEntry(data_histograms[1], data_histograms[1].GetTitle())
    
            pad2.cd()
            pad2.SetLogy()
            ratio2 = data_histograms[1].Clone()
            ratio2.Divide(mc_histograms[1])
            ratio2.Draw("same p")
    
            canvas.SaveAs("frplots/" + variable + ".pdf")
        
