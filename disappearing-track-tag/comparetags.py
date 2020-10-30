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


def doplots(folder, significance_formula, suffix, significance_label):

    labels = {}  
    
    labels["sg_p0"] = [
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
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1575_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1675_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1775_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1875_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1975_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2075_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2275_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2375_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2475_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2575_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-25_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2675_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2775_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-75_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-975_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        ]
        
    labels["bg_p0"] = [
        "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"Summer16.TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8",
        #"Summer16.TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"Summer16.TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        #"Summer16.TTTT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8",
        "Summer16.TT_TuneCUETP8M2T4_13TeV-powheg-pythia8",
        "Summer16.WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WW_TuneCUETP8M1_13TeV-pythia8",
        "Summer16.WZ_TuneCUETP8M1_13TeV-pythia8",
        "Summer16.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-200To400_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-600To800_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_Zpt-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.ZZ_TuneCUETP8M1_13TeV-pythia8",
        ]

    labels["sg_p1"] = [
        #"RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-10_TuneCP2_13TeV-madgraphMLM-pythia8",
        #"RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8ext1",
        "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8",
        #"RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-50_TuneCP2_13TeV-madgraphMLM-pythia8ext1",
    ]

    labels["bg_p1"] = [
        "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
        #"RunIIFall17MiniAODv2.GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
        #"RunIIFall17MiniAODv2.GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",
        "RunIIFall17MiniAODv2.QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",
        "RunIIFall17MiniAODv2.QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",
        "RunIIFall17MiniAODv2.QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8",
        "RunIIFall17MiniAODv2.QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",
        "RunIIFall17MiniAODv2.QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",
        "RunIIFall17MiniAODv2.QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",
        #"RunIIFall17MiniAODv2.TTGamma_Dilept_TuneCP5_PSweights_13TeV_madgraph_pythia8",
        #"RunIIFall17MiniAODv2.TTGamma_SingleLeptFromTbar_TuneCP5_PSweights_13TeV_madgraph_pythia8",
        #"RunIIFall17MiniAODv2.TTGamma_SingleLeptFromT_TuneCP5_PSweights_13TeV_madgraph_pythia8",
        #"RunIIFall17MiniAODv2.TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
        #"RunIIFall17MiniAODv2.TTHH_TuneCP5_13TeV-madgraph-pythia8",
        #"RunIIFall17MiniAODv2.TTJets_DiLept_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8",
        #"RunIIFall17MiniAODv2.TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",
        #"RunIIFall17MiniAODv2.TTJets_SingleLeptFromTbar_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8",
        #"RunIIFall17MiniAODv2.TTJets_SingleLeptFromT_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.TTJets_TuneCP5_13TeV-madgraphMLM-pythia8",
        #"RunIIFall17MiniAODv2.TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8",
        #"RunIIFall17MiniAODv2.TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8",
        #"RunIIFall17MiniAODv2.TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",
        #"RunIIFall17MiniAODv2.TTTW_TuneCP5_13TeV-madgraph-pythia8",
        #"RunIIFall17MiniAODv2.TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8",
        #"RunIIFall17MiniAODv2.TTWZ_TuneCP5_13TeV-madgraph-pythia8",
        #"RunIIFall17MiniAODv2.TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
        #"RunIIFall17MiniAODv2.TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8",
        #"RunIIFall17MiniAODv2.TTZZ_TuneCP5_13TeV-madgraph-pythia8",
        "RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",
        "RunIIFall17MiniAODv2.WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
        "RunIIFall17MiniAODv2.WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
        "RunIIFall17MiniAODv2.WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_v2",
        #"RunIIFall17MiniAODv2.WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
        "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
        "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
        "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400_13TeV-madgraph",
        "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
        "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
        "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800_13TeV-madgraph",
        "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
        #"RunIIFall17MiniAODv2.ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8",
    ]
    
    labels["sg_p0"] = ["RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV"]
    labels["bg_p0"] = ["Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM"]
    #labels["sg_p1"] = ["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV"]
    #labels["bg_p1"] = ["RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM"]
    #labels["sg_p1"] = list(labels["sg_p0"])
    #labels["bg_p1"] = list(labels["bg_p0"])
    
    #labels["sg_p0"] = ["RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP"]
    #labels["sg_p1"] = ["RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP"]
    #labels["bg_p0"] = ["Summer16.WJetsToLNu_TuneCUETP8M1_13TeV"]
    #labels["bg_p1"] = ["Summer16.WJetsToLNu_TuneCUETP8M1_13TeV"]
    
    for label in labels:
        for i, item in enumerate(labels[label]):
            labels[label][i] = folder + "/" + item + "*root"
    
    basecuts = " && tracks_baseline==1 && pass_baseline==1"
    #basecuts = ""

    # get histograms
    histos = {}
    histos["bg_short_p0"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_pt>10" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_p0"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_p0"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_pt>10 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_p0"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    
    histos["bg_short_p0_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_p0_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_p0_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_p0_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"

    histos["bg_short_wp"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_mva_tight_may20_chi2_pt10>0.05 && tracks_is_pixel_track==1 && tracks_pt>10" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_wp"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_mva_tight_may20_chi2_pt10>0 && tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_wp"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_mva_tight_may20_chi2_pt10>0.05 && tracks_is_pixel_track==1 && tracks_pt>10 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_wp"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_mva_tight_may20_chi2_pt10>0 && tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_short_wp_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_wp_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_wp_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_wp_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"

    histos["bg_short_pt15_p0"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2", "tracks_is_pixel_track==1 && tracks_pt>15" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_pt15_p0"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_pt15_p0"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2", "tracks_is_pixel_track==1 && tracks_pt>15 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_pt15_p0"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_short_pt15_p0_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_pt15_p0_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_pt15_p0_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_pt15_p0_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"
    
    histos["bg_short_pt30_p0"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2", "tracks_is_pixel_track==1 && tracks_pt>30" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_pt30_p0"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_pt30_p0"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2", "tracks_is_pixel_track==1 && tracks_pt>30 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_pt30_p0"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_short_pt30_p0_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_pt30_p0_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_pt30_p0_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_pt30_p0_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"
    
    #histos["bg_short_p1"] = plotting.get_all_histos(labels["bg_p1"], "Events", "tracks_mva_tight_may20_chi2", "tracks_is_pixel_track==1 && tracks_pt>10" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    #histos["bg_long_p1"] = plotting.get_all_histos(labels["bg_p1"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    #histos["sg_short_p1"] = plotting.get_all_histos(labels["sg_p1"], "Events", "tracks_mva_tight_may20_chi2", "tracks_is_pixel_track==1 && tracks_pt>10 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    #histos["sg_long_p1"] = plotting.get_all_histos(labels["sg_p1"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    #
    #histos["bg_short_p1_denom"] = plotting.get_all_histos(labels["bg_p1"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1", nBinsX=200, xmin=-1, xmax=1); print "OK"
    #histos["bg_long_p1_denom"] = plotting.get_all_histos(labels["bg_p1"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2", nBinsX=200, xmin=-1, xmax=1); print "OK"
    #histos["sg_short_p1_denom"] = plotting.get_all_histos(labels["sg_p1"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"
    #histos["sg_long_p1_denom"] = plotting.get_all_histos(labels["sg_p1"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01", nBinsX=200, xmin=-1, xmax=1); print "OK"
    
    histos["bg_short_mt2"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "(tracks_mt2tag>=115 && tracks_mt2tag<150)", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_mt2"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "((tracks_mt2tag>=215 && tracks_mt2tag<250) || (tracks_mt2tag>=316 && tracks_mt2tag<350)) && tracks_nMissingOuterHits>=2", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_mt2"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "(tracks_mt2tag>=115 && tracks_mt2tag<150) && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_mt2"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "((tracks_mt2tag>=215 && tracks_mt2tag<250) || (tracks_mt2tag>=316 && tracks_mt2tag<350)) && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_short_mt2_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_mt2_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_mt2_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_mt2_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"

    histos["bg_short_exo"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_exotag>=17", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_exo"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_exotag>=17 && tracks_nMissingOuterHits>=2", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_exo"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_exotag>=17 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_exo"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_exotag>=17 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_short_exo_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["bg_long_exo_denom"] = plotting.get_all_histos(labels["bg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2", nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_short_exo_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    histos["sg_long_exo_denom"] = plotting.get_all_histos(labels["sg_p0"], "Events", "tracks_mva_tight_may20_chi2_pt10", "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01" + basecuts, nBinsX=200, xmin=-1, xmax=1); print "OK"
    
    for label in histos:
        shared_utils.histoStyler(histos[label])
        if "p0" in label:
            histos[label].Scale(35000)
        elif "p1" in label:
            histos[label].Scale(137000)
        
    # get efficiencies:
    efficiencies = {}
    for label in histos:
        
        if "denom" in label: continue
        
        efficiencies[label] = []
        denominator = histos[label + "_denom"].Integral(histos[label + "_denom"].GetXaxis().FindBin(-1), histos[label + "_denom"].GetXaxis().FindBin(1))

        if "mt2" in label or "exo" in label or "wp" in label:        
            numerator = histos[label].Integral(histos[label].GetXaxis().FindBin(-1), histos[label].GetXaxis().FindBin(1))
            efficiencies[label].append([0, numerator/denominator, numerator])
        else:
            for i_score in numpy.arange(-1.0, 1.0, 0.005): 
                numerator = histos[label].Integral(histos[label].GetXaxis().FindBin(i_score), histos[label].GetXaxis().FindBin(1))
                efficiencies[label].append([i_score, numerator/denominator, numerator])

    # build TGraphs
    graphs_roc = {}
    graphs_sgeff = {}
    graphs_bgeff = {}
    graphs_significance = {}
    ymax = 0
    ymax_short = 0
    ymax_long = 0
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
            
            significance = 0
            try:
                significance = eval(significance_formula)
            except:
                significance = 0
            
            if "p1" not in label and significance > ymax:
                ymax = significance

            if "p1" not in label and significance > ymax_short and "short" in label:
                ymax_short = significance

            if "p1" not in label and significance > ymax_long and "long" in label:
                ymax_long = significance
            graphs_significance[label].SetPoint(graphs_significance[label].GetN(), score, significance)

    for category in ["short", "long"]:

        # plot ROC curves:
        canvas = shared_utils.mkcanvas()
        
        if category == "short":
            histo = TH2F("empty", "empty", 1, 0, 1, 1, 0.9, 1)
        else:
            histo = TH2F("empty", "empty", 1, 0, 1, 1, 0.99, 1)
        
        shared_utils.histoStyler(histo)
        histo.Draw()
        histo.SetTitle(";#epsilon_{  sg};1 - #epsilon_{  bg}")
        
        if category == "short":
            legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.5)
        else: 
            legend = shared_utils.mklegend(x1=0.17, y1=0.2, x2=0.65, y2=0.4)

        for label in sorted(graphs_roc):
                        
            if category not in label:
                continue

            graphStyler(graphs_roc[label])
            
            if "mt2" in label:
                graphs_roc[label].SetMarkerStyle(20)
                graphs_roc[label].SetMarkerColor(kTeal)
                graphs_roc[label].SetLineColor(kWhite)
                graphs_roc[label].Draw("same p")
                legendlabel = "SUS-19-005 tag"
                legend.AddEntry(graphs_roc[label], legendlabel)
            elif "exo" in label:
                graphs_roc[label].SetMarkerStyle(20)
                graphs_roc[label].SetMarkerColor(kViolet)
                graphs_roc[label].SetLineColor(kWhite)
                graphs_roc[label].Draw("same p")
                legendlabel = "EXO-19-010 tag"
                legend.AddEntry(graphs_roc[label], legendlabel)
            elif "wp" in label:
                graphs_roc[label].SetMarkerStyle(20)
                graphs_roc[label].SetMarkerColor(kAzure-3)
                graphs_roc[label].Draw("same p")
                graphs_roc[label].SetLineColor(kWhite)
                legendlabel = "AN-18-214 working point"
                legend.AddEntry(graphs_roc[label], legendlabel)
            elif "pt15" in label:
                if category == "short":
                    legendlabel = "BDT (track p_{T}>15 GeV)"  
                    graphs_roc[label].SetLineColor(kAzure-9)
                    graphs_roc[label].Draw("same")
                    legend.AddEntry(graphs_roc[label], legendlabel)
            elif "pt30" in label:
                if category == "short":
                    legendlabel = "BDT (track p_{T}>30 GeV)"  
                    graphs_roc[label].SetLineColor(kMagenta-8)
                    graphs_roc[label].Draw("same")
                    legend.AddEntry(graphs_roc[label], legendlabel)
            else:
                legendlabel = "BDT (track p_{T}>10 GeV)"   
                graphs_roc[label].SetLineColor(kAzure-3)             
                graphs_roc[label].Draw("same")
                legend.AddEntry(graphs_roc[label], legendlabel)
                

            #if "p1" in label:
            #    graphs_roc[label].SetLineStyle(2)
            #    graphs_significance[label].SetLineStyle(2)
            #legendlabel = label.replace("sg_", "").replace("short_", "short tracks ").replace("long_", "long tracks ").replace("p0", " (phase 0)").replace("p1", " (phase 1)")
            #legendlabel = label.replace("sg_", "").replace("short_", "short tracks ").replace("long_", "long tracks ").replace("p0", "").replace("p1", "")

                
        legend.SetTextSize(0.045)
        legend.Draw()
        shared_utils.stamp()
        canvas.Print("roc_%s_%s.pdf" % (folder.split("/")[-1], category))
        
        if ymax < 1:
            ymax = 1
        else:
            ymax = 1.1 * ymax
        
        if ymax_short < 1:
            ymax_short = 1
        else:
            ymax_short = 1.1 * ymax_short
         
        if ymax_long < 1:
            ymax_long = 1
        else:
            ymax_long = 1.1 * ymax_long
        
        
        # plot significance:
        canvas = shared_utils.mkcanvas()
        #histo = TH2F("empty", "empty", 1, -1, 1, 1, 0, ymax)
        #histo = TH2F("empty", "empty", 1, -1, 1, 1, 0, ymax)
        
        if category == "short":
            histo = TH2F("empty", "empty", 1, -1, 1, 1, 0, ymax_short)
        else:
            histo = TH2F("empty", "empty", 1, -1, 1, 1, 0, ymax_long)
        
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

            graphs_bgeff[label].Draw("same")
            graphStyler(graphs_bgeff[label])
            graphs_bgeff[label].SetLineColor(kRed)

            if "p1" in label:
                graphs_significance[label].SetLineStyle(2)
                graphs_sgeff[label].SetLineStyle(2)
                graphs_bgeff[label].SetLineStyle(2)

            legendlabel = label.replace("sg_", "").replace("short_", "short tracks ").replace("long_", "long tracks ").replace("p0", " (phase 0)").replace("p1", " (phase 1)")
        
        phase0 = graphs_significance["sg_short_p0"].Clone()
        #phase1 = graphs_significance["sg_short_p1"].Clone()
        phase0.SetLineColor(kBlack)
        #phase1.SetLineColor(kBlack)
        
        
        legend.AddEntry(phase0, "Phase 0")
        #legend.AddEntry(phase1, "Phase 1")

        legend.AddEntry(graphs_sgeff["sg_short_p0"], "signal efficiency #epsilon_{sg}")
        legend.AddEntry(graphs_bgeff["sg_short_p0"], "background efficiency #epsilon_{bg}")

        #legend.AddEntry(graphs_significance["sg_short_p0"], "#epsilon_{sg} / #sqrt{#epsilon_{sg} + #epsilon_{bg}}")
        legend.AddEntry(graphs_significance["sg_short_p0"], significance_label)
        
        legend.Draw()
        shared_utils.stamp()
        os.system("mkdir -p plot-significance")
        canvas.Print("plot-significance/significance_%s%s.pdf" % (category, suffix))
       

if __name__ == "__main__":

    #folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_52_iso_merged"
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/tools"
    #folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_56_pixelpt10_cutflow"


    significances = {
            "_scaled1": ["N_sg / math.sqrt( N_sg + N_bg )", "S / #sqrt{S+B}"],
            #"_10BG_scaled1": ["N_sg / math.sqrt( N_bg + (0.1*N_bg)**2 )", "S / #sqrt{B+(0.1B)^{2}}"],
            #"_20BG_scaled1": ["N_sg / math.sqrt( N_bg + (0.2*N_bg)**2 )", "S / #sqrt{B+(0.2B)^{2}}"],
            #"_30BG_scaled1": ["N_sg / math.sqrt( N_bg + (0.3*N_bg)**2 )", "S / #sqrt{B+(0.3B)^{2}}"],
            #"_scaled1e4": ["1e4*N_sg / math.sqrt( 1e4*N_sg + N_bg )", "1e4*S / #sqrt{1e4*S+B}"],
            #"_scaled1e5": ["1e5*N_sg / math.sqrt( 1e5*N_sg + N_bg )", "1e5*S / #sqrt{1e5*S+B}"],
            #"_scaled1e6": ["1e6*N_sg / math.sqrt( 1e6*N_sg + N_bg )", "1e6*S / #sqrt{1e6*S+B}"],
            #"_scaled1e7": ["1e7*N_sg / math.sqrt( 1e7*N_sg + N_bg )", "1e7*S / #sqrt{1e7*S+B}"],
            #"_20BG_scaled1e4": ["1e4*N_sg / math.sqrt( N_bg + (0.2*N_bg)**2 )", "1e4*S / #sqrt{B+(0.2B)^{2}}"],
            #"_20BG_scaled1e5": ["1e5*N_sg / math.sqrt( N_bg + (0.2*N_bg)**2 )", "1e5*S / #sqrt{B+(0.2B)^{2}}"],
            #"_20BG_scaled1e6": ["1e6*N_sg / math.sqrt( N_bg + (0.2*N_bg)**2 )", "1e6*S / #sqrt{B+(0.2B)^{2}}"],
            #"_30BG_scaled1e4": ["1e4*N_sg / math.sqrt( N_bg + (0.3*N_bg)**2 )", "1e4*S / #sqrt{B+(0.3B)^{2}}"],
            #"_30BG_scaled1e5": ["1e5*N_sg / math.sqrt( N_bg + (0.3*N_bg)**2 )", "1e5*S / #sqrt{B+(0.3B)^{2}}"],
            #"_30BG_scaled1e6": ["1e6*N_sg / math.sqrt( N_bg + (0.3*N_bg)**2 )", "1e6*S / #sqrt{B+(0.3B)^{2}}"],
    }
    
    for significance_suffix in significances:
        significance_formula = significances[significance_suffix][0]
        significance_label = significances[significance_suffix][1]
        doplots(folder, significance_formula, significance_suffix, significance_label)
    
    
    
