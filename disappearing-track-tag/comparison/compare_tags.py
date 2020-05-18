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


def main():

    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_15_merged"
        
    labels = collections.OrderedDict()

    labels["Background"] = [
            #"Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1",
            #"Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1",
            "Summer16.WJetsToLNu_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
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
            "Summer16.TTJets_DiLept",
            "Summer16.TTJets_SingleLeptFromT",
            "Summer16.TTJets_SingleLeptFromTbar",
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
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1075_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1275_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1375_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1475_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                ]
    

    cutstrings = {}
    
    for i_score in numpy.arange(-1,1,0.1): 
        cutstrings["tight_%s" % i_score] = "tracks_mva_tight>=%s" % i_score
        cutstrings["loose_%s" % i_score] = "tracks_mva_loose>=%s" % i_score

    cutstrings["nocuts"] = "tracks_is_pixel_track>=0"
    cutstrings["pixeltrack_bdttag"] = "tracks_SR_short>=1"
    cutstrings["stripstrack_bdttag"] = "tracks_SR_long>=1"
    cutstrings["pixeltrack_bdtEDeptag"] = "tracks_SR_short>=1 && tracks_matchedCaloEnergy<10"
    cutstrings["stripstrack_bdtEDeptag"] = "tracks_SR_long>=1 && tracks_matchedCaloEnergy<10"
    cutstrings["pixeltrack_exotag"] = "tracks_is_pixel_track==1 && tracks_passexotag==1"
    cutstrings["stripstrack_exotag"] = "tracks_is_pixel_track==0 && tracks_passexotag==1"
    cutstrings["pixeltrack_mt2tag"] = "tracks_passmt2tag==1"
    cutstrings["stripstrack_mt2tag"] = "tracks_passmt2tag>=2"
    
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
            

    for is_pixel_track, category in enumerate(["long", "short"]): 
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.5, y2=0.5)
        
        g_tight = TGraph(); graphStyler(g_tight)
        g_loose = TGraph(); graphStyler(g_loose)
        g_bdt = TGraph(); graphStyler(g_bdt)
        g_bdtEDep = TGraph(); graphStyler(g_bdtEDep)
        g_mt2 = TGraph(); graphStyler(g_mt2)
        g_exo = TGraph(); graphStyler(g_exo)
           
        for label in histos:
            if "Background" in label: continue
                                    
            sg_num = histos[label].GetBinContent(1 + is_pixel_track)
            sg_den = histos["Signal_nocuts"].GetBinContent(1 + is_pixel_track)
            if sg_den > 0:
                eff_sg = 1.0 * sg_num / sg_den
            else:
                eff_sg = 0
                
            bg_num = histos[label.replace("Signal", "Background")].GetBinContent(1 + is_pixel_track)
            bg_den = histos["Background_nocuts"].GetBinContent(1 + is_pixel_track)
            if bg_den > 0:
                eff_bg = 1.0 * bg_num / bg_den
            else:
                eff_bg = 0
              
            if "tight" in label:
                g_tight.SetPoint(g_tight.GetN(), eff_sg, 1 - eff_bg)
            if "loose" in label:
                g_loose.SetPoint(g_loose.GetN(), eff_sg, 1 - eff_bg)
            
            if (category == "short" and "pixeltrack" in label) \
                or (category == "long" and "stripstrack" in label):
                
                if "bdttag" in label:
                    g_bdt.SetPoint(g_bdt.GetN(), eff_sg, 1 - eff_bg)
                elif "bdtEDep" in label:
                    g_bdtEDep.SetPoint(g_bdtEDep.GetN(), eff_sg, 1 - eff_bg)
                elif "exotag" in label:
                    g_exo.SetPoint(g_exo.GetN(), eff_sg, 1 - eff_bg)
                elif "mt2tag" in label:
                    g_mt2.SetPoint(g_mt2.GetN(), eff_sg, 1 - eff_bg)
    
        g_tight.Sort()
        g_tight.SetLineWidth(2)
        g_tight.SetLineColor(kRed-4)
        g_tight.SetTitle(";#epsilon_{  sg};1 - #epsilon_{  bg}")
        g_tight.GetXaxis().SetRangeUser(0,1)
        g_tight.GetXaxis().SetLimits(0,1)
        g_tight.GetYaxis().SetRangeUser(0,1)
        g_tight.GetYaxis().SetLimits(0,1)
        g_tight.SetFillColor(kWhite)
        g_tight.Draw("")
        legend.AddEntry(g_tight, "d_{xy}-informed BDT")

        g_loose.Sort()
        g_loose.SetLineWidth(2)
        g_loose.SetLineColor(kAzure-3)
        g_loose.Draw("same")
        g_loose.SetFillColor(kWhite)
        legend.AddEntry(g_loose, "BDT")

        g_bdt.SetMarkerStyle(20)
        g_bdt.SetMarkerColor(kRed)
        g_bdt.Draw("same p")
        g_bdt.SetLineColor(kWhite)
        g_bdt.SetFillColor(kWhite)
        legend.AddEntry(g_bdt, "Full tag")

        g_bdtEDep.SetMarkerStyle(20)
        g_bdtEDep.SetMarkerColor(kOrange)
        g_bdtEDep.Draw("same p")
        g_bdtEDep.SetLineColor(kWhite)
        g_bdtEDep.SetFillColor(kWhite)
        legend.AddEntry(g_bdtEDep, "Full tag + EDep<10 GeV")

        g_exo.SetMarkerStyle(20)
        g_exo.SetMarkerColor(kMagenta-3)
        g_exo.Draw("same p")
        g_exo.SetLineColor(kWhite)
        g_exo.SetFillColor(kWhite)
        legend.AddEntry(g_exo, "EXO-19-010 tag")

        g_mt2.SetMarkerStyle(20)
        g_mt2.SetMarkerColor(kCyan+1)
        g_mt2.Draw("same p")
        g_mt2.SetLineColor(kWhite)
        g_mt2.SetFillColor(kWhite)
        legend.AddEntry(g_mt2, "SUS-19-005 tag")
        
        legend.SetHeader("%s tracks" % category)
        legend.Draw()
        
        canvas.Print(category + ".pdf")
        

if __name__ == "__main__":

    main()
    