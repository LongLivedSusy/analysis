#!/bin/env python
from __future__ import division
from ROOT import *
import os
import collections
import shared_utils
import glob
from optparse import OptionParser

if __name__ == "__main__":

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    parser = OptionParser()
    (options, args) = parser.parse_args()
    folder = args[0]
    
    os.system("mkdir -p %s_plots" % folder)
    
    if len(args)>0:
        fin = TFile("%s/fakeratekappa.root" % folder, "read")
    else:
        print "Usage: ./plot_fakerate.py <folder>"
        quit()
       
    for identifier, datasets in [
                                  ("2016", ["Summer16", "Run2016"]),
                                  #("2017", ["Fall17", "Run2017"]),
                                  #("2018", ["Fall17", "Run2018"])
                                ]:
    
        for fakeratetype in ["fakerate", "kappa"]: 
            
            if fakeratetype == "fakerate":
                region = "QCDLowMHT"
                variables = [
                             #"tracks_pt",
                             "HT",
                             #"MHT",
                             #"n_goodjets",
                             #"n_allvertices",
                             #"n_btags",
                             #"HT_n_allvertices",
                             #"tracks_is_pixel_track",
                            ]
            else:
                region = "PromptDY"
                variables = [
                             "tracks_pt",
                            ]
        
            for variable in variables:
                
                histos = collections.OrderedDict()
                
                
                for category in ["_short", "_long"]:
                    
                    
                    for dataset in datasets:
            
                        if "Run" not in dataset: continue
                        label = "%s_%s_%s_%s%s" % (dataset, variable, region, fakeratetype, category)
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
                            histos[label].GetZaxis().SetLabelSizeser(3e-3, 2e-1)
                            histos[label].GetZaxis().SetTitleOffset(1.2)
                            histos[label].GetXaxis().SetNdivisions(5)
                            histos[label].SetTitle(";%s;%s;fake rate" % (myvariable.split(":")[0], myvariable.split(":")[1]))
            
                            canvas = shared_utils.mkcanvas()
                            canvas.SetRightMargin(0.2)
                            histos[label].Draw("colz")
                            canvas.SetLogz(True)
                            shared_utils.stamp()
                            
                            text = TLatex()
                            text.SetTextFont(132)
                            text.SetTextSize(0.05)
                            text.SetNDC()
                            text.DrawLatex(0.175, 0.825, "%s, %s tracks" % (dataset, category.replace("_", "")))
                            
                            canvas.SaveAs(folder + "_plots/" + label + ".pdf")
            
            
                if ":" not in variable:
                    
                    for i, dataset in enumerate(datasets):       #"Summer16"
                    
                        # only data! FIXME
                        if "Run" not in dataset: continue
                    
                        for category in ["long", "short"]:          #"combined"
                        
                            if category == "combined" and variable != "tracks_is_pixel_track":
                                continue
                        
                            if category == "short":
                                color = kRed
                            elif category == "long":
                                color = kBlue
                            else:
                                color = kBlack
                            
                            if category == "combined":
                                label = "%s_%s_%s_%s" % (dataset, variable.replace(":", "_"), region, fakeratetype)
                            else:
                                label = "%s_%s_%s_%s_%s" % (dataset, variable.replace(":", "_"), region, fakeratetype, category)
                                
                            print label
                                
                            if "Run" not in dataset:
                                histos[label].SetLineStyle(2)
                            
                            histos[label].SetLineColor(color)
                            histos[label].SetTitle(category + " tracks, " + dataset)
                                
                            if category == "combined":
                                break
                              
                    legend = shared_utils.mklegend(x1 = 0.15, y1 = 0.7, x2 = 0.5, y2 = 0.83)
                    legend.SetTextSize(0.04)
                    canvas = shared_utils.mkcanvas()

                    maxvalue = 0
                    
                    for i, label in enumerate(histos):
                        
                        if i == 0:
                            histos[label].Draw("hist e")
                        else:
                            histos[label].Draw("hist e same")

                        histos[label].GetXaxis().SetNdivisions(6)
                        
                        binmax = histos[label].GetMaximumBin()
                        currentmax = histos[label].GetXaxis().GetBinCenter(binmax)
                        print currentmax
                        if currentmax > maxvalue:
                            maxvalue = currentmax
                                                
                        if fakeratetype == "fakerate":
                            ylabel = "Fake rate"
                        elif fakeratetype == "kappa":
                            ylabel = "Prompt transfer factor"
                                                                            
                        histos[label].SetTitle(";%s;%s" % (variable.replace("tracks_pt", "p_{T}^{track} (GeV)"), ylabel))
                        legendlabel = "%s, %s tracks" % (label.split("_")[0], label.split("_")[-1])
                        legend.AddEntry(histos[label], legendlabel)

                    maxvalue = 3
                    for i, label in enumerate(histos):
                        histos[label].GetYaxis().SetRangeUser(0, 1.1 * maxvalue)

                    legend.Draw()
                    shared_utils.stamp()
                        
                    canvas.SaveAs(folder + "_plots/" + fakeratetype + "_" + variable + "_" + identifier + ".pdf")
            
