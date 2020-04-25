import os, sys
from ROOT import *
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')

redoBinning = binningAnalysis
sourcename = 'output/totalweightedbkgsDataDrivenDataNoSmear.root'
sourcename = 'output/totalweightedbkgsDataDrivenMCYesZSmear.root'
sourcename = 'output/totalweightedbkgsDataDrivenMCSmearLeps4ZedFalse.root'
sourcename = 'closureAbcd_phase0.root'
fofinterest = TFile(sourcename)


fofinterest.ls()

fnew = TFile('prompt-bg-results.root','recreate')
vars = ['BinNumber']#, 'Log10DedxMass', 'NJets', 'Mht', 'DeDxAverage']

for var in vars:
	kinvar = var.replace('Method','').replace('Truth','').replace('Control','')
	hElectron = fofinterest.Get('hElBaseline_'+var+'Method')
	
	print 'collecting', 'hElBaseline_'+var+'Method'
	
	hTruth = fofinterest.Get('hElBaseline_'+var+'Truth')
	
	print 'hElectron.GetXaxis().GetBinLowEdge(1)', hElectron.GetXaxis().GetBinLowEdge(1)
	hists = [hElectron, hTruth]
	for hist in hists:
		xax = hist.GetXaxis()
		#hist.SetBinContent(xax.FindBin(0.1), 0)
		if len(redoBinning[kinvar])!=3:
			nbins = len(redoBinning[kinvar])-1
			newxs = array('d',redoBinning[kinvar])
			hist = hist.Rebin(nbins,'',newxs)
		else:
			newbinning = []
			stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
			for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
			nbins = len(newbinning)-1
			newxs = array('d',newbinning)
			hist = hist.Rebin(nbins,'',newxs)
			print 'hist.GetXaxis().GetBinLowEdge(1)', hist.GetXaxis().GetBinLowEdge(1)

	fnew.cd()
	hElectron = hists[0]
	hTruth = hists[1]
	
	
	
	print 'hElectron.GetXaxis().GetBinLowEdge(1)', hElectron.GetXaxis().GetBinLowEdge(1)
	thing = hElectron.GetName().replace('Zone2p1to4p0','')
	thing = thing.replace('Control','Method')	
	hElectron.Write(thing)

	#hTruth.Write()
	


print 'just created', fnew.GetName()

fnew.Close()