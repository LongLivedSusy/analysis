#!/bin/env python
from stackedplot import *
from ROOT import *

folder = "output_skim_44_merged"

samples_Summer16 = {
    "DYJetsToLL": {"select": "Summer16.DYJetsToLL", "type": "bg", "color": 62},
    "QCD": {"select": "Summer16.QCD", "type": "bg", "color": 97},
    "WJetsToLNu": {"select": "Summer16.WJetsToLNu", "type": "bg", "color": 85},
    "ZJetsToNuNu": {"select": "Summer16.ZJetsToNuNu_HT", "type": "bg", "color": 67},
    "Diboson": {"select": "Summer16.WW_TuneCUETP8M1|Summer16.WZ_TuneCUETP8M1|Summer16.ZZ_TuneCUETP8M1", "type": "bg", "color": 51},
    "TT": {"select": "Summer16.TTJets_TuneCUETP8M1_13TeV", "type": "bg", "color": 8}, 
    #"signal": {"select": "Signal.S16.g1800_chi1400_27_200970", "type": "sg", "color": kBlue},
    "rare": {"select": "Summer16.ST|Summer16.GJets", "type": "bg", "color": 15},
          }

samples_Fall17 = {
    "DYJetsToLL": {"select": "RunIIFall17MiniAODv2.DYJetsToLL", "type": "bg", "color": 62},
    "QCD": {"select": "RunIIFall17MiniAODv2.QCD", "type": "bg", "color": 97},
    "WJetsToLNu": {"select": "RunIIFall17MiniAODv2.WJetsToLNu", "type": "bg", "color": 85},
    "ZJetsToNuNu": {"select": "RunIIFall17MiniAODv2.ZJetsToNuNu", "type": "bg", "color": 67},
    "Diboson": {"select": "RunIIFall17MiniAODv2.WW|RunIIFall17MiniAODv2.WZ|RunIIFall17MiniAODv2.ZZ", "type": "bg", "color": 51},
    "TT": {"select": "RunIIFall17MiniAODv2.TTJets_Tune|RunIIFall17MiniAODv2.TTJets_HT", "type": "bg", "color": 8}, 
    #"signal": {"select": "Signal.A18.g1800_chi1400_27_200970", "type": "sg", "color": kBlue},
    "rare": {"select": "RunIIFall17MiniAODv2.TTJets_Tune.ST|RunIIFall17MiniAODv2.TTJets_Tune.GJets_HT", "type": "bg", "color": 15},
          }

for year in ['2016']: #, '2017', '2018']:

    for lepton in ['e', 'mu']:

        if year == '2016':
            samples = samples_Summer16
            if lepton == 'mu': samples["data"] = {"select": "Run2016*SingleMuon", "type": "data", "color": kBlack, "lumi": 19177}
            if lepton == 'e':  samples["data"] = {"select": "Run2016*SingleElectron", "type": "data", "color": kBlack, "lumi": 13102}
        elif year == '2017':
            samples = samples_Fall17
            if lepton == 'mu': samples["data"] = {"select": "Run2017*SingleMuon", "type": "data", "color": kBlack, "lumi": 18694}
            if lepton == 'e':  samples["data"] = {"select": "Run2017*SingleElectron", "type": "data", "color": kBlack, "lumi": 24303}
        elif year == '2018':
            samples = samples_Fall17
            if lepton == 'mu': samples["data"] = {"select": "Run2018*SingleMuon", "type": "data", "color": kBlack, "lumi": 32152}
            if lepton == 'e':  continue

        if lepton == 'e':
             variables = {
                      "dilepton_invmass": [20, 81, 101, "passesUniversalSelection==1 && MET<100 && dilepton_CR==1 && dilepton_leptontype==11 && dilepton_pt1>40 && dilepton_pt2>40"],
                      #"madHT": [40, 0, 1000, "madHT>0"],
                         }
	elif lepton == 'mu':
             variables = {
                      "dilepton_invmass": [20, 81, 101, "passesUniversalSelection==1 && MET<100 && dilepton_CR==1 && dilepton_leptontype==13 && dilepton_pt1>40 && dilepton_pt2>40"],
                      #"madHT": [40, 0, 1000, "madHT>0"],
                         }

        for variable in variables:
            histos = get_histograms_from_folder(folder, samples, variable, variables[variable][3], variables[variable][0], variables[variable][1], variables[variable][2])
            stack_histograms(histos, samples, variable, variable, "Events", folder, suffix= "_" + lepton + "_" + year)

