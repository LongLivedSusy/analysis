from ROOT import *
from utils import *
gStyle.SetOptStat(0)
gROOT.SetBatch(1)

drawttbar = True
Season = 'Fall17'
Season = 'Summer16'
#files = [TFile('RawKappaMaps/RawKapps_'+Season+'.DYJets_PixAndStrips_YesZSmear.root'),TFile('RawKappaMaps/RawKapps_'+Season+'.DYJets_PixOnly_YesZSmear.root')]#,TFile('RawKappaMaps/RawKapps_'+Season+'.DYJets_PixAndStrips_YesZSmear.root')]#, TFile('RawKappaMaps/RawKapps_Run2016_PixOnly.root')]
files = [TFile('RawKappaMaps/RawKapps_Run2016_PixAndStrips_YesZSmear.root'),TFile('RawKappaMaps/RawKapps_Run2016_PixOnly_YesZSmear.root'),TFile('RawKappaMaps/RawKapps_Run2016_PixAndStrips_NoZSmear.root'),TFile('RawKappaMaps/RawKapps_Run2016_PixOnly_NoZSmear.root')]

labels = {}
files[0].ls()

c1 = mkcanvas('c1')
#c1.SetLogy()

newkeys = files[0].GetListOfKeys()
for file in files:
  file.ls()
  lilbit = file.GetName().split('RawKapps_')[1].replace('.root','')
  fnew = TFile('InvMass'+lilbit+'.root','recreate')
  for key_ in newkeys:
	key = key_.GetName()
	if not ('hInvMass' in key): continue
	if not ('_RECOden' in key): continue
	if 'eta1.4442to1.566' in key: continue
	if 'ElFromTau' in key: continue
	if 'MuFromTau' in key: continue	
	etarange, ptrange = key.split('_')[1], key.split('_')[2]
	leg = mklegend(x1=.12, y1=.54, x2=.59, y2=.68, color=kWhite)
	print 'getting', key
	shortbit = file.GetName().split('_')[1].replace('.root','').replace('Run ','Run')
	#hGood.Rebin()
	#hdens = []
	hGood = file.Get(key)	
	#hdens.append(hGood)
	print 'trying to get ',key.replace('_RECOden','_DTnum'), 'from', file.GetName()
	hnum = file.Get(key.replace('_RECOden','_DTnum'))
	#hnum.Rebin()	
	if 'El' in key: 
		hGood.SetFillColor(kTeal)		
		hnum.SetMarkerColor(kGreen+3)
		hnum.SetLineColor(kGreen+3)		
		lepname = '#e'
		hGood.SetTitle('DY Z#rightarrow ee')
	if 'Mu' in key: 
		lepname = '#mu'		
		hGood.SetFillColor(kViolet)
		hnum.SetMarkerColor(kMagenta+3)
		hnum.SetLineColor(kMagenta+3)		
	if 'Pi' in key: 
		lepname = '#pi'		
		hGood.SetFillColor(kOrange+1)
		hnum.SetMarkerColor(kOrange+2)
		hnum.SetLineColor(kOrange+2)
		helfromtau = file.Get(key.replace('Pi','ElFromTauWtd').replace('DT','RECO').replace('num','den'))
		helfromtau.SetLineColor(kGreen+1)
		#helfromtau.SetFillColor(kGreen+1)		
		hmufromtau = file.Get(key.replace('Pi','MuFromTauWtd').replace('DT','RECO').replace('num','den'))
		helfromtau.SetLineColor(kGreen+1)
		hmufromtau.SetFillColor(kViolet)				
		#hdens.append(helfromtau)
		#hdens.append(hmufromtau)		
	hGood.SetTitle(shortbit+ ' Tag + smeared '+lepname)		
	hGood.SetLineColor(kGray+2)
	hnum.SetTitle(shortbit+ ' Tag + dis. trk')
	hGood.SetFillStyle(1001)
	
	integralGood = hGood.Integral(-1,9999)
	integralDT = hnum.Integral(-1,9999)	
	if integralGood>0: hGood.Scale(1.0/integralGood)
	if integralDT>0: hnum.Scale(1.0/integralDT)
	hGood.GetYaxis().SetRangeUser(0.0001+0.1*min(hGood.GetMinimum(0.001),hnum.GetMinimum(0.001)), 0.0002+200*max(hGood.GetMaximum(), hnum.GetMaximum()))
	
	hratio = FabDraw(c1,leg,hnum,[hGood],datamc='Data',lumi='', title = '', LinearScale=False, fractionthing='(mc-data)/data')
	
	if 'Pi' in key: 
		c1.cd(1)
		if integralDT>0:
			helfromtau.Scale(1.0/integralDT)
			hmufromtau.Scale(1.0/integralDT)
		elif integralGood>0:
			helfromtau.Scale(1.0/integralGood)
			hmufromtau.Scale(1.0/integralGood)			
		helfromtau.Draw('same')	
		hmufromtau.Draw('same')	
							
		
	hnum.GetYaxis().SetRangeUser(0.0001+0.1*min(hGood.GetMinimum(0.001),hnum.GetMinimum(0.001)), 0.0002+2*max(hGood.GetMaximum(), hnum.GetMaximum()))
	hratio.GetYaxis().SetRangeUser(0.001,4.99)
	hratio.GetXaxis().SetTitle('m(tag, probe) [GeV]')
	range = (etarange+' '+ptrange).replace('to','-').replace('eta', '|eta|=').replace('pt', 'p_{T}=')
	tl.DrawLatex(0.6,0.7,range)
	if 'AllMC' in file.GetName():
		fCompanion = TFile(file.GetName().replace('AllMC','TTJets'))
		hCompanion = fCompanion.Get(key.replace('_RECOden','_DTnum'))
		hCompanion.SetLineColor(kOrange)
		hCompanion.SetMarkerColor(kOrange)
		hCompanion.SetMarkerStyle(hnum.GetMarkerStyle())		
		#hCompanion.SetFillStyle(1001)
		if integralDT>0: hCompanion.Scale(1.0/integralDT)
		hCompanion.Draw('same')
		leg.AddEntry(hCompanion,'t#bar{t} MC','p')
		print 'yep we just added ttjets stuff'
		
	c1.Update()
	#pause()	
	fnew.cd()
	c1.Write(shortbit.replace(' ','').replace('.','p')+key.replace('.','p'))
	print 'making pdf associated with', file	
	c1.Print(('pdfs/tagandprobe/'+lilbit+key.replace('_RECOden','')).replace('.','p')+'.pdf')
  print 'just created', fnew.GetName()
  fnew.Close()
exit(0)