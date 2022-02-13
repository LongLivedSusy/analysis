#!/bin/env python
from __future__ import division
import __main__ as main
from ROOT import *
from optparse import OptionParser
from array import array
import math, os, glob
import GridEngineTools
import math
import shared_utils
import collections
import numpy as np

parser = OptionParser()
parser.add_option("--inputfile", dest = "inputfile", default = "")
parser.add_option("--outputfile", dest = "outputfile")
parser.add_option("--mode", dest="mode")
parser.add_option("--outputfolder", dest="outputfolder", default = "ddbg_400")
parser.add_option("--skimfolder", dest="skimfolder", default = "../ntupleanalyzer/skim_120_full_merged")
parser.add_option("--nev", dest = "nev", default = -1)
parser.add_option("--jobs_per_file", dest = "jobs_per_file", default = 10)
parser.add_option("--files_per_job", dest = "files_per_job", default = 1)
parser.add_option("--event_start", dest = "event_start", default = 0)
parser.add_option("--runmode", dest="runmode", default="grid")
parser.add_option("--debug", dest="debug", action="store_true")
(options, args) = parser.parse_args()

if options.inputfile != "":
    if "Run2016" in options.inputfile or "Summer16" in options.inputfile:
        phase = 0
    elif "Run2017" in options.inputfile or "Run2018" in options.inputfile or "Fall17" in options.inputfile or "Autumn18" in options.inputfile:
        phase = 1
else:
    phase = 0

binnings = {}
binnings["analysis"] = {}
binnings["analysis"]["LepMT"] = [8, 0, 160]
binnings["analysis"]["leptons_mt"] = binnings["analysis"]["LepMT"]
binnings["analysis"]["leadinglepton_mt"] = binnings["analysis"]["LepMT"]
binnings["analysis"]["InvMass"] = [20, 50, 170]
binnings["analysis"]["tracks_invmass"] = binnings["analysis"]["InvMass"]
binnings["analysis"]["Ht"] = [5, 0, 2000]
binnings["analysis"]["HT"] = binnings["analysis"]["Ht"]
binnings["analysis"]["Met"] = [20, 0, 600]
binnings["analysis"]["MET"] = binnings["analysis"]["Met"]
binnings["analysis"]["Mht"] = binnings["analysis"]["Met"]
binnings["analysis"]["MHT"] = binnings["analysis"]["Met"]
binnings["analysis"]["tracks_pt"] = [50, 0, 1000]
binnings["analysis"]["leadinglepton_pt"] = binnings["analysis"]["Ht"]
binnings["analysis"]["leadinglepton_eta"] = [15, 0, 3]
binnings["analysis"]["tracks_eta"] = [15, 0, 3]
binnings["analysis"]["tracks_dxyVtx"] = [25, 0, 0.1]
binnings["analysis"]["DeDxAverage"] = [5, 2, 7]
binnings["analysis"]["tracks_massfromdeDxPixel"] = binnings["analysis"]["DeDxAverage"]
binnings["analysis"]["tracks_deDxHarmonic2pixel"] = binnings["analysis"]["DeDxAverage"]
binnings["analysis"]["BinNumber"] = [ 88, 1, 89]
binnings["analysis"]["region"] = binnings["analysis"]["BinNumber"]
binnings["analysis"]["n_tags"] = [ 3, 0, 3]
binnings["analysis"]["n_goodjets"] = [ 10, 0, 10]
binnings["analysis"]["n_btags"] = binnings["analysis"]["n_goodjets"]
binnings["analysis"]["n_goodelectrons"] = [ 5, 0, 5]
binnings["analysis"]["n_goodmuons"] = [ 5, 0, 5]
binnings["analysis"]["BTags"] = [ 4, 0, 4]
binnings["analysis"]["tracks_is_pixel_track"] = [ 2, 0, 2]
binnings["analysis"]["Track1MassFromDedx"] = [ 25, 0, 1000]
binnings["analysis"]["Log10DedxMass"] = [10, 0, 5]
binnings["analysis"]["region"] = [54,1,55]
binnings["analysis"]["region_sideband"] = binnings["analysis"]["region"]
binnings["analysis"]["region"] = binnings["analysis"]["region"]
binnings["analysis"]["tracks_matchedCaloEnergy"] = [25, 0, 50]
binnings["analysis"]["tracks_trkRelIso"] = [20, 0, 0.2]
binnings["analysis"]["tracks_region"] = [54, 1, 55]
binnings["analysis"]["tracks_ECaloPt"] = [25, 0, 1]
binnings["analysis"]["tracks_MinDeltaPhiTrackMht"] = [32, 0, 3.2]
binnings["analysis"]["tracks_MinDeltaPhiTrackLepton"] = binnings["analysis"]["tracks_MinDeltaPhiTrackMht"]
binnings["analysis"]["tracks_MinDeltaPhiTrackJets"] = binnings["analysis"]["tracks_MinDeltaPhiTrackMht"]
binnings["analysis"]["tracks_ptRatioTrackMht"] = [20, 0, 10]
binnings["analysis"]["tracks_ptRatioTrackLepton"] = binnings["analysis"]["tracks_ptRatioTrackMht"]
binnings["analysis"]["tracks_ptRatioTrackJets"] = binnings["analysis"]["tracks_ptRatioTrackMht"]
binnings["analysis"]["MinDeltaPhiMhtJets"] = binnings["analysis"]["tracks_MinDeltaPhiTrackMht"]
binnings["analysis"]["MinDeltaPhiLeptonMht"] = binnings["analysis"]["tracks_MinDeltaPhiTrackMht"]
binnings["analysis"]["MinDeltaPhiLeptonJets"] = binnings["analysis"]["tracks_MinDeltaPhiTrackMht"]
binnings["analysis"]["ptRatioMhtJets"] = binnings["analysis"]["tracks_ptRatioTrackMht"]
binnings["analysis"]["ptRatioLeptonMht"] = binnings["analysis"]["tracks_ptRatioTrackMht"]
binnings["analysis"]["ptRatioLeptonJets"] = binnings["analysis"]["tracks_ptRatioTrackMht"]
binnings["fakerate"] = {}
binnings["fakerate"]["tracks_pt"] = [20, 0, 1000]
binnings["fakerate"]["tracks_eta"] = ["variable", 0, 1.5, 2.0, 3.0]
binnings["fakerate"]["tracks_is_pixel_track"] = [2, 0, 2]
binnings["fakerate"]["HT"] = ["variable", 0, 200, 400, 600, 800, 1000, 2000]
binnings["fakerate"]["MHT"] = [10, 0, 2000]
binnings["fakerate"]["n_allvertices"] = [25, 0, 50]
binnings["fakerate"]["n_goodjets"] = [20, 0, 20]
binnings["fakerate"]["n_btags"] = [10, 0, 10]
binnings["fakerate"]["MinDeltaPhiMhtJets"] = [100, 0, 5]
binnings["fakerate"]["tracks_eta"] = [12, -3, 3]
binnings["fakerate"]["tracks_phi"] = [16, -4, 4]
binnings["fakerate"]["HT:n_allvertices"] = [3, 0, 2000, 3, 0, 50]
binnings["kappa"] = {}
binnings["kappa"]["tracks_pt"] = ["variable", 0, 40, 60, 300]
binnings["trackvars"] = {}
binnings["trackvars"]["tracks_dxyVtx"] = [25, 0, 0.1]
binnings["trackvars"]["tracks_trkRelIso"] = [40, 0, 0.2]
binnings["trackvars"]["tracks_dzVtx"] = [25, 0, 0.05]
binnings["trackvars"]["tracks_nMissingOuterHits"] = [20, 0, 20]
binnings["trackvars"]["tracks_nValidPixelHits"] = [10, 0, 10]
binnings["trackvars"]["tracks_nValidTrackerHits"] = [20, 0, 20]
binnings["trackvars"]["tracks_chi2perNdof"] = [20, 0, 5.0]
binnings["trackvars"]["tracks_ptErrOverPt2"] = [20, 0, 0.1]               
binnings["trackvars"]["tracks_deDxHarmonic2pixel"] = [20, 0, 10]
binnings["trackvars"]["tracks_matchedCaloEnergy"] = [20, 0, 50]
binnings["trackvars"]["tracks_invmass"] = [50, 50, 140]
binnings["trackvars"]["n_tags"] = [25, 0, 25]
binnings["mcplots"] = binnings["analysis"]

variables = {}
variables["analysis"] = [
                          "HT",
                          "MHT",
                          "n_goodjets",
                          "n_btags",
                          "leadinglepton_mt",
                          "tracks_invmass",
                          "tracks_is_pixel_track",
                          "tracks_pt",
                          "tracks_eta",
                          "tracks_deDxHarmonic2pixel",
                          "tracks_matchedCaloEnergy",
                          "tracks_trkRelIso",
                          "tracks_MinDeltaPhiTrackMht",
                          "tracks_ptRatioTrackMht",
                          "n_tags",
                          #"tracks_MinDeltaPhiTrackLepton",
                          #"tracks_MinDeltaPhiTrackJets",
                          #"tracks_ptRatioTrackLepton",
                          #"tracks_ptRatioTrackJets",
                          #"MinDeltaPhiMhtJets",
                          #"MinDeltaPhiLeptonMht",
                          #"MinDeltaPhiLeptonJets",
                          #"ptRatioMhtJets",
                          #"ptRatioLeptonMht",
                          #"ptRatioLeptonJets",
                          #"tracks_ECaloPt",
                          "region",
                        ]
                        
variables["mcplots"] = variables["analysis"]

variables["fakerate"] = [
                          #"HT:n_allvertices",
                          #"tracks_pt",
                          "tracks_eta",
                          #"tracks_is_pixel_track",
                          #"HT",
                          #"MHT",
                          #"n_goodjets",
                          #"n_allvertices",
                          #"n_btags",
                        ]

variables["kappa"] = [
                          "tracks_pt",
                     ]
                     
variables["trackvars"] = [
                          "tracks_dxyVtx",
                          "tracks_trkRelIso",
                          "tracks_dzVtx",
                          "tracks_nMissingOuterHits",
                          "tracks_nValidPixelHits",
                          "tracks_nValidTrackerHits",
                          "tracks_chi2perNdof",
                          "tracks_ptErrOverPt2",
                          "tracks_deDxHarmonic2pixel",
                          "tracks_matchedCaloEnergy",
                          "tracks_invmass",
                          "n_tags",
                         ]                     
                     
categories = [
                          "short",
                          "long",
             ]

######### event-level cuts #########

event_selections = {}
event_selections["analysis"] = collections.OrderedDict()
event_selections["analysis"]["Baseline"] =               "(event.n_goodjets>=1 and event.MHT>30 and (event.n_goodelectrons==0 and event.n_goodmuons==0) or (event.leadinglepton_mt>110 and event.tracks_invmass[i_track]>120))"
#event_selections["analysis"]["QCDLowMHTValidationJets"] = "event.n_goodelectrons==0 and event.n_goodmuons==0 and event.MHT>60 and event.MHT<100 and event.n_goodjets>=1"
#event_selections["analysis"]["QCDLowMHTJets"] =         "event.n_goodelectrons==0 and event.n_goodmuons==0 and event.MHT>30 and event.MHT<60 and event.n_goodjets>=1"
#event_selections["analysis"]["QCDLowMHT"] =             "event.n_goodelectrons==0 and event.n_goodmuons==0 and event.MHT>30 and event.MHT<60"
#event_selections["analysis"]["QCDLowMHTConstruction"] = "event.n_goodelectrons==0 and event.n_goodmuons==0 and event.MHT<60"
event_selections["analysis"]["HadBaseline"] =            "event.HT>150 and event.MHT>150 and event.n_goodjets>=1 and event.n_goodelectrons==0 and event.n_goodmuons==0"
event_selections["analysis"]["SMuBaseline"] =            "event.MHT>30 and event.n_goodjets>=1 and event.n_goodmuons>=1 and event.n_goodelectrons==0 and event.tracks_invmass[i_track]>120 and event.leadinglepton_mt>110"
event_selections["analysis"]["SMuValidationZLL"] =       "event.MHT>30 and event.n_goodjets>=1 and event.n_goodmuons>=1 and event.n_goodelectrons==0 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<110"
event_selections["analysis"]["SMuValidationLowMT"] =     "event.MHT>30 and event.n_goodjets>=1 and event.n_goodmuons>=1 and event.n_goodelectrons==0 and event.tracks_invmass[i_track]>120 and event.leadinglepton_mt>30 and event.leadinglepton_mt<100"
event_selections["analysis"]["SMuValidationHighMT"] =    "event.MHT>30 and event.n_goodjets>=1 and event.n_goodmuons>=1 and event.n_goodelectrons==0 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<120 and event.leadinglepton_mt>100"
event_selections["analysis"]["SElBaseline"] =            "event.MHT>30 and event.n_goodjets>=1 and event.n_goodelectrons>=1 and event.tracks_invmass[i_track]>120 and event.leadinglepton_mt>110"
event_selections["analysis"]["SElValidationZLL"] =       "event.MHT>30 and event.n_goodjets>=1 and event.n_goodelectrons>=1 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<110"
event_selections["analysis"]["SElValidationLowMT"] =     "event.MHT>30 and event.n_goodjets>=1 and event.n_goodelectrons>=1 and event.tracks_invmass[i_track]>120 and event.leadinglepton_mt>30 and event.leadinglepton_mt<100"
event_selections["analysis"]["SElValidationHighMT"] =    "event.MHT>30 and event.n_goodjets>=1 and event.n_goodelectrons>=1 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<120 and event.leadinglepton_mt>100"
event_selections["analysis"]["QCDLowMHTVal"] =           "event.n_goodelectrons==0 and event.n_goodmuons==0 and event.MHT>60 and event.MHT<100 and event.n_goodjets>=1"
event_selections["analysis"]["QCDLowMHT"] =              "event.n_goodelectrons==0 and event.n_goodmuons==0 and event.MHT<60"
event_selections["analysis"]["PromptDY"] =               "event.n_goodelectrons==1 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<110"

event_selections["mcplots"] = event_selections["analysis"]

event_selections["fakerate"] = collections.OrderedDict()
event_selections["fakerate"]["QCDLowMHT"] =              "event.n_goodelectrons==0 and event.n_goodmuons==0 and event.MHT<60"

event_selections["kappa"] = collections.OrderedDict()
event_selections["kappa"]["PromptDY"] =                  "event.n_goodelectrons==1 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<110"

event_selections["trackvars"] = collections.OrderedDict()
event_selections["trackvars"]["DYEl"] =                  "event.n_goodelectrons>=1 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<110"
event_selections["trackvars"]["DYElSingle"] =            "event.n_goodelectrons>=1 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<110"
event_selections["trackvars"]["DYMu"] =                  "event.n_goodmuons>=1 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<110"
event_selections["trackvars"]["DYMuSingle"] =            "event.n_goodmuons>=1 and event.tracks_invmass[i_track]>65 and event.tracks_invmass[i_track]<110"

######### region definitons #########

# some common cuts, baseline selection already applied in event/track selection:
#vetoes = " and event.tracks_passpionveto[i_track]==1 and event.tracks_passjetveto[i_track]==1 and event.tracks_passleptonveto[i_track]==1"
#baselineShort = "event.tracks_is_pixel_track[i_track]==1 and abs(event.tracks_eta[i_track])<2.0" + vetoes
#baselineLong = "event.tracks_is_pixel_track[i_track]==0 and event.tracks_nMissingOuterHits>=2 and abs(event.tracks_eta[i_track])<2.0" + vetoes
baselineShort = "event.tracks_is_pixel_track[i_track]==1 "
baselineLong = "event.tracks_is_pixel_track[i_track]==0 "


if phase == 0:
    SignalShort = "event.tracks_mva_nov20_noEdep[i_track]>0.1 and (event.tracks_matchedCaloEnergy[i_track]<15 or event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.15)"
    SignalLong = "event.tracks_mva_nov20_noEdep[i_track]>0.1 and (event.tracks_matchedCaloEnergy[i_track]<15 or event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.15)"
    FakeSidebandShort = "event.tracks_mva_nov20_noEdep[i_track]>-0.5 and event.tracks_mva_nov20_noEdep[i_track]<0.1 and (event.tracks_matchedCaloEnergy[i_track]<15 or event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.15)"
    FakeSidebandLong = "event.tracks_mva_nov20_noEdep[i_track]>-0.5 and event.tracks_mva_nov20_noEdep[i_track]<0.1 and (event.tracks_matchedCaloEnergy[i_track]<15 or event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.15)"
    PromptSidebandShort = "event.tracks_mva_nov20_noEdep[i_track]>0.1 and event.tracks_matchedCaloEnergy[i_track]>20 and event.tracks_matchedCaloEnergy[i_track]<90"
    PromptSidebandLong = "event.tracks_mva_nov20_noEdep[i_track]>0.1 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]>0.45 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.95"
    FakeSidebandCRShort = "event.tracks_mva_nov20_noEdep[i_track]>-0.1 and event.tracks_mva_nov20_noEdep[i_track]<0.1 and event.tracks_matchedCaloEnergy[i_track]<5"
    FakeSidebandCRLong = "event.tracks_mva_nov20_noEdep[i_track]>-0.3 and event.tracks_mva_nov20_noEdep[i_track]<0.1 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.05"
    PromptSidebandCRShort = "event.tracks_mva_nov20_noEdep[i_track]>-0.4 and event.tracks_matchedCaloEnergy[i_track]>20 and event.tracks_matchedCaloEnergy[i_track]<50"
    PromptSidebandCRLong = "event.tracks_mva_nov20_noEdep[i_track]>-0.3 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]>0.45 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.90"
else:
    SignalShort = "event.tracks_mva_nov20_noEdep[i_track]>0.12 and (event.tracks_matchedCaloEnergy[i_track]<15 or event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.15)"
    SignalLong = "event.tracks_mva_nov20_noEdep[i_track]>0.15 and (event.tracks_matchedCaloEnergy[i_track]<15 or event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.15)"
    FakeSidebandShort = "event.tracks_mva_nov20_noEdep[i_track]>-0.5 and event.tracks_mva_nov20_noEdep[i_track]<0.1 and (event.tracks_matchedCaloEnergy[i_track]<15 or event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.15)"
    FakeSidebandLong = "event.tracks_mva_nov20_noEdep[i_track]>-0.5 and event.tracks_mva_nov20_noEdep[i_track]<0.1 and (event.tracks_matchedCaloEnergy[i_track]<15 or event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.15)"
    PromptSidebandShort = "event.tracks_mva_nov20_noEdep[i_track]>0.12 and event.tracks_matchedCaloEnergy[i_track]>20 and event.tracks_matchedCaloEnergy[i_track]<90"
    PromptSidebandLong = "event.tracks_mva_nov20_noEdep[i_track]>0.15 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]>0.45 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.95"
    FakeSidebandCRShort = "event.tracks_mva_nov20_noEdep[i_track]>-0.3 and event.tracks_mva_nov20_noEdep[i_track]<0.12 and event.tracks_matchedCaloEnergy[i_track]<5"
    FakeSidebandCRLong = "event.tracks_mva_nov20_noEdep[i_track]>-0.3 and event.tracks_mva_nov20_noEdep[i_track]<0.15 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.05"
    PromptSidebandCRShort = "event.tracks_mva_nov20_noEdep[i_track]>-0.5 and event.tracks_matchedCaloEnergy[i_track]>20 and event.tracks_matchedCaloEnergy[i_track]<40"
    PromptSidebandCRLong = "event.tracks_mva_nov20_noEdep[i_track]>-0.2 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]>0.2 and event.tracks_matchedCaloEnergy[i_track]/event.tracks_p[i_track]<0.5"

regions = collections.OrderedDict()
regions["sr_short"] = baselineShort + " and " + SignalShort
regions["sr_long"] = baselineLong + " and " + SignalLong
regions["promptSideband_short"] = baselineShort + " and " + PromptSidebandShort
regions["promptSideband_long"] = baselineLong + " and " + PromptSidebandLong    
regions["fakeSideband_short"] = baselineShort + " and " + FakeSidebandShort
regions["fakeSideband_long"] = baselineLong + " and " + FakeSidebandLong    
regions["promptcr_short"] = baselineShort + " and " + PromptSidebandCRShort + " and event.tracks_MinDeltaPhiTrackMht[i_track]<(3.14/3)"
regions["promptcr_long"] = baselineLong + " and " + PromptSidebandCRLong + " and event.tracks_MinDeltaPhiTrackMht[i_track]<(3.14/3)"
regions["fakecr_short"] = baselineShort + " and " + FakeSidebandCRShort + " and event.tracks_MinDeltaPhiTrackMht[i_track]>(3.14/2)"
regions["fakecr_long"] = baselineLong + " and " + FakeSidebandCRLong + " and event.tracks_MinDeltaPhiTrackMht[i_track]>(3.14/2)"

for kappa_variable in variables["kappa"]:
    regions["promptprediction_%s_short" % kappa_variable] = regions["promptcr_short"]
    regions["promptprediction_%s_long" % kappa_variable] = regions["promptcr_long"]

for fakerate_variable in variables["fakerate"]:
    regions["fakeprediction_%s_short" % fakerate_variable] = regions["fakecr_short"]
    regions["fakeprediction_%s_long" % fakerate_variable] = regions["fakecr_long"]

######### add genfake and genprompt info to all regions #########

for regionlabel in regions.keys():
    regions[regionlabel.replace("_short", "_genfake_short").replace("_long", "_genfake_long")] = regions[regionlabel] + " and event.tracks_fake[i_track]==1"
    regions[regionlabel.replace("_short", "_genprompt_short").replace("_long", "_genprompt_long")] = regions[regionlabel] + " and event.tracks_fake[i_track]==0"

######### samples #########

mc_summer16 = [
               "Summer16.DYJetsToLL*root",
               "Summer16.QCD*root",
               "Summer16.WJetsToLNu*root",
               "Summer16.ZJetsToNuNu_HT*root",
               "Summer16.WW_TuneCUETP8M1*root",
               "Summer16.WZ_TuneCUETP8M1*root",
               "Summer16.ZZ_TuneCUETP8M1*root",
               "Summer16.TTJets_DiLept*root",
               "Summer16.TTJets_SingleLeptFromT*root",
              ]
mc_fall17 = [
               "RunIIFall17MiniAODv2.DYJetsToLL*root",
               "RunIIFall17MiniAODv2.QCD*root",
               "RunIIFall17MiniAODv2.WJetsToLNu*root",
               "RunIIFall17MiniAODv2.ZJetsToNuNu_HT*root",
               "RunIIFall17MiniAODv2.WW*root",
               "RunIIFall17MiniAODv2.WZ*root",
               "RunIIFall17MiniAODv2.ZZ*root",
               "RunIIFall17MiniAODv2.TTJets_DiLept_Tune*root",
               "RunIIFall17MiniAODv2.TTJets_SingleLeptFromT_Tune*root",
              ]
              
samples = {}
samples["fakerate"] = {
            "Summer16": mc_summer16,
            "Run2016": ["Run2016*JetHT*root"],
            "Fall17": mc_fall17,
            "Run2017": ["Run2017*JetHT*root"],
            "Run2018": ["Run2018*JetHT*root"],
          }
samples["kappa"] = {
            "Summer16": mc_summer16,
            "Run2016": ["Run2016*SingleElectron*root"],
            "Fall17": mc_fall17,
            "Run2017": ["Run2017*SingleElectron*root"],
            "Run2018": ["Run2018*EGamma*root"],
          }
samples["analysis"] = {
            "Summer16": mc_summer16,
            "T1qqqq16": ["RunIISummer16MiniAODv3.SMS-T1qqqq*root"],
            "T2bt16": ["RunIISummer16MiniAODv3.SMS-T2bt*root"],
            "Run2016SingleElectron": ["Run2016*SingleElectron*root"],
            "Run2016SingleMuon": ["Run2016*SingleMuon*root"],
            "Run2016MET": ["Run2016*MET*root"],
            "Run2016JetHT": ["Run2016*JetHT*root"],
            "Fall17": mc_fall17,
            "T1qqqq17": ["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq*root"],
            "Run2017SingleElectron": ["Run2017*SingleElectron*root"],
            "Run2017SingleMuon": ["Run2017*SingleMuon*root"],
            "Run2017MET": ["Run2017*MET*root"],
            "Run2017JetHT": ["Run2017*JetHT*root"],
            "Run2018SingleElectron": ["Run2018*EGamma*root"],
            "Run2018SingleMuon": ["Run2018*SingleMuon*root"],
            "Run2018MET": ["Run2018*MET*root"],
            "Run2018JetHT": ["Run2018*JetHT*root"],
          }
samples["trackvars"] = {
            "Summer16": mc_summer16,
            #"T1qqqq16": ["RunIISummer16MiniAODv3.SMS-T1qqqq*root"],
            #"T2bt16": ["RunIISummer16MiniAODv3.SMS-T2bt*root"],
            "Run2016SingleElectron": ["Run2016*SingleElectron*root"],
            "Run2016SingleMuon": ["Run2016*SingleMuon*root"],
            #"Run2016MET": ["Run2016*MET*root"],
            #"Run2016JetHT": ["Run2016*JetHT*root"],
          }
samples["mcplots"] = {
            #"Summer16": mc_summer16,
            #"T1qqqq16": ["RunIISummer16MiniAODv3.SMS-T1qqqq*root"],
            #"T2bt16": ["RunIISummer16MiniAODv3.SMS-T2bt*root"],
            "PMSSM17": ["RunIIFall17FS.PMSSM*root"],
            "PMSSM18": ["RunIIFall18FS.PMSSM*root"],
          }

signal_cuts = {
               "pooled": "event.tracks_chiCandGenMatchingDR[i_track]<0.01",
               "glu2000_lsp1000": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_gluino_mass==2000 and event.signal_lsp_mass==1000",
               "glu2000_lsp1975": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_gluino_mass==2000 and event.signal_lsp_mass==1975",
               "glu2700_lsp1700": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_gluino_mass==2700 and event.signal_lsp_mass==1700",
               "glu2700_lsp2672": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_gluino_mass==2700 and event.signal_lsp_mass==2672",
               "stop2000_lsp1000": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_stop_mass==2000 and event.signal_lsp_mass==1000",
               "stop2000_lsp1900": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_stop_mass==2000 and event.signal_lsp_mass==1900",
               "stop2500_lsp1500": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_stop_mass==2500 and event.signal_lsp_mass==1500",
               "stop2500_lsp2000": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_stop_mass==2500 and event.signal_lsp_mass==2000",
            }


def calculate_ratio(mode, rootfile, path, numerator_label, denominator_label, ratio_label):
    
    for variable in variables[mode]:
        for run_period in samples[mode]:
            for event_selection in event_selections[mode]:
                for category in categories:
                    
                    tfile_merged = TFile(path + "/merged_%s.root" % run_period, "read")
                    fakes_numerator = tfile_merged.Get(run_period + "_" + variable + "_" + event_selection + "_" + numerator_label + "_" + category)
                    fakes_numerator.SetDirectory(0)
                    fakes_denominator = tfile_merged.Get(run_period + "_" + variable + "_" + event_selection + "_" + denominator_label + "_" + category)
                    fakes_denominator.SetDirectory(0)
                    tfile_merged.Close()

                    print "histo", run_period + "_" + variable + "_" + event_selection + "_" + numerator_label + "_" + category
                    print "last", fakes_numerator.GetBinCenter(fakes_numerator.GetXaxis().GetNbins())
                    print "overflow", fakes_numerator.GetBinCenter(fakes_numerator.GetXaxis().GetNbins()+1)
                    

                    tfile_fakerate = TFile(rootfile, "update")
                    fakes_numerator.Write()
                    fakes_denominator.Write()
                    fakerate = fakes_numerator.Clone()
                    fakerate.SetName(fakerate.GetName().replace("_" + numerator_label + "_", "_" + ratio_label + "_"))
                    fakerate.Divide(fakes_denominator)
                    fakerate.Write()
                    tfile_fakerate.Close()


def hadd_everything(samples, outputfolder):
    
    contains_data = False
    commands = []
    
    for data_period in samples:
        
        if "T1qqqq" in data_period or "T2bt" in data_period:
            extracuts = signal_cuts
        else:
            extracuts = {
                      "": "",
                    }
            
        for extracut_label in extracuts:
            
            if "T1qqqq" in data_period and "stop" in extracut_label:
                continue
            elif "T2bt" in data_period and "glu" in extracut_label:
                continue
            
            command = "hadd -f %s/merged_%s%s.root " % (outputfolder, data_period, extracut_label)
            for sample in samples[data_period]:
                command += "%s/%s " % (outputfolder, sample.replace("*root", "*%s*root" % extracut_label))
            commands.append(command)
        
            if "Run201" in data_period:
                contains_data = True
        
    GridEngineTools.runParallel(commands, "multi", "none", confirm=False)

    if contains_data:
        os.system("hadd -f %s/merged_Run2016All.root %s/merged_Run2016*root " % (outputfolder, outputfolder))
        os.system("hadd -f %s/merged_Run2017All.root %s/merged_Run2017*root " % (outputfolder, outputfolder))
        os.system("hadd -f %s/merged_Run2018All.root %s/merged_Run2018*root " % (outputfolder, outputfolder))


def submit_files(mode, outputfolder, options, submit = True):

    this_script_name = os.path.basename(__file__)

    inputfiles = []
    for data_period in samples[mode]:
        for sample in samples[mode][data_period]:
            if options.debug:
                inputfiles += glob.glob(options.skimfolder + "/" + sample)[0:1]
            else:
                inputfiles += glob.glob(options.skimfolder + "/" + sample)[:]
    commands = []

    for i, inputfile in enumerate(inputfiles):            
        print inputfile
        if options.jobs_per_file>1:
            fin = TFile(inputfile)
            tree = fin.Get("Events")
            nev = tree.GetEntries()
            fin.Close()
            if nev>0 and int(nev/options.jobs_per_file)>0:
                for iStart in range(0, nev, int(nev/options.jobs_per_file)):
                    cmd = "./%s/%s --outputfolder %s --inputfile %s --outputfile %s --mode %s --event_start %s --nev %s; " % (options.outputfolder, this_script_name, outputfolder, inputfile, outputfolder + "/" + inputfile.split("/")[-1], mode, iStart, int(nev/options.jobs_per_file))
                    commands.append(cmd)
        else:
            cmd = "./%s/%s --outputfolder %s --inputfile ../%s --outputfile ../%s --mode %s; " % (options.outputfolder, this_script_name, outputfolder, inputfile, outputfolder + "/" + inputfile.split("/")[-1], mode)
            commands.append(cmd)
            
    if options.files_per_job>1:
        old_commands = list(commands)
        commands = []
        for chunk in chunks(old_commands, options.files_per_job):
            commands.append(" ".join(chunk))

    if submit:
        print "Running %s jobs..." % len(commands)        
        GridEngineTools.runParallel(commands, options.runmode, "%s.condor" % outputfolder, confirm=False)

    return commands
            

def spawn_jobs(options):
    
    if options.mode == "trackvars" or options.mode == "mcplots":
        
        os.system("mkdir -p %s" % options.outputfolder)
        
        this_script_name = os.path.basename(__file__)
        os.system("cp %s %s/" % (this_script_name, options.outputfolder) )
        os.system("cp ../tools/shared_utils.py %s/" % options.outputfolder )
                
        submit_files(options.mode, options.outputfolder, options)
        hadd_everything(samples[options.mode], options.outputfolder)                

    else:
        
        print "Full chain..."
        
        os.system("mkdir -p %s" % options.outputfolder)
        os.system("mkdir -p %s_fakerate" % options.outputfolder)
        os.system("mkdir -p %s_kappa" % options.outputfolder)
        
        this_script_name = os.path.basename(__file__)
        os.system("cp %s %s/" % (this_script_name, options.outputfolder) )
        os.system("cp ../tools/shared_utils.py %s/" % options.outputfolder )
        
        outputfolder_fakerate = options.outputfolder + "_fakerate"
        outputfolder_kappa = options.outputfolder + "_kappa"
        rootfile = options.outputfolder + "/fakeratekappa.root"
        
        if os.path.exists(rootfile): os.system("rm " + rootfile)
        cmds_fakerate = submit_files("fakerate", outputfolder_fakerate, options, submit = False)
        cmds_kappa = submit_files("kappa", outputfolder_kappa, options, submit = False)

        print cmds_fakerate[0]
        raw_input()

        GridEngineTools.runParallel(cmds_fakerate + cmds_kappa, options.runmode, "%s_tfactors.condor" % options.outputfolder, confirm=False)
        
        #hadd_everything(samples["fakerate"], outputfolder_fakerate)
        #calculate_ratio("fakerate", rootfile, outputfolder_fakerate, "sr", "fakeSideband", "fakerate")
        #hadd_everything(samples["kappa"], outputfolder_kappa)
        #calculate_ratio("kappa", rootfile, outputfolder_kappa, "sr", "promptSideband", "kappa")
        #os.system("./plot_fakerate.py %s &" % options.outputfolder)
        
        #submit_files("analysis", options.outputfolder, options)
        #hadd_everything(samples["analysis"], options.outputfolder)
        #os.system("./plot_validation.py %s" % options.outputfolder)


def get_signal_region(HT, MHT, NJets, n_btags, MinDeltaPhiMhtJets, n_DT, is_pixel_track, DeDxAverage, n_goodelectrons, n_goodmuons, filename):
  
    is_tracker_track = not is_pixel_track
    dedxcutLow = shared_utils.dedxcutLow
    dedxcutMid = shared_utils.dedxcutMid
    binnumbers = shared_utils.binnumbers

    region = 0
    for binkey in binnumbers:
        if HT >= binkey[0][0] and HT <= binkey[0][1] and \
           MHT >= binkey[1][0] and MHT <= binkey[1][1] and \
           NJets >= binkey[2][0] and NJets <= binkey[2][1] and \
           n_btags >= binkey[3][0] and n_btags <= binkey[3][1] and \
           n_DT >= binkey[4][0] and n_DT <= binkey[4][1] and \
           is_pixel_track >= binkey[5][0] and is_pixel_track <= binkey[5][1] and \
           is_tracker_track >= binkey[6][0] and is_tracker_track <= binkey[6][1] and \
           MinDeltaPhiMhtJets >= binkey[7][0] and MinDeltaPhiMhtJets <= binkey[7][1] and \
           DeDxAverage >= binkey[8][0] and DeDxAverage <= binkey[8][1] and \
           n_goodelectrons >= binkey[9][0] and n_goodelectrons <= binkey[9][1] and \
           n_goodmuons >= binkey[10][0] and n_goodmuons <= binkey[10][1]:
              region = binnumbers[binkey]
              break
    
    if "Run201" in filename:
        # running on data, need to check datastream:
        if "MET" in filename and (n_goodelectrons + n_goodmuons) != 0:
            return 0
        elif "SingleMuon" in filename and (n_goodmuons==0 or n_goodelectrons>0):
            return 0
        elif "SingleElectron" in filename and (n_goodmuons>0 or n_goodelectrons==0):
            return 0
        else:
            return region
    else:
        return region


def get_value(event, variable, i_track, filename):
                        
    if ":" not in variable:
        # for filling a 1D histogram
        if "tracks_" in variable:
            if variable == "tracks_ECaloPt":
                value = event.tracks_matchedCaloEnergy[i_track] / event.tracks_pt[i_track]
            elif variable == "tracks_eta":
                value = eval("abs(event.tracks_eta[%s])" % (i_track))
            else:
                value = eval("event.%s[%s]" % (variable, i_track))
        elif variable == "region":
            value = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, 1, event.tracks_is_pixel_track[i_track], event.tracks_deDxHarmonic2pixel[i_track], event.n_goodelectrons, event.n_goodmuons, filename)
        else:
            value = eval("event.%s" % variable)
        return value
    
    else:
        # for filling a 2D histogram
        if "tracks_" in variable.split(":")[0]:
            xvalue = eval("event.%s[%s]" % (variable.split(":")[0], i_track))
        else:
            xvalue = eval("event.%s" % variable.split(":")[0])
        if "tracks_" in variable.split(":")[1]:
            yvalue = eval("event.%s[%s]" % (variable.split(":")[1], i_track))
        else:
            yvalue = eval("event.%s" % variable.split(":")[1])
        return (xvalue, yvalue)


def getBinContent_with_overflow(histo, xval, yval = False):
    
    print "xval", xval
    
    if not yval:
        # overflow for TH1Fs:
        if xval >= histo.GetXaxis().GetXmax():
            print histo.GetTitle()
            print "Overflow", xval, histo.GetXaxis().GetXmax()
            print "last val:", histo.GetBinContent(histo.GetXaxis().GetNbins()-1)            
            value = histo.GetBinContent(histo.GetXaxis().GetNbins())
            print value
        else:
            value = histo.GetBinContent(histo.GetXaxis().FindBin(xval))
        return value
    else:
        # overflow for TH2Fs:
        if xval >= histo.GetXaxis().GetXmax() and yval < histo.GetYaxis().GetXmax():
            xbins = histo.GetXaxis().GetNbins()
            value = histo.GetBinContent(xbins, histo.GetYaxis().FindBin(yval))
        elif xval < histo.GetXaxis().GetXmax() and yval >= histo.GetYaxis().GetXmax():
            ybins = histo.GetYaxis().GetNbins()
            value = histo.GetBinContent(histo.GetXaxis().FindBin(xval), ybins)
        elif xval >= histo.GetXaxis().GetXmax() or yval >= histo.GetYaxis().GetXmax():
            xbins = histo.GetXaxis().GetNbins()
            ybins = histo.GetYaxis().GetNbins()
            value = histo.GetBinContent(xbins, ybins)
        else:
            value = histo.GetBinContent(histo.GetXaxis().FindBin(xval), histo.GetYaxis().FindBin(yval))
        return value


def fill_histogram(variable, value, histograms, event_selection, data_period, region, weight, scaling):

    h_name = data_period + "_" + variable + "_" + event_selection + "_" + region
    if ":" not in variable:
        histograms[h_name].Fill(value, weight*scaling)    
    else:
        histograms[h_name].Fill(value[0], value[1], weight*scaling)


def event_loop(input_filenames, output_file, outputfolder, mode, event_start, nevents):

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    if "SMS" in input_filenames[0] and "T1qqqq" in input_filenames[0]:
        is_signal = True
        extracuts = signal_cuts
    elif "SMS" in input_filenames[0] and "T2bt" in input_filenames[0]:
        is_signal = True
        extracuts = signal_cuts
    else:
        is_signal = False
        extracuts = {
                      "": "",
                    }

    if "PMSSM" in input_filenames[0]:
        is_pmssm = True
    else:
        is_pmssm = False
        
    for extracut_label in extracuts:

        if "glu" in extracut_label and "T2bt" in input_filenames[0]:
            continue
        elif "stop" in extracut_label and "T1qqqq" in input_filenames[0]:
            continue

        # check if data:
        phase = 0
        data_period = ""
        is_data = False
        filename = input_filenames[0]
        for label in ["Run2016", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18"]:
            if label in filename:
                data_period = label
                if "Run201" in label:
                    is_data = True
                if label == "Run2016" or label == "Summer16":
                    phase = 0
                elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
                    phase = 1
        
        nev = 0
        for tree_file in input_filenames:
            fin = TFile(tree_file)
            h_nev = fin.Get("nev")
            nev += int(h_nev.GetBinContent(1))
            fin.Close()
        
        print "data period: %s, phase: %s, N_ev: %s" % (data_period, phase, nev)
        
        tree = TChain("Events")       
        for i, tree_file in enumerate(input_filenames):
            tree.Add(tree_file)
        
        # construct all histograms:
        histograms = {}
        for variable in variables[mode]:
            for event_selection in event_selections[mode]:
                for region in regions:
                    h_name = data_period + "_" + variable + "_" + event_selection + "_" + region
                    if ":" not in variable:
                        if binnings[mode][variable][0] == "variable":
                            histograms[h_name] = TH1F(h_name, h_name, len(binnings[mode][variable][1:]) - 1, array('d', binnings[mode][variable][1:]) )                    
                        else:
                            histograms[h_name] = TH1F(h_name, h_name, binnings[mode][variable][0], binnings[mode][variable][1], binnings[mode][variable][2])
                    else:
                        histograms[h_name] = TH2F(h_name, h_name, binnings[mode][variable][0], binnings[mode][variable][1], binnings[mode][variable][2], binnings[mode][variable][3], binnings[mode][variable][4], binnings[mode][variable][5])
        
        # speed things up:
        event_selections_converted_notracks = {}
        for event_selection in event_selections[mode]:
            if event_selection == "Baseline":
                # don't change this
                event_selections_converted_notracks[event_selection] = event_selections["analysis"]["Baseline"].replace("and event.tracks_invmass[i_track]>120", "")
            else:
                cutstring = event_selections[mode][event_selection]
                # remove tracks variables:
                cutstring_parts = cutstring.split()
                new_cutstring = ""
                for cutstring_part in cutstring_parts:
                    if "tracks_" not in cutstring_part:
                        new_cutstring += cutstring_part + " "
                for i in range(10):
                    new_cutstring = new_cutstring.replace("and and", "and")
                if new_cutstring.split()[-1] == "and":
                    new_cutstring = " ".join(new_cutstring.split()[:-1])            
                event_selections_converted_notracks[event_selection] = new_cutstring
        
        # Get fakerate and kappa histograms:
        if mode == "analysis":
            tfile_factors = TFile(outputfolder + "/fakeratekappa.root", "open")
            tfactors = {}
            
            for variable in variables["kappa"]:
                tfactors["kappa_%s_short" % variable] = tfile_factors.Get(data_period + "_%s_PromptDY_kappa_short" % variable)
                tfactors["kappa_%s_long" % variable] = tfile_factors.Get(data_period + "_%s_PromptDY_kappa_long" % variable)
                tfactors["kappa_%s_short" % variable].SetDirectory(0)
                tfactors["kappa_%s_long" % variable].SetDirectory(0)
                
            for variable in variables["fakerate"]:
                tfactors["fakerate_%s_short" % variable] = tfile_factors.Get(data_period + "_%s_QCDLowMHT_fakerate_short" % variable)
                tfactors["fakerate_%s_long" % variable] = tfile_factors.Get(data_period + "_%s_QCDLowMHT_fakerate_long" % variable)
                tfactors["fakerate_%s_short" % variable].SetDirectory(0)
                tfactors["fakerate_%s_long" % variable].SetDirectory(0)
            
            tfile_factors.Close()
            
        # implement THnSparse:
        if is_pmssm:
            pMSSMid1_max = 600
            pMSSMid1_low = 0.5
            pMSSMid1_up = pMSSMid1_max + 0.5
            pMSSMid2_max = 144855
            pMSSMid2_low = 0.5
            pMSSMid2_up = pMSSMid2_max + 0.5
            sr_max = 50
            sr_low = 0.5
            sr_up = sr_max + 0.5
            
            bins = np.intc([pMSSMid1_max, pMSSMid2_max, sr_max])
            low = np.float64([pMSSMid1_low, pMSSMid2_low, sr_low])
            high = np.float64([pMSSMid1_up, pMSSMid2_up, sr_up])
            hnsparse = THnSparseS("disappearingtracks", "disappearingtracks", 3, bins, low, high)

        # main event loop:
        nev_tree = tree.GetEntries()
        print "nev_tree", nev_tree
        for iEv, event in enumerate(tree):
        
            if iEv < int(event_start):
                continue
            if int(nevents) > 0 and iEv > int(nevents) + int(event_start):
                break
            
            if (iEv+1) % 100 == 0:
                if int(event_start) < 0:
                    Nstart = iEv
                else:
                    Nstart = int(event_start) + iEv
                if int(event_start) + int(nevents) > nev_tree:
                    Nend = nev_tree
                else:
                    Nend = int(event_start) + int(nevents)
                print "Running %s on %s: %s/%s" % (mode, filename.split("/")[-1], Nstart, Nend)
        
            weight = 1.0
            if not is_data:
                weight = 1.0 * event.CrossSection * event.puWeight / nev
                
            # loop over all event selections:
            for event_selection in event_selections[mode]:
        
                for region in regions:
        
                    if "gen" in region and is_data:
                        continue
                    
                    # this is to speed things up       
                    if not eval(event_selections_converted_notracks[event_selection]):
                        continue
        
                    cutstring = event_selections[mode][event_selection] + " and " + regions[region]
        
                    n_DT = 0
        
                    kappas = []
        
                    values = {}
                    for variable in variables[mode]:
                        values[variable] = []
                    if "tracks_is_pixel_track" not in variables[mode]:
                        values["tracks_is_pixel_track"] = []
                                    
                    # loop over all tracks:
                    for i_track in xrange(len(event.tracks_ptError)):
                            
                        # check signal cut:
                        if is_signal and not eval(extracuts[extracut_label]):
                            continue
                                                                                    
                        if eval(cutstring):
                                                    
                            # save track info....
                            for variable in variables[mode]:
        
                                if variable == "n_tags": continue
        
                                # for event level quantities, fill only once:
                                if "tracks_" not in variable and len(values[variable]) > 0:
                                    continue
        
                                values[variable].append(get_value(event, variable, i_track, filename))
                            
                            if "tracks_is_pixel_track" not in variables[mode]:
                                values["tracks_is_pixel_track"].append(event.tracks_is_pixel_track[i_track])
                            
                            # get fakerate:
                            if mode == "analysis":
                                fakerates = {}
                                for tfactortype in ["fakerate", "kappa"]:
                                    for variable in variables[tfactortype]:
                                        if ":" not in variable:
                                            if "tracks_" in variable:
                                                xval = eval("event.%s[i_track]" % variable)
                                            else:
                                                xval = eval("event.%s" % variable)
                                            fakerates["%s_%s_short" % (tfactortype, variable)] = getBinContent_with_overflow(tfactors["%s_%s_short" % (tfactortype, variable)], xval)
                                            fakerates["%s_%s_long" % (tfactortype, variable)] = getBinContent_with_overflow(tfactors["%s_%s_long" % (tfactortype, variable)], xval)
                                        else:
                                            xval = eval("event.%s" % variable.split(":")[0])
                                            yval = eval("event.%s" % variable.split(":")[1])
                                            fakerates["%s_%s_short" % (tfactortype, variable)] = getBinContent_with_overflow(tfactors["%s_%s_short" % (tfactortype, variable)], xval, yval = yval)
                                            fakerates["%s_%s_long" % (tfactortype, variable)] = getBinContent_with_overflow(tfactors["%s_%s_long" % (tfactortype, variable)], xval, yval = yval)
                            
                            # save kappa:
                            if mode == "analysis" and "prompt" in region:
                                if is_pixel_track:
                                    kappa = getBinContent_with_overflow(tfactors["kappa_tracks_pt_short"], event.tracks_pt[i_track])
                                else:
                                    kappa = getBinContent_with_overflow(tfactors["kappa_tracks_pt_long"], event.tracks_pt[i_track])
                                kappas.append(kappa)
                                
                            # fill THnSparse:
                            if is_pmssm:
                                signal_region = 1            
                                pMSSMid1 = event.SusyMotherMass
                                pMSSMid2 = event.SusyLSPMass
                                coordinates = np.float64([pMSSMid1, pMSSMid2, signal_region])
                                hnsparse.Fill(coordinates, weight)

                            if "Single" in event_selection:
                                # look at only one selected track per event
                                continue
        
                    n_tags = len(values["tracks_is_pixel_track"])
                    if variable == "n_tags":
                        values["n_tags"].append(n_tags)
                    
                    if n_tags == 0: continue
        
                    # Last but not least fill n_tags:
                    values["n_tags"] = [n_tags]
                    event.n_tags = n_tags
        
                    if n_tags>1 and "region" in values:
                        if event.n_goodelectrons == 0 and event.n_goodmuons == 0:
                            values["region"] = [49]
                        if event.n_goodelectrons == 0 and event.n_goodmuons > 0:
                            values["region"] = [50]
                        if event.n_goodelectrons > 0 and event.n_goodmuons > 0:
                            values["region"] = [51]
        
                    for i, is_pixel_track in enumerate(values["tracks_is_pixel_track"]):
                        for variable in variables[mode]:
        
                            if variable == "n_tags" and i>0: continue
        
                            value = values[variable][i]
        
                            scaling = 1.0
                            if mode == "analysis" and "fakeprediction" in region:
                                for fakevariable in variables["fakerate"]:
                                    if fakevariable in region:
                                        if is_pixel_track:
                                            scaling = fakerates["fakerate_%s_short" % fakevariable]
                                        else:
                                            scaling = fakerates["fakerate_%s_long" % fakevariable]
                                        break
        
                                if n_tags > 1:
                                    scaling = fakerate_short * fakerate_long
        
                            #elif mode == "analysis" and "promptpredictionsubtracted" in region:
                            #    scaling = kappas[i]
                            #    if n_tags > 1:
                            #        scaling = kappas[i] * kappas[i]
                            #        
                            #    # subtract fake background: N_ev * kappa - N_ev * FR = N_ev * (kappa - FR)
                            #    if is_pixel_track:
                            #        scaling -= fakerate_short
                            #    else:
                            #        scaling -= fakerate_long
                            #    
                            #    if scaling < 0:
                            #        scaling = 0
        
                            #elif mode == "analysis" and "promptprediction" in region:
                            #    
                            #    for fakevariable in variables["fakerate"]:
                            #        if fakevariable in region:
                            #            if is_pixel_track:
                            #                scaling = kappas[i] * fakerates["fakerate_%s_short" % fakevariable]
                            #            else:
                            #                scaling = kappas[i] * fakerates["fakerate_%s_long" % fakevariable]
                            #            break
                            #    
                            #    #if is_pixel_track:
                            #    #    scaling = kappas[i] * fakerate_short
                            #    #else:
                            #    #    scaling = kappas[i] * fakerate_long
                            #    #elif n_tags > 1:
                            #    #    scaling = kappas[i] * kappas[i] * fakerate_short * fakerate_long
                                    
                            elif mode == "analysis" and "promptprediction" in region:
                                scaling = kappas[i]
                                if n_tags > 1:
                                    scaling = kappas[i] * kappas[i]
        
                            fill_histogram(variable, value, histograms, event_selection, data_period, region, weight, scaling)
                                
        if event_start>0:
            this_output_file = output_file.replace(".root", "_%s.root" % event_start)
            if is_signal:
                this_output_file = this_output_file.replace(".root", "_%s.root" % extracut_label)
        
        fout = TFile(this_output_file, "recreate")
        for h_name in histograms:
            histograms[h_name].Write()

        if is_pmssm:
            hnsparse.Write()

        fout.Close()


if __name__ == "__main__":

    if options.inputfile == "":
        spawn_jobs(options)
    else:
        event_loop([options.inputfile], options.outputfile, options.outputfolder, options.mode, options.event_start, options.nev)
