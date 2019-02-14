#!/bin/env python
from submit import *

# configured with:
#   - 2016v2 data/MC ntuples for 2016
#   - Run2v2 data/MC ntuples for 2017/18

Run2016_ntuples_2016v2 = [
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
                    #"Run2016B-03Feb2017_ver2-v2.SingleElectron",
                    #"Run2016C-03Feb2017-v1.SingleElectron",
                    #"Run2016D-03Feb2017-v1.SingleElectron",
                    #"Run2016E-03Feb2017-v1.SingleElectron",
                    #"Run2016F-03Feb2017-v1.SingleElectron",
                    #"Run2016G-03Feb2017-v1.SingleElectron",
                    #"Run2016H-03Feb2017_ver2-v1.SingleElectron",
                    #"Run2016B-03Feb2017_ver2-v2.SingleMuon",
                    #"Run2016C-03Feb2017-v1.SingleMuon",
                    #"Run2016D-03Feb2017-v1.SingleMuon",
                    #"Run2016E-03Feb2017-v1.SingleMuon",
                    #"Run2016F-03Feb2017-v1.SingleMuon",
                    #"Run2016G-03Feb2017-v1.SingleMuon",
                    #"Run2016H-03Feb2017_ver2-v1.SingleMuon",
                    #"Run2016B-03Feb2017_ver2-v2.MET",
                    #"Run2016C-03Feb2017-v1.MET",
                    #"Run2016D-03Feb2017-v1.MET",
                    #"Run2016E-03Feb2017-v1.MET",
                    #"Run2016F-03Feb2017-v1.MET",
                    #"Run2016G-03Feb2017-v1.MET",
                    #"Run2016H-03Feb2017_ver2-v1.MET",
                 ]

Run20172018_ntuples = [
                    #"ProductionRun2v2Run2017B-31Mar2018-v1.JetHT",
                    "ProductionRun2v2Run2017B-31Mar2018-v1.MET",
                    "ProductionRun2v2Run2017B-31Mar2018-v1.SingleElectron",
                    "ProductionRun2v2Run2017B-31Mar2018-v1.SingleMuon",
                    #"ProductionRun2v2Run2017C-31Mar2018-v1.JetHT",
                    "ProductionRun2v2Run2017C-31Mar2018-v1.MET",
                    "ProductionRun2v2Run2017C-31Mar2018-v1.SingleElectron",
                    "ProductionRun2v2Run2017C-31Mar2018-v1.SingleMuon",
                    #"ProductionRun2v2Run2017D-31Mar2018-v1.JetHT",
                    "ProductionRun2v2Run2017D-31Mar2018-v1.MET",
                    #"ProductionRun2v2Run2017E-31Mar2018-v1.JetHT",
                    #"ProductionRun2v2Run2017F-31Mar2018-v1.JetHT",
                    "ProductionRun2v2Run2017F-31Mar2018-v1.MET",
                    #"Run2018A-17Sep2018-v1.JetHT",
                    "Run2018A-17Sep2018-v1.MET",
                    "Run2018A-17Sep2018-v1.SingleMuon",
                    #"Run2018B-17Sep2018-v1.JetHT",
                    "Run2018B-17Sep2018-v1.MET",
                    "Run2018B-17Sep2018-v1.SingleMuon",
                    #"Run2018C-17Sep2018-v1.JetHT",
                    "Run2018C-17Sep2018-v1.MET",
                    "Run2018C-17Sep2018-v1.SingleMuon",
                    "ProductionRun2v2RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8_ext1",
                    "ProductionRun2v2RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_ext1",
                    "ProductionRun2v2RunIIFall17MiniAODv2.QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_PSweights_13TeV-powheg-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_ext1",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTGamma_Dilept_TuneCP5_PSweights_13TeV_madgraph_pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTGamma_SingleLeptFromT_TuneCP5_PSweights_13TeV_madgraph_pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTGamma_SingleLeptFromTbar_TuneCP5_PSweights_13TeV_madgraph_pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTHH_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTTW_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTWH_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTWZ_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTZH_TuneCP5_13TeV-madgraph-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_v2",
                    "ProductionRun2v2RunIIFall17MiniAODv2.WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400_13TeV-madgraph",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8",
                    "ProductionRun2v2RunIIFall17MiniAODv2.ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8",
                 ]

command = "./looper.py $INPUT $OUTPUT 0 1"
output_folder = "output_skim_sideband2"
commands = []
commands += prepare_command_list("/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2", Run2016_ntuples_2016v2, output_folder, command = command, files_per_job = 1, files_per_sample = 4)
#commands += prepare_command_list("/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub", Run20172018_ntuples, output_folder, command = command, files_per_job = 5)

do_submission(commands, output_folder, executable = "looper.py")