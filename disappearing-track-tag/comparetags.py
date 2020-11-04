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


def roc_and_efficiencies(sg_filelist, bg_filelist, phase, batchname):
    
    mt2_short = " && ".join(cutflow.cuts["MT2_short"])
    mt2_long = " && ".join(cutflow.cuts["MT2_long"])
    exo_short = " && ".join(cutflow.cuts["EXO_short"])
    exo_long = " && ".join(cutflow.cuts["EXO_long"])
    exo_pt15_short = " && ".join(cutflow.cuts["EXO_pt15_short"])
    exo_pt15_long = " && ".join(cutflow.cuts["EXO_pt15_long"])
    exo_noeta_short = " && ".join(cutflow.cuts["EXO_noeta_short"])
    exo_noeta_long = " && ".join(cutflow.cuts["EXO_noeta_long"])
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
        lumi = 35000
        
    histos = collections.OrderedDict()
    drawoptions = collections.OrderedDict()
    # get histograms:

    def fill_histos(label, variable, shortcuts, longcuts):
                
        histos["bg_short_%s" % label] = plotting.get_all_histos(bg_filelist, "Events", variable, "tracks_is_pixel_track==1 && " + shortcuts, nBinsX=200, xmin=-1, xmax=1)
        histos["bg_long_%s" % label] =  plotting.get_all_histos(bg_filelist, "Events", variable, "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && " + longcuts, nBinsX=200, xmin=-1, xmax=1)
        histos["sg_short_%s" % label] = plotting.get_all_histos(sg_filelist, "Events", variable, "tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01 && " + shortcuts, nBinsX=200, xmin=-1, xmax=1)
        histos["sg_long_%s" % label] =  plotting.get_all_histos(sg_filelist, "Events", variable, "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01 && " + longcuts, nBinsX=200, xmin=-1, xmax=1)
    
    # get common denominator:
    fill_histos("denom", "tracks_mva_tight_may20_chi2", "tracks_pt>10", "tracks_pt>30")
    
    # get numerator, ROC curve scans:
    fill_histos("pt10", "tracks_mva_tight_may20_chi2_pt10", "tracks_pt>10 && " + bdt_short, "tracks_pt>30 && " + bdt_long)
    drawoptions["pt10"] = ["BDT (track p_{T}>10 GeV)", "same", kRed, 1, True, False]
    
    fill_histos("pt15", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && " + bdt_short, "tracks_pt>30 && " + bdt_long)
    drawoptions["pt15"] = ["BDT (track p_{T}>15 GeV)", "same", kOrange, 1, True, True]

    fill_histos("pt15_nojets", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && " + bdt_nojets_short, "tracks_pt>30 && " + bdt_nojets_long)
    drawoptions["pt15_nojets"] = ["BDT (track p_{T}>15 GeV, no jet veto)", "same", kOrange, 2, True, True]

    fill_histos("pt15_ratio12", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_short, "tracks_pt>30 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_long)
    drawoptions["pt15_ratio12"] = ["BDT (track p_{T}>15 GeV, EDep/p<0.12)", "same", kOrange, 3, True, True]

    fill_histos("pt15_ratio20", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_short, "tracks_pt>30 && tracks_matchedCaloEnergy/tracks_p<0.20 && " + bdt_long)
    drawoptions["pt15_ratio20"] = ["BDT (track p_{T}>15 GeV, EDep/p<0.20)", "same", kOrange, 4, True, True]

    fill_histos("pt15_ratio30", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_short, "tracks_pt>30 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_long)
    drawoptions["pt15_ratio30"] = ["BDT (track p_{T}>15 GeV, EDep/p<0.30)", "same", kOrange, 5, True, True]

    fill_histos("pt15_moreiso", "tracks_mva_tight_may20_chi2_pt15", "tracks_pt>15 && tracks_trkRelIso<0.1 && " + bdt_nojets_short, "tracks_pt>30 && tracks_trkRelIso<0.1 && " + bdt_nojets_long)
    drawoptions["pt15_moreiso"] = ["BDT (track p_{T}>15 GeV, relIso<0.1)", "same", kGreen-3, 1, True, True]

    fill_histos("pt30", "tracks_mva_tight_may20_chi2", "tracks_pt>30 && " + bdt_short, "tracks_pt>30 && " + bdt_long)
    drawoptions["pt30"] = ["BDT (track p_{T}>30 GeV)", "same", kPink+4, 1, True, False]

    # get numerator, working points:
    if phase == 0:
        fill_histos("wpA", "tracks_mva_tight_may20_chi2", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>0.13 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2_pt15>0.13 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_long) 
        fill_histos("wpB", "tracks_mva_tight_may20_chi2", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>-0.02 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2_pt15>0 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_long)        
    elif phase == 1:
        fill_histos("wpA", "tracks_mva_tight_may20_chi2", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>0 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2_pt15>0 && tracks_matchedCaloEnergy/tracks_p<0.12 && " + bdt_long)        
        fill_histos("wpB", "tracks_mva_tight_may20_chi2", "tracks_pt>15 && tracks_mva_tight_may20_chi2_pt15>-0.1 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_short, "tracks_pt>30 && tracks_mva_tight_may20_chi2_pt15>-0.14 && tracks_matchedCaloEnergy/tracks_p<0.30 && " + bdt_long)        
    drawoptions["wpA"] = ["working point A", "same p", kRed, 1, True, True]
    drawoptions["wpB"] = ["working point B", "same p", kMagenta, 1, True, True]
    
    fill_histos("mt2", "tracks_mva_tight_may20_chi2", mt2_short, mt2_long)
    drawoptions["mt2"] = ["SUS-19-005 tag", "same p", kTeal, 1, True, True]
    
    fill_histos("exo", "tracks_mva_tight_may20_chi2", exo_short, exo_long)
    drawoptions["exo"] = ["EXO-19-010 tag", "same p", kAzure, 1, True, True]
    
    fill_histos("exo_pt15", "tracks_mva_tight_may20_chi2", exo_pt15_short, exo_pt15_long)
    drawoptions["exo_pt15"] = ["EXO-19-010 tag (p_{T}>15 GeV)", "same p", kAzure+7, 1, True, True]
    
    fill_histos("exo_noeta", "tracks_mva_tight_may20_chi2", exo_noeta_short, exo_noeta_long)
    drawoptions["exo_noeta"] = ["EXO-19-010 tag (no #eta cuts)", "same p", kAzure+5, 1, True, True]

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

    efffile = "plots/roc_%s_phase%s.dat" % (batchname, phase)
    with open(efffile, "w+") as fout:
        for label in efficiencies:
            fout.write("Label: " + label + "\n**************\n")
            for item in efficiencies[label]:
                fout.write("%s, %s, %s\n" % (item[0], item[1], item[2]))
            fout.write("\n")

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
                histo = TH2F("empty", "empty", 1, 0, 1, 1, 0.99, 1)
            else:
                histo = TH2F("empty", "empty", 1, 0, 1, 1, 0.99, 1)
        
        shared_utils.histoStyler(histo)
        histo.Draw()
        histo.SetTitle(";#epsilon_{  sg};1 - #epsilon_{  bg}")
        
        if category == "short":
            legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.65)
        else: 
            legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.55)

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
                graphs_roc[label].SetMarkerStyle(20)
                graphs_roc[label].SetMarkerColor(drawoptions[optionslabel][2])
            else:
                graphs_roc[label].SetLineColor(drawoptions[optionslabel][2])
                graphs_roc[label].SetLineStyle(drawoptions[optionslabel][3])
                print label, optionslabel, drawoptions[optionslabel][3]
            graphs_roc[label].Draw(drawoptions[optionslabel][1])
            
            if category == "long":
                legendlabel = legendlabel.replace("p_{T}>15 GeV", "p_{T}>30 GeV")
        
            legend.AddEntry(graphs_roc[label], legendlabel)
                            
        #legend.SetTextSize(0.045)
        legend.SetTextSize(0.04)
        legend.SetHeader("Phase %s, %s tracks" % (phase, category))
        legend.Draw()
        shared_utils.stamp()
        
        canvas.Print("plots/roc_%s_%s_phase%s.pdf" % (batchname, category, phase))
        
        continue

        ####################                
        # plot significance:
        ####################
        
        #canvas = shared_utils.mkcanvas()
        #
        #if category == "short":
        #    histo = TH2F("empty", "empty", 1, -1, 1, 1, 0, 4)
        #else:
        #    histo = TH2F("empty", "empty", 1, -1, 1, 1, 0, 4)
        #
        #shared_utils.histoStyler(histo)
        #histo.Draw()
        #histo.SetTitle(";BDT response;efficiency, significance")
        #legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.45)
        #
        #first = True
        #for label in graphs_significance:
        #                
        #    if category not in label: continue
        #
        #    graphs_significance[label].Draw("same")
        #    graphStyler(graphs_significance[label])
        #    graphs_significance[label].SetLineColor(210)
        #
        #    graphs_sgeff[label].Draw("same")
        #    graphStyler(graphs_sgeff[label])
        #    graphs_sgeff[label].SetLineColor(kBlue)
        #
        #    graphs_bgeff[label].Draw("same")
        #    graphStyler(graphs_bgeff[label])
        #    graphs_bgeff[label].SetLineColor(kRed)
        #        
        #    legendlabel = label.replace("sg_", "").replace("short_", "short tracks ").replace("long_", "long tracks ").replace("p0", " (phase 0)").replace("p1", " (phase 1)")
        #
        #phase0 = graphs_significance["sg_short_p0"].Clone()
        ##phase1 = graphs_significance["sg_short_p1"].Clone()
        #phase0.SetLineColor(kBlack)
        ##phase1.SetLineColor(kBlack)
        #        
        #legend.AddEntry(graphs_sgeff["sg_short"], "signal efficiency #epsilon_{sg}")
        #legend.AddEntry(graphs_bgeff["sg_short"], "background efficiency #epsilon_{bg}")
        #
        #legend.AddEntry(graphs_significance["sg_short"], "#epsilon_{sg} / #sqrt{#epsilon_{sg} + #epsilon_{bg}}")
        #
        #legend.Draw()
        #shared_utils.stamp()
        #canvas.Print("plots/significance_%s_%s_phase%s.pdf" % (folder.split("/")[-1], category, phase))
       

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index", default = False)
    (options, args) = parser.parse_args()

    if not options.index:
        for i in range(1,10):
            os.system("./comparetags.py --index %s &" % i)

    os.system("mkdir -p plots")

    quick = False

    if not quick:
        signal_p0 = ["../ntupleanalyzer/skim_63_cutflow/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP*root"]
        background_p0 = ["../ntupleanalyzer/skim_63_cutflow/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM*root"]
        signal_p1 = ["../ntupleanalyzer/skim_63_cutflow/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8ext1-AOD_110000*root"]
        background_p1 = ["../ntupleanalyzer/skim_63_cutflow/RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8AOD_70000*root"]
    
    else:
        signal_p0 = ["../ntupleanalyzer/tools/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP*root"]
        background_p0 = ["../ntupleanalyzer/tools/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM*root"]
        signal_p1 = ["../ntupleanalyzer/tools/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8*root"]
        background_p1 = ["../ntupleanalyzer/tools/RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraph*root"]

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
    
    
