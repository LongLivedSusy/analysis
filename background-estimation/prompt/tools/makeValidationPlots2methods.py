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
#lumi = 137.

makepdfs = True
datamc = 'data'# should pretty much always be this way
doblinding = True
dofakesidebandsubtraction = False

makePredictionMode = False
extrascale = 1.0
#extrascale = 137./35.9


tag = 'MaxAwesTrkEnPt30'
tag = '2ndTestPt10Short'
tag = 'ShortPt10NoDPhi'
tag = 'StraightenedOut'
tag = 'ViktorsLong'
tag = 'ClassicReversion'
tag = 'TryAgainJ2MakeSure'
tag = 'ClassicBut20'
tag = 'BabyStepAcrsTheRoom'
tag = 'SplitLSLowMvaMp5'
tag = 'ViktorAtLast'
tag = 'ViktorTighterPh0L'
tag = 'VikTighterPh0LBmp6'
tag = 'VikTighterPh0LBmp5'
tag = 'VikTighterEdP5FxSb'
tag = 'KlassikP5FxSb'
tag = 'KlassikKlassic'
tag = 'FirstWithCharged'
tag = 'TryPiOver2'
tag = 'TightViktorPiO2'
tag = 'TightViktorEdep18'
tag = 'AataViktorEdep20'
tag = 'LooserBdtViktorEdep20'
tag = 'ReLsrBdtViktorEdep20'
tag = 'SmFxLsrBdtVikEdep20'
tag = 'BkToDp23LBdtVEdep20'
tag = 'BasicFixDp23LBVdep20'
tag = 'ViktagDp23LBVdep12'
tag = 'ViktagDp23LBVdep10'
tag = 'VtgDp23MBVdep15Sbt'
tag = 'Exo'
tag = 'LoosePlus10ECal15'
tag = 'Lp10Lmp1ECal15'
tag = 'Lpp1Lmp1ECal15P'
tag = 'BdtNoEdepECal15'
tag = '1BdtNoEdep4pECal15'
tag = '1BdtNoed4prECal15Pt'
tag = '1BdtNoed4prEc15PtLfb'
tag = '1BdtNoedEc15Pt40'
tag = '1BdtNoedE15Pt40Loose'
tag = '1BNoedPt40LsnLsr'
tag = 'Intuitive1Dedx5Pt40'
tag = 'Intuitive1Dedx5Pt75'
tag = 'BackHomeDedx4Pt30'
tag = 'BHoDx4p5Pt100TFkDphi'
tag = 'Dx4p5Pt100TFkDphiPrEta'
tag = 'Dx45Pt100DphiPrEtaJV'
tag = 'Dx45Pt100DphiPrEtaMoPt'
tag = 'Dx45Pt100MoPtNrmBNpu'
tag = 'Dx45Pt100MoPtNrmBNumsk'
tag = 'Dx45Pt75MoPtNrmBNumsk'
tag = 'Dx45Pt75MoPtNrmBEta2p2'
tag = 'Dx45Pt30MoPtNrmBEta2p2'
tag = 'Dx45Pt30MoPtJVEta2p2'
tag = 'Dx45Pt30MoPtJVEta2p2Mu'
tag = 'Dx45Pt30JVEta2p2Mu2'
tag = 'Dx45Pt30JVEt2p2Mu2WdMv'
tag = 'Dx45Pt30JVEt2p2MuFlgen'
tag = 'Dx45Pt30JVEt2p2ExclMu'
tag = 'Dx45Pt30MoPtJVEta2p1'
tag = 'Dx45Pt40MoPtJVEta2p1'
tag = 'Dx4Pt40MoPtJVEt2p1Nopi'
tag = 'Dx4Pt40MoPtJVEt2p1Pi'
tag = 'Dx4Pt40MoPtJVEt2p1Gfx'
tag = 'Dx4Pt40MoPtJV2p1Nopimu'
tag = 'Dx4Pt40Et2p1onlFJV10p6'
tag = 'Dx4Pt40Et2p1onlFJV15p6'
tag = 'Dx4Pt40Et2p1JV10p6'
tag = 'Dx4Pt40Et2p1JV10p6NoTrw'
tag = 'Dx4Pt40Et2p1JVFkVsEt'
tag = 'Dx4Pt40Et2p1JVFkVfewEt'
tag = 'Dx4Pt40Et2p4JVFkVfewEt'
tag = 'Dx4Pt40Et2p2JVFkVfewEt'
tag = 'Dx4Pt40Et2p2JVPrVfewPt'
tag = 'Dx4Pt40Et2p2JVDdxMin'
tag = 'Dx4Pt40Et22JVDxmnNuMsk'
tag = 'Dx4Pt40Et22JVCoarsrFR'
tag = 'Dx4Pt40Et22JVMindphib'
tag = 'Dx4Pt40Et22JVMindphij'
tag = 'Dx4Pt40Et22NoJV'
tag = 'Dx4Pt40Et22NoJVTtnShrt'
tag = 'Dx4Pt40Et22JVdnTtnShrt'
tag = 'Dx4Pt40Et22JVdnTtShrt'
tag = 'Dx4Pt40Et22JVdnTtShPdf'
tag = 'Dx4Pt40Et22JVdnTShPdf'
tag = 'Dx4Pt40Et22Jan2021b'
tag = 'Dx4Pt40Jan2021geq1b'
tag = 'Dx4Pt40J21geq1bLsrEdp'
tag = 'Dx4Pt40J21LsrEdpJndPt'
tag = 'J21LsrEdpJndPtLsrb4Mc'
tag = 'J21LsrEdpLsrbd4mcNow'
tag = 'J21LsrEdpLsrb4mcFkhlf'
tag = 'J21LsrEdpLsrb4mcFkonly'
tag = 'J21LsrEdpLsrb4mcFkonly'
tag = 'J21LsrEdpLssrb4mcFknly'
tag = 'J21LsrEdpLssrb4mc'
tag = 'J21LsrEdpLssrb4mcFo2'
tag = 'J21LsrEdpLssrb4mcBk2b'
tag = 'Dx4Pt40Et22LsrEdpJndPt'
tag = 'Dx4Pt40Et22LsrEdpMrPtaf'
tag = 'Dx4Pt40Et22LsrEdMrMcwts'
tag = 'Dx4Pt40Et22Calm40MrMcwts'
tag = 'Dx4Pt40Et22Calm40MrMcnow'
tag = 'Dx4Pt40Et22ed40Two2bins'
tag = 'Dx4Pt40Et22ed40TwobinMnb'
tag = 'Dx4Pt40Et22ed40Two2Nof2'
tag = 'Dx4Pt40Et22ed40Two2sampt'
tag = 'Dx4Et22ed40Two2actsampt'
tag = 'Dx4Et22ed40Two3Hemv'
tag = 'Dx4Et22ed40Two3HvIronout'
tag = 'Dx4Et22ed40Two3HvIronagn'
tag = 'Dx4Et22ed40Two3HvIron3'
tag = 'Dx4Et22ed40Two3HvPinPt'
tag = 'Dx4Et22ed40Two3Hv2bin'
tag = 'Dx4Et22Two3Hv2bin2'
tag = 'Dx4Et22Two3Hv2bin2chns'
tag = 'Dx4Et22Two3Hv2bin2numsk'



'''
rm -rf pdfs/Validation/prompt-bkg/*
python tools/makeValidationPlots2methods.py Summer16 MC
python tools/makeValidationPlots2methods.py Run2016
python tools/makeValidationPlots2methods.py Phase1


python tools/makeValidationPlots2methods.py 2017
python tools/makeValidationPlots2methods.py 2018

#after all this, you can do
hadd -f predictionRun2.root Valid_yearRun2016.root Valid_yearPhase1.root
cp predictionRun2.root /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v4PtDe75dx5twoNoJV/Background
'''

try: year = sys.argv[1]
except:
	year = 'Run2016'
	year = 'Run2017'
	year = 'Run2018'
	year = 'RunPhase1'	
	year = 'Summer16'	
	
try: datamc = sys.argv[2].lower()
except: datamc = 'data'

isdata = bool(datamc=='data')
if not isdata: doblinding = False


#binning['MatchedCalo'] = [120,0,60]
binning['DtStatus'] = [6,-3,3]
binning['FakeCrNr'] = [6,-3,3]

redoBinning = binning
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
redoBinning['DeDxAverage'] = [1.999999999,2,3.0,4.0,5.0,6.0,7.0]
redoBinning['DeDxAverage'] = [1.999999999,2,4.0,10.0]
#redoBinning['InvMass'] = [15,50,170]
##redoBinning['InvMass'] = [50,0,200]
#redoBinning['InvMass'] = [24,60,180]
redoBinning['ElPt'] = [30,0,300]
redoBinning['Ht']=[5,0,2000]
redoBinning['Met'] = [20,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['TrkEta']=[30,0,3]
redoBinning['NJets'] = [6,1,7]
redoBinning['NJets'] = [0.999999,1,4,7]
redoBinning['BTags'] = [-0.0000000001,0,1,4]
#redoBinning['MatchedCalo'] = [0,10,13,23,40]
#redoBinning['InvMass'] = [25,0,200]#same as analysis

makefolders = False


calm = 20
calh = 25

calm = 10
calh = 15

calm = 17
calh = 27

calm = 20
calh = 60

calm = 20
calh = 80

call = 12
calm = 12
calh = 80

#calm = 20
#calh = 30


if year=='Run2017': lumi = 41.8
if year=='Run2018': lumi = 55.0
if year=='Phase1': lumi = 41.8+55.0

mainfilename = 'rootfiles/PromptBkgTree_promptDataDriven'+year+'_mcal'+str(calm)+'to'+str(calh)+'.root'
if datamc=='mc': mainfilename = mainfilename.replace('DataDriven','DataDrivenMC')

print 'opening', mainfilename
infile = TFile(mainfilename)
infile.ls()
keys = infile.GetListOfKeys()

hShapeShort = infile.Get('hPromptShortSElValidZLL_MatchedCaloTruth').Clone('hShapeShort')##
shax = hShapeShort.GetXaxis()
binm = shax.FindBin(calm)
binh = shax.FindBin(calh)


fout = 'Valid_year'+str(year)+'.root'
fnew = TFile(fout,'recreate')


searchbinresults = {}
hratios = []
clist = []
directories = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	
	if 'hFake' in name: continue
	
	if not ('Valid' in name or 'MhtSideband' in name or 'Baseline' in name): continue#): continue# 
	
	
	if not 'Truth' in name: continue
	#if 'Baseline' in name: continue
	if not 'CaloSideband' in name: continue
	if not 'hPrompt' in name: continue
	if 'FakeCr' in name: continue
	
	if makePredictionMode:
		if not 'BinNumber' in name: continue

	print 'name', name
	kinvar = name.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
	
	hsideband =   infile.Get(name).Clone()
	hsideband.Scale(extrascale)
	
	htruth =                  infile.Get(name.replace('CaloSideband','')).Clone()
	if not isdata: htruth.Add(infile.Get(name.replace('CaloSideband','').replace('hPrompt','hFake')))
	
	htruth.Scale(extrascale)
	
	if isdata:
		if 'Baseline' in name:
			for ibin in range(1,htruth.GetXaxis().GetNbins()+1):
				htruth.SetBinContent(ibin, 0)
	
	if doblinding and 'ZLL' in name:
		if kinvar=='InvMass':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: htruth.SetBinContent(ibin, 0)
	if doblinding and 'ValidMT' in name:			
		if kinvar=='LepMT':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=105: htruth.SetBinContent(ibin, 0)	
			
			
	
	hpromptmethod = infile.Get(name.replace('Truth','Method2')).Clone()###then for MC complete totals:
	if not isdata: hpromptmethod.Add(infile.Get(name.replace('Truth','Method2').replace('hPrompt','hFake')))
	
	hpromptmethod.Scale(extrascale)
	if dofakesidebandsubtraction: 
		fakecontrib2sub_name = name.replace('hPrompt','hFake').replace('Truth','Method3').replace('_','FakeCr_')
		print 'fakecontrib2sub_name', fakecontrib2sub_name	
		hfakecontrib2sub = infile.Get(fakecontrib2sub_name).Clone()
		if not isdata: hfakecontrib2sub.Add(infile.Get(fakecontrib2sub_name.replace('Prompt','Fake')))
		hfakecontrib2sub.Scale(extrascale)	
		hpromptmethod.Add(hfakecontrib2sub,-1)	
		for ibin in range(1,hpromptmethod.GetXaxis().GetNbins()+1):
			if hpromptmethod.GetBinContent(ibin)<0: hpromptmethod.SetBinContent(ibin, 0) ## needs a systematic?		
	

	hfakemethod =                  infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_')) ###
	if not isdata: hfakemethod.Add(infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_').replace('hFake','hPrompt')))
	hfakemethod.Scale(extrascale)
	histoStyler(hfakemethod,38) ###
	hfakemethod.SetFillColor(38)
	hfakemethod.SetFillStyle(1001)
		
	if 'BinNumber' in name and False:
		hpromptmethod = merge2dtbins(hpromptmethod)
		hfakemethod = merge2dtbins(hfakemethod)
		hsideband = merge2dtbins(hsideband)
		htruth = merge2dtbins(htruth)
		

	if 'MatchedCalo' in name and False:
		dintHigh, dintLow = Double(), Double()
		integ_high = hpromptmethod.IntegralAndError(binm,binh-1,dintHigh)
		hspecialAux = TH1F('hspecialMethod','hspecialMethod',1,0,1)
		hspecialAux.SetBinContent(1,integ_high)
		hspecialAux.SetBinError(1,dintHigh)		

		

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
	hpromptmethod = hpromptmethod.Rebin(nbins,'',newxs)
	
	hfakemethod = hfakemethod.Rebin(nbins,'',newxs)####
	
	for ibin in range(1,hfakemethod.GetXaxis().GetNbins()+1):
	  if isdata:
		if 'Short' in name:
			binc = hpromptmethod.GetBinContent(ibin)
			bine = hpromptmethod.GetBinError(ibin)
			hpromptmethod.SetBinError(ibin, TMath.Sqrt(pow(binc,2)))
			
			binc = hfakemethod.GetBinContent(ibin)
			bine = hfakemethod.GetBinError(ibin)
			hfakemethod.SetBinError(ibin, TMath.Sqrt(pow(0.3*binc,2)+pow(bine,2)))
				
		if 'Long' in name:
			binc = hfakemethod.GetBinContent(ibin)
			bine = hfakemethod.GetBinError(ibin)
			hfakemethod.SetBinError(ibin, TMath.Sqrt(pow(0.5*binc,2)+pow(bine,2)))			
			
			binc = hpromptmethod.GetBinContent(ibin)
			bine = hpromptmethod.GetBinError(ibin)
			hpromptmethod.SetBinError(ibin, TMath.Sqrt(pow(0.2*binc,2)+pow(bine,2)))				
			
		if hfakemethod.GetBinContent(ibin)<=0: 
			hfakemethod.SetBinContent(ibin, 0)
			hfakemethod.SetBinError(ibin, 1)			
				
			

		
	if year=='Run2016':
			htruth.SetTitle('data (2016)')
			hpromptmethod.SetTitle('prompt prediction (2016)')
			hfakemethod.SetTitle('fake pred. (2016)')
	if year == 'Summer16':			
			htruth.SetTitle('obs. (Summer16 MC)')	
			hpromptmethod.SetTitle('prompt pred. (Summer16 MC)')
			hfakemethod.SetTitle('prompt pred. (Summer16 MC)')			
	if year=='Run2017':
			htruth.SetTitle('data (2017)')
			hpromptmethod.SetTitle('prompt prediction (2017)')
			hfakemethod.SetTitle('fake pred. (2017)')	
	if year == 'Fall17':			
			htruth.SetTitle('obs. (Fall17 MC)')	
			hpromptmethod.SetTitle('prompt pred. (Fall17 MC)')
			hfakemethod.SetTitle('prompt pred. (Fall17 MC)')			
	if year=='Run2018':
			htruth.SetTitle('data (2018)')
			hpromptmethod.SetTitle('prompt prediction (2018)')
			hfakemethod.SetTitle('fake pred. (2018)')	
	if year == 'Autumn18':
			htruth.SetTitle('obs. (Autumn18 MC)')	
			hpromptmethod.SetTitle('prompt pred. (Autumn18 MC)')
			hfakemethod.SetTitle('prompt pred. (Autumn18 MC)')			
	if year=='Phase1':
			htruth.SetTitle('data (Phase 1)')
			hpromptmethod.SetTitle('prompt prediction (Phase 1)')
			hfakemethod.SetTitle('fake pred. (Phase 1)')			
						
			

	
	c1 = mkcanvas('c1')
	shortname = name.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
	directory = shortname.split('_')[0].replace('hPrompt','').replace('CaloSideband','')
	if not directory in directories:
		directories.append(directory)
		if not os.path.exists('pdfs/Validation/prompt-bkg/'+year+'/'+directory):
			os.system('mkdir -p pdfs/Validation/prompt-bkg/'+year+'/'+directory)	

	varname = shortname.split('_')[-1]
	htruth.GetXaxis().SetTitle(namewizard(varname))
	hpromptmethod.GetXaxis().SetTitle(namewizard(varname))    
	#leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)


	themax = 150*max([hpromptmethod.GetMaximum(),htruth.GetMaximum()])

	hpromptmethod.SetLineColor(kTeal-5)
	hpromptmethod.SetFillStyle(1001)
	hpromptmethod.SetFillColor(hpromptmethod.GetLineColor()-1)	
	fnew.cd()
	plotname = shortname.replace('_','').replace('CaloSideband','')
	
	if 'BinNumber' in name:
		hpromptmethod.Write(hpromptmethod.GetName().replace('CaloSideband','').replace('Method2','Method'))
		hfakemethod.Write(hfakemethod.GetName().replace('FakeCr','').replace('Method1','Method'))
		if 'Short' in name or 'Long' in name:
			regionkey = name.split('_')[0].replace('hPrompt','').replace('Long','').replace('Short','')
			if not regionkey in searchbinresults.keys(): searchbinresults[regionkey] = {}
			if 'Long' in name: searchbinresults[regionkey]['Long'] = [htruth.Clone(), hpromptmethod.Clone(),hfakemethod.Clone()]
			if 'Short' in name: searchbinresults[regionkey]['Short'] = [htruth.Clone(), hpromptmethod.Clone(), hfakemethod.Clone()]
				
	hratio, hpromptmethodsyst = FabDrawSystyRatio(c1,leg,htruth,[hfakemethod,hpromptmethod],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	pad1, pad2 = hpromptmethodsyst[-2:]
	hratio.GetYaxis().SetRangeUser(0.0,2.125)	
	hratio.GetYaxis().SetTitle('data/pred.')
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	

	pad2.cd()
	leg2 = mklegend(x1=.68, y1=.85, x2=.94, y2=.965, color=kWhite)
	leg2.Draw()	

	pad1.cd()
	htruth.GetYaxis().SetRangeUser(0.09,themax)
	hfakemethod.GetYaxis().SetRangeUser(0.01,themax)
	hpromptmethod.GetYaxis().SetRangeUser(0.09,themax)		
	hpromptmethod.SetTitle('')
	htruth.SetTitle('')	
	hpromptmethod.SetLineWidth(3)
						
	c1.Update()
	fnew.cd()
	c1.Write('c_'+plotname)

		
	shortname = shortname.replace('CaloSideband','')
	pdfname = 'pdfs/Validation/prompt-bkg/'+year+'/'+directory+'/'+shortname.replace('_','')+'.png'
	c1.Print(pdfname)
	if makepdfs: c1.Print(pdfname.replace('.png','.pdf'))
	
	#clist.append(c1)
	c1.Delete()
	hratios.append([hratio, hpromptmethodsyst])


print 'searchbinresults', searchbinresults.keys()
for regionkey in searchbinresults:
	
	print 'doing regionkey', regionkey
	htruthLong, hpromptmethodLong, hfakemethodLong = searchbinresults[regionkey]['Long']
	htruthShort, hpromptmethodShort, hfakemethodShort = searchbinresults[regionkey]['Short']	
	htruthLong.Add(htruthShort)
	hpromptmethodLong.Add(hpromptmethodShort)
	hfakemethodLong.Add(hfakemethodShort)	
	
	
	if year=='Run2016':
			htruthLong.SetTitle('data (2016)')
			hpromptmethodLong.SetTitle('prompt prediction (2016)')
			hfakemethodLong.SetTitle('fake prediction (2016)')			
	if year == 'Summer16':
			htruthLong.SetTitle('obs. (Summer16 MC)')	
			hpromptmethodLong.SetTitle('prompt pred. (Summer16 MC)')
			hfakemethodLong.SetTitle('fake pred. (Summer16 MC)')				
	if year=='Run2017':
			htruthLong.SetTitle('data (2017)')
			hpromptmethodLong.SetTitle('prompt prediction (2017)')
			hfakemethodLong.SetTitle('fake prediction (2017)')	
	if year == 'Fall17':
			htruthLong.SetTitle('obs. (Fall17 MC)')	
			hpromptmethodLong.SetTitle('prompt pred. (Fall17 MC)')
			hfakemethodLong.SetTitle('fake pred. (Fall17 MC)')	
	if year=='Run2018':
			htruthLong.SetTitle('data (2018)')
			hpromptmethodLong.SetTitle('prompt prediction (2018)')
			hfakemethodLong.SetTitle('fake prediction (2018)')
	if year=='Phase1':
			htruthLong.SetTitle('data (Phase 1)')
			hpromptmethodLong.SetTitle('prompt prediction (Phase 1)')
			hfakemethodLong.SetTitle('fake prediction (Phase 1)')
			

	themax = 100*max([htruthLong.GetMaximum(),hpromptmethodLong.GetMaximum()])
	hpromptmethodLong.GetYaxis().SetRangeUser(0.01,themax)
	htruthLong.GetYaxis().SetRangeUser(0.01,themax)
		
		
	hpromptmethodLong.Write(hpromptmethodLong.GetName().replace('CaloSideband','MASTER'))
	hfakemethodLong.Write(hfakemethodLong.GetName().replace('FakeCr','MASTER'))	

	plotname = regionkey.replace('_','').replace('CaloSideband','')
	c1 = mkcanvas('c1')
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)
	hratio, hpromptmethodsyst = FabDraw(c1,leg,htruthLong,[hpromptmethodLong,hfakemethodLong],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	pad1, pad2 = hpromptmethodsyst[-2:]
	hratio.GetYaxis().SetRangeUser(0.0,3.4)	
	hratio.GetYaxis().SetTitle('(B/A*C)/D')
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	
	pad2.cd()
	leg2 = mklegend(x1=.68, y1=.85, x2=.94, y2=.965, color=kWhite)

	leg2.Draw()
	pad1.cd()
	hpromptmethod.SetTitle('')
	htruth.SetTitle('')	
	hpromptmethod.SetLineWidth(3)
	histoStyler(hsideband, kViolet)
	hsideband.Draw('same hist')		
			

	c1.Update()
	fnew.cd()
	c1.Write('c_'+plotname+'BinNumber_merged')
	directory_ = 'SearchBins'
	if not directory_ in directories:
		directories.append(directory_)
	if not os.path.exists('pdfs/Validation/prompt-bkg/'+str(year)+'/'+directory_):
		os.system('mkdir pdfs/Validation/prompt-bkg/'+str(year)+'/'+directory_)
		
	shortname = regionkey.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
	shortname = shortname.replace('CaloSideband','')
	pdfname = 'pdfs/Validation/prompt-bkg/'+str(year)+'/'+directory_+'/'+str(year)+'_'+shortname.replace('_','')+'.png'
	c1.Print(pdfname)	
	if makepdfs: c1.Print(pdfname.replace('.png','.pdf'))
		
	c1.Delete()
	
	
import os, sys
os.system('echo echo hello > htmlwhippy.sh')
pipe = '>'
print 'reached the end of things'
for directory_ in directories:
	os.system('echo python tools/whiphtml.py \\"pdfs/Validation/prompt-bkg/'+year+'/'+directory_+'/*.png\\" '+pipe+' htmlwhippy.sh')
	pipe = '>>'
os.system('bash htmlwhippy.sh')
thename = fnew.GetName()
print 'just created', os.getcwd()+'/'+thename
fnew.Close()
print 'now do'
copycommand = 'cp -r pdfs/Validation/prompt-bkg/'+year+' /afs/desy.de/user/b/beinsam/www/DisappearingTracks/Validation/'+tag+'_'+year
print copycommand
os.system(copycommand)


if makePredictionMode: 
	print 'you might want to hadd these end products together', thename
	print 'a la'
	print 'hadd -f predictionRun2.root Valid_year2016.root Valid_yearPhase1.root'

