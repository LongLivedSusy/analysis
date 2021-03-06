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

blinding = False

datamc = 'data'

fnameviktor = '/nfs/dust/cms/user/kutznerv/shorttrack/analysis/background-estimation/non-prompt/prediction_zones/fakebg_Run2016_SingleElectron.root'
fnameviktor = '/nfs/dust/cms/user/kutznerv/shorttrack/analysis/analyzer/prediction_zones/fakebg_Run2016_SingleElectron.root'
fviktor = TFile(fnameviktor)

print 'first viktor'
fviktor.ls()



redoBinning = binningAnalysis
redoBinning['DeDxAverage'] = [21,0,7]
redoBinning['TrkPt'] = [30,0,300]
redoBinning['LepMT'] = [8,0,80]
redoBinning['InvMass'] = [20,0,160]
makefolders = False

phase = 0

drawhists = True

zoneOfDedx = {}
zonebinning = binning['DeDxZones']
for izone in range(len(zonebinning)-1):
	dedx_zone = str(zonebinning[izone]).replace('.','p')+'To'+str(zonebinning[izone+1]).replace('.','p')
	zoneOfDedx[izone] = dedx_zone
	
print 'zonebinning', zonebinning
normzone = zoneOfDedx[0]

if phase==0:	
	fCentralMC = 'output/totalweightedbkgsDataDrivenSingleElDataNoSmear.root'
	#fCentralMC = 'output/mediumchunks/TTJets_SingleLeptFromTbar_SmearLeps4ZedFalse.root'
	#fCentralMC = 'testWJHT100.root'
	#fCentralMC = 'output/bigchunks/WJetsSmearLeps4ZedTrue.root'
	#fCentralMC = 'output/bigchunks/TTJetsSmearLeps4ZedTrue.root'
	#fCentralMC = 'output/mediumchunks/WJetsToLNu_HT-100To200SmearLeps4ZedTrue.root'
	#fCentralMC = 'output/totalweightedbkgsNoSmearedKappa.root'
	#fCentralMC = 'test.root'
	listOfVariationFilenames = []

if phase==1:
	fCentralMC = 'output/totalweightedbkgsDataDrivenMCPhase1.root'
	listOfVariationFilenames = ['output/totalweightedbkgsTrueKappaPhase1.root']	
listOfVariationFiles = []
for variationFileName in listOfVariationFilenames: listOfVariationFiles.append(TFile(variationFileName))
variationColors = [kBlue-1, kBlue, kBlue+1]

drawVariations = True
usePredictionWithClosureCorrection = False
			


infile = TFile(fCentralMC)



fout = 'validationPromptFake_phase'+str(phase)+'.root'

fnew = TFile(fout,'recreate')

c1 = mkcanvas('c1')
		
keys = infile.GetListOfKeys()

hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	if 'Fake' in name: continue
	#if not ('DeDxAverage' in name or 'BinNumber' in name): continue
	
	if not 'hEl'==name[:3]: continue
	
	if not 'Validation' in name: continue


	if not ('Control' in name.split('_')[-1]): continue
	if 'hEl'==name[:3]: lepname = 'el'
	if 'hMu'==name[:3]: lepname = '#mu'
	if 'hPi'==name[:3]: lepname = '#pi^#pm/k^#pm'		

	if normzone in name: continue
	
	if zoneOfDedx[2] in name and ('BinNumber' in name): continue# or 'DeDxAverage' in name): continue
	
	controlname = name
	hControl = infile.Get(controlname)	
	hControl.SetTitle('single '+lepname)
	truthname = controlname.replace('Control','Truth')
	print 'starting out on hist', truthname
	hTruth = infile.Get(truthname)
	hTruth.SetTitle('observed (Run2016)')
	
	
	zone = name.split('Zone')[-1].split('_')[0]
	normnameNum     = truthname.replace(zone,normzone)
	controlnameNorm = controlname.replace(zone,normzone)	
	hNormTruth = infile.Get(normnameNum)
	
	hControlNorm = infile.Get(controlnameNorm)	
	
	
	if not ('LepMT' in name or 'InvMass' in name or 'DeDxAverage' in name): continue
	

	viktormethodname = controlname.replace('Control','Method').replace('hEl','').replace('Zone','ZoneDeDx').replace('2p1To4','2p1To4p0').replace('4To99','4p0ToInf').replace('To','to')
	
	
	print 'trying to get', viktormethodname, 'from', fviktor.GetName()
	hViktorMethod = fviktor.Get(viktormethodname)
	
	funkyscale = 1
	hViktorMethod.Scale(funkyscale)
	
	
	print 'taking method name', viktormethodname, 'replacing', zone.replace('2p1To4','2p1To4p0'), 'with', normzone
	vlowdedxname = viktormethodname.replace(zone.replace('2p1To4','2p1To4p0'),normzone).replace('To','to')
	print 'going for dedx fake sideband', vlowdedxname
	hViktorLowDeDx = fviktor.Get(vlowdedxname)
	hViktorLowDeDx.Scale(funkyscale)


		
		
		
	kinvar = name.replace('Control','').replace('Truth','').replace('Method','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
			
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
		
	hMethod = hControl.Clone(controlname)#.replace('Control','Method'))		
		
	hTruth = hTruth.Rebin(nbins,'',newxs)
	hViktorLowDeDx = hViktorLowDeDx.Rebin(nbins,'',newxs)
	hViktorMethod = hViktorMethod.Rebin(nbins,'',newxs)	
	hNormTruth = hNormTruth.Rebin(nbins,'',newxs)
	hViktorLowDeDx = hViktorLowDeDx.Rebin(nbins,'',newxs)
	hMethod = hMethod.Rebin(nbins,'',newxs)
	hControlNorm = hControlNorm.Rebin(nbins,'',newxs)
	
	
	print 'adding', hViktorLowDeDx.GetXaxis().GetNbins(), 'with', hNormTruth.GetXaxis().GetNbins()
	hNormTruth.Add(hViktorLowDeDx,-1)
	hMethod.Divide(hControlNorm)
	hMethod.Multiply(hNormTruth)
	
	histoStyler(hViktorMethod, kRed+2)	
	hViktorMethod.SetFillStyle(1001)
	hViktorMethod.SetFillColor(hViktorMethod.GetLineColor())
	hViktorMethod.SetMarkerStyle(0)
	hViktorMethod.SetTitle('fake prediction')	
	
	
	if 'DeDxAverage' in name:
			hTruth.Add(hNormTruth)
			hTruth.Add(hViktorLowDeDx)# to undo what was done
			hControl.Add(hControlNorm)
			hViktorMethod.Add(fviktor.Get(viktormethodname.replace('2p1To4','0p0To2p1').replace('To','to')),funkyscale)
			hViktorLowDeDx.Add(fviktor.Get(vlowdedxname.replace('2p1To4','0p0To2p1').replace('To','to')),funkyscale)			
			if zone==zoneOfDedx[1]:
				hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2])))
				hControl.Add(infile.Get(name.replace(zone,zoneOfDedx[2])))
				hViktorMethod.Add(fviktor.Get(viktormethodname.replace('2p1To4','4p0ToInf').replace('To','to')),funkyscale)
				hViktorLowDeDx.Add(fviktor.Get(vlowdedxname.replace('2p1To4','4p0ToInf').replace('To','to')),funkyscale)
			#hTruth = infile.Get(truthname.replace(zone,zoneOfDedx[0]))
			#hControl = infile.Get(controlname.replace(zone,zoneOfDedx[0]))
	if 'BinNumber' in name:# or 'DeDxAverage' in name:
		continue
		hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2])))
		hControl.Add(infile.Get(controlname.replace(zone,zoneOfDedx[2])))
		
	
	
	if 'hMu'==name[:3]: 
		hMethod.SetLineColor(kViolet+2)
		hControl.SetLineColor(kRed+2)
	elif 'hPi'==name[:3]:
		hMethod.SetLineColor(kOrange+1)
		hControl.SetLineColor(kOrange)	
	else:
		hMethod.SetLineColor(kGreen+3)	


	if kinvar=='InvMass' and blinding:
		xaxt = hTruth.GetXaxis()
		for ibin in range(1,xaxt.GetNbins()+1):
			if xaxt.GetBinLowEdge(ibin)>=110: hTruth.SetBinContent(ibin, 0)
	if kinvar=='LepMT':
		xaxt = hTruth.GetXaxis()
		for ibin in range(1,xaxt.GetNbins()+1):
			if xaxt.GetBinLowEdge(ibin)>=90: hTruth.SetBinContent(ibin, 0)
				
	hMethod = hMethod.Rebin(nbins,'',newxs)
	hControl = hControl.Rebin(nbins,'',newxs)		
	hNormTruth = hNormTruth.Rebin(nbins,'',newxs)
	hControlNorm = hControlNorm.Rebin(nbins,'',newxs)
		
	hMethod.SetTitle('prompt prediction')
	shortname = name.replace('Control','').replace('Truth','').replace('Method','')
	varname = shortname.split('_')[-1]
	xax = hMethod.GetXaxis()
	hControl.GetXaxis().SetTitle(namewizard(varname))
	hTruth.GetXaxis().SetTitle(namewizard(varname))
	hMethod.GetXaxis().SetTitle(namewizard(varname))    
	

        	
	#leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	leg = mklegend(x1=.5, y1=.5, x2=.99, y2=.8, color=kWhite)
	legname = 'single-lep'
	if 'hEl' in name: legname = legname.replace('lep','electron')
	if 'hMu' in name: legname = legname.replace('lep','muon')
	#hMethod.Scale()
	themax = 1000*max([hMethod.GetMaximum(),hControl.GetMaximum(),hTruth.GetMaximum()])
	themax = 10000*max([hMethod.GetMaximum()])	
	#hMethod.SetFillStyle(1001)
	hMethod.SetFillColor(hMethod.GetLineColor()-1)	
	hMethod.SetLineColor(kGray+2)
	fnew.cd()
	plotname = shortname.replace('_','')
	c1 = mkcanvas('c_'+plotname)
	if makefolders:
		fnew.mkdir(shortname.replace('_',''))
		if 'Bin' in name: 
			hMethodCorrected, hVarCorrectionFactor = makeClosureCorrectionAndUncertainty(hMethod, hTruth)
			fnew.cd()
			hMethodCorrected.Write()
			if usePredictionWithClosureCorrection:
				fnew.cd(plotname) 
				hVarCorrectionFactor.Write()		
				fnew.cd('../')				
				#for ibin in range(1, xax.GetNbins()+1): print 'after', ibin, hVarCorrectionFactor.GetBinContent(ibin)
				hMethod = hMethodCorrected
	

	hratio, pad1, pad2 = FabDraw(c1,leg,hTruth,[hViktorMethod,hMethod],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	
	hMethod.GetYaxis().SetRangeUser(0.1,themax)
	hTruth.GetYaxis().SetRangeUser(0.1,themax)
	hControl.GetYaxis().SetRangeUser(0.1,themax)	
	#hratio.GetYaxis().SetRangeUser(0.0,2.5)
	hratio.GetYaxis().SetRangeUser(-0.1,2.6)	
	hratio.GetYaxis().SetTitle('data/prediction')
	#hratio.GetYaxis().SetRangeUser(-3,3)		
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	c1.cd(2)
	c1.SetLogy()
	c1.Update()
	c1.cd(1)
	hMethod.SetTitle('')
	hTruth.SetTitle('')
						
	c1.Update()
	fnew.cd()
	c1.Write()
	if 'BinNumber' in name:
		hTruth.Write(truthname.replace('Zone'+zone,''))
		hMethod.Write(truthname.replace('Zone'+zone,'').replace('Truth','Method'))		
	#hTruth.Write()
	#hMethod.Write()
	
	c1.Print('pdfs/validation/'+shortname.replace('_','')+'.pdf')
	
	clist.append(c1)
	hratios.append([hratio, pad1, pad2])
	c1.Update()


	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'test c'



