from ROOT import *
import os, sys
from glob import glob
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
import time

lumi = 36.0

try: infiles = sys.argv[1]
except: infiles = 'Hists*.root'

try: outdir = sys.argv[2]
except: outdir = '../interpretation/HistsBkgObsSig/TheWholeEnchilada/Signal/'

tempfolder = str(time.time())
os.system('mkdir '+tempfolder)

if not os.path.isdir(outdir):
	dircmd = 'mkdir -p '+outdir
	print dircmd
	os.system(dircmd)

infilelist = glob(infiles)
keywords = []

for fname in infilelist:
	fkey = fname.split('_time')[0].replace('Hists_','')
	if not fkey in keywords:
		keywords.append(fkey)
	
for fkey in keywords:

	cmd = 'hadd -f '+tempfolder+'/'+fkey+'.root *'+fkey+'*.root'
	print cmd	
	os.system(cmd)

	#pause()
	fintermediate = TFile(tempfolder+'/'+fkey+'.root')
	keys = fintermediate.GetListOfKeys()	
	if len(keys)==0: 
		print 'couldnt make sense of', fkey
		continue
	ffinal = TFile(outdir+'/'+fkey+'.root', 'recreate')
	hHt = fintermediate.Get('hHt')
	nentries = hHt.GetEntries()
	for key in keys:
		name = key.GetName()
		if name=='hHt': continue
		hist = fintermediate.Get(name)
		hist.Scale(1.0*1000*lumi/nentries)
		ffinal.cd()
		hist.Write()
	fintermediate.Close()
	print 'just created', ffinal.GetName()
	ffinal.Close()	
	