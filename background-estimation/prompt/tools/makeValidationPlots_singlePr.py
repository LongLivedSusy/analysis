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



datamc = 'data'# should pretty much always be this way
doblinding = True
dofakesidebandsubtraction = True

'''
python tools/makeValidationPlots.py 2016 && python tools/makeValidationPlots.py 2017 && python tools/makeValidationPlots.py 2018  
'''

try: year = sys.argv[1]
except:
	year = '2016'
	year = '2017'
	year = '2018'


binning['MatchedCalo'] = [120,0,60]
binning['DtStatus'] = [6,-3,3]
binning['FakeCrNr'] = [6,-3,3]

redoBinning = binning
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
redoBinning['LepMT'] = [8,0,160]
redoBinning['DeDxAverage'] = [1.999999999,2,3.0,4.0,5.0,6.0,7.0]
#redoBinning['InvMass'] = [15,50,170]
redoBinning['InvMass'] = [15,50,170]
redoBinning['ElPt'] = [30,0,300]
redoBinning['Ht']=[5,0,2000]
redoBinning['Met'] = [20,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['TrkPt']=[5,0,150]
redoBinning['TrkEta'] = [5,0,3]
redoBinning['MatchedCalo'] = [0,10,13,23,40]
redoBinning['InvMass'] = [25,0,200]#same as analysis
'''
redoBinning['Met'] = [20,0,600]
redoBinning['Mht'] = redoBinning['Met']


redoBinning['TrkEta'] = [5,0,3]
redoBinning['MuPt'] = redoBinning['ElPt']
redoBinning['DeDxAverage'] = [1.999999,2,4,7]

redoBinning['TrkPt']=[5,0,200]
redoBinning['Ht']=[10,0,1000]
redoBinning['MatchedCalo'] = [0,10,12,15,17,20,25,30,60]
'''
makefolders = False


calm = 20
calh = 25

calm = 10
calh = 15

calm = 15
calh = 20

calm = 13
calh = 23

calm = 13
calh = 27

calm = 13
calh = 35


if year=='2017': lumi = 41.8
if year=='2018': lumi = 55.0

if year=='2016': mainfilename = 'rootfiles/PromptBkgTree_promptDataDrivenRun2016_mcal'+str(calm)+'to'+str(calh)+'.root'
if year=='2017': mainfilename = 'rootfiles/PromptBkgTree_promptDataDrivenRun2017_mcal'+str(calm)+'to'+str(calh)+'.root'
if year=='2018': mainfilename = 'rootfiles/PromptBkgTree_promptDataDrivenRun2018_mcal'+str(calm)+'to'+str(calh)+'.root'

infile = TFile(mainfilename)
infile.ls()
keys = infile.GetListOfKeys()

hShapeShort = infile.Get('hPromptShortSElValidationZLL_MatchedCaloTruth').Clone('hShapeShort')##

hShapeLong = infile.Get('hPromptLongSElValidationZLL_MatchedCaloTruth').Clone('hShapeLong')##

shax = hShapeShort.GetXaxis()


binm = shax.FindBin(calm)
binh = shax.FindBin(calh)

low_over_high_short = hShapeShort.Integral(shax.FindBin(0),shax.FindBin(10)-1)/hShapeShort.Integral(binm,binh-1)
low_over_high_long = hShapeLong.Integral(shax.FindBin(0),shax.FindBin(10)-1)/hShapeLong.Integral(binm,binh-1)

fout = 'validation_year'+str(year)+'.root'
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

	
	htruth = infile.Get(name.replace('CaloSideband','')).Clone()

	if doblinding and 'ZLL' in name:
		if kinvar=='InvMass':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: htruth.SetBinContent(ibin, 0)
	if doblinding and 'ValidationMT' in name:			
		if kinvar=='LepMT':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=90: htruth.SetBinContent(ibin, 0)	
			
			
	
	hSidebandFakePrediction = infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method').replace('_','FakeCr_')).Clone()
	if dofakesidebandsubtraction: 
		print 'gonna subtract this thing', name.replace('hPrompt','hFake').replace('Truth','Method').replace('_','FakeCr_')
		hsideband.Add(hSidebandFakePrediction,-1)
		for ibin in range(1,hsideband.GetXaxis().GetNbins()+1):
			if hsideband.GetBinContent(ibin)<0: hsideband.SetBinContent(ibin, 0) ## needs a systematic?
	
				
	hmethod = hsideband.Clone(hsideband.GetName().replace('Truth','PrMethod'))

	

	hfakemethod = infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method').replace('CaloSideband','').replace('_','FakeCr_')) ###
	#histoStyler(hfakemethod,kRed) ###
		
	if 'BinNumber' in name:
		hmethod = merge2dtbins(hmethod)
		hfakemethod = merge2dtbins(hfakemethod)
		hsideband = merge2dtbins(hsideband)
		htruth = merge2dtbins(htruth)
		

	if 'MatchedCalo' in name:
		dintHigh, dintLow = Double(), Double()
		integ_high = hmethod.IntegralAndError(binm,binh-1,dintHigh)
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
	hmethod = hmethod.Rebin(nbins,'',newxs)
	
	hfakemethod = hfakemethod.Rebin(nbins,'',newxs)####
				
			
			
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
				
	else:
		hmethod.Scale(low_over_high)
		
	if year=='2016':
		if datamc=='MC': 
			htruth.SetTitle('obs. (Summer16 MC)')	
			hmethod.SetTitle('prompt pred. (Summer16 MC)')
			hfakemethod.SetTitle('prompt pred. (Summer16 MC)')
		else:
			htruth.SetTitle('data (2016)')
			hmethod.SetTitle('prompt prediction (2016)')
			hfakemethod.SetTitle('fake pred. (2016)')
	if year=='2017':
		if datamc=='MC': 
			htruth.SetTitle('obs. (Fall17 MC)')	
			hmethod.SetTitle('prompt pred. (Fall17 MC)')
			hfakemethod.SetTitle('prompt pred. (Fall17 MC)')
		else:
			htruth.SetTitle('data (2017)')
			hmethod.SetTitle('prompt prediction (2017)')
			hfakemethod.SetTitle('fake pred. (2017)')	
	if year=='2018':
		if datamc=='MC': 
			htruth.SetTitle('obs. (Autumn18 MC)')	
			hmethod.SetTitle('prompt pred. (Autumn18 MC)')
			hfakemethod.SetTitle('prompt pred. (Autumn18 MC)')
		else:
			htruth.SetTitle('data (2018)')
			hmethod.SetTitle('prompt prediction (2018)')
			hfakemethod.SetTitle('fake pred. (2018)')						
			

	
	c1 = mkcanvas('c1')
	shortname = name.replace('Control','').replace('Truth','').replace('Method','')

	varname = shortname.split('_')[-1]
	htruth.GetXaxis().SetTitle(namewizard(varname))
	hmethod.GetXaxis().SetTitle(namewizard(varname))    
	#leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)


	themax = 150*max([hmethod.GetMaximum(),htruth.GetMaximum()])

	hmethod.SetLineColor(kTeal-5)
	hmethod.SetFillStyle(1001)
	hmethod.SetFillColor(hmethod.GetLineColor()-1)	
	fnew.cd()
	plotname = shortname.replace('_','').replace('CaloSideband','')
	hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,htruth,[hfakemethod,hmethod],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	pad1, pad2 = hmethodsyst[-2:]
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
	hmethod.GetYaxis().SetRangeUser(0.09,themax)		
	hmethod.SetTitle('')
	htruth.SetTitle('')	
	hmethod.SetLineWidth(3)
						
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
			if 'Long' in name: searchbinresults[regionkey]['Long'] = [htruth.Clone(), hmethod.Clone()]
			if 'Short' in name: searchbinresults[regionkey]['Short'] = [htruth.Clone(), hmethod.Clone()]
		
	shortname = shortname.replace('CaloSideband','')
	pdfname = 'pdfs/validation/year'+str(year)+'_'+shortname.replace('_','')+'.pdf'
	c1.Print(pdfname)
	
	#clist.append(c1)
	c1.Delete()
	hratios.append([hratio, hmethodsyst])

for regionkey in searchbinresults:

	print 'doing regionkey', regionkey
	htruthLong, hmethodLong = searchbinresults[regionkey]['Long']
	htruthShort, hmethodShort = searchbinresults[regionkey]['Short']	
	htruthLong.Add(htruthShort)
	hmethodLong.Add(hmethodShort)
	
	
	if year=='2016':
		if datamc=='MC': 
			htruthLong.SetTitle('obs. (Summer16 MC)')	
			hmethodLong.SetTitle('prompt pred. (Summer16 MC)')
		else:
			htruthLong.SetTitle('data (2016)')
			hmethodLong.SetTitle('prompt prediction (2016)')
	if year=='2017':
		if datamc=='MC': 
			htruthLong.SetTitle('obs. (Fall17 MC)')	
			hmethodLong.SetTitle('prompt pred. (Fall17 MC)')
		else:
			htruthLong.SetTitle('data (2017)')
			hmethodLong.SetTitle('prompt prediction (2017)')
	if year=='2018':
		if datamc=='MC': 
			htruthLong.SetTitle('obs. (Autumn18 MC)')	
			hmethodLong.SetTitle('prompt pred. (Autumn18 MC)')
		else:
			htruthLong.SetTitle('data (2018)')
			hmethodLong.SetTitle('prompt prediction (2018)')
			

	themax = 100*max([htruthLong.GetMaximum(),hmethodLong.GetMaximum()])
	hmethodLong.GetYaxis().SetRangeUser(0.01,themax)
	htruthLong.GetYaxis().SetRangeUser(0.01,themax)
		
	plotname = regionkey.replace('_','').replace('CaloSideband','')
	c1 = mkcanvas('c1')
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)
	hratio, hmethodsyst = FabDraw(c1,leg,htruthLong,[hmethodLong],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	pad1, pad2 = hmethodsyst[-2:]
	hratio.GetYaxis().SetRangeUser(0.0,2.4)	
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
	hmethod.SetTitle('')
	htruth.SetTitle('')	
	hmethod.SetLineWidth(3)
			
			

	c1.Update()
	fnew.cd()
	c1.Write('c_'+plotname+'BinNumber_merged')
	
	pdfname = 'pdfs/validation/year'+str(year)+'_'+plotname+'BinNumber_merged'+'.pdf'
	c1.Print(pdfname)
		
	c1.Delete()
	
	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'test c'



