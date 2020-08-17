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
extrascale = 137./35.9

datamc = 'data'# should pretty much always be this way
doblinding = True
dofakesidebandsubtraction = True

'''
rm -rf pdfs/validation/prompt-bkg/MatchedCalo/*
python tools/makeValidationPlots2methods.py 2016 && python tools/makeValidationPlots2methods.py 2017 && python tools/makeValidationPlots2methods.py 2018  
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
redoBinning['InvMass'] = [20,50,170]
redoBinning['ElPt'] = [30,0,300]
redoBinning['Ht']=[5,0,2000]
redoBinning['Met'] = [20,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['TrkPt']=[5,0,150]
redoBinning['TrkEta'] = [5,0,3]
redoBinning['MatchedCalo'] = [0,10,13,23,40]
#redoBinning['InvMass'] = [25,0,200]#same as analysis
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

calm = 15
calh = 22

calm = 17
calh = 27

#calm = 20
#calh = 30


if year=='2017': lumi = 41.8
if year=='2018': lumi = 55.0

if year=='2016': mainfilename = 'rootfiles/PromptBkgTree_promptDataDrivenRun2016_mcal'+str(calm)+'to'+str(calh)+'.root'
if year=='2017': mainfilename = 'rootfiles/PromptBkgTree_promptDataDrivenRun2017_mcal'+str(calm)+'to'+str(calh)+'.root'
if year=='2018': mainfilename = 'rootfiles/PromptBkgTree_promptDataDrivenRun2018_mcal'+str(calm)+'to'+str(calh)+'.root'

infile = TFile(mainfilename)
infile.ls()
keys = infile.GetListOfKeys()

hShapeShort = infile.Get('hPromptShortSElValidationZLL_MatchedCaloTruth').Clone('hShapeShort')##
shax = hShapeShort.GetXaxis()
binm = shax.FindBin(calm)
binh = shax.FindBin(calh)


fout = 'validation_year'+str(year)+'.root'
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
	
	if not ('Validation' in name or 'MhtSideband' in name or 'Baseline' in name): continue
	
	if not 'Truth' in name: continue
	#if not 'Baseline' in name: continue
	if not 'CaloSideband' in name: continue
	if not 'hPrompt' in name: continue
	if 'FakeCr' in name: continue
	

	kinvar = name.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
	
	hsideband =   infile.Get(name).Clone()
	hsideband.Scale(extrascale)
	
	htruth = infile.Get(name.replace('CaloSideband','')).Clone()
	htruth.Scale(extrascale)
	
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
			
			
	
	hpromptmethod = infile.Get(name.replace('Truth','Method2')).Clone()
	hpromptmethod.Scale(extrascale)
	fakecontrib2sub_name = name.replace('hPrompt','hFake').replace('Truth','Method3').replace('_','FakeCr_')
	hfakecontrib2sub = infile.Get(fakecontrib2sub_name).Clone()		
	hfakecontrib2sub.Scale(extrascale)
	if dofakesidebandsubtraction: 
		hpromptmethod.Add(hfakecontrib2sub,-1)	
		for ibin in range(1,hpromptmethod.GetXaxis().GetNbins()+1):
			if hpromptmethod.GetBinContent(ibin)<0: hpromptmethod.SetBinContent(ibin, 0) ## needs a systematic?		
	

	hfakemethod = infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_')) ###
	hfakemethod.Scale(extrascale)
	histoStyler(hfakemethod,kRed+2) ###
	hfakemethod.SetFillColor(kRed+2)
	hfakemethod.SetFillStyle(1001)
		
	if 'BinNumber' in name:
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
				
			

		
	if year=='2016':
		if datamc=='MC': 
			htruth.SetTitle('obs. (Summer16 MC)')	
			hpromptmethod.SetTitle('prompt pred. (Summer16 MC)')
			hfakemethod.SetTitle('prompt pred. (Summer16 MC)')
		else:
			htruth.SetTitle('data (2016)')
			hpromptmethod.SetTitle('prompt prediction (2016)')
			hfakemethod.SetTitle('fake pred. (2016)')
	if year=='2017':
		if datamc=='MC': 
			htruth.SetTitle('obs. (Fall17 MC)')	
			hpromptmethod.SetTitle('prompt pred. (Fall17 MC)')
			hfakemethod.SetTitle('prompt pred. (Fall17 MC)')
		else:
			htruth.SetTitle('data (2017)')
			hpromptmethod.SetTitle('prompt prediction (2017)')
			hfakemethod.SetTitle('fake pred. (2017)')	
	if year=='2018':
		if datamc=='MC': 
			htruth.SetTitle('obs. (Autumn18 MC)')	
			hpromptmethod.SetTitle('prompt pred. (Autumn18 MC)')
			hfakemethod.SetTitle('prompt pred. (Autumn18 MC)')
		else:
			htruth.SetTitle('data (2018)')
			hpromptmethod.SetTitle('prompt prediction (2018)')
			hfakemethod.SetTitle('fake pred. (2018)')						
			

	
	c1 = mkcanvas('c1')
	shortname = name.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
	directory = shortname.split('_')[0].replace('hPrompt','').replace('CaloSideband','')
	if not directory in directories:
		directories.append(directory)
		if not os.path.exists('pdfs/validation/prompt-bkg/MatchedCalo/'+directory):
			os.system('mkdir -p pdfs/validation/prompt-bkg/MatchedCalo/'+directory)	

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

	if 'BinNumber' in name:
		hpromptmethod.Write(hpromptmethod.GetName().replace('CaloSideband','').replace('Method2','Method'))
		hfakemethod.Write(hfakemethod.GetName().replace('FakeCr','').replace('Method1','Method'))
		if 'Short' in name or 'Long' in name:
			regionkey = name.split('_')[0].replace('hPrompt','').replace('Long','').replace('Short','')
			if not regionkey in searchbinresults.keys(): searchbinresults[regionkey] = {}
			if 'Long' in name: searchbinresults[regionkey]['Long'] = [htruth.Clone(), hpromptmethod.Clone(),hfakemethod.Clone()]
			if 'Short' in name: searchbinresults[regionkey]['Short'] = [htruth.Clone(), hpromptmethod.Clone(), hfakemethod.Clone()]
		
	shortname = shortname.replace('CaloSideband','')
	pdfname = 'pdfs/validation/prompt-bkg/MatchedCalo/'+directory+'/year'+str(year)+'_'+shortname.replace('_','')+'.png'
	c1.Print(pdfname)	
	
	#clist.append(c1)
	c1.Delete()
	hratios.append([hratio, hpromptmethodsyst])

for regionkey in searchbinresults:
	break
	print 'doing regionkey', regionkey
	htruthLong, hpromptmethodLong, hfakemethodLong = searchbinresults[regionkey]['Long']
	htruthShort, hpromptmethodShort, hfakemethodShort = searchbinresults[regionkey]['Short']	
	htruthLong.Add(htruthShort)
	hpromptmethodLong.Add(hpromptmethodShort)
	
	
	if year=='2016':
		if datamc=='MC': 
			htruthLong.SetTitle('obs. (Summer16 MC)')	
			hpromptmethodLong.SetTitle('prompt pred. (Summer16 MC)')
			hfakemethodLong.SetTitle('fake pred. (Summer16 MC)')			
		else:
			htruthLong.SetTitle('data (2016)')
			hpromptmethodLong.SetTitle('prompt prediction (2016)')
			hfakemethodLong.SetTitle('fake prediction (2016)')			
	if year=='2017':
		if datamc=='MC': 
			htruthLong.SetTitle('obs. (Fall17 MC)')	
			hpromptmethodLong.SetTitle('prompt pred. (Fall17 MC)')
			hfakemethodLong.SetTitle('fake pred. (Fall17 MC)')			
		else:
			htruthLong.SetTitle('data (2017)')
			hpromptmethodLong.SetTitle('prompt prediction (2017)')
			hfakemethodLong.SetTitle('fake prediction (2017)')	
	if year=='2018':
		if datamc=='MC': 
			htruthLong.SetTitle('obs. (Autumn18 MC)')	
			hpromptmethodLong.SetTitle('prompt pred. (Autumn18 MC)')
			hfakemethodLong.SetTitle('fake pred. (Autumn18 MC)')			
		else:
			htruthLong.SetTitle('data (2018)')
			hpromptmethodLong.SetTitle('prompt prediction (2018)')
			hfakemethodLong.SetTitle('fake prediction (2018)')			
			

	themax = 100*max([htruthLong.GetMaximum(),hpromptmethodLong.GetMaximum()])
	hpromptmethodLong.GetYaxis().SetRangeUser(0.01,themax)
	htruthLong.GetYaxis().SetRangeUser(0.01,themax)
		
	plotname = regionkey.replace('_','').replace('CaloSideband','')
	c1 = mkcanvas('c1')
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)
	hratio, hpromptmethodsyst = FabDraw(c1,leg,htruthLong,[hpromptmethodLong,hfakemethodLong],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	pad1, pad2 = hpromptmethodsyst[-2:]
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
	hpromptmethod.SetTitle('')
	htruth.SetTitle('')	
	hpromptmethod.SetLineWidth(3)
			
			

	c1.Update()
	fnew.cd()
	c1.Write('c_'+plotname+'BinNumber_merged')
	hpromptmethodLong.Write(hpromptmethodLong.GetName().replace('CaloSideband','MASTER'))
	hfakemethodLong.Write(hfakemethodLong.GetName().replace('FakeCr','MASTER'))	
	if not os.path.exists('pdfs/validation/prompt-bkg/MatchedCalo/'+'SearchBins/'):
		os.system('mkdir pdfs/validation/prompt-bkg/MatchedCalo/'+'SearchBins/')
	pdfname = 'pdfs/validation/prompt-bkg/MatchedCalo/SearchBins/year'+str(year)+'_'+shortname.replace('_','')+'.png'
	c1.Print(pdfname)	
		
	c1.Delete()
	
	
import os, sys
os.system('echo echo hello > htmlwhippy.sh')
pipe = '>'
print 'reached the end of things'
for directory_ in directories:
	os.system('echo python tools/whiphtml.py \\"pdfs/validation/prompt-bkg/MatchedCalo/'+directory_+'/*.png\\" '+pipe+' htmlwhippy.sh')
	pipe = '>>'
os.system('bash htmlwhippy.sh')
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'now do'
print 'cp -r pdfs/validation/prompt-bkg/MatchedCalo /afs/desy.de/user/b/beinsam/www/DisappearingTracks/validation/'
print 'could also have done'
print 'rm -rf pdfs/validation/prompt-bkg/MatchedCalo/*'



