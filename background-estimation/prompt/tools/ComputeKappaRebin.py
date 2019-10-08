from ROOT import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from namelib import *
import sys
from random import shuffle
gROOT.SetBatch(1)

dofit = True
if dofit: funcs = {}

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
print file.GetName()

keys = file.GetListOfKeys()

c1 = mkcanvas('c1')
#c1.SetLogy()
#c1.SetLogx()
fnew = TFile(foname,'recreate')
fnew.cd()

for key in keys:
	name = key.GetName()
	if not 'ProbePtDT_eta' in name: continue
	if 'FromTau' in name: continue
	hnum   = file.Get(name).Clone('hnum')
	if not 'Gen' in name:
	  if 'Pi' in name: 
	  	print 'subtracting stuff'
		print 'integral before', hnum.Integral()
		hnum.Draw('hist')
		n2sub = name.replace('Pi','ElFromTau').replace('DT','RECO').replace('num','den').replace('Pt','PtWtd')
		h1tosubtract = file.Get(n2sub)
		h1tosubtract.SetLineColor(kGreen+1)
		h1tosubtract.Draw('same hist')
		hnum.SetLineColor(kBlue)
		print 'integral after', hnum.Integral()
		n2sub = name.replace('Pi','MuFromTau').replace('DT','RECO').replace('num','den').replace('Pt','PtWtd')
		h2tosubtract = file.Get(n2sub)
		#h2tosubtract.SetLineColor(kViolet+1)
		#h2tosubtract.Draw('same')
		#c1.Update()
		#pause()

		n2sub = name.replace('Pi','FakeFromTau').replace('DT','CR').replace('num','den').replace('Pt','PtWtd')
		print 'now subtracting', n2sub, 'from', name
		h3tosubtract = file.Get(n2sub)
		h3tosubtract.SetLineColor(kBlue+1)
		h3tosubtract.Draw('same hist')
		
		fnew.cd()
		h1tosubtract.Write()
		h2tosubtract.Write()
		h3tosubtract.Write()				
		hnum.Add(h1tosubtract,-1)
		hnum.Add(h2tosubtract,-1)
		hnum.Add(h3tosubtract,-1)		
	hden    = file.Get(name.replace('_num','_den').replace('DT','RECO'))	
	if 'Gen' in name: hnum.SetLineColor(kAzure)
	else: hnum.SetLineColor(kViolet)
	if 'Run' in fname: 
		hnum.SetLineColor(kBlack)
		hnum.SetMarkerStyle(20)
		hnum.SetMarkerSize(.85*hnum.GetMarkerSize())
	ratname = name.replace('_num','').replace('DT','Kappa')

	xax = hnum.GetXaxis()
	newbinedges = list(PtBinEdges)
	binNumbers2remove = []
	for ibin in range(2, xax.GetNbins()+1):##just added+1
		if hnum.GetBinContent(ibin)<1 or hden.GetBinContent(ibin)<1 or hnum.GetBinContent(ibin-1)<1 or hden.GetBinContent(ibin-1)<1:
			binNumbers2remove.append(ibin)
	binNumbers2remove.reverse()
	for binNumber in binNumbers2remove:
		del newbinedges[binNumber-1]
	if len(newbinedges)>=2: 
		print 'old bins', PtBinEdges
		print 'new bins', newbinedges
		nbins = len(newbinedges)-1
		newxs = array('d',newbinedges)
		hnum = hnum.Rebin(nbins,'',newxs)
		hden = hden.Rebin(nbins,'',newxs)
	
	#hnumend = hnum.Clone()
	#hnumend.SetLineColor(kGreen)
	#hnumend.Draw('same')
	#c1.Update()
	#pause()
	hratio = hnum.Clone(ratname)
	hratio.Divide(hden)


	hratio.SetTitle('')
	hratio.GetXaxis().SetTitle('p_{T}[GeV]')
	hratio.GetYaxis().SetTitle('#kappa = n(DT)/n(reco-lep)')    
	hratio.GetYaxis().SetLabelSize(0.05)
	hratio.GetXaxis().SetLabelSize(0.05)    
	hratio.GetYaxis().SetTitleOffset(1.25)
	hratio.Draw()

	#funcs['f1'+ratname] = TF1('f1'+ratname,'0.1*[0] + 0.1*[1]/(pow(x,0.5)) + 0.1*[5]/(pow(x,1)) + 0.1*[2]/pow(x,2) + [3]*exp(-[4]*x)',5,350)
	if nbins>60: 
		#funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0] * (0.001*[1]/(pow(x,1)) + exp(-[2]*x))',30,3500)
		funcs['f1'+ratname] = TF1('f1'+ratname,'expo(6)',0,350)
	if nbins>50: 
		#funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0] * (0.001*[1]/(pow(x,1)) + exp(-[2]*x))',30,3500)
		funcs['f1'+ratname] = TF1('f1'+ratname,'expo(5)',0,350)		
	if nbins>40: 
		#funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0] * (0.001*[1]/(pow(x,1)) + exp(-[2]*x))',30,3500)
		funcs['f1'+ratname] = TF1('f1'+ratname,'expo(4)',0,350)
	elif nbins>50: 
		#funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0] * (0.001*[1]/(pow(x,1)) + exp(-[2]*x))',30,3500)
		#funcs['f1'+ratname] = TF1('f1'+ratname,'expo(3)',0,350)
		#funcs['f1'+ratname] = TF1('f1'+ratname,'0.0001*[0]*exp([1]*x+[2]*x*x+[3]*x*x*x)',5,350)
		funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0]*exp([1]*(x-10)+[2]*(x-10)*(x-10)+[3]*(x-10)*(x-10)*(x-10))',5,2500)
		#funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0]*exp([1]*(x-10)+[2]*(x-10)*(x-10))',5,350)
	elif nbins>40: 
		funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0]*exp([1]*(x-10)+[2]*(x-10)*(x-10))',5,2500)
		#funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0]*TMath::Landau((x-10),[1],[2])',5,350)		
	elif nbins>40: 
		funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0]*exp([1]*(x-10)+[2]*(x-10))',5,2500)
	elif nbins>2: 
		#funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0] * (exp(-[1]*x))',30,3500)
		funcs['f1'+ratname] = TF1('f1'+ratname,'0.001*[0]*exp([1]*(x-10))',5,2500)
	else: 
		#funcs['f1'+ratname] = TF1('f1'+ratname,'1.0e-06*[0]',30,3500)
		funcs['f1'+ratname] = TF1('f1'+ratname,'[0]*1',5,350)
	funcs['f1'+ratname].SetParLimits(0,0, 9999)
	#funcs['f1'+ratname].SetParLimits(2,0, 9999)
	print 'nbins', nbins, ratname
	hratio.Fit('f1'+ratname,'','EMRSN',15,200)###this is questionable
	funcs['f1'+ratname].SetLineColor(hratio.GetLineColor())	

	leg = mklegend(x1=.22, y1=.66, x2=.79, y2=.82)
	legname = ratname.split('_')[-1].replace('eta','eta ')
	if 'Gen' in name: legname+=' (W+Jets MC, 2016 geom)'
	leg.AddEntry(hratio,legname)
	leg.Draw()
	c1.Update()
	print name
	#pause()	
	fnew.cd()
	#sratio = TSpline3(hratio,'',5,350).Clone(hratio.GetName()+'_s')
	hratio.Write(hratio.GetName().replace('.','p'))
	#sratio.Write((hratio.GetName()+'_s').replace('.','p'))
	c1.Write('c_'+hratio.GetName().replace('.','p'))
	#hratio.Write()
#	funcs['f1'+ratname].Write()
	funcs['f1'+ratname].SetLineColor(hratio.GetLineColor())
	funcs['f1'+ratname].Write('f1'+ratname.replace('.','p'))
	#if not 'Gen' in name:
	#  if 'Pi' in name: 
	#    c1.Update()
	#    pause()

print 'just made', fnew.GetName()
fnew.Close()
exit(0)