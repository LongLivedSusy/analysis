from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep
lumi = 35.9 #just for labeling. this weightw as already applied
#must agree with lumi in merged...py!


mycutedatatest = False
if mycutedatatest: datamc = 'data'
else: datamc = 'MC'

biggerNormbox = False
redoBinning = binningAnalysis
redoBinning['DeDxAverage'] = [21,0,7]
redoBinning['TrkPt'] = [30,0,300]
makefolders = False

phase = 0

drawhists = True


	

if phase==0:	
	if mycutedatatest: fCentralMC = 'output/totalweightedbkgsDataDrivenSingleElDataNoSmear.root'#for my cute
	else:fCentralMC = 'output/totalweightedbkgsDataDrivenMCSmearLeps4ZedFalse.root'
	#fCentralMC = 'output/mediumchunks/TTJets_SingleLeptFromTbar_SmearLeps4ZedFalse.root'
	#fCentralMC = 'testWJHT100.root'
	#fCentralMC = 'output/bigchunks/WJetsSmearLeps4ZedTrue.root'
	#fCentralMC = 'output/bigchunks/TTJetsSmearLeps4ZedTrue.root'
	#fCentralMC = 'output/mediumchunks/WJetsToLNu_HT-100To200SmearLeps4ZedTrue.root'
	#fCentralMC = 'output/totalweightedbkgsNoSmearedKappa.root'
	#fCentralMC = 'test.root'
	listOfVariationFilenames = []

if phase==1:
	fCentralMC = 'output/totalweightedbkgsDataDrivenMCPhase1.root'
	listOfVariationFilenames = ['output/totalweightedbkgsTrueKappaPhase1.root']	
listOfVariationFiles = []
for variationFileName in listOfVariationFilenames: listOfVariationFiles.append(TFile(variationFileName))
variationColors = [kBlue-1, kBlue, kBlue+1]

drawVariations = True
usePredictionWithClosureCorrection = False
CombineLeptons_ = True
			


infile = TFile(fCentralMC)
infile.ls()

fout = 'closureMoh_phase'+str(phase)+'.root'
if mycutedatatest: fout = fout.replace('.root','_cute.root')

fnew = TFile(fout,'recreate')

c1 = mkcanvas('c1')
		
keys = infile.GetListOfKeys()

hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	if 'Fake' in name: continue
	#if not ('DeDxAverage' in name or 'BinNumber' in name): continue
	
	if CombineLeptons_: 
		if not ('Control' in name.split('_')[-1] and 'hEl'==name[:3]): continue# and 'hElBaseline' in name): continue
		lepname = 'candidate (el, #mu, or #pi^{#pm})'
	else: 
		if not ('Control' in name.split('_')[-1]): continue
		if 'hEl'==name[:3]: lepname = 'el'
		if 'hMu'==name[:3]: lepname = '#mu'
		if 'hPi'==name[:3]: lepname = '#pi^#pm/k^#pm'		

	if 'MohSB' in name: continue
	
	
	
	
	controlname = name
	hControl = infile.Get(controlname)	
	hControl.SetTitle('single '+lepname)
	truthname = controlname.replace('Control','Truth')
	print 'starting out on hist', truthname
	hTruth = infile.Get(truthname)
	hTruth.SetTitle('MC observed (prompt)')
	
	normnameNum     = truthname.replace('MohST','').replace('_','MohSB_')
	controlnameNorm = controlname.replace('MohST','').replace('_','MohSB_')
	hNormTruth = infile.Get(normnameNum)
	hControlNorm = infile.Get(controlnameNorm)	
	
	print 'going for', normnameNum
	if CombineLeptons_: 
		hControl.Add(infile.Get(name.replace('hEl','hMu')))
		hControl.Add(infile.Get(name.replace('hEl','hPi')))
		hTruth.Add(infile.Get(truthname.replace('hEl','hMu')))
		hTruth.Add(infile.Get(truthname.replace('hEl','hPi')))	
		hNormTruth.Add(infile.Get(normnameNum.replace('hEl','hMu')))
		hNormTruth.Add(infile.Get(normnameNum.replace('hEl','hPi')))		
		hControlNorm.Add(infile.Get(controlnameNorm.replace('hEl','hMu')))
		hControlNorm.Add(infile.Get(controlnameNorm.replace('hEl','hPi')))
				
		#hTruth.Add(infile.Get(truthname.replace('hEl','hFake')))
		
	
	#hTruth.Draw()
	#c1.SetLogy()
	#c1.Update()
	#pause()	
	
	if 'DeDxAverage' in name and False:#this might be about Moh! 
			hTruth.Add(hNormTruth)
			hControl.Add(hControlNorm)
			if zone==zoneOfDedx[1]:
				hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2])))
				hControl.Add(infile.Get(name.replace(zone,zoneOfDedx[2])))
				if CombineLeptons_:				
					hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2]).replace('hEl','hMu')))
					hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2]).replace('hEl','hPi')))					
					
					hControl.Add(infile.Get(controlname.replace(zone,zoneOfDedx[2]).replace('hEl','hMu')))
					hControl.Add(infile.Get(controlname.replace(zone,zoneOfDedx[2]).replace('hEl','hPi')))										
			
			
			#hTruth = infile.Get(truthname.replace(zone,zoneOfDedx[0]))
			#hControl = infile.Get(controlname.replace(zone,zoneOfDedx[0]))
			a = 1
	if 'BinNumber' in name and False:# or 'DeDxAverage' in name:
		hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2])))
		hControl.Add(infile.Get(controlname.replace(zone,zoneOfDedx[2])))
		if CombineLeptons_:
			hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2]).replace('hEl','hMu')))
			hControl.Add(infile.Get(controlname.replace(zone,zoneOfDedx[2]).replace('hEl','hMu')))
			hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2]).replace('hEl','hMu')))
			hControl.Add(infile.Get(controlname.replace(zone,zoneOfDedx[2]).replace('hEl','hMu')))			
		
		

	
			
	hMethod = hControl.Clone(controlname)#.replace('Control','Method'))
	
	
	if biggerNormbox or 'DeDxAverage' in name:
		b = hControlNorm.Integral()
		c = hNormTruth.Integral()
		if b>0: hMethod.Scale(c/b)	
		hMethod.SetLineWidth(4)		
	else:
		hMethod.Divide(hControlNorm)
		hMethod.Multiply(hNormTruth)	
	
	if 'hMu'==name[:3]: 
		hMethod.SetLineColor(kViolet+2)
		hControl.SetLineColor(kRed+2)
	elif 'hPi'==name[:3]:
		hMethod.SetLineColor(kOrange+1)
		hControl.SetLineColor(kOrange)	
	else:
		hMethod.SetLineColor(kGreen+3)
		
		
		
		
	kinvar = name.replace('Control','').replace('Truth','').replace('Method','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
			
	if len(redoBinning[kinvar])!=3: 
		nbins = len(redoBinning[kinvar])-1
		newxs = array('d',redoBinning[kinvar])
	else:
		newbinning = []
		print kinvar, name
		stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
		for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
		nbins = len(newbinning)-1
		newxs = array('d',newbinning)
	hTruth = hTruth.Rebin(nbins,'',newxs)
	if mycutedatatest: 
		if kinvar=='InvMass':
			xaxt = hTruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: hTruth.SetBinContent(ibin, 0)
		if kinvar=='LepMT':
			xaxt = hTruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=90: hTruth.SetBinContent(ibin, 0)				
	hMethod = hMethod.Rebin(nbins,'',newxs)
	hControl = hControl.Rebin(nbins,'',newxs)		
	hNormTruth = hNormTruth.Rebin(nbins,'',newxs)
	hControlNorm = hControlNorm.Rebin(nbins,'',newxs)
		
	hMethod.SetTitle('prediction')
	shortname = name.replace('Control','').replace('Truth','').replace('Method','')
	if CombineLeptons_: shortname = shortname.replace('hEl','hObj')[1:]
	varname = shortname.split('_')[-1]
	xax = hMethod.GetXaxis()
	hControl.GetXaxis().SetTitle(namewizard(varname))
	hTruth.GetXaxis().SetTitle(namewizard(varname))
	hMethod.GetXaxis().SetTitle(namewizard(varname))    
	

        	
	#leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	leg = mklegend(x1=.5, y1=.5, x2=.99, y2=.8, color=kWhite)
	legname = 'single-lep'
	if 'hEl' in name: legname = legname.replace('lep','electron')
	if 'hMu' in name: legname = legname.replace('lep','muon')
	leg.AddEntry(hControl,'prompt-CR moh>1','lp')
	#hMethod.Scale()
	themax = 1000000*max([hMethod.GetMaximum(),hControl.GetMaximum(),hTruth.GetMaximum()])
	hMethod.GetYaxis().SetRangeUser(0.01,themax)
	#hMethod.SetFillStyle(1001)
	hMethod.SetFillColor(hMethod.GetLineColor()-1)	
	hTruth.GetYaxis().SetRangeUser(0.01,themax)
	hControl.GetYaxis().SetRangeUser(0.01,themax)
	hMethod.SetLineColor(kGray+2)
	fnew.cd()
	plotname = shortname.replace('_','')
	c1 = mkcanvas('c_'+plotname)
	if makefolders:
		fnew.mkdir(shortname.replace('_',''))
		if 'Bin' in name: 
			hMethodCorrected, hVarCorrectionFactor = makeClosureCorrectionAndUncertainty(hMethod, hTruth)
			fnew.cd()
			hMethodCorrected.Write()
			if usePredictionWithClosureCorrection:
				fnew.cd(plotname) 
				hVarCorrectionFactor.Write()		
				fnew.cd('../')				
				#for ibin in range(1, xax.GetNbins()+1): print 'after', ibin, hVarCorrectionFactor.GetBinContent(ibin)
				hMethod = hMethodCorrected
	

	hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,hTruth,[hMethod],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	#hratio.GetYaxis().SetRangeUser(0.0,2.5)
	hratio.GetYaxis().SetRangeUser(-0.1,2.6)	
	hratio.GetYaxis().SetTitle('(B/A*C)/D')
	#hratio.GetYaxis().SetRangeUser(-3,3)		
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	c1.cd(2)
	c1.SetLogy()
	c1.Update()
	c1.cd(1)
	hMethod.SetTitle('')
	hTruth.SetTitle('')	

	#leg.AddEntry(hControl,'Method','l')
	leg.AddEntry(hControlNorm,'prompt-CR 0 moh','l')
	leg.AddEntry(hNormTruth,'answer 0 moh','l')
	hControl.Draw('same')	
	hControlNorm.SetLineColor(hControl.GetLineColor()+1)	
	hControlNorm.Draw('same')
	hNormTruth.SetLineColor(kGray)
	hNormTruth.Draw('same')
	
	hMethod.SetLineWidth(3)
	hMethod.Draw('same')
						
	c1.Update()
	fnew.cd()
	c1.Write()
	if 'BinNumber' in name:
		hTruth.Write(truthname)
		hMethod.Write(truthname.replace('Truth','Method'))		
	#hTruth.Write()
	#hMethod.Write()
	
	#c1.Print('pdfs/closure/prompt-bkg/'+shortname.replace('_','')+'.pdf')
	
	clist.append(c1)
	#c1.Delete()
	hratios.append([hratio, hmethodsyst])
	c1.Update()
	#pause()

	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'test c'



