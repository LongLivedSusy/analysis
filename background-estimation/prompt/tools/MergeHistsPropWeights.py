#this module should work just like hadd
from ROOT import *
import glob, sys
import numpy as np
from utils import *
import os as os_



lumi = 35.9*1000
#lumi = 5.746*1000 # 2016B from Ra2/b
#lumi = 2.572*1000#2016C from Ra2/b
lumi = 2.57*1000
lumi = 137*1000


analyzer = 'Simple'
analyzer = 'Prompt'

istest = False
try: folder = sys.argv[1]
except:
    print 'please give folder name as first argument'
    exit(0)
    
try: erakey = sys.argv[2]
except: erakey = 'Summer16' # Fall17

dotree = True
verbosity = 1000

'''#low stats version:
keywordsOfContribution = {}
keywordsOfContribution['TTJets'] = ['TTJets_Tune']
keywordsOfContribution['WJets'] = ['WJetsToLNu_Tune']
keywordsOfContribution['DYJets'] = ['_DYJetsToLL_M-50_Tune']
'''

keywordsOfContribution = {}#one element for each color on the final plot
keywordsOfContribution['WJets'] = ['WJetsToLNu_HT-100To200','WJetsToLNu_HT-200To400','WJetsToLNu_HT-400To600','WJetsToLNu_HT-600To800','WJetsToLNu_HT-800To1200','WJetsToLNu_HT-1200To2500','WJetsToLNu_HT-2500ToInf']
#keywordsOfContribution['WJets'] = ['WJetsToLNu_HT-100To200']
keywordsOfContribution['TTJets'] = ['TTJets_SingleLeptFromT_','TTJets_SingleLeptFromTbar_', 'TTJets_DiLept','ST_t-channel_top_4f_inclusiveDecays', 'ST_t-channel_antitop_4f_inclusiveDecays','ST_tW_top_5f_inclusiveDecays','ST_tW_antitop_5f_inclusiveDecays']
keywordsOfContribution['ZJetsToNuNu'] = ['ZJetsToNuNu_HT-100To200','ZJetsToNuNu_HT-200To400','ZJetsToNuNu_HT-400To600','ZJetsToNuNu_HT-600To800','ZJetsToNuNu_HT-800To1200','ZJetsToNuNu_HT-1200To2500']#,'ZJetsToNuNu_HT-2500ToInf']
keywordsOfContribution['DYJets'] = ['DYJetsToLL_M-50_HT-100to200','DYJetsToLL_M-50_HT-200to400','DYJetsToLL_M-50_HT-400to600','DYJetsToLL_M-50_HT-600to800','DYJetsToLL_M-50_HT-800to1200','DYJetsToLL_M-50_HT-1200to2500','DYJetsToLL_M-50_HT-2500toInf']
keywordsOfContribution['QCD'] = ['QCD_HT200to300','QCD_HT300to500','QCD_HT500to700','QCD_HT700to1000','QCD_HT1000to1500','QCD_HT1500to2000','QCD_HT2000toInf']
#keywordsOfContribution['VBFHHTo4B_CV_1_C2V_2_C3_1'] = ['VBFHHTo4B_CV_1_C2V_2_C3_1']

if erakey=="":
	keywordsOfContribution['DYJets'] = ['DYJetsToLL_M-50_Tune']	
if not 'Fall17' in erakey: 
	keywordsOfContribution['WJets'].append('WJetsToLNu_Tune')
	keywordsOfContribution['TTJets'].append('ST_s-channel_4f_InclusiveDecays')
	keywordsOfContribution['VV'] = ['ZZ_Tune','WW_Tune','WZ_Tune','ZZ_Tune']

for contkey in keywordsOfContribution.keys():
	thingsInHadd = ''
	for keyword in keywordsOfContribution[contkey]:
		command = 'hadd -f output/mediumchunks/unwghtd'+erakey+keyword+analyzer+'.root '+folder+'/'+analyzer+'*'+erakey+'*'+keyword+'*'+'-nfpj*.root'
		print 'command', command
		if not istest: os_.system(command)    
		fuw = TFile('output/mediumchunks/unwghtd'+erakey+keyword+analyzer+'.root')
		fw = TFile('output/mediumchunks/'+erakey+keyword+analyzer+'.root', 'recreate')
		thingsInHadd+='output/mediumchunks/'+erakey+keyword+analyzer+'.root '
		hHt = fuw.Get('hHt')
		hHt.SetDirectory(0)
		nsimulated = hHt.GetEntries()
		keys = fuw.GetListOfKeys()
		for key in keys:
			name = key.GetName()
			if name=='hHt': continue
			if 'TreeMaker2' in name: continue
			if 'PreSelection' in name: continue
			if not len(name.split('/'))>0: continue
			hist = fuw.Get(name)
			hist.Scale(lumi*1.0/nsimulated)
			fw.cd()
			hist.Write()
		fuw.Close()
			
		if dotree:
			print 'opening', 'output/mediumchunks/unwghtd'+erakey+keyword+analyzer+'.root'
			print folder+'/'+analyzer+'*'+erakey+'*'+keyword+'*'+'-nfpj*.root'
			chain_in = TChain('TreeMaker2/PreSelection')
			rawlist = glob.glob(folder+'/'+analyzer+'*'+erakey+'*'+keyword+'*'+'-nfpj*.root')
			for thing in rawlist: 
				print 'adding in', thing
				chain_in.Add(thing)
			#chain_in.Add('output/mediumchunks/unwghtd'+erakey+keyword+analyzer+'.root')

			print 'will process', chain_in.GetEntries(), 'entries'
			if chain_in.GetEntries()==0: continue
			fw.cd()
			tree_out = chain_in.CloneTree(0)
			weight = np.zeros(1, dtype=float)
			b_weight = tree_out.Branch('weight', weight, 'weight/D')
			nentries = chain_in.GetEntries()
			print 'gonna do', keyword
			for ientry in range(nentries):
				if ientry % 1000 == 0:
					print 'Processing entry %d of %d' % (ientry, nentries),'('+'{:.1%}'.format(1.0*ientry/nentries)+')'
				chain_in.GetEntry(ientry)
				#continue
				weight[0] = chain_in.CrossSection*lumi*1.0/nsimulated			
				if ientry==0: print keyword, 'event weight', 36000*weight[0]
				tree_out.Fill()
				
			fw.cd()
			print 'test 1'
			hHt.Write()
			print 'test 2'			
			fw.mkdir('TreeMaker2')
			print 'test 3'			
			fw.cd('TreeMaker2')
			print 'test 3'
			tree_out.Write()
			print 'test 4'			
		
		else: hHt.Write()
				
		fuw.Close()
		command = 'rm output/mediumchunks/unwghtd'+erakey+keyword+analyzer+'.root'
		print command
		if not istest: os_.system(command)
		fw.Close()
	command = 'hadd -f output/bigchunks/'+erakey+contkey+analyzer+'.root '+thingsInHadd
	print 'command', command
	os_.system(command)
	
	
	
	
	