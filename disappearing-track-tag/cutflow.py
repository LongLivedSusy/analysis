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

def plot_cutflow(files, header, is_signal, prefix):
        
    cuts = {}
    
    cuts["BDT_short"] = [
                "tracks_is_pixel_track==1",
                "tracks_pt>30",
                "tracks_trackQualityHighPurity==1",
                "abs(tracks_eta)<2.4",
                "tracks_ptErrOverPt2<10",
                "tracks_dzVtx<0.1",
                "tracks_trkRelIso<0.1",
                "tracks_trackerLayersWithMeasurement>=2",
                "tracks_nValidTrackerHits>=2",
                "tracks_nMissingInnerHits==0",
                "tracks_nValidPixelHits>=2",
                "tracks_passPFCandVeto==1",
                "tracks_passleptonveto==1",
                "tracks_passpionveto==1",
                "tracks_passjetveto==1",
                "tracks_deDxHarmonic2pixel>2.0",
                "tracks_nMissingOuterHits>=0",
                "tracks_mva_tight_may20_chi2_pt10>0",
                "tracks_matchedCaloEnergy/tracks_p<0.12",
    ]
    
    cuts["BDT_long"] = [
                "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
                "tracks_pt>30",
                "tracks_trackQualityHighPurity==1",
                "abs(tracks_eta)<2.4",
                "tracks_ptErrOverPt2<10",
                "tracks_dzVtx<0.1",
                "tracks_trkRelIso<0.1",
                "tracks_trackerLayersWithMeasurement>=2",
                "tracks_nValidTrackerHits>=2",
                "tracks_nMissingInnerHits==0",
                "tracks_nValidPixelHits>=2",
                "tracks_passPFCandVeto==1",                 # removed
                "tracks_passleptonveto==1",
                "tracks_passpionveto==1",
                "tracks_passjetveto==1",                    # removed
                "tracks_deDxHarmonic2pixel>2.0",
                "tracks_nMissingOuterHits>=2",
                "tracks_mva_tight_may20_chi2_pt10>0",
                "tracks_matchedCaloEnergy/tracks_p<0.12",
    ]
    
    
    cuts["updated_BDT_short"] = [
                "tracks_is_pixel_track==1",
                "tracks_pt>10",
                "tracks_trackQualityHighPurity==1",
                "abs(tracks_eta)<2.4",
                "tracks_ptErrOverPt2<10",
                "tracks_dzVtx<0.1",
                "tracks_trkRelIso<0.1",
                "tracks_trackerLayersWithMeasurement>=2",
                "tracks_nValidTrackerHits>=2",
                "tracks_nMissingInnerHits==0",
                "tracks_nValidPixelHits>=2",
                "tracks_passPFCandVeto==1",
                "tracks_passleptonveto==1",
                "tracks_passpionveto==1",
                "tracks_passjetveto==1",
                "tracks_deDxHarmonic2pixel>2.0",
                "tracks_nMissingOuterHits>=0",
                "tracks_mva_tight_may20_chi2_pt10>0",
                "tracks_matchedCaloEnergy/tracks_p<0.3",
    ]
    
    cuts["updated_BDT_long"] = [
                "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
                "tracks_pt>30",
                "tracks_trackQualityHighPurity==1",
                "abs(tracks_eta)<2.4",
                "tracks_ptErrOverPt2<10",
                "tracks_dzVtx<0.1",
                "tracks_trkRelIso<0.1",
                "tracks_trackerLayersWithMeasurement>=2",
                "tracks_nValidTrackerHits>=2",
                "tracks_nMissingInnerHits==0",
                "tracks_nValidPixelHits>=2",
                "tracks_passPFCandVeto>=0",                 # removed
                "tracks_passleptonveto==1",
                "tracks_passpionveto==1",
                "tracks_passjetveto>=0",                    # removed
                "tracks_deDxHarmonic2pixel>2.0",
                "tracks_nMissingOuterHits>=2",
                "tracks_mva_tight_may20_chi2_pt10>0",
                "tracks_matchedCaloEnergy/tracks_p<0.12",
    ]
    
    cuts["MT2_short"] = [
                "tracks_is_pixel_track==1",
                "tracks_pt>15",
                "abs(tracks_eta)<2.4",
                "(abs(tracks_eta)<1.38 || abs(tracks_eta)>1.6)",
                "tracks_ptErrOverPt2<0.2",
                "tracks_dxyVtx<0.02",
                "tracks_dzVtx<0.05",
                "tracks_neutralPtSum<10",
                "tracks_neutralPtSum/tracks_pt<0.1",
                "tracks_chargedPtSum<10",
                "tracks_chargedPtSum/tracks_pt<0.2",
                "tracks_pixelLayersWithMeasurement>=3",     #CHECK THIS
                "tracks_nMissingInnerHits==0",
                "tracks_nMissingOuterHits>=2",
                "tracks_passPFCandVeto==1",
                "tracks_mt2_leptoniso==1",
                "tracks_mt2_trackiso==1",
    ]
    
    cuts["MT2_long"] = [
                "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
                "tracks_pt>15",
                "abs(tracks_eta)<2.4",
                "(abs(tracks_eta)<1.38 || abs(tracks_eta)>1.6)",
                "tracks_ptErrOverPt2<0.005",
                "tracks_dxyVtx<0.01",
                "tracks_dzVtx<0.05",
                "tracks_neutralPtSum<10",
                "tracks_neutralPtSum/tracks_pt<0.1",
                "tracks_chargedPtSum<10",
                "tracks_chargedPtSum/tracks_pt<0.2",
                "tracks_pixelLayersWithMeasurement>=2",
                "tracks_nMissingInnerHits==0",
                "tracks_nMissingOuterHits>=2",
                "tracks_passPFCandVeto==1",
                "tracks_mt2_leptoniso==1",
                "tracks_mt2_trackiso==1",
    ]
    
    cuts["EXO_short"] = [
                "tracks_is_pixel_track==1",
                "tracks_pt>10",                                                 # 55->30
                "abs(tracks_eta)<2.1",
                "tracks_exo_trackiso==1",
                "tracks_exo_jetiso==1",
                "tracks_dxyVtx<0.02",
                "tracks_dzVtx<0.5",
                "tracks_nMissingInnerHits==0",
                "tracks_nMissingMiddleHits==0",
                "tracks_nValidPixelHits>=3",
                "tracks_exo_leptoniso==1",
                "(abs(tracks_eta)<0.15 || abs(tracks_eta)>0.35)",
                "(abs(tracks_eta)<1.42 || abs(tracks_eta)>1.65)",
                "(abs(tracks_eta)<1.55 || abs(tracks_eta)>1.85)",
                "tracks_trkRelIso<0.05",
                "tracks_nMissingOuterHits>=3",                                 
                "tracks_matchedCaloEnergy<10",                
    ]
    
    cuts["EXO_long"] = [
                "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
                "tracks_pt>10",                                                 # 55->30
                "abs(tracks_eta)<2.1",
                "tracks_exo_trackiso==1",
                "tracks_exo_jetiso==1",
                "tracks_dxyVtx<0.02",
                "tracks_dzVtx<0.5",
                "tracks_nMissingInnerHits==0",
                "tracks_nMissingMiddleHits==0",
                "tracks_nValidPixelHits>=3",
                "tracks_exo_leptoniso==1",
                "(abs(tracks_eta)<0.15 || abs(tracks_eta)>0.35)",
                "(abs(tracks_eta)<1.42 || abs(tracks_eta)>1.65)",
                "(abs(tracks_eta)<1.55 || abs(tracks_eta)>1.85)",
                "tracks_trkRelIso<0.05",
                "tracks_nMissingOuterHits>=3",
                "tracks_matchedCaloEnergy<10",                
    ]
    
    if is_signal:
        signal_cutstring = " && tracks_chiCandGenMatchingDR<0.01"
    else:
        signal_cutstring = ""
    
    histos = {}
    for label in cuts:
        histos[label] = TH1D(label, label, 20, 0, 20)
    
    # get consecutive cuts:
    cuts_consecutive = {}
    for label in cuts:
        cuts_consecutive[label] = []
        for i, cut in enumerate(cuts[label]):
            cuts_consecutive[label].append(" && ".join(cuts[label][:i+1]))

    # get nev:
    counts = {} 
    for label in cuts_consecutive:
        counts[label] = []
        for i, cut in enumerate(cuts_consecutive[label]):
            
            if "p1" in prefix:
                #FIXME phase 1 dE/dx
                cut = cut.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
            
            h_tmp = plotting.get_all_histos(files, "Events", "tracks_is_pixel_track", cut + signal_cutstring, nBinsX=2, xmin=0, xmax=2)
            if h_tmp:
                count = h_tmp.Integral()
            else:
                count = 0
            counts[label].append(count)
            histos[label].Fill(i, count)
    
    # normalize histos:
    for label in histos:
        normalization = histos[label].GetBinContent(1)
        if normalization > 0:
            histos[label].Scale(1.0/normalization)
        
    # set alphanumeric x-axis labels:
    for label in histos:
        for i in range(histos[label].GetNbinsX()):
            if i<=len(cuts[label]):           
                
                binlabel = cuts[label][i-1]
                if "tracks_is_pixel_track" in binlabel: binlabel = "category"
                elif "tracks_ptErrOverPt2" in binlabel: binlabel = "#Delta pT"
                elif "tracks_neutralPtSum/tracks_pt" in binlabel: binlabel = "nt. pTSum/pT"
                elif "tracks_neutralPtSum" in binlabel: binlabel = "nt. pTSum"
                elif "tracks_chargedPtSum/tracks_pt" in binlabel: binlabel = "ch. pTSum/pT"
                elif "tracks_chargedPtSum" in binlabel: binlabel = "ch. pTSum"
                elif "tracks_pt" in binlabel: binlabel = "pT"
                elif "tracks_trackQualityHighPurity" in binlabel: binlabel = "purity"
                elif "tracks_eta" in binlabel: binlabel = "eta"
                elif "tracks_dzVtx" in binlabel: binlabel = "dz"
                elif "tracks_dxyVtx" in binlabel: binlabel = "dxy"
                elif "tracks_trkRelIso" in binlabel: binlabel = "relIso"
                elif "tracks_trackerLayersWithMeasurement" in binlabel: binlabel = "layers"
                elif "tracks_nValidTrackerHits" in binlabel: binlabel = "tracker hits"
                elif "tracks_nMissingInnerHits" in binlabel: binlabel = "miss. inner hits"
                elif "tracks_nValidPixelHits" in binlabel: binlabel = "pixel hits"
                elif "tracks_passPFCandVeto" in binlabel: binlabel = "PFCand"
                elif "tracks_passleptonveto" in binlabel: binlabel = "lepton veto"
                elif "tracks_passpionveto" in binlabel: binlabel = "pion veto"
                elif "tracks_passjetveto" in binlabel: binlabel = "jet veto"
                elif "tracks_deDxHarmonic2pixel" in binlabel: binlabel = "dE/dx"
                elif "tracks_mva_tight_may20_chi2" in binlabel: binlabel = "BDT"
                elif "tracks_matchedCaloEnergy/tracks_p" in binlabel: binlabel = "EDep/track p"     
                elif "tracks_nMissingOuterHits" in binlabel: binlabel = "miss. outer hits"
                elif "tracks_nMissingMiddleHits" in binlabel: binlabel = "miss. middle hits"
                elif "tracks_exo_leptoniso" in binlabel: binlabel = "lepton iso"
                elif "tracks_exo_trackiso" in binlabel: binlabel = "track iso"
                elif "tracks_exo_jetiso" in binlabel: binlabel = "jet iso"
                elif "tracks_matchedCaloEnergy" in binlabel: binlabel = "EDep"     
                elif "tracks_mt2_leptoniso" in binlabel: binlabel = "lepton iso"
                elif "tracks_mt2_trackiso" in binlabel: binlabel = "track iso"
                elif "tracks_pixelLayersWithMeasurement" in binlabel: binlabel = "pixel layers"

                histos[label].GetXaxis().SetBinLabel(i, binlabel);
        
    for label in histos:
    
        if "long" in label: continue
    
    	canvas = TCanvas("c1","c1",1000,630)
    	canvas.SetBottomMargin(.16)
    	canvas.SetLeftMargin(.14)
    	canvas.SetGrid()
        
        if is_signal:
            legend = shared_utils.mklegend(x1=0.17, y1=0.17, x2=0.4, y2=0.4)
        else:
            legend = shared_utils.mklegend(x1=0.6, y1=0.7, x2=0.9, y2=0.9)
        legend.SetTextSize(0.03)
            
        shared_utils.histoStyler(histos[label])
        histos[label].Draw("hist")
        histos[label].SetLineColor(kRed)
        histos[label].SetTitle(";;percentage of tracks remaining")
        legend.AddEntry(histos[label], "short tracks")
        
        label_long = label.replace("short", "long")
        shared_utils.histoStyler(histos[label_long])
        histos[label_long].Draw("hist same")
        histos[label_long].SetLineColor(kBlue)
        histos[label_long].SetTitle(";cut stage;tracks")
        legend.AddEntry(histos[label_long], "long tracks")
        
        legend.SetTextSize(0.045)
        legend.SetHeader(header + ", " + label.replace("_short", "").replace("_", " ") + " tag")
        legend.Draw()
        
        shared_utils.stamp()
        canvas.Print("plots/" + prefix + "_" + label.replace("_short", "") + ".pdf")  
                

if __name__ == "__main__":

    signal_p0 = ["../ntupleanalyzer/tools/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_240000-043F9F4D-DA87-E911-A393-0242AC1C0502_RA2AnalysisTree.root"]    
    signal_p1 = ["../ntupleanalyzer/tools/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8-AOD_110000-18089184-3A3B-E911-936C-0025905A60BC_RA2AnalysisTree.root"]    
    background_p0 = ["../ntupleanalyzer/tools/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_120000-40EE4B49-34BB-E611-A332-001E674FB2D4_RA2AnalysisTree.root"]
    background_p1 = ["../ntupleanalyzer/tools/RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8AOD_10000-F8CE1FD1-D253-E811-A8C1-0242AC130002_RA2AnalysisTree.root"]
    
    #plot_cutflow(signal_p0, "Signal phase 0", True, "sg_p0")
    #plot_cutflow(signal_p1, "Signal phase 1", True, "sg_p1")
    plot_cutflow(background_p0, "WJets phase 0", False, "bg_p0")
    plot_cutflow(background_p1, "WJets phase 1", False, "bg_p1")
