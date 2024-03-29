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
     
    # check data period:
    #data_periods = []
    #merged_files = glob.glob(folder + "_fakerate/merged_*.root")
    #for merged_file in merged_files:
    #    if "All" in merged_file: continue
    #    for period in ["Summer16", "Fall17", "Run2016", "Run2017", "Run2018"]:
    #        if period in merged_file and period not in data_periods:
    #                data_periods.append(period)
    #                print "Looking at %s" % period 
    
    for dataset in [
                    #"Run2",
                    "Summer16",
                    "Fall17",                    
                    "Run2016",
                    "Run20172018",
                   ]:
        for fakeratetype in ["fakerate", "kappa", "mukappa"]: 
            if fakeratetype == "fakerate":
                region = "QCDLowMHT"
                variables = [
                             "tracks_eta",
                            ]
            elif fakeratetype == "kappa":
                region = "PromptDYEl"
                variables = [
                             "tracks_pt",
                            ]
            elif fakeratetype == "mukappa":
                region = "PromptDYMu"
                variables = [
                             "tracks_pt",
                            ]
        
            for variable in variables:
                histos = collections.OrderedDict()
                for category in ["_short", "_long"]:    
            
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
                    for category in ["long", "short"]:
                    
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
                            ylabel = "Fake transfer factor"
                        elif fakeratetype == "kappa":
                            ylabel = "Prompt transfer factor"
                                                 
                        betterlabel = variable                     
                        betterlabel = betterlabel.replace("tracks_pt", "p_{T}^{track} (GeV)")
                        betterlabel = betterlabel.replace("tracks_eta", "|\eta|")
      
                        histos[label].SetTitle(";%s;%s" % (betterlabel, ylabel))
                        legendlabel = "%s, %s tracks" % (label.split("_")[0], label.split("_")[-1])

                        legendlabel = legendlabel.replace("Run2016", "Data phase 0")
                        legendlabel = legendlabel.replace("Run20172018", "Data phase 1")
                        legendlabel = legendlabel.replace("Summer16", "MC phase 0")
                        legendlabel = legendlabel.replace("Fall17", "MC phase 1")

                        legend.AddEntry(histos[label], legendlabel)

                    maxvalue = 3
                    for i, label in enumerate(histos):
                        if fakeratetype == "fakerate":
                            histos[label].GetYaxis().SetRangeUser(0, 1.5)
                        else:
                            histos[label].GetYaxis().SetRangeUser(0, 1.5)


                    legend.Draw()
                    shared_utils.stamp()
                        
                    canvas.SaveAs(folder + "_plots/" + fakeratetype + "_" + variable + "_" + dataset + ".pdf")
            
