from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep
lumi = 35.6 #just for labeling. this weightw as already applied
#lumi = 5.746 # for 2016 B tests
#lumi = 2.572 # 2016C tests
#must agree with lumi in merged...py!

######Ok, I need to track down, event by event, which are getting filled in NoCuts mode for a control region muon

#lumi = 35.9 # for Sang Il Muon comparison
simple = False

redoBinning = binningAnalysis
redoBinning['InvMass'] = [60,50,170]
redoBinning['ElPt'] = [30,0,300]
redoBinning['TrkEta'] = [15,0,3]
redoBinning['MuPt'] = redoBinning['ElPt']
redoBinning['DeDxAverage'] = [35,0,7]
makefolders = False

basezone = '0p0to2p1'

phase = 0
drawhists = True


if phase==0:
	fMCs = ['output/bigchunks/Summer16ZJetsToNuNu.root','output/bigchunks/Summer16QCD.root','output/bigchunks/Summer16WJets.root','output/bigchunks/Summer16TTJets.root','output/bigchunks/Summer16VV.root','output/bigchunks/Summer16DYJets.root']
	fData = 'output/promptDataDrivenSingleElData2016.root'
	#fData = 'output/totalweightedbkgsDataDrivenSingleMuDataNoSmear.root'	
	#fData = 'output/totalweightedbkgsDataDrivenDataNoSmear.root'
	#fData = 'output/totalweightedRun2016BMET.root'
if phase==1:
	fMCs = ['output/bigchunks/Fall17ZJetsToNuNu.root','output/bigchunks/Fall17QCD.root','output/bigchunks/Fall17WJets.root','output/bigchunks/Fall17TTJets.root','output/bigchunks/Fall17VV.root','output/bigchunks/Fall17DYJets.root']
	fData = 'output/promptDataDrivenSingleElData2017.root'	

testscale = 1# = lumi*1000


if simple:
	#for fn in fMCs: fn = fn.replace('.root','_simple.root')
	fData = fData.replace('.root','_simple.root')	

print 'fData' , fData

mcfile = TFile(fMCs[0])
mcfile.ls()
datfile = TFile(fData)

fout = 'datamc_phase'+str(phase)+'.root'
if simple: fout = fout.replace('.root','_simple.root')
fnew = TFile(fout,'recreate')

c1 = mkcanvas('c1')

colors = [kBlue+1, kOrange+1, kGreen+1, kViolet+1, kTeal, kRed+1]
		
keys = mcfile.GetListOfKeys()
names = []
for key in keys: names.append(key.GetName())
	
mcfile.Close()

hratios = []
clist = []
print 'len(keys)', len(keys)
for name in sorted(names):#[:241]:
	mcfile.cd()
	if simple:
		if not 'Truth' in name: continue	
	else:
		if not 'Control' in name: continue
	
	if not 'Validation' in name: continue
		
	print 'going for', name, 'from', datfile.GetName()
	hData = datfile.Get(name)

	if 'Zone' in name:
		if not basezone in name: continue
		print 'hData.GetName()', hData.GetName()
		hData.Add(datfile.Get(name.replace(basezone,'2p1to4p0')))
		hData.Add(datfile.Get(name.replace(basezone,'4p0to99')))		
		
				
	kinvar = name.replace('Method','').replace('Truth','').replace('Control','')
	kinvar = kinvar[kinvar.find('_')+1:]


	if len(redoBinning[kinvar])!=3: 
		nbins = len(redoBinning[kinvar])-1
		newxs = array('d',redoBinning[kinvar])
		hData = hData.Rebin(nbins,'',newxs)
	else:
		newbinning = []
		stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
		for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
		nbins = len(newbinning)-1
		newxs = array('d',newbinning)
		hData = hData.Rebin(nbins,'',newxs)

        
	leg = mklegend(x1=.69, y1=.36, x2=.945, y2=.78, color=kWhite)
	legname = 'single-lep'
	if 'hElB' in name: legname = legname.replace('lep','electron')
	if 'hMuB' in name: legname = legname.replace('lep','muon')
	hData.SetTitle('data')
	hData.SetLineColor(kBlack)
	hData.SetMarkerColor(kBlack)
	hData.SetMarkerStyle(22)
	hData.SetDirectory(0)
	
	hmcs = []
	for imc, fMC in enumerate(fMCs):
		mcfile = TFile(fMC)
		hMC = mcfile.Get(name).Clone(name+str(imc))
		
		if basezone in name:
			hMC.Add(mcfile.Get(name.replace(basezone,'2p1to4p0')).Clone(name.replace(basezone,'2p1to4p0')+str(imc)))
			hMC.Add(mcfile.Get(name.replace(basezone,'4p0to99')).Clone(name.replace(basezone,'4p0to99')+str(imc)))
				
		hMC.SetDirectory(0)
		#hMC.Scale(1.0*lumi/136)

		#if 'WJ' in fMC: hMC.Scale(3)
		themax = 5*max([hMC.GetMaximum(),hData.GetMaximum()])
		hMC.GetYaxis().SetRangeUser(1,themax)
		hData.GetYaxis().SetRangeUser(1,themax)	
		#hVarMethod.SetFillStyle(1001)
		hMC.SetFillStyle(1001)
		
		hMC.SetLineColor(colors[imc]+1)
		hMC.SetFillColor(hMC.GetLineColor()-1)
		hMC.SetTitle(mcfile.GetName().replace('output/bigchunks/','').split('Smear')[0].replace('Summer16',''))
		mcfile.Close()
		
		if len(redoBinning[kinvar])!=3: hMC = hMC.Rebin(nbins,'',newxs)
		else: hMC = hMC.Rebin(nbins,'',newxs)
				
		hmcs.append(hMC)

	fnew.cd()
	plotname = name.replace('_','')
	c1 = mkcanvas('c_'+plotname)

	#hratio = FabDraw(c1,leg,hVarTruth,[hVarMethod],datamc='MC',lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	hratio, pad1, pad2 = FabDraw(c1,leg,hData,hmcs,datamc='data',lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	
	hMC.GetYaxis().SetRangeUser(1.,themax)
	hData.GetYaxis().SetRangeUser(1.,themax)	
			
	hratio.GetYaxis().SetRangeUser(0.0,2.35)	
	
	if 'Eta' in name: 
		hMC.GetYaxis().SetRangeUser(100.,themax)
		hData.GetYaxis().SetRangeUser(100.,themax)		
	hratio.GetYaxis().SetTitle('data/MC')
	hratio.GetXaxis().SetTitle(kinvar)
	hratio.SetLineColor(kBlack)

	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	hratio.GetXaxis().SetTitle(namewizard(hratio.GetXaxis().GetTitle()))
	c1.cd(2)
	c1.SetLogy()
	c1.Update()
	c1.cd(1)
	hMC.SetTitle('')
	if 'DeDx' in name:
		tline = TLine()
		tline.SetLineWidth(3)
		tline.SetLineStyle(kDashed)
		tline.SetLineColor(kBlack)		
		tline.DrawLine(2.1,0,2.1,.005*themax)
		tline.DrawLine(4.0,0,4.0,.005*themax)
		tl.SetTextSize(1.3*tl.GetTextSize())
		tl.DrawLatex(0.18, .6, 'sideband')
		tl.DrawLatex(.37, .6, 'intermediate')
		tl.DrawLatex(.6, .6, 'upper')
		tl.SetTextSize(tl.GetTextSize()/1.3)
		pad1.SetGridx(0)	
		
	if 'InvMass' in name:
		tline = TLine()
		tline.SetLineWidth(3)
		tline.SetLineStyle(kDashed)
		tline.SetLineColor(kBlack)		
		tline.DrawLine(65,0,65,.003*themax)
		tline.DrawLine(110.0,0,110.0,.003*themax)
		tl.SetTextSize(1.3*tl.GetTextSize())
		tl.DrawLatex(0.3, .6, 'e^{+}e^{-} DY CR')
		tl.SetTextSize(tl.GetTextSize()/1.3)
		pad1.SetGridx(0)					
	elif 'Validation' in name and 'ZLL' in name:
		tl.SetTextSize(1.3*tl.GetTextSize())
		tl.DrawLatex(0.52, .71, 'e^{+}e^{-} DY CR')
		tl.SetTextSize(tl.GetTextSize()/1.3)	
	
	c1.Update()
	fnew.cd()
	c1.Write()
	clist.append(c1)	
	c1.Print('pdfs/controlregions/phase'+str(phase)+plotname.replace('_','')+'.png')
		
import os, sys
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()



