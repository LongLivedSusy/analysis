from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep
lumi = 135 #just for labeling. this weightw as already applied
#must agree with lumi in merged...py!


redoBinning = binningAnalysis
#redoBinning = binning
makefolders = False

phase = 0

drawhists = True

if phase==0:
	fCentralMC = 'output/totalweightedbkgsDataDrivenMCYesZSmear.root'
	#fCentralMC = 'output/totalweightedbkgsNoSmearedKappa.root'
	#fCentralMC = 'test.root'
	#fCentralMC = 'output/totalweightedbkgsTrueKappa.root'
	listOfVariationFilenames = ['output/totalweightedbkgsDataDrivenMCNoZSmear.root']
	#listOfVariationFilenames = ['output/totalweightedbkgsTrueKappa.root']
	#listOfVariationFilenames = ['output/totalweightedbkgsNoSmearedKappa.root']#,'output/totalweightedbkgsTrueKappa.root']
	#listOfVariationFilenames = []
if phase==1:
	fCentralMC = 'output/totalweightedbkgsDataDrivenMCPhase1.root'
	listOfVariationFilenames = ['output/totalweightedbkgsTrueKappaPhase1.root']	
#listOfVariationFilenames = []
listOfVariationFiles = []
for variationFileName in listOfVariationFilenames: listOfVariationFiles.append(TFile(variationFileName))
variationColors = [kBlue-1, kBlue, kBlue+1]

drawVariations = True
usePredictionWithClosureCorrection = False
CombineLeptons_ = True
			


testscale = 1# = lumi*1000


infile = TFile(fCentralMC)
infile.ls()

fout = 'closure_phase'+str(phase)+'.root'

fnew = TFile(fout,'recreate')

c1 = mkcanvas('c1')

applyClosureCorrection = False
def makeClosureCorrectionAndUncertainty(hMethod, hTruth):
	hCorrectedPrediction = hMethod.Clone('hCorrectedPrediction_'+hMethod.GetName())
	hCorrectionFactor = hMethod.Clone('hCorrectionFactor_'+hMethod.GetName())
	hCorrectedPrediction.Reset()
	hCorrectionFactor.Reset()	
	xax = hTruth.GetXaxis()
	for ibin in range(1, xax.GetNbins()+1):
		nmeth = hMethod.GetBinContent(ibin)
		ntrut = hTruth.GetBinContent(ibin)
		newcv = (nmeth+ntrut)/2.0
		hCorrectedPrediction.SetBinContent(ibin, newcv)
		hCorrectedPrediction.SetBinError(ibin, TMath.Sqrt(pow(hMethod.GetBinError(ibin),2)+pow(abs(newcv-ntrut),2)))
		if (nmeth>0 and ntrut>0): 
			hCorrectionFactor.SetBinContent(ibin, 1.0*newcv/nmeth)
			print 'before ibin', ibin, 1.0*newcv/nmeth
			hCorrectionFactor.SetBinError(ibin, 1.0*abs(newcv-ntrut)/newcv)
		else: 
			hCorrectionFactor.SetBinContent(ibin, 1.0)
			hCorrectionFactor.SetBinError(ibin, 0.0)
	return hCorrectedPrediction, hCorrectionFactor
		
keys = infile.GetListOfKeys()

hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	
	if 'LowHt' in name or 'HighHt' in name: continue
	if 'Fake' in name: continue
	if CombineLeptons_: 
		if not ('Control' in name.split('_')[-1] and 'hEl'==name[:3]): continue# and 'hElBaseline' in name): continue
		###if 'PixOnly' in name or 'PixAndStrips' in name: continue# for sharing
		lepname = 'candidate (el, #mu, or #pi^{#pm})'
	else: 
		if not ('Control' in name.split('_')[-1]): continue
		if 'hEl'==name[:3]: lepname = 'el'
		if 'hMu'==name[:3]: lepname = '#mu'
		if 'hPi'==name[:3]: lepname = '#pi^#pm/k^#pm'		
	#if 'Ttbar' in name: continue
	hVarControl = infile.Get(name)
	if CombineLeptons_: 
		hVarControl.Add(infile.Get(name.replace('hEl','hMu')))
		hVarControl.Add(infile.Get(name.replace('hEl','hPi')))
		#hVarControl.Add(infile.Get(name.replace('hEl','hFake')))		
	hVarControl.SetTitle('single '+lepname)	
	truthname = name.replace('barControl','barBarf')
	truthname = truthname.replace('Control','Truth')
	truthname = truthname.replace('barBarf','barControl')
	hVarTruth = infile.Get(truthname)
	hVarTruth.Scale(testscale)
	hVarTruth.SetTitle('MC observed (truth)')
	if CombineLeptons_: 
		mu2add = infile.Get(truthname.replace('hEl','hMu'))
		mu2add.Scale(testscale)
		hVarTruth.Add(mu2add)
		pi2add = infile.Get(truthname.replace('hEl','hPi'))
		pi2add.Scale(testscale)
		hVarTruth.Add(pi2add)
		#hVarTruth.Add(infile.Get(truthname.replace('hEl','hFake')))
			
			
	#if 'hPi' in name: hVarTruth.Add(infile.Get(truthname.replace('hPi','hFake')))###
	methodname = name.replace('barControl','barBarf')
	methodname = methodname.replace('Control','Method')
	methodname = methodname.replace('barBarf','barControl')
			
	hVarMethod = infile.Get(methodname)
	hVarMethod.Scale(testscale)
	if 'hMu'==name[:3]: 
		hVarMethod.SetLineColor(kViolet+2)
		hVarControl.SetLineColor(kRed+2)
	elif 'hPi'==name[:3]:
		hVarMethod.SetLineColor(kOrange+1)
		hVarControl.SetLineColor(kOrange)	
	else:
		hVarMethod.SetLineColor(kGreen+3)
	if CombineLeptons_: 
		h2add = infile.Get(methodname.replace('hEl','hMu'))
		h2add.Scale(testscale)
		hVarMethod.Add(h2add)
		h2add2 = infile.Get(methodname.replace('hEl','hPi'))
		h2add2.Scale(testscale)
		hVarMethod.Add(h2add2)
		hVarMethod.SetLineColor(kCyan-7)
		hVarControl.SetLineColor(kCyan+2)
	hVarMethod.SetTitle('weighted single '+lepname)
	shortname = name[1:].replace('Control','').replace('Truth','').replace('Method','')
	if CombineLeptons_: shortname = shortname.replace('El','Obj')
	varname = shortname.split('_')[-1]
	xax = hVarMethod.GetXaxis()
	hVarControl.GetXaxis().SetTitle(namewizard(varname))
	hVarTruth.GetXaxis().SetTitle(namewizard(varname))
	hVarMethod.GetXaxis().SetTitle(namewizard(varname))
		
	kinvar = name.replace('Method','').replace('Truth','').replace('Control','')
	kinvar = kinvar[kinvar.find('_')+1:]
	#print 'got kinvar', kinvar
	#pause()
	if len(redoBinning[kinvar])!=3: 
		nbins = len(redoBinning[kinvar])-1
		newxs = array('d',redoBinning[kinvar])
		hVarTruth = hVarTruth.Rebin(nbins,'',newxs)
		hVarMethod = hVarMethod.Rebin(nbins,'',newxs)
		hVarControl = hVarControl.Rebin(nbins,'',newxs)		
	else:
		newbinning = []
		print kinvar, name
		stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
		for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
		nbins = len(newbinning)-1
		newxs = array('d',newbinning)
		hVarTruth = hVarTruth.Rebin(nbins,'',newxs)
		hVarMethod = hVarMethod.Rebin(nbins,'',newxs)
		hVarControl = hVarControl.Rebin(nbins,'',newxs)		
        
        	
	leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	legname = 'single-lep'
	if 'hEl' in name: legname = legname.replace('lep','electron')
	if 'hMu' in name: legname = legname.replace('lep','muon')
	leg.AddEntry(hVarControl,'single-'+lepname,'lp')
	#hVarMethod.Scale()
	themax = 10000*max([hVarMethod.GetMaximum(),hVarControl.GetMaximum(),hVarTruth.GetMaximum()])
	hVarMethod.GetYaxis().SetRangeUser(0.001,themax)
	#hVarMethod.SetFillStyle(1001)
	hVarMethod.SetFillColor(hVarMethod.GetLineColor()-1)	
	hVarTruth.GetYaxis().SetRangeUser(0.01,themax)
	hVarControl.GetYaxis().SetRangeUser(0.01,themax)
	hVarMethod.SetLineColor(kGray+2)
	fnew.cd()
	plotname = shortname.replace('_','')
	c1 = mkcanvas('c_'+plotname)
	if makefolders:
		fnew.mkdir(shortname.replace('_',''))
		if 'Bin' in name: 
			hVarMethodCorrected, hVarCorrectionFactor = makeClosureCorrectionAndUncertainty(hVarMethod, hVarTruth)
			fnew.cd()
			hVarMethodCorrected.Write()
			if usePredictionWithClosureCorrection:
				fnew.cd(plotname) 
				hVarCorrectionFactor.Write()		
				fnew.cd('../')				
				#for ibin in range(1, xax.GetNbins()+1): print 'after', ibin, hVarCorrectionFactor.GetBinContent(ibin)
				hVarMethod = hVarMethodCorrected
			
	hvariations = []
	for f in listOfVariationFiles:
		hAlt = f.Get(methodname)
		hAlt.SetDirectory(0)
		hAlt.SetLineColor(kAzure)
		hAlt.Scale(testscale)
		hAlt.SetTitle('')
		if CombineLeptons_: 
			h2add = f.Get(methodname.replace('hEl','hMu'))
			h2add.Scale(testscale)
			hAlt.Add(h2add)
			#h2add2 = f.Get(methodname.replace('hEl','hPi'))
			#h2add2.Scale(testscale)
			#hAlt.Add(h2add2)			
		hAlt = hAlt.Rebin(nbins,'',newxs)
		hRatioVariation = hAlt.Clone()
		hRatioVariation.Divide(hVarMethod)
		fnew.cd()
		if makefolders: 
			fnew.cd(plotname)
			hAlt.Write(methodname+'variation')
			hRatioVariation.Write(methodname+'varyRatio')
			fnew.cd('../')
		hvariations.append(hAlt)
		for ibin in range(1, xax.GetNbins()+1): 
			olderr = hVarMethod.GetBinError(ibin)
			syst = abs(hVarMethod.GetBinContent(ibin)-hAlt.GetBinContent(ibin))
			hVarMethod.SetBinError(ibin, TMath.Sqrt(pow(olderr,2)+pow(syst,2)))

	#hratio = FabDraw(c1,leg,hVarTruth,[hVarMethod],datamc='MC',lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,hVarTruth,[hVarMethod],datamc='MC',lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	#hratio.GetYaxis().SetRangeUser(0.0,2.5)
	hratio.GetYaxis().SetRangeUser(-0.1,2.6)	
	hratio.GetYaxis().SetTitle('Events/bin')
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
	hVarMethod.SetTitle('')
	hVarTruth.SetTitle('')	
	hVarControl.SetTitle('')
	hVarControl.Scale(testscale)
	hVarControl.SetMarkerColor(hVarControl.GetLineColor())		
	hVarControl.SetMarkerStyle(23)
	hVarControl.SetLineColor(kWhite)
	hVarControl.Draw('same p')
	if drawVariations:
		for hvari in hvariations: 
			hvari.SetLineColor(kRed)
			hvari.Draw('same')
						
	c1.Update()
	fnew.cd()
	c1.Write()
	#hVarTruth.Write()
	#hVarMethod.Write()
	
	c1.Print('pdfs/closure/prompt-bkg/'+shortname.replace('_','')+'.pdf')
	
	clist.append(c1)
	#c1.Delete()
	hratios.append([hratio, hmethodsyst])
	c1.Update()
	#pause()

print 'test a'
	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'test c'



