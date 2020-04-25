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
lumi = 137.



datamc = 'MC'
dofakesidebandsubtraction = False


binning['MatchedCalo'] = [120,0,60]
binning['DtStatus'] = [6,-3,3]
binning['FakeCrNr'] = [6,-3,3]


redoBinning = binning
redoBinning['Met'] = [20,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['InvMass'] = [15,50,170]
redoBinning['ElPt'] = [5,0,300]
redoBinning['TrkEta'] = [5,0,3]
redoBinning['MuPt'] = redoBinning['ElPt']
redoBinning['DeDxAverage'] = [1.999999999,2,3.0,4.0,5.0,6.0,7.0]
redoBinning['DeDxAverage'] = [1.999999,2,4,7]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
redoBinning['TrkPt']=[5,0,200]
redoBinning['LepMT'] = binningAnalysis['LepMT']
redoBinning['Ht']=[10,0,1000]
redoBinning['MatchedCalo'] = [0,10,12,15,17,20,25,30,60]
makefolders = False
mycutedatatest = bool(datamc=='data')



phase = 0
phase = 1


if phase==0:	
	fCentralMC = 'test.root'
	fCentralMC = 'output/promptDataDrivenMCSummer16.root'
	#fCentralMC = 'PromptBkgHist_Summer16WJets.root'
	#fCentralMC = 'test.root'
	fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenMCSummer16_mcal15to20.root'
	if mycutedatatest: fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenRun2016_mcal15to20.root'
if phase==1: fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenMCFall17_mcal15to20.root'
	


infile = TFile(fCentralMC)
infile.ls()
keys = infile.GetListOfKeys()

hShapeShort = infile.Get('hPromptShortSElValidationZLL_MatchedCaloTruth').Clone('hShapeShort')##
if not mycutedatatest: hShapeShort.Add(infile.Get('hFakeShortSElValidationZLL_MatchedCaloTruth'))

hShapeLong = infile.Get('hPromptLongSElValidationZLL_MatchedCaloTruth').Clone('hShapeLong')##
if not mycutedatatest: hShapeLong.Add(infile.Get('hFakeLongSElValidationZLL_MatchedCaloTruth'))

shax = hShapeShort.GetXaxis()

calm = 20
calh = 25

calm = 10
calh = 15

calm = 15
calh = 20

binm = shax.FindBin(calm)
binh = shax.FindBin(calh)

low_over_high_short = hShapeShort.Integral(shax.FindBin(0),shax.FindBin(10)-1)/hShapeShort.Integral(binm,binh-1)
low_over_high_long = hShapeLong.Integral(shax.FindBin(0),shax.FindBin(10)-1)/hShapeLong.Integral(binm,binh-1)

fout = 'closureMatchedCalo_phase'+str(phase)+'.root'
if mycutedatatest: fout = fout.replace('.root','_cute.root')
fnew = TFile(fout,'recreate')


searchbinresults = {}
hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	
	if 'hFake' in name: continue
	
	
	if not 'Truth' in name: continue
	#if not 'Baseline' in name: continue
	if not 'CaloSideband' in name: continue
	if not 'hPrompt' in name: continue
	if 'FakeCr' in name: continue
	
	if 'Short' in name: low_over_high = low_over_high_short
	else: low_over_high = low_over_high_long
	
	kinvar = name.replace('Control','').replace('Truth','').replace('Method','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
	
	hsideband =   infile.Get(name).Clone()
	hsidebandfake=infile.Get(name.replace('hPrompt','hFake')).Clone()
	if not mycutedatatest: hsideband.Add(hsidebandfake)
	
	htruth = infile.Get(name.replace('CaloSideband','')).Clone()
	if mycutedatatest: 
		if kinvar=='InvMass':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: htruth.SetBinContent(ibin, 0)
		if kinvar=='LepMT':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=90: htruth.SetBinContent(ibin, 0)	
			
		
	if dofakesidebandsubtraction: 	
		print 'gonna subtract this thing', name.replace('hPrompt','hFake').replace('Truth','Method').replace('_','FakeCr_')
		hSidebandFakePrediction = infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method').replace('_','FakeCr_')).Clone()
		if not mycutedatatest: hSidebandFakePrediction.Add(infile.Get(name.replace('Truth','Method').replace('_','FakeCr_')))
		hsideband.Add(hSidebandFakePrediction,-1)
	
				
	hmethod = hsideband.Clone(hsideband.GetName().replace('Truth','Method'))
	hmethod_fakecontam = hsidebandfake.Clone(hsidebandfake.GetName().replace('Truth','Method'))



	if 'BinNumber' in name:
		hmethod_fakecontam = merge2dtbins(hmethod_fakecontam)
		hmethod = merge2dtbins(hmethod)
		hsideband = merge2dtbins(hsideband)
		htruth = merge2dtbins(htruth)

	
	if 'MatchedCalo' in name:
		dintHigh, dintLow = Double(), Double()
		integ_high = hmethod.IntegralAndError(binm,binh-1,dintHigh)
		hspecialAux = TH1F('hspecialMethod','hspecialMethod',1,0,1)
		hspecialAux.SetBinContent(1,integ_high)
		hspecialAux.SetBinError(1,dintHigh)		
		
		integ_high = hmethod_fakecontam.IntegralAndError(binm,binh-1,dintHigh)
		hspecialContamAux = TH1F('hspecialMethod','hspecialMethod',1,0,1)
		hspecialContamAux.SetBinContent(1,integ_high)
		hspecialContamAux.SetBinError(1,dintHigh)

		

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
	htruth = htruth.Rebin(nbins,'',newxs)
	hmethod = hmethod.Rebin(nbins,'',newxs)
	hmethod_fakecontam = hmethod_fakecontam.Rebin(nbins,'',newxs)
				
			
			
	if 'MatchedCalo' in name:
		shax2 = hspecialAux.GetXaxis() # this is the rebinned matchedcalo axis
		for ibin in range(1,shax2.GetNbins()+1):
			mcvalue = shax2.GetBinLowEdge(ibin)
			if mcvalue<10:
				oldcontent, olderror = hmethod.GetBinContent(ibin), hmethod.GetBinError(ibin)
				hspecialMethod = hspecialAux.Clone()
				hspecialMethod.Scale(low_over_high)
				print dintHigh, 'just scaled this puppy:', ibin, hspecialMethod.GetBinContent(ibin), hspecialMethod.GetBinError(ibin)
				hmethod.SetBinContent(ibin, hspecialMethod.GetBinContent(ibin))
				hmethod.SetBinError(ibin, hspecialMethod.GetBinError(ibin))
				
				hspecialMethod = hspecialContamAux.Clone()
				hspecialMethod.Scale(low_over_high)
				hmethod_fakecontam.SetBinContent(ibin, hspecialMethod.GetBinContent(ibin))
				hmethod_fakecontam.SetBinError(ibin, hspecialMethod.GetBinError(ibin))	
	else:
		hmethod.Scale(low_over_high)
		hmethod_fakecontam.Scale(low_over_high)
		
	if datamc=='MC': 
		if phase==0:
			htruth.SetTitle('fake obs. (Summer 16 MC)')	
			hmethod.SetTitle('pred. (Summer 16 MC)')		
		if phase==1:
			htruth.SetTitle('fake obs. (Fall 17 MC)')
			hmethod.SetTitle('pred. (Fall 17 MC)')			
	else:
		if phase==0:
			htruth.SetTitle('data (2016)')	
			hmethod.SetTitle('prediction')	
		if phase==1:
			htruth.SetTitle('data (2017)')	
			hmethod.SetTitle('prediction')	
			
	histoStyler(hmethod_fakecontam,kRed+1)

	
	c1 = mkcanvas('c1')
	shortname = name.replace('Control','').replace('Truth','').replace('Method','')

	varname = shortname.split('_')[-1]
	htruth.GetXaxis().SetTitle(namewizard(varname))
	hmethod.GetXaxis().SetTitle(namewizard(varname))    
	#leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)


	themax = 10000*max([hmethod.GetMaximum(),htruth.GetMaximum()])
	hmethod.GetYaxis().SetRangeUser(0.02,themax)
	hmethod.SetLineColor(kTeal-5)
	hmethod.SetFillStyle(1001)
	hmethod.SetFillColor(hmethod.GetLineColor()-1)	
	htruth.GetYaxis().SetRangeUser(0.02,themax)
	fnew.cd()
	plotname = shortname.replace('_','').replace('CaloSideband','')
	hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,htruth,[hmethod],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	pad1, pad2 = hmethodsyst[-2:]
	hratio.GetYaxis().SetRangeUser(0.0,2.125)	
	hratio.GetYaxis().SetTitle('(B/A*C)/D')
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	
	hfakeratio = hmethod_fakecontam.Clone()
	hfakeratio.Divide(hmethod)

	pad2.cd()
	leg2 = mklegend(x1=.68, y1=.85, x2=.94, y2=.965, color=kWhite)
	leg2.AddEntry(hfakeratio, 'CR fake contam.')
	leg2.Draw()	
	hfakeratio.Draw('hist same')

	pad1.cd()
	hmethod.SetTitle('')
	htruth.SetTitle('')	
	hmethod.SetLineWidth(3)
	hmethod_fakecontam.Draw('hist same')
	leg.AddEntry(hmethod_fakecontam, 'fake contrib. to pred.')
						
	c1.Update()
	fnew.cd()
	c1.Write('c_'+plotname)

	if 'BinNumber' in name:
		hmethod.Write(hmethod.GetName().replace('CaloSideband',''))
		hfake = infile.Get(name.replace('hPrompt','hFake').replace('CaloSideband',''))
		hfake = hfake.Rebin(nbins,'',newxs)
		hfake.Write()
		if 'Short' in name or 'Long' in name:
			regionkey = name.split('_')[0].replace('hPrompt','').replace('Long','').replace('Short','')
			if not regionkey in searchbinresults.keys(): searchbinresults[regionkey] = {}
			if 'Long' in name: searchbinresults[regionkey]['Long'] = [htruth.Clone(), hmethod.Clone(),hmethod_fakecontam.Clone()]
			if 'Short' in name: searchbinresults[regionkey]['Short'] = [htruth.Clone(), hmethod.Clone(),hmethod_fakecontam.Clone()]		
		
	shortname = shortname.replace('CaloSideband','')
	pdfname = 'pdfs/closure/prompt-bkg/MatchedCalo/phase'+str(phase)+'_'+shortname.replace('_','')+'.pdf'
	if mycutedatatest: pdfname = pdfname.replace('.','_cute.')
	c1.Print(pdfname)
	
	#clist.append(c1)
	c1.Delete()
	hratios.append([hratio, hmethodsyst])

for regionkey in searchbinresults:

	print 'doing regionkey', regionkey
	htruthLong, hmethodLong, hmethodLongContam = searchbinresults[regionkey]['Long']
	htruthShort, hmethodShort, hmethodShortContam = searchbinresults[regionkey]['Short']	
	htruthLong.Add(htruthShort)
	hmethodLong.Add(hmethodShort)
	hmethodLongContam.Add(hmethodShortContam)


	if datamc=='MC': 
		if phase==0:
			htruthLong.SetTitle('fake obs. (Summer 16 MC)')	
			hmethodLong.SetTitle('pred. (Summer 16 MC)')		
		if phase==1:
			htruthLong.SetTitle('fake obs. (Fall 17 MC)')
			hmethodLong.SetTitle('pred. (Fall 17 MC)')			
	else:
		if phase==0:
			htruthLong.SetTitle('data (2016)')	
			hmethodLong.SetTitle('prediction')	
		if phase==1:
			htruthLong.SetTitle('data (2017)')	
			hmethodLong.SetTitle('prediction')	
	
	hmethodLongContam.SetTitle('fake contrib. to pred.')

	themax = 10000*max([htruthLong.GetMaximum(),htruthLong.GetMaximum()])
	hmethodLong.GetYaxis().SetRangeUser(0.01,themax)
	htruthLong.GetYaxis().SetRangeUser(0.01,themax)
		
	plotname = regionkey.replace('_','').replace('CaloSideband','')
	c1 = mkcanvas('c1')
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)
	hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,htruthLong,[hmethodLong],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	pad1, pad2 = hmethodsyst[-2:]
	hratio.GetYaxis().SetRangeUser(0.0,2.4)	
	hratio.GetYaxis().SetTitle('(B/A*C)/D')
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	
	hfakeratio = hmethodLongContam.Clone()
	hfakeratio.Divide(hmethodLong)

	pad2.cd()
	hfakeratio.Draw('hist same')
	leg2 = mklegend(x1=.68, y1=.85, x2=.94, y2=.965, color=kWhite)
	leg2.AddEntry(hfakeratio, 'CR fake contam.')
	leg2.Draw()
	pad1.cd()
	hmethod.SetTitle('')
	htruth.SetTitle('')	
	hmethod.SetLineWidth(3)
	hmethodLongContam.Draw('hist same')
	leg.AddEntry(hmethod_fakecontam, 'fake contribution to pred.')
			
			

	c1.Update()
	fnew.cd()
	hmethodLong.GetYaxis().SetRangeUser(0,600)
	hmethodLong.Write('h'+plotname+'BinNumber_merged')
	c1.Write('c_'+plotname+'BinNumber_merged')
	
	pdfname = 'pdfs/closure/prompt-bkg/MatchedCalo/phase'+str(phase)+'_'+plotname+'BinNumber_merged'+'.pdf'
	if mycutedatatest: pdfname = pdfname.replace('.','_cute.')
	c1.Print(pdfname)
		
	c1.Delete()
	
	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'test c'



