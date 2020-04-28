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

mycutedatatest = False
if mycutedatatest: datamc = 'data'
else: datamc = 'MC'

redoBinning = binning
#redoBinning['DeDxAverage'] = [42,0,7]
redoBinning['Mht'] = [45,0,960]
redoBinning['Met'] = [45,0,960]
redoBinning['InvMass'] = [60,50,170]
redoBinning['ElPt'] = [30,0,300]
redoBinning['TrkEta'] = [15,0,3]
redoBinning['MuPt'] = redoBinning['ElPt']
redoBinning['DeDxAverage'] = [15,1,7]
#redoBinning['TrkPt'] = [30,0,300]

#redoBinning['DeDxAverage'] = [1,1,7]
#redoBinning['MinDPhiMhtJets'] = [1,redoBinning['MinDPhiMhtJets'][1],redoBinning['MinDPhiMhtJets'][2]]
#redoBinning['Ht'] = [1,redoBinning['Ht'][1],redoBinning['Ht'][2]]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']

makefolders = False

phase = 0

zoneOfDedx = {}
zonebinning = binning['DeDxZones']
for izone in range(len(zonebinning)-1):
	dedx_zone = str(zonebinning[izone]).replace('.','p')+'to'+str(zonebinning[izone+1]).replace('.','p')
	zoneOfDedx[izone] = dedx_zone
	
print 'zonebinning', zonebinning
normzone = zoneOfDedx[0]

if phase==0:	
	if mycutedatatest: fCentralMC = 'output/totalweightedbkgsDataDrivenSingleElDataNoSmear.root'#for my cute
	else:fCentralMC = 'output/promptDataDrivenMCSummer16.root'
	#fCentralMC = 'test.root'

if phase==1: fCentralMC = 'output/promptDataDrivenMCFall17.root'
	

CombineLeptons_ = True

infile = TFile(fCentralMC)
#infile.ls()

fout = 'closureAbcd_phase'+str(phase)+'.root'
if mycutedatatest: fout = fout.replace('.root','_cute.root')

fnew = TFile(fout,'recreate')

c1 = mkcanvas('c1')
		
keys = infile.GetListOfKeys()

'''
hcontrollow = infile.Get('hElSElValidationZLLendcapZone0p0to2p1_InvMassControl')
hcontrolmed = infile.Get('hElSElValidationZLLendcapZone2p1to4p0_InvMassControl')
hcontrolhigh = infile.Get('hElSElValidationZLLendcapZone4p0to99_InvMassControl')
'''
#get eta-weighted de/dx extrapolator
hcelow = infile.Get('hElSElValidationZLLendcapZone0p0to2p1_InvMassControl')
hcemed = infile.Get('hElSElValidationZLLendcapZone2p1to4p0_InvMassControl')
hcehigh = infile.Get('hElSElValidationZLLendcapZone4p0to99_InvMassControl')
hcblow = infile.Get('hElSElValidationZLLbarrelZone0p0to2p1_InvMassControl')
hcbmed = infile.Get('hElSElValidationZLLbarrelZone2p1to4p0_InvMassControl')
hcbhigh = infile.Get('hElSElValidationZLLbarrelZone4p0to99_InvMassControl')
hetaweighting = infile.Get('hElSElValidationZLLZone2p1to4p0_TrkEtaTruth')
etaax = hetaweighting.GetXaxis()
ntot = hetaweighting.Integral()
hb = hetaweighting.Integral(etaax.FindBin(0), etaax.FindBin(1.5))
he = hetaweighting.Integral(etaax.FindBin(1.5), etaax.FindBin(2.5))
weightb = hb/(hb+he)
weighte = he/(hb+he)
print 'weights are', weightb, weighte
hcontrollow = hcelow.Clone(); hcontrollow.Reset()
hcontrollow.Add(hcelow, weighte); hcontrollow.Add(hcblow, weightb)
hcontrolmed = hcemed.Clone(); hcontrolmed.Reset()
hcontrolmed.Add(hcemed, weighte); hcontrolmed.Add(hcbmed, weightb)
hcontrolhigh = hcehigh.Clone(); hcontrolhigh.Reset()
hcontrolhigh.Add(hcehigh, weighte); hcontrolhigh.Add(hcbhigh, weightb)


mxax = hcontrollow.GetXaxis()

highlowZeeA = hcontrolmed.Integral (mxax.FindBin(65),mxax.FindBin(110))/hcontrollow.Integral(mxax.FindBin(65),mxax.FindBin(110))
highlowZeeB = hcontrolhigh.Integral(mxax.FindBin(65),mxax.FindBin(110))/hcontrollow.Integral(mxax.FindBin(65),mxax.FindBin(110))


hratios = []
clist = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	
	if 'Fake' in name: continue
	
		
	if CombineLeptons_: 
		if not ('Control' in name.split('_')[-1] and 'hEl'==name[:3]): continue# and 'hElBaseline' in name): continue
		lepname = 'candidate (el, #mu, or #pi^{#pm})'
	else: 
		if not ('Control' in name.split('_')[-1]): continue
		if 'hEl'==name[:3]: lepname = 'el'
		if 'hMu'==name[:3]: lepname = '#mu'
		if 'hPi'==name[:3]: lepname = '#pi^#pm/k^#pm'		

	if normzone in name: continue
	
	kinvar = name.replace('Control','').replace('Truth','').replace('Method','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
	
	if zoneOfDedx[2] in name and ('BinNumber' in name or 'DeDxAverage' in name): continue
	
	controlname = name
	
	zone = name.split('Zone')[-1].split('_')[0]

	truthname = controlname.replace('Control','Truth')
	print 'starting out on hist', truthname
	hTruth = infile.Get(truthname).Clone(truthname+'_copy')
	hTruth.SetTitle('MC observed (prompt)')
	
	
	
	normnameNum     = truthname.replace(zone,normzone)

	
	hNormTruth = infile.Get(normnameNum)
	
		
	if CombineLeptons_: 
		hTruth.Add(infile.Get(truthname.replace('hEl','hMu')))
		hTruth.Add(infile.Get(truthname.replace('hEl','hPi')))	
		hNormTruth.Add(infile.Get(normnameNum.replace('hEl','hMu')))
		hNormTruth.Add(infile.Get(normnameNum.replace('hEl','hPi')))		
		
	
	#hTruth.Draw()
	#c1.SetLogy()
	#c1.Update()
	#pause()	
	
	if 'BinNumber' in name:# or 'DeDxAverage' in name:
		hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2])))
		if CombineLeptons_:
			hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2]).replace('hEl','hMu')))
			hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2]).replace('hEl','hPi')))

		
	if 'DeDxAverage' in name:
		# can get full shape from the El CR
		hMethod = infile.Get('hElSElValidationZLLZone2p1to4p0_DeDxAverageControl').Clone(name+'_dy')
		hMethod.Add(infile.Get('hElSElValidationZLLZone0p0to2p1_DeDxAverageControl'))
		hMethod.Add(infile.Get('hElSElValidationZLLZone4p0to99_DeDxAverageControl'))
		hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2])))
		hTruth.Add(infile.Get(truthname.replace(zone,normzone)))
		if CombineLeptons_: 	
			hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2]).replace('hEl','hMu')))
			hTruth.Add(infile.Get(truthname.replace(zone,normzone).replace('hEl','hMu')))
			hTruth.Add(infile.Get(truthname.replace(zone,zoneOfDedx[2]).replace('hEl','hPi')))
			hTruth.Add(infile.Get(truthname.replace(zone,normzone).replace('hEl','hPi')))			
	else: 
		hMethod = hNormTruth.Clone(name+'_control')#.replace('Control','Method'))
		

	#if not 'BinNumber' in name: continue
			
	
	
	
	if 'BinNumber' in name:
		for ibin in range(1,hMethod.GetXaxis().GetNbins()+1):
			val, err = hMethod.GetBinContent(ibin), hMethod.GetBinError(ibin)
			if val>0: relerr = err/val
			else: relerr = 0.
			if ibin%2==0: 
				val = highlowZeeA*val
			else:
				val = highlowZeeB*val
			err = relerr*val	
			hMethod.SetBinContent(ibin, val)
			hMethod.SetBinError(ibin, err)
	elif 'DeDxAverage' in name:
		xaxdedx = hTruth.GetXaxis()
		#sfactor = hTruth.Integral(xaxdedx.FindBin(0),xaxdedx.FindBin(2.1))/hMethod.Integral(xaxdedx.FindBin(0),xaxdedx.FindBin(2.1))
		sfactor = infile.Get(truthname.replace(zone,normzone)).Integral()/infile.Get('hElSElValidationZLLZone0p0to2p1_DeDxAverageControl').Integral()
		hMethod.Scale(sfactor)
		print 'dedx integral on name', name, 'is', hMethod.Integral()
		#pause()
	else:
		if '2p1' in name: 
			hMethod.Scale(highlowZeeA)
			if 'Min' in name: 
				print 'min thingy integral on name', name, 'is', hMethod.Integral()
				#pause()
		if 'to99' in name: hMethod.Scale(highlowZeeB)	
	

	
	if 'hMu'==name[:3]: 
		hMethod.SetLineColor(kViolet+2)
	elif 'hPi'==name[:3]:
		hMethod.SetLineColor(kOrange+1)
	else:
		hMethod.SetLineColor(kGreen+3)
		
		
		
	
			
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
	hTruth = hTruth.Rebin(nbins,'',newxs)
	if mycutedatatest: 
		if kinvar=='InvMass':
			xaxt = hTruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: hTruth.SetBinContent(ibin, 0)
		if kinvar=='LepMT':
			xaxt = hTruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=90: hTruth.SetBinContent(ibin, 0)
	hMethod = hMethod.Rebin(nbins,'',newxs)

	hNormTruth = hNormTruth.Rebin(nbins,'',newxs)

	hMethod.SetTitle('prediction')
	shortname = name.replace('Control','').replace('Truth','').replace('Method','')
	if CombineLeptons_: shortname = shortname.replace('hEl','hObj')[1:]
	varname = shortname.split('_')[-1]
	xax = hMethod.GetXaxis()

	hTruth.GetXaxis().SetTitle(namewizard(varname))
	hMethod.GetXaxis().SetTitle(namewizard(varname))    
	

        	
	#leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	leg = mklegend(x1=.5, y1=.5, x2=.93, y2=.8, color=kWhite)
	leg.AddEntry(hNormTruth,'de/dx sideband','l')
	legname = 'single-lep'
	if 'hEl' in name: legname = legname.replace('lep','electron')
	if 'hMu' in name: legname = legname.replace('lep','muon')

	#hMethod.Scale()
	themax = 10000*max([hMethod.GetMaximum(),hTruth.GetMaximum()])
	hMethod.GetYaxis().SetRangeUser(0.01,themax)
	#hMethod.SetFillStyle(1001)
	hMethod.SetFillColor(hMethod.GetLineColor()-1)	
	hTruth.GetYaxis().SetRangeUser(0.01,themax)
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
	

	hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,hTruth,[hMethod],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	#hratio.GetYaxis().SetRangeUser(0.0,2.5)
	hratio.GetYaxis().SetRangeUser(0.0,2.6)	
	hratio.GetYaxis().SetTitle('(B/A*C)/D')
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

	hNormTruth.SetLineColor(kAzure)
	hNormTruth.Draw('same')
	
	hMethod.SetLineWidth(3)
						
	c1.Update()
	fnew.cd()
	c1.Write()
	if 'BinNumber' in name:
		hTruth.Write(truthname.replace('Zone'+zone,''))
		hMethod.Write(truthname.replace('Zone'+zone,'').replace('Truth','Method'))		

	
	c1.Print('pdfs/closure/prompt-bkg/ZShape/phase'+str(phase)+shortname.replace('_','')+'.png')
	
	clist.append(c1)
	#c1.Delete()
	hratios.append([hratio, hmethodsyst])
	c1.Update()
	#pause()

	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'test c'



