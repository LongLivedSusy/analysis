from ROOT import *
from utils import *
import sys

gStyle.SetOptStat(0)
gROOT.SetBatch(1)

mkpdfs = False

try: dtmode = sys.argv[1]
except:	dtmode = 'PixOrStrips'

try: smear = sys.argv[2]
except: smear = 'Yes'


UseFits = True

print 'dtmode', dtmode
if dtmode == 'PixOnly': 
	PixMode = True
	PixStripsMode = False
	CombineMode = False
elif dtmode == 'PixAndStrips': 
	PixMode = False
	PixStripsMode = True
	CombineMode = False	
else:
	PixMode = False
	PixStripsMode = False
	CombineMode = True
	print 'cant do combine mode'
	exit(0)	
	

#from launchcomputekappa.sh: 
#python tools/PlotKappaClosureAndDataSplit.py PixAndStrips && python tools/PlotKappaClosureAndDataSplit.py PixOnly
useAllForDYJets = True
if PixMode:
	fTTJets = TFile('usefulthings/KappaSummer16.TTJets_PixOnly_'+smear+'ZSmear.root')
	fWJetsToLL = TFile('usefulthings/KappaSummer16.WJets_PixOnly_'+smear+'ZSmear.root')
	#fWJetsToLL = TFile('usefulthings/KappaDYJets_PixOnly.root')
	if useAllForDYJets: fMethodMC = TFile('usefulthings/KappaSummer16.AllMC_PixOnly_'+smear+'ZSmear.root')
	else: fMethodMC = TFile('usefulthings/KappaSummer16.DYJets_PixOnly_'+smear+'ZSmear.root')
	fMethodDataList = [TFile('usefulthings/KappaRun2016_PixOnly_'+smear+'ZSmear.root')]
	fMethodDataList = [TFile('usefulthings/KappaSummer16.DYJets_PixOnly_'+smear+'ZSmear.root')]
if PixStripsMode:
	fTTJets = TFile('usefulthings/KappaSummer16.TTJets_PixAndStrips_'+smear+'ZSmear.root')
	fWJetsToLL = TFile('usefulthings/KappaSummer16.WJets_PixAndStrips_'+smear+'ZSmear.root')
	#fWJetsToLL = TFile('usefulthings/KappaDYJets_PixAndStrips.root')
	if useAllForDYJets: fMethodMC = TFile('usefulthings/KappaSummer16.AllMC_PixAndStrips_'+smear+'ZSmear.root')
	else: fMethodMC = TFile('usefulthings/KappaSummer16.DYJets_PixAndStrips_'+smear+'ZSmear.root')	
	fMethodDataList = [TFile('usefulthings/KappaRun2016_PixAndStrips_'+smear+'ZSmear.root')]
	#fMethodDataList = [TFile('usefulthings/KappaSummer16.DYJets_PixAndStrips_'+smear+'ZSmear.root')]	
	#fMethodDataList = [TFile('usefulthings/KappaRun2016B.root'), TFile('usefulthings/KappaRun2016D.root'), TFile('usefulthings/KappaRun2016G.root'), TFile('usefulthings/KappaRun2016.root')]	


fWJetsToLL.ls()
names_ = []
for key in fWJetsToLL.GetListOfKeys():
	names_.append(key.GetName())
	
#fnew = TFile('ClosureKappaWithData_'+dtmode+'.root', 'recreate')
fnew = TFile('ClosureKappaWithData_'+dtmode+'_'+fTTJets.GetName().split('_')[-1], 'recreate')

c1 = mkcanvas('c1')
#c1.SetLogy()
#c1.SetLogx()
counter = 0
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
	if UseFits: funcWJetsToLL = fWJetsToLL.Get('f1'+name)
	
	#hTTJets = fTTJets.Get(name)
	#if UseFits: funcTTJets = fTTJets.Get('f1'+name)
	#hTTJets.SetLineColor(kGreen+2)
	#if UseFits: funcTTJets.SetLineColor(kGreen+2)	
	
	mname = name.replace('Gen','')	
	hMethodMC = fMethodMC.Get(mname)
	if UseFits: funcMethodMC = fMethodMC.Get('f1'+mname)

	xrangemax = min(500, hWJetsToLL.GetXaxis().GetBinLowEdge(hWJetsToLL.GetXaxis().GetNbins()))
	print 'arrived at xrangemax', xrangemax
	leg = mklegend(x1=.41, y1=.69, x2=.89, y2=.87)
	hWJetsToLL.GetXaxis().SetRangeUser(0,xrangemax)
	#hWJetsToLL.GetYaxis().SetRangeUser(0.0000001,0.1)
	dmax = fMethodDataList[0].Get(mname).GetMaximum()
	hWJetsToLL.GetYaxis().SetRangeUser(0*hWJetsToLL.GetMinimum(),2*max(hWJetsToLL.GetMaximum(),dmax))
	hWJetsToLL.Draw()
	hWJetsToLL.Write()
	#c1.Update()
	#pause()		
	
		
	#hTTJets.GetXaxis().SetRangeUser(0,xrangemax)
	#hTTJets.GetYaxis().SetRangeUser(0.000001,2)
	#hTTJets.Draw('same e0')
	
		
	if UseFits: funcWJetsToLL.Draw('same')
	leg.AddEntry(hWJetsToLL, 'MC Truth (W+Jets)')
	
	#if UseFits: funcTTJets.Draw('same')
	#leg.AddEntry(hTTJets, 'MC Truth (t#bar{t}+Jets)')
		
	hMethodMC.Draw('same e0')
	hMethodMC.Write()
	if UseFits: funcMethodMC.Draw('same')
	leg.AddEntry(hMethodMC, 'MC Tag and Probe')
		
	
	for iFile, fMethodData in enumerate(fMethodDataList):
		MethodData = fMethodData.Get(mname)
		if UseFits: funcMethodData = fMethodData.Get('f1'+mname)	
		MethodData.Draw('same')
		#MethodData.Write()
		if UseFits: 
			funcMethodData.Draw('same')
			funcUp = funcMethodData.Clone()
			funcUp.SetLineColor(kYellow)
			print dir(funcUp)
			funcUp.SetParameter(0,funcMethodData.GetParameters()[0]+funcMethodData.GetParError(0))
			funcUp.SetParameter(1,funcMethodData.GetParameters()[1]+funcMethodData.GetParError(1))
			funcUp.SetParameter(2,funcMethodData.GetParameters()[2]+funcMethodData.GetParError(2))						
			funcUp.Draw('same')
		MethodData.SetLineColor(kBlack+iFile)
		MethodData.SetMarkerColor(kBlack+iFile)
		if UseFits: funcMethodData.SetLineColor(kBlack+iFile)
		yearstr = fMethodData.GetName().split('/')[-1].split('.root')[0].replace('Kappa','').split('_')[0]
		if 'El' in name: leg.AddEntry(MethodData, yearstr+' Tag and Probe')
		if 'Mu' in name: leg.AddEntry(MethodData, yearstr+' Tag and Probe')			

	leg.Draw()
	stamp()	
	tl.DrawLatex(.2,.8,name.split('_')[-1].replace('eta','#eta=').replace('to','-'))
	if 'hMu' in name: 
		tl.DrawLatex(.2,.74,'muons')	
	if 'hEl' in name: 
		tl.DrawLatex(.2,.74,'electrons')
	tl.DrawLatex(.2,.69,dtmode.replace('And','+').replace('Only','-only').replace('Pix','pix').replace('Strips','strips'))
	
	c1.Update()
	
	
	#pause()
	
	
	fnew.cd()
	c1.Write(name.replace('hGen','c_').replace('.','p'))
	#MethodMC.Write()
	namypoo = 'pdfs/closure/tpkappa/'+name.replace('hGen','kappa').replace('.','p')+'_'+dtmode+'.pdf'
	if mkpdfs: c1.Print(namypoo)
	


print 'just created'
import os
print os.getcwd()+'/'+fnew.GetName()
fnew.Close()
