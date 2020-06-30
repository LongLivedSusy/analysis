#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import os
import collections
import shared_utils
import glob
import numpy
import math

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


def main(labels):

    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_21"
    
    cutstrings = {}
    
    SR_short = "tracks_basecuts==1 && tracks_is_pixel_track==1 && tracks_mva_loose>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
    SR_long = "tracks_basecuts==1 && tracks_is_pixel_track==0 && tracks_mva_loose>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"

    basecuts = "tracks_basecuts==1 && tracks_pass_reco_lepton==1 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_nValidPixelHits[iCand]>=3"
    #vetoes = "tracks_pass_reco_lepton==1 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_nValidPixelHits>=3"
    vetoes = "tracks_pass_reco_lepton==1 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_nValidPixelHits>=2"
    baseline = "abs(tracks_eta)<2.4 && !(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566) && tracks_ptErrOverPt2<10 && tracks_dxyVtx<0.1 && tracks_dzVtx<0.1 && tracks_trkRelIso<0.2 && tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2 && tracks_nMissingInnerHits==0 && tracks_chi2perNdof<2.88 && tracks_pixelLayersWithMeasurement>2 && tracks_nMissingMiddleHits==0"
    
    baseline_loose_long = [
        "abs(tracks_eta)<2.4",   
        #"!(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566)",                              
        "tracks_highpurity==1",  
        "tracks_ptErrOverPt2<10",
        "tracks_dzVtx<0.1",
        "tracks_trkRelIso<0.2",  
        "tracks_trackerLayersWithMeasurement>=2",
        "tracks_nValidTrackerHits>=2",           
        "tracks_nMissingInnerHits==0",                                                     
        "tracks_nValidPixelHits>=2",    
        "tracks_pass_reco_lepton==1",
        "tracks_passPFCandVeto==1",                                   
        ##"tracks_passpionveto==1",
        ##"tracks_passjetveto==1",
        ##"tracks_nMissingMiddleHits==0",
        ##"tracks_chi2perNdof<2.88",
        ##"tracks_pixelLayersWithMeasurement>=2",
        ##"tracks_passmask==1",
             ]
             
    baseline_loose_long = " && ".join(baseline_loose_long)

    baseline_loose_short = [
        "abs(tracks_eta)<2.4",   
        #"!(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566)",                              
        "tracks_highpurity==1",  
        "tracks_ptErrOverPt2<10",
        "tracks_dzVtx<0.1",      
        "tracks_trkRelIso<0.2",  
        "tracks_trackerLayersWithMeasurement>=2",
        "tracks_nValidTrackerHits>=2",           
        "tracks_nMissingInnerHits==0",                                                     
        "tracks_nValidPixelHits>=2",    
        "tracks_pass_reco_lepton==1",
        "tracks_passPFCandVeto==1",                                   
        ##"tracks_passpionveto==1",
        ##"tracks_passjetveto==1",
        ##"tracks_nMissingMiddleHits==0",
        ##"tracks_chi2perNdof<2.88",
        ##"tracks_pixelLayersWithMeasurement>=2",
        ##"tracks_passmask==1",
             ]
             
    baseline_loose_short = " && ".join(baseline_loose_short)

    #baseline_loose = baseline_loose)
    baseline_tight_long = baseline_loose_long + " && tracks_dxyVtx<0.1 "
    baseline_tight_short = baseline_loose_short + " && tracks_dxyVtx<0.1 "
    
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
    
    for i_score in numpy.arange(-1.0, 1.0, 0.1): 
        
        use_score = i_score
        if i_score == -1.0:
            use_score = -10
        elif i_score == 1.0:
            use_score = 10
        
        #cutstrings["pixeltrack_tightBase_%s" % i_score] = oldbaseline_short_tight + "  && tracks_basecuts==1 && tracks_mva_tight>=%s" % i_score
        #cutstrings["pixeltrack_looseBase_%s" % i_score] = oldbaseline_short_loose + " && tracks_basecuts==1 && tracks_mva_loose>=%s" % i_score
        #cutstrings["stripstrack_tightBase_%s" % i_score] = "tracks_nMissingOuterHits>=2 && tracks_mva_tight>=%s" % i_score
        #cutstrings["stripstrack_looseBase_%s" % i_score] = "tracks_nMissingOuterHits>=2 && tracks_mva_loose>=%s" % i_score
        #cutstrings["pixeltrack_tightSimple_%s" % i_score] = "tracks_mva_tight>=%s" % i_score
        #cutstrings["pixeltrack_looseSimple_%s" % i_score] = "tracks_mva_loose>=%s" % i_score
        ##cutstrings["pixeltrack_tight2_%s" % i_score] = baseline_tight + " && tracks_mva_tight_may20>=%s" % i_score
        ##cutstrings["pixeltrack_loose2_%s" % i_score] = baseline_loose + " && tracks_mva_loose_may20>=%s" % i_score
        ##cutstrings["pixeltrack_tight3_%s" % i_score] = baseline_tight + " && tracks_mva_tight_may20_chi2>=%s" % i_score
        ##cutstrings["pixeltrack_loose3_%s" % i_score] = baseline_loose + " && tracks_mva_loose_may20_chi2>=%s" % i_score
        #cutstrings["pixeltrack_tight2_%s" % i_score] = baseline_tight_short + " && tracks_mva_tight_may20>=%s" % i_score
        #cutstrings["pixeltrack_loose2_%s" % i_score] = baseline_loose_short + " && tracks_mva_loose_may20>=%s" % i_score
        #cutstrings["pixeltrack_tight3_%s" % i_score] = baseline_tight_short + " && tracks_mva_tight_may20_chi2>=%s" % i_score
        cutstrings["pixeltrack_loose3_%s" % i_score] = baseline_loose_short + " && tracks_mva_loose_may20_chi2>=%s" % use_score
        #cutstrings["stripstrack_tightSimple_%s" % i_score] = "tracks_nMissingOuterHits>=2 && tracks_mva_tight>=%s" % i_score
        #cutstrings["stripstrack_looseSimple_%s" % i_score] = "tracks_nMissingOuterHits>=2 && tracks_mva_loose>=%s" % i_score
        ##cutstrings["stripstrack_tight2_%s" % i_score] = baseline_tight + " && tracks_nMissingOuterHits>=2 && tracks_mva_tight_may20>=%s" % i_score
        ##cutstrings["stripstrack_loose2_%s" % i_score] = baseline_loose + " && tracks_nMissingOuterHits>=2 && tracks_mva_loose_may20>=%s" % i_score
        ##cutstrings["stripstrack_tight3_%s" % i_score] = baseline_tight + " && tracks_nMissingOuterHits>=2 && tracks_mva_tight_may20_chi2>=%s" % i_score
        ##cutstrings["stripstrack_loose3_%s" % i_score] = baseline_loose + " && tracks_nMissingOuterHits>=2 && tracks_mva_loose_may20_chi2>=%s" % i_score
        #cutstrings["stripstrack_tight2_%s" % i_score] = baseline_loose_long + " && tracks_nMissingOuterHits>=2 && tracks_mva_tight_may20>=%s" % i_score
        #cutstrings["stripstrack_loose2_%s" % i_score] = baseline_loose_long + " && tracks_nMissingOuterHits>=2 && tracks_mva_loose_may20>=%s" % i_score
        #cutstrings["stripstrack_tight3_%s" % i_score] = baseline_loose_long + " && tracks_nMissingOuterHits>=2 && tracks_mva_tight_may20_chi2>=%s" % i_score
        cutstrings["stripstrack_loose3_%s" % i_score] = baseline_loose_long + " && tracks_nMissingOuterHits>=2 && tracks_mva_loose_may20_chi2>=%s" % use_score

    #cutstrings["nocuts_short"]              = baseline_loose + " && tracks_is_pixel_track==1"
    #cutstrings["nocuts_long"]               = baseline_loose + " && tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2"
    cutstrings["nocuts_short"]              = "tracks_is_pixel_track==1"
    cutstrings["nocuts_long"]               = "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_bdtEDep10tag"]   = SR_short + " && tracks_matchedCaloEnergy<10"
    #cutstrings["stripstrack_bdtEDep10tag"]  = SR_long + " && tracks_matchedCaloEnergy<10 && tracks_nMissingOuterHits>=2 "
    cutstrings["pixeltrack_bdtEDep15tag"]   = SR_short + " && tracks_matchedCaloEnergy<15"
    cutstrings["stripstrack_bdtEDep15tag"]  = SR_long + " && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2 "
    #cutstrings["pixeltrack_bdtEDep20tag"]   = SR_short + " && tracks_matchedCaloEnergy<20"
    #cutstrings["stripstrack_bdtEDep20tag"]  = SR_long + " && tracks_matchedCaloEnergy<20 && tracks_nMissingOuterHits>=2 "
    #cutstrings["pixeltrack_exotag"]         = "tracks_passexotag==17"
    #cutstrings["stripstrack_exotag"]        = "tracks_passexotag==17 && tracks_nMissingOuterHits>=2"
    cutstrings["pixeltrack_mt2tag"]         = "tracks_passmt2tag==115"
    cutstrings["stripstrack_mt2tag"]        = "(tracks_passmt2tag==215 || tracks_passmt2tag==316) && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test1"]          = "tracks_basecuts==1 && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test1"]         = "tracks_basecuts==1 && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15"
    #cutstrings["pixeltrack_test2"]          = baseline + " && " + vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test2"]         = baseline + " && " + vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15"
    #cutstrings["pixeltrack_test3"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test3"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test3b"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<20"
    #cutstrings["stripstrack_test3b"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<20 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test4"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose>0 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test4"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose>0 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test5"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<10"
    #cutstrings["stripstrack_test5"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<10 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test5"]          = " tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test5"]         = " tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>0 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2 && tracks_trkRelIso<0.01"
    #cutstrings["pixeltrack_test6"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test6"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>0 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2 && tracks_trkRelIso<0.01"
    #cutstrings["pixeltrack_test7"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test7"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>0 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2 && tracks_trkRelIso<0.01"
    #cutstrings["pixeltrack_test8"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_trkRelIso<0.01"
    #cutstrings["stripstrack_test8"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2 && tracks_trkRelIso<0.01"
    #cutstrings["pixeltrack_test9"]          = " tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test9"]         = " tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2 && tracks_trkRelIso<0.01"
    #cutstrings["pixeltrack_test9"]           = "tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test9"]          = "tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test10"]          = "tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_trkRelIso<0.01"
    #cutstrings["stripstrack_test10"]         = "tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2 && tracks_trkRelIso<0.01"
    #cutstrings["pixeltrack_test11"]          = baseline_loose_short + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_trkRelIso<0.01"
    #cutstrings["stripstrack_test11"]         = baseline_loose_long + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2 && tracks_trkRelIso<0.01"
    #cutstrings["pixeltrack_test12"]          = baseline_loose_short + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    #cutstrings["stripstrack_test12"]         = baseline_loose_long + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test13"]          = baseline_loose_short + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<10"
    #cutstrings["stripstrack_test13"]         = baseline_loose_long + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<10 && tracks_nMissingOuterHits>=2"
    cutstrings["pixeltrack_test14"]          = baseline_loose_short + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    cutstrings["stripstrack_test14"]         = baseline_loose_long + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test15"]          = baseline_loose_short + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<20"
    #cutstrings["stripstrack_test15"]         = baseline_loose_long + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<20 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test7"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<20"
    #cutstrings["stripstrack_test7"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<20 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test8"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.3 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<40"
    #cutstrings["stripstrack_test8"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.3 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<40 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test9"]          = "tracks_pass_reco_lepton==1 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_nValidPixelHits>=3" + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>=-10"
    #cutstrings["stripstrack_test9"]         = "tracks_pass_reco_lepton==1 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_nValidPixelHits>=3" + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>=-10 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_test10"]          = vetoes + " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>=-10"
    #cutstrings["stripstrack_test10"]         = vetoes + " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>=-10 && tracks_nMissingOuterHits>=2"
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
                currenthisto = plotting.get_histogram_from_file(input_files, "Events", "tracks_is_pixel_track", cutstring, nBinsX=2, xmin=0, xmax=2, unweighted = False)
                if histos[label] == 0:
                    histos[label] = currenthisto.Clone()
                    histos[label].SetDirectory(0)
                else:
                    histos[label].Add(currenthisto.Clone())
            
            
    for is_pixel_track, category in enumerate(["long", "short"]): 

        graphs = {}
        efficiencies_sg = {}
        efficiencies_bg = {}
        significances1 = {}
        significances2 = {}
        significances3 = {}
        graph_list = collections.OrderedDict()
        
        #graph_list["tight2"] =      [1, kAzure-4, "fully informed BDT"]
        #graph_list["loose2"] =      [2, kAzure-4, "d_{xy}-uninformed BDT"]
        #graph_list["tight3"] =      [1, kRed-4, "fully informed BDT"]
        graph_list["loose3"] =      [2, kRed-4, "d_{xy}-uninformed BDT"]
        #graph_list["bdtEDep10"] =   [20, kGreen+2, "Full tag (E_{matched}^{calo}<10 GeV)"]
        graph_list["bdtEDep15"] =   [21, kGreen+2, "Full tag (E_{matched}^{calo}<15 GeV)"]
        #graph_list["bdtEDep20"] =   [22, kGreen+2, "Full tag (E_{matched}^{calo}<20 GeV)"]
        #graph_list["test13"] =       [20, kOrange+7, "Modified tag (E_{matched}^{calo}<10 GeV)"]
        graph_list["test14"] =       [21, kOrange+7, "Modified tag (E_{matched}^{calo}<15 GeV)"]
        #graph_list["test15"] =       [22, kOrange+7, "Modified tag (E_{matched}^{calo}<20 GeV)"]
        graph_list["mt2"] =         [20, kCyan+1, "SUS-19-005 tag"]
                      
        canvas = shared_utils.mkcanvas()
        
        legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.65)
                
        for g_label in graph_list.keys():
            graphs[g_label] = TGraph()
            graphStyler(graphs[g_label])

            significances1[g_label] = TH1D("significances1_" + g_label, "significances1_" + g_label, 20, -1, 1)
            graphStyler(significances1[g_label])

            significances2[g_label] = TH1D("significances2_" + g_label, "significances2_" + g_label, 20, -1, 1)
            graphStyler(significances2[g_label])

            significances3[g_label] = TH1D("significances3_" + g_label, "significances3_" + g_label, 20, -1, 1)
            graphStyler(significances3[g_label])
            
            efficiencies_sg[g_label] = TH1D("effsg_" + g_label, "effsg_" + g_label, 20, -1, 1)
            graphStyler(efficiencies_sg[g_label])

            efficiencies_bg[g_label] = TH1D("effbg_" + g_label, "effbg_" + g_label, 20, -1, 1)
            graphStyler(efficiencies_bg[g_label])
           
        for label in histos:
            if "Background" in label: continue
             
            if (category == "short" and "pixeltrack" in label) \
                or (category == "long" and "stripstrack" in label):
                             
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

                if eff_bg>1 or eff_sg>1:
                    print "eff_bg, eff_sg", eff_bg, eff_sg
                                
                for g_label in graph_list.keys():
                    if g_label in label:
                        
                        # save efficiency:
                        graphs[g_label].SetPoint(graphs[g_label].GetN(), eff_sg, 1 - eff_bg)
                    
                        # save significance:
                        if (bg_num)>0:
                            significance1 = sg_num / math.sqrt(sg_num + bg_num)
                            significance2 = sg_num / math.sqrt(bg_num + (0.2*bg_num)**2)
                            significance3 = sg_num / math.sqrt(bg_num + (0.8*bg_num)**2)
                        else:
                            significance1 = 0
                            significance2 = 0
                            significance3 = 0
                        
                        if len(label.split("_")) == 4:
                            score = float(label.split("_")[-1])
                            significances1[g_label].Fill(score, significance1)
                            significances2[g_label].Fill(score, significance2)
                            significances3[g_label].Fill(score, significance3)
                            efficiencies_sg[g_label].Fill(score, eff_sg)
                            efficiencies_bg[g_label].Fill(score, eff_bg)
                         
                    
        # print ROC curves:
        background = TH2F("bg", "bg", 10, 0.0, 1.0, 10, 0.9, 1.0)
        background.SetTitle(";#epsilon_{  sg};1 - #epsilon_{  bg}")
        shared_utils.histoStyler(background)
        background.Draw()
                        
        for graph in graph_list.keys():
            graphs[graph].Sort()
            graphs[graph].SetLineWidth(2)
            
            if graph_list[graph][0]<20:
                graphs[graph].SetLineStyle(graph_list[graph][0])
                graphs[graph].SetLineColor(graph_list[graph][1])
                graphs[graph].Draw("same")
                
            else:
                graphs[graph].SetMarkerStyle(graph_list[graph][0])
                graphs[graph].SetMarkerColor(graph_list[graph][1])
                graphs[graph].SetLineColor(kWhite)
                graphs[graph].Draw("same p")
            
            graphs[graph].SetFillColor(kWhite)
            legend.AddEntry(graphs[graph], graph_list[graph][2])
        
        if category == "short":
            legend.SetHeader("short tracks")
        else:
            legend.SetHeader("long tracks, #geq2 miss. outer hits")
                
        legend.Draw()        
        shared_utils.stamp()
        canvas.Print("roc_%s_tracks.pdf" % category)
        
        # print significances:
        for label in ["loose3"]:
        
            canvas.Clear()        
            background = TH2F("bg", "bg", 10, -1.0, 1.0, 10, 0.0, 1.0)
            background.SetTitle(";BDT score;#epsilon , norm. significance")
            shared_utils.histoStyler(background)
            background.Draw()
            
            significances1[label].SetLineWidth(2)
            significances1[label].SetLineStyle(1)
            significances1[label].SetLineColor(kMagenta)
            significances1[label].Draw("same hist")
            significances1[label].SetFillColor(kWhite)
            significances1[label].Scale(1.0/significances1[label].Integral(significances1[label].GetXaxis().FindBin(-1), significances1[label].GetXaxis().FindBin(1)))

            significances2[label].SetLineWidth(2)
            significances2[label].SetLineStyle(1)
            significances2[label].SetLineColor(kGreen-6)
            significances2[label].Draw("same hist")
            significances2[label].SetFillColor(kWhite)
            significances2[label].Scale(1.0/significances2[label].Integral(significances2[label].GetXaxis().FindBin(-1), significances2[label].GetXaxis().FindBin(1)))

            significances3[label].SetLineWidth(2)
            significances3[label].SetLineStyle(1)
            significances3[label].SetLineColor(kGreen+3)
            significances3[label].Draw("same hist")
            significances3[label].SetFillColor(kWhite)
            significances3[label].Scale(1.0/significances3[label].Integral(significances3[label].GetXaxis().FindBin(-1), significances3[label].GetXaxis().FindBin(1)))

            efficiencies_sg[label].SetLineColor(kBlue)
            efficiencies_sg[label].Draw("same hist")
            efficiencies_bg[label].SetLineColor(kRed)
            efficiencies_bg[label].Draw("same hist")
            
            legend2 = shared_utils.mklegend(x1=0.6, y1=0.73, x2=0.9, y2=0.9)
            legend2.AddEntry(efficiencies_sg[label], "#epsilon_{sg}")
            legend2.AddEntry(efficiencies_bg[label], "#epsilon_{bg}")
            legend2.AddEntry(significances1[label], "S/#sqrt{S+B}")
            legend2.AddEntry(significances2[label], "S/#sqrt{B+(0.2*B)^2}")
            legend2.AddEntry(significances3[label], "S/#sqrt{B+(0.8*B)^2}")
            legend2.Draw()
            
            shared_utils.stamp()
            
            canvas.Print("significances_%s_%s.pdf" % (label, category))
        

if __name__ == "__main__":

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
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1075_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1275_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1375_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1475_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                ]
                
    # speed things up
    
    labels["Background"] = [
        #"Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1AOD_120000-389A0510-B8BD-E611-8546-008CFAFBF0BA",
        "Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_120000-02067A2D-48BB-E611-BE1E-001E67E71C95",
                           ]
    labels["Signal"] = [
        "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-00D93B88-C0A7-E911-9163-001F29087EE8",
        "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-0270362B-FBA4-E911-AA6B-FA163E3F6D58",
        #"Summer16.g1800_chi1400_27_200970_step4_10AODSIM",
        #"Summer16.g1800_chi1400_27_200970_step4_30AODSIM",
        #"Summer16.g1800_chi1400_27_200970_step4_50AODSIM",
        #"Summer16.g1800_chi1400_27_200970_step4_100AODSIM",
                       ]        
    

    main(labels)
    