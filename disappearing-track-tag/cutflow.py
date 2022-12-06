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

cuts = {}

cuts["BDT_short"] = [
            "tracks_is_pixel_track==1",
            "tracks_pt>25",
            "tracks_passmask==1",
            "tracks_trackQualityHighPurity==1",
            "abs(tracks_eta)<2.0",
            "tracks_ptErrOverPt2<10",
            "tracks_dxyVtx<0.1",
            "tracks_dzVtx<0.1",
            "tracks_trkRelIso<0.2",
            "tracks_trackerLayersWithMeasurement>=2",
            "tracks_nValidTrackerHits>=2",
            "tracks_nMissingInnerHits==0",
            "tracks_nValidPixelHits>=2",
            "tracks_passPFCandVeto==1",
            "tracks_passleptonveto==1",
            "tracks_passpionveto==1",
            "tracks_passjetveto==1",
            #"tracks_deDxHarmonic2pixel>2.0",
            "tracks_nMissingOuterHits>=0",
            "tracks_matchedCaloEnergy<0.15",
            "tracks_mva_nov20_noEdep>0.1",
]

cuts["BDT_long"] = [
            "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
            "tracks_pt>40",
            "tracks_passmask==1",
            "tracks_trackQualityHighPurity==1",
            "abs(tracks_eta)<2.0",
            "tracks_ptErrOverPt2<10",
            "tracks_dxyVtx<0.1",
            "tracks_dzVtx<0.1",
            "tracks_trkRelIso<0.2",
            "tracks_trackerLayersWithMeasurement>=2",
            "tracks_nValidTrackerHits>=2",
            "tracks_nMissingInnerHits==0",
            "tracks_nValidPixelHits>=2",
            "tracks_passPFCandVeto==1",
            "tracks_passleptonveto==1",
            "tracks_passpionveto==1",
            "tracks_passjetveto==1",
            #"tracks_deDxHarmonic2pixel>2.0",
            "tracks_nMissingOuterHits>=2",
            "tracks_matchedCaloEnergy/tracks_p<0.2",
            "tracks_mva_nov20_noEdep>0.12",
]

cuts["BDT_noJetVeto_short"] = [
            "tracks_is_pixel_track==1",
            "tracks_pt>25",
            "tracks_passmask==1",
            "tracks_trackQualityHighPurity==1",
            "abs(tracks_eta)<2.0",
            "tracks_ptErrOverPt2<10",
            "tracks_dxyVtx<0.1",
            "tracks_dzVtx<0.1",
            "tracks_trkRelIso<0.2",
            "tracks_trackerLayersWithMeasurement>=2",
            "tracks_nValidTrackerHits>=2",
            "tracks_nMissingInnerHits==0",
            "tracks_nValidPixelHits>=2",
            "tracks_passPFCandVeto==1",
            "tracks_passleptonveto==1",
            "tracks_passpionveto==1",
            #"tracks_passjetveto==1",
            #"tracks_deDxHarmonic2pixel>2.0",
            "tracks_nMissingOuterHits>=0",
            "tracks_matchedCaloEnergy/tracks_p<0.2 && tracks_matchedCaloEnergy<20",
            "tracks_mva_nov20_noEdep>0.1",

]

cuts["BDT_noJetVeto_long"] = [
            "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
            "tracks_pt>40",
            "tracks_passmask==1",
            "tracks_trackQualityHighPurity==1",
            "abs(tracks_eta)<2.0",
            "tracks_ptErrOverPt2<10",
            "tracks_dxyVtx<0.1",
            "tracks_dzVtx<0.1",
            "tracks_trkRelIso<0.2",
            "tracks_trackerLayersWithMeasurement>=2",
            "tracks_nValidTrackerHits>=2",
            "tracks_nMissingInnerHits==0",
            "tracks_nValidPixelHits>=2",
            "tracks_passPFCandVeto==1",
            "tracks_passleptonveto==1",
            "tracks_passpionveto==1",
            "tracks_passjetveto==1",
            #"tracks_deDxHarmonic2pixel>2.0",
            "tracks_nMissingOuterHits>=2",
            "tracks_matchedCaloEnergy/tracks_p<0.2 && tracks_matchedCaloEnergy<20",
            "tracks_mva_nov20_noEdep>0.1",
]

cuts["MT2_short"] = [
            "tracks_is_pixel_track==1",
            "tracks_passPFCandVeto==1",
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
            "tracks_pixelLayersWithMeasurement>=3",
            "tracks_nMissingInnerHits==0",
            "tracks_nMissingOuterHits>=2",
            "tracks_mt2_leptoniso==1",
]

cuts["MT2_long"] = [
            "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
            "tracks_passPFCandVeto==1",
            "tracks_pt>15",
            "abs(tracks_eta)<2.4",
            "(abs(tracks_eta)<1.38 || abs(tracks_eta)>1.6)",
            "tracks_ptErrOverPt2<0.02",
            "tracks_dxyVtx<0.01",
            "tracks_dzVtx<0.05",
            "tracks_neutralPtSum<10",
            "tracks_neutralPtSum/tracks_pt<0.1",
            "tracks_chargedPtSum<10",
            "tracks_chargedPtSum/tracks_pt<0.2",
            "tracks_pixelLayersWithMeasurement>=2",
            "tracks_nMissingInnerHits==0",
            "tracks_nMissingOuterHits>=2",
            "tracks_mt2_leptoniso==1",
]

cuts["EXO_short"] = [
            "tracks_is_pixel_track==1",
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
            "tracks_pt>55",
]

cuts["EXO_long"] = [
            "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
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
            "tracks_pt>55",
]

cuts["EXO_noeta_short"] = [
            "tracks_is_pixel_track==1",
            "tracks_exo_trackiso==1",
            "tracks_exo_jetiso==1",
            "tracks_dxyVtx<0.02",
            "tracks_dzVtx<0.5",
            "tracks_nMissingInnerHits==0",
            "tracks_nMissingMiddleHits==0",
            "tracks_nValidPixelHits>=3",
            "tracks_exo_leptoniso==1",
            "tracks_trkRelIso<0.05",
            "tracks_nMissingOuterHits>=3",                                 
            "tracks_matchedCaloEnergy<10",                
            "tracks_pt>55",
]

cuts["EXO_noeta_long"] = [
            "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
            "tracks_exo_trackiso==1",
            "tracks_exo_jetiso==1",
            "tracks_dxyVtx<0.02",
            "tracks_dzVtx<0.5",
            "tracks_nMissingInnerHits==0",
            "tracks_nMissingMiddleHits==0",
            "tracks_nValidPixelHits>=3",
            "tracks_exo_leptoniso==1",
            "tracks_trkRelIso<0.05",
            "tracks_nMissingOuterHits>=3",
            "tracks_matchedCaloEnergy<10",                
            "tracks_pt>55",
]

cuts["EXO_noetapt_short"] = [
            "tracks_is_pixel_track==1",
            "tracks_exo_trackiso==1",
            "tracks_exo_jetiso==1",
            "tracks_dxyVtx<0.02",
            "tracks_dzVtx<0.5",
            "tracks_nMissingInnerHits==0",
            "tracks_nMissingMiddleHits==0",
            "tracks_nValidPixelHits>=3",
            "tracks_exo_leptoniso==1",
            "tracks_trkRelIso<0.05",
            "tracks_nMissingOuterHits>=3",                                 
            "tracks_matchedCaloEnergy<10",                
            #"tracks_pt>55",
]

cuts["EXO_noetapt_long"] = [
            "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
            "tracks_exo_trackiso==1",
            "tracks_exo_jetiso==1",
            "tracks_dxyVtx<0.02",
            "tracks_dzVtx<0.5",
            "tracks_nMissingInnerHits==0",
            "tracks_nMissingMiddleHits==0",
            "tracks_nValidPixelHits>=3",
            "tracks_exo_leptoniso==1",
            "tracks_trkRelIso<0.05",
            "tracks_nMissingOuterHits>=3",
            "tracks_matchedCaloEnergy<10",                
            #"tracks_pt>55",
]

cuts["EXO_pt15_short"] = [
            "tracks_is_pixel_track==1",
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
            "tracks_pt>15",
]

cuts["EXO_pt15_long"] = [
            "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
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
            "tracks_pt>15",
]




def plot_cutflow(files, header, is_signal, prefix):
            
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
                elif "tracks_ptErrOverPt2" in binlabel: binlabel = "#Delta p_{T}"
                elif "tracks_neutralPtSum/tracks_pt" in binlabel: binlabel = "nt. #Sigma p_{T}/pT"
                elif "tracks_neutralPtSum" in binlabel: binlabel = "nt. pTSum"
                elif "tracks_chargedPtSum/tracks_pt" in binlabel: binlabel = "ch. #Sigma p_{T}/pT"
                elif "tracks_chargedPtSum" in binlabel: binlabel = "ch. #Sigma p_{T}"
                elif "tracks_pt" in binlabel: binlabel = "p_{T}"
                elif "tracks_passmask" in binlabel: binlabel = "mask"
                elif "tracks_trackQualityHighPurity" in binlabel: binlabel = "purity"
                elif "tracks_eta" in binlabel: binlabel = "#eta"
                elif "tracks_dzVtx" in binlabel: binlabel = "d_{z}"
                elif "tracks_dxyVtx" in binlabel: binlabel = "d_{xy}"
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
        
        if "bg" in prefix:
            canvas.SetLogy()
        
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

        if "bg" in prefix:
            histos[label].GetYaxis().SetRangeUser(1e-4,2e0)
        else:
            histos[label].GetYaxis().SetRangeUser(0,1.1)
        
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
        
        batchname = files[0].split("/")[2]
        canvas.Print("plots/cutflow_" + batchname + "_" + prefix + "_" + label.replace("_short", "") + ".pdf")  
        
