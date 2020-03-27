#!/bin/env python
from __future__ import division
from ROOT import *
import collections
import glob
import os
import shared_utils
from optparse import OptionParser
import time

def rebin_histo(histogram, nbins, xmin, xmax):
    h_name = histogram.GetName()
    h_rebinned = TH1F(h_name + "_rebin", h_name + "_rebin", nbins, xmin, xmax)
    for ibin in range(1, histogram.GetXaxis().GetNbins()+1):
        xvalue = histogram.GetBinLowEdge(ibin)
        value = histogram.GetBinContent(ibin)
        valueErr = histogram.GetBinError(ibin)
        
        h_rebinned.SetBinContent(h_rebinned.GetXaxis().FindBin(xvalue), value)
        h_rebinned.SetBinError(h_rebinned.GetXaxis().FindBin(xvalue), valueErr)

    shared_utils.histoStyler(h_rebinned)
    return h_rebinned


if __name__ == "__main__":
        
    root_file_out = "fkbg.root"
    os.system("rm " + root_file_out)
        
    for datalabel in ["Summer16", "Run2016"]:
        
        for variable in ["regionCorrected", "regionCorrected_sideband"]:
        
            for region in ["Baseline"]:
            
                if "region" in variable:
                    root_file = "prediction3_%s.root" % datalabel
                else:
                    root_file = "prediction3_%s.root" % datalabel
                
                h_name = variable + "_" + region + "_" + datalabel + "_fakeprediction"
                
                histos = {}
                fin = TFile(root_file, "read")
                histos[h_name + "_short"] = fin.Get(h_name + "_short")
                histos[h_name + "_long"] = fin.Get(h_name + "_long")
                
                # combine short and long:
                histos[h_name] = histos[h_name + "_short"].Clone()
                histos[h_name].Add(histos[h_name + "_long"])
                
                for label in histos:
                    histos[label].SetDirectory(0)
                    if "Run201" not in label:
                        histos[label].Scale(137000)
                    shared_utils.histoStyler(histos[label])
                fin.Close()
                
                fout = TFile(root_file_out, "update")
                
                newvariable = variable
                newvariable = newvariable.replace("regionCorrected", "BinNumber")
                newvariable = newvariable.replace("region", "BinNumberUncorrected")
                newvariable = newvariable.replace("leadinglepton_mt", "LepMT")
                newvariable = newvariable.replace("tracks_invmass", "InvMass")
                newvariable = newvariable.replace("_sideband", "Sideband")
                newvariable = newvariable.replace("MHT", "Mht")
                newvariable = newvariable.replace("HT", "Ht")
                newvariable = newvariable.replace("n_goodjets", "NJets")
                newvariable = newvariable.replace("n_btags", "BTags")
                
                binningAnalysis = collections.OrderedDict()
                binningAnalysis["region"] = shared_utils.binningAnalysis['BinNumber']
                binningAnalysis["leadinglepton_mt"] = shared_utils.binningAnalysis['LepMT']
                binningAnalysis["tracks_invmass"] = shared_utils.binningAnalysis['InvMass']
                binningAnalysis["MHT"] = shared_utils.binningAnalysis['Mht']
                binningAnalysis["Ht"] = shared_utils.binningAnalysis['Mht']
                binningAnalysis["n_goodjets"] = shared_utils.binningAnalysis['Ht']
                binningAnalysis["n_btags"] = shared_utils.binningAnalysis['BTags']
                
                if "region" in variable:
                    histos[h_name] = rebin_histo(histos[h_name], binningAnalysis["region"][0], binningAnalysis["region"][1], binningAnalysis["region"][2])
                
                if "Run201" in h_name:
                    histos[h_name].SetName("%s_%sMethod" % (region, newvariable))
                    histos[h_name].SetTitle("%s_%sMethod" % (region, newvariable))

                else:
                    histos[h_name].SetName("%s_%sMethodTruth" % (region, newvariable))
                    histos[h_name].SetTitle("%s_%sMethodTruth" % (region, newvariable))                

                histos[h_name].Write()
                
                fout.Close()
                
