#this module should work just like hadd
from ROOT import *
import glob, sys
import numpy as np
from utils import *
import os as os_


lumi = 36*1000

istest = False
try: folder = sys.argv[1]
except:
    print 'please give folder name as first argument'
    exit(0)
    
try: predmode = sys.argv[2]
except: predmode = 'YesZSmear'
    
keywordsOfContribution = {}#one element for each color on the final plot
keywordsOfContribution['TTJets'] = ['TTJets_SingleLeptFromT', 'TTJets_DiLept']
keywordsOfContribution['WJets'] = ['WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500','WJetsToLNu_HT-2500ToInf']
#keywordsOfContribution['QCD'] = ['QCD_HT200to300','QCD_HT300to500','QCD_HT500to700','QCD_HT700to1000','QCD_HT1000to1500','QCD_HT1500to2000','QCD_HT2000toInf']
#keywordsOfContribution['VBFHHTo4B_CV_1_C2V_2_C3_1'] = ['VBFHHTo4B_CV_1_C2V_2_C3_1']

for contkey in keywordsOfContribution.keys():
	thingsInHadd = ''
	for keyword in keywordsOfContribution[contkey]:
		command = 'python tools/ahadd.py -f output/mediumchunks/unwghtd'+keyword+predmode+'.root '+folder+'/Prompt*'+keyword+'*'+predmode+'.root'
		print 'command', command
		if not istest: os_.system(command)    
		fuw = TFile('output/mediumchunks/unwghtd'+keyword+predmode+'.root')
		fw = TFile('output/mediumchunks/'+keyword+predmode+'.root', 'recreate')
		thingsInHadd+='output/mediumchunks/'+keyword+predmode+'.root '
		hHt = fuw.Get('hHt')
		nentries = hHt.GetEntries()
		keys = fuw.GetListOfKeys()
		for key in keys:
			name = key.GetName()
			if not len(name.split('/'))>0: continue
			hist = fuw.Get(name)
			hist.Scale(lumi*1.0/nentries)
			fw.cd()
			hist.Write()
		fuw.Close()
		command = 'rm output/mediumchunks/unwghtd'+keyword+predmode+'.root'
		print command
		if not istest: os_.system(command)
		fw.Close()
	command = 'hadd -f output/bigchunks/'+contkey+predmode+'.root '+thingsInHadd
	print 'command', command
	os_.system(command)