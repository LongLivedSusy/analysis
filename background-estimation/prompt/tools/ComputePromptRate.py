from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep


'''
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

python tools/ComputeFakeRate.py Run2 data &
python tools/ComputePromptRate.py Run2 data &
python tools/ComputeMuRate.py Run2 data &

'''
#python tools/ComputePromptRate.py 2016 Signal

varname_kappaBinning = 'TrkEta'
varname_kappaBinning = 'TrkPt'

try: era = sys.argv[1]
except: 
	era = '2017'
	era = '2018'
	era = '2016'
	era = 'Phase1'	
	
try: datamc = sys.argv[2]
except:  datamc = 'MC'# era = 'data'

print 'datamc', datamc

if datamc=='data':
	lumi = 35.9 #just for labeling. this weightw as already applied #must agree with lumi in merged...py!
else:
	lumi = 137.
	
	

drawcanvs = False
c1 = mkcanvas('c1')
binning['MatchedCalo'] = [100,0,100]
binning['DtStatus'] = [6,-3,3]

redoBinning = dict(binning)

redoBinning['Met'] = [5,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['InvMass'] = [5,50,170]
redoBinning['ElPt'] = [5,0,300]
#redoBinning['TrkEta'] = [0,1.5,2.2,3.0]
redoBinning['TrkEta']=[1,0,2.0]
redoBinning['TrkEta']=[0,1.4,2.4,3.0]#tried 5 before
redoBinning['MuPt'] = redoBinning['ElPt']
redoBinning['DeDxAverage'] = [1.999999999,2,5.0,10.0]

#redoBinning['DeDxAverage'] = [1.999999999,2,3.0,4.0,5.0,6.0,7.0]
#redoBinning['DeDxAverage'] = [1.999999999,2,4,7]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
##redoBinning['TrkPt']=[0,25,30,40,50,75,100,150,300]
##redoBinning['TrkPt']=[0,25,30,40,50,75,150,300]
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
coarseBinningPatch['TrkPt']=[0,15,30,40,50,60,100,225,300]
coarseBinningPatch['TrkPt']=[0,15,30,40,60,300]
#coarseBinningPatch['TrkPt']=[0,15,30,40,70,300]
#coarseBinningPatch['TrkPt']=[0,15,20,25,30,40,50,60,70,100,225,300]
#coarseBinningPatch['TrkPt']=[0,40,70,300]
#coarseBinningPatch['TrkPt']=[0,25,40,300]##[0,40,75,300]
#coarseBinningPatch['TrkPt']=[0,14,15,300]#same as other thing



#coarserBinningPatch = redoBinning
#coarseBinningPatch = redoBinning

#coarseBinningPatch['TrkPt'] = [0,25,30,40,50,75,100,150,200,250,300]#identical to shared_utils.py to debug short zell
#coarserBinningPatch['TrkPt'] = coarseBinningPatch['TrkPt']
makefolders = False

coarseBinningPatch['TrkPt']=[1,0,300]
coarserBinningPatch['TrkPt']=[1,0,300]

#rootfiles/PromptBkgTree_promptDataDrivenRun2016_mcal20to30.root

if datamc=='MC' or datamc=='Signal': isdata = False
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
	
	
print 'fsource', fsource


#hack for test:
#fsource = 'PromptBkgTree_Summer16DYJetsPrompt-processskimsTrue.root'


infile = TFile(fsource)
#infile.ls()
keys = infile.GetListOfKeys()



fout = 'usefulthings/promptrateInfo_era'+str(era)+'.root'
if isdata: fout = fout.replace('.root','_data.root')
elif datamc=='Signal':
	print 'yessirebob'
	fout = fout.replace('.root','_Signal.root')
else: fout = fout.replace('.root','_mc.root')

print 'creating', fout
fnew = TFile(fout,'recreate')


if datamc=='Signal': region = 'Baseline'
else: region = 'SElValidZLL'

hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	
	#hPromptShort'+region+'_MatchedCaloTruth

	if not region in name: continue
	if 'FakeCr_' in name: continue
	if not 'Truth' in name: continue
	if not 'CaloSideband' in name: continue ##fakecr_
	if not 'hPrompt' in name: continue
	if 'Up' in name: continue
	
	kinvar = name.replace('Control','').replace('Truth','').replace('Method2','')
	kinvar = kinvar[kinvar.find('_')+1:]
	
	if not kinvar==varname_kappaBinning: continue
	
	hcontrolregion =   infile.Get(name).Clone()

		
	htarget = infile.Get(name.replace('CaloSideband_','_')).Clone()
	
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
		if era=='2016':
			htarget.SetTitle('')	
			hcontrolregion.SetTitle('')		
		if era=='2017':
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')	
		if era=='2018':			
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
		if era=='Phase1':			
			htarget.SetTitle('')
			hcontrolregion.SetTitle('')	
		if era=='Run2':			
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
	if drawcanvs:
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


		#c1.Print('pdfs/closure/prompt-bkg/ZShape/year'+str(era)+shortname.replace('_','')+'.png')
	
		#clist.append(c1)
		shortname = shortname.replace('FakeCr','')
		pdfname = 'pdfs/closure/fake-bkg/fakerates/year'+str(era)+'_'+shortname.replace('_','')+'.pdf'
		if isdata: pdfname = pdfname.replace('.','_data.')
		else: pdfname = pdfname.replace('.','_mc.')	
		#c1.Print(pdfname)
		c1.Delete()
		hratios.append([hratio, hcontrolregionsyst])
		#pause()


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

	

	
import os, sys
print 'just created', fnew.GetName()
fnew.Close()



if isdata:  fpromptrate = TFile('usefulthings/promptrateInfo_era'+era+'_data.root', 'update')
elif datamc=='Signal': 
	fpromptrate = TFile('usefulthings/promptrateInfo_era'+era+'_Signal.root','update')
else:       fpromptrate = TFile('usefulthings/promptrateInfo_era'+era+'_mc.root', 'update')
    
    
print 'gonna look for', 'hPromptShort'+region+'_'+varname_kappaBinning+'Truth'
print 'in ', fpromptrate.GetName()

hnum = fpromptrate.Get('hPromptShort'+region+'_'+varname_kappaBinning+'Truth').Clone()


hden = fpromptrate.Get('hPromptShort'+region+'CaloSideband_'+varname_kappaBinning+'Truth').Clone()



#if not isdata:# this might be needed for the true final closure test...................#these already added above
#	hnum.Add(fpromptrate.Get('hFakeShort'+region+'_'+varname_kappaBinning+'Truth'))
#	hden.Add(fpromptrate.Get('hFakeShort'+region+'CaloSideband_'+varname_kappaBinning+'Truth'))
#	a=2
hprshort = hnum.Clone('hprshort')
hprshort.Divide(hden)


hnum = fpromptrate.Get('hPromptLong'+region+'_'+varname_kappaBinning+'Truth').Clone()

hden = fpromptrate.Get('hPromptLong'+region+'CaloSideband_'+varname_kappaBinning+'Truth').Clone()
#if not isdata:
#	hnum.Add(fpromptrate.Get('hFakeLong'+region+'_'+varname_kappaBinning+'Truth'))
#	hden.Add(fpromptrate.Get('hFakeLong'+region+'CaloSideband_'+varname_kappaBinning+'Truth'))	
#	a = 2


hprlong = hnum.Clone('hprlong')
hprlong.Divide(hden)



hprlong.GetYaxis().SetRangeUser(0,2)
hprshort.GetYaxis().SetRangeUser(0,2)

if datamc=='Signal':
	hprlong.GetYaxis().SetRangeUser(0.001,300)
	hprshort.GetYaxis().SetRangeUser(0.001,100)
hprlong.Write()
hprshort.Write()

print 'just updated', fpromptrate.GetName()
fpromptrate.Close()


'''
#for transfer factors:
python tools/PromptBkgHistMakerFullyInformed.py --fnamekeyword /pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-847A896B-2AA6-E911-B940-0242AC1C0506_RA2AnalysisTree.root,/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-CEC26DAF-1AA6-E911-84AA-A0369FE2C19A_RA2AnalysisTree.root,/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-EEB177FF-29A6-E911-B4EC-20CF307C98DC_RA2AnalysisTree.root,/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_130000-100A3AB6-5FA5-E911-8D43-0CC47AFF2472_RA2AnalysisTree.root,/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-400D950E-14A6-E911-BC4D-C4346BB20BC0_RA2AnalysisTree.root,/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_130000-8EC7B211-FFA5-E911-9391-6CC2173C3E80_RA2AnalysisTree.root,/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_130000-3E225006-4AA5-E911-8CBB-00266CFCC490_RA2AnalysisTree.root,/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_130000-229CC212-4AA5-E911-AEB1-008CFA1982C0_RA2AnalysisTree.root,/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_130000-685851F6-E6A7-E911-9451-002590FD5838_RA2AnalysisTree.root,/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_130000-08EA6CF8-58A5-E911-835E-A0369F7FC934_RA2AnalysisTree.root --processskims True --smearvar Nom

'''

