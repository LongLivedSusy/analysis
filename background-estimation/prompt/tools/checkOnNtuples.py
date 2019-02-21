from ROOT import *
from glob import glob


flist = glob('/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v1/*.root')
#flist = glob('/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/*.root')

for fname in flist:
	f = TFile(fname)
	t = f.Get('TreeMaker2/PreSelection')
	try:
		t.GetEntry(0)
		print len(t.tracks)
		print 'yes', fname		
	except:
		print 'no', fname
	f.Close()