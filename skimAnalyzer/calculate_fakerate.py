#!/bin/env python
from __future__ import division
from ROOT import *
import collections
import glob
import os
import shared_utils
import array

def rebin(histo, variable, category):

    if variable == "HT_n_allvertices":
        if category == "short":
            histo = histo.RebinX(3)
            histo = histo.RebinY(3)
        else:
            histo = histo.RebinX(3)
            histo = histo.RebinY(3)
    
    elif variable == "HT":
        if category == "short":
            histo = histo.Rebin(10)
        else:
            histo = histo.Rebin(2)

    elif variable == "n_allvertices":
        histo = histo.Rebin(5)

    elif variable == "n_goodjets":
        histo = histo.Rebin(2)

    elif variable == "MinDeltaPhiMhtJets":
        histo = histo.Rebin(2)

    elif variable == "tracks_pt":
        binning = [0, 100, 200, 300, 400, 1000]
        histo = histo.Rebin(len(binning) - 1, histo.GetTitle(), array.array('d', binning))

    return histo


if __name__ == "__main__":

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
   
    variables = [
                 #"tracks_pt",
                 #"HT",
                 #"n_goodjets",
                 #"n_allvertices",
                 #"n_btags",
                 #"MinDeltaPhiMhtJets",
                 "HT:n_allvertices",
                 #"tracks_eta:tracks_phi",
                ]

    #datasets = ["Summer16", "Run2016", "Run2017", "Run2018", "Run2016B", "Run2016C", "Run2016D", "Run2016E", "Run2016F", "Run2016G", "Run2016H", "Run2017B", "Run2017C", "Run2017D", "Run2017E", "Run2017F", "Run2018A", "Run2018B", "Run2018C", "Run2018D"]
    datasets = ["Summer16", "Run2016", "Run2016GH"]
    
    output_file = "fakerate3.root"
    numdenom_file = "fakerate_numdenom3.root"
    os.system("mv %s %s.bak" % (output_file, output_file))

    #datasets = ["Run2016", "Summer16"]
    for dataset in datasets:
        if "Run201" in dataset:
            dataset += "JetHT"
        for variable in variables:
            variable = variable.replace(":", "_")
            for category in ["short", "long"]:
                for region in ["FakeRateDet"]:
                    for region_fakeid in ["", "MVA", "EDep10", "EDep20"]:

                        dedx = ""

                        print "%s_%s_%s_sr%s_%s" % (variable, region, dataset, dedx, category)
                        print "%s_%s_%s_fakecr%s%s_%s" % (variable, region, dataset, region_fakeid, dedx, category)
                        
                        fin = TFile(numdenom_file, "read")       
                        
                        numerator = fin.Get("%s_%s_%s_sr%s_%s" % (variable, region, dataset, dedx, category))
                        numerator.SetDirectory(0)
                        numerator = rebin(numerator, variable, category)
                        
                        denominator = fin.Get("%s_%s_%s_fakecr%s%s_%s" % (variable, region, dataset, region_fakeid, dedx, category))
                        denominator.SetDirectory(0)
                        denominator = rebin(denominator, variable, category)
                        
                        fin.Close()
                        
                        fakerate = numerator.Clone()
                        fakerate.Divide(denominator)
                        fakerate.SetName(fakerate.GetName().replace("_sr", "_fakerate" + region_fakeid).replace("JetHT", ""))
                        fakerate.SetTitle(fakerate.GetTitle().replace("_sr", "_fakerate" + region_fakeid).replace("JetHT", ""))
                        
                        fout = TFile(output_file, "update")
                        fakerate.Write()                        
                        fout.Close()
                        
