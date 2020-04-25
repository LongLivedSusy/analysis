from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep


datamc = 'data'

if datamc=='data':
	lumi = 35.9 #just for labeling. this weightw as already applied #must agree with lumi in merged...py!
else:
	lumi = 137.

binning['MatchedCalo'] = [100,0,100]
binning['DtStatus'] = [6,-3,3]

redoBinning = binning

redoBinning['Met'] = [5,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['InvMass'] = [5,50,170]
redoBinning['ElPt'] = [5,0,300]
redoBinning['TrkEta'] = [5,0,3]
redoBinning['MuPt'] = redoBinning['ElPt']
redoBinning['DeDxAverage'] = [1.999999999,2,4,7]

redoBinning['DeDxAverage'] = [1.999999999,2,3.0,4.0,5.0,6.0,7.0]
#redoBinning['DeDxAverage'] = [1.999999999,2,4,7]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
redoBinning['TrkPt']=[4,0,400]
redoBinning['LepMT'] = [4,0,160]
redoBinning['Ht']=[4,0,1200]
redoBinning['NJets']=[-0.00000001,0,4,10]
redoBinning['NJets']=[5,0,10]
redoBinning['MatchedCalo'] = [0,10,15,20,25,30,60]
redoBinning['BTags'] = [-0.000000000001,0,1,4]


makefolders = False

year = '2016'
year = '2017'
year = '2018'

if datamc=='MC': mycutedatatest = False
else: mycutedatatest = True

zoneOfDedx = {}
zonebinning = binning['DeDxZones']
for izone in range(len(zonebinning)-1):
	dedx_zone = str(zonebinning[izone]).replace('.','p')+'to'+str(zonebinning[izone+1]).replace('.','p')
	zoneOfDedx[izone] = dedx_zone
	
print 'zonebinning', zonebinning
normzone = zoneOfDedx[0]

if year=='2016':	
	fCentralMC = 'test.root'
	fCentralMC = 'output/promptDataDrivenMCSummer16.root'
	fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenMCSummer16_mcal15to20.root'
	if mycutedatatest: fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenRun2016_mcal15to20.root'

if year=='2017': 
	fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenMCFall17_mcal15to20.root'
	if mycutedatatest: fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenRun2017_mcal15to20.root'
	
if year=='2018': 
	if mycutedatatest: fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenRun2018_mcal15to20.root'	
	

print 'going to use', fCentralMC
infile = TFile(fCentralMC)
infile.ls()
keys = infile.GetListOfKeys()


fout = 'closureFakeTest_year'+str(year)+'.root'
if mycutedatatest: fout = fout.replace('.root','_cute.root')
fnew = TFile(fout,'recreate')



hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	

	
	if not 'Method' in name: continue
	#if not 'Baseline' in name: continue
	if not 'FakeCr_' in name: continue
	if not 'hFake' in name: continue
	

	
	kinvar = name.replace('Control','').replace('Truth','').replace('Method','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
	
	hmethod =   infile.Get(name)
	if not mycutedatatest: hmethod.Add(infile.Get(name.replace('hFake','hPrompt')))
	
	if not mycutedatatest: 
		hmethod_promptcontam = infile.Get(name.replace('hFake','hPrompt'))
		htruth_promptcontam = infile.Get(name.replace('FakeCr_','_').replace('Method','Truth').replace('hFake','hPrompt'))
		histoStyler(hmethod_promptcontam, kTeal-5)
		hmethod_promptcontam.SetFillStyle(0)
	
	htruth = infile.Get(name.replace('FakeCr_','_').replace('Method','Truth'))
	

	#if hmethod.Integral()>0: hmethod.Scale(htruth.Integral()/hmethod.Integral())
			
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
	if not mycutedatatest:
		hmethod_promptcontam = hmethod_promptcontam.Rebin(nbins,'',newxs)
		htruth_promptcontam = htruth_promptcontam.Rebin(nbins,'',newxs)		
		
	if datamc=='MC': 
		if year=='2016':
			htruth.SetTitle('fake obs. (Summer 16 MC)')	
			hmethod.SetTitle('pred. (Summer 16 MC)')		
		if year=='2017':
			htruth.SetTitle('fake obs. (Fall 17 MC)')
			hmethod.SetTitle('pred. (Fall 17 MC)')	
		if year=='2018':			
			htruth.SetTitle('fake obs. (Fall 18 MC)')
			hmethod.SetTitle('pred. (Fall 18 MC)')						
	else:
		if year=='2016':
			htruth.SetTitle('data (2016)')	
			hmethod.SetTitle('prediction')	
		if year=='2017':
			htruth.SetTitle('data (2017)')	
			hmethod.SetTitle('prediction')
		if year=='2018':			
			htruth.SetTitle('data (2018)')	
			hmethod.SetTitle('prediction')					

		
	if mycutedatatest: 
		if kinvar=='InvMass':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: htruth.SetBinContent(ibin, 0)
		if kinvar=='LepMT':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=90: htruth.SetBinContent(ibin, 0)		
	
	shortname = name.replace('Control','').replace('Truth','').replace('Method','')

	varname = shortname.split('_')[-1]
	xax = hmethod.GetXaxis()

	htruth.GetXaxis().SetTitle(namewizard(varname))
	hmethod.GetXaxis().SetTitle(namewizard(varname))    
	

        	
	#leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)


	#hMethod.Scale()
	themax = 10000*max([hmethod.GetMaximum(),htruth.GetMaximum()])
	hmethod.GetYaxis().SetRangeUser(0.01,themax)
	hmethod.SetLineColor(kRed+2)
	hmethod.SetFillStyle(1001)
	hmethod.SetFillColor(hmethod.GetLineColor()-1)	
	htruth.GetYaxis().SetRangeUser(0.01,themax)
	#hmethod.SetLineColor(kGray+2)
	fnew.cd()
	plotname = shortname.replace('_','').replace('FakeCr','')
	c1 = mkcanvas('c1')


	hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,htruth,[hmethod],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	hratio.GetYaxis().SetRangeUser(0.0,2.6)	
	hratio.GetYaxis().SetTitle('(B/A*C)/D')
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	pad1, pad2 = hmethodsyst[-2:]
	

	
	pad1.cd()
	if not mycutedatatest:  hmethod_promptcontam.Draw('hist same')
	hmethod.SetTitle('')
	htruth.SetTitle('')	
	
	hmethod.SetLineWidth(3)
	
	
	pad2.cd()
	leg2 = mklegend(x1=.65, y1=.85, x2=.91, y2=.965, color=kWhite)
	
	if not mycutedatatest: 
		leg.AddEntry(hmethod_promptcontam, 'prompt contrib. to pred.')
		hpromptratio = hmethod_promptcontam.Clone()
		hpromptratio.Divide(hmethod)		
		leg2.AddEntry(hpromptratio, 'CR prompt contam.')
		hpromptratio.Draw('hist same')
	leg2.Draw()	
						
	c1.Update()
	fnew.cd()
	c1.Write('c_'+plotname)

	if 'BinNumber' in name:
		hmethod.Write(hmethod.GetName().replace('FakeCr_','_'))
		hfake = infile.Get(name.replace('hPrompt','hFake').replace('FakeCr_','_'))
		hfake = hfake.Rebin(nbins,'',newxs)
		hfake.Write()
	if 'Ht' in name:
		htruth.Write()
		hfakecrtruth = infile.Get(name.replace('Method', 'Truth'))
		hfakecrtruth = hfakecrtruth.Rebin(nbins,'',newxs)
		hfakecrtruth.Write()
		if not mycutedatatest:
			hmethod_promptcontam.Write()
			print 'writing', htruth_promptcontam.GetName()
			htruth_promptcontam.Write()
			hpromptcrtruth = infile.Get(name.replace('Method', 'Truth').replace('hFake','hPrompt'))
			hpromptcrtruth = hpromptcrtruth.Rebin(nbins,'',newxs)
			hpromptcrtruth.Write()			
		
	
	#c1.Print('pdfs/closure/prompt-bkg/ZShape/year'+str(year)+shortname.replace('_','')+'.png')
	
	#clist.append(c1)
	shortname = shortname.replace('FakeCr','')
	pdfname = 'pdfs/closure/fake-bkg/FrVsHt/year'+str(year)+'_'+shortname.replace('_','')+'.pdf'
	if mycutedatatest: pdfname = pdfname.replace('.','_cute.')
	c1.Print(pdfname)
	c1.Delete()
	hratios.append([hratio, hmethodsyst])
	#pause()

	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'test c'



