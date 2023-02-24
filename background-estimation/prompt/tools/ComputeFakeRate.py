from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep


'''
python tools/ComputeFakeRate.py Run2 data &
python tools/ComputePromptRate.py Run2 data 
python tools/ComputeMuRate.py Run2 data 

python tools/ComputeFakeRate.py 2016 MC &
python tools/ComputePromptRate.py 2016 MC &
python tools/ComputeMuRate.py 2016 MC &

python tools/ComputeFakeRate.py 2017 MC &
python tools/ComputePromptRate.py 2017 MC &
python tools/ComputeMuRate.py 2017 MC &

python tools/ComputeFakeRate.py Phase1 data &
python tools/ComputePromptRate.py Phase1 data &
python tools/ComputeMuRate.py Phase1 data &

python tools/ComputeFakeRate.py 2016 data &
python tools/ComputePromptRate.py 2016 data &
python tools/ComputeMuRate.py 2016 data &


python tools/ComputeFakeRate.py 2017 data &
python tools/ComputePromptRate.py 2017 data &
python tools/ComputeMuRate.py 2017 data &

python tools/ComputeFakeRate.py 2018 data &
python tools/ComputePromptRate.py 2018 data &
python tools/ComputeMuRate.py 2018 data &



'''

#python tools/ComputeFakeRate.py 2016 Signal
varname_thetaBinning = 'Ht'
varname_thetaBinning = 'TrkEta'
varname_thetaBinning = 'TrkPt'
varname_thetaBinning = 'Ht'
varname_thetaBinning = 'TrkEta'

try: era = sys.argv[1]
except: 
	era = '2017'
	era = '2016'
	era = '2018'
	era = 'Phase1'
try: datamc = sys.argv[2]
except:  datamc = 'MC'# era = 'data'

if datamc=='MC' or datamc=='Signal': isdata = False
else: isdata=True

if isdata: lumi = 35.9 #just for labeling. this weightw as already applied #must agree with lumi in merged...py!
else: lumi = 137.

binning['MatchedCalo'] = [100,0,100]
binning['DtStatus'] = [6,-3,3]

redoBinning = dict(binning)

redoBinning['Met'] = [5,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['InvMass'] = [5,50,170]
redoBinning['ElPt'] = [5,0,300]
#redoBinning['TrkEta'] = [5,0,3]
redoBinning['TrkEta']=[9,0,3]#tried 5 before
redoBinning['TrkEta']=[10,0,3]#tried 5 before
redoBinning['TrkEta']=[0,1.6,2.4,3.0]#tried 5 before
redoBinning['TrkEta']=[0,1.4,2.4,3.0]#official one! 
#redoBinning['TrkEta']=[0,1.0,2.4,3.0]#tried 5 before
#redoBinning['TrkEta']=binning['TrkEta']



##redoBinning['TrkEta']=[1,0,3]#tried 5 before
redoBinning['MuPt'] = redoBinning['ElPt']
redoBinning['DeDxAverage'] = [1.999999999,2,5.0,10.0]

#redoBinning['DeDxAverage'] = [1.999999999,2,3.0,4.0,5.0,6.0,7.0]
#redoBinning['DeDxAverage'] = [1.999999999,2,4,7]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
#redoBinning['TrkPt']=[0,25,30,40,50,300]
#redoBinning['TrkPt']=[0,15,30,40,300]
redoBinning['LepMT'] = [4,0,160]
redoBinning['Ht']=[5,0,2000]
redoBinning['NJets']=[-0.00000001,0,4,10]
redoBinning['NJets']=[5,0,10]
redoBinning['MatchedCalo'] = [0,10,15,20,25,30,60]
redoBinning['BTags'] = [-0.000000000001,0,1,4]


coarserBinningPatch = {}
coarserBinningPatch['TrkPt']=[0,14,15,300]
coarserBinningPatch['TrkPt']=[0,14,15,300]
coarseBinningPatch = {}
#coarseBinningPatch['TrkPt']=[0,15,30,40,50,60,100,225,300]
coarseBinningPatch['TrkPt']=[0,40,70,300]
coarseBinningPatch['TrkPt']=[0,5,40,300]

#redoBinning['TrkEta'] = binning['TrkEta']
redoBinning['TrkEta']=[0,1.4,2.4,2.7,3.0]#tried 5 before
redoBinning['TrkEta']=[0,2.4,3.0,4.0]#trying new one for Harrison
#redoBinning['TrkEta'] = binning['TrkEta']
coarseBinningPatch['TrkPt'] = [0,15,20,25,30,40,60,70,100,225,300]
coarserBinningPatch['TrkPt'] = binning['TrkPt']

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



if era=='2016':	
	fsource = 'test.root'
	fsource = 'output/promptDataDrivenMCSummer16.root'
	fsource = 'rootfiles/PromptBkgTree_promptDataDrivenMCSummer16_mcal'+str(calm)+'to'+str(calh)+'.root'
	if isdata: fsource = 'rootfiles/PromptBkgTree_promptDataDrivenRun2016_mcal'+str(calm)+'to'+str(calh)+'.root'
	if datamc=='Signal': fsource = 'PromptBkgHist_RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-847A896B-2AA6-E911-B940-0242AC1C0506_-processskimsTrue-smearvarNom.root'
if era=='2017': 
	fsource = 'rootfiles/PromptBkgTree_promptDataDrivenMCFall17_mcal'+str(calm)+'to'+str(calh)+'.root'
	if isdata: fsource = 'rootfiles/PromptBkgTree_promptDataDrivenRun2017_mcal'+str(calm)+'to'+str(calh)+'.root'
	
if era=='2018': 
	if isdata: fsource = 'rootfiles/PromptBkgTree_promptDataDrivenRun2018_mcal'+str(calm)+'to'+str(calh)+'.root'	
	
if era=='Phase1': 
	if isdata: fsource = 'rootfiles/PromptBkgTree_promptDataDrivenPhase1_mcal'+str(calm)+'to'+str(calh)+'.root'	
	
if era=='Run2': 
	if isdata: fsource = 'rootfiles/PromptBkgTree_promptDataDrivenRun2_mcal'+str(calm)+'to'+str(calh)+'.root'		
	

print 'going to use', fsource
infile = TFile(fsource)
infile.ls()
keys = infile.GetListOfKeys()


fout = 'usefulthings/fakerateInfo_era'+str(era)+'.root'
if isdata: fout = fout.replace('.root','_data.root')
elif datamc=='Signal': fout = fout.replace('.root','_Signal.root')
else: fout = fout.replace('.root','_mc.root')
fnew = TFile(fout,'recreate')

if datamc=='Signal': region = 'Baseline'
else: region = 'HadMhtSideband'

hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	
	if 'Up' in name: continue
	if not region in name: continue
	if 'CaloSideband' in name: continue
	if not 'Truth' in name: continue
	#if not 'Baseline' in name: continue
	if not 'FakeCr_' in name: continue
	if not 'hFake' in name: continue
	

	
	kinvar = name.replace('Control','').replace('Truth','').replace('Method1','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
	if not kinvar==varname_thetaBinning: continue
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
	if 'TrkPt' in varname_thetaBinning:
		if 'Short' in name and 'TrkPt' in name: 
			backuplist = list(redoBinning[kinvar])
			redoBinning[kinvar] = coarserBinningPatch[kinvar]
		if 'Long' in name and 'TrkPt' in name:
			backuplist = list(redoBinning[kinvar])
			redoBinning[kinvar] = coarseBinningPatch[kinvar]
			
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
	if 'Short' in name and 'TrkPt' in name: redoBinning[kinvar] = backuplist	
	if not isdata:
		hcontrolregion_promptcontam = hcontrolregion_promptcontam.Rebin(nbins,'',newxs)
		htarget_promptcontam = htarget_promptcontam.Rebin(nbins,'',newxs)		
							
	if isdata:
		if era=='2016':
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')
		if era=='2017':
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')
		if era=='2018':			
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')
		if era=='Phase1':			
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')			
	else:
		if era=='2016':
			htarget.SetTitle('')	
			hcontrolregion.SetTitle('')		
		if era=='2017':
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')	
		if era=='2018':			
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
		cnew.Print('pdfs/closure/fake-bkg/fakerates/year'+str(era)+'_'+shortname.replace('_','')+'_numerator.pdf')
		hcontrolregion.GetYaxis().SetTitle('low-MHT nL=0; denominator events')		
		hcontrolregion.SetBinContent(-1,0)
		hcontrolregion.SetBinContent(99,0)
		hcontrolregion.GetYaxis().SetRangeUser(0.0,2*max(hcontrolregion.GetBinContent(1),hcontrolregion.GetBinContent(3)))
		hcontrolregion.Draw('hist text')
		cnew.Update()
		hcontrolregion.Write()				
		cnew.Print('pdfs/closure/fake-bkg/fakerates/year'+str(era)+'_'+shortname.replace('_','')+'_denominator.pdf')		
		hratio.GetYaxis().SetRangeUser(0,1.2*hratio.GetMaximum())
		hratio.GetXaxis().SetLabelSize(0.05)
		hratio.GetYaxis().SetLabelSize(0.05)		
		hratio.GetYaxis().SetTitle('FR')
		hratio.Draw('hist text')
		cnew.Print('pdfs/closure/fake-bkg/fakerates/year'+str(era)+'_'+shortname.replace('_','')+'_fr.pdf')
	
	#c1.Print('pdfs/closure/prompt-bkg/ZShape/year'+str(era)+shortname.replace('_','')+'.png')
	
	#clist.append(c1)
	shortname = shortname.replace('FakeCr','')
	pdfname = 'pdfs/closure/fake-bkg/fakerates/year'+str(era)+'_'+shortname.replace('_','')+'.pdf'
	if isdata: pdfname = pdfname.replace('.','_data.')
	else: pdfname = pdfname.replace('.','_mc.')	
	#c1.Print(pdfname)
	c1.Delete()

	
	
	
print 'just created', fnew.GetName()
#fnew.ls()
fnew.Close()

#now get the fake rate and stuff
if isdata:  ffakerate = TFile('usefulthings/fakerateInfo_era'+era+'_data.root', 'update')
elif datamc=='Signal': 
	ffakerate = TFile('usefulthings/fakerateInfo_era'+era+'_Signal.root','update')
else: ffakerate = TFile('usefulthings/fakerateInfo_era'+era+'_mc.root', 'update')
	
print 'giving', 'hFakeShort'+region+'_'+varname_thetaBinning+'Truth', 'a slug'
hnum = ffakerate.Get('hFakeShort'+region+'_'+varname_thetaBinning+'Truth')
hden = ffakerate.Get('hFakeShort'+region+'FakeCr_'+varname_thetaBinning+'Truth')

hfrshort = hnum.Clone('hfrshort')
hfrshort.Divide(hden)
hnum = ffakerate.Get('hFakeLong'+region+'_'+varname_thetaBinning+'Truth')
hden = ffakerate.Get('hFakeLong'+region+'FakeCr_'+varname_thetaBinning+'Truth')
hfrlong = hnum.Clone('hfrlong')
hfrlong.Divide(hden)

hfrlong.GetYaxis().SetRangeUser(0,2)
hfrshort.GetYaxis().SetRangeUser(0,2)

if datamc=='Signal':
	hfrlong.GetYaxis().SetRangeUser(0.001,100)
	hfrshort.GetYaxis().SetRangeUser(0.001,300)
	
hfrlong.Write()
hfrshort.Write()

print 'just updated', ffakerate.GetName()
ffakerate.Close()
	
	
	
	
	
	
	




