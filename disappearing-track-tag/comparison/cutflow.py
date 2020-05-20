#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import os
import collections
import shared_utils
import glob
import numpy

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

if __name__ == "__main__":

    canvas = shared_utils.mkcanvas()
    canvas.SetLogy(True)
    
    fin = TFile("../../ntupleanalyzer/skim_18/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-00D93B88-C0A7-E911-9163-001F29087EE8_skim.root")
    h_cutflow_exo = fin.Get("cutflow_exo")
    h_cutflow_mt2 = fin.Get("cutflow_mt2")
    
    shared_utils.histoStyler(h_cutflow_exo)
    shared_utils.histoStyler(h_cutflow_mt2)
    
    h_cutflow_exo.SetTitle("EXO track tag;cut stage;unweighted tracks")
    
    h_cutflow_mt2.SetTitle("MT2 track tag;cut stage;unweighted tracks")    
    
    h_cutflow_exo.Draw("hist")
    shared_utils.stamp()
    canvas.Print("cutflow_exo.pdf")
    
    
    
    