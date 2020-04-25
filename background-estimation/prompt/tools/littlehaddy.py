import os
from glob import glob
from ROOT import *

TestMode = False

uniquestems = [ 'Summer16.ZJetsToNuNu_HT-200To400',\
                'Summer16.ZJetsToNuNu_HT-400To600',\
				'Summer16.ZJetsToNuNu_HT-600To800',\
				'Summer16.ZJetsToNuNu_HT-800To1200',\
				'Summer16.ZJetsToNuNu_HT-1200To2500',\
				'Summer16.ZJetsToNuNu_HT-2500ToInf',\
                'Summer16.WJetsToLNu_HT-100To200',\
                'Summer16.WJetsToLNu_HT-200To400',\
                'Summer16.WJetsToLNu_HT-400To600',\
                'Summer16.WJetsToLNu_HT-600To800',\
                'Summer16.WJetsToLNu_HT-800To1200',\
                'Summer16.WJetsToLNu_HT-1200To2500',\
                'Summer16.WJetsToLNu_HT-2500ToInf',\
'','', '','', '','ST_tW_top_5f_inclusiveDecays','ST_tW_antitop_5f_inclusiveDecays'                
                'TTJets_SingleLeptFromT_',\
                'TTJets_SingleLeptFromTbar_',\
                'TTJets_DiLept',\
                'ST_t-channel_top_4f_inclusiveDecays',\
                'ST_t-channel_top_4f_inclusiveDecays',\
                'ST_t-channel_antitop_4f_inclusiveDecays'
                'Summer16.TTJets_HT-2500toInf',\
                'Summer16.DYJetsToLL_M-50_HT-100to200',\
                'Summer16.DYJetsToLL_M-50_HT-200to400',\
                'Summer16.DYJetsToLL_M-50_HT-400to600',\
                'Summer16.DYJetsToLL_M-50_HT-600to800',\
                'Summer16.DYJetsToLL_M-50_HT-800to1200',\
                'Summer16.DYJetsToLL_M-50_HT-1200to2500',\
                'Summer16.DYJetsToLL_M-50_HT-2500toInf',\
                'Summer16.QCD_HT200to300',\
                'Summer16.QCD_HT300to500',\
                'Summer16.QCD_HT500to700',\
                'Summer16.QCD_HT700to1000',\
                'Summer16.QCD_HT1000to1500',\
                'Summer16.QCD_HT1500to2000',\
                'Summer16.QCD_HT2000toInf',\
                'Summer16.WWTo2L2Nu_13TeV',\
                'Summer16.WWTo1L1Nu2Q_13TeV',\
                'Summer16.WZTo1L1Nu2Q_13TeV',\
                'Summer16.WZTo1L3Nu_13TeV',\
                'Summer16.ZZTo2Q2Nu_13TeV',\
                'Summer16.ZZTo2L2Q_13TeV',\
                'Summer16.WWZ_TuneCUETP8M1',\
                'Summer16.ZZZ_TuneCUETP8M1']
'''
uniquestems = [ 'pMSSM12_MCMC1_10_374794',\
                'pMSSM12_MCMC1_12_865833',\
                'pMSSM12_MCMC1_13_547677',\
                'pMSSM12_MCMC1_20_690321',\
                'pMSSM12_MCMC1_22_237840',\
                'pMSSM12_MCMC1_24_345416',\
#'pMSSM12_MCMC1_27_200970',\
                'pMSSM12_MCMC1_27_969542',\
                'pMSSM12_MCMC1_28_737434',\
#'pMSSM12_MCMC1_37_569964',\
                'pMSSM12_MCMC1_44_855871',\
                'pMSSM12_MCMC1_47_872207',\
                'pMSSM12_MCMC1_4_252033',\
                'pMSSM12_MCMC1_5_448429',\
                'pMSSM12_MCMC1_8_373637']
'''
#sourcedir = '/eos/uscms//store/user/sbein/StealthSusy/Production/ntuple/*'
#sourcedir = '/nfs/dust/cms/user/beinsam/LongLiveTheChi/ntuple_sidecar/smallchunks/*'


#Get signal cross section information
sourcedir = 'output/smallchunks/PromptBkgTree*'
verbosity = 10000

    
import numpy as np
for stem in uniquestems:
	targetname = stem.replace('SIM','').replace('step3','').replace('___','_').replace('__','_')
	targetnamewithpath = (sourcedir.replace('*','_')+targetname).replace('/smallchunks','/unweighted')+'.root'
	command = 'hadd -f '+ targetnamewithpath + ' ' + sourcedir+stem+'*.root'
	print command
	if not TestMode: os.system(command)
	fjustcombined = TFile(targetnamewithpath)
	hHt = fjustcombined.Get('hHt')
	try: hHt.SetDirectory(0)
	except: continue
	nsimulated = hHt.GetEntries()
	fjustcombined.Close()
	chain_in = TChain('TreeMaker2/PreSelection')
	chain_in.Add(targetnamewithpath)
	if chain_in.GetEntries()==0: continue
	fileout = TFile(targetnamewithpath.replace('unweighted','weighted'),'recreate')
	tree_out = chain_in.CloneTree(0)
	weight = np.zeros(1, dtype=float)
	b_weight = tree_out.Branch('weight', weight, 'weight/D')
	nentries = chain_in.GetEntries()
	for ientry in range(nentries):
		if ientry % verbosity == 0:
			print 'Processing entry %d of %d' % (ientry, nentries),'('+'{:.1%}'.format(1.0*ientry/nentries)+')'    
		chain_in.GetEntry(ientry)
		weight[0] = chain_in.CrossSection*1.0/nsimulated
		if ientry==0: print stem, 'event weight', 100000*weight[0]

	fileout.cd()
	tree_out.Write()
	hHt.Write()		
	print 'just created', fileout.GetName()
	fileout.Close()
#os.system('mv output/weighted/*pMSSM*.root output/Signal/')
#os.system('mv output/weighted/*.root output/Background/')



