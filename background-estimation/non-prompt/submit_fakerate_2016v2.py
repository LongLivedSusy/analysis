#!/bin/env python
from submit import *

cmssw8_samples = [
                    "Summer16.WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-200To400_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-600To800_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
                    "Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
                    "Summer16.WW_TuneCUETP8M1_13TeV-pythia8",
                    "Summer16.ZZ_TuneCUETP8M1_13TeV-pythia8",
                    "Summer16.WZ_TuneCUETP8M1_13TeV-pythia8",
                    "Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                    "Run2016B-03Feb2017_ver2-v2.SingleElectron",
                    "Run2016C-03Feb2017-v1.SingleElectron",
                    "Run2016D-03Feb2017-v1.SingleElectron",
                    "Run2016E-03Feb2017-v1.SingleElectron",
                    "Run2016F-03Feb2017-v1.SingleElectron",
                    "Run2016G-03Feb2017-v1.SingleElectron",
                    "Run2016H-03Feb2017_ver2-v1.SingleElectron",
                    "Run2016B-03Feb2017_ver2-v2.SingleMuon",
                    "Run2016C-03Feb2017-v1.SingleMuon",
                    "Run2016D-03Feb2017-v1.SingleMuon",
                    "Run2016E-03Feb2017-v1.SingleMuon",
                    "Run2016F-03Feb2017-v1.SingleMuon",
                    "Run2016G-03Feb2017-v1.SingleMuon",
                    "Run2016H-03Feb2017_ver2-v1.SingleMuon",
                 ]

cmssw9_samples = [
                    "Run2016C-17Jul2018-v1.JetHT",
                    "Run2016E-17Jul2018-v1.JetHT",
                    "Run2016F-17Jul2018-v1.JetHT",
                    "Run2016G-17Jul2018-v1.JetHT",
                    "Run2016H-17Jul2018-v1.JetHT",
                 ]

command = "./looper.py $INPUT $OUTPUT 0 0"
output_folder = "output_fakerate_2016v2_sideband"
commands = []
commands += prepare_command_list("/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2", cmssw8_samples, output_folder, command = command, files_per_job = 10)
commands += prepare_command_list("/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v2", cmssw9_samples, output_folder, command = command, files_per_job = 10)

do_submission(commands, output_folder)
