from ROOT import *
from utils import *
import os, sys


#f = TFile('PromptBkgHist_Summer16.WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1AOD_70000-F85B7AB3-5BC6-E611-909F-02163E013D4E_-SmearLeps4ZedTrue-nfpj100.root')
f = TFile('test.root')
#f = TFile('output/totalweightedbkgsDataDrivenMCSmearLeps4ZedTrue.root')

f.ls()
keys = f.GetListOfKeys()

colors = [1,2,4, kTeal-5, kYellow, kOrange+1, kGreen-2, kGreen-1, kGreen, kGreen+1, kGreen+2]
c1 = mkcanvas()
c1.SetLogy()
targets = []
for key in keys:
	name = key.GetName()
	#if not 'Pt' in name: continue
	#if '10to15' in name: continue
	#if '15to20' in name: continue	
	if not ('DeDxAverageControl' in name): continue# or 'DeDxAverageTruth' in name): continue

	if not 'Zone0p0To3p1' in name: continue
	#if not 'hElBaseline' in name: continue
	#if not 'To' in name: continue
	
	print 'doing', name
	hist = f.Get(name).Clone()
	hist.Add(f.Get(name.replace('Zone0p0To3p1','Zone3p1To5p0')))
	hist.Add(f.Get(name.replace('Zone0p0To3p1','Zone5p0To99')))	
	hist.Rebin(4)
	if hist.Integral()==0: continue
	hist.Scale(1.0/hist.Integral())
	targets.append(hist)
	hist.Draw('hist')
	h2 = f.Get(name.replace('Control','Truth'))
	h2.Add(f.Get(name.replace('Control','Truth').replace('Zone0p0To3p1','Zone3p1To5p0')))
	h2.Add(f.Get(name.replace('Control','Truth').replace('Zone0p0To3p1','Zone5p0To99')))		
	h2.Rebin(4)	
	h2.Scale(1.0/h2.Integral())
	h2.Draw('same')
	c1.Update()
	pause()
	

leg = mklegend()
arg = 'hist e'
for it, target in enumerate(targets):
	target.SetLineColor(colors[it])
	target.Rebin(5)	
	target.Draw(arg)
	leg.AddEntry(target,target.GetName())
	arg = 'hist same e'
	print target.GetName(), target.GetRMS()
leg.Draw()
	
c1.Update()
pause()
f.Close()
	


	
