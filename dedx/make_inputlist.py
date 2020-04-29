import os, sys
from glob import glob

def make_inputlist(samples):
    userlist = []
    hub_folders = "/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3*"

    print "Making input ntuples list.."
    if not os.path.exists("./inputs"):
	os.system("mkdir -p inputs")
    
    for sample in samples:
	outputname = sample
	if "*" in sample : 
	    outputname = sample.replace("*","-")
        print outputname
	with open("./inputs/%s.txt"%outputname,'w') as f:
	    for inputfile in sorted(glob(hub_folders + "/*"+sample+"*.root")):
		f.write(inputfile+'\n')
   

if __name__ == "__main__" : 
   
    # Sample name for globbing

    Summer16_bkg = [
    "Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
    "Summer16.DYJetsToLL_M-50_HT-100to200",
    "Summer16.DYJetsToLL_M-50_HT-200to400",
    "Summer16.DYJetsToLL_M-50_HT-400to600",
    "Summer16.DYJetsToLL_M-50_HT-600to800",
    "Summer16.DYJetsToLL_M-50_HT-800to1200",
    "Summer16.DYJetsToLL_M-50_HT-1200to2500",
    "Summer16.DYJetsToLL_M-50_HT-2500toInf",
    "Summer16.QCD_HT200to300",
    "Summer16.QCD_HT300to500",
    "Summer16.QCD_HT500to700",
    "Summer16.QCD_HT700to1000",
    "Summer16.QCD_HT1000to1500",
    "Summer16.QCD_HT1500to2000",
    "Summer16.QCD_HT2000toInf",
    "Summer16.TTJets_TuneCUETP8M1_13TeV",
    "Summer16.WJetsToLNu_TuneCUETP8M1",
    "Summer16.WJetsToLNu_HT-100To200",
    "Summer16.WJetsToLNu_HT-200To400",
    "Summer16.WJetsToLNu_HT-400To600",
    "Summer16.WJetsToLNu_HT-600To800",
    "Summer16.WJetsToLNu_HT-800To1200",
    "Summer16.WJetsToLNu_HT-1200To2500",
    "Summer16.WJetsToLNu_HT-2500ToInf",
    "Summer16.ZJetsToNuNu_HT-100To200",
    "Summer16.ZJetsToNuNu_HT-200To400",
    "Summer16.ZJetsToNuNu_HT-400To600",
    "Summer16.ZJetsToNuNu_HT-600To800",
    "Summer16.ZJetsToNuNu_HT-800To1200",
    "Summer16.ZJetsToNuNu_HT-1200To2500",
    "Summer16.ZJetsToNuNu_HT-2500ToInf",
    "Summer16.WW_TuneCUETP8M1",
    "Summer16.WZ_TuneCUETP8M1",
    "Summer16.ZZ_TuneCUETP8M1",
    ]

    Run2016_MET = [
    "Run2016B*MET",
    "Run2016C*MET",
    "Run2016D*MET",
    "Run2016E*MET",
    "Run2016F*MET",
    "Run2016G*MET",
    "Run2016H*MET",
    ]
    
    Run2016_SingleMuon=[
    "Run2016B*SingleMuon",
    "Run2016C*SingleMuon",
    "Run2016D*SingleMuon",
    "Run2016E*SingleMuon",
    "Run2016F*SingleMuon",
    "Run2016G*SingleMuon",
    "Run2016H*SingleMuon",
    ]
    
    Run2016_SingleElectron=[
    "Run2016B*SingleElectron",
    "Run2016C*SingleElectron",
    "Run2016D*SingleElectron",
    "Run2016E*SingleElectron",
    "Run2016F*SingleElectron",
    "Run2016G*SingleElectron",
    "Run2016H*SingleElectron",
    ]
    
    Summer16_signal = [
    #"RunIISummer16MiniAODv3.SMS-T1qqqq",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-100_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_",
    "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_",
    ]

    Fall17_bkg = [
    "RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5",
    "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200",
    "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400",
    "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600",
    "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800",
    "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200",
    "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500",
    "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-2500toInf",
    "RunIIFall17MiniAODv2.QCD_HT200to300",
    "RunIIFall17MiniAODv2.QCD_HT300to500",
    "RunIIFall17MiniAODv2.QCD_HT500to700",
    "RunIIFall17MiniAODv2.QCD_HT700to1000",
    "RunIIFall17MiniAODv2.QCD_HT1000to1500",
    "RunIIFall17MiniAODv2.QCD_HT1500to2000",
    "RunIIFall17MiniAODv2.QCD_HT2000toInf",
    "RunIIFall17MiniAODv2.TTJets_TuneCP5",
    "RunIIFall17MiniAODv2.TTJets_HT-600to800",
    "RunIIFall17MiniAODv2.TTJets_HT-800to1200",
    "RunIIFall17MiniAODv2.TTJets_HT-1200to2500",
    "RunIIFall17MiniAODv2.TTJets_HT-2500toInf",
    "RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200",
    "RunIIFall17MiniAODv2.WJetsToLNu_HT-200To400",
    "RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600",
    "RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800",
    "RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200",
    "RunIIFall17MiniAODv2.WJetsToLNu_HT-1200To2500",
    "RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf",
    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200",
    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400",
    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600",
    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800",
    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200",
    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500",
    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf",
    "RunIIFall17MiniAODv2.WWTo1L1Nu2Q",
    "RunIIFall17MiniAODv2.WZTo1L1Nu2Q",
    "RunIIFall17MiniAODv2.WZTo1L3Nu",
    "RunIIFall17MiniAODv2.ZZTo2L2Q",
    "RunIIFall17MiniAODv2.WZZ_TuneCP5",
    ]
    
    Run2017_SingleMuon = [
    "Run2017B*SingleMuon",
    "Run2017C*SingleMuon",
    "Run2017D*SingleMuon",
    "Run2017E*SingleMuon",
    "Run2017F*SingleMuon",
    #"Run2017G*SingleMuon",
    #"Run2017H*SingleMuon",
    ]

    Run2017_SingleElectron=[
    "Run2017B*SingleElectron",
    "Run2017C*SingleElectron",
    "Run2017D*SingleElectron",
    "Run2017E*SingleElectron",
    "Run2017F*SingleElectron",
    #"Run2017G*SingleElectron",
    #"Run2017H*SingleElectron",
    ]

    samples=[]
    #samples.extend(Summer16_bkg)
    samples.extend(Summer16_signal)
    #samples.extend(Run2016_SingleMuon)
    #samples.extend(Run2016_SingleElectron)
    #samples.extend(Fall17_bkg)
    #samples.extend(Run2017_SingleMuon)
    #samples.extend(Run2017_SingleElectron)
    
    #Input list for each process
    make_inputlist(samples)

    #Split list for number of files per job
    #nfpj = 100
    #split_inputlist(nfpj)

