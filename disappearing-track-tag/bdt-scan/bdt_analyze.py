#!/bin/env python
from __future__ import division
from ROOT import *
import ROOT
import math
import tmva_tools
import glob
import os
import uuid

#gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def read_catalogue(catalogue_file):

    configurations = {}

    # line:
    # cmssw8-short-2-50-3bc44cee: ['dxyVtx', 'dzVtx', 'matchedCaloEnergy', 'trkRelIso', 'nValidPixelHits', 'nValidTrackerHits', 'ptErrOverPt2'], pt>15 && abs(eta)<2.4 && passPFCandVeto==1 && trackQualityHighPurity==1 && dxyVtx<0.1 && dzVtx<0.1 && trkRelIso<0.2 && ptErrOverPt2<0.5, n_depth=50, n_trees=2, /nfs/dust/cms/user/kutznerv/DisappTrksNtuple-cmssw8/tracks-mini-short

    with open(catalogue_file) as f:
        lines = f.readlines()
        for line in lines:
            folder_name = line.split(":")[0]
            variables = line.split(":")[1].split(",")[0]
            preselection = line.split(":")[1].split(",")[1]
            n_depth = line.split(":")[1].split(",")[2]
            n_trees = line.split(":")[1].split(",")[3]
            configurations[folder_name] = {"variables": variables, "preselection": preselection, "n_depth": n_depth, "n_trees": n_trees}

    return configurations
     

def analyze_tmva_output(tmva_output_folder, min_x_value = 50.0):

    fin = TFile(tmva_output_folder + "/output.root")
    h_mva_bdt_B = fin.Get("Method_BDT/BDT/MVA_BDT_B")
    h_mva_bdt_S = fin.Get("Method_BDT/BDT/MVA_BDT_S")
    h_mva_bdt_effB = fin.Get("Method_BDT/BDT/MVA_BDT_effB")
    h_mva_bdt_effS = fin.Get("Method_BDT/BDT/MVA_BDT_effS")

    fNSignal = h_mva_bdt_S.GetEntries()
    fNBackground = h_mva_bdt_B.GetEntries()

    h_roc = TGraph()
    h_significance = TH1D("sig_" + tmva_output_folder, "sig_" + tmva_output_folder, h_mva_bdt_effS.GetNbinsX(), h_mva_bdt_effS.GetXaxis().GetXmin(), h_mva_bdt_effS.GetXaxis().GetXmax())

    for i in range(1, h_significance.GetNbinsX()):

        mva = h_mva_bdt_effS.GetBinCenter(i)
        eff_S = h_mva_bdt_effS.GetBinContent(i)
        eff_B = h_mva_bdt_effB.GetBinContent(i)

        h_roc.SetPoint(i, eff_S, 1-eff_B)

        S = eff_S * fNSignal
        B = eff_B * fNBackground
        if (S+B)>0:
            sign = 1.0 * S/math.sqrt(S+B)
            h_significance.SetBinContent(i, sign)
            h_significance.SetBinError(i, 0)

    # set first and last point:
    #h_roc.SetPoint(0, h_mva_bdt_effS.GetBinContent(h_roc.GetN()-1), 0)
    #h_roc.SetPoint(h_roc.GetN(), h_mva_bdt_effS.GetBinContent(h_roc.GetN()-1), 0)
    h_roc.SetPoint(0, 0, 0)   
    dummy = Double(0)
    yval = Double(0)
    h_roc.GetPoint(h_roc.GetN()-1, dummy, yval)
    h_roc.SetPoint(h_roc.GetN(), 0, yval)
    h_roc.SetPoint(h_roc.GetN(), 0, 0)

    # get integral value:
    area = h_roc.Integral(h_roc.GetXaxis().FindBin(min_x_value), -1)
    print "area=%s, min_x_value=%s, folder=%s" % (area, min_x_value, tmva_output_folder)

    h_significance.Scale(1.0/h_significance.GetMaximum())

    min_mva_value = h_significance.GetBinCenter(h_significance.GetMaximumBin())
    eff_sg_best_Z = h_mva_bdt_effS.GetBinContent(h_significance.GetMaximumBin())
    eff_bg_rejection_best_Z = 1 - h_mva_bdt_effB.GetBinContent(h_significance.GetMaximumBin())

    h_roc_out = h_roc.Clone()
    h_significance_out = h_significance.Clone()
    h_significance_out.SetDirectory(0)
    fin.Close()

    return h_roc_out, h_significance_out, min_mva_value, eff_sg_best_Z, eff_bg_rejection_best_Z, area, min_x_value


if __name__ == "__main__":

    configs = read_catalogue("tmva/tmva_catalogue")

    for label in configs:
        
        print configs[label]
        quit()
        
        h_roc, h_significance, min_mva_value, eff_sg_best_Z, eff_bg_rejection_best_Z, area, min_x_value = analyze_tmva_output("tmva/" + label, min_x_value = 50.0)
        





