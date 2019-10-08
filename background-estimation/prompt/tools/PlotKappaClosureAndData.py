from ROOT import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')

gStyle.SetOptStat(0)
gROOT.SetBatch(1)

fWJetsToLL = TFile('usefulthings/KappaWJets.root')
fMethodMC = TFile('usefulthings/KappaDYJets.root')

#fMethodDataList = [TFile('usefulthings/KappaRun2016B.root'), TFile('usefulthings/KappaRun2016D.root'), TFile('usefulthings/KappaRun2016G.root'), TFile('usefulthings/KappaRun2016H.root')]
fMethodDataList = [TFile('usefulthings/KappaRun2016.root')]
#fMethodData = TFile('usefulthings/KappaRun2016B.root')


fWJetsToLL.ls()
names_ = []
for key in fWJetsToLL.GetListOfKeys():
	names_.append(key.GetName())
	
fnew = TFile('ClosureKappaWithData.root', 'recreate')

c1 = mkcanvas('c1')
c1.SetLogy()
#c1.SetLogx()
for name in names_:
	if not 'hGen' in name: continue
	if name[0]=='c' or name[0]=='f': continue
	print name
	'''
	hWJetsToLL = fWJetsToLL.Get('hGenElProbePtKappa_eta0to1.4442')
	funcWJetsToLL = fWJetsToLL.Get('f1hGenElProbePtKappa_eta0to1.4442')
	MethodMC = fMethodMC.Get('hElProbePtKappa_eta0to1.4442')
	funcMethodMC = fMethodMC.Get('f1hElProbePtKappa_eta0to1.4442')
	MethodData = fMethodData.Get('hElProbePtKappa_eta0to1.4442')
	funcMethodData = fMethodData.Get('f1hElProbePtKappa_eta0to1.4442')
	'''
	hWJetsToLL = fWJetsToLL.Get(name)
	funcWJetsToLL = fWJetsToLL.Get('f1'+name)
	mname = name.replace('Gen','')	
	MethodMC = fMethodMC.Get(mname)
	funcMethodMC = fMethodMC.Get('f1'+mname)

	leg = mklegend(x1=.47, y1=.66, x2=.94, y2=.82)
	hWJetsToLL.GetXaxis().SetRangeUser(0,800)
	hWJetsToLL.GetYaxis().SetRangeUser(0.0001,2)
	hWJetsToLL.SetLineColor(kBlue)
	hWJetsToLL.Draw('hist')
	funcWJetsToLL.Draw('same')
	leg.AddEntry(hWJetsToLL, 'MC Truth (W+Jets)')
	MethodMC.Draw('same')
	funcMethodMC.Draw('same')
	leg.AddEntry(MethodMC, 'MC Tag and Probe (DY+Jets)')
	
	for iFile, fMethodData in enumerate(fMethodDataList):
		MethodData = fMethodData.Get(mname)
		funcMethodData = fMethodData.Get('f1'+mname)	
		MethodData.Draw('same')
		funcMethodData.Draw('same')
		MethodData.SetLineColor(kGreen-2+iFile)
		MethodData.SetMarkerColor(kGreen-2+iFile)
		funcMethodData.SetLineColor(kGreen-2+iFile)
		yearstr = fMethodData.GetName().split('/')[-1].split('.root')[0].replace('Kappa','')
		if 'El' in name: leg.AddEntry(MethodData, yearstr+' Tag and Probe (SingleEl)')
		if 'Mu' in name: leg.AddEntry(MethodData, yearstr+' Tag and Probe (SingleMu)')	

	leg.Draw()
	tl.DrawLatex(.2,.8,name.split('_')[-1].replace('eta','#eta=').replace('to','-'))
	if 'Mu' in name: tl.DrawLatex(.2,.74,'muons')	
	if 'El' in name: tl.DrawLatex(.2,.74,'electrons')		
	stamp()
	c1.Update()
	fnew.cd()
	c1.Write(name.replace('hGen','c_').replace('.','p'))
	c1.Print('pdfs/closure/tpkappa/'+name.replace('hGen','kappa').replace('.','p')+'.pdf')


print 'just created'
import os
print os.getcwd()+'/'+fnew.GetName()
fnew.Close()
