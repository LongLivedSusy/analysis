from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep
lumi = 35.6 #just for labeling. this weightw as already applied
#must agree with lumi in merged...py!


redoBinning = binning#binningAnalysis
#redoBinning = binning
makefolders = False

phase = 0

drawhists = True

if phase==0:
	fMCs = ['output/bigchunks/TTJetsNoZSmear.root','output/bigchunks/WJetsNoZSmear.root']
	fData = 'output/totalweightedbkgsDataDrivenDataNoSmear.root'
if phase==1:
	fMC = 'output/totalweightedbkgsDataDrivenMCNoZSmear.root'
	fData = 'output/totalweightedbkgsDataDrivenDataNoSmear.root'	
			

testscale = 1# = lumi*1000


mcfile = TFile(fMCs[0])
mcfile.ls()
datfile = TFile(fData)

fout = 'datamc_phase'+str(phase)+'.root'

fnew = TFile(fout,'recreate')

c1 = mkcanvas('c1')


		
keys = mcfile.GetListOfKeys()
names = []
for key in keys: 
	name = key.GetName()
	names.append(name)
	
mcfile.Close()

hratios = []
clist = []
print 'len(keys)', len(keys)
for name in sorted(names):#[:241]:
	mcfile.cd()
	if not 'Control' in name: continue
	hData = datfile.Get(name)
		
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

        
	leg = mklegend(x1=.7, y1=.6, x2=.92, y2=.8, color=kWhite)
	legname = 'single-lep'
	if 'hElB' in name: legname = legname.replace('lep','electron')
	if 'hMuB' in name: legname = legname.replace('lep','muon')
	hData.SetTitle('data')
	hData.SetLineColor(kBlack)
	hData.SetMarkerColor(kBlack)
	hData.SetMarkerStyle(22)
	hData.SetDirectory(0)
	#leg.AddEntry(hData,'data','lp')
	
	hmcs = []
	for imc, fMC in enumerate(fMCs):
		mcfile = TFile(fMC)
		hMC = mcfile.Get(name)
	
		hMC.Scale(lumi/136)
		#leg.AddEntry(hMC,'MC','lp')	
		themax = 10000*max([hMC.GetMaximum(),hData.GetMaximum()])
		hMC.GetYaxis().SetRangeUser(0.001,themax)
		hData.GetYaxis().SetRangeUser(0.001,themax)	
		#hVarMethod.SetFillStyle(1001)
		hMC.SetFillStyle(1001)
		if 'hElB' in name:
			hMC.SetLineColor(kGreen+1)
		if 'hMuB' in name:
			hMC.SetLineColor(kViolet+1)			
		if 'hPiB' in name:
			hMC.SetLineColor(kOrange+1)						
		hMC.SetFillColor(hMC.GetLineColor()-1+imc)
		hMC.SetDirectory(0)
		hMC.SetTitle(mcfile.GetName().replace('output/bigchunks/','').split('NoZ')[0])
		mcfile.Close()
		
		if len(redoBinning[kinvar])!=3: hMC = hMC.Rebin(nbins,'',newxs)
		else: hMC = hMC.Rebin(nbins,'',newxs)
				
		hmcs.append(hMC)

	fnew.cd()
	plotname = name.replace('_','')
	c1 = mkcanvas('c_'+plotname)

	#hratio = FabDraw(c1,leg,hVarTruth,[hVarMethod],datamc='MC',lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	hratio = FabDraw(c1,leg,hData,hmcs,datamc='MC',lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	hratio.GetYaxis().SetRangeUser(-0.1,2.6)	
	hratio.GetYaxis().SetTitle('Events/bin')
	hratio.GetXaxis().SetTitle(kinvar)
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
	hMC.SetTitle('')
	#hMC.Draw('same p')

	c1.Update()
	fnew.cd()
	c1.Write()
	clist.append(c1)	
	#c1.Print('pdfs/closure/prompt-bkg/'+shortname.replace('_','')+'.pdf')
	


print 'test a'
	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'test c'



