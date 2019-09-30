from ROOT import *
import os, sys

fraw_datadriven_name = 'prompt-bg-results.root'
fraw_datadriven = TFile(fraw_datadriven_name)
fraw_datadriven.ls()

print '=='*20

ffrog_name = 'plots.root'
ffrog = TFile(ffrog_name)
ffrog.ls()

fnew = TFile('prompt-bg-results_repaired.root','recreate')

keys = fraw_datadriven.GetListOfKeys()



for key in keys:
	name = key.GetName()
	obj = fraw_datadriven.Get(name)	
	obj.SetDirectory(0)
	print 'trying to process', name, obj
	if not 'hEl' in name: 		
		fnew.cd()
		obj.Write(name)
		continue
	else:
		objfrog = ffrog.Get(name.replace('Method','Truth'))
		objfrog.SetDirectory(0)
		xax = obj.GetXaxis()
		nbins = xax.GetNbins()
		for ibin in range(1, nbins+1):
			newest = max(objfrog.GetBinContent(ibin), obj.GetBinContent(ibin))
			obj.SetBinContent(ibin, newest)
			fnew.cd()
		obj.Write()
			
print 'just created', fnew.GetName()
fraw_datadriven.Close()
ffrog.Close()
fnew.Close()
exit(0)
