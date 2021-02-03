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

python tools/ComputeFakeRate.py 2016 data
python tools/ComputePromptRate.py 2016 data

python tools/ComputeFakeRate.py 2017 data
python tools/ComputePromptRate.py 2017 data

python tools/ComputeFakeRate.py 2018 data
python tools/ComputePromptRate.py 2018 data

python tools/ComputeFakeRate.py Phase1 data
python tools/ComputePromptRate.py Phase1 data

'''

varname_thetaBinning = 'Ht'
varname_thetaBinning = 'TrkEta'

try: year = sys.argv[1]
except: 
	year = '2017'
	year = '2016'
	year = '2018'
	year = 'Phase1'
try: datamc = sys.argv[2]
except:  datamc = 'MC'# year = 'data'

isdata = bool(datamc=='data')

if isdata: lumi = 35.9 #just for labeling. this weightw as already applied #must agree with lumi in merged...py!
else: lumi = 137.

binning['MatchedCalo'] = [100,0,100]
binning['DtStatus'] = [6,-3,3]

redoBinning = binning

redoBinning['Met'] = [5,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['InvMass'] = [5,50,170]
redoBinning['ElPt'] = [5,0,300]
#redoBinning['TrkEta'] = [5,0,3]
redoBinning['TrkEta']=[9,0,3]#tried 5 before
redoBinning['TrkEta']=[10,0,3]#tried 5 before
redoBinning['TrkEta']=[0,1.9,2.2,3.0]#tried 5 before
redoBinning['MuPt'] = redoBinning['ElPt']
redoBinning['DeDxAverage'] = [1.999999999,2,5.0,10.0]

#redoBinning['DeDxAverage'] = [1.999999999,2,3.0,4.0,5.0,6.0,7.0]
#redoBinning['DeDxAverage'] = [1.999999999,2,4,7]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
#redoBinning['TrkPt']=[0,25,30,40,50,300]
redoBinning['TrkPt']=[0,15,30,40,300]
redoBinning['LepMT'] = [4,0,160]
redoBinning['Ht']=[5,0,2000]
redoBinning['NJets']=[-0.00000001,0,4,10]
redoBinning['NJets']=[5,0,10]
redoBinning['MatchedCalo'] = [0,10,15,20,25,30,60]
redoBinning['BTags'] = [-0.000000000001,0,1,4]

calm = 15
calh = 25

#calm = 20
#calh = 30

calm = 17
calh = 27

calm = 20
calh = 60

calm = 12
calh = 80

makefolders = False



if year=='2016':	
	fCentralMC = 'test.root'
	fCentralMC = 'output/promptDataDrivenMCSummer16.root'
	fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenMCSummer16_mcal'+str(calm)+'to'+str(calh)+'.root'
	if isdata: fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenRun2016_mcal'+str(calm)+'to'+str(calh)+'.root'

if year=='2017': 
	fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenMCFall17_mcal15to20.root'
	if isdata: fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenRun2017_mcal'+str(calm)+'to'+str(calh)+'.root'
	
if year=='2018': 
	if isdata: fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenRun2018_mcal'+str(calm)+'to'+str(calh)+'.root'	
	
if year=='Phase1': 
	if isdata: fCentralMC = 'rootfiles/PromptBkgTree_promptDataDrivenPhase1_mcal'+str(calm)+'to'+str(calh)+'.root'	
	

print 'going to use', fCentralMC
infile = TFile(fCentralMC)
#infile.ls()
keys = infile.GetListOfKeys()


fout = 'usefulthings/fakerateInfo_year'+str(year)+'.root'
if isdata: fout = fout.replace('.root','_data.root')
else: fout = fout.replace('.root','_mc.root')
fnew = TFile(fout,'recreate')



hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	

	if not 'MhtSideband' in name: continue
	if 'CaloSideband' in name: continue
	if not 'Truth' in name: continue
	#if not 'Baseline' in name: continue
	if not 'FakeCr_' in name: continue
	if not 'hFake' in name: continue
	

	
	kinvar = name.replace('Control','').replace('Truth','').replace('Method1','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
	
	hcontrolregion =   infile.Get(name)

	
	if not isdata: 
		hcontrolregion_promptcontam = infile.Get(name.replace('hFake','hPrompt'))
		htarget_promptcontam = infile.Get(name.replace('FakeCr_','_').replace('hFake','hPrompt'))
		histoStyler(hcontrolregion_promptcontam, kTeal-5)
		hcontrolregion_promptcontam.SetFillStyle(0)
	
	htarget = infile.Get(name.replace('FakeCr_','_').replace('Method1','Truth'))
	
	if not isdata: 
		hcontrolregion.Add(infile.Get(name.replace('hFake','hPrompt')))
		htarget.Add(infile.Get(name.replace('FakeCr_','_').replace('Method1','Truth').replace('hFake','hPrompt')))

	#if hcontrolregion.Integral()>0: hcontrolregion.Scale(htarget.Integral()/hcontrolregion.Integral())
			
	if len(redoBinning[kinvar])!=3: 
		nbins = len(redoBinning[kinvar])-1
		newxs = array('d',redoBinning[kinvar])
		print 'newbinss', redoBinning[kinvar]
	else:
		newbinning = []
		print kinvar, name
		stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
		for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
		nbins = len(newbinning)-1
		newxs = array('d',newbinning)
		print 'newbins', newbinning
	htarget = htarget.Rebin(nbins,'',newxs)
	hcontrolregion = hcontrolregion.Rebin(nbins,'',newxs)
	if not isdata:
		hcontrolregion_promptcontam = hcontrolregion_promptcontam.Rebin(nbins,'',newxs)
		htarget_promptcontam = htarget_promptcontam.Rebin(nbins,'',newxs)		
							
	if isdata:
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
			
		
	if isdata: 
		if kinvar=='InvMass':
			xaxt = htarget.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: htarget.SetBinContent(ibin, 0)
		if kinvar=='LepMT':
			xaxt = htarget.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=90: htarget.SetBinContent(ibin, 0)		
	
	shortname = name.replace('Control','').replace('Truth','').replace('Method1','')

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

	
	pad1.cd()
	if not isdata:  hcontrolregion_promptcontam.Draw('hist same')
	hcontrolregion.SetTitle('')
	htarget.SetTitle('')	
	
	hcontrolregion.SetLineWidth(3)
	
	
	pad2.cd()
	leg2 = mklegend(x1=.65, y1=.85, x2=.91, y2=.965, color=kWhite)
	
	if not isdata: 
		leg.AddEntry(hcontrolregion_promptcontam, 'prompt contrib. to pred.')
		hpromptratio = hcontrolregion_promptcontam.Clone()
		hpromptratio.Divide(hcontrolregion)		
		leg2.AddEntry(hpromptratio, 'CR prompt contam.')
		hpromptratio.Draw('hist same')
	leg2.Draw()	
						
	c1.Update()
	fnew.cd()
	c1.Write('c_'+plotname)

	if 'BinNumber' in name:
		hcontrolregion.Write(hcontrolregion.GetName().replace('FakeCr_','_'))
		hfake = infile.Get(name.replace('hPrompt','hFake').replace('FakeCr_','_'))
		hfake = hfake.Rebin(nbins,'',newxs)
		hfake.Write()
	if varname_thetaBinning in name:
		cnew = mkcanvas('cnew')	
		#cnew.SetLogy()
		htarget.SetBinContent(-1,0)
		htarget.SetBinContent(99,0)		
		htarget.GetYaxis().SetTitle('low-MHT nL=0; numerator events')
		htarget.GetYaxis().SetRangeUser(0.0,2*max(htarget.GetBinContent(1),htarget.GetBinContent(3)))
		htarget.Draw('hist text')
		cnew.Update()
		htarget.Write()		
		cnew.Print('pdfs/closure/fake-bkg/fakerates/year'+str(year)+'_'+shortname.replace('_','')+'_numerator.pdf')
		hcontrolregion.GetYaxis().SetTitle('low-MHT nL=0; denominator events')		
		hcontrolregion.SetBinContent(-1,0)
		hcontrolregion.SetBinContent(99,0)
		hcontrolregion.GetYaxis().SetRangeUser(0.0,2*max(hcontrolregion.GetBinContent(1),hcontrolregion.GetBinContent(3)))
		hcontrolregion.Draw('hist text')
		cnew.Update()
		hcontrolregion.Write()				
		cnew.Print('pdfs/closure/fake-bkg/fakerates/year'+str(year)+'_'+shortname.replace('_','')+'_denominator.pdf')		
		hratio.GetYaxis().SetRangeUser(0,1.2*hratio.GetMaximum())
		hratio.GetXaxis().SetLabelSize(0.05)
		hratio.GetYaxis().SetLabelSize(0.05)		
		hratio.GetYaxis().SetTitle('FR')
		hratio.Draw('hist text')
		cnew.Print('pdfs/closure/fake-bkg/fakerates/year'+str(year)+'_'+shortname.replace('_','')+'_fr.pdf')
	
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

	
	
	
print 'just created', fnew.GetName()
fnew.Close()

#now get the fake rate and stuff
if isdata:  ffakerate = TFile('usefulthings/fakerateInfo_year'+year+'_data.root', 'update')
else: ffakerate = TFile('usefulthings/fakerateInfo_year'+year+'_mc.root', 'update')
	
hnum = ffakerate.Get('hFakeShortHadMhtSideband_'+varname_thetaBinning+'Truth')
hden = ffakerate.Get('hFakeShortHadMhtSidebandFakeCr_'+varname_thetaBinning+'Truth')
hfrshort = hnum.Clone('hfrshort')
hfrshort.Divide(hden)
hnum = ffakerate.Get('hFakeLongHadMhtSideband_'+varname_thetaBinning+'Truth')
hden = ffakerate.Get('hFakeLongHadMhtSidebandFakeCr_'+varname_thetaBinning+'Truth')
hfrlong = hnum.Clone('hfrlong')
hfrlong.Divide(hden)

hfrlong.GetYaxis().SetRangeUser(0,2)
hfrshort.GetYaxis().SetRangeUser(0,2)
hfrlong.Write()
hfrshort.Write()

print 'just updated', ffakerate.GetName()
ffakerate.Close()
	
	
	
	
	
	
	




