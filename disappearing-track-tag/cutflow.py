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

def exoandmt2(sg_file):
    
    canvas = shared_utils.mkcanvas()
    shared_utils.stamp()
    canvas.SetLogy(True)
    
    fin = TFile(sg_file)
    h_cutflow_exo = fin.Get("cutflow_exo")
    h_cutflow_mt2 = fin.Get("cutflow_mt2")
    
    shared_utils.histoStyler(h_cutflow_exo)
    shared_utils.histoStyler(h_cutflow_mt2)
    
    h_cutflow_exo.SetTitle(";cut stage;unweighted tracks")
    h_cutflow_mt2.SetTitle(";cut stage;unweighted tracks")    
    
    h_cutflow_exo.Draw("hist")
    canvas.Print("cutflow_exo_sg.pdf")
    
    h_cutflow_mt2.Draw("hist")
    h_cutflow_mt2.GetXaxis().SetRangeUser(100,120)
    canvas.Print("cutflow_mt2_short_sg.pdf")
    h_cutflow_mt2.GetXaxis().SetRangeUser(200,220)
    canvas.Print("cutflow_mt2_medium_sg.pdf")
    h_cutflow_mt2.GetXaxis().SetRangeUser(300,320)
    canvas.Print("cutflow_mt2_long_sg.pdf")
    
    
def bdttag(files, is_signal=True):
    
    canvas = shared_utils.mkcanvas()
    canvas.SetLogy(True)
    
    legend = shared_utils.mklegend(x1=0.55, y1=0.75, x2=0.9, y2=0.9)
    legend.SetTextSize(0.03)
    
    tree = TChain("Events")
    for i_file in files:
        tree.Add(i_file)
    
    if is_signal:
        special_cutstring = "tracks_chiCandGenMatchingDR<0.01"
    else:
        special_cutstring = "tracks_pt>=0"
        
    baseline_selection = [
        "abs(tracks_eta)<2.4",                                                             # 3
        "!(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566)",                              # 4
        "tracks_highpurity==1",                                                            # 5
        "tracks_ptErrOverPt2<10",                                                          # 6
        "tracks_dxyVtx<0.1",                                                               # 7
        "tracks_dzVtx<0.1",                                                                # 8
        "tracks_trkRelIso<0.2",                                                            # 9
        "tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2",           # 10
        "tracks_nMissingInnerHits==0",                                                     # 11
        "tracks_nMissingMiddleHits==0",                                                    # 12
        "tracks_chi2perNdof<2.88",                                                         # 13
        "tracks_pixelLayersWithMeasurement>2",                                             # 14
        "tracks_passmask==1",                                                              # 15
                         ]                                                                      
                                                                                           
    vetoes = [
        "tracks_pass_reco_lepton==1",                                                      # 16
        "tracks_passPFCandVeto==1",                                                        # 17
        "tracks_nValidPixelHits>=3",                                                       # 18
        "tracks_passpionveto==1",                                                          # 19
        "tracks_passjetveto==1",                                                           # 20
             ]                                                                             
                                                                                           
    cuts_short = [
        "tracks_pt>=0",                                                                    # 0
        "tracks_is_pixel_track==1",                                                        # 1
        special_cutstring,                                                                 # 2
                 ] + baseline_selection + vetoes + [                                           
        "tracks_mva_loose>(tracks_dxyVtx*(0.65/0.01)-0.5)",                                # 21
        "tracks_trkRelIso<0.01",                                                           # 22
        "tracks_matchedCaloEnergy<10"                                                      # 23
           ]                                                                               
                                                                                           
    cuts_long = [
        "tracks_pt>=0",                                                                    # 0
        "tracks_is_pixel_track==0",                                                        # 1
        special_cutstring,                                                                 # 2
                ] + baseline_selection + vetoes + [                                            
        "tracks_mva_loose>(tracks_dxyVtx*(0.7/0.01)-0.05)",                                # 21
        "tracks_trkRelIso<0.01",                                                           # 22
        "tracks_matchedCaloEnergy<10"                                                      # 23
           ]

    xmax = 30

    h_short = TH1D("short", "short", xmax, 0, xmax)
    h_long = TH1D("long", "long", xmax, 0, xmax)
    shared_utils.histoStyler(h_short)
    shared_utils.histoStyler(h_long)
    h_short.SetTitle(";cut stage;unweighted tracks")
    h_short.SetLineColor(kRed-4)
    h_long.SetTitle(";cut stage;unweighted tracks")    
    h_long.SetLineColor(kAzure+7)

    if is_signal:
        legend.AddEntry(h_short, "short #chi-matched tracks")
        legend.AddEntry(h_long, "long #chi-matched tracks")
    else:
        legend.AddEntry(h_short, "short background tracks")
        legend.AddEntry(h_long, "long background tracks")
        
    cuts_short_consecutive = []
    for i, cut in enumerate(cuts_short):
        cuts_short_consecutive.append(" && ".join(cuts_short[:i+1]))

    cuts_long_consecutive = []
    for i, cut in enumerate(cuts_long):
        cuts_long_consecutive.append(" && ".join(cuts_long[:i+1]))
    
    for i, cut in enumerate(cuts_short_consecutive):
        print "short", i
        currenthisto = plotting.get_histogram_from_file(files, "Events", "tracks_is_pixel_track", cut, nBinsX=2, xmin=0, xmax=2, unweighted=True)
        count = currenthisto.Integral()
        h_short.Fill(i, count)
        
    for i, cut in enumerate(cuts_long_consecutive):
        print "long", i
        currenthisto = plotting.get_histogram_from_file(files, "Events", "tracks_is_pixel_track", cut, nBinsX=2, xmin=0, xmax=2, unweighted=True)
        count = currenthisto.Integral()
        h_long.Fill(i, count)
        
    h_short.Draw("hist")
    h_long.Draw("same hist")
        
    legend.Draw()
    shared_utils.stamp()
    if is_signal:
        canvas.Print("cutflow_bdt_sg.pdf")
        canvas.Print("cutflow_bdt_sg.root")
    else:
        canvas.Print("cutflow_bdt_bg.pdf")
        canvas.Print("cutflow_bdt_bg.root")
        

if __name__ == "__main__":

    sg_file = "../ntupleanalyzer/skim_19/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-00D93B88-C0A7-E911-9163-001F29087EE8_skim.root"    
    bg_file = "../ntupleanalyzer/skim_19/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2AOD_100000-0034ACBB-B9D5-E611-B27B-0CC47A78A436_skim.root"
    exoandmt2(sg_file)
    
    #sg_files = glob.glob("../ntupleanalyzer/skim_19/RunIISummer16MiniAODv3.SMS-T2*.root")    
    #bg_files = glob.glob("../ntupleanalyzer/skim_19/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV*.root")    

    sg_files = [sg_file]
    bg_files = [bg_file]
    
    bdttag(sg_files, is_signal = True)
    bdttag(bg_files, is_signal = False)
    