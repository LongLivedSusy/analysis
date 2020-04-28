from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
gStyle.SetOptStat(0)
#gROOT.SetBatch(1)
from time import sleep
lumi = 35.9 #just for labeling. this weightw as already applied
#must agree with lumi in merged...py!



datamc = 'MC'

mainzone = 'Zone2p1To4'
sideband = 'Zone0p0To2p1'
tightzone ='Zone4To99'

biggerNormbox = False
redoBinning = binningAnalysis
redoBinning['DeDxAverage'] = [42,0,7]
redoBinning['TrkPt'] = [30,0,300]

makefolders = False

phase = 0

drawhists = True
firsttime = True
zoneOfDedx = {}
zonebinning = binning['DeDxZones']
for izone in range(len(zonebinning)-1):
	dedx_zone = str(zonebinning[izone]).replace('.','p')+'To'+str(zonebinning[izone+1]).replace('.','p')
	zoneOfDedx[izone] = dedx_zone
	
print 'zonebinning', zonebinning
normzone = zoneOfDedx[0]

if phase==0:	
	fCentralMC = 'output/totalweightedbkgsDataDrivenMCSmearLeps4ZedFalse.root'

if phase==1:
	fCentralMC = 'output/totalweightedbkgsDataDrivenMCPhase1.root'


			

infile = TFile(fCentralMC)
#infile.ls()

fout = 'dedxConsistency_phase'+str(phase)+'.root'

fnew = TFile(fout,'recreate')

c1 = mkcanvas('c1')
leg = mklegend(x1=.53, y1=.5, x2=.92, y2=.9, color=kWhite)
		
keys = infile.GetListOfKeys()

colors = [kAzure+1,   kBlue, kRed, kGreen+1, kYellow, kTeal-5, kCyan, kOrange, kSpring, kTeal, kAzure, kViolet, kTeal, kOrange+2, kCyan+2, kViolet+1, kRed+1, kGray+2, kBlue+1]
hlist = []

names = []
for key in keys: names.append(key.GetName())
names = sorted(names)

for name in names:
	if not 'Control' in name: continue
	if not 'DeDx' in name: continue
	if not 'hEl' in name: continue
	if not mainzone in name: continue
	
	print 'getting', name
	h = infile.Get(name).Clone()
	#h.Rebin(5)
	h.Add(infile.Get(name.replace(mainzone,sideband)))
	h.Add(infile.Get(name.replace(mainzone,tightzone)))	
	if h.Integral()>0: 
		h.Scale(1.0/h.Integral())
	h.SetTitle(name.replace(mainzone,''))
	histoStyler(h, colors[len(hlist)%len(colors)])
	h.GetYaxis().SetRangeUser(0.0001,10)
	h.GetXaxis().SetRangeUser(0,5)
	hlist.append(h)
	
#hlist.reverse()
href = hlist[0].Clone('href')
href.SetLineColor(kBlack)
href.SetMarkerColor(kBlack)
href.SetTitle('reference')
href.Reset()
hratio, pad1, pad2 = FabDraw(c1,leg,href,[href],datamc='data',lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
hratio.GetYaxis().SetRangeUser(-0.1,2.6)	

pad1.cd()
leg = mklegend(x1=.68, y1=.4, x2=.94, y2=.88, color=kWhite)
arg = 'hist e'
for h in hlist:
	h.Draw(arg)
	leg.AddEntry(h, h.GetTitle().split('_')[0])
	arg = 'hist e0 same'
	h.Draw(arg)
	arg = 'hist e same'
leg.Draw()

href = hlist[0].Clone('href')
href.SetLineColor(kBlack)
href.SetMarkerColor(kBlack)
pad2.cd()
ratlist = []
arg = 'hist'

for h in hlist:
	h.GetXaxis().SetTitle('de/dx')
	hratio = h.Clone(h.GetName()+'_ratio')
	histoStyler(hratio,hratio.GetLineColor())
	hratio.Divide(href)
	hratio.GetXaxis().SetTitleSize(0.05)
	hratio.GetXaxis().SetLabelSize(0.05)	
	hratio.GetYaxis().SetRangeUser(0,2)
	hratio.Draw(arg)
	arg = 'hist same'
	ratlist.append(hratio)
	
	
c1.Update()

pause()

c1.Write()

	
import os, sys
print 'test b'
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
print 'test c'



