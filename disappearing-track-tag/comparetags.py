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
import cutflow
from optparse import OptionParser

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def graphStyler(h, color=kBlack):
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
    h.SetFillColor(kWhite)


def roc_and_efficiencies(sg_filelist, bg_filelist, phase, batchname, style = "A"):
    
    mt2_short = " && ".join(cutflow.cuts["MT2_short"])
    mt2_long = " && ".join(cutflow.cuts["MT2_long"])
    exo_short = " && ".join(cutflow.cuts["EXO_short"])
    exo_long = " && ".join(cutflow.cuts["EXO_long"])
    exo_pt15_short = " && ".join(cutflow.cuts["EXO_pt15_short"])
    exo_pt15_long = " && ".join(cutflow.cuts["EXO_pt15_long"])
    exo_noeta_short = " && ".join(cutflow.cuts["EXO_noeta_short"])
    exo_noeta_long = " && ".join(cutflow.cuts["EXO_noeta_long"])
    exo_noetapt_short = " && ".join(cutflow.cuts["EXO_noetapt_short"])
    exo_noetapt_long = " && ".join(cutflow.cuts["EXO_noetapt_long"])
    bdt_short = " && ".join(cutflow.cuts["BDT_short"][:-2])
    bdt_long = " && ".join(cutflow.cuts["BDT_long"][:-2])
    bdt_nojets_short = " && ".join(cutflow.cuts["BDT_noJetVeto_short"][:-2])
    bdt_nojets_long = " && ".join(cutflow.cuts["BDT_noJetVeto_long"][:-2])
    
    #FIXME phase 1 dE/dx
    if phase == 1:
        bdt_short = bdt_short.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        bdt_long = bdt_long.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        bdt_nojets_short = bdt_nojets_short.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        bdt_nojets_long = bdt_nojets_long.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        lumi = 137000
    else:
        bdt_short = bdt_short.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        bdt_long = bdt_long.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        bdt_nojets_short = bdt_nojets_short.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        bdt_nojets_long = bdt_nojets_long.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        lumi = 35000
        
    histos = collections.OrderedDict()
    drawoptions = collections.OrderedDict()
    # get histograms:

    def fill_histos(label, variable, shortcuts, longcuts):
        histos["bg_short_%s" % label] = plotting.get_all_histos(bg_filelist, "Events", variable, cutstring="tracks_is_pixel_track==1 && " + shortcuts, nBinsX=200, xmin=-1, xmax=1)
        histos["bg_long_%s" % label] =  plotting.get_all_histos(bg_filelist, "Events", variable, cutstring="tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && " + longcuts, nBinsX=200, xmin=-1, xmax=1)
        histos["sg_short_%s" % label] = plotting.get_all_histos(sg_filelist, "Events", variable, cutstring="tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01 && " + shortcuts, nBinsX=200, xmin=-1, xmax=1)
        histos["sg_long_%s" % label] =  plotting.get_all_histos(sg_filelist, "Events", variable, cutstring="tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01 && " + longcuts, nBinsX=200, xmin=-1, xmax=1)
    
    # get common denominator:
    #fill_histos("denom", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15", "tracks_pt>40")
    fill_histos("denom", "tracks_mva_nov20_noEdep", "tracks_pt>15", "tracks_pt>40")
    
    #fill_histos("denom", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>30 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)
    
    # get numerator, ROC curve scans:
    #fill_histos("pt10", "tracks_mva_tight_may20_chi2_pt10", "tracks_pt>10 && " + bdt_short, "tracks_pt>30 && " + bdt_long)
    #drawoptions["pt10"] = ["BDT (track p_{T}>10 GeV)", "same", kRed, 1, True, False]
    
    #fill_histos("noBLpt15", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && " + bdt_short.replace("tracks_passleptonveto==1", "MHT>=0"), "tracks_pt>30 && " + bdt_long.replace("tracks_passleptonveto==1", "MHT>=0"))
    #drawoptions["noBLpt15"] = ["BDT (track p_{T}>15 GeV, no leptonveto)", "same", kYellow, 1, True, True]
    #
    #fill_histos("noBLpt15b", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && " + bdt_short.replace("tracks_passpionveto==1", "MHT>=0"), "tracks_pt>30 && " + bdt_long.replace("tracks_passpionveto==1", "MHT>=0"))
    #drawoptions["noBLpt15b"] = ["BDT (track p_{T}>15 GeV, no pionveto)", "same", kYellow+1, 1, True, True]
    #
    #fill_histos("noBLpt15c", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && " + bdt_short.replace("tracks_passjetveto==1", "MHT>=0"), "tracks_pt>30 && " + bdt_long.replace("tracks_passjetveto==1", "MHT>=0"))
    #drawoptions["noBLpt15c"] = ["BDT (track p_{T}>15 GeV, no jetveto)", "same", kYellow+2, 1, True, True]
    #
    #fill_histos("noBLpt15d", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && " + bdt_short.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0"), "tracks_pt>30 && " + bdt_long.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0"))
    #drawoptions["noBLpt15d"] = ["BDT (track p_{T}>15 GeV, no dedx)", "same", kYellow+3, 1, True, True]
    

    if style == "A":

        fill_histos("pt15noEdep", "tracks_mva_nov20_noEdep", "tracks_pt>25 && " + bdt_short, "tracks_pt>40 && " + bdt_long)
        drawoptions["pt15noEdep"] = ["BDT (track p_{T}>25 GeV)", "same", kOrange, 1, True, False]
        
        fill_histos("pt30noEdep", "tracks_mva_nov20_noEdep", "tracks_pt>40 && " + bdt_short, "tracks_pt>40 && " + bdt_long)
        drawoptions["pt30noEdep"] = ["BDT (track p_{T}>40 GeV)", "same", kOrange, 1, False, True]
        
        #fill_histos("pt30noEdepNoJetVeto", "tracks_mva_nov20_noEdep", "tracks_pt>25 && " + bdt_short.replace("tracks_passjetveto==1 &&", " "), "tracks_pt>40 && " + bdt_long.replace("tracks_passjetveto==1 &&", " "))
        #drawoptions["pt30noEdepNoJetVeto"] = ["BDT (track p_{T}>40 GeV, no jet veto)", "same", kOrange, 2, False, True]

        fill_histos("pt15_ratio12", "tracks_mva_nov20_noEdep", "tracks_pt>25 && tracks_matchedCaloEnergy<20 && tracks_matchedCaloEnergy/tracks_p<0.2 && " + bdt_short, "tracks_pt>40 && tracks_matchedCaloEnergy/tracks_p<0.2 && " + bdt_long)
        drawoptions["pt15_ratio12"] = ["BDT (track p_{T}>25 GeV, with cut on E_{dep}/p)", "same", kRed, 1, True, True]

    if style == "B":
    
        #fill_histos("pt15", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && " + bdt_short, "tracks_pt>40 && " + bdt_long)
        #drawoptions["pt15"] = ["BDT (track p_{T}>15 GeV), trained with E_{dep}", "same", kOrange, 1, True, True]
    
        fill_histos("pt15noEdep", "tracks_mva_nov20_noEdep", "tracks_pt>25 && " + bdt_short, "tracks_pt>40 && " + bdt_long)
        drawoptions["pt15noEdep"] = ["BDT (track p_{T}>25 GeV)", "same", kOrange, 1, True, True]

        fill_histos("pt15_ratio12", "tracks_mva_nov20_noEdep", "tracks_pt>25 && tracks_matchedCaloEnergy<20 && tracks_matchedCaloEnergy/tracks_p<0.2 && " + bdt_short, "tracks_pt>40 && tracks_matchedCaloEnergy<20 && tracks_matchedCaloEnergy/tracks_p<0.2 && " + bdt_long)
        drawoptions["pt15_ratio12"] = ["BDT (track p_{T}>25 GeV, E_{Dep}<20 GeV, E_{Dep}<0.2*p)", "same", kRed, 1, True, True]

    #fill_histos("noBLpt15c", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && " + bdt_short.replace("tracks_passjetveto==1", "MHT>=0"), "tracks_pt>30 && " + bdt_long.replace("tracks_passjetveto==1", "MHT>=0"))
    #drawoptions["noBLpt15c"] = ["BDT (track p_{T}>15 GeV, no jet veto)", "same", kOrange, 2, True, True]

    #fill_histos("pt30", "tracks_mva_tight_may20_chi2", "tracks_pt>30 && " + bdt_short, "tracks_pt>30 && " + bdt_long)
    #drawoptions["pt30"] = ["BDT (track p_{T}>30 GeV)", "same", kOrange, 2, True, False]
    
    #fill_histos("pt15_nojets", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && " + bdt_nojets_short, "tracks_pt>30 && " + bdt_nojets_long)
    #drawoptions["pt15_nojets"] = ["BDT (track p_{T}>15 GeV, no jet veto)", "same", kOrange, 2, True, True]
    
    #fill_histos("pt15_ratio12", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_short, "tracks_pt>30 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_long)
    #drawoptions["pt15_ratio12"] = ["BDT (track p_{T}>15 GeV, EDep/p<0.12)", "same", kOrange, 3, True, True]
    
    #fill_histos("pt15_ratio20", "tracks_mva_nov20_noEdep", "tracks_pt>15 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>40 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)
    #drawoptions["pt15_ratio20"] = ["BDT (track p_{T}>15 GeV, not tr. on E_{dep}, E_{Dep}/p<20%)", "same", kRed, 1, True, True]

    
    #fill_histos("pt15_ratio30", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_short, "tracks_pt>30 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_long)
    #drawoptions["pt15_ratio30"] = ["BDT (track p_{T}>15 GeV, EDep/p<0.30)", "same", kOrange, 5, True, True]
    
    #fill_histos("pt15_moreiso", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_trkRelIso<0.1 && " + bdt_short, "tracks_pt>30 && tracks_trkRelIso<0.1 && " + bdt_long)
    #drawoptions["pt15_moreiso"] = ["BDT (track p_{T}>15 GeV, relIso<0.1)", "same", kGreen-3, 1, True, True]
    
    #fill_histos("pt30", "tracks_mva_tight_may20_chi2", "tracks_pt>30 && " + bdt_short, "tracks_pt>30 && " + bdt_long)
    #drawoptions["pt30"] = ["BDT (track p_{T}>30 GeV)", "same", kPink+4, 1, True, False]
    
    # get numerator, working points:
    if phase == 0:
        #fill_histos("wpA", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>30 && tracks_mva_tight_may20_chi2>0.13 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2>0.13 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_long) 
        fill_histos("wpA", "tracks_mva_nov20_noEdep", "tracks_pt>25 && tracks_mva_nov20_noEdep>0.1 && tracks_matchedCaloEnergy<20 && tracks_matchedCaloEnergy/tracks_p<0.2 && " + bdt_short, "tracks_pt>40 && tracks_mva_nov20_noEdep>0.1 && tracks_matchedCaloEnergy<20 && tracks_matchedCaloEnergy/tracks_p<0.2 && " + bdt_long) 
        #fill_histos("wpB", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>-0.02 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2_pt15>0 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)        
        #fill_histos("wpC", "tracks_mva_nov20_noEdep", "tracks_pt>15 && tracks_mva_nov20_noEdep>0 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>40 && tracks_mva_nov20_noEdep>0.05 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)        
        #fill_histos("wpB_pt150", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>-0.02 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>150 && tracks_mva_tight_may20_chi2_pt15>0 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)        
        #fill_histos("wpB", "tracks_mva_tight_may20_chi2", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>0.05 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2_pt15>0.1 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_long)        
    elif phase == 1:
        #fill_histos("wpA", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>30 && tracks_mva_tight_may20_chi2>0 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2>0 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_long)        
        fill_histos("wpA", "tracks_mva_nov20_noEdep", "tracks_pt>25 && tracks_mva_nov20_noEdep>0.12 && tracks_matchedCaloEnergy<20 && tracks_matchedCaloEnergy/tracks_p<0.2 && " + bdt_short, "tracks_pt>40 && tracks_mva_nov20_noEdep>0.15 && tracks_matchedCaloEnergy<20 && tracks_matchedCaloEnergy/tracks_p<0.2 && " + bdt_long)        
        #fill_histos("wpB", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>-0.1 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2_pt15>-0.14 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)        
        #fill_histos("wpC", "tracks_mva_nov20_noEdep", "tracks_pt>15 && tracks_mva_nov20_noEdep>-0.1 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>40 && tracks_mva_nov20_noEdep>0 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)        
        #fill_histos("wpB_pt150", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>-0.1 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>150 && tracks_mva_tight_may20_chi2_pt15>-0.14 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)        
        #fill_histos("wpB", "tracks_mva_tight_may20_chi2", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>0.1 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2_pt15>0.1 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_long)        
    drawoptions["wpA"] = ["working point", "same p", kRed, 21, True, True]
    #drawoptions["wpA2"] = ["working point A, pT>15", "same p", kRed, 22, True, False]
    #drawoptions["wpB"] = ["working point B", "same p", kMagenta, 20, True, True]
    #drawoptions["wpC"] = ["working point (loose)", "same p", kRed, 20, True, True]
    
    if style == "A":
        fill_histos("mt2", "tracks_mva_tight_may20_chi2_pt15", mt2_short, mt2_long)
        drawoptions["mt2"] = ["SUS-19-005 tag", "same p", kTeal, 20, True, True]

        #fill_histos("mt2_pt150", "tracks_mva_tight_may20_chi2_pt15", mt2_short, mt2_long + " && tracks_pt>150")
        #drawoptions["mt2_pt150"] = ["SUS-19-005 tag (track p_{T}>150 GeV)", "same p", kTeal, 22, False, True]
        
        fill_histos("exo", "tracks_mva_tight_may20_chi2_pt15", exo_short, exo_long)
        drawoptions["exo"] = ["EXO-19-010 tag", "same p", kAzure, 20, True, True]
        
        #fill_histos("exo_pt15", "tracks_mva_tight_may20_chi2", exo_pt15_short, exo_pt15_long)
        #drawoptions["exo_pt15"] = ["EXO-19-010 tag (p_{T}>15 GeV)", "same p", kAzure+7, 20, True, True]
        
        fill_histos("exo_noeta", "tracks_mva_tight_may20_chi2_pt15", exo_noeta_short, exo_noeta_long)
        drawoptions["exo_noeta"] = ["EXO-19-010 tag (no #eta cuts)", "same p", kAzure+5, 20, True, True]
        
        fill_histos("exo_noetapt", "tracks_mva_tight_may20_chi2_pt15", exo_noetapt_short, exo_noetapt_long)
        drawoptions["exo_noetapt"] = ["EXO-19-010 tag (no p_{T} and #eta cuts)", "same p", kAzure+5, 21, True, True]

    # scale with lumi
    for label in histos:
        shared_utils.histoStyler(histos[label])
        histos[label].Scale(lumi)
        
    # get efficiencies:
    efficiencies = {}
    for label in histos:
        
        if "denom" in label: continue
        
        efficiencies[label] = []
        
        denom_label = label.split("_")[0] + "_" + label.split("_")[1] + "_denom"
        denominator = histos[denom_label].Integral()

        if "mt2" in label or "exo" in label or "wp" in label:
            numerator = histos[label].Integral()
            if denominator > 0:
                efficiencies[label].append([0, numerator/denominator, numerator])
            else:
                efficiencies[label].append([0, 0, numerator])
        else:
            for i_score in numpy.arange(-1.0, 1.0, 0.005):
                numerator = histos[label].Integral(histos[label].GetXaxis().FindBin(i_score), histos[label].GetXaxis().FindBin(1))
                if denominator > 0:
                    efficiencies[label].append([i_score, numerator/denominator, numerator])
                else:
                    efficiencies[label].append([i_score, 0, numerator])

    #efffile = "plots/roc_%s_phase%s.dat" % (batchname, phase)
    #with open(efffile, "w+") as fout:
    #    for label in efficiencies:
    #        fout.write("Label: " + label + "\n**************\n")
    #        for item in efficiencies[label]:
    #            fout.write("%s, %s, %s\n" % (item[0], item[1], item[2]))
    #        fout.write("\n")

    # build TGraphs
    graphs_roc = {}
    graphs_sgeff = {}
    graphs_bgeff = {}
    graphs_significance = {}
    for label in efficiencies:

        if "bg" in label: continue
        graphs_roc[label] = TGraph()
        graphs_sgeff[label] = TGraph()
        graphs_bgeff[label] = TGraph()
        graphs_significance[label] = TGraph()
        
        for i in range(len(efficiencies[label])):
            score = efficiencies[label][i][0]
            eff_sg = efficiencies[label][i][1]
            eff_bg = efficiencies[label.replace("sg", "bg")][i][1]
            N_sg = efficiencies[label][i][2]
            N_bg = efficiencies[label.replace("sg", "bg")][i][2]
            graphs_roc[label].SetPoint(graphs_roc[label].GetN(), eff_sg, 1 - eff_bg)
            graphs_sgeff[label].SetPoint(graphs_sgeff[label].GetN(), score, eff_sg)
            graphs_bgeff[label].SetPoint(graphs_bgeff[label].GetN(), score, eff_bg)
            
            try:            
                significance = N_sg / math.sqrt(N_sg+N_bg)
                #significance = N_sg / math.sqrt( N_bg + (0.1*N_bg)**2 )
            except:
                significance = 0

            graphs_significance[label].SetPoint(graphs_significance[label].GetN(), score, significance)

    for category in ["short", "long"]:

        # plot ROC curves:
        ##################
        
        canvas = shared_utils.mkcanvas()
        
        if category == "short":
            if phase == 0:
                histo = TH2F("empty", "empty", 1, 0, 1, 1, 0.9, 1)
            else:
                histo = TH2F("empty", "empty", 1, 0, 1, 1, 0.98, 1)
        else:
            if phase == 0:
                histo = TH2F("empty", "empty", 1, 0, 1, 1, 0.97, 1)
            else:
                histo = TH2F("empty", "empty", 1, 0, 1, 1, 0.97, 1)
                
        shared_utils.histoStyler(histo)
        histo.Draw()
        histo.SetTitle(";#epsilon_{  sg};1 - #epsilon_{  bg}")
        
        if category == "short":
            legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.6)
        else: 
            legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.6)

        for label in sorted(graphs_roc):
                        
            if category not in label:
                continue
                
            graphStyler(graphs_roc[label])
            
            # e.g. drawoptions["pt30"] = ["BDT (track p_{T}>30 GeV)", "same", kPink+4, 1, True, True]
            
            optionslabel = "_".join(label.split("_")[2:])
            
            if category == "short" and not drawoptions[optionslabel][4]:
                continue
            if category == "long" and not drawoptions[optionslabel][5]:
                continue
            
            legendlabel = drawoptions[optionslabel][0]
            if drawoptions[optionslabel][1] == "same p":
                graphs_roc[label].SetLineColor(kWhite)
                graphs_roc[label].SetMarkerStyle(drawoptions[optionslabel][3])
                graphs_roc[label].SetMarkerColor(drawoptions[optionslabel][2])
            else:
                graphs_roc[label].SetLineColor(drawoptions[optionslabel][2])
                graphs_roc[label].SetLineStyle(drawoptions[optionslabel][3])
                print label, optionslabel, drawoptions[optionslabel][3]
            graphs_roc[label].Draw(drawoptions[optionslabel][1])
            
            if category == "long":
                legendlabel = legendlabel.replace("p_{T}>15 GeV", "p_{T}>40 GeV")
                legendlabel = legendlabel.replace("p_{T}>25 GeV", "p_{T}>40 GeV")
        
            legend.AddEntry(graphs_roc[label], legendlabel)
                            
        #legend.SetTextSize(0.045)
        legend.SetTextSize(0.035)
        legend.SetHeader("Phase %s, %s tracks" % (phase, category))
        legend.Draw()
        #shared_utils.stamp()
        
        pdfname = "plots/roc_%s_%s_phase%s_noedep_sep21v2_baseline.pdf" % (batchname, category, phase)
        
        if style == "A":
            pdfname = pdfname.replace(".pdf", "_styleA.pdf")
        
        canvas.Print(pdfname)
        

def significances(sg_filelist, bg_filelist, phase, batchname, signalcut = ""):
    
    bdt_short = " && ".join(cutflow.cuts["BDT_short"][:-2])
    bdt_long = " && ".join(cutflow.cuts["BDT_long"][:-2])
        
    #FIXME phase 1 dE/dx
    if phase == 1:
        bdt_short = bdt_short.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        bdt_long = bdt_long.replace("tracks_deDxHarmonic2pixel>2.0", "MHT>=0")
        lumi = 137000
    else:
        lumi = 35000
        
    histos = collections.OrderedDict()
    drawoptions = collections.OrderedDict()
    # get histograms:

    def fill_histos(label, variable, shortcuts, longcuts):
        histos["bg_short_%s" % label] = plotting.get_all_histos(bg_filelist, "Events", variable, cutstring="tracks_is_pixel_track==1 && " + shortcuts, nBinsX=200, xmin=-1, xmax=1)
        histos["bg_long_%s" % label] =  plotting.get_all_histos(bg_filelist, "Events", variable, cutstring="tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && " + longcuts, nBinsX=200, xmin=-1, xmax=1)
        histos["sg_short_%s" % label] = plotting.get_all_histos(sg_filelist, "Events", variable, cutstring="tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01 && " + shortcuts + signalcut, nBinsX=200, xmin=-1, xmax=1)
        histos["sg_long_%s" % label] =  plotting.get_all_histos(sg_filelist, "Events", variable, cutstring="tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01 && " + longcuts + signalcut, nBinsX=200, xmin=-1, xmax=1)
    
    # get common denominator:
    fill_histos("study", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>40 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)
    fill_histos("denom", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15", "tracks_pt>40")

    # scale with lumi
    for label in histos:
        shared_utils.histoStyler(histos[label])
        histos[label].Scale(lumi)
        
    # get efficiencies:
    efficiencies = {}
    
    for label in histos:
                
        if "denom" in label: continue
                
        efficiencies[label] = []
        
        #denominator = histos[label.replace("study", "denom")].Integral(histos[label].GetXaxis().FindBin(-1), histos[label].GetXaxis().FindBin(1))
        denominator = histos[label.replace("study", "denom")].Integral()
        #denominator = histos[label].Integral(histos[label].GetXaxis().FindBin(-1), histos[label].GetXaxis().FindBin(1))
        
        for i_score in numpy.arange(-1.0, 1.0, 0.005):
            numerator = histos[label].Integral(histos[label].GetXaxis().FindBin(i_score), histos[label].GetXaxis().FindBin(1))
            if denominator > 0:
                efficiencies[label].append([i_score, numerator/denominator, numerator])
            else:
                efficiencies[label].append([i_score, 0, numerator])

    # build TGraphs
    graphs_roc = {}
    graphs_sgeff = {}
    graphs_bgeff = {}
    graphs_significance = {}
    scalingfactor = 1.0
    signlabel = ""
    
    for label in efficiencies:

        if "bg" in label: continue
        graphs_roc[label] = TGraph()
        graphs_sgeff[label] = TGraph()
        graphs_bgeff[label] = TGraph()
        graphs_significance[label] = TGraph()
        
        for i in range(len(efficiencies[label])):
            score = efficiencies[label][i][0]
            eff_sg = efficiencies[label][i][1]
            eff_bg = efficiencies[label.replace("sg", "bg")][i][1]
            N_sg = efficiencies[label][i][2]
            N_bg = efficiencies[label.replace("sg", "bg")][i][2]
            graphs_roc[label].SetPoint(graphs_roc[label].GetN(), eff_sg, 1 - eff_bg)
            graphs_sgeff[label].SetPoint(graphs_sgeff[label].GetN(), score, eff_sg)
            graphs_bgeff[label].SetPoint(graphs_bgeff[label].GetN(), score, eff_bg)
            
            try:            
                #N = 1000
                #significance = N * eff_sg / math.sqrt(N*eff_sg+N*eff_bg)
                #signlabel = "#epsilon_{sg} / #sqrt{#epsilon_{sg} + #epsilon_{bg}}"
                #significance = 5e4 * N_sg / math.sqrt(5e4*N_sg + N_bg)
                significance = N_sg / math.sqrt(N_sg + N_bg)
                signlabel = "significance = N_{sg} / #sqrt{N_{sg} + N_{bg}}"
                #significance = 1e3 * N_sg / math.sqrt( N_bg + (0.2*N_bg)**2 )
                #signlabel = "significance = 1e3 * N_{sg} / #sqrt{N_{bg} + (0.2*N_{bg})^{2}}"
            except:
                significance = 0
            
            #scalingfactor = 1.0/1000
            #scalingfactor = 1.0/100
            graphs_significance[label].SetPoint(graphs_significance[label].GetN(), score, significance)

    for category in ["short", "long"]:

        # plot significances:
        #####################
        
        canvas = shared_utils.mkcanvas()
        
        if category == "short":
            histo = TH2F("empty", "empty", 1, -1, 1, 1, 0, 1)
        else:
            histo = TH2F("empty", "empty", 1, -1, 1, 1, 0, 1)
        
        shared_utils.histoStyler(histo)
        histo.Draw()
        histo.SetTitle(";BDT response;efficiency, significance")
        legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.45)
        
        first = True
        for label in graphs_significance:
                        
            if category not in label: continue
        
            graphs_significance[label].Draw("same")
            graphStyler(graphs_significance[label])
            graphs_significance[label].SetLineColor(210)
        
            graphs_sgeff[label].Draw("same")
            graphStyler(graphs_sgeff[label])
            graphs_sgeff[label].SetLineColor(kBlue)
            graphs_sgeff[label].SetFillColor(0)
        
            graphs_bgeff[label].Draw("same")
            graphStyler(graphs_bgeff[label])
            graphs_bgeff[label].SetLineColor(kRed)
            graphs_bgeff[label].SetFillColor(0)
                
            legendlabel = label.replace("sg_", "").replace("short_", "short tracks ").replace("long_", "long tracks ").replace("p0", " (phase 0)").replace("p1", " (phase 1)")
         
        legend.SetHeader("Phase %s, %s tracks" % (phase, category))
        legend.AddEntry(graphs_sgeff["sg_short_study"], "signal efficiency #epsilon_{sg}")
        legend.AddEntry(graphs_bgeff["sg_short_study"], "background efficiency #epsilon_{bg}")
        
        legend.AddEntry(graphs_significance["sg_short_study"], signlabel)
        
        legend.Draw()
        shared_utils.stamp()
        canvas.Print("plots/significance_%s_%s_phase%s_completestats.pdf" % (batchname, category, phase))
        canvas.Print("plots/significance_%s_%s_phase%s_completestats.root" % (batchname, category, phase))



if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index", default = False)
    (options, args) = parser.parse_args()

    if not options.index:
        os.system("./comparetags.py --index 1 &")
        os.system("./comparetags.py --index 2 &")

    os.system("mkdir -p plots")
    
    skim = "skim_67_newmask"
    #skim = "skim_108_cutflow"

    signal_p0 = ["../ntupleanalyzer/%s/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP*root" % skim]
    background_p0 = ["../ntupleanalyzer/%s/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM*root" % skim]
    signal_p1 = ["../ntupleanalyzer/%s/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8-AOD_110001-F48D076B-623B-E911-8432-FA163E754652_skim*root" % skim]
    background_p1 = ["../ntupleanalyzer/%s/RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8AOD_70000*root" % skim]
    
    if options.index == "1":
        roc_and_efficiencies(signal_p0, background_p0, 0, signal_p0[0].split("/")[2])
    elif options.index == "2":
        roc_and_efficiencies(signal_p1, background_p1, 1, signal_p1[0].split("/")[2])      
    elif options.index == "3":
        cutflow.plot_cutflow(signal_p0, "Signal phase 0", True, "sg_p0")
    elif options.index == "4":
        cutflow.plot_cutflow(signal_p1, "Signal phase 1", True, "sg_p1")
    elif options.index == "5":
        cutflow.plot_cutflow(background_p0, "WJets phase 0", False, "bg_p0")
    elif options.index == "6":
        cutflow.plot_cutflow(background_p1, "WJets phase 1", False, "bg_p1")
    elif options.index == "7":
        
        background_p0 = [
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.WJetsToLNu_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.DYJetsToLL_M-50_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.QCD_HT200to300_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.QCD_HT300to500_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.QCD_HT500to700_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.QCD_HT700to1000_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.QCD_HT1000to1500_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.QCD_HT1500to2000_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.QCD_HT2000toInf_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.TTJets_DiLept*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.TTJets_SingleLeptFromT*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.TTJets_SingleLeptFromTbar*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.ZZ_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.WW_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.WZ_TuneCUETP8M1*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.ZJetsToNuNu_HT-100To200_13TeV*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.ZJetsToNuNu_HT-200To400_13TeV*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.ZJetsToNuNu_HT-400To600_13TeV*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.ZJetsToNuNu_HT-600To800_13TeV*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.ZJetsToNuNu_HT-800To1200_13TeV*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.ZJetsToNuNu_HT-1200To2500_13TeV*",
                    "../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV*",
                    ]
        signal_p0 = ["../ntupleanalyzer/skim_65_p15OptionalJetVetoRevisedJets_merged/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq*"]
        
        significances(signal_p0, background_p0, 0, signal_p0[0].split("/")[2], signalcut = " && signal_gluino_mass==2000 && signal_lsp_mass==1975")
        
    elif options.index == "8":
        significances(signal_p1, background_p1, 1, signal_p1[0].split("/")[2])
    
    
    
