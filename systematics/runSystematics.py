#! /usr/bin/env python

from ROOT import *
from lib_systematics import *
import os, sys
from glob import glob
from shared_utils import *
import argparse

gStyle.SetOptStat(111111)

def runSystematics(inputfile, outputdir, doSyst=False, systname='', nSigmaBtag=0, nSigmaJec=0, nSigmaJer=0, nSigmaIsr=0) :

    print 'inputfile : {}, outputdir : {}, doSyst : {}'.format(inputfile, outputdir, doSyst)
    
    tree = TChain("TreeMaker2/PreSelection")
    with open (inputfile,"r") as filenamelists : 
	filenamelist = filenamelists.readlines()
	for filename in filenamelist : 
	    tree.Add(filename.strip())
	    #print 'adding', filename

    nentries = min(100,tree.GetEntries())
    print 'will analyze', nentries

    csv_b = 0.6324  #DeepCSVM

    if 'Fall17' in inputfile or 'Run2017' in inputfile : phase = 1
    else : phase = 0

    ###########################################
    # Book histogram
    ##########################################
    hNev = TH1D('Nev','Total number of events',1,0,1)
    hNev_passAllSel = TH1D('Nev_passAllSel','Number of events passed all selection',1,0,1)

    outputfilename = outputdir+'/'+(inputfile.split('/')[-1]).replace('*','').replace("txt","root")
    if doSyst == True : 
	outputfilename = outputdir+'/'+(inputfile.split('/')[-1]).replace('*','').replace(".txt",systname+"_.root")
	
	readerBtag = prepareReaderBtagSF()
    
    fout = TFile(outputfilename,'recreate')
    print 'outputfilename : ',outputfilename

    # Event Loop
    for ientry in range(nentries) :
	verbosity = 1000
	if ientry %verbosity==0:
	    print 'analyzing event %d of %d' % (ientry, nentries)+ '....%f'%(100.*ientry/nentries)+'%'
	weight = 1.0
	weight_btag = 1.0
	weight_ISR = 1.0

	tree.GetEntry(ientry)
	hNev.Fill(0)
    
	if doSyst == True : 
	    # For B tag syst
	    nSigmaBtagFastSim = 1.0
	    isFastSim = False
	    weight_btag = get_btag_weight(tree,nSigmaBtag,nSigmaBtagFastSim,isFastSim,readerBtag)
	    
	    # For Jet syst
	    applysmearing = True
	    if applysmearing : 
	        Jets = jets_rescale_smear(tree,applysmearing,nSigmaJec,nSigmaJer) # 'Jets' is list containing TLorentzVector jet
	    else : Jets = tree.Jets

	    # For ISR syst
	    weight_ISR = get_isr_weight(tree, nSigmaIsr)
	    
	# Total weight
	weight = weight_btag * weight_ISR 
	print 'weight:{}, weight_btag:{}, weight_ISR:{}'.format(weight, weight_btag, weight_ISR)


    # Save to root file
    fout.cd()
    hNev.Write()
    hNev_passAllSel.Write()
    print 'just created',fout.GetName() 

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--doSyst", default=False, action='store_true')
    args = parser.parse_args()
    doSyst = args.doSyst

    #inputfile = "../dedx/inputs/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.txt"
    inputfile = "../dedx/inputs/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1.txt"
    outputdir = 'output'
    
    if not os.path.exists(outputdir) : 
	os.system('mkdir -p '+outputdir)
    
    '''
    if doSyst : 
	#read_sigmas('./syst_sigmas.txt')
	for systname, nsigmas in read_sigmas('./syst_sigmas.txt').iteritems():
	    nSigmaBtag=nsigmas[0]
	    nSigmaJec=nsigmas[1]
	    nSigmaJer=nsigmas[2]
	    nSigmaIsr=nsigmas[3]

	    print systname, nSigmaBtag, nSigmaJec, nSigmaJer, nSigmaIsr
	    #runSystematics(inputfile, outputdir, doSyst, systname, nSigmaBtag, nSigmaJec, nSigmaJer, nSigmaIsr)

    else : runSystematics(inputfile, outputdir)
    '''

    #runSystematics(inputfile, outputdir)
    runSystematics(inputfile, outputdir, doSyst=True, systname='IsrUp', nSigmaBtag=0, nSigmaJec=0, nSigmaJer=0, nSigmaIsr=1)
    
