from ROOT import *
import os, sys
from glob import glob
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
import time

lumi = 137

binningAnalysis['MatchedCalo'] = [100,0,100]
binningAnalysis['DtStatus'] = [6,-3,3]
binningAnalysis['FakeCrNr'] = [6,-3,3]
redoBinning = binningAnalysis

try: infiles = sys.argv[1]
except: infiles = 'holdingbay/Hists*.root'

try: outdir = sys.argv[2]
except: 
	#outdir = '../interpretation/HistsBkgObsSig/Piano/Signal/'
	outdir = '/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Signal/T1qqqqLL'
	outdir = '/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Signal/T2btLL'
	outdir = '/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Xenon/v2/Signal/T2btLL'	


bayname = infiles.split('/')[0]

tempfolder = str(time.time())
os.system('mkdir '+tempfolder)

if not os.path.isdir(outdir):
	dircmd = 'mkdir -p '+outdir
	print dircmd
	os.system(dircmd)

infilelist = glob(infiles)
keywords = []

for fname in infilelist:
	fkey = fname.split('/')[-1].split('_time')[0].replace('Hists_','')
	fkey = fkey.split('_pu')[0]
	if not fkey in keywords:
		keywords.append(fkey)


for fkey in keywords:

	cmd = 'python tools/ahadd.py -f '+tempfolder+'/'+fkey+'.root '+bayname+'/*'+fkey+'_*.root'
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
		if name=='hHt': 
			hHt = fintermediate.Get(name)
			ffinal.cd()
			hHt.Write()
			continue
		if name=='hHtWeighted': 
			hHt = fintermediate.Get(name)
			ffinal.cd()
			hHt.Write()		
			continue
		hist = fintermediate.Get(name)
		
		
		if 'BinNumber' in name:
			hist = merge2dtbins(hist)
				
		
		kinvar = name.replace('Method','').replace('Truth','').replace('Method','')
		kinvar = kinvar[kinvar.find('_')+1:]
		print 'got kinvar', kinvar, 'name', name
			
		if len(redoBinning[kinvar])!=3: 
			nbins = len(redoBinning[kinvar])-1
			newxs = array('d',redoBinning[kinvar])
			hist = hist.Rebin(nbins,'',newxs)	
		else:
			newbinning = []
			print kinvar, name
			stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
			for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
			nbins = len(newbinning)-1
			newxs = array('d',newbinning)
			hist = hist.Rebin(nbins,'',newxs)
		
		hist.Scale(1.0*1000*lumi/nentries)
		ffinal.cd()
		hist.Write()
	fintermediate.Close()
	print 'just created', ffinal.GetName()
	ffinal.Close()	
	
	
	
	
	
	

	