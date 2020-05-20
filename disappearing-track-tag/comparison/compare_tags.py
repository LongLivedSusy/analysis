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

    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_18"
        
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
            "Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_120000-02067A2D-48BB-E611-BE1E-001E67E71C95",
                               ]
        labels["Signal"] = [
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-00D93B88-C0A7-E911-9163-001F29087EE8",
                           ]
    else:
        raw_input("Note: for checking different cuts, better use quick mode. Continue?")
        
    
    cutstrings = {}

    tags = {}
    tags["SR_short"] = "tracks_basecuts && tracks_is_pixel_track==1 && tracks_mva_loose>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
    tags["SR_long"] = "tracks_basecuts && tracks_is_pixel_track==0 && tracks_mva_loose>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"
    
    for i_score in numpy.arange(-1,1,0.1): 
    #for i_score in numpy.arange(-0.2,0.2,0.1): 
        cutstrings["tight_%s" % i_score] = "tracks_mva_tight>=%s" % i_score
        cutstrings["loose_%s" % i_score] = "tracks_mva_loose>=%s" % i_score

    cutstrings["nocuts_short"]              = "tracks_is_pixel_track>=0"
    cutstrings["nocuts_long"]               = "tracks_is_pixel_track>=0 && tracks_nMissingOuterHits>=2"
    #cutstrings["pixeltrack_bdttag"]        = "tracks_SR_short>=1"
    #cutstrings["stripstrack_bdttag"]       = "tracks_SR_long>=1"
    cutstrings["pixeltrack_bdtEDep10tag"]   = "tracks_SR_short>=1 && tracks_matchedCaloEnergy<10"
    cutstrings["stripstrack_bdtEDep10tag"]  = "tracks_SR_long>=1 && tracks_matchedCaloEnergy<10"
    cutstrings["pixeltrack_bdtEDep20tag"]   = "tracks_SR_short>=1 && tracks_matchedCaloEnergy<20"
    cutstrings["stripstrack_bdtEDep20tag"]  = "tracks_SR_long>=1 && tracks_matchedCaloEnergy<20"
    cutstrings["pixeltrack_exotag"]         = "tracks_is_pixel_track==1 && tracks_passexotag>=18"
    cutstrings["stripstrack_exotag"]        = "tracks_is_pixel_track==0 && tracks_passexotag>=18"
    cutstrings["pixeltrack_mt2tag"]         = "tracks_passmt2tag==115"
    cutstrings["stripstrack_mt2tag"]        = "tracks_passmt2tag==215 || tracks_passmt2tag==316"
    cutstrings["pixeltrack_test"]           = "tracks_basecuts==1 && tracks_is_pixel_track==1 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.02 && tracks_matchedCaloEnergy<15"
    cutstrings["stripstrack_test"]          = "tracks_basecuts==1 && tracks_pass_reco_lepton==1 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15"
    cutstrings["stripstrack_test2"]         = "tracks_pass_reco_lepton==1 && tracks_passPFCandVeto==1 && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_is_pixel_track==0 && tracks_mva_loose>0.1 && tracks_dxyVtx<0.04 && tracks_matchedCaloEnergy<15"
    
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
                if len(input_files) == 0: continue
                print label, ":\n", ",".join(input_files), "\n"
                currenthisto = plotting.get_histogram_from_file(input_files, "Events", "tracks_is_pixel_track", cutstring, nBinsX=2, xmin=0, xmax=2)
                if histos[label] == 0:
                    histos[label] = currenthisto.Clone()
                    histos[label].SetDirectory(0)
                else:
                    histos[label].Add(currenthisto.Clone())
            
    graphs = {}
    graph_list = ["tight", "loose", "bdtEDep10", "bdtEDep20", "mt2", "exo", "test", "test2"]
    
    for is_pixel_track, category in enumerate(["long", "short"]): 
        
        print category
        
        canvas = shared_utils.mkcanvas()
        #canvas.SetLogx(True)
        #canvas.SetLogy(True)
        
        legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.5, y2=0.65)
        
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
              
            if "tight" in label:
                graphs["tight"].SetPoint(graphs["tight"].GetN(), eff_sg, 1 - eff_bg)
            if "loose" in label:
                graphs["loose"].SetPoint(graphs["loose"].GetN(), eff_sg, 1 - eff_bg)
            
            if (category == "short" and "pixeltrack" in label) \
                or (category == "long" and "stripstrack" in label):
                
                for g_label in graph_list:
                    if not "tight" in g_label and not "loose" in g_label:
                        if g_label in label:
                            graphs[g_label].SetPoint(graphs[g_label].GetN(), eff_sg, 1 - eff_bg)
                
                #if "bdttag" in label:
                #    g_bdt.SetPoint(g_bdt.GetN(), eff_sg, 1 - eff_bg)
                #elif "bdtEDep10" in label:
                #    g_bdtEDep10.SetPoint(g_bdtEDep10.GetN(), eff_sg, 1 - eff_bg)
                #elif "bdtEDep12" in label:
                #    g_bdtEDep12.SetPoint(g_bdtEDep12.GetN(), eff_sg, 1 - eff_bg)
                #elif "bdtEDep15" in label:
                #    g_bdtEDep15.SetPoint(g_bdtEDep15.GetN(), eff_sg, 1 - eff_bg)
                #elif "bdtEDep20" in label:
                #    graphs["bdtEDep20"].SetPoint(graphs["bdtEDep20"].GetN(), eff_sg, 1 - eff_bg)
                #elif "exotag" in label:
                #    graphs["exo"].SetPoint(graphs["exo"].GetN(), eff_sg, 1 - eff_bg)
                #elif "mt2tag" in label:
                #    graphs["mt2"].SetPoint(graphs["mt2"].GetN(), eff_sg, 1 - eff_bg)
    
        graphs["tight"].Sort()
        graphs["tight"].SetLineWidth(2)
        graphs["tight"].SetLineColor(kRed-4)
        graphs["tight"].SetTitle(";#epsilon_{  sg};1 - #epsilon_{  bg}")
        graphs["tight"].GetXaxis().SetRangeUser(0,1)
        graphs["tight"].GetXaxis().SetLimits(0,1)
        graphs["tight"].GetYaxis().SetRangeUser(0.95,1)
        graphs["tight"].GetYaxis().SetLimits(0.95,1)
        graphs["tight"].SetFillColor(kWhite)
        graphs["tight"].Draw("")
        legend.AddEntry(graphs["tight"], "d_{xy}-informed BDT")

        graphs["loose"].Sort()
        graphs["loose"].SetLineWidth(2)
        graphs["loose"].SetLineColor(kAzure-3)
        graphs["loose"].Draw("same")
        graphs["loose"].SetFillColor(kWhite)
        legend.AddEntry(graphs["loose"], "BDT")

        graphs["bdtEDep10"].SetMarkerStyle(20)
        graphs["bdtEDep10"].SetMarkerColor(kOrange)
        graphs["bdtEDep10"].Draw("same p")
        graphs["bdtEDep10"].SetLineColor(kWhite)
        graphs["bdtEDep10"].SetFillColor(kWhite)
        legend.AddEntry(graphs["bdtEDep10"], "Full tag (E_{matched}^{calo}<10 GeV)")

        #g_bdtEDep12.SetMarkerStyle(20)
        #g_bdtEDep12.SetMarkerColor(kOrange+1)
        #g_bdtEDep12.Draw("same p")
        #g_bdtEDep12.SetLineColor(kWhite)
        #g_bdtEDep12.SetFillColor(kWhite)
        #legend.AddEntry(g_bdtEDep12, "Full tag + EDep<12 GeV")
        #
        #g_bdtEDep15.SetMarkerStyle(20)
        #g_bdtEDep15.SetMarkerColor(kOrange+2)
        #g_bdtEDep15.Draw("same p")
        #g_bdtEDep15.SetLineColor(kWhite)
        #g_bdtEDep15.SetFillColor(kWhite)
        #legend.AddEntry(g_bdtEDep15, "Full tag + EDep<15 GeV")

        graphs["bdtEDep20"].SetMarkerStyle(20)
        graphs["bdtEDep20"].SetMarkerColor(kOrange+3)
        graphs["bdtEDep20"].Draw("same p")
        graphs["bdtEDep20"].SetLineColor(kWhite)
        graphs["bdtEDep20"].SetFillColor(kWhite)
        legend.AddEntry(graphs["bdtEDep20"], "Full tag (E_{matched}^{calo}<20 GeV)")

        graphs["test"].SetMarkerStyle(20)
        graphs["test"].SetMarkerColor(kGreen)
        graphs["test"].Draw("same p")
        graphs["test"].SetLineColor(kWhite)
        graphs["test"].SetFillColor(kWhite)
        legend.AddEntry(graphs["test"], "Full tag (changed)")
        
        if category == "long":
            graphs["test2"].SetMarkerStyle(20)
            graphs["test2"].SetMarkerColor(kGreen+2)
            graphs["test2"].Draw("same p")
            graphs["test2"].SetLineColor(kWhite)
            graphs["test2"].SetFillColor(kWhite)
            legend.AddEntry(graphs["test2"], "Full tag (changed, no baseline)")


        graphs["exo"].SetMarkerStyle(20)
        graphs["exo"].SetMarkerColor(kMagenta-3)
        graphs["exo"].Draw("same p")
        graphs["exo"].SetLineColor(kWhite)
        graphs["exo"].SetFillColor(kWhite)
        legend.AddEntry(graphs["exo"], "EXO-19-010 tag")

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
        canvas.Print(category + ".pdf")
        canvas.Print(category + ".root")
        

if __name__ == "__main__":

    main(quick_mode = False)
    