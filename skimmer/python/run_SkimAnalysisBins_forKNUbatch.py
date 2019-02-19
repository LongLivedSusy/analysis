#!/bin/env python
import sys, os
from glob import glob
from GridEngineTools import runParallel

def create_inputlist(infiles) :
    inputfiles = glob(infiles)
    files = "" 
    for inputfilename in inputfiles : 
	files += 'dcap://cluster142.knu.ac.kr/'+inputfilename + " "
    
    return files

def main() :
    
    path = '/pnfs/knu.ac.kr/data/cms/store/user/spak/DisappTrks/outputs/TREE/'
    Signals = [
    #"g1800_chi1400_27_200970_step4_100.root", 
    #"pMSSM12_MCMC1_4_252033_step4_TREEMAKER*_RA2AnalysisTree.root", 
    #"pMSSM12_MCMC1_5_448429_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_8_373637_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_10_374794_step4_TREEMAKER*_RA2AnalysisTree.root", 
    #"pMSSM12_MCMC1_12_865833_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_13_547677_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_20_690321_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_22_237840_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_24_345416_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_27_969542_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_28_737434_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_37_569964_ctau250_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_37_569964_ctau750_step4_TREEMAKER*_RA2AnalysisTree.root",
    #"pMSSM12_MCMC1_44_855871_step4_TREEMAKER*_RA2AnalysisTree.root",
    "pMSSM12_MCMC1_47_872207_step4_TREEMAKER*_RA2AnalysisTree.root",
    ]

    inputfiles = ""
    syst_args = ""	    # for systematics(eg. --dojetsyst --nsigmajes 1)
    suffix = ""
    commands = []

    for signal in Signals :
	inputfiles = create_inputlist(path+signal)
	outfilename = 'skim_'+(signal.split('/')[-1]).replace('*','')
	
	command = 'python SkimAnalysisBins_work.py -fin %s -fout %s %s' %(inputfiles,outfilename, syst_args)
	commands.append(command)

	# local test
	os.system(command)

    ### For batch job
    #runParallel(commands, runmode='grid', dryrun=False, qsubOptions='-q cms', dontCheckOnJobs=True)    
    #runParallel(commands, runmode='multi', dryrun=False, dontCheckOnJobs=True)    



if __name__ == '__main__' :
    main()

#path_bkg = '/pnfs/knu.ac.kr/data/cms/store/user/ssekmen/distrack/BGMC/Production2016v2/'
#Bkgs = [
#	"'Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_*_RA2AnalysisTree.root'",
#	"'Summer16.QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WWTo2L2Nu_13TeV-powheg_*_RA2AnalysisTree.root'",
#	"'Summer16.WW_TuneCUETP8M1_13TeV-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.WZ_TuneCUETP8M1_13TeV-pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.ZJetsToNuNu_HT-100To200_13TeV-madgraph_*_RA2AnalysisTree.root'",
#	"'Summer16.ZJetsToNuNu_HT-200To400_13TeV-madgraph_*_RA2AnalysisTree.root'",
#	"'Summer16.ZJetsToNuNu_HT-400To600_13TeV-madgraph_*_RA2AnalysisTree.root'",
#	"'Summer16.ZJetsToNuNu_HT-600To800_13TeV-madgraph_*_RA2AnalysisTree.root'",
#	"'Summer16.ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_*_RA2AnalysisTree.root'",
#	"'Summer16.ZZTo2Q2Nu_13TeV_amcatnloFXFX_madspin_pythia8_*_RA2AnalysisTree.root'",
#	]
