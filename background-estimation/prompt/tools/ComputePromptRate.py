from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep


'''
python tools/ComputeFakeRate.py 2016 MC
python tools/ComputePromptRate.py 2016 MC

python tools/ComputeFakeRate.py Phase1 data
python tools/ComputePromptRate.py Phase1 data

python tools/ComputeFakeRate.py 2016 data
python tools/ComputePromptRate.py 2016 data

python tools/ComputeFakeRate.py 2017 data
python tools/ComputePromptRate.py 2017 data

python tools/ComputeFakeRate.py 2018 data
python tools/ComputePromptRate.py 2018 data

'''

varname_kappaBinning = 'TrkEta'
varname_kappaBinning = 'TrkPt'

try: year = sys.argv[1]
except: 
	year = '2017'
	year = '2018'
	year = '2016'
	year = 'Phase1'	
	
try: datamc = sys.argv[2]
except:  datamc = 'MC'# year = 'data'


if datamc=='data':
	lumi = 35.9 #just for labeling. this weightw as already applied #must agree with lumi in merged...py!
else:
	lumi = 137.

binning['MatchedCalo'] = [100,0,100]
binning['DtStatus'] = [6,-3,3]

redoBinning = dict(binning)

redoBinning['Met'] = [5,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['InvMass'] = [5,50,170]
redoBinning['ElPt'] = [5,0,300]
#redoBinning['TrkEta'] = [5,0,3]
redoBinning['MuPt'] = redoBinning['ElPt']
redoBinning['DeDxAverage'] = [1.999999999,2,5.0,10.0]

#redoBinning['DeDxAverage'] = [1.999999999,2,3.0,4.0,5.0,6.0,7.0]
#redoBinning['DeDxAverage'] = [1.999999999,2,4,7]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
####redoBinning['TrkPt']=[4,0,400]
redoBinning['TrkPt']=[25,0,250]
redoBinning['TrkPt']=[0,25,30,35,40,45,50,55,60,120]
#redoBinning['TrkPt']=[0,25,30,40,50,110]
redoBinning['TrkPt']=[0,25,30,40,50,75,100,150,300]
redoBinning['TrkPt']=[0,25,30,40,50,75,100,300]
redoBinning['LepMT'] = [4,0,160]
redoBinning['Ht']=[5,0,2000]
redoBinning['NJets']=[-0.00000001,0,4,10]
redoBinning['NJets']=[5,0,10]
redoBinning['MatchedCalo'] = [0,10,15,20,25,30,60]
redoBinning['BTags'] = [-0.000000000001,0,1,4]


coarserBinningPatch = {}
coarserBinningPatch['TrkPt']=[0,15,40,300]
coarseBinningPatch = {}
coarseBinningPatch['TrkPt']=[0,40,75,300]##[0,40,75,300]#give everything the shorties


#coarseBinningPatch['TrkPt'] = [0,25,30,40,50,75,100,150,200,250,300]#identical to shared_utils.py to debug short zell
#coarserBinningPatch['TrkPt'] = coarseBinningPatch['TrkPt']
makefolders = False


#rootfiles/PromptBkgTree_promptDataDrivenRun2016_mcal20to30.root

if datamc=='MC': isdata = False
else: isdata = True

calm = 15
calh = 25

calm = 17
calh = 27

calm = 20
calh = 60

#these turned into nonsense, sorry
calm = 12
calh = 80

#calm = 20
#calh = 30


if year=='2016':	
	fsource = 'test.root'
	fsource = 'output/promptDataDrivenMCSummer16.root'
	fsource = 'rootfiles/PromptBkgTree_promptDataDrivenMCSummer16_mcal'+str(calm)+'to'+str(calh)+'.root'
	if isdata: fsource = 'rootfiles/PromptBkgTree_promptDataDrivenRun2016_mcal'+str(calm)+'to'+str(calh)+'.root'

if year=='2017': 
	fsource = 'rootfiles/PromptBkgTree_promptDataDrivenMCFall17_mcal'+str(calm)+'to'+str(calh)+'.root'
	if isdata: fsource = 'rootfiles/PromptBkgTree_promptDataDrivenRun2017_mcal'+str(calm)+'to'+str(calh)+'.root'
	
if year=='2018': 
	if isdata: fsource = 'rootfiles/PromptBkgTree_promptDataDrivenRun2018_mcal'+str(calm)+'to'+str(calh)+'.root'	
	
if year=='Phase1': 
	if isdata: fsource = 'rootfiles/PromptBkgTree_promptDataDrivenPhase1_mcal'+str(calm)+'to'+str(calh)+'.root'		
	
	
	
print 'fsource', fsource
	
#hack for test:
#fsource = 'PromptBkgTree_Summer16DYJetsPrompt-processskimsTrue.root'


infile = TFile(fsource)
#infile.ls()
keys = infile.GetListOfKeys()


fout = 'usefulthings/promptrateInfo_year'+str(year)+'.root'
if isdata: fout = fout.replace('.root','_data.root')
else: fout = fout.replace('.root','_mc.root')
fnew = TFile(fout,'recreate')



hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	
	#hPromptShortSElValidZLL_MatchedCaloTruth

	if not 'SElValidZLL' in name: continue
	if 'FakeCr_' in name: continue
	if not 'Truth' in name: continue
	if not 'CaloSideband' in name: continue ##fakecr_
	if not 'hPrompt' in name: continue

	
	kinvar = name.replace('Control','').replace('Truth','').replace('Method2','')
	kinvar = kinvar[kinvar.find('_')+1:]
	
	print 'processing', name, 'got kinvar', kinvar
	
	hcontrolregion =   infile.Get(name)

		
	htarget = infile.Get(name.replace('CaloSideband_','_'))
	
	if not isdata: 
		print 'we do see MC'
		hcontrolregion.Add(infile.Get(name.replace('hPrompt','hFake')))
		htarget.Add(infile.Get(name.replace('CaloSideband_','_').replace('hPrompt','hFake')))

	#if hcontrolregion.Integral()>0: hcontrolregion.Scale(htarget.Integral()/hcontrolregion.Integral())
			
	if 'Short' in name and 'TrkPt' in name: 
		backuplist = list(redoBinning[kinvar])
		redoBinning[kinvar] = coarserBinningPatch[kinvar]
	if 'Long' in name and 'TrkPt' in name:
		backuplist = list(redoBinning[kinvar])
		redoBinning[kinvar] = coarseBinningPatch[kinvar]		
	if len(redoBinning[kinvar])!=3: 
		nbins = len(redoBinning[kinvar])-1
		newxs = array('d',redoBinning[kinvar])
	else:
		newbinning = []
		stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
		for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
		nbins = len(newbinning)-1
		newxs = array('d',newbinning)
	htarget = htarget.Rebin(nbins,'',newxs)
	hcontrolregion = hcontrolregion.Rebin(nbins,'',newxs)
	if 'Short' in name and 'TrkPt' in name: redoBinning[kinvar] = backuplist
	
	if datamc=='MC': 
		if year=='2016':
			htarget.SetTitle('')	
			hcontrolregion.SetTitle('')		
		if year=='2017':
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')	
		if year=='2018':			
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')						
	else:
		if year=='2016':
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')
		if year=='2017':
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')
		if year=='2018':			
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')
		if year=='Phase1':			
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')			

		
	if isdata: 
		if kinvar=='InvMass':
			xaxt = htarget.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: htarget.SetBinContent(ibin, 0)
		if kinvar=='LepMT':
			xaxt = htarget.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=90: htarget.SetBinContent(ibin, 0)		
	
	shortname = name.replace('Control','').replace('Truth','').replace('Method2','')

	varname = shortname.split('_')[-1]
	xax = hcontrolregion.GetXaxis()

	htarget.GetXaxis().SetTitle(namewizard(varname))
	hcontrolregion.GetXaxis().SetTitle(namewizard(varname))    
	

        	
	#leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)


	#hcontrolregion.Scale()
	themax = 10000*max([hcontrolregion.GetMaximum(),htarget.GetMaximum()])
	hcontrolregion.GetYaxis().SetRangeUser(0.02,themax)
	hcontrolregion.SetLineColor(kRed+2)
	hcontrolregion.SetFillStyle(1001)
	hcontrolregion.SetFillColor(hcontrolregion.GetLineColor()-1)	
	htarget.GetYaxis().SetRangeUser(0.02,themax)
	#hcontrolregion.SetLineColor(kGray+2)
	fnew.cd()
	plotname = shortname.replace('_','').replace('FakeCr','')
	c1 = mkcanvas('c1')


	hratio, hcontrolregionsyst = FabDraw(c1,leg,htarget,[hcontrolregion],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	hratio.GetYaxis().SetRangeUser(0,0.12)	
	hratio.GetYaxis().SetTitle('n(SR)/n(CR)')
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	pad1, pad2 = hcontrolregionsyst[-2:]
	pad2.SetGridx()
	pad2.SetGridy()	

						
	c1.Update()
	fnew.cd()
	c1.Write('c_'+plotname)

	#if 'TrkEta' in name:
	if varname_kappaBinning in name:	
		htarget.SetBinContent(-1,0)
		htarget.SetBinContent(99,0)		
		htarget.GetYaxis().SetTitle('')
		htarget.GetYaxis().SetRangeUser(0.0,2*max(htarget.GetBinContent(1),htarget.GetBinContent(3)))
		htarget.Draw('hist text')
		htarget.Write()		
		hcontrolregion.GetYaxis().SetTitle('')		
		hcontrolregion.SetBinContent(-1,0)
		hcontrolregion.SetBinContent(99,0)
		hcontrolregion.GetYaxis().SetRangeUser(0.0,2*max(hcontrolregion.GetBinContent(1),hcontrolregion.GetBinContent(3)))
		hcontrolregion.Draw('hist text')
		hcontrolregion.Write()				

	
	#c1.Print('pdfs/closure/prompt-bkg/ZShape/year'+str(year)+shortname.replace('_','')+'.png')
	
	#clist.append(c1)
	shortname = shortname.replace('FakeCr','')
	pdfname = 'pdfs/closure/fake-bkg/fakerates/year'+str(year)+'_'+shortname.replace('_','')+'.pdf'
	if isdata: pdfname = pdfname.replace('.','_data.')
	else: pdfname = pdfname.replace('.','_mc.')	
	#c1.Print(pdfname)
	c1.Delete()
	hratios.append([hratio, hcontrolregionsyst])
	#pause()

	
import os, sys
print 'just created', fnew.GetName()
fnew.Close()



if isdata:  fpromptrate = TFile('usefulthings/promptrateInfo_year'+year+'_data.root', 'update')
else:       fpromptrate = TFile('usefulthings/promptrateInfo_year'+year+'_mc.root', 'update')
    
    
print 'gonna look for', 'hPromptShortSElValidZLL_'+varname_kappaBinning+'Truth'
print 'in ', fpromptrate.GetName()

hnum = fpromptrate.Get('hPromptShortSElValidZLL_'+varname_kappaBinning+'Truth')
hden = fpromptrate.Get('hPromptShortSElValidZLLCaloSideband_'+varname_kappaBinning+'Truth')
#if not isdata:# this might be needed for the true final closure test...................#these already added above
#	hnum.Add(fpromptrate.Get('hFakeShortSElValidZLL_'+varname_kappaBinning+'Truth'))
#	hden.Add(fpromptrate.Get('hFakeShortSElValidZLLCaloSideband_'+varname_kappaBinning+'Truth'))
#	a=2
hprshort = hnum.Clone('hprshort')
hprshort.Divide(hden)
hnum = fpromptrate.Get('hPromptLongSElValidZLL_'+varname_kappaBinning+'Truth')
hden = fpromptrate.Get('hPromptLongSElValidZLLCaloSideband_'+varname_kappaBinning+'Truth')
#if not isdata:
#	hnum.Add(fpromptrate.Get('hFakeLongSElValidZLL_'+varname_kappaBinning+'Truth'))
#	hden.Add(fpromptrate.Get('hFakeLongSElValidZLLCaloSideband_'+varname_kappaBinning+'Truth'))	
#	a = 2
hprlong = hnum.Clone('hprlong')
hprlong.Divide(hden)


hprlong.GetYaxis().SetRangeUser(0,2)
hprshort.GetYaxis().SetRangeUser(0,2)
hprlong.Write()
hprshort.Write()

print 'just updated', fpromptrate.GetName()
fpromptrate.Close()

