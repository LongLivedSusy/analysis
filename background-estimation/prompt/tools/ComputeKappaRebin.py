from ROOT import *
from utils import *
from namelib import *
import sys
from random import shuffle
gROOT.SetBatch(1)

gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendTextSize(0.026)
try:fname =sys.argv[1]
except:
	fname = 'TagnProbe_DYJetsToLL.root'
	print 'Histogram file not specified, will run default file:',fname

try:foname =sys.argv[2]
except:
	foname = 'Kappa.root'
	print 'Output file not specified, will create output as: Kappa.root'
file  = TFile(fname)
#file.ls()

keys = file.GetListOfKeys()

c1 = mkcanvas('c1')
c1.SetLogy()
c1.SetLogx()
fnew = TFile(foname,'recreate')
fnew.cd()

for key in keys:
	name = key.GetName()
	if not 'ProbePtDT_eta' in name: continue
	hnum   = file.Get(name).Clone('hnum')
	hden    = file.Get(name.replace('_num','_den').replace('DT','RECO'))	
	if 'Gen' in name: hnum.SetLineColor(kAzure)
	else: hnum.SetLineColor(kViolet)
	if 'Run' in fname: 
		hnum.SetLineColor(kBlack)
		hnum.SetMarkerStyle(20)
		hnum.SetMarkerSize(.85*hnum.GetMarkerSize())
	xax = hnum.GetXaxis()
	newbins = list(PtBinEdges)
	binNumbers2remove = []
	for ibin in range(1, xax.GetNbins()+1):
		if hnum.GetBinContent(ibin)==0 or hden.GetBinContent(ibin)==0:
			binNumbers2remove.append(ibin)
	binNumbers2remove.reverse()
	for binNumber in binNumbers2remove:
		del newbins[binNumber-1]
		#a = 1
		#del newbins[binNumber]		
	
	if len(newbins)>=2: 
		print 'old bins', PtBinEdges
		print 'new bins', newbins
		nbins = len(newbins)-1
		newxs = array('d',newbins)
		hnum = hnum.Rebin(nbins,'',newxs)
		hden = hden.Rebin(nbins,'',newxs)
		#hnum.Draw()
		#c1.Update()
		#pause()
	#print 'before and after are'
	#hnum.Draw('hist e')
	#file.Get(name).Draw('same l')
	ratname = name.replace('_num','').replace('DT','Kappa')
	print 'ratname', ratname
	
	hratio = hnum.Clone(ratname)
	hratio.Divide(hden)


	hratio.SetTitle('')
	hratio.GetXaxis().SetTitle('p_{T}[GeV]')
	hratio.GetYaxis().SetTitle('#kappa = n(DT)/n(reco-lep)')    
	hratio.GetYaxis().SetLabelSize(0.05)
	hratio.GetXaxis().SetLabelSize(0.05)    
	hratio.GetYaxis().SetTitleOffset(1.25)
	hratio.Draw()

	leg = mklegend(x1=.22, y1=.66, x2=.79, y2=.82)
	legname = ratname.split('_')[-1].replace('eta','eta ')
	if 'Gen' in name: legname+=' (W+Jets MC, 2016 geom)'
	leg.AddEntry(hratio,legname)
	leg.Draw()
	c1.Update()
	print name
	#pause()	
	fnew.cd()
	hratio.Write(hratio.GetName())
	c1.Write('c_'+hratio.GetName())
	#hratio.Write()


print 'just made', fnew.GetName()
fnew.Close()
exit(0)