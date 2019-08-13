#!/bin/env python
from stackedplot import *
from ROOT import *

folder = "output_skim_11_merged"

samples_Summer16 = {
    "DYJetsToLL": {"select": "Summer16.DYJetsToLL", "type": "bg", "color": 62},
    "QCD": {"select": "Summer16.QCD", "type": "bg", "color": 97},
    "WJetsToLNu": {"select": "Summer16.WJetsToLNu", "type": "bg", "color": 85},
    "ZJetsToNuNu": {"select": "Summer16.ZJetsToNuNu_HT", "type": "bg", "color": 67},
    "Diboson": {"select": "Summer16.WW_TuneCUETP8M1|Summer16.WZ_TuneCUETP8M1|Summer16.ZZ_TuneCUETP8M1", "type": "bg", "color": 51},
    "TT": {"select": "Summer16.TTJets_TuneCUETP8M1_13TeV", "type": "bg", "color": 8}, 
    "Signal": {"select": "Summer16.g1800_chi1400_27_200970", "type": "sg", "color": kBlue},
    #"Rare": {"select": "Summer16.ST|Summer16.GJets", "type": "bg", "color": 15},
    #"Data": {"select": "Run2016*MET", "type": "data", "lumi": 26216, "color": kBlack},
          }

signal_region = "passesUniversalSelection==1 && MHT>250 && MinDeltaPhiMhtJets>0.3 && n_jets>0 && n_leptons==0 && tracks_is_reco_lepton==0 "

variables = {
              "log10(tracks_massfromdeDxStrips)": [50, 0, 5, signal_region],
              "log10(tracks_massfromdeDxPixel)": [50, 0, 5, signal_region],
              #"tracks_dxyVtx": [30, 0, 0.03, signal_region],
            }

cuts = {
          #"_Summer16_short_tight": [samples_Summer16, " && tracks_is_pixel_track==1 && tracks_mva_bdt>0.1"],
          #"_Summer16_long_tight": [samples_Summer16, " && tracks_is_pixel_track==0 && tracks_mva_bdt>0.25"],
          #"_Summer16_short_loose": [samples_Summer16, " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>0 && tracks_dxyVtx<=0.01"],
          #"_Summer16_long_loose": [samples_Summer16, " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>0 && tracks_dxyVtx<=0.01"],
          #"_Summer16_short_loose_dxy002": [samples_Summer16, " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>0 && tracks_dxyVtx<=0.02"],
          #"_Summer16_long_loose_dxy002": [samples_Summer16, " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>0 && tracks_dxyVtx<=0.02"],
          "_Summer16_short_loose": [samples_Summer16, " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>0"],
          "_Summer16_long_loose": [samples_Summer16, " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>0"],
       }

for label in cuts:
    for variable in variables:        
        samples = cuts[label][0]
        mycuts = variables[variable][3] + cuts[label][1]
              
        if "deDxStrips" in variable and "long" not in label: continue
        if "deDxPixel" in variable and "short" not in label: continue
         
        histos = get_histograms_from_folder(folder, samples, variable, mycuts, variables[variable][0], variables[variable][1], variables[variable][2], threads=12, numevents=-1)    
        stack_histograms(histos, samples, variable, variable, "Events", folder, suffix=variable + label, lumi=26216, logx=False, ymax=10e4, ymin=10e-3)
