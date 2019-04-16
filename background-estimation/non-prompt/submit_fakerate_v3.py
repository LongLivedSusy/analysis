#!/bin/env python
from submit import *
from optparse import OptionParser

parser = OptionParser()
(options, args) = parser.parse_args()
if len(args) > 0:
    files_per_job = int(args[0])
else:
    files_per_job = 50

ntuples = {}

ntuples["/pnfs/desy.de/cms/tier2/store/user/vormwald/NtupleHub/ProductionRun2v3"] = [
        "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8",
        "Summer16.ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
        "Summer16.ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1",
        "Summer16.ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1",
        "Summer16.ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1",
        "Summer16.ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1_ext1",
        "Summer16.ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_ext1",
        "Summer16.ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1",
        "Summer16.ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1_ext1",
        "Summer16.ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_ext1",
        "Summer16.TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_ext1",
        "Summer16.TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.TTTT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8",
        "Summer16.TT_TuneCUETP8M2T4_13TeV-powheg-pythia8",
        "Summer16.WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2",
        "Summer16.WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
        "Summer16.WWTo2L2Nu_13TeV-powheg",
        "Summer16.WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8",
        "Summer16.WW_TuneCUETP8M1_13TeV-pythia8",
        "Summer16.WW_TuneCUETP8M1_13TeV-pythia8_ext1",
        "Summer16.WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
        "Summer16.WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8",
        "Summer16.WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8",
        "Summer16.WZ_TuneCUETP8M1_13TeV-pythia8",
        "Summer16.WZ_TuneCUETP8M1_13TeV-pythia8_ext1",
        "Summer16.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-100To200_13TeV-madgraph_ext1",
        "Summer16.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-200To400_13TeV-madgraph_ext1",
        "Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-400To600_13TeV-madgraph_ext1",
        "Summer16.ZJetsToNuNu_HT-600To800_13TeV-madgraph",
        "Summer16.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
        #"Summer16.ZJetsToNuNu_Zpt-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        #"Summer16.ZJetsToNuNu_Zpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1",
        "Summer16.ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8",
        "Summer16.ZZTo2Q2Nu_13TeV_amcatnloFXFX_madspin_pythia8",
        "Summer16.ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8",
        "Summer16.ZZ_TuneCUETP8M1_13TeV-pythia8",
        "Summer16.ZZ_TuneCUETP8M1_13TeV-pythia8_ext1",
                 ]

ntuples["/pnfs/desy.de/cms/tier2/store/user/jarieger/NtupleHub/ProductionRun2v3"] = [
        "Run2016B-17Jul2018_ver2-v1.METAOD",
        "Run2016C-17Jul2018-v1.METAOD",
        "Run2016D-17Jul2018-v1.METAOD",
        "Run2016E-17Jul2018-v1.METAOD",
        "Run2016B-17Jul2018_ver2-v1.SingleMuonAOD",
        "Run2016C-17Jul2018-v1.SingleMuonAOD",
        "Run2016D-17Jul2018-v1.SingleMuonAOD",
        "Run2016E-17Jul2018-v1.SingleMuonAOD",
        "Run2016C-17Jul2018-v1.SingleElectronAOD",
        "Run2016D-17Jul2018-v1.SingleElectronAOD",
        "Run2016E-17Jul2018-v1.SingleElectronAOD",
        "Run2016C-17Jul2018-v1.JetHTAOD",
        "Run2016E-17Jul2018-v1.JetHTAOD",
]

ntuples["/pnfs/desy.de/cms/tier2/store/user/ssekmen/NtupleHub/ProductionRun2v3"] = [
        "Run2016F-17Jul2018-v1.JetHTAOD",
        "Run2016F-17Jul2018-v1.METAOD",
        "Run2016F-17Jul2018-v1.SingleMuonAOD",
        "Run2016G-17Jul2018-v1.JetHTAOD",
        "Run2016G-17Jul2018-v1.METAOD",
        "Run2016G-17Jul2018-v1.SingleElectronAOD",
        "Run2016G-17Jul2018-v1.SingleMuonAOD",
        "Run2016H-17Jul2018-v1.JetHTAOD",
        "Run2016H-17Jul2018-v1.SingleElectronAOD",
]

ntuples["/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v4"] = [
        "Run2017B-31Mar2018-v1.JetHTAOD0",
        "Run2017B-31Mar2018-v1.JetHTAOD1",
        "Run2017B-31Mar2018-v1.METAOD",
        "Run2017B-31Mar2018-v1.SingleElectronAOD",
        "Run2017B-31Mar2018-v1.SingleMuonAOD0",
        "Run2017B-31Mar2018-v1.SingleMuonAOD1",
        "Run2017B-31Mar2018-v1.SingleMuonAOD2",
        "Run2017C-31Mar2018-v1.JetHTAOD",
        "Run2017C-31Mar2018-v1.JetHTAOD0",
        "Run2017C-31Mar2018-v1.JetHTAOD1",
        "Run2017C-31Mar2018-v1.METAOD",
        "Run2017C-31Mar2018-v1.METAOD0",
        "Run2017C-31Mar2018-v1.SingleElectronAOD",
        "Run2017D-31Mar2018-v1.METAOD",
        "Run2017D-31Mar2018-v1.SingleElectronAOD",
        "Run2017D-31Mar2018-v1.SingleMuonAOD",
        "Run2017E-31Mar2018-v1.JetHTAOD",
        "Run2017E-31Mar2018-v1.JetHTAOD0",
        "Run2017E-31Mar2018-v1.METAOD",
        "Run2017E-31Mar2018-v1.SingleElectronAOD",
        "Run2017E-31Mar2018-v1.SingleMuonAOD",
]

ntuples["/pnfs/desy.de/cms/tier2/store/user/aksingh/NtupleHub/ProductionRun2v3"] = [
        "Run2017F-31Mar2018-v1.JetHTAOD",
        "Run2017F-31Mar2018-v1.METAOD0",
        "Run2017F-31Mar2018-v1.SingleElectronAOD",
        "Run2017F-31Mar2018-v1.SingleMuonAOD0",
]

ntuples["/pnfs/desy.de/cms/tier2/store/user/spak/NtupleHub/ProductionRun2v3"] = [
        "Run2018A-17Sep2018-v1.JetHTAOD",
        "Run2018A-17Sep2018-v1.METAOD",
]

ntuples["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3"] = [
        "Run2018A-17Sep2018-v1.JetHTAOD",
        "Run2018A-17Sep2018-v1.METAOD",
        "Run2018B-17Sep2018-v1.JetHTAOD",
        "Run2018B-17Sep2018-v1.SingleMuonAOD",
]

ntuples["/pnfs/desy.de/cms/tier2/store/user/tokramer/NtupleHub/ProductionRun2v3"] = [
        "Run2018C-17Sep2018-v1.JetHTAOD",
        "Run2018C-17Sep2018-v1.METAOD",
        "Run2018C-17Sep2018-v1.SingleMuonAOD",
]

ntuples["/pnfs/desy.de/cms/tier2/store/user/jsonneve/NtupleHub/ProductionRun2v3"] = [
        "Run2018D-PromptReco-v1.METAOD",
        "Run2018D-PromptReco-v2.JetHTAOD0",
        "Run2018D-PromptReco-v2.JetHTAOD1",
        "Run2018D-PromptReco-v2.JetHTAOD2",
        "Run2018D-PromptReco-v2.JetHTAOD3",
        "Run2018D-PromptReco-v2.JetHTAOD4",
        "Run2018D-PromptReco-v2.JetHTAOD5",
        "Run2018D-PromptReco-v2.JetHTAOD6",
        "Run2018D-PromptReco-v2.METAOD0",
        "Run2018D-PromptReco-v2.METAOD1",
        "Run2018D-PromptReco-v2.METAOD2",
        "Run2018D-PromptReco-v2.SingleMuonAOD0",
        "Run2018D-PromptReco-v2.SingleMuonAOD1",
        "Run2018D-PromptReco-v2.SingleMuonAOD2",
        "Run2018D-PromptReco-v2.SingleMuonAOD3",
        "Run2018D-PromptReco-v2.SingleMuonAOD4",
        "Run2018D-PromptReco-v2.SingleMuonAOD5",
        "Run2018D-PromptReco-v2.SingleMuonAOD6",
        "Run2018D-PromptReco-v2.SingleMuonAOD7",
        "Run2018D-PromptReco-v2.SingleMuonAOD8",
]

ntuples["/nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/LongLivedSMS/ntuple_sidecar"] = [
        "g1800_chi1400_27_200970_step4_10",
        "g1800_chi1400_27_200970_step4_30",
        "g1800_chi1400_27_200970_step4_50",
        "g1800_chi1400_27_200970_step4_100",
        "g1800_chi1400_27_200970_step4_1000",
]

#command = "./looper_ng.py --input $INPUT --output $OUTPUT --only_fakerate --loose_dxy"
command = "./looper_ng.py --input $INPUT --output $OUTPUT --only_fakerate"
output_folder = "output_fakerate_ng_3"
commands = []
for folder in ntuples:

    def is_string_in_list(text, mylist):
        for item in mylist:
            if text in item:
                return True
        return False
   
    #if is_string_in_list("Summer16", ntuples[folder]): continue
    if is_string_in_list("Run2016", ntuples[folder]): continue
    if is_string_in_list("Run2017", ntuples[folder]): continue
    if is_string_in_list("Run2018", ntuples[folder]): continue

    if is_string_in_list("g1800", ntuples[folder]):
        nowildcard = True
    else:
        nowildcard = False

    commands += prepare_command_list(folder, ntuples[folder], output_folder, command=command, files_per_job=files_per_job, nowildcard=nowildcard)
do_submission(commands, output_folder, executable = "looper_ng.py")
