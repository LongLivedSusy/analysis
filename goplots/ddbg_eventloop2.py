#!/bin/env python
from __future__ import division
import __main__ as main
from ROOT import *
from optparse import OptionParser
from array import array
import math, os, glob
import GridEngineTools
import shared_utils
import collections

parser = OptionParser()
parser.add_option("--inputfile", dest = "inputfile", default = "")
parser.add_option("--outputfile", dest = "outputfile")
parser.add_option("--mode", dest = "mode")
parser.add_option("--outputfolder", dest = "outputfolder", default = "ddbg_n3a1")
parser.add_option("--skimfolder", dest = "skimfolder", default = "../ntupleanalyzer/skim_fullC1_merged")
parser.add_option("--dataperiodlabel", dest = "dataperiodlabel", default = "none")
parser.add_option("--nev", dest = "nev", default = -1)
parser.add_option("--jobs_per_file", dest = "jobs_per_file", default = 2)
parser.add_option("--files_per_job", dest = "files_per_job", default = 1)
parser.add_option("--event_start", dest = "event_start", default = 0)
parser.add_option("--runmode", dest = "runmode", default = "multi")
parser.add_option("--debug", dest = "debug", action = "store_true")
parser.add_option("-f", dest = "do_fakerate", action = "store_true")
parser.add_option("-k", dest = "do_kappa", action = "store_true")
parser.add_option("-m", dest = "do_mukappa", action = "store_true")
parser.add_option("-a", dest = "do_analysis", action = "store_true")
parser.add_option("-c", dest = "cleartransferfactor", action = "store_true")
parser.add_option("-s", dest = "submit", action = "store_true")
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
binnings["analysis"]["invmass"] = binnings["analysis"]["InvMass"]
binnings["analysis"]["Ht"] = [5, 0, 2000]
binnings["analysis"]["HT"] = binnings["analysis"]["Ht"]
binnings["analysis"]["Met"] = [20, 0, 600]
binnings["analysis"]["MET"] = binnings["analysis"]["Met"]
binnings["analysis"]["Mht"] = binnings["analysis"]["Met"]
binnings["analysis"]["MHT"] = binnings["analysis"]["Met"]
#binnings["analysis"]["tracks_pt"] = [50, 0, 1000]
binnings["analysis"]["tracks_pt"] = ["variable", 0, 300]
binnings["analysis"]["leadinglepton_pt"] = binnings["analysis"]["Ht"]
binnings["analysis"]["leadinglepton_eta"] = [15, 0, 3]
#binnings["analysis"]["tracks_eta"] = [15, 0, 3]
binnings["analysis"]["tracks_eta"] = ["variable", 0, 1.5, 2.4, 3.0]
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
binnings["analysis"]["tracks_mva_sep21v1_baseline_corrdxydz"] = [ 20, -1, 1]
binnings["analysis"]["Track1MassFromDedx"] = [ 25, 0, 1000]
binnings["analysis"]["Log10DedxMass"] = [10, 0, 5]
binnings["analysis"]["region"] = [54,1,55]
binnings["analysis"]["region"] = binnings["analysis"]["region"]
binnings["analysis"]["tracks_matchedCaloEnergy"] = [25, 0, 50]
binnings["analysis"]["tracks_trkRelIso"] = [20, 0, 0.2]
binnings["analysis"]["tracks_region"] = [54, 1, 55]
binnings["analysis"]["tracks_ECaloPt"] = [25, 0, 1]
binnings["analysis"]["dphiMhtDt"] = [32, 0, 3.2]
binnings["analysis"]["MinDeltaPhiTrackMht"] = [32, 0, 3.2]
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
binnings["analysis"]["tracks_nMissingOuterHits"] = [20, 0, 20]

# override some binnings for transfer factors...
#binnings["fakerate"] = binnings["analysis"].copy()
binnings["fakerate"] = {}
binnings["fakerate"]["tracks_eta"] = ["variable", 0, 1.5, 2.4, 3.0]
#binnings["kappa"] = binnings["analysis"].copy()
binnings["kappa"] = {}
binnings["kappa"]["tracks_pt"] = ["variable", 0, 300]
#binnings["mukappa"] = binnings["analysis"].copy()
binnings["mukappa"] = {}
binnings["mukappa"]["tracks_pt"] = ["variable", 0, 300]

variables = {}
variables["analysis"] = [
                          "HT",
                          "MHT",
                          "n_goodjets",
                          "n_btags",
                          "leadinglepton_mt",
                          "invmass",
                          "tracks_mva_sep21v1_baseline_corrdxydz",
                          "tracks_pt",
                          "tracks_eta",
                          "tracks_deDxHarmonic2pixel",
                          "tracks_matchedCaloEnergy",
                          "tracks_nMissingOuterHits",
                          "n_tags",
                          "region",
                        ]
                      
if False:
    variables["fakerate"] = variables["analysis"]
    variables["kappa"] = variables["analysis"]
    variables["mukappa"] = variables["analysis"]

if True:
    variables["fakerate"] = [
                              "tracks_eta",
                            ]

    variables["kappa"] = [
                              "tracks_pt",
                         ]
    variables["mukappa"] = [
                              "tracks_pt",
                           ]

                                         
categories = [
               "short",
               "long",
             ]

######### event-level cuts #########

event_selections = {}
event_selections["analysis"] = collections.OrderedDict()
event_selections["fakerate"] = collections.OrderedDict()
event_selections["kappa"] = collections.OrderedDict()
event_selections["mukappa"] = collections.OrderedDict()

event_selections["analysis"]["HadBaseline"] =       "event.MHT>30 and \
                                                     event.n_goodjets>=1 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.n_goodelectrons==0 and \
                                                     event.n_goodmuons==0 and \
                                                     event.mtDtMht>20"
event_selections["analysis"]["SMuBaseline"] =       "event.MHT>30 and \
                                                     event.n_goodjets>=1 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.n_goodmuons>=1 and \
                                                     event.n_goodelectrons==0 and \
                                                     event.invmass>140 and \
                                                     event.leadinglepton_mt>110 and \
                                                     event.leadinglepton_pt>40 and \
                                                     event.mtDtMht>20"
event_selections["analysis"]["SElBaseline"] =       "event.MHT>30 and \
                                                     event.n_goodjets>=1 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.n_goodelectrons>=1 and \
                                                     event.invmass>140 and \
                                                     event.leadinglepton_mt>110 and \
                                                     event.leadinglepton_pt>40 and \
                                                     event.mtDtMht>20"

# validation regions:
event_selections["analysis"]["SElValidZLLHighMT"] = "event.MHT>30 and \
                                                     event.n_goodjets>=1 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.n_goodelectrons==1 and \
                                                     event.n_goodmuons==0 and \
                                                     event.invmass>70 and event.invmass<110 and \
                                                     event.leadinglepton_mt>100 and \
                                                     event.leadinglepton_pt>40 and \
                                                     event.mtDtMht>20"
event_selections["analysis"]["SMuValidZLLHighMT"] = "event.MHT>30 and \
                                                     event.n_goodjets>=1 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.n_goodelectrons==0 and \
                                                     event.n_goodmuons==1 and \
                                                     event.invmass>70 and event.invmass<110 and \
                                                     event.leadinglepton_mt>100 and \
                                                     event.leadinglepton_pt>40 and \
                                                     event.mtDtMht>20"
event_selections["analysis"]["SElValidMT"]  =       "event.MHT>30 and \
                                                     event.n_goodjets>=1 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.n_goodelectrons==1 and \
                                                     event.n_goodmuons==0 and \
                                                     event.invmass>140 and \
                                                     event.leadinglepton_mt<100 and \
                                                     event.leadinglepton_pt>40 and \
                                                     event.mtDtMht>20"
event_selections["analysis"]["SMuValidMT"] =        "event.MHT>30 and \
                                                     event.n_goodjets>=1 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.n_goodelectrons==0 and \
                                                     event.n_goodmuons==1 and \
                                                     event.invmass>140 and \
                                                     event.leadinglepton_mt<100 and \
                                                     event.leadinglepton_pt>40 and \
                                                     event.mtDtMht>20"

# transfer factors:
event_selections["fakerate"]["QCDLowMHT"] =         "event.MHT>30 and \
                                                     event.MHT<60 and \
                                                     event.n_goodjets>=1 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.n_goodelectrons==0 and \
                                                     event.n_goodmuons==0 and \
                                                     event.n_btags==0 and \
                                                     event.mtDtMht>20"
event_selections["kappa"]["PromptDYEl"] =           "event.n_goodelectrons==1 and \
                                                     event.n_goodmuons==0 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.leadinglepton_mt<100"
event_selections["mukappa"]["PromptDYMu"] =         "event.n_goodelectrons==0 and \
                                                     event.n_goodmuons==1 and \
                                                     event.MinDeltaPhiMhtJets>0.4 and \
                                                     event.leadinglepton_mt<100"
                                               
# tf measurement regions:
event_selections["analysis"]["QCDLowMHT"] =         event_selections["fakerate"]["QCDLowMHT"]
event_selections["analysis"]["PromptDYEl"] =        event_selections["kappa"]["PromptDYEl"]
event_selections["analysis"]["PromptDYMu"] =        event_selections["mukappa"]["PromptDYMu"]

######### region definitons #########


#       #########################
#       #           #           #
#  Side #     A     #     C     #
#  band #"sideband" #   "CR"    #
#       #           #           #
#       #########################           D_SR = C_CR * TF(B / A)
#  BDT  #           #           #
#  EDep #     B     #     D     #
#  SR   #   "SR"    #   "SR"    #tracks_DrJetDt
#       #           #           #
#       #########################
#          transf.     analysis
#           meas.      baseline
#          DY / QCD      MHT

replacevars = collections.OrderedDict()
replacevars['pixeltrack'] =   'event.tracks_is_pixel_track[i_track]'
replacevars['baseline'] =     'event.tracks_baseline[i_track]'
replacevars['BDT'] =          'event.tracks_mva_sep21v1_baseline_corrdxydz[i_track]'
replacevars['EDep'] =         'event.tracks_matchedCaloEnergy[i_track]'
replacevars['dphiMhtDt'] =    'event.dphiMhtDt'
replacevars['trackp'] =       'event.tracks_p[i_track]'
replacevars['leptonveto'] =   'event.tracks_passleptonveto[i_track]'
replacevars['pfveto'] =       'event.tracks_passPFCandVeto[i_track]'
replacevars['invmass'] =      'event.invmass'
replacevars['DrJetDt'] =      'event.tracks_DrJetDt[i_track]'

baselineShort =             "baseline==1 and pixeltrack==1 and "
baselineLong =              "baseline==1 and pixeltrack==0 and "

if phase == 0:
    SignalShort =           "BDT>0.1 and EDep<15 and DrJetDt>0.2" 
    SignalLong =            "BDT>0.12 and EDep/trackp<0.2 and DrJetDt>0.2" 
    PromptSidebandShort =   "BDT>0.1 and EDep>30 and EDep<300 and DrJetDt>0.1" 
    PromptSidebandLong =    "BDT>0.1 and EDep/trackp>0.30 and EDep/trackp<1.20 and DrJetDt>0.1" 
    PromptSidebandCRShort =  PromptSidebandShort 
    PromptSidebandCRLong =   PromptSidebandLong
    FakeSidebandShort =     "BDT>-0.1 and BDT<-0.05 and EDep<15 and DrJetDt>0.2"   
    FakeSidebandLong =      "BDT>-0.1 and BDT<0.0 and EDep/trackp<0.2 and DrJetDt>0.2"    
    FakeSidebandCRShort =   FakeSidebandShort
    FakeSidebandCRLong =    FakeSidebandLong
else:
    SignalShort =           "BDT>0.15 and EDep<15 and DrJetDt>0.2"          
    SignalLong =            "BDT>0.08 and EDep/trackp<0.2 and DrJetDt>0.2" 
    PromptSidebandShort =   "BDT>0.05 and EDep>30 and EDep<300 and DrJetDt>0.1" 
    PromptSidebandLong =    "BDT>0.08 and EDep/trackp>0.30 and EDep/trackp<1.20 and DrJetDt>0.1" 
    PromptSidebandCRShort =  PromptSidebandShort
    PromptSidebandCRLong =   PromptSidebandLong
    FakeSidebandShort =     "BDT>-0.1 and BDT<0.0 and EDep<15 and DrJetDt>0.2"                 
    FakeSidebandLong =      "BDT>-0.1 and BDT<0.0 and EDep/trackp<0.2 and DrJetDt>0.2"                  
    FakeSidebandCRShort =    FakeSidebandShort               
    FakeSidebandCRLong =     FakeSidebandLong             


regions = collections.OrderedDict()
if options.mode == "kappa":
    regions["sr_short"] = baselineShort + SignalShort + " and dphiMhtDt<3.14/4 and invmass>70 and invmass<105"
    regions["sr_long"] = baselineLong + SignalLong + " and dphiMhtDt<3.14/2 and invmass>75 and invmass<100 and event.MHT>30"
    regions["promptSideband_short"] = baselineShort + PromptSidebandShort + " and dphiMhtDt<3.14/4 and invmass>70 and invmass<105"
    regions["promptSideband_long"] = baselineLong + PromptSidebandLong + " and dphiMhtDt<3.14/2 and invmass>75 and invmass<100 and event.MHT>30"
elif options.mode == "mukappa":
    regions["sr_short"] = "pixeltrack==1 and baseline==0 and " + SignalShort + " and dphiMhtDt<3.14/4 and invmass>70 and invmass<105 and event.MHT>30"
    regions["sr_long"] = "pixeltrack==0 and baseline==0 and " + SignalLong + " and dphiMhtDt<3.14/2 and invmass>75 and invmass<100"
    regions["promptSideband_short"] = "pixeltrack==1 and " + PromptSidebandShort + " and dphiMhtDt<3.14/4 and invmass>70 and invmass<105 and event.MHT>30"
    regions["promptSideband_long"] = "pixeltrack==0 and " + PromptSidebandLong + " and dphiMhtDt<3.14/2 and invmass>75 and invmass<100"
elif options.mode == "fakerate":
    regions["sr_short"] = baselineShort + SignalShort
    regions["sr_long"] = baselineLong + SignalLong
    regions["fakeSideband_short"] = baselineShort + FakeSidebandShort
    regions["fakeSideband_long"] = baselineLong + FakeSidebandLong    
else:
    regions["sr_short"] = baselineShort + SignalShort
    regions["sr_long"] = baselineLong + SignalLong
    regions["sr"] = "(%s) or (%s)" % (SignalShort, SignalLong)
    regions["promptSideband_short"] = baselineShort + PromptSidebandShort
    regions["promptSideband_long"] = baselineLong + PromptSidebandLong
    regions["fakeSideband_short"] = baselineShort + FakeSidebandShort
    regions["fakeSideband_long"] = baselineLong + FakeSidebandLong
    regions["promptcr_short"] = baselineShort + PromptSidebandCRShort
    regions["promptcr_long"] = baselineLong + PromptSidebandCRLong
    regions["fakecr_short"] = baselineShort + FakeSidebandCRShort
    regions["fakecr_long"] = baselineLong + FakeSidebandCRLong

    for kappa_variable in variables["kappa"]:
        regions["promptprediction_%s_short" % kappa_variable] = regions["promptcr_short"]
        regions["promptprediction_%s_long" % kappa_variable] = regions["promptcr_long"]
    for kappa_variable in variables["mukappa"]:
        regions["mupromptprediction_%s_short" % kappa_variable] = regions["promptcr_short"]
        regions["mupromptprediction_%s_long" % kappa_variable] = regions["promptcr_long"]
    for fakerate_variable in variables["fakerate"]:
        regions["fakeprediction_%s_short" % fakerate_variable] = regions["fakecr_short"]
        regions["fakeprediction_%s_long" % fakerate_variable] = regions["fakecr_long"]

########## add genfake and genprompt info to all regions #########
for regionlabel in regions.keys():

    for shortvar in replacevars:
        regions[regionlabel] = regions[regionlabel].replace(shortvar, replacevars[shortvar])

    #regions[regionlabel.replace("_short", "_genfake_short").replace("_long", "_genfake_long")] = regions[regionlabel] + " and event.tracks_fake[i_track]==1"
    #regions[regionlabel.replace("_short", "_genprompt_short").replace("_long", "_genprompt_long")] = regions[regionlabel] + " and event.tracks_fake[i_track]==0"

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
            "Fall17": mc_fall17,
            "Run2016": ["Run2016*JetHT*root"],
            #"Run2017": ["Run2017*JetHT*root"],
            #"Run2018": ["Run2018*JetHT*root"],
            "Run20172018": ["Run2017*JetHT*root", "Run2018*JetHT*root"],
            #"Run2": ["Run2016*JetHT*root", "Run2017*JetHT*root", "Run2018*JetHT*root"],
            #"Run2018": ["Run2018*JetHT*root"],
          }
samples["kappa"] = {
            "Summer16": mc_summer16,
            "Fall17": mc_fall17,
            "Run2016": ["Run2016*SingleElectron*root"],
            #"Run2017": ["Run2017*SingleElectron*root"],
            #"Run2018": ["Run2018*EGamma*root"],
            "Run20172018": ["Run2017*SingleElectron*root", "Run2018*EGamma*root"],
            #"Run2": ["Run2016*SingleElectron*root", "Run2017*SingleElectron*root", "Run2018*EGamma*root"],
            #"Run2018": ["Run2018*EGamma*root"],
          }
samples["mukappa"] = {
            "Summer16": mc_summer16,
            "Fall17": mc_fall17,
            "Run2016": ["Run2016*SingleMuon*root"],
            #"Run2017": ["Run2017*SingleMuon*root"],
            #"Run2018": ["Run2018*SingleMuon*root"],
            "Run20172018": ["Run2017*SingleMuon*root", "Run2018*SingleMuon*root"],
            #"Run2": ["Run2016*SingleMuon*root", "Run2017*SingleMuon*root", "Run2018*SingleMuon*root"],
            #"Run2018": ["Run2018*SingleMuon*root"],
          }
samples["analysis"] = {
            "Summer16": mc_summer16,
            "Fall17": mc_fall17,
            #"T1qqqq16": ["RunIISummer16MiniAODv3.SMS-T1qqqq*root"],
            #"T2bt16": ["RunIISummer16MiniAODv3.SMS-T2bt*root"],
            #"T1qqqq17": ["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq*root"],

            "Run2016MET": ["Run2016*MET*root"],
            "Run2016SingleElectron": ["Run2016*SingleElectron*root"],
            "Run2016SingleMuon": ["Run2016*SingleMuon*root"],

            "Run2017MET": ["Run2017*MET*root"],
            "Run2017SingleElectron": ["Run2017*SingleElectron*root"],
            "Run2017SingleMuon": ["Run2017*SingleMuon*root"],

            "Run2018MET": ["Run2018*MET*root"],
            "Run2018SingleElectron": ["Run2018*EGamma*root"],
            "Run2018SingleMuon": ["Run2018*SingleMuon*root"],
          }

signal_cuts = {
               "pooled": "event.tracks_chiCandGenMatchingDR[i_track]<0.01",
               #"glu2000_lsp1000": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_gluino_mass==2000 and event.signal_lsp_mass==1000",
               #"glu2000_lsp1975": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_gluino_mass==2000 and event.signal_lsp_mass==1975",
               #"glu2700_lsp1700": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_gluino_mass==2700 and event.signal_lsp_mass==1700",
               #"glu2700_lsp2672": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_gluino_mass==2700 and event.signal_lsp_mass==2672",
               #"stop2000_lsp1000": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_stop_mass==2000 and event.signal_lsp_mass==1000",
               #"stop2000_lsp1900": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_stop_mass==2000 and event.signal_lsp_mass==1900",
               #"stop2500_lsp1500": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_stop_mass==2500 and event.signal_lsp_mass==1500",
               #"stop2500_lsp2000": "event.tracks_chiCandGenMatchingDR[i_track]<0.01 and event.signal_stop_mass==2500 and event.signal_lsp_mass==2000",
            }


def calculate_ratio(mode, rootfile, path, numerator_label, denominator_label, ratio_label):
    
    for variable in variables[mode]:
        for run_period in samples[mode]:
            for event_selection in event_selections[mode]:
                for category in categories:
                    
                    tfile_merged = TFile(path + "/merged_%s.root" % run_period, "read")
                    print "get", run_period + "_" + variable + "_" + event_selection + "_" + numerator_label + "_" + category, "from", path + "/merged_%s.root" % run_period
                    fakes_numerator = tfile_merged.Get(run_period + "_" + variable + "_" + event_selection + "_" + numerator_label + "_" + category)
                    fakes_numerator.SetDirectory(0)
                    print "get", run_period + "_" + variable + "_" + event_selection + "_" + denominator_label + "_" + category, "from", path + "/merged_%s.root" % run_period
                    fakes_denominator = tfile_merged.Get(run_period + "_" + variable + "_" + event_selection + "_" + denominator_label + "_" + category)
                    fakes_denominator.SetDirectory(0)
                    tfile_merged.Close()

                    tfile_fakerate = TFile(rootfile, "update")
                    fakes_numerator.Write()
                    fakes_denominator.Write()
                    fakerate = fakes_numerator.Clone()
                    fakerate.SetName(fakerate.GetName().replace("_" + numerator_label + "_", "_" + ratio_label + "_"))
                    fakerate.Divide(fakes_denominator)
                    
                    print "%s, ratio = (%s, %s, %s)" % (category, fakerate.GetBinContent(1), fakerate.GetBinContent(2), fakerate.GetBinContent(3))
                    
                    fakerate.Write()
                    tfile_fakerate.Close()


def hadd_everything(samples, outputfolder):
    
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
            
            command = "hadd -f -k %s/merged_%s%s.root " % (outputfolder, data_period, extracut_label)
            for sample in samples[data_period]:
                command += "%s/%s " % (outputfolder, data_period + "*" + sample.replace("*root", "*%s*root" % extracut_label))
            commands.append(command)
        
    GridEngineTools.runParallel(commands, "multi", confirm=False)


def submit_files(mode, outputfolder, options, submit = True):

    this_script_name = os.path.basename(__file__)

    inputfiles_dataperiods = []
    inputfiles = []
    for data_period in samples[mode]:
        for sample in samples[mode][data_period]:
            if options.debug:
                globlist = glob.glob(options.skimfolder + "/" + sample)[0:1]
                inputfiles += globlist
                for i in range(len(globlist)):
                    inputfiles_dataperiods += [data_period]
            else:
                globlist = glob.glob(options.skimfolder + "/" + sample)
                inputfiles += globlist
                for i in range(len(globlist)):
                    inputfiles_dataperiods += [data_period]
    commands = []

    print "inputfiles", inputfiles

    for i, inputfile in enumerate(inputfiles):

        inputfiles_dataperiod = inputfiles_dataperiods[i]

        print(inputfile)
        if options.jobs_per_file>1:
            try:
                fin = TFile(inputfile)
                tree = fin.Get("Events")
                nev = tree.GetEntries()
                fin.Close()
                if nev>0 and int(nev/options.jobs_per_file)>0:
                    for iStart in range(0, nev, int(nev/options.jobs_per_file)):
                        cmd = "./%s/%s --outputfolder %s --inputfile %s --outputfile %s --mode %s --event_start %s --nev %s --dataperiodlabel %s; " % (options.outputfolder, this_script_name, outputfolder, inputfile, outputfolder + "/" + inputfiles_dataperiod + "_" + inputfile.split("/")[-1], mode, iStart, int(nev/options.jobs_per_file), inputfiles_dataperiod)
                        commands.append(cmd)
            except:
                print "@@@ issue w/ file:", inputfile
        else:
            cmd = "./%s/%s --outputfolder %s --inputfile %s --outputfile %s --mode %s --dataperiodlabel %s; " % (options.outputfolder, this_script_name, outputfolder, inputfile, outputfolder + "/" + inputfiles_dataperiod + "_" + inputfile.split("/")[-1], mode, inputfiles_dataperiod)
            commands.append(cmd)
            
    if options.files_per_job>1:
        old_commands = list(commands)
        commands = []
        for chunk in chunks(old_commands, options.files_per_job):
            commands.append(" ".join(chunk))

    if submit:
        print(commands[0])
        print("Running %s jobs..." % len(commands))
        raw_input("Submit?")
        GridEngineTools.runParallel(commands, options.runmode, "%s.condor" % outputfolder, confirm=False)

    return commands
            

def spawn_jobs(options):
            
    if options.do_fakerate:
        print "Doing fakerate"
    if options.do_kappa:
        print "Doing kappa"
    if options.do_mukappa:
        print "Doing mukappa"
    if options.do_analysis:
        print "Doing analysis"

    os.system("mkdir -p %s" % options.outputfolder)
    os.system("mkdir -p %s_fakerate" % options.outputfolder)
    os.system("mkdir -p %s_kappa" % options.outputfolder)
    os.system("mkdir -p %s_mukappa" % options.outputfolder)
    
    this_script_name = os.path.basename(__file__)
    os.system("cp %s %s/" % (this_script_name, options.outputfolder) )
    os.system("cp ../tools/shared_utils.py %s/" % options.outputfolder )
    
    outputfolder_fakerate = options.outputfolder + "_fakerate"
    outputfolder_kappa = options.outputfolder + "_kappa"
    outputfolder_mukappa = options.outputfolder + "_mukappa"
    rootfile = options.outputfolder + "/fakeratekappa.root"

    cmds = []
    if options.do_fakerate:
        cmds += submit_files("fakerate", outputfolder_fakerate, options, submit = False)
    if options.do_kappa:
        cmds += submit_files("kappa", outputfolder_kappa, options, submit = False)
    if options.do_mukappa:
        cmds += submit_files("mukappa", outputfolder_mukappa, options, submit = False)

    if options.do_fakerate or options.do_kappa or options.do_mukappa:
        GridEngineTools.runParallel(cmds, options.runmode, "%s_tfactors.condor" % options.outputfolder, confirm = True)

    if options.cleartransferfactor:
            if os.path.exists(rootfile):
                os.system("rm " + rootfile)

    if options.do_fakerate or options.do_kappa or options.do_mukappa:

        print "Fakerate"
        hadd_everything(samples["fakerate"], outputfolder_fakerate)
        calculate_ratio("fakerate", rootfile, outputfolder_fakerate, "sr", "fakeSideband", "fakerate")

        print "Kappa"
        hadd_everything(samples["kappa"], outputfolder_kappa)
        calculate_ratio("kappa", rootfile, outputfolder_kappa, "sr", "promptSideband", "kappa")

        print "Mukappa"
        hadd_everything(samples["mukappa"], outputfolder_mukappa)
        calculate_ratio("mukappa", rootfile, outputfolder_mukappa, "sr", "promptSideband", "mukappa")

    if options.do_analysis:
        submit_files("analysis", options.outputfolder, options, submit = True)
        hadd_everything(samples["analysis"], options.outputfolder)
        os.system("cd %s; hadd -f merged_Run2MET.root merged_Run2016MET.root merged_Run2017MET.root merged_Run2018MET.root" % options.outputfolder)
        os.system("cd %s; hadd -f merged_Run2SingleMuon.root merged_Run2016SingleMuon.root merged_Run2017SingleMuon.root merged_Run2018SingleMuon.root" % options.outputfolder)
        os.system("cd %s; hadd -f merged_Run2SingleElectron.root merged_Run2016SingleElectron.root merged_Run2017SingleElectron.root merged_Run2018SingleElectron.root" % options.outputfolder)


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
        
    value = -1
        
    if not yval:
        if xval >= histo.GetXaxis().GetXmax():
            value = histo.GetBinContent(histo.GetXaxis().GetNbins())
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
    elif variable == "region" and value == 51:
        histograms[h_name].Fill(value[0], value[1], weight*scaling*scaling)
    else:
        histograms[h_name].Fill(value[0], value[1], weight*scaling)


def event_loop(input_filenames, output_file, outputfolder, mode, event_start, nevents, dataperiodlabel):

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    if "SMS" in input_filenames[0]:
        is_signal = True
    else:
        is_signal = False
       
    # check if data:
    phase = 0
    data_period = ""
    is_data = False
    filename = input_filenames[0]
    for label in ["Run2016", "Run20172018", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18"]:
        if label in filename:
            data_period = label
            if "Run201" in label:
                is_data = True
            if label == "Run2016" or label == "Summer16":
                phase = 0
            elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18" or label == "Run20172018":
                phase = 1
   
    if dataperiodlabel == "none":
        dataperiodlabel = data_period

    nev = 0
    nev_puweighted = 0
    for i, tree_file in enumerate(input_filenames):
                
        print "Loading %s" % tree_file
            
        fin = TFile(tree_file)
    
        # get nev count:
        h_nev = fin.Get("nev")
        nev += int(h_nev.GetBinContent(1))
        #nev_puweighted += float(h_nev.GetBinContent(2))

        fin.Close()
    
    print("data period: %s, phase: %s, N_ev: %s" % (dataperiodlabel, phase, nev))
    
    tree = TChain("Events")       
    for i, tree_file in enumerate(input_filenames):
        tree.Add(tree_file)
    
    # construct all histograms:
    histograms = {}
    for variable in variables[mode]:
        for event_selection in event_selections[mode]:
            for region in regions:
                h_name = dataperiodlabel + "_" + variable + "_" + event_selection + "_" + region
                if ":" not in variable:
                    if binnings[mode][variable][0] == "variable":
                        histograms[h_name] = TH1F(h_name, h_name, len(binnings[mode][variable][1:]) - 1, array('d', binnings[mode][variable][1:]) )
                    else:
                        histograms[h_name] = TH1F(h_name, h_name, binnings[mode][variable][0], binnings[mode][variable][1], binnings[mode][variable][2])
                else:
                    histograms[h_name] = TH2F(h_name, h_name, binnings[mode][variable][0], binnings[mode][variable][1], binnings[mode][variable][2], binnings[mode][variable][3], binnings[mode][variable][4], binnings[mode][variable][5])
    
    # Get fakerate and kappa histograms:
    if mode == "analysis":
        tfile_factors = TFile(outputfolder + "/fakeratekappa.root", "open")
        tfactors = {}
        
        if is_data:
            if phase == 0:
                tfdataperiodlabel = "Run2016"
            elif phase == 1:
                tfdataperiodlabel = "Run20172018"
        else:
            if phase == 0:
                tfdataperiodlabel = "Summer16"
            elif phase == 1:
                tfdataperiodlabel = "Fall17"
        
        for variable in variables["kappa"]:
            tfactors["kappa_%s_short" % variable] = tfile_factors.Get(tfdataperiodlabel + "_%s_PromptDYEl_kappa_short" % variable)
            tfactors["kappa_%s_long" % variable] = tfile_factors.Get(tfdataperiodlabel + "_%s_PromptDYEl_kappa_long" % variable)
            tfactors["kappa_%s_short" % variable].SetDirectory(0)
            tfactors["kappa_%s_long" % variable].SetDirectory(0)
            
        for variable in variables["mukappa"]:
            tfactors["mukappa_%s_short" % variable] = tfile_factors.Get(tfdataperiodlabel + "_%s_PromptDYMu_mukappa_short" % variable)
            tfactors["mukappa_%s_long" % variable] = tfile_factors.Get(tfdataperiodlabel + "_%s_PromptDYMu_mukappa_long" % variable)
            tfactors["mukappa_%s_short" % variable].SetDirectory(0)
            tfactors["mukappa_%s_long" % variable].SetDirectory(0)

        for variable in variables["fakerate"]:
            tfactors["fakerate_%s_short" % variable] = tfile_factors.Get(tfdataperiodlabel + "_%s_QCDLowMHT_fakerate_short" % variable)
            tfactors["fakerate_%s_long" % variable] = tfile_factors.Get(tfdataperiodlabel + "_%s_QCDLowMHT_fakerate_long" % variable)
            tfactors["fakerate_%s_short" % variable].SetDirectory(0)
            tfactors["fakerate_%s_long" % variable].SetDirectory(0)
        
        tfile_factors.Close()
        print "Loaded fakeratekappa.root"
    
    # main event loop:
    nev_tree = tree.GetEntries()
    print("nev_tree", nev_tree)
    for iEv, event in enumerate(tree):
    
        if iEv < int(event_start):
            continue
        if int(nevents) > 0 and iEv > int(nevents) + int(event_start):
            break
        
        if (iEv+1) % 1000 == 0:
            if int(event_start) < 0:
                Nstart = iEv
            else:
                Nstart = int(event_start) + iEv
            if int(event_start) + int(nevents) > nev_tree:
                Nend = nev_tree
            else:
                Nend = int(event_start) + int(nevents)
            print("Running %s on %s: %s/%s" % (mode, filename.split("/")[-1], Nstart, Nend))
    
        weight = 1.0
        if not is_data:
            weight = 1.0 * event.CrossSection * event.puWeight / nev
            
        # loop over all event selections:
        for event_selection in event_selections[mode]:

            # loop over all regions (ABCD, SR, CRs) 
            for region in regions:
    
                if "gen" in region and is_data:
                    continue
                   
                cutstring = event_selections[mode][event_selection] + " and " + regions[region]
                n_tags = 0
                values = collections.OrderedDict()               
                for variable in variables[mode]:
                    values[variable] = []
                values["mukappa"] = []
                values["kappa"] = []
                values["theta"] = []
                                
                # loop over all tracks:
                for i_track in range(len(event.tracks_ptError)):
                    
                    # check chargino matching:
                    if is_signal and not eval(event.tracks_chiCandGenMatchingDR[i_track]<0.01):
                        continue
                            
                    #print "cutstring", cutstring
                    if eval(cutstring):
                                                                             
                        # save this track:
                        for variable in variables[mode]:
                    
                            if variable == "n_tags" or variable == "kappa" or variable == "theta" or variable == "mukappa":
                                continue
                    
                            # for event level quantities, fill only once:
                            if "tracks_" not in variable and len(values[variable]) > 0:
                                continue
                    
                            values[variable].append(get_value(event, variable, i_track, filename))

                        n_tags += 1
                                                
                        # get transfer factors:
                        if mode == "analysis":
                        
                            is_pixel_track = bool(event.tracks_is_pixel_track[i_track])
    
                            # get kappa:
                            if "prompt" in region:
                                if is_pixel_track:
                                    kappa = getBinContent_with_overflow(tfactors["kappa_tracks_pt_short"], event.tracks_pt[i_track])
                                else:
                                    kappa = getBinContent_with_overflow(tfactors["kappa_tracks_pt_long"], event.tracks_pt[i_track])
                                values["kappa"].append(kappa)

                                if is_pixel_track:
                                    mukappa = getBinContent_with_overflow(tfactors["mukappa_tracks_pt_short"], event.tracks_pt[i_track])
                                else:
                                    mukappa = getBinContent_with_overflow(tfactors["mukappa_tracks_pt_long"], event.tracks_pt[i_track])
                                values["mukappa"].append(mukappa)

                            # get theta:
                            if "fake" in region:
                                if is_pixel_track:
                                    theta = getBinContent_with_overflow(tfactors["fakerate_tracks_eta_short"], event.tracks_eta[i_track])
                                else:
                                    theta = getBinContent_with_overflow(tfactors["fakerate_tracks_eta_long"], event.tracks_eta[i_track])
                                values["theta"].append(theta)

                if n_tags == 0:
                    continue
                                                
                event.n_tags = n_tags
                if variables[mode] == n_tags:
                    values["n_tags"] = [n_tags]               

                if n_tags > 1:
                    message = ""
                    for i in enumerate(values[values.keys()[0]]):
                        message += "%s " % values["tracks_pt"]
                    print "**** n_tags=%s, tracks_pt = %s" % (n_tags, message)
                                
                for variable in variables[mode]:

                    if variable == "kappa" or variable == "mukappa" or variable == "theta":
                        continue

                    # back on event level. Fill histograms:
                    for i in range(len(values[variable])):
               
                        value = values[variable][i]

                        if "tracks_" in variable:
                            idx = i
                        else:
                            idx = 0
               
                        if mode == "analysis" and "fakeprediction" in region:
                            scaling = values["theta"][idx]
                        elif mode == "analysis" and "mupromptprediction" in region:
                            scaling = values["mukappa"][idx]
                        elif mode == "analysis" and "promptprediction" in region:
                            scaling = values["kappa"][idx]
                        else:
                            scaling = 1.0
                
                        #if "prediction" in region:
                        #    print region, scaling

                        # FastSim weight: apply for displacements < 30 cm
                        if event.tracks_chiLabXY[i_track]>-1 and event.tracks_chiLabXY[i_track]<300:
                            weight_final = 0.75 * weight
                        else:
                            weight_final = weight

                        # TODO apply 90% trigger efficiency:
                        # if not is_data and n_goodleptons>0:
                        #    weight *= 0.9

                        fill_histogram(variable, value, histograms, event_selection, dataperiodlabel, region, weight_final, scaling)
                            
    if event_start>0:
        this_output_file = output_file.replace(".root", "_%s.root" % event_start)
    else:
        this_output_file = output_file
    
    fout = TFile(this_output_file, "recreate")
    for h_name in histograms:
        histograms[h_name].Write()

    fout.Close()


if __name__ == "__main__":

    if options.inputfile == "":
        spawn_jobs(options)
    else:
        event_loop(
                    [options.inputfile],
                    options.outputfile,
                    options.outputfolder,
                    options.mode,
                    options.event_start,
                    options.nev,
                    options.dataperiodlabel
                   )
