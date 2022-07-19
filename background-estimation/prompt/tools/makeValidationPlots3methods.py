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

doPurePromptClosure = False

shutterLeps = False

grabasignal = False

tag = '2021_28_7_26Oct2021'
tag = '2021_28_7_26Oct2021b'
tag = '2021_28_7_26Oct2021c'
tag = '2021_28_7_27Oct2021'
tag = '2021_28_7_27Oct2021b'
tag = '2021_27_7_Oct2021c'
tag = '2021_31_Oct2021'
tag = '2021_31_Oct2021b'
tag = '2021_31_Oct2021c'
tag = '2021_31_Oct2021d'
tag = '2021_1_Nov2021'
tag = '2021_1_Nov2021b'
tag = '2021_1_Nov2021c'
tag = '2021_2_Nov2021'
tag = '2021_2_Nov2021b'
tag = '2021_2_Nov2021c'
tag = '2021_3_Nov2021'
tag = '2021_3_Nov2021b'
tag = '2021_3_Nov2021c'
tag = '2021_4_Nov2021'
tag = '2021_4_Nov2021b'
tag = '2021_5_Nov2021'
tag = '2021_5_Nov2021b'
tag = '2021_8_Nov2021b'
tag = '2021_8_Nov2021bad'
tag = '2021_10_Nov2021'
tag = '2021_12_Nov2021'
tag = '2021_13_Nov2021'
tag = '2021_13_Nov2021b'
tag = '2021_14_Nov2021'
tag = '2021_15_Nov2021'
tag = '2021_15_Nov2021b'
tag = '2021_15_Nov2021c'
tag = '2021_15_Nov2021e'
tag = '2021_15_Nov2021f'
tag = '2021_16_Nov2021b'
tag = '2021_16_Nov2021c'
tag = '2021_16_Nov2021d'
tag = '2021_17_Nov2021'
tag = '2021_17_Nov2021b'
tag = '2021_18_Nov2021'
tag = '2021_18_Nov2021b'
tag = '2021_19_Nov2021'
tag = '2021_19_Nov2021b'
tag = '2021_20_Nov2021'
tag = '2021_20_Nov2021b'
tag = '2021_20_Nov2022'
tag = '2021_21_Nov2021'
tag = '2021_21_Nov2021b'
tag = '2021_21_Nov2021c'
tag = '2021_21_Nov2021d'
tag = '2021_21_Nov2022'
tag = '2021_21_Nov2022b'
tag = '2021_21_Nov2022c'
tag = '2021_21_Nov23'
tag = '2021_21_Nov23b'
tag = '2021_21_Nov23c'
tag = '2021_21_Nov23d'
tag = '2021_Nov24b'
tag = '2021_Nov24c2'
tag = '2021_Nov24cNoFake'
tag = '2021_Nov24cPurePromptClose'
tag = '2021_Nov25'
tag = '2021_Nov25b'
tag = '2021_Nov256'
tag = '2021_Nov27'
tag = '2021_Nov27b'
tag = '2021_Nov27c'
tag = '2021_Nov28EtaPrompt'
tag = '2021_Nov29EtaPrPurePprompt'
tag = '2021_Nov29EtaPromptb'
tag = '2021_Nov29EtaPromptc'
tag = '2021_Nov29EtaPromptd'
tag = '2021_Nov29EtaPrompte'
tag = '2021_Nov30EtaPrompt'
tag = '2021_Nov30EtaPromptb'
tag = '2021_Dec1EtaPrompt'
tag = '2021_Dec1EtaPromptb'
tag = '2021_Dec1EtaPromptc'
tag = '2021_Dec1EtaPromptd'
tag = '2021_Dec2PtPrompt'
tag = '2021_Dec2PtPromptb'
tag = '2021_Dec2PtPromptc'
tag = '2021_Dec2PtPromptc_pdf'
tag = '2021_Dec2PtPromptcErr_pdf'
tag = '2021_Dec2PtPromptdErr_pdf'
tag = '2021_Dec2PtPrompteErr_pdf'
tag = '2021_Dec2PtPromptfErr_pdf'
tag = '2021_Dec2PtPromptgErr_pdf'
tag = '2021_Dec9PtPromptgErr_pdf'
tag = '2021_Dec10PtPrompt_pdf'
tag = '2021_Dec10PtPromptb_pdf'
tag = '2021_Dec11PtPrompt_pdf'
tag = '2021_Dec12PtPrompt_pdf'
tag = '2021_Dec16PtPrompt_v13'
tag = '2021_Dec18PtPrompt_v13Shutterleps'

tag = '2022_Feb181binUNoPuWts'
tag = '2022_Feb23UniBins'
tag = '2022_March31'
tag = '2022_March31pdfs'
tag = '2022_April7back2muons2'
tag = '2022_Apr9muon'
tag = '2022_Apr17muon'
tag = '2022_Apr17muonFine'
tag = '2022_Apr17muonCoarse'
tag = '2022_Apr19_threemethods'
tag = '2022_May26_RenewMu'
tag = '2022_May28_RenewMuHyb'

'''
rm -rf pdfs/Validation/prompt-bkg/* 
python tools/makeValidationPlots3methods.py Summer16 MC &
python tools/makeValidationPlots3methods.py Fall17 MC &
python tools/makeValidationPlots3methods.py Phase1 &
python tools/makeValidationPlots3methods.py Run2016 &



python tools/makeValidationPlots3methods.py Run2017
python tools/makeValidationPlots3methods.py Run2018

#after all this, you can do
hadd -f predictionRun2.root Valid_yearRun2016.root Valid_yearPhase1.root
cp predictionRun2.root /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v4PtDe75dx5twoNoJV/Background
'''

try: year = sys.argv[1]
except:
	year = 'Run2016'
	year = 'Run2017'
	year = 'Run2018'
	year = 'Phase1'	
	year = 'Summer16'	
	
try: datamc = sys.argv[2].lower()
except: datamc = 'data'

isdata = bool(datamc=='data')
if not isdata: doblinding = False

binning['DtStatus'] = [6,-3,3]
binning['FakeCrNr'] = [6,-3,3]

redoBinning = dict(binning)
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
redoBinning['DeDxAverage'] = [-0.000001,0,4.0,10.0]
redoBinning['ElPt'] = [30,0,300]
redoBinning['Ht']=[5,0,2000]
redoBinning['Met'] = [20,0,600]
redoBinning['HardMet'] = redoBinning['Met']
redoBinning['Mht'] = redoBinning['Met']
redoBinning['TrkEta']=[0,1.4,2.0,2.4]#tried 5 before
redoBinning['TrkEta']=binning['TrkEta']
redoBinning['BTags'] = [-0.0000000001,0,1,4]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']

makefolders = False

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

if grabasignal: 
	fsignal = TFile('/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v11/Signal/T2btLL//Stop1100_Chi1ne1000.root')

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
	
	if not ('Low' in name or 'Valid' in name or 'MhtSideband' in name or 'Baseline' in name or 'Bin23' in name): continue#): continue# 
	
	
	if not 'Truth' in name: continue
	#if 'Baseline' in name: continue
	if not 'CaloSideband' in name: continue
	if not 'hPrompt' in name: continue
	if 'FakeCr' in name: continue
	print 'still taking', name
	
	if makePredictionMode:
		if not 'BinNumber' in name: continue

	print 'name', name
	kinvar = name.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
	
	hsideband =   infile.Get(name).Clone()
	hsideband.Scale(extrascale)


	
	htruth =                  infile.Get(name.replace('CaloSideband','')).Clone()
	#htruth.Reset()##this gets rid true prompt
	if not isdata and not doPurePromptClosure: 
		htruth.Add(infile.Get(name.replace('CaloSideband','').replace('hPrompt','hFake')))
	
	htruth.Scale(extrascale)
	

	
	if isdata:
		if 'Baseline' in name:
			for ibin in range(1,htruth.GetXaxis().GetNbins()+1):
				htruth.SetBinContent(ibin, 0)
				htruth.SetBinError(ibin, 0)
	
	if doblinding and 'ZLL' in name:
		if kinvar=='InvMass':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: 
					htruth.SetBinContent(ibin, 0)
					htruth.SetBinError(ibin, 0)
	if doblinding and 'ValidMT' in name:			
		if kinvar=='LepMT':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: 
					htruth.SetBinContent(ibin, 0)
					htruth.SetBinError(ibin, 0)
			
			
	
	hpromptmethod = infile.Get(name.replace('Truth','Method2')).Clone()###then for MC complete totals:
	if not isdata and not doPurePromptClosure: 
		hpromptmethod.Add(infile.Get(name.replace('Truth','Method2').replace('hPrompt','hFake')))
	
	hpromptmethod.Scale(extrascale)
	
	'''
	if dofakesidebandsubtraction: 
		fakecontrib2sub_name = name.replace('hPrompt','hFake').replace('Truth','Method3').replace('_','FakeCr_')
		print 'fakecontrib2sub_name', fakecontrib2sub_name	
		hfakecontrib2sub = infile.Get(fakecontrib2sub_name).Clone()
		if not isdata: hfakecontrib2sub.Add(infile.Get(fakecontrib2sub_name.replace('Prompt','Fake')))
		hfakecontrib2sub.Scale(extrascale)	
		hpromptmethod.Add(hfakecontrib2sub,-1)	
		for ibin in range(1,hpromptmethod.GetXaxis().GetNbins()+1):
			if hpromptmethod.GetBinContent(ibin)<0: hpromptmethod.SetBinContent(ibin, 0) ## needs a systematic?		
	'''

	hfakemethod =                  infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_')) ###
	if not isdata: hfakemethod.Add(infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_').replace('hFake','hPrompt')))
	hfakemethod.Scale(extrascale)
	histoStyler(hfakemethod,38) ###
	hfakemethod.SetFillColor(38)
	hfakemethod.SetFillStyle(1001)
	
	hmuonmethod =                  infile.Get(name.replace('Truth','Method3').replace('CaloSideband','').replace('_','RecoMuMatched_')) ###
	if not isdata: hmuonmethod.Add(infile.Get(name.replace('Truth','Method3').replace('CaloSideband','').replace('_','RecoMuMatched_').replace('hPrompt','hFake')))
	hmuonmethod.Scale(extrascale)
	histoStyler(hmuonmethod,kViolet+1) ########
	hmuonmethod.SetFillColor(kViolet+1)
	hmuonmethod.SetFillStyle(1001)
		
		
	if 'BinNumber' in name:
	
		if shutterLeps: 
			for ibin in range(1, hpromptmethod.GetXaxis().GetNbins()+1):
				xval = int(hpromptmethod.GetXaxis().GetBinLowEdge(ibin))
				if (xval>=25 and xval<=48) or xval==50 or xval==51: 
					hpromptmethod.SetBinContent(ibin, 0)
					hpromptmethod.SetBinError(ibin, 0)					
					hfakemethod.SetBinContent(ibin, 0)
					hfakemethod.SetBinError(ibin, 0)					
					hmuonmethod.SetBinContent(ibin, 0)
					hmuonmethod.SetBinError(ibin, 0)					
					hsideband.SetBinContent(ibin, 0)
					hsideband.SetBinError(ibin, 0)					
					htruth.SetBinContent(ibin, 0)
					htruth.SetBinError(ibin, 0)																									
		hpromptmethod = merge2dtbins(hpromptmethod)
		hfakemethod = merge2dtbins(hfakemethod)
		hmuonmethod = merge2dtbins(hmuonmethod)		#######
		hsideband = merge2dtbins(hsideband)
		htruth = merge2dtbins(htruth)
		

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
	hmuonmethod = hmuonmethod.Rebin(nbins,'',newxs)####	
	
	
	for ibin in range(1,hfakemethod.GetXaxis().GetNbins()+1):
	  if (isdata or True) and (not 'BinNumber' in name):  ####systematics!
		if 'Short' in name:
			binc = hpromptmethod.GetBinContent(ibin)
			bine = hpromptmethod.GetBinError(ibin)
			#hpromptmethod.SetBinError(ibin, TMath.Sqrt(pow(binc,2)))
			#hpromptmethod.SetBinContent(ibin, 0)
			hpromptmethod.SetBinError(ibin, binc)
			#hpromptmethod.SetBinContent(ibin, 0)
			
			binc = hfakemethod.GetBinContent(ibin)
			bine = hfakemethod.GetBinError(ibin)
			hfakemethod.SetBinError(ibin, TMath.Sqrt(pow(0.3*binc,2)+pow(bine,2)))			
				
		if 'Long' in name:
			binc = hfakemethod.GetBinContent(ibin)
			bine = hfakemethod.GetBinError(ibin)
			hfakemethod.SetBinError(ibin, TMath.Sqrt(pow(0.3*binc,2)+pow(bine,2)))			
			
			binc = hpromptmethod.GetBinContent(ibin)
			bine = hpromptmethod.GetBinError(ibin)
			hpromptmethod.SetBinError(ibin, TMath.Sqrt(pow(0.2*binc,2)+pow(bine,2)))				
			
		if hfakemethod.GetBinContent(ibin)<=0: 
			hfakemethod.SetBinContent(ibin, 0)
			hfakemethod.SetBinError(ibin, 1)	
	  elif not isdata:
		
		if 'Short' in name:
			hpromptmethod.SetBinError(ibin, hpromptmethod.GetBinContent(ibin))		
			

		
	if year=='Run2016':
			htruth.SetTitle('data (2016)')
			hpromptmethod.SetTitle('showering prediction (2016)')
			hfakemethod.SetTitle('combo pred. (2016)'); hmuonmethod.SetTitle('MIP pred. (2016)')
	if year == 'Summer16':			
			htruth.SetTitle('observed (Summer16 MC)')	
			hpromptmethod.SetTitle('showering pred. (Summer16 MC)')
			hfakemethod.SetTitle('combo pred. (Summer16 MC)'); hmuonmethod.SetTitle('MIP pred. (Summer16 MC)')
			if 'Short' in name: hfakemethod.Scale(0.78)
	if year=='Run2017':
			htruth.SetTitle('data (2017)')
			hpromptmethod.SetTitle('showering prediction (2017)')
			hfakemethod.SetTitle('combo pred. (2017)');hmuonmethod.SetTitle('MIP pred. (2017)');
	if year == 'Fall17':			
			htruth.SetTitle('observed (Fall17 MC)')	
			hpromptmethod.SetTitle('showering pred. (Fall17 MC)')
			hfakemethod.SetTitle('combo pred. (Fall17 MC)');hmuonmethod.SetTitle('MIP pred. (Fall17 MC)')
			lumi = 41.8
	if year=='Run2018':
			htruth.SetTitle('data (2018)')
			hpromptmethod.SetTitle('showering prediction (2018)')
			hfakemethod.SetTitle('combo pred. (2018)');hmuonmethod.SetTitle('MIP pred. (2018)')
	if year == 'Autumn18':
			htruth.SetTitle('observed (Autumn18 MC)')	
			hpromptmethod.SetTitle('showering pred. (Autumn18 MC)')
			hfakemethod.SetTitle('combo pred. (Autumn18 MC)');hmuonmethod.SetTitle('MIP pred. (Autumn18 MC)')
	if year=='Phase1':
			htruth.SetTitle('data (Phase 1)')
			hpromptmethod.SetTitle('showering prediction (Phase 1)')
			hfakemethod.SetTitle('combo pred. (Phase 1)'); hmuonmethod.SetTitle('MIP pred. (Phase 1)')
						
			

	
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
	leg = mklegend(x1=.49, y1=.5, x2=.91, y2=.78, color=kWhite)


	themax = 150*max([hpromptmethod.GetMaximum(),htruth.GetMaximum()])

	hpromptmethod.SetLineColor(kTeal-5)
	hpromptmethod.SetFillStyle(1001)
	hpromptmethod.SetFillColor(hpromptmethod.GetLineColor()-1)	
	fnew.cd()
	plotname = shortname.replace('_','').replace('CaloSideband','')
	
	if 'BinNumber' in name:
		hpromptmethod.Write(hpromptmethod.GetName().replace('CaloSideband','').replace('Method2','Method'))
		hfakemethod.Write(hfakemethod.GetName().replace('FakeCr','').replace('Method1','Method'))
		hmuonmethod.Write(hmuonmethod.GetName()+'namesOfOthersSameQM')		
		if 'Short' in name or 'Long' in name:
			regionkey = name.split('_')[0].replace('hPrompt','').replace('Long','').replace('Short','')
			if not regionkey in searchbinresults.keys(): searchbinresults[regionkey] = {}
			if 'Long' in name: searchbinresults[regionkey]['Long'] = [htruth.Clone(), hpromptmethod.Clone(),hfakemethod.Clone(),hmuonmethod.Clone()]
			if 'Short' in name: searchbinresults[regionkey]['Short'] = [htruth.Clone(), hpromptmethod.Clone(), hfakemethod.Clone(), hmuonmethod.Clone()]
			
	if doPurePromptClosure: bkgs = [hpromptmethod]
	else: bkgs = [hfakemethod, hpromptmethod]
	if not 'Short' in name: bkgs.append(hmuonmethod)
	hratio, hpromptmethodsyst = FabDrawSystyRatio(c1,leg,htruth,bkgs,datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	
			
	pad1, pad2 = hpromptmethodsyst[-2:]
	hratio.GetYaxis().SetRangeUser(0.0,2.125)	
	hratio.GetYaxis().SetTitle('data/pred.')
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	
	pad1.cd()
	if grabasignal and ('Baseline' in name or 'ValidZLL' in name or 'MhtSideband' in name) and not ('HighMT' in name ) and not ('LepPt' in name): 
		#fsignal.ls()
		sname = name.replace('CaloSideband','').replace('_','SystNom_').replace('Prompt','')
		print 'looking for signal name', sname
		hsignal = fsignal.Get(sname)
		hsignal = hsignal.Rebin(nbins,'',newxs)
		histoStyler(hsignal, kRed)
		hsignal.Draw('hist same')
		leg.AddEntry(hsignal, 'T2bt g1100, chi1000)')
	fnew.cd()			

	pad2.cd()
	leg2 = mklegend(x1=.68, y1=.85, x2=.94, y2=.965, color=kWhite)
	leg2.Draw()	

	pad1.cd()
	htruth.GetYaxis().SetRangeUser(0.09,themax)
	hfakemethod.GetYaxis().SetRangeUser(0.01,themax)
	hpromptmethod.GetYaxis().SetRangeUser(0.09,themax)
	hmuonmethod.GetYaxis().SetRangeUser(0.09,themax)		
	hpromptmethod.SetTitle('')
	htruth.SetTitle(''); hmuonmethod.SetTitle('')
	hpromptmethod.SetLineWidth(3)


	#p1 = c1.FindObject('pad1')
	#p2 = c1.FindObject('pad2')	
	#for p in p1.GetListOfPrimitives():
	#	print p.GetName()
		
	#pave = p1.FindObject('TPave')
	#pave.Delete()
	#c1.Update()

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
	htruthLong, hpromptmethodLong, hfakemethodLong, hmuonmethodLong = searchbinresults[regionkey]['Long']
	htruthShort, hpromptmethodShort, hfakemethodShort, hmuonmethodShort = searchbinresults[regionkey]['Short']	
	htruthLong.Add(htruthShort)
	
	for ibin in range(1, htruthLong.GetXaxis().GetNbins()+1):
		if htruthLong.GetBinContent(ibin)==0:
			htruthLong.SetBinError(ibin, 1)
				
	hpromptmethodLong.Add(hpromptmethodShort)
	hfakemethodLong.Add(hfakemethodShort)	
	#hmuonmethodLong.Add(hmuonmethodShort)		
	
	'''
	if year=='Run2016':
			htruthLong.SetTitle('data (2016)')
			hpromptmethodLong.SetTitle('prompt prediction (2016)')
			hfakemethodLong.SetTitle('fake prediction (2016)')			
	if year == 'Summer16':
			htruthLong.SetTitle('observed (Summer16 MC)')	
			hpromptmethodLong.SetTitle('prompt pred. (Summer16 MC)')
			hfakemethodLong.SetTitle('fake pred. (Summer16 MC)')				
	if year=='Run2017':
			htruthLong.SetTitle('data (2017)')
			hpromptmethodLong.SetTitle('prompt prediction (2017)')
			hfakemethodLong.SetTitle('fake prediction (2017)')	
	if year == 'Fall17':
			htruthLong.SetTitle('observed (Fall17 MC)')	
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
	'''	

	themax = 500*max([htruthLong.GetMaximum(),hpromptmethodLong.GetMaximum()])
		
	fnew.cd()
	hpromptmethodLong.Write(hpromptmethodLong.GetName().replace('CaloSideband','MASTER'))
	hfakemethodLong.Write(hfakemethodLong.GetName().replace('FakeCr','MASTER'))	
	hmuonmethodLong.Write(hmuonmethodLong.GetName().replace('RecoMuMatched','MASTER'))		

	plotname = regionkey.replace('_','').replace('CaloSideband','')
	c1 = mkcanvas('c1')
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)
	hrattot = htruthLong.Clone()
	hdenom = hpromptmethodLong.Clone()
	hdenom.Add(hfakemethodLong)
	hrattot.Add(hdenom, -1)
	hratio, hpromptmethodsyst = FabDrawSystyRatio(c1,leg,htruthLong,[hmuonmethodLong, hpromptmethodLong,hfakemethodLong],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
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
	hpromptmethodLong.GetYaxis().SetRangeUser(0.01,themax)
	hfakemethodLong.GetYaxis().SetRangeUser(0.01,themax)	
	hmuonmethodLong.GetYaxis().SetRangeUser(0.01,themax)		
	htruthLong.GetYaxis().SetRangeUser(0.01,themax)	
	hpromptmethod.SetTitle('')
	htruth.SetTitle('')	
	hpromptmethod.SetLineWidth(3)
			
			
	c1.Update()
	
	c1.Write('c_'+plotname+'BinNumber_merged')
	

	hres = TH1F('resid_'+plotname+'BinNumber_merged','resid_'+plotname+'BinNumber_merged',32,-4,4)
	hres.GetYaxis().SetTitle('number of signal regions')
	hres.GetXaxis().SetTitle('pull')
	for ibin in range(1,hrattot.GetXaxis().GetNbins()+1):
		print ibin, 'doing residuals', hrattot.GetBinContent(ibin)
		if hrattot.GetBinError(ibin)>0:
			hres.Fill(hrattot.GetBinContent(ibin)/hrattot.GetBinError(ibin))
				
	
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
	

	gStyle.SetOptFit(1111)	
	gStyle.SetOptStat(0)
	c2 = mkcanvas('c2')
	hres.Draw('hist e')
	hres.Fit('gaus')
	thegaus = hres.GetListOfFunctions()[0]
	thegaus.SetLineColor(kBlue+1)
	thegaus.Draw('same')
	c2.Update()

	c2.Print(pdfname.replace('.png','Pull.png'))
	if makepdfs: c2.Print(pdfname.replace('.png','Pull.pdf'))	
	c2.Delete()
		
	c1.Delete()
	
	
import os, sys
whippyname = 'htmlwhippy'+year+'.sh'
os.system('echo echo hello > '+whippyname)
pipe = '>'
print 'reached the end of things'
for directory_ in directories:
	os.system('echo python tools/whiphtml.py \\"pdfs/Validation/prompt-bkg/'+year+'/'+directory_+'/*.png\\" '+pipe+' '+whippyname)
	pipe = '>>'
os.system('bash '+whippyname)
thename = fnew.GetName()
print 'just created', os.getcwd()+'/'+thename
fnew.Close()
print 'now do'
copycommand = 'cp -r pdfs/Validation/prompt-bkg/'+year+' /afs/desy.de/user/b/beinsam/www/DisappearingTracks/Validation/'+tag+'_'+year
print copycommand
os.system(copycommand)
copycode = 'cp tools/PromptBkgHistMakerMuCr.py /afs/desy.de/user/b/beinsam/www/DisappearingTracks/Validation/'+tag+'_'+year
print copycode
os.system(copycode)

if True: 
	print 'you might want to hadd these end products together', thename
	print 'a la'
	print 'hadd -f predictionRun2.root Valid_yearRun2016.root Valid_yearPhase1.root'
	print 'cp predictionRun2.root /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v13/Background'
	

