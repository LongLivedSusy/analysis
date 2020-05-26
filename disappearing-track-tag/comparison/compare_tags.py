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

def graphStyler(h,color=kBlack):
	h.SetLineWidth(2)
	h.SetLineColor(color)
	h.SetMarkerColor(color)
	size = 0.059 #.059
	font = 132
	h.GetXaxis().SetLabelFont(font)
	h.GetYaxis().SetLabelFont(font)
	h.GetXaxis().SetTitleFont(font)
	h.GetYaxis().SetTitleFont(font)
	h.GetYaxis().SetTitleSize(size)
	h.GetXaxis().SetTitleSize(size)
	h.GetXaxis().SetLabelSize(size)   
	h.GetYaxis().SetLabelSize(size)
	h.GetXaxis().SetTitleOffset(1.0)
	h.GetYaxis().SetTitleOffset(1.05)


def main(quick_mode = False):

    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_21"
        
    labels = collections.OrderedDict()

    labels["Background"] = [
            #"Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1",
            "Summer16.WJetsToLNu_TuneCUETP8M1",
            #"Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
            #"Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1",
            #"Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1",
            #"Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1",
            #"Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1",
            #"Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1",
            #"Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1",
            #"Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1",
            ##"Summer16.QCD_HT200to300_TuneCUETP8M1",
            ##"Summer16.QCD_HT300to500_TuneCUETP8M1",
            ##"Summer16.QCD_HT500to700_TuneCUETP8M1",
            ##"Summer16.QCD_HT700to1000_TuneCUETP8M1",
            ##"Summer16.QCD_HT1000to1500_TuneCUETP8M1",
            ##"Summer16.QCD_HT1500to2000_TuneCUETP8M1",
            ##"Summer16.QCD_HT2000toInf_TuneCUETP8M1",
            #"Summer16.TTJets_DiLept",
            #"Summer16.TTJets_SingleLeptFromT",
            #"Summer16.TTJets_SingleLeptFromTbar",
            ##"Summer16.ZZ_TuneCUETP8M1",
            ##"Summer16.WW_TuneCUETP8M1",
            ##"Summer16.WZ_TuneCUETP8M1",
            ##"Summer16.ZJetsToNuNu_HT-100To200_13TeV",
            ##"Summer16.ZJetsToNuNu_HT-200To400_13TeV",
            ##"Summer16.ZJetsToNuNu_HT-400To600_13TeV",
            ##"Summer16.ZJetsToNuNu_HT-600To800_13TeV",
            ##"Summer16.ZJetsToNuNu_HT-800To1200_13TeV",
            ##"Summer16.ZJetsToNuNu_HT-1200To2500_13TeV",
            ##"Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV",
            ]
    labels["Signal"] = [
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1075_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1275_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1375_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1475_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                ]
                
    if quick_mode:
        labels["Background"] = [
            #"Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1AOD_120000-389A0510-B8BD-E611-8546-008CFAFBF0BA",
            "Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_120000-02067A2D-48BB-E611-BE1E-001E67E71C95",
                               ]
        labels["Signal"] = [
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-00D93B88-C0A7-E911-9163-001F29087EE8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-0270362B-FBA4-E911-AA6B-FA163E3F6D58",
                           ]        
    
    cutstrings = {}
    
    SR_short = "tracks_basecuts==1 && tracks_is_pixel_track==1 && tracks_mva_loose>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
    SR_long = "tracks_basecuts==1 && tracks_is_pixel_track==0 && tracks_mva_loose>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"

    basecuts = "tracks_basecuts==1 && tracks_pass_reco_lepton==1 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_nValidPixelHits[iCand]>=3"
    vetoes = "tracks_pass_reco_lepton==1 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_nValidPixelHits>=3"
    baseline = "abs(tracks_eta)<2.4 && !(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566) && tracks_ptErrOverPt2<10 && tracks_dxyVtx<0.1 && tracks_dzVtx<0.1 && tracks_trkRelIso<0.2 && tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2 && tracks_nMissingInnerHits==0 && tracks_chi2perNdof<2.88 && tracks_pixelLayersWithMeasurement>2 && tracks_nMissingMiddleHits==0"
    
    baseline_loose = [
        "abs(tracks_eta)<2.4",   
        "!(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566)",                              
        "tracks_highpurity==1",  
        "tracks_ptErrOverPt2<10",
        "tracks_dzVtx<0.1",      
        "tracks_trkRelIso<0.2",  
        "tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2",           
        "tracks_nMissingInnerHits==0",                                                     
        "tracks_nValidPixelHits>=3",    
        #"tracks_nMissingMiddleHits==0",
        #"tracks_chi2perNdof<2.88",
        #"tracks_pixelLayersWithMeasurement>=2",
        #"tracks_passmask==1",
        "tracks_pass_reco_lepton==1",
        "tracks_passPFCandVeto==1",                                   
        #"tracks_passpionveto==1",
        #"tracks_passjetveto==1",
             ]
             
    baseline_loose = " && ".join(baseline_loose)
    baseline_tight = baseline_loose + " && tracks_dxyVtx<0.1 "
    
    oldbaseline = [
        "abs(tracks_eta)<2.4",   
        "tracks_highpurity==1",  
        "tracks_ptErrOverPt2<10",
        "tracks_dzVtx<0.1",      
        "tracks_trkRelIso<0.2",  
        "tracks_nMissingMiddleHits==0",                                                     
        #"tracks_passPFCandVeto==1",                                                        
             ]
    
    # short:
    oldbaseline_short_loose = "tracks_is_pixel_track==1 && " + " && ".join(oldbaseline)
    oldbaseline_short_tight = oldbaseline_short_loose + " && tracks_dxyVtx<0.1 "
    # long:
    oldbaseline_long_loose = "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && " + " && ".join(oldbaseline)
    oldbaseline_long_tight = oldbaseline_long_loose + " && tracks_dxyVtx<0.1 "
    
    for i_score in [-10] + list(numpy.arange(-1, 1, 0.1)) + [10]: 
        #cutstrings["pixeltrack_tightBase_%s" % i_score] = oldbaseline_short_tight + "  && tracks_basecuts==1 && tracks_mva_tight>=%s" % i_score
        #cutstrings["pixeltrack_looseBase_%s" % i_score] = oldbaseline_short_loose + " && tracks_basecuts==1 && tracks_mva_loose>=%s" % i_score
        #cutstrings["stripstrack_tightBase_%s" % i_score] = "tracks_nMissingOuterHits>=2 && tracks_mva_tight>=%s" % i_score
        #cutstrings["stripstrack_looseBase_%s" % i_score] = "tracks_nMissingOuterHits>=2 && tracks_mva_loose>=%s" % i_score
        cutstrings["pixeltrack_tightSimple_%s" % i_score] = "tracks_mva_tight>=%s" % i_score
        cutstrings["pixeltrack_looseSimple_%s" % i_score] = "tracks_mva_loose>=%s" % i_score
        cutstrings["pixeltrack_tight2_%s" % i_score] = "tracks_mva_tight_may20>=%s" % i_score
        cutstrings["pixeltrack_loose2_%s" % i_score] = "tracks_mva_loose_may20>=%s" % i_score
        cutstrings["pixeltrack_tight3_%s" % i_score] = "tracks_mva_tight_may20_chi2>=%s" % i_score
        cutstrings["pixeltrack_loose3_%s" % i_score] = "tracks_mva_loose_may20_chi2>=%s" % i_score
        cutstrings["stripstrack_tightSimple_%s" % i_score] = "tracks_nMissingOuterHits>=2 && tracks_mva_tight>=%s" % i_score
        cutstrings["stripstrack_looseSimple_%s" % i_score] = "tracks_nMissingOuterHits>=2 && tracks_mva_loose>=%s" % i_score
        cutstrings["stripstrack_tight2_%s" % i_score] = " tracks_nMissingOuterHits>=2 && tracks_mva_tight_may20>=%s" % i_score
        cutstrings["stripstrack_loose2_%s" % i_score] = " tracks_nMissingOuterHits>=2 && tracks_mva_loose_may20>=%s" % i_score
        cutstrings["stripstrack_tight3_%s" % i_score] = " tracks_nMissingOuterHits>=2 && tracks_mva_tight_may20_chi2>=%s" % i_score
        cutstrings["stripstrack_loose3_%s" % i_score] = " tracks_nMissingOuterHits>=2 && tracks_mva_loose_may20_chi2>=%s" % i_score

    cutstrings["nocuts_short"]              = "tracks_is_pixel_track==1"
    cutstrings["nocuts_long"]               = "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2"
    cutstrings["pixeltrack_bdtEDep10tag"]   = SR_short + " && tracks_matchedCaloEnergy<10"
    cutstrings["stripstrack_bdtEDep10tag"]  = SR_long + " && tracks_matchedCaloEnergy<10 && tracks_nMissingOuterHits>=2 "
    cutstrings["pixeltrack_bdtEDep20tag"]   = SR_short + " && tracks_matchedCaloEnergy<20"
    cutstrings["stripstrack_bdtEDep20tag"]  = SR_long + " && tracks_matchedCaloEnergy<20 && tracks_nMissingOuterHits>=2 "
    #cutstrings["pixeltrack_exotag"]         = "tracks_passexotag==17"
    #cutstrings["stripstrack_exotag"]        = "tracks_passexotag==17 && tracks_nMissingOuterHits>=2"
    cutstrings["pixeltrack_mt2tag"]         = "tracks_passmt2tag==115"
    cutstrings["stripstrack_mt2tag"]        = "(tracks_passmt2tag==215 || tracks_passmt2tag==316) && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test1"]          = "tracks_basecuts==1 && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test1"]         = "tracks_basecuts==1 && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15"
    #cutstrings["pixeltrack_test2"]          = baseline + " && " + vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test2"]         = baseline + " && " + vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15"
    cutstrings["pixeltrack_test3"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    cutstrings["stripstrack_test3"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2"
    cutstrings["pixeltrack_test3b"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<20"
    cutstrings["stripstrack_test3b"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<20 && tracks_nMissingOuterHits>=2"
    cutstrings["pixeltrack_test4"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>0 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    cutstrings["stripstrack_test4"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>0 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2"
    cutstrings["pixeltrack_test5"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>-0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    cutstrings["stripstrack_test5"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>-0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test4"]          = "tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test4"]         = "tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15"
    #cutstrings["pixeltrack_test5"]          = "abs(tracks_eta)<2.4 && !(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566) && tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2 && tracks_nMissingInnerHits==0 && tracks_pixelLayersWithMeasurement>2 && tracks_nMissingMiddleHits==0 && " + vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test5"]         = "abs(tracks_eta)<2.4 && !(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566) && tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2 && tracks_nMissingInnerHits==0 && tracks_pixelLayersWithMeasurement>2 && tracks_nMissingMiddleHits==0 && " + vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15"
    
    histos = {}
    for cut in cutstrings:
        for label in labels:

            cutstring = cutstrings[cut]
            globstrings = labels[label] 
        
            label = label + "_" + cut
        
            if "Signal" in label:
                cutstring += " && tracks_chiCandGenMatchingDR<0.01"
            
            histos[label] = 0        
            for globstring in globstrings:
                input_files = glob.glob(folder + "/" + globstring + "*.root")
                if len(input_files) == 0:
                    print "hmm"
                    continue
                print label, ":\n", ",".join(input_files), "\n"
                currenthisto = plotting.get_histogram_from_file(input_files, "Events", "tracks_is_pixel_track", cutstring, nBinsX=2, xmin=0, xmax=2)
                if histos[label] == 0:
                    histos[label] = currenthisto.Clone()
                    histos[label].SetDirectory(0)
                else:
                    histos[label].Add(currenthisto.Clone())
            

    for is_pixel_track, category in enumerate(["long", "short"]): 

        graphs = {}
        graph_list = ["tightSimple", "looseSimple", "loose2", "tight2", "loose3", "tight3", "bdtEDep10", "bdtEDep20", "test3", "test3b", "test4", "test5", "mt2"] #"exo" "tightBase", "looseBase",  , "test1", "test2", "test3", "test4", "test5"]
        
        print category
        
        canvas = shared_utils.mkcanvas()
        
        legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.65)
        
        for g_label in graph_list:
            graphs[g_label] = TGraph()
            graphStyler(graphs[g_label])
           
        for label in histos:
            if "Background" in label: continue
                                    
            sg_num = histos[label].GetBinContent(1 + is_pixel_track)
            sg_den = histos["Signal_nocuts_%s" % category].GetBinContent(1 + is_pixel_track)
            if sg_den > 0:
                eff_sg = 1.0 * sg_num / sg_den
            else:
                eff_sg = 0
                
            bg_num = histos[label.replace("Signal", "Background")].GetBinContent(1 + is_pixel_track)
            bg_den = histos["Background_nocuts_%s" % category].GetBinContent(1 + is_pixel_track)
            if bg_den > 0:
                eff_bg = 1.0 * bg_num / bg_den
            else:
                eff_bg = 0

            print label, eff_sg, 1 - eff_bg
                        
            if (category == "short" and "pixeltrack" in label) \
                or (category == "long" and "stripstrack" in label):
                
                for g_label in graph_list:
                    if g_label in label:
                        graphs[g_label].SetPoint(graphs[g_label].GetN(), eff_sg, 1 - eff_bg)
                    
        background = TH2F("bg", "bg", 10, 0.0, 1.0, 10, 0.9, 1.0)
        background.SetTitle(";#epsilon_{  sg};1 - #epsilon_{  bg}")
        shared_utils.histoStyler(background)
        background.Draw()
                
        graphs["tightSimple"].Sort()
        graphs["tightSimple"].SetLineWidth(2)
        graphs["tightSimple"].SetLineStyle(1)
        graphs["tightSimple"].SetLineColor(kRed-4)
        graphs["tightSimple"].SetTitle(";#epsilon_{  sg};1 - #epsilon_{  bg}")
        #graphs["tightSimple"].GetXaxis().SetRangeUser(0,1)
        #graphs["tightSimple"].GetXaxis().SetLimits(0,1)
        graphs["tightSimple"].SetFillColor(kWhite)
        graphs["tightSimple"].Draw("same")
        legend.AddEntry(graphs["tightSimple"], "fully informed BDT")

        graphs["looseSimple"].Sort()
        graphs["looseSimple"].SetLineWidth(2)
        graphs["looseSimple"].SetLineStyle(2)
        graphs["looseSimple"].SetLineColor(kRed-4)
        graphs["looseSimple"].Draw("same")
        graphs["looseSimple"].SetFillColor(kWhite)
        legend.AddEntry(graphs["looseSimple"], "d_{xy}-uninformed BDT")

        graphs["tight2"].Sort()
        graphs["tight2"].SetLineWidth(2)
        graphs["tight2"].SetLineStyle(1)
        graphs["tight2"].SetLineColor(kAzure-4)
        graphs["tight2"].Draw("same")
        graphs["tight2"].SetFillColor(kWhite)
        legend.AddEntry(graphs["tight2"], "fully informed BDT (adjusted)")
        
        graphs["loose2"].Sort()
        graphs["loose2"].SetLineWidth(2)
        graphs["loose2"].SetLineStyle(2)
        graphs["loose2"].SetLineColor(kAzure-3)
        graphs["loose2"].Draw("same")
        graphs["loose2"].SetFillColor(kWhite)
        legend.AddEntry(graphs["loose2"], "d_{xy}-uninformed BDT (adjusted)")

        #graphs["tight3"].Sort()
        #graphs["tight3"].SetLineWidth(2)
        #graphs["tight3"].SetLineStyle(1)
        #graphs["tight3"].SetLineColor(kOrange)
        #graphs["tight3"].Draw("same")
        #graphs["tight3"].SetFillColor(kWhite)
        #legend.AddEntry(graphs["tight3"], "fully informed BDT (3)")
        #
        #graphs["loose3"].Sort()
        #graphs["loose3"].SetLineWidth(2)
        #graphs["loose3"].SetLineStyle(2)
        #graphs["loose3"].SetLineColor(kOrange)
        #graphs["loose3"].Draw("same")
        #graphs["loose3"].SetFillColor(kWhite)
        #legend.AddEntry(graphs["loose3"], "d_{xy}-uninformed BDT (3)")

        graphs["bdtEDep10"].SetMarkerStyle(20)
        graphs["bdtEDep10"].SetMarkerColor(kGreen+2)
        graphs["bdtEDep10"].Draw("same p")
        graphs["bdtEDep10"].SetLineColor(kWhite)
        graphs["bdtEDep10"].SetFillColor(kWhite)
        legend.AddEntry(graphs["bdtEDep10"], "Full tag (E_{matched}^{calo}<10 GeV)")

        graphs["bdtEDep20"].SetMarkerStyle(22)
        graphs["bdtEDep20"].SetMarkerColor(kGreen+2)
        graphs["bdtEDep20"].Draw("same p")
        graphs["bdtEDep20"].SetLineColor(kWhite)
        graphs["bdtEDep20"].SetFillColor(kWhite)
        legend.AddEntry(graphs["bdtEDep20"], "Full tag (E_{matched}^{calo}<20 GeV)")

        #graphs["test1"].SetMarkerStyle(20)
        #graphs["test1"].SetMarkerColor(kGreen)
        #graphs["test1"].Draw("same p")
        #graphs["test1"].SetLineColor(kWhite)
        #graphs["test1"].SetFillColor(kWhite)
        #legend.AddEntry(graphs["test1"], "Test tag")
        
        #graphs["test2"].SetMarkerStyle(20)
        #graphs["test2"].SetMarkerColor(kGreen+2)
        #graphs["test2"].Draw("same p")
        #graphs["test2"].SetLineColor(kWhite)
        #graphs["test2"].SetFillColor(kWhite)
        #legend.AddEntry(graphs["test2"], "test 2")

        graphs["test3"].SetMarkerStyle(22)
        graphs["test3"].SetMarkerColor(kOrange+10)
        graphs["test3"].Draw("same p")
        graphs["test3"].SetLineColor(kWhite)
        graphs["test3"].SetFillColor(kWhite)
        legend.AddEntry(graphs["test3"], "Adjusted tag (MVA>0.1, E_{matched}^{calo}<15 GeV)")

        graphs["test3b"].SetMarkerStyle(23)
        graphs["test3b"].SetMarkerColor(kOrange+10)
        graphs["test3b"].Draw("same p")
        graphs["test3b"].SetLineColor(kWhite)
        graphs["test3b"].SetFillColor(kWhite)
        legend.AddEntry(graphs["test3b"], "Adjusted tag (MVA>0.1, E_{matched}^{calo}<20 GeV)")

        graphs["test5"].SetMarkerStyle(24)
        graphs["test5"].SetMarkerColor(kOrange+10)
        graphs["test5"].Draw("same p")
        graphs["test5"].SetLineColor(kWhite)
        graphs["test5"].SetFillColor(kWhite)
        legend.AddEntry(graphs["test5"], "Adjusted tag (MVA>-0.1, E_{matched}^{calo}<15 GeV)")


        #graphs["test4"].SetMarkerStyle(22)
        #graphs["test4"].SetMarkerColor(kMagenta)
        #graphs["test4"].Draw("same p")
        #graphs["test4"].SetLineColor(kWhite)
        #graphs["test4"].SetFillColor(kWhite)
        #legend.AddEntry(graphs["test4"], "test 4")
        #
        #graphs["test5"].SetMarkerStyle(23)
        #graphs["test5"].SetMarkerColor(kMagenta-1)
        #graphs["test5"].Draw("same p")
        #graphs["test5"].SetLineColor(kWhite)
        #graphs["test5"].SetFillColor(kWhite)
        #legend.AddEntry(graphs["test5"], "test 5")

        #graphs["exo"].SetMarkerStyle(20)
        #graphs["exo"].SetMarkerColor(kMagenta-3)
        #graphs["exo"].Draw("same p")
        #graphs["exo"].SetLineColor(kWhite)
        #graphs["exo"].SetFillColor(kWhite)
        #legend.AddEntry(graphs["exo"], "EXO-19-010 tag")

        graphs["mt2"].SetMarkerStyle(20)
        graphs["mt2"].SetMarkerColor(kCyan+1)
        graphs["mt2"].Draw("same p")
        graphs["mt2"].SetLineColor(kWhite)
        graphs["mt2"].SetFillColor(kWhite)
        legend.AddEntry(graphs["mt2"], "SUS-19-005 tag")
        
        if category == "short":
            legend.SetHeader("short tracks")
        else:
            legend.SetHeader("long tracks, #geq2 miss. outer hits")
                
        legend.Draw()
        
        shared_utils.stamp()
                
        if quick_mode:
            canvas.Print("roc_%s_tracks_quick.pdf" % category)
            canvas.Print("roc_%s_tracks_quick.root" % category)
        else:
            canvas.Print("roc_%s_tracks.pdf" % category)
            canvas.Print("roc_%s_tracks.root" % category)
            

if __name__ == "__main__":

    main(quick_mode = True)
    