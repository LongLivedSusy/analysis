#!/bin/env python
from __future__ import division
from optparse import OptionParser
from ROOT import *
import plotting
import os
import collections
import shared_utils
import glob
import numpy
import collections

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def plot_cutflow(channel, basecuts, category, batchname, numevents = -1):
                        
    if category == "short":
        cuts = [
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
                    "tracks_nMissingOuterHits>=0",
                    "tracks_mva_sep21v1_baseline>$BDTCUT",
                    "tracks_matchedCaloEnergy<15",
        ]
    else:
        cuts = [
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
                    "tracks_nMissingOuterHits>=2",
                    "tracks_mva_sep21v1_baseline>$BDTCUT",
                    "tracks_matchedCaloEnergy/tracks_p<0.2",
        ]
    
    cuts_consecutive = []
    for i, cut in enumerate(cuts):
        cuts_consecutive.append(" && ".join(cuts[:i+1]))
            
    # get counts:
    counts = {}
    histos = {}
    for year in ["2016", "2017", "2018"]:                
        for bgsg in ["T1btbt", "T2tb", "bg"]:

            histos[year + "_" + bgsg] = TH1D(year + "_" + bgsg, year + "_" + bgsg, 20, 0, 20)

            if "T" in bgsg:
                if "2016" in year or "2017" in year:
                    mcstring = "RunIIFall17FSv3"
                elif "2018" in year:
                    mcstring = "RunIIAutumn18FSv3"
                files = mcstring + ".SMS-" + bgsg + "*"

            else:
                if channel == "hadronic":
                    if "2016" in year:
                        files = "Summer16.QCD*"
                    elif "2017" in year or "2018" in year:
                        files = "RunIIFall17MiniAODv2.QCD*"
                else:
                    if "2016" in year:
                        files = "Summer16.WJets*"
                    elif "2017" in year or "2018" in year:
                        files = "RunIIFall17MiniAODv2.WJets*"

            files = ["../ntupleanalyzer/skim_cutflowOct9_merged/" + files + ".root"]

            print year, bgsg, files
            
            counts[year + "_" + bgsg] = []
            for i, cut in enumerate(cuts_consecutive):
                                                
                finalcuts = basecuts + cut

                if "2016" in year:
                    if category == "short":
                        finalcuts = finalcuts.replace("$BDTCUT", "0.1")
                    else:
                        finalcuts = finalcuts.replace("$BDTCUT", "0.12")
                elif "2017" in year or "2018" in year:
                    if category == "short":
                        finalcuts = finalcuts.replace("$BDTCUT", "0.15")
                    else:
                        finalcuts = finalcuts.replace("$BDTCUT", "0.08")                
                                                    
                if "bg" not in bgsg:
                    finalcuts = finalcuts + " && tracks_chiCandGenMatchingDR<0.01"

                #Select specific model point
                #if "T1btbt" in bgsg:
                #    finalcuts += " && SusyMotherMass==1000 && SusyLSPMass==900"
                #elif "T2tb" in bgsg:
                #    finalcuts += " && SusyMotherMass==1500 && SusyLSPMass==1100"

                h_tmp = plotting.get_all_histos(files, "Events", "tracks_is_pixel_track", cutstring = finalcuts, nBinsX=2, xmin=0, xmax=2, numevents=numevents)

                if h_tmp:
                    count = h_tmp.Integral()
                else:
                    count = 0
                counts[year + "_" + bgsg].append(count)
                histos[year + "_" + bgsg].Fill(i, count)
        
    # Scale lumis:
    for bgsg in ["T1btbt", "T2tb", "bg"]:
        histos["Run2" + "_" + bgsg] = histos["2016" + "_" + bgsg]
        histos["Run2" + "_" + bgsg].Scale(36.3/136.76)
        histos["Run2" + "_" + bgsg].SetDirectory(0)
        histos["Run2" + "_" + bgsg].Add(histos["2017" + "_" + bgsg])
        histos["Run2" + "_" + bgsg].Scale(41.37/136.76)
        histos["Run2" + "_" + bgsg].Add(histos["2018" + "_" + bgsg])
        histos["Run2" + "_" + bgsg].Scale(59.09/136.76)
    
    # normalize histos:
    for label in histos:
        normalization = histos[label].GetBinContent(1)
        if normalization > 0:
            histos[label].Scale(1.0/normalization)
        
    # set alphanumeric x-axis labels:
    for label in histos:
        for i in range(1, histos[label].GetNbinsX() + 1):
            #if i<=len(cuts[label.replace("sg_", "").replace("bg_", "").replace("T1btbt_", "").replace("T2tb_", "")]):           
            if i<=len(cuts):           
                
                #binlabel = cuts[label.replace("sg_", "").replace("bg_", "")][i-1]
                binlabel = cuts[i-1]
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
                elif "tracks_mva_" in binlabel: binlabel = "BDT"
                elif "tracks_matchedCaloEnergy/tracks_p" in binlabel: binlabel = "EDep/track p"     
                elif "tracks_nMissingOuterHits" in binlabel: binlabel = "miss. outer hits"
                elif "tracks_nMissingMiddleHits" in binlabel: binlabel = "miss. middle hits"
                elif "tracks_exo_leptoniso" in binlabel: binlabel = "lepton iso"
                elif "tracks_exo_trackiso" in binlabel: binlabel = "track iso"
                elif "tracks_exo_jetiso" in binlabel: binlabel = "jet iso"
                #elif "tracks_matchedCaloEnergy" in binlabel: binlabel = "$E_{\text{dep}}$"     
                elif "tracks_matchedCaloEnergy" in binlabel: binlabel = "E_{dep}"     
                elif "tracks_mt2_leptoniso" in binlabel: binlabel = "lepton iso"
                elif "tracks_mt2_trackiso" in binlabel: binlabel = "track iso"
                elif "tracks_pixelLayersWithMeasurement" in binlabel: binlabel = "pixel layers"
                elif "tracks_mva_sep21v1_baseline" in binlabel: binlabel = "BDT"
                histos[label].GetXaxis().SetBinLabel(i, binlabel)
        
	canvas = TCanvas("c1","c1",1000,630)
	canvas.SetBottomMargin(.16)
	canvas.SetLeftMargin(.14)
	canvas.SetGrid()
        
    legend = shared_utils.mklegend(x1=0.17, y1=0.17, x2=0.4, y2=0.4)
    legend.SetTextSize(0.03)
        
    #for i_label, label in enumerate(cuts.keys()):
    #for i_label, label in enumerate(cuts):
    i = 0
    for year in [
                 "Run2",
                 #"2016",
                 #"2017",
                 #"2018"
                 ]:                
        for bgsg in ["T1btbt", "T2tb", "bg"]:
        
            if i == 0:
                drawoptions = "hist"
            else:
                drawoptions = "hist same"
            i+=1
        
            identifier = year + "_" + bgsg
            shared_utils.histoStyler(histos[identifier])
            
            if "T1btbt" in bgsg:
                histos[identifier].SetLineColor(kRed)
            elif "T2tb" in bgsg:
                histos[identifier].SetLineColor(kBlue)
                    
            histos[identifier].GetXaxis().SetLabelSize(0.5 * histos[identifier].GetXaxis().GetLabelSize())
            histos[identifier].GetYaxis().SetLabelSize(histos[identifier].GetXaxis().GetLabelSize())
            histos[identifier].GetZaxis().SetLabelSize(0.6 * histos[identifier].GetYaxis().GetLabelSize())
            histos[identifier].GetYaxis().SetTitleSize(0.7 * histos[identifier].GetYaxis().GetTitleSize())
            histos[identifier].GetYaxis().SetMaxDigits(4)
            histos[identifier].SetTitleSize(0.6 * histos[identifier].GetTitleSize())            
                    
            histos[identifier].Draw(drawoptions)
            
            if bgsg == "bg":
                histos[identifier].SetLineStyle(2)
            else:
                histos[identifier].SetLineStyle(1)
            
            histos[identifier].SetTitle(";;percentage of tracks remaining")
            legend.AddEntry(histos[identifier], bgsg.replace("bg", "background").replace("T2tb", "T6tbLL").replace("T1btbt", "T5btbtLL"))
            histos[identifier].GetYaxis().SetRangeUser(0,1.1)
                        
    legend.SetTextSize(0.045)
    legend.SetHeader(category + " tracks")
    legend.Draw()
            
    shared_utils.stamp()

    canvas.Print("plots/cutflow_" + category + "_" + batchname + ".pdf")  
    canvas.SaveAs("plots/cutflow_" + category + "_" + batchname + ".root")  
        

if __name__ == "__main__":
    
    parser = OptionParser()
    parser.add_option("--index", dest="index", default=-1)
    (options, args) = parser.parse_args()
    options.index = int(options.index)
    
    batchname = "new"
    
    for category in [
                     "short",
                     #"long",
                    ]:
                    
        plot_cutflow("hadronic", "HT>150 && MHT>150 && n_goodjets>=1 && n_goodelectrons==0 && n_goodmuons==0 && ", category, batchname)
        #plot_cutflow("electron", "MHT>30 && n_goodjets>=1 && n_goodelectrons>=1 && tracks_invmass>120 && leadinglepton_mt>110 && ", category, batchname)
        #plot_cutflow("muon",     "MHT>30 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>120 && leadinglepton_mt>110 && ", category, batchname)
