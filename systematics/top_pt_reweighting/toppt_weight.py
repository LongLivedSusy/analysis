#!/usr/bin/env python

from ROOT import *
import os, sys
from glob import glob
import math

#infilenames = sys.argv[1]
infilenames = '/pnfs/knu.ac.kr/data/cms/store/user/ssekmen/NtupleHub/Production2016v2/Summer16.TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1_112_RA2AnalysisTree.root'
#infilenames = '/pnfs/knu.ac.kr/data/cms/store/user/ssekmen/NtupleHub/Production2016v2/Summer16.TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_*_RA2AnalysisTree.root'

c = TChain('TreeMaker2/PreSelection')
filenamelist = glob(infilenames)
print 'adding', filenamelist
filelist = []
for filename in filenamelist:
    fname = filename.strip()
    c.Add(fname)

c.Show(0)
nentries = min(9999999,c.GetEntries())
print 'will analyze', nentries

newfilename = 'syst_'+(infilenames.split('/')[-1]).replace('*','')
fnew = TFile(newfilename,'recreate')

import numpy as np
var_weight_toppt_up = np.zeros(1,dtype=float)
var_weight_toppt = np.zeros(1,dtype=float)
var_weight_toppt_down = np.zeros(1,dtype=float)

tEvent = TTree('tEvent','tEvent')
tEvent.Branch('weight_toppt_up', var_weight_toppt_up, 'weight_toppt_up/D')
tEvent.Branch('weight_toppt', var_weight_toppt, 'weight_toppt/D')
tEvent.Branch('weight_toppt_down', var_weight_toppt_down, 'weight_toppt_down/D')

verbosity = 1000

#for ientry in range(nentries):
for ientry in range(1000):
    if ientry%verbosity==0:
	print 'analyzing event %d of %d' %(ientry, nentries)+ '....%f' %(100.*ientry/nentries)+'%'

    c.GetEntry(ientry)
    
    weight_nom = 1
    for i,Genpar in enumerate(c.GenParticles):
	if c.GenParticles_ParentId[i]!=c.GenParticles_PdgId[i] and c.GenParticles_ParentId[i]!=c.GenParticles_PdgId[i] : #FIXME, should use GenParticles_Daughter0Id and Daughter1Id instead of ParentId
	    if abs(c.GenParticles_PdgId[i])==6 :
		    a=0.0615
		    b=-0.0005
		    weight_nom *=math.exp(a+b*Genpar.Pt())
		    #print ientry, i
    
    weight_nom = math.sqrt(weight_nom)
    weight_toppt_up=1
    weight_toppt = math.sqrt(weight_nom)
    weight_toppt_down = weight_nom
    print 'up nom down', weight_toppt_up, weight_toppt, weight_toppt_down

    var_weight_toppt_up[0] = weight_toppt_up
    var_weight_toppt[0] = weight_toppt
    var_weight_toppt_down[0] = weight_toppt_down

    tEvent.Fill()

fnew.cd()
tEvent.Write()
fnew.Close()

