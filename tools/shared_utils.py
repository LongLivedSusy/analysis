#import pdb; pdb.set_trace()
from ROOT import *
from array import array
import collections

dedxcutLow = 2.1
dedxcutMid = 4.0

dedxcutLow = 2.0
dedxcutMid = 4.0

#dedxcutLow = 3.4
#dedxcutMid = 6

#PtBinEdges = [0,20, 30,40, 50, 60, 90, 120, 180, 250, 350, 400,500,600,700]
PtBinEdges = [0,20,24,27,30,31,32,34,36,38,40,45,50,60,90,120,180,250]#best
#PtBinEdges = [32,250]#for inv. mass plots
EtaBinEdges = [0, 2.4]#best

PtBinEdgesForSmearing = [0,20, 30,40, 50, 70, 90, 120, 200, 300, 310]
EtaBinEdgesForSmearing = [0,1.4442,1.566,2.4]



tl = TLatex()
tl.SetNDC()
cmsTextFont = 61
extraTextFont = 50
lumiTextSize = 0.6
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffset = 0.1
regularfont = 42
originalfont = tl.GetTextFont()
epsi = "#scale[1.3]{#font[122]{e}}"
epsilon = 0.0001

#ptbins = [(15, 30), (30,60), (60,90),(90,9999)]
#etabins = [(0,1.1), (1.1,2.5)]

#ptbins = [(15, 9999)]
#etabins = [(0, 2.5)]


binning = {}
#binning['Met']=[0,20,50,100,150,250,400,650,800,900,1000]
binning['Met']=[400,0,1200]
binning['Mht']=binning['Met']
#binning['TrkPt']=[15,30,50,100,300]
#binning['TrkPt']=[15,30,50,70,90,120,200,300,400,410]#good for gen check, and two eta bins
#binning['TrkPt']=[15,30,50,70,90,120,200,300,310]
binning['TrkPt']=PtBinEdges#[15, 30, 60, 120, 130]#just seemed to work very well
binning['TrkPt']=[15, 30, 60, 120, 130]#just seemed to work very well######comment out after studies
binning['TrkPt']=[100,0,500]
#binning['TrkEta']=[0,1.4442,1.566,2.4]
binning['TrkEta']=EtaBinEdges
binning['TrkEta']=[30,-3,3]
#binning['TrkEta']=[30,-3,3]###comment out ater studies
binning['TrkLen']=[2, 1, 3]
binning['NJets']=[10,0,10]
binning['NLeptons']=[5,0,5]
binning['NElectrons']=binning['NLeptons']
binning['NMuons']=binning['NLeptons']
binning['NPions']=binning['NLeptons']
binning['MuPt']=[60,0,600]
binning['ElPt']=[60,0,600]
binning['ElEta']=[30,-3,3]###comment out ater studies
binning['MuEta']=[30,-3,3]###comment out ater studies
binning['TrkEta']=[30,-3,3]###comment out ater studies
binning['NTags']=[3,0,3]
binning['NPix']=binning['NTags']
binning['NPixStrips']=binning['NTags']
binning['BTags']=[4,0,4]
binning['Ht']=[40,0,2000]
binning['MinDPhiMhtJets'] = [16,0,3.2]
binning['DPhiMhtDt'] = [32,0,3.2]
binning['InvMass'] = [20,60,180]
binning['LepMT'] = [20,0,160]
binning['Track1MassFromDedx'] = [25,0,1000]
binning['BinNumber'] = [58,0,58]
binning['Log10DedxMass'] = [10,0,5]
binning['DeDxAverage'] = [100,0,10]
binning['MinDPhiMhtHemJet'] = [16,0,3.2]
binning['MatchedCalo'] = [30,0,150]
binning['LeadTrkMva'] = [44,-1.1,1.1]
binning['DtStatus'] = [6,-3,3]

binningAnalysis = {}
for key in binning: binningAnalysis[key] = binning[key]

binningAnalysis['Met']=[35,0,700]
binningAnalysis['Mht']=binningAnalysis['Met']
binningAnalysis['BinNumber'] = [51,1,52]
binningAnalysis['DeDxAverage'] = [0,dedxcutLow,0.5*(dedxcutMid+dedxcutLow),dedxcutMid,6.0]
#binningAnalysis['InvMass'] = [25,0,200]
binningAnalysis['LepMT'] = [16,0,160]
binningAnalysis['DPhiMhtDt'] = [32,0,3.2]

'''
binningAnalysis['TrkPt']=PtBinEdges#[15, 30, 60, 120, 130]#just seemed to work very well
binningAnalysis['TrkEta']=EtaBinEdges
binningAnalysis['TrkLen']=[2, 1, 3]
binningAnalysis['NJets']=[1,2,6,8]
binningAnalysis['NLeptons']=[3,0,3]
binningAnalysis['NElectrons']=binningAnalysis['NLeptons']
binningAnalysis['NMuons']=binningAnalysis['NLeptons']
binningAnalysis['NPions']=binningAnalysis['NLeptons']
binningAnalysis['NTags']=[3,0,3]
binningAnalysis['NPix']=binningAnalysis['NTags']
binningAnalysis['NPixStrips']=binningAnalysis['NTags']
binningAnalysis['BTags']=[4,0,4]
binningAnalysis['Ht']=[10,0,2000]
binningAnalysis['MinDPhiMhtJets'] = [16,0,3.2]
binningAnalysis['DeDxAverage'] = [20,0,10]
binningAnalysis['Track1MassFromDedx'] = [25,0,1000]
binningAnalysis['BinNumber'] = [50,1,51]
binningAnalysis['Log10DedxMass'] = [10,0,5]
'''

def histoStyler(h,color=kBlack):
	h.SetLineWidth(2)
	h.SetLineColor(color)
	h.SetMarkerColor(color)
	#h.SetFillColor(color)
	size = 0.059 #.059
	font = 132
	h.GetXaxis().SetLabelFont(font)
	h.GetYaxis().SetLabelFont(font)
	h.GetXaxis().SetTitleFont(font)
	h.GetYaxis().SetTitleFont(font)
	h.GetYaxis().SetTitleSize(size)
	h.GetXaxis().SetTitleSize(size)
	h.GetXaxis().SetLabelSize(size)   
	h.GetYaxis().SetLabelSize(size)
	h.GetXaxis().SetTitleOffset(1.0)
	h.GetYaxis().SetTitleOffset(1.05)
	if not h.GetSumw2N(): h.Sumw2()

def makeHist(name, title, nb, low, high, color):
	h = TH1F(name,title,nb,low,high)
	histoStyler(h,color)
	return h

def makeTh1(name, title, nbins, low, high, color=kBlack): 
	h = TH1F(name, title, nbins, low, high)
	histoStyler(h, color)
	return h


def makeTh1VB(name, title, nbins, arrayOfBins): 
	h = TH1F(name, title, nbins, np.asarray(arrayOfBins, 'd'))
	histoStyler(h, 1)
	return h

def makeTh2(name, title, nbinsx, lowx, highx, nbinsy, lowy, highy): 
	h = TH2F(name, title, nbinsx, lowx, highx, nbinsy, lowy, highy)
	histoStyler(h)
	return h

def makeTh2VB(name, title, nbinsx, arrayOfBinsx, nbinsy, arrayOfBinsy):
	h = TH2F(name, title, nbinsx, np.asarray(arrayOfBinsx, 'd'), nbinsy, np.asarray(arrayOfBinsy, 'd'))
	histoStyler(h)
	return h

def graphStyler(g,color):
	g.SetLineWidth(2)
	g.SetLineColor(color)
	g.SetMarkerColor(color)
	#g.SetFillColor(color)
	size = 0.055
	font = 132
	g.GetXaxis().SetLabelFont(font)
	g.GetYaxis().SetLabelFont(font)
	g.GetXaxis().SetTitleFont(font)
	g.GetYaxis().SetTitleFont(font)
	g.GetYaxis().SetTitleSize(size)
	g.GetXaxis().SetTitleSize(size)
	g.GetXaxis().SetLabelSize(size)   
	g.GetYaxis().SetLabelSize(size)
	g.GetXaxis().SetTitleOffset(1.0)
	g.GetYaxis().SetTitleOffset(1.05)

def mkcanvas(name='c1'):
	c1 = TCanvas(name,name,750,630)
	c1.SetBottomMargin(.16)
	c1.SetLeftMargin(.14)
	#c1.SetTopMargin(.13)
	#c1.SetRightMargin(.04)
	return c1

def mkcanvas_wide(name):
	c1 = TCanvas(name,name,1200,700)
	c1.Divide(2,1)
	c1.GetPad(1).SetBottomMargin(.14)
	c1.GetPad(1).SetLeftMargin(.1)
	c1.GetPad(2).SetBottomMargin(.14)
	c1.GetPad(2).SetLeftMargin(.1)    
	c1.GetPad(1).SetGridx()
	c1.GetPad(1).SetGridy()
	c1.GetPad(2).SetGridx()
	c1.GetPad(2).SetGridy()    
	#c1.SetTopMargin(.13)
	#c1.SetRightMargin(.04)
	return c1

def mklegend(x1=.22, y1=.66, x2=.69, y2=.82, color=kWhite):
	lg = TLegend(x1, y1, x2, y2)
	lg.SetFillColor(color)
	lg.SetTextFont(42)
	lg.SetBorderSize(0)
	lg.SetShadowColor(kWhite)
	lg.SetFillStyle(0)
	return lg

def mklegend_(x1=.22, y1=.66, x2=.69, y2=.82, color=kWhite):
	lg = TLegend(x1, y1, x2, y2)
	lg.SetFillColor(color)
	lg.SetTextFont(42)
	lg.SetBorderSize(0)
	lg.SetShadowColor(kWhite)
	lg.SetFillStyle(0)
	return lg

def fillth1(h,x,weight=1):
	h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon),weight)

def fillth2(h,x,y,weight=1):
	h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon), min(max(y,h.GetYaxis().GetBinLowEdge(1)+epsilon),h.GetYaxis().GetBinLowEdge(h.GetYaxis().GetNbins()+1)-epsilon),weight)

def findbin(thebins, value):
	for bin in thebins:
		if value>=bin[0] and value<=bin[1]:
			return bin
	if value>thebins[-1]: return thebins[-1]
	if value<thebins[0]: return thebins[0]	




selectionsets = {}
inf = 9999
#selectionsets order: HT,MET,NJets,DeltaPhi1,DeltaPhi2
selectionsets['nocuts'] = [(0,inf),(0,inf),(0,inf),(0,inf),(0,inf)]
selectionsets['highmet'] = [(0,inf),(250,inf),(0,inf),(0,inf),(0,inf)]
CutStages = {}
CutStages[1] = 'All tracks'
CutStages[2] = 'pt>15, |eta|<2.4'
CutStages[3] = 'd(xy)<0.02/0.01'#0.02 if pixel-only
CutStages[4] = 'd(z)<0.05'
CutStages[5] = 'Neut. PF sum (#DeltaR<0.05)'
CutStages[6] = 'Ch. PF sum (DeltaR,0.01)'
CutStages[7] = 'PF lepton overlap'
CutStages[8] = 'PF relIso < 0.2'
CutStages[9] = 'PF absIso < 10.0'
CutStages[10] = '#geq2 hits, #geq2 layers'
CutStages[11] = 'NO lost inner hits'
CutStages[12] = '#geq2 lost outer hits'
CutStages[13] = 'pT resolution'
CutStages[14] = 'High purity'


def namewizard(name):
	if 'Mht' == name:
		return r'hard E_{T}^{miss} [GeV]'
	if 'Met' == name:
		return r'E_{T}^{miss} [GeV]'
	if 'Ht' == name:
		return r'H_{T} [GeV]'
	if 'NJets' == name:
		return r'n_{j}'        
	if 'BTags' == name:
		return r'n_{b}'                
	if 'MinDPhiMhtJets' == name:
		return r'#Delta#phi_{min}'                        
	if 'NLeptons' == name:
		return r'n_{l}'
	if 'NMuons' == name:
		return r'n(#mu)'
	if 'NTags' == name:
		return r'n_{DT}'
	if 'SumTagPtOverMet' == name:
		return r'R^{*}'
	if 'DPhiMetSumTags' == name:
		return r'#Delta#phi^{*}'
	if 'InvMass' == name:
		return r'm_{l,track}'
	if 'DeDxAverage' == name:
		return 'de/dx (MeV/cm)'
	if 'TrkPt' == name:
		return r'p_{T} [GeV]'
	if 'TrkEta' == name:
		return '|#eta|'
	if 'MatchedCalo' == name:
		return 'E_{matched}^{calo} [GeV]'
	if 'NPix' == name:
		return 'n(short DT)'
	if 'BinNumber' == name:
		return 'Bin number'
	return name

def mkEfficiencies(hPassList, hAllList):
	gEffList = []
	for i in range(len(hPassList)):
		hPassList[i].Sumw2()
		hAllList[i].Sumw2()
		g = TGraphAsymmErrors(hPassList[i],hAllList[i],'cp')
		FixEfficiency(g,hPassList[i])
		g.SetMarkerSize(3)
		gEffList.append(g)
	return gEffList

def Struct(*args, **kwargs):
	def init(self, *iargs, **ikwargs):
		for k,v in kwargs.items():
			setattr(self, k, v)
		for i in range(len(iargs)):
			setattr(self, args[i], iargs[i])
		for k,v in ikwargs.items():
			setattr(self, k, v)

	name = kwargs.pop("name", "MyStruct")
	kwargs.update(dict((k, None) for k in args))
	return type(name, (object,), {'__init__': init, '__slots__': kwargs.keys()})


def mkHistoStruct(hname, binning=binning):
	if '_' in hname: var = hname[hname.find('_')+1:]
	else: var =  hname
	histoStruct = Struct('Truth','Control','Method1','Method2','Method3')
	if len(binning[var])==3:
		nbins = binning[var][0]
		low = binning[var][1]
		high = binning[var][2]
		histoStruct.Truth = TH1F('h'+hname+'Truth',hname+'Truth',nbins,low,high)
		histoStruct.Control = TH1F('h'+hname+'Control',hname+'Control',nbins,low,high)
		histoStruct.Method1 = TH1F('h'+hname+'Method1',hname+'Method1',nbins,low,high)
		histoStruct.Method2 = TH1F('h'+hname+'Method2',hname+'Method2',nbins,low,high)
		histoStruct.Method3 = TH1F('h'+hname+'Method3',hname+'Method3',nbins,low,high)		

	else:
		nBin = len(binning[var])-1
		binArr = array('d',binning[var])
		histoStruct.Truth = TH1F('h'+hname+'Truth',hname+'Truth',nBin,binArr)
		histoStruct.Control = TH1F('h'+hname+'Control',hname+'Control',nBin,binArr)
		histoStruct.Method1 = TH1F('h'+hname+'Method1',hname+'Method1',nBin,binArr)
		histoStruct.Method2 = TH1F('h'+hname+'Method2',hname+'Method2',nBin,binArr)	
		histoStruct.Method3 = TH1F('h'+hname+'Method3',hname+'Method3',nBin,binArr)				
	histoStyler(histoStruct.Truth,kBlack)
	histoStyler(histoStruct.Control,kTeal-1)
	histoStyler(histoStruct.Method1,kAzure-2)
	histoStyler(histoStruct.Method2,kViolet-2)	
	histoStruct.Method1.SetFillStyle(1001)
	histoStruct.Method1.SetFillColor(histoStruct.Method1.GetLineColor()+1)
	histoStruct.Method2.SetFillStyle(1001)
	histoStruct.Method2.SetFillColor(histoStruct.Method2.GetLineColor()+1)	
	histoStruct.Method3.SetFillStyle(1001)
	histoStruct.Method3.SetFillColor(histoStruct.Method2.GetLineColor()+2)		
	return histoStruct


def writeHistoStruct(hStructDict, opt = 'truthcontrolmethod1method2'):
	keys = sorted(hStructDict.keys())
	for key in keys:
		#print 'writing histogram structure:', key
		if 'truth' in opt: hStructDict[key].Truth.Write()
		if 'control' in opt: hStructDict[key].Control.Write()
		if 'method1' in opt: hStructDict[key].Method1.Write()
		if 'method2' in opt: hStructDict[key].Method2.Write()
		if 'method3' in opt: hStructDict[key].Method3.Write()		
	
def mkEfficiencyRatio(hPassList, hAllList,hName = 'hRatio'):#for weighted MC, you need TEfficiency!
	hEffList = []
	for i in range(len(hPassList)):
		hPassList[i].Sumw2()
		hAllList[i].Sumw2()    
		g = TGraphAsymmErrors(hPassList[i],hAllList[i],'cp')
		print 'RATIO........'
		FixEfficiency(g,hPassList[i])
		hEffList.append(hPassList[i].Clone('hEff'+str(i)))
		hEffList[-1].Divide(hAllList[i])
		cSam1 = TCanvas('cSam1')
		print 'this is the simply divided histogram:'
		hEffList[-1].Draw()
		cSam1.Update()

		print 'now putting in the uncertainties under ratio'
		for ibin in range(1,hEffList[-1].GetXaxis().GetNbins()+1):
			print 'setting errory(ibin)=',ibin,g.GetX()[ibin],g.GetErrorY(ibin)
			print 'compared with histo',ibin,
			hEffList[-1].SetBinError(ibin,1*g.GetErrorY(ibin-1))
			print 'errory(ibin)=',g.GetX()[ibin],g.GetErrorY(ibin-1)
		#histoStyler(hEffList[-1],hPassList[i].GetLineColor())

		cSam2 = TCanvas('cSam2')
		print 'this is the after divided histogram:'
		hEffList[-1].Draw()
		cSam2.Update()


		hEffList[-1].Draw()
	hRatio = hEffList[0].Clone(hName)
	hRatio.Divide(hEffList[1])
	hRatio.GetYaxis().SetRangeUser(0.95,1.05)
	c3 = TCanvas()
	hRatio.Draw()
	c3.Update()
	return hRatio


def pause(str_='push enter key when ready'):
		import sys
		print str_
		sys.stdout.flush() 
		raw_input('')

datamc = 'Data'
def stamp(lumi='35.9', showlumi = False, WorkInProgress = True):
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(0.98*tl.GetTextSize())
	tl.DrawLatex(0.135,0.915, 'CMS')
	tl.SetTextFont(extraTextFont)
	tl.SetTextSize(1.0/0.98*tl.GetTextSize())
	xlab = 0.213
	if WorkInProgress: tl.DrawLatex(xlab,0.915, ' Preliminary')
	else: tl.DrawLatex(xlab,0.915, ('MC' in datamc)*' simulation '+'preliminary')
	tl.SetTextFont(regularfont)
	tl.SetTextSize(0.81*tl.GetTextSize())    
	thingy = ''
	if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
	xthing = 0.6202
	if not showlumi: xthing+=0.13
	tl.DrawLatex(xthing,0.915,thingy)
	tl.SetTextSize(1.0/0.81*tl.GetTextSize())  


def stamp2(lumi,datamc='MC'):
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(1.6*tl.GetTextSize())
	tl.DrawLatex(0.152,0.82, 'CMS')
	tl.SetTextFont(extraTextFont)
	tl.DrawLatex(0.14,0.74, ('MC' in datamc)*' simulation'+' internal')
	tl.SetTextFont(regularfont)
	if lumi=='': tl.DrawLatex(0.62,0.82,'#sqrt{s} = 13 TeV')
	else: tl.DrawLatex(0.47,0.82,'#sqrt{s} = 13 TeV, L = '+str(lumi)+' fb^{-1}')
	#tl.DrawLatex(0.64,0.82,'#sqrt{s} = 13 TeV')#, L = '+str(lumi)+' fb^{-1}')	
	tl.SetTextSize(tl.GetTextSize()/1.6)


#------------------------------------------------------------------------------
def mkcdf(hist, minbin=1):
	hist.Scale(1.0/hist.Integral(1,hist.GetXaxis().GetNbins()))
	c = [0.0]*(hist.GetNbinsX()-minbin+2+1)
	j=1
	for ibin in xrange(minbin, hist.GetNbinsX()+1):
		c[j] = c[j-1] + hist.GetBinContent(ibin)
		j += 1
	c[j] = hist.Integral()
	return c


def calcTrackIso(trk, tracks):
	ptsum =  -trk.pt()
	for track in tracks:
		dR = TMath.Sqrt( (trk.eta()-track.eta())**2 + (trk.phi()-track.phi())**2)
		if dR<0.3: ptsum+=track.pt()
	return ptsum/trk.pt()

def calcTrackJetIso(trk, jets):
	for jet in jets:
		if not jet.pt()>30: continue
		if  TMath.Sqrt( (trk.eta()-jet.eta())**2 + (trk.phi()-jet.phi())**2)<0.5: return False
	return True

def calcMiniIso(trk, tracks):
	pt = trk.pt()
	ptsum = -pt
	if pt<=50: R = 0.2
	elif pt<=200: R = 10.0/pt
	else: R = 0.05
	for track in tracks:
		dR = TMath.Sqrt( (trk.eta()-track.eta())**2 + (trk.phi()-track.phi())**2)
		if dR<R: ptsum+=track.pt()
	return ptsum/trk.pt()

def isMatched2(obj, col, dR=0.02, verbose = False):
	matchedIdx = -1
	bigDR = inf
	for ic, thing in enumerate(col):
		dr = thing.DeltaR(obj)
		if verbose: print 'dr=',dr
		if dr<dR:
			ismatched = True
			return thing
	return False

def isMatched_(obj, col, dR=0.02, verbose = False):
	matchedIdx = -1
	bigDR = inf
	for ic, thing in enumerate(col):
		dr = thing[0].DeltaR(obj[0])
		if verbose: print 'dr=',dr
		if dr<dR:
			ismatched = True
			return thing
	return False

def FabDraw(cGold,leg,hTruth,hComponents,datamc='MC',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
	print 'datamc in FabDraw'
	cGold.cd()
	pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
	pad1.SetBottomMargin(0.0)
	pad1.SetLeftMargin(0.12)
	if not LinearScale:
		pad1.SetLogy()

	pad1.SetGridx()
	#pad1.SetGridy()
	pad1.Draw()
	pad1.cd()
	for ih in range(1,len(hComponents[1:])+1):
		hComponents[ih].Add(hComponents[ih-1])
	hComponents.reverse()        
	if abs(hComponents[0].Integral(-1,999)-1)<0.001:
		hComponents[0].GetYaxis().SetTitle('Normalized')
	else: hComponents[0].GetYaxis().SetTitle('Events/bin')
	cGold.Update()
	hTruth.GetYaxis().SetTitle('Normalized')
	hTruth.GetYaxis().SetTitleOffset(1.15)
	hTruth.SetMarkerStyle(20)
	histheight = 1.5*max(hComponents[0].GetMaximum(),hTruth.GetMaximum())
	if LinearScale: low, high = 0, histheight
	else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hTruth.GetMinimum())), 1000*histheight

	title0 = hTruth.GetTitle()
	if datamc=='MC':
		for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
		leg.AddEntry(hTruth,hTruth.GetTitle(),'lpf')        
	else:
		for ihComp, hComp in enumerate(hComponents):
			leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
		leg.AddEntry(hTruth,title0,'lp')    
	hTruth.SetTitle('')
	hComponents[0].SetTitle('')
	if LinearScale: hComponents[0].GetYaxis().SetRangeUser(0, 1.5*hTruth.GetMaximum())
	else: hComponents[0].GetYaxis().SetRangeUser(0.001, 100*hTruth.GetMaximum())
	hComponents[0].Draw('hist')

	for h in hComponents[1:]: 
		h.Draw('hist same')
		cGold.Update()
		print 'updating stack', h
	hComponents[0].Draw('same') 
	hTruth.Draw('p same')
	hTruth.Draw('e same')    
	cGold.Update()
	hComponents[0].Draw('axis same')           
	leg.Draw()        
	cGold.Update()
	stamp2(lumi,datamc)
	cGold.Update()
	cGold.cd()
	pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
	pad2.SetTopMargin(0.0)
	pad2.SetBottomMargin(0.3)
	pad2.SetLeftMargin(0.12)
	pad2.SetGridx()
	pad2.SetGridy()
	pad2.Draw()
	pad2.cd()
	hTruthCopy = hTruth.Clone('hTruthClone'+hComponents[0].GetName())
	hRatio = hTruthCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
	hRatio.SetMarkerStyle(20)
	#hFracDiff = hComponents[0].Clone('hFracDiff')
	#hFracDiff.SetMarkerStyle(20)
	hTruthCopy.SetMarkerStyle(20)
	hTruthCopy.SetMarkerColor(1) 
	#histoStyler(hFracDiff, 1)
	histoStyler(hTruthCopy, 1)
	#hFracDiff.Add(hTruthCopy,-1)
	#hFracDiff.Divide(hTruthCopy)
	#hRatio.Divide(hTruthCopy)
	hRatio.Divide(hComponents[0])
	hRatio.GetYaxis().SetRangeUser(0.0,.1)###
	hRatio.SetTitle('')
	if 'prediction' in title0: hFracDiff.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
	else: hRatio.GetYaxis().SetTitle(fractionthing)
	hRatio.GetXaxis().SetTitleSize(0.12)
	hRatio.GetXaxis().SetLabelSize(0.11)
	hRatio.GetYaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetLabelSize(0.12)
	hRatio.GetYaxis().SetNdivisions(5)
	hRatio.GetXaxis().SetNdivisions(10)
	hRatio.GetYaxis().SetTitleOffset(0.5)
	hRatio.GetXaxis().SetTitleOffset(1.0)
	hRatio.GetXaxis().SetTitle(hTruth.GetXaxis().GetTitle())
	hRatio.Draw()
	hRatio.Draw('e0')    
	pad1.cd()
	hComponents.reverse()
	hTruth.SetTitle(title0)
	return hRatio, [pad1, pad2]


def FabDrawSystyRatio(cGold,leg,hTruth,hComponents,datamc='MC',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
	cGold.cd()
	pad1 = TPad("pad1", "pad1", 0, 0.45, 1, 1.0)
	pad1.SetBottomMargin(0.0)
	pad1.SetLeftMargin(0.12)
	if not LinearScale:
		pad1.SetLogy()

	#pad1.SetGridx()
	#pad1.SetGridy()
	pad1.Draw()
	pad1.cd()
	for ih in range(1,len(hComponents[1:])+1):
		hComponents[ih].Add(hComponents[ih-1])
	hComponents.reverse()        
	if abs(hComponents[0].Integral(-1,999)-1)<0.001:
		hComponents[0].GetYaxis().SetTitle('Normalized')
	else: hComponents[0].GetYaxis().SetTitle('Events/bin')
	cGold.Update()
	hTruth.GetYaxis().SetTitle('Normalized')
	hTruth.GetYaxis().SetTitleOffset(1.2)
	hTruth.SetMarkerStyle(20)
	histheight = 1.5*max(hComponents[0].GetMaximum(),hTruth.GetMaximum())
	if LinearScale: low, high = 0, histheight
	else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hTruth.GetMinimum())), 1000*histheight

	title0 = hTruth.GetTitle()
	if datamc=='MC':
		for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
		leg.AddEntry(hTruth,hTruth.GetTitle(),'p')        
	else:
		for ihComp, hComp in enumerate(hComponents):
			leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
		leg.AddEntry(hTruth,title0,'p')    
	hTruth.SetTitle('')
	hComponents[0].SetTitle('')	
	xax = hComponents[0].GetXaxis()
	hComponentsUp = hComponents[0].Clone(hComponents[0].GetName()+'UpVariation')
	hComponentsUp.SetLineColor(kWhite)	
	hComponentsDown = hComponents[0].Clone(hComponents[0].GetName()+'DownVariation')	
	hComponentsDown.SetFillColor(10)
	hComponentsDown.SetFillStyle(1001)
	hComponentsDown.SetLineColor(kWhite)
	for ibin in range(1, xax.GetNbins()+1):
		hComponentsUp.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)+hComponents[0].GetBinError(ibin))
		hComponentsDown.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)-hComponents[0].GetBinError(ibin))		

	hComponentsUp.GetYaxis().SetTitleSize(0.11)
	hComponentsUp.GetYaxis().SetTitleOffset(0.5)
	hComponentsUp.GetYaxis().SetLabelSize(0.095)
	#hComponentsUp.Draw('hist')
	hComponents[0].SetLineColor(kGray+1)
	hComponents[0].SetLineWidth(2)
	hComponents[0].Draw('hist e')
	#hComponentsDown.Draw('hist same')
	for h in hComponents[1:]: 
		#h.SetFillStyle(3244)
		print 'there are actually components here!'
		h.Draw('hist same')
	ErrorHistogram = hComponents[0].Clone('ErrorHistogram')
	ErrorHistogram.SetFillStyle(3244)
	ErrorHistogram.SetFillColor(kGray)
	ErrorHistogram.Draw('e2 sames')		
	cGold.Update()
	#hComponents[0].Draw('same') 
	hTruth.Draw('p same')
	hTruth.Draw('e same')    
	cGold.Update()
	hComponents[0].Draw('axis same')           
	leg.Draw()        
	cGold.Update()
	stampFab(lumi,datamc)
	cGold.Update()
	cGold.cd()
	pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.45)
	pad2.SetTopMargin(0.0)
	pad2.SetBottomMargin(0.3)
	pad2.SetLeftMargin(0.12)
	#pad2.SetGridx()
	pad2.SetGridy()
	pad2.Draw()
	pad2.cd()
	hTruthCopy = hTruth.Clone('hTruthClone'+hComponents[0].GetName())
	hRatio = hTruthCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
	hRatio.SetMarkerStyle(20)
	#hFracDiff = hComponents[0].Clone('hFracDiff')
	#hFracDiff.SetMarkerStyle(20)
	hTruthCopy.SetMarkerStyle(20)
	hTruthCopy.SetMarkerColor(1) 
	#histoStyler(hFracDiff, 1)
	histoStyler(hTruthCopy, 1)
	#hFracDiff.Add(hTruthCopy,-1)
	#hFracDiff.Divide(hTruthCopy)
	#hRatio.Divide(hTruthCopy)
	histoByWhichToDivide = hComponents[0].Clone()
	for ibin in range(1, xax.GetNbins()+1): histoByWhichToDivide.SetBinError(ibin, 0)
	hRatio.Divide(histoByWhichToDivide)
	hRatio.GetYaxis().SetRangeUser(0.0,.1)###
	hRatio.SetTitle('')
	if 'prediction' in title0: hFracDiff.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
	else: hRatio.GetYaxis().SetTitle(fractionthing)
	hRatio.GetXaxis().SetTitleSize(0.13)
	hRatio.GetXaxis().SetLabelSize(0.13)
	hRatio.GetYaxis().SetTitleSize(0.13)
	hRatio.GetYaxis().SetLabelSize(0.13)
	hRatio.GetYaxis().SetNdivisions(5)
	hRatio.GetXaxis().SetNdivisions(10)
	hRatio.GetYaxis().SetTitleOffset(0.4)
	hRatio.GetXaxis().SetTitleOffset(1.0)
	hRatio.GetXaxis().SetTitle(hTruth.GetXaxis().GetTitle())
	hRatio.Draw()


	histoMethodFracErrorNom = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystNom')
	histoMethodFracErrorNom.SetLineColor(kBlack)
	histoMethodFracErrorNom.SetFillStyle(1)
	histoMethodFracErrorUp = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystUp')
	histoMethodFracErrorUp.SetFillStyle(3001)
	histoMethodFracErrorUp.SetLineColor(kWhite)	
	histoMethodFracErrorUp.SetFillColor(kGray)#hComponents[0].GetFillColor())	
	histoMethodFracErrorUp.SetFillStyle(3244)
	histoMethodFracErrorDown = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystDown')
	histoMethodFracErrorDown.SetLineColor(kWhite)
	#histoMethodFracErrorDown.SetFillStyle(1001)
	histoMethodFracErrorDown.SetFillColor(10)
	for ibin in range(1, xax.GetNbins()+1): 
		content = histoMethodFracErrorUp.GetBinContent(ibin)
		if content>0: err = histoMethodFracErrorUp.GetBinError(ibin)/content
		else: err = 0
		histoMethodFracErrorUp.SetBinContent(ibin, 1+err)
		histoMethodFracErrorUp.SetBinError(ibin, 0)
		histoMethodFracErrorDown.SetBinContent(ibin, 1-err)
		histoMethodFracErrorDown.SetBinError(ibin, 0)		
		histoMethodFracErrorNom.SetBinContent(ibin, 1)		
		histoMethodFracErrorNom.SetBinError(ibin, 0)
	hRatio.GetYaxis().SetRangeUser(-0.2,2.7)	
	hRatio.Draw('e0')
	histoMethodFracErrorUp.Draw('same hist')	
	histoMethodFracErrorNom.Draw('same')
	histoMethodFracErrorDown.Draw('same hist')
	hRatio.Draw('e0 same')
	hRatio.Draw('axis same')
	pad1.cd()
	hComponents.reverse()
	hTruth.SetTitle(title0)
	pad1.Update()

	return hRatio, [histoMethodFracErrorNom, histoMethodFracErrorUp, histoMethodFracErrorDown, hComponentsUp, hComponentsDown, ErrorHistogram,pad1, pad2]

def stampFab(lumi,datamc='MC'):
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(1.6*tl.GetTextSize())
	tl.DrawLatex(0.152,0.82, 'CMS')
	tl.SetTextFont(extraTextFont)
	tl.DrawLatex(0.14,0.74, ('MC' in datamc)*' simulation'+' internal')
	tl.SetTextFont(regularfont)
	if lumi=='': tl.DrawLatex(0.62,0.82,'#sqrt{s} = 13 TeV')
	else: tl.DrawLatex(0.55,0.82,'L = '+str(lumi)+' fb^{-1} (13 TeV)')
	#tl.DrawLatex(0.64,0.82,'#sqrt{s} = 13 TeV')#, L = '+str(lumi)+' fb^{-1}')	
	tl.SetTextSize(tl.GetTextSize()/1.6)


def stampE(energy):
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(.8*tl.GetTextSize())
	tl.SetTextFont(regularfont)
	tl.DrawLatex(0.68,.91,'#sqrt{s} = 13 TeV')#(L = '+str(lumi)+' '#fb^{-1}')##from Akshansh


import numpy as np
_dxyVtx_ = array('f',[0])
_dzVtx_ = array('f',[0])
_matchedCaloEnergy_ = array('f',[0])
_trkRelIso_ = array('f',[0])
_nValidPixelHits_ = array('f',[0])
_nValidTrackerHits_ = array('f',[0])
_nMissingOuterHits_ = array('f',[0])
_ptErrOverPt2_ = array('f',[0])
_trkRelIsoSTARpt_ = array('f',[0])
_neutralPtSum_ = array('f',[0])
_chargedPtSum_ = array('f',[0])
_pixelLayersWithMeasurement_ = array('f',[0])
_trackerLayersWithMeasurement_ = array('f',[0])
_nMissingMiddleHits_ = array('f',[0])
_chi2perNdof_ = array('f',[0])

def prepareReaderPixelStrips(reader, xmlfilename):
		reader.AddVariable("dzVtx",_dzVtx_)          
		reader.AddVariable("matchedCaloEnergy",_matchedCaloEnergy_)
		reader.AddVariable("trkRelIso",_trkRelIso_)
		reader.AddVariable("nValidPixelHits",_nValidPixelHits_)
		reader.AddVariable("nValidTrackerHits",_nValidTrackerHits_)
		reader.AddVariable("nMissingOuterHits",_nMissingOuterHits_)
		reader.AddVariable("ptErrOverPt2",_ptErrOverPt2_)
		reader.BookMVA("BDT", xmlfilename)

def prepareReaderPixel(reader, xmlfilename):
		reader.AddVariable("dzVtx",_dzVtx_)           
		reader.AddVariable("matchedCaloEnergy",_matchedCaloEnergy_)
		reader.AddVariable("trkRelIso",_trkRelIso_)
		reader.AddVariable("nValidPixelHits",_nValidPixelHits_)
		reader.AddVariable("nValidTrackerHits",_nValidTrackerHits_)
		reader.AddVariable("ptErrOverPt2",_ptErrOverPt2_)
		reader.BookMVA("BDT", xmlfilename)      


def evaluateBDT(reader, trackfv):
		_dxyVtx_[0] = trackfv[0]
		_dzVtx_[0] = trackfv[1]
		_matchedCaloEnergy_[0] = trackfv[2]
		_trkRelIso_[0] = trackfv[3]
		_nValidPixelHits_[0] = trackfv[4]
		_nValidTrackerHits_[0] = trackfv[5]
		_nMissingOuterHits_[0] = trackfv[6]
		_ptErrOverPt2_[0] = trackfv[7]
		_chi2perNdof_[0] = trackfv[8]
		return  reader.EvaluateMVA("BDT")

def prepareReaderPixelStrips_loose(reader, xmlfilename):
		reader.AddVariable("tracks_dzVtx",_dzVtx_)          
		reader.AddVariable("tracks_matchedCaloEnergy",_matchedCaloEnergy_)
		reader.AddVariable("tracks_trkRelIso",_trkRelIso_)
		reader.AddVariable("tracks_nValidPixelHits",_nValidPixelHits_)
		reader.AddVariable("tracks_nValidTrackerHits",_nValidTrackerHits_)
		reader.AddVariable("tracks_nMissingOuterHits",_nMissingOuterHits_)
		reader.AddVariable("tracks_ptErrOverPt2",_ptErrOverPt2_)
		reader.AddVariable("tracks_chi2perNdof",_chi2perNdof_)		
		reader.BookMVA("BDT", xmlfilename)

def prepareReaderPixel_loose(reader, xmlfilename):
		reader.AddVariable("tracks_dzVtx",_dzVtx_)           
		reader.AddVariable("tracks_matchedCaloEnergy",_matchedCaloEnergy_)
		reader.AddVariable("tracks_trkRelIso",_trkRelIso_)
		reader.AddVariable("tracks_nValidPixelHits",_nValidPixelHits_)
		reader.AddVariable("tracks_ptErrOverPt2",_ptErrOverPt2_)
		reader.AddVariable("tracks_chi2perNdof",_chi2perNdof_)
		reader.BookMVA("BDT", xmlfilename)  
		
		
def prepareReaderPixelStrips_fullyinformed(reader, xmlfilename):
		reader.AddVariable("tracks_dxyVtx",_dxyVtx_)
		reader.AddVariable("tracks_dzVtx",_dzVtx_)		       
		reader.AddVariable("tracks_matchedCaloEnergy",_matchedCaloEnergy_)
		reader.AddVariable("tracks_trkRelIso",_trkRelIso_)
		reader.AddVariable("tracks_nValidPixelHits",_nValidPixelHits_)
		reader.AddVariable("tracks_nValidTrackerHits",_nValidTrackerHits_)
		reader.AddVariable("tracks_nMissingOuterHits",_nMissingOuterHits_)
		reader.AddVariable("tracks_ptErrOverPt2",_ptErrOverPt2_)
		reader.AddVariable("tracks_chi2perNdof",_chi2perNdof_)		
		reader.BookMVA("BDT", xmlfilename)

def prepareReaderPixel_fullyinformed(reader, xmlfilename):
		reader.AddVariable("tracks_dxyVtx",_dxyVtx_)
		reader.AddVariable("tracks_dzVtx",_dzVtx_)		        
		reader.AddVariable("tracks_matchedCaloEnergy",_matchedCaloEnergy_)
		reader.AddVariable("tracks_trkRelIso",_trkRelIso_)
		reader.AddVariable("tracks_nValidPixelHits",_nValidPixelHits_)
		reader.AddVariable("tracks_ptErrOverPt2",_ptErrOverPt2_)
		reader.AddVariable("tracks_chi2perNdof",_chi2perNdof_)
		reader.BookMVA("BDT", xmlfilename)        



def isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips, threshes=[.1,.25]):###from Akshansh
		moh_ = c.tracks_nMissingOuterHits[itrack]
		phits = c.tracks_nValidPixelHits[itrack]
		thits = c.tracks_nValidTrackerHits[itrack]
		tlayers = c.tracks_trackerLayersWithMeasurement[itrack]
		pixelOnly = phits>0 and thits==phits
		medium = tlayers< 7 and (thits-phits)>0
		long   = tlayers>=7 and (thits-phits)>0
		pixelStrips = medium or long
		if pixelStrips:
			if not moh_>=2: return 0, -11

		if not (c.tracks_nMissingInnerHits[itrack]==0): return 0, -11
		if not (pixelOnly or pixelStrips): return 0, -11                                                                                                    
		if not c.tracks_passPFCandVeto[itrack]: return 0, -11
		pterr = c.tracks_ptError[itrack]/(track.Pt()*track.Pt())        
		dxyVtx = abs(c.tracks_dxyVtx[itrack])
		dzVtx = abs(c.tracks_dzVtx[itrack])                        
		if not c.tracks_nMissingMiddleHits[itrack]==0: 
			#print 'loss to MMH'
			return 0,-11
		if not (c.tracks_trackQualityHighPurity[itrack]): return 0,-11
		nhits = c.tracks_nValidTrackerHits[itrack]
		nlayers = c.tracks_trackerLayersWithMeasurement[itrack]
		if not (nlayers>=2 and nhits>=2): return 0,-11
		matchedCalo = c.tracks_matchedCaloEnergy[itrack]
		if not c.tracks_chi2perNdof[itrack]<2.88: 
			#print 'loss to chi2'
			return 0,-11
		
		if not dxyVtx < 0.1: return 0,-11
		if not c.tracks_trkRelIso[itrack]<0.01: 
			return 0,-11
		trackfv = [dxyVtx, dzVtx, matchedCalo, c.tracks_trkRelIso[itrack], phits, thits, moh_, pterr]

		if pixelOnly:
				mva_ = evaluateBDT(readerPixelOnly, trackfv)
				if mva_ > (dxyVtx*0.65/0.01-0.5): return 1, mva_      #tightening if not mva_ > dxyVtx*0.5/0.01-0.3: return 0 in any fashion tended to kill the electron and pion, but only with dphileps
				elif dxyVtx>0.04: return -1, mva_
				else: 	
					return 0, mva_
		elif pixelStrips:
				mva_ = evaluateBDT(readerPixelStrips, trackfv) 
				if mva_>(dxyVtx*0.7/0.01-0.05): return 2, mva_# this made the MC "happy": if not (mva_>dxyVtx*0.6/0.01+0.05): return 0					
				elif dxyVtx>0.04: return -2, mva_
				else: 
					return 0, mva_
		else:
				return 0, mva_
				
				
def isDisappearingTrack_Loosetag(track, itrack, c, readerPixelOnly, readerPixelStrips, threshes=[.1,.25]):###from Akshansh
		moh_ = c.tracks_nMissingOuterHits[itrack]
		phits = c.tracks_nValidPixelHits[itrack]
		thits = c.tracks_nValidTrackerHits[itrack]
		tlayers = c.tracks_trackerLayersWithMeasurement[itrack]
		pixelOnly = phits>0 and thits==phits
		medium = tlayers< 7 and (thits-phits)>0
		long   = tlayers>=7 and (thits-phits)>0
		pixelStrips = medium or long
		if pixelStrips:
			if not moh_>=2: return 0, -11

		if not (pixelOnly or pixelStrips): return 0, -11                                                                                                    
		if not c.tracks_passPFCandVeto[itrack]: return 0, -11
		pterr = c.tracks_ptError[itrack]/(track.Pt()*track.Pt())        
		dxyVtx = abs(c.tracks_dxyVtx[itrack])
		dzVtx = abs(c.tracks_dzVtx[itrack])                        
		
		nhits = c.tracks_nValidTrackerHits[itrack]
		nlayers = c.tracks_trackerLayersWithMeasurement[itrack]
		if not (nlayers>=2 and nhits>=2): return 0,-11
		matchedCalo = c.tracks_matchedCaloEnergy[itrack]
		chi2  = c.tracks_chi2perNdof[itrack]
		
		trackfv = [dxyVtx, dzVtx, matchedCalo, c.tracks_trkRelIso[itrack], phits, thits, moh_, pterr,chi2]

		if pixelOnly:
				mva_ = evaluateBDT(readerPixelOnly, trackfv)
				if mva_ > (dxyVtx*0.65/0.01-0.5): return 1, mva_      #tightening if not mva_ > dxyVtx*0.5/0.01-0.3: return 0 in any fashion tended to kill the electron and pion, but only with dphileps
				elif dxyVtx>0.05: return -1, mva_
				else: 	
					return 0, mva_
		elif pixelStrips:
				mva_ = evaluateBDT(readerPixelStrips, trackfv) 
				if mva_>(dxyVtx*0.7/0.01-0.2): return 2, mva_# this made the MC "happy": if not (mva_>dxyVtx*0.6/0.01+0.05): return 0					
				elif dxyVtx>0.05: return -2, mva_
				else: ##17July changed this from -0.05
					return 0, mva_
		else:
				return 0, mva_
				
				
def isDisappearingTrack_FullyInformed(track, itrack, c, readerPixelOnly, readerPixelStrips, threshes=[.1,.25]):###from Akshansh
		moh_ = c.tracks_nMissingOuterHits[itrack]
		phits = c.tracks_nValidPixelHits[itrack]
		thits = c.tracks_nValidTrackerHits[itrack]
		tlayers = c.tracks_trackerLayersWithMeasurement[itrack]
		pixelOnly = phits>0 and thits==phits
		medium = tlayers< 7 and (thits-phits)>0
		long   = tlayers>=7 and (thits-phits)>0
		pixelStrips = medium or long
		if pixelStrips:
			if not moh_>=2: return 0, -11

		if not (pixelOnly or pixelStrips): return 0, -11                                                                                                    
		if not c.tracks_passPFCandVeto[itrack]: return 0, -11
		pterr = c.tracks_ptError[itrack]/(track.Pt()*track.Pt())        
		dxyVtx = abs(c.tracks_dxyVtx[itrack])
		dzVtx = abs(c.tracks_dzVtx[itrack])                        
		
		nhits = c.tracks_nValidTrackerHits[itrack]
		nlayers = c.tracks_trackerLayersWithMeasurement[itrack]
		if not (nlayers>=2 and nhits>=2): return 0,-11
		matchedCalo = c.tracks_matchedCaloEnergy[itrack]
		chi2  = c.tracks_chi2perNdof[itrack]
		
		trackfv = [dxyVtx, dzVtx, matchedCalo, c.tracks_trkRelIso[itrack], phits, thits, moh_, pterr,chi2]
		if pixelOnly:
				mva_ = evaluateBDT(readerPixelOnly, trackfv)
				if mva_ > -0.05: return 1, mva_  
				#elif dxyVtx>0.05: return -1, mva_
				else: return 0, mva_ 
		elif pixelStrips:
				mva_ = evaluateBDT(readerPixelStrips, trackfv) 
				if mva_>-0.05: return 2, mva_
				#elif dxyVtx>0.05: return -2, mva_
				else: return 0, mva_ ##this -2 was nominally 0
		else:
				return 0, mva_								
		
#just changed a couple of lines above to loosen the tag
		
def isBaselineTrack(track, itrack, c, hMask=''):
	if not abs(track.Eta())< 2.4: return False
	if not (abs(track.Eta()) < 1.4442 or abs(track.Eta()) > 1.566): return False
	if not bool(c.tracks_trackQualityHighPurity[itrack]) : return False
	if not (c.tracks_ptError[itrack]/(track.Pt()*track.Pt()) < 10): return False
	if not abs(c.tracks_dxyVtx[itrack]) < 0.1: return False
	if not abs(c.tracks_dzVtx[itrack]) < 0.1 : return False
	if not c.tracks_trkRelIso[itrack] < 0.2: return False
	if not (c.tracks_trackerLayersWithMeasurement[itrack] >= 2 and c.tracks_nValidTrackerHits[itrack] >= 2): return False
	if not c.tracks_nMissingInnerHits[itrack]==0: return False
	if not c.tracks_nMissingMiddleHits[itrack]==0: return False
	if not c.tracks_chi2perNdof[itrack]<2.88: return 0
	if not c.tracks_pixelLayersWithMeasurement[itrack]>2: return 0
	if hMask!='':
		xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
		ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
		if hMask.GetBinContent(ibinx, ibiny)==0: 
			#print 'zeroing out this DT', ibinx, ibiny
			return False
	return True


def isBaselineTrackLoosetag(track, itrack, c, hMask=''):
	base_cuts = abs(track.Eta())<2.4 and \
		bool(c.tracks_trackQualityHighPurity[itrack]) and \
		c.tracks_ptError[itrack]/c.tracks[itrack].Pt()/c.tracks[itrack].Pt()<10 and \
		c.tracks_dzVtx[itrack]<0.1 and \
		c.tracks_trkRelIso[itrack]<0.01 and \
		c.tracks_trackerLayersWithMeasurement[itrack]>=2 and \
		c.tracks_nValidTrackerHits[itrack]>=2 and \
		c.tracks_nMissingInnerHits[itrack]==0 and \
		c.tracks_nValidPixelHits[itrack]>=2 and \
		bool(c.tracks_passPFCandVeto[itrack])
	return base_cuts
		
def overflow(h):
	bin = h.GetNbinsX()+1
	c = h.GetBinContent(bin)
	h.AddBinContent((bin-1),c)

def mkmet(metPt, metPhi):
	met = TLorentzVector()
	met.SetPtEtaPhiE(metPt, 0, metPhi, metPt)
	return met

def passQCDHighMETFilter(t):
	metvec = mkmet(t.MET, t.METPhi)
	for ijet, jet in enumerate(t.Jets):
		if not (jet.Pt() > 200): continue
		if not (t.Jets_muonEnergyFraction[ijet]>0.5):continue 
		if (abs(jet.DeltaPhi(metvec)) > (3.14159 - 0.4)): return False
	return True


def passQCDHighMETFilter2(t):
	if len(t.Jets)>0:
		metvec = TLorentzVector()
		metvec.SetPtEtaPhiE(t.MET, 0, t.METPhi,0)
		if abs(t.Jets[0].DeltaPhi(metvec))>(3.14159-0.4) and t.Jets_neutralEmEnergyFraction[0]<0.03:
			return False
	return True

def passesUniversalSelection(t):
	if not bool(t.JetID): return False
	if not t.NVtx>0: return False
	#print 'made a'
	if not  passQCDHighMETFilter(t): return False
	if not passQCDHighMETFilter2(t): return False
	#print 'made b'    
	#if not t.PFCaloMETRatio<5: return False # turned off now that we use muons
	###if not t.globalSuperTightHalo2016Filter: return False
	#print 'made c'    
	if not t.HBHENoiseFilter: return False    
	if not t.HBHEIsoNoiseFilter: return False
	if not t.eeBadScFilter: return False      
	#print 'made d'    
	if not t.BadChargedCandidateFilter: return False
	if not t.BadPFMuonFilter: return False
	#print 'made e'    
	if not t.CSCTightHaloFilter: return False
	#print 'made f'        
	if not t.EcalDeadCellTriggerPrimitiveFilter: return False      ##I think this one makes a sizeable difference    
	##if not t.ecalBadCalibReducedExtraFilter: return False
	##if not t.ecalBadCalibReducedFilter: return False      
	   
	return True

def passesUniversalSelectionFastSim(t):
	if not bool(t.JetID): return False
	if not t.NVtx>0: return False
	#print 'made a'
	if not  passQCDHighMETFilter(t): return False
	if not passQCDHighMETFilter2(t): return False
	   
	return True



def passesUniversalDataSelection(t):
	if not (bool(t.JetID) and  t.NVtx>0): return False
	if not  passQCDHighMETFilter(t): return False
	if not passQCDHighMETFilter2(t): return False
	if not t.PFCaloMETRatio<5: return False
	if not t.globalSuperTightHalo2016Filter: return False
	if not t.HBHENoiseFilter: return False    
	if not t.HBHEIsoNoiseFilter: return False
	if not t.eeBadScFilter: return False      
	if not t.BadChargedCandidateFilter: return False
	if not t.BadPFMuonFilter: return False
	if not t.CSCTightHaloFilter: return False
	if not t.EcalDeadCellTriggerPrimitiveFilter: return False                         
	return True


binnumbers = collections.OrderedDict()
#varlist_  = ['Ht',   'Mht',     'NJets', 'BTags', 'NTags','NPix','NPixStrips','MinDPhiMhtJets','DeDxAverage',      'NElectrons', 'NMuons', 'InvMass', 'LepMT', 'TrkPt',        'TrkEta',  'MatchedCalo', 'DtStatus', 'DPhiMhtDt',     'LeadTrkMva',    'BinNumber', 'MinDPhiMhtHemJet','Met','Log10DedxMass']
listagain = ['Ht',    'Mht',     'NJets', 'BTags','NTags','NPix','NPixStrips','MinDPhiMhtJets', 'DeDxAverage',      'NElectrons', 'NMuons', 'InvMass', 'LepMT', 'TrkPt',        'TrkEta',  'MatchedCalo', 'DtStatus', 'DPhiMhtDt',     'LeadTrkMva',    'BinNumber', 'MinDPhiMhtHemJet','Met','Log10DedxMass']
binnumbers[((0,inf),    (150,300),(1,3),    (0,0),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (0,0))] = 1
binnumbers[((0,inf),    (150,300),(1,3),    (0,0),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutMid,inf),         (0,0),   (0,0))] = 2
binnumbers[((0,inf),    (150,300),(1,3),    (0,0),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (0,0))] = 3
binnumbers[((0,inf),    (150,300),(1,3),    (0,0),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutMid,inf),         (0,0),   (0,0))] = 4
binnumbers[((0,inf),    (150,300),(4,inf),  (0,0),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (0,0))] = 5
binnumbers[((0,inf),    (150,300),(4,inf),  (0,0),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutMid,inf),         (0,0),   (0,0))] = 6
binnumbers[((0,inf),    (150,300),(4,inf),  (0,0),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (0,0))] = 7
binnumbers[((0,inf),    (150,300),(4,inf),  (0,0),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutMid,inf),         (0,0),   (0,0))] = 8
binnumbers[((0,inf),    (150,300),(1,3),    (1,inf),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutLow,dedxcutMid),(0,0),   (0,0))] = 9
binnumbers[((0,inf),    (150,300),(1,3),    (1,inf),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutMid,inf),       (0,0),   (0,0))] = 10
binnumbers[((0,inf),    (150,300),(1,3),    (1,inf),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutLow,dedxcutMid),(0,0),   (0,0))] = 11
binnumbers[((0,inf),    (150,300),(1,3),    (1,inf),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutMid,inf),       (0,0),   (0,0))] = 12
binnumbers[((0,inf),    (150,300),(4,inf),  (1,inf),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutLow,dedxcutMid),(0,0),   (0,0))] = 13
binnumbers[((0,inf),    (150,300),(4,inf),  (1,inf),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutMid,inf),       (0,0),   (0,0))] = 14
binnumbers[((0,inf),    (150,300),(4,inf),  (1,inf),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutLow,dedxcutMid),(0,0),   (0,0))] = 15
binnumbers[((0,inf),    (150,300),(4,inf),  (1,inf),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutMid,inf),       (0,0),   (0,0))] = 16
binnumbers[((0,inf),    (300,inf),(1,3),    (0,inf),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutLow,dedxcutMid),(0,0),   (0,0))] = 17
binnumbers[((0,inf),    (300,inf),(1,3),    (0,inf),(1,1),  (0,0),(1,1),      (0.0,inf),          (dedxcutMid,inf),       (0,0),   (0,0))] = 18
binnumbers[((0,inf),    (300,inf),(1,3),    (0,inf),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutLow,dedxcutMid),(0,0),   (0,0))] = 19
binnumbers[((0,inf),    (300,inf),(1,3),    (0,inf),(1,1),  (1,1),(0,0),      (0.0,inf),          (dedxcutMid,inf),       (0,0),   (0,0))] = 20
binnumbers[((0,inf),    (300,inf),(4,inf),  (0,inf),  (1,1),  (0,0),(1,1),    (0.0,inf),      (dedxcutLow,dedxcutMid),  (0,0),   (0,0))] = 21
binnumbers[((0,inf),    (300,inf),(4,inf),  (0,inf),  (1,1),  (0,0),(1,1),    (0.0,inf),      (dedxcutMid,inf),         (0,0),   (0,0))] = 22
binnumbers[((0,inf),    (300,inf),(4,inf),  (0,inf),  (1,1),  (1,1),(0,0),    (0.0,inf),      (dedxcutLow,dedxcutMid),  (0,0),   (0,0))] = 23
binnumbers[((0,inf),    (300,inf),(4,inf),  (0,inf),  (1,1),  (1,1),(0,0),    (0.0,inf),      (dedxcutMid,inf),         (0,0),   (0,0))] = 24
#listagain =  ['Ht',  'Mht',    'NJets',  'BTags','NTags','NPix','NPixStrips','MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
binnumbers[((0,inf),   (0,100),   (0,inf),  (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (1,inf))] = 25
binnumbers[((0,inf),   (0,100),   (0,inf),  (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutMid,inf),         (0,0),   (1,inf))] = 26
binnumbers[((0,inf),   (0,100),   (0,inf),  (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (1,inf))] = 27
binnumbers[((0,inf),   (0,100),   (0,inf),  (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutMid,inf),         (0,0),   (1,inf))] = 28
binnumbers[((0,inf),   (0,inf),   (0,inf),  (1,inf),(1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (1,inf))] = 29
binnumbers[((0,inf),   (0,inf),   (0,inf),  (1,inf),(1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutMid,inf),         (0,0),   (1,inf))] = 30
binnumbers[((0,inf),   (0,inf),   (0,inf),  (1,inf),(1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (1,inf))] = 31
binnumbers[((0,inf),   (0,inf),   (0,inf),  (1,inf),(1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutMid,inf),         (0,0),   (1,inf))] = 32
binnumbers[((0,inf),   (100,inf), (0,inf),  (0,inf),(1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (1,inf))] = 33
binnumbers[((0,inf),   (100,inf), (0,inf),  (0,inf),(1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutMid,inf),         (0,0),   (1,inf))] = 34
binnumbers[((0,inf),   (100,inf), (0,inf),  (0,inf),(1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (0,0),   (1,inf))] = 35
binnumbers[((0,inf),   (100,inf), (0,inf),  (0,inf),(1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutMid,inf),         (0,0),   (1,inf))] = 36
#listagain =  ['Ht',  'Mht',    'NJets',  'BTags','NTags','NPix','NPixStrips','MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
binnumbers[((0,inf),   (0,100),   (0,inf),  (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (1,inf), (0,inf))] = 37
binnumbers[((0,inf),   (0,100),   (0,inf),  (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutMid,inf),         (1,inf), (0,inf))] = 38
binnumbers[((0,inf),   (0,100),   (0,inf),  (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (1,inf), (0,inf))] = 39
binnumbers[((0,inf),   (0,100),   (0,inf),  (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutMid,inf),         (1,inf), (0,inf))] = 40
binnumbers[((0,inf),   (0,inf),   (0,inf),  (1,inf),(1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (1,inf), (0,inf))] = 41
binnumbers[((0,inf),   (0,inf),   (0,inf),  (1,inf),(1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutMid,inf),         (1,inf), (0,inf))] = 42
binnumbers[((0,inf),   (0,inf),   (0,inf),  (1,inf),(1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (1,inf), (0,inf))] = 43
binnumbers[((0,inf),   (0,inf),   (0,inf),  (1,inf),(1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutMid,inf),         (1,inf), (0,inf))] = 44
binnumbers[((0,inf),   (100,inf), (0,inf),  (0,inf),(1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (1,inf), (0,inf))] = 45
binnumbers[((0,inf),   (100,inf), (0,inf),  (0,inf),(1,1), (0,0),  (1,1),     (0.0,inf),          (dedxcutMid,inf),         (1,inf), (0,inf))] = 46
binnumbers[((0,inf),   (100,inf), (0,inf),  (0,inf),(1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutLow,dedxcutMid),  (1,inf), (0,inf))] = 47
binnumbers[((0,inf),   (100,inf), (0,inf),  (0,inf),(1,1), (1,1),  (0,0),     (0.0,inf),          (dedxcutMid,inf),         (1,inf), (0,inf))] = 48
#listagain =  ['Ht',  'Mht',      'NJets', 'BTags','NTags','NPix','NPixStrips','MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons',  'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
binnumbers[((0,inf),   (150,inf), (0,inf),  (0,inf),(2,inf),(0,inf),(0,inf),  (0.0,inf),          (dedxcutLow,inf),        (0,0),   (0,0))]   = 49
binnumbers[((0,inf),   (0,inf),   (0,inf),  (0,inf),(2,inf),(0,inf),(0,inf),  (0.0,inf),          (dedxcutLow,inf),        (0,0),   (1,inf))] = 50
binnumbers[((0,inf),   (0,inf),   (0,inf),  (0,inf),(2,inf),(0,inf),(0,inf),  (0.0,inf),          (dedxcutLow,inf),        (1,inf), (0,inf))] = 51


def GetMinDeltaPhiMhtHemJets(jets, mht):
	lowestDPhi = 10
	for jet in jets:
		if not jet.Pt()>30: continue
		if -3.2<jet.Eta() and jet.Eta()<-1.2 and -1.77<jet.Phi() and jet.Phi()<-0.67:
			if abs(jet.DeltaPhi(mht))<lowestDPhi:
				lowestDPhi = abs(jet.DeltaPhi(mht))
	if lowestDPhi<0: return 10
	else: return lowestDPhi


susybypdg = {}
susybypdg[1000021] = 'Glu'
susybypdg[1000006] = 'Stop'
susybypdg[2000006] = 'Stop'
susybypdg[1000005] = 'Sbottom'
susybypdg[2000005] = 'Sbottom'
susybypdg[1000022] = 'Chi1ne'
susybypdg[1000023] = 'Chi2ne'
susybypdg[1000024] = 'Chi1pm'

def merge2dtbins(hist):
	haux1 = TH1F('haux1','haux1',1,0,1)
	haux2 = TH1F('haux2','haux2',1,0,1)
	haux3 = TH1F('haux3','haux3',1,0,1)
	bnxax = hist.GetXaxis()
	haux1.SetBinContent(1, hist.GetBinContent(bnxax.FindBin(49.5)))
	haux1.SetBinError(1, hist.GetBinError(bnxax.FindBin(49.5)))
	haux2.SetBinContent(1, hist.GetBinContent(bnxax.FindBin(50.5)))
	haux2.SetBinError(1, hist.GetBinError(bnxax.FindBin(50.5)))
	haux3.SetBinContent(1, hist.GetBinContent(bnxax.FindBin(51.5)))
	haux3.SetBinError(1, hist.GetBinError(bnxax.FindBin(51.5)))
	haux1.Add(haux2)	
	haux1.Add(haux3)				
	hist.SetBinContent(bnxax.FindBin(49.5), haux1.GetBinContent(1))
	hist.SetBinError(bnxax.FindBin(49.5), haux1.GetBinError(1))
	hist.SetBinContent(bnxax.FindBin(50.5),0)
	hist.SetBinError(bnxax.FindBin(50.5),0)
	hist.SetBinContent(bnxax.FindBin(51.5),0)
	hist.SetBinError(bnxax.FindBin(51.5),0)
	return hist

triggerIndeces = {}
triggerIndeces['MhtMet6pack'] = [124,109,110,111,112,114,115,116]#123
triggerIndeces['SingleMuon'] = [49,50,65]
triggerIndeces['SingleElectron'] = [36,37,39,40]
triggerIndeces['HtTrain'] = [67,68,69,70,73,74,75,81,85,89,92,93,94,96,97,100,103,104,105]



def PassTrig(c,trigname):
	for trigidx in triggerIndeces[trigname]: 
		if c.TriggerPass[trigidx]==1: return True
		#print "Passing trigger %s, index:%s"%(c.TriggerNames[trigidx],trigidx)
	return False

# Pixel dEdx correction factors
# Standard candle : dE/dx from Summer16 FullSim background MC gen-matched muon track at barrel region
# Fit dEdx shape by gaussian to find a peak.
# Correction Factor : Peak of standard candle / Peak of each data to be correctected
DedxCorr_Pixel_barrel = {
	# Run2016
	'Run2016B' : 1.1759157007,
	'Run2016C' : 1.20850798978,
	'Run2016D' : 1.23427599765,
	'Run2016E' : 1.28826839246,
	'Run2016F' : 1.31364557124,
	'Run2016G' : 1.37770046065,
	'Run2016H' : 1.36903038497,

	# Run2017
	'Run2017B' : 1.0,
	'Run2017C' : 1.0,
	'Run2017D' : 1.0,
	'Run2017E' : 1.0,
	'Run2017F' : 1.0,

	# Run2018
	'Run2018A' : 1.0,
	'Run2018B' : 1.0,
	'Run2018C' : 1.0,
	'Run2018D' : 1.0,

	# Summer16 MC
	'Summer16' : 1.0,
	
	# Summer16 Private fastsim signal
	'Summer16FastSim' : 0.630164946858,

	# Fall17 MC
	'Fall17' : 1.0,

	}

DedxCorr_Pixel_endcap = {
	# Run2016
	'Run2016B' : 1.1906198167,
	'Run2016C' : 1.19781783734,
	'Run2016D' : 1.20288995199,
	'Run2016E' : 1.23451267095,
	'Run2016F' : 1.28124951223,
	'Run2016G' : 1.31090072648,
	'Run2016H' : 1.3131533895,

	# Run2017
	'Run2017B' : 1.0,
	'Run2017C' : 1.0,
	'Run2017D' : 1.0,
	'Run2017E' : 1.0,
	'Run2017F' : 1.0,

	# Run2018
	'Run2018A' : 1.0,
	'Run2018B' : 1.0,
	'Run2018C' : 1.0,
	'Run2018D' : 1.0,

	# Summer16 MC
	'Summer16' : 1.0,
	
	# Summer16 Private fastsim signal
	'Summer16FastSim' : 0.630164946858,

	# Fall17 MC
	'Fall17' : 1.0,

	}

'''
#Deprecated correction factor
Dedxcalibdict_Muon_barrel = {
	# Run2016
	'Run2016B' : 1.17636779514,
	'Run2016C' : 1.20891418822,
	'Run2016D' : 1.23273182391,
	'Run2016E' : 1.28736734126,
	'Run2016F' : 1.31353747918,
	'Run2016G' : 1.37715068895,
	'Run2016H' : 1.36878067322,
	# Run2017
	'Run2017B' : 0.963801899609,
	'Run2017C' : 1.20140470672,
	'Run2017D' : 1.19791461654,
	'Run2017E' : 1.05157145077,
	'Run2017F' : 1.13770618643,
	# Run2018
	'Run2018A' : 1.14073449743,
	'Run2018B' : 1.18492683612,
	'Run2018C' : 1.19878707494,
	'Run2018D' : 1.22751598814,
	# Summer16 MC
	'Summer16' : 1.0,
	# Fall17 MC
	'Fall17' : 0.969011079587,
	}

Dedxcalibdict_Muon_endcap = {
	# Run2016
	'Run2016B' : 1.18791104187,
	'Run2016C' : 1.19741550573,
	'Run2016D' : 1.20143536049,
	'Run2016E' : 1.23522243433,
	'Run2016F' : 1.27912918923,
	'Run2016G' : 1.31137102021,
	'Run2016H' : 1.31391843523,
	# Run2017
	'Run2017B' : 1.06222928757,
	'Run2017C' : 1.18481128585,
	'Run2017D' : 1.20570879851,
	'Run2017E' : 1.23734438471,
	'Run2017F' : 1.33529854936,
	# Run2018
	'Run2018A' : 1.22322665702,
	'Run2018B' : 1.27013767105,
	'Run2018C' : 1.2950130203,
	'Run2018D' : 1.26567462258,
	# Summer16 MC
	'Summer16' : 0.954869489523,
	# Fall17 MC
	'Fall17' : 0.949087793289,
	}

Dedxcalibdict_Electron_barrel = {
	# Run2016
	'Run2016B' : 1.17402383132,
	'Run2016C' : 1.20684301222,
	'Run2016D' : 1.23179339234,
	'Run2016E' : 1.28562324175,
	'Run2016F' : 1.31188575138,
	'Run2016G' : 1.3733546783,
	'Run2016H' : 1.36435519035,
	# Run2017
	'Run2017B' : 0.964114469507,
	'Run2017C' : 1.20763025908,
	'Run2017D' : 1.19527561327,
	'Run2017E' : 1.0533676592,
	'Run2017F' : 1.13926942947,
	# Run2018
	'Run2018A' : 1.14433246845,
	'Run2018B' : 1.18837716859,
	'Run2018C' : 1.20391423501,
	'Run2018D' : 1.0,   # not yet
	# Summer16 MC
	'Summer16' : 1.0,
	# Fall17 MC
	'Fall17' : 0.972916363528,
	}

Dedxcalibdict_Electron_endcap = {
	# Run2016
	'Run2016B' : 1.18244438538,
	'Run2016C' : 1.18734689713,
	'Run2016D' : 1.19146464655,
	'Run2016E' : 1.21923754436,
	'Run2016F' : 1.26899666821,
	'Run2016G' : 1.29357275765,
	'Run2016H' : 1.29338476783,
	# Run2017
	'Run2017B' : 1.04700939961,
	'Run2017C' : 1.17904524318,
	'Run2017D' : 1.19531524496,
	'Run2017E' : 1.21618713126,
	'Run2017F' : 1.30235512632,
	# Run2018
	'Run2018A' : 1.22167930566,
	'Run2018B' : 1.26678309764,
	'Run2018C' : 1.29334118935,
	'Run2018D' : 1.0,   # not yet
	# Summer16 MC
	'Summer16' : 0.950670487473,
	# Fall17 MC
	'Fall17' : 0.950210140051,
	}
'''


'''
0 HLT_AK8DiPFJet250_200_TrimMass30_v 0 15
1 HLT_AK8DiPFJet280_200_TrimMass30_v 0 10
2 HLT_AK8DiPFJet300_200_TrimMass30_v -1 1
3 HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v 0 1
4 HLT_AK8PFHT800_TrimMass50_v -1 1
5 HLT_AK8PFHT850_TrimMass50_v -1 1
6 HLT_AK8PFHT900_TrimMass50_v -1 1
7 HLT_AK8PFJet360_TrimMass30_v 0 1
8 HLT_AK8PFJet400_TrimMass30_v -1 1
9 HLT_AK8PFJet420_TrimMass30_v -1 1
10 HLT_AK8PFJet450_v -1 1
11 HLT_AK8PFJet500_v -1 1
12 HLT_AK8PFJet550_v -1 1
13 HLT_CaloJet500_NoJetID_v 0 1
14 HLT_CaloJet550_NoJetID_v -1 1
15 HLT_DiCentralPFJet55_PFMET110_v 0 1
16 HLT_DiPFJet40_DEta3p5_MJJ600_PFMETNoMu140_v 0 1
17 HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v -1 1
18 HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT300_v 0 1
19 HLT_DoubleMu8_Mass8_PFHT300_v 0 1
20 HLT_DoubleMu8_Mass8_PFHT350_v -1 1
21 HLT_Ele105_CaloIdVT_GsfTrkIdT_v 0 1
22 HLT_Ele115_CaloIdVT_GsfTrkIdT_v 0 1
23 HLT_Ele135_CaloIdVT_GsfTrkIdT_v -1 1
24 HLT_Ele145_CaloIdVT_GsfTrkIdT_v -1 1
25 HLT_Ele15_IsoVVVL_PFHT350_PFMET50_v 0 1
26 HLT_Ele15_IsoVVVL_PFHT350_v 0 1
27 HLT_Ele15_IsoVVVL_PFHT400_v -1 1
28 HLT_Ele15_IsoVVVL_PFHT450_CaloBTagCSV_4p5_v -1 1
29 HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v -1 1
30 HLT_Ele15_IsoVVVL_PFHT450_v -1 1
31 HLT_Ele15_IsoVVVL_PFHT600_v 0 1
32 HLT_Ele20_WPLoose_Gsf_v -1 1
33 HLT_Ele20_eta2p1_WPLoose_Gsf_v -1 1
34 HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v 0 1
35 HLT_Ele25_eta2p1_WPTight_Gsf_v 0 1
36 HLT_Ele27_WPTight_Gsf_v 0 1
37 HLT_Ele27_eta2p1_WPLoose_Gsf_v 0 1
38 HLT_Ele28_eta2p1_WPTight_Gsf_HT150_v -1 1
39 HLT_Ele32_WPTight_Gsf_v -1 1
40 HLT_Ele35_WPTight_Gsf_v -1 1
41 HLT_Ele45_WPLoose_Gsf_v 0 1
42 HLT_Ele50_IsoVVVL_PFHT400_v -1 1
43 HLT_Ele50_IsoVVVL_PFHT450_v -1 1
44 HLT_IsoMu16_eta2p1_MET30_v 0 1
45 HLT_IsoMu20_v 0 1
46 HLT_IsoMu22_eta2p1_v -1 1
47 HLT_IsoMu22_v 0 1
48 HLT_IsoMu24_eta2p1_v -1 1
49 HLT_IsoMu24_v 0 1
50 HLT_IsoMu27_v 0 1
51 HLT_IsoTkMu22_v 0 1
52 HLT_IsoTkMu24_v 0 1
53 HLT_Mu15_IsoVVVL_PFHT350_PFMET50_v 0 1
54 HLT_Mu15_IsoVVVL_PFHT350_v 0 1
55 HLT_Mu15_IsoVVVL_PFHT400_v -1 1
56 HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5_v -1 1
57 HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v -1 1
58 HLT_Mu15_IsoVVVL_PFHT450_v -1 1
59 HLT_Mu15_IsoVVVL_PFHT600_v 0 1
60 HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v 0 1
61 HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v 0 1
62 HLT_Mu45_eta2p1_v 0 1
63 HLT_Mu50_IsoVVVL_PFHT400_v -1 1
64 HLT_Mu50_IsoVVVL_PFHT450_v -1 1
65 HLT_Mu50_v 0 1
66 HLT_Mu55_v 0 1
67 HLT_PFHT1050_v -1 1
68 HLT_PFHT180_v -1 1
69 HLT_PFHT200_v 0 1
70 HLT_PFHT250_v 0 1
71 HLT_PFHT300_PFMET100_v 0 1
72 HLT_PFHT300_PFMET110_v 0 1
73 HLT_PFHT300_v 0 512
74 HLT_PFHT350_v 0 256
75 HLT_PFHT370_v -1 1
76 HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2_v -1 1
77 HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2_v -1 1
78 HLT_PFHT380_SixPFJet32_v -1 1
79 HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v 0 1
80 HLT_PFHT400_SixJet30_v 0 2
81 HLT_PFHT400_v 0 128
82 HLT_PFHT430_SixJet40_BTagCSV_p056_v -1 1
83 HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5_v -1 1
84 HLT_PFHT430_SixPFJet40_v -1 1
85 HLT_PFHT430_v -1 1
86 HLT_PFHT450_SixJet40_BTagCSV_p056_v 0 1
87 HLT_PFHT450_SixJet40_v 0 1
88 HLT_PFHT450_SixPFJet40_PFBTagCSV_1p5_v -1 1
89 HLT_PFHT475_v 0 64
90 HLT_PFHT500_PFMET100_PFMHT100_IDTight_v -1 1
91 HLT_PFHT500_PFMET110_PFMHT110_IDTight_v -1 1
92 HLT_PFHT510_v -1 1
93 HLT_PFHT590_v -1 1
94 HLT_PFHT600_v 0 16
95 HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v 0 1
96 HLT_PFHT650_v 0 8
97 HLT_PFHT680_v -1 1
98 HLT_PFHT700_PFMET85_PFMHT85_IDTight_v -1 1
99 HLT_PFHT700_PFMET95_PFMHT95_IDTight_v -1 1
100 HLT_PFHT780_v -1 1
101 HLT_PFHT800_PFMET75_PFMHT75_IDTight_v -1 1
102 HLT_PFHT800_PFMET85_PFMHT85_IDTight_v -1 1
103 HLT_PFHT800_v 0 1
104 HLT_PFHT890_v -1 1
105 HLT_PFHT900_v 0 1
106 HLT_PFJet450_v 0 1
107 HLT_PFJet500_v 0 1
108 HLT_PFJet550_v -1 1
109 HLT_PFMET100_PFMHT100_IDTight_PFHT60_v -1 1
110 HLT_PFMET100_PFMHT100_IDTight_v 0 1
111 HLT_PFMET110_PFMHT110_IDTight_PFHT60_v -1 1
112 HLT_PFMET110_PFMHT110_IDTight_v 0 1
113 HLT_PFMET120_PFMHT120_IDTight_HFCleaned_v -1 1
114 HLT_PFMET120_PFMHT120_IDTight_PFHT60_HFCleaned_v -1 1
115 HLT_PFMET120_PFMHT120_IDTight_PFHT60_v -1 1
116 HLT_PFMET120_PFMHT120_IDTight_v 0 1
117 HLT_PFMET130_PFMHT130_IDTight_PFHT60_v -1 1
118 HLT_PFMET130_PFMHT130_IDTight_v -1 1
119 HLT_PFMET140_PFMHT140_IDTight_PFHT60_v -1 1
120 HLT_PFMET140_PFMHT140_IDTight_v -1 1
121 HLT_PFMET500_PFMHT500_IDTight_CalBTagCSV_3p1_v -1 1
122 HLT_PFMET700_PFMHT700_IDTight_CalBTagCSV_3p1_v -1 1
123 HLT_PFMET800_PFMHT800_IDTight_CalBTagCSV_3p1_v -1 1
124 HLT_PFMET90_PFMHT90_IDTight_v 0 1
125 HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60_v -1 1
126 HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v 0 1
127 HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_PFHT60_v -1 1
128 HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v 0 1
129 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_HFCleaned_v -1 1
130 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v -1 1
131 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v 0 1
132 HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_PFHT60_v -1 1
133 HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v -1 1
134 HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_PFHT60_v -1 1
135 HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v -1 1
136 HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v 0 1
137 HLT_Photon135_PFMET100_v 0 1
138 HLT_Photon165_HE10_v 0 1
139 HLT_Photon165_R9Id90_HE10_IsoM_v 0 1
140 HLT_Photon175_v 0 1
141 HLT_Photon200_v -1 1
142 HLT_Photon300_NoHE_v 0 1
143 HLT_Photon90_CaloIdL_PFHT500_v 0 1
144 HLT_Photon90_CaloIdL_PFHT600_v 0 1
145 HLT_Photon90_CaloIdL_PFHT700_v -1 1
146 HLT_TkMu100_v -1 1
147 HLT_TkMu50_v -1 1
0 HLT_AK8DiPFJet250_200_TrimMass30_v 15 0.0
1 HLT_AK8DiPFJet280_200_TrimMass30_v 10 0.0
2 HLT_AK8DiPFJet300_200_TrimMass30_v 1 0.0
3 HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v 1 0.0
4 HLT_AK8PFHT800_TrimMass50_v 1 0.0
5 HLT_AK8PFHT850_TrimMass50_v 1 0.0
6 HLT_AK8PFHT900_TrimMass50_v 1 0.0
7 HLT_AK8PFJet360_TrimMass30_v 1 0.0
8 HLT_AK8PFJet400_TrimMass30_v 1 0.0
9 HLT_AK8PFJet420_TrimMass30_v 1 0.0
10 HLT_AK8PFJet450_v 1 0.0
11 HLT_AK8PFJet500_v 1 0.0
12 HLT_AK8PFJet550_v 1 0.0
13 HLT_CaloJet500_NoJetID_v 1 0.0
14 HLT_CaloJet550_NoJetID_v 1 0.0
15 HLT_DiCentralPFJet55_PFMET110_v 1 0.0
16 HLT_DiPFJet40_DEta3p5_MJJ600_PFMETNoMu140_v 1 0.0
17 HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v 1 0.0
18 HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT300_v 1 0.0
19 HLT_DoubleMu8_Mass8_PFHT300_v 1 0.0
20 HLT_DoubleMu8_Mass8_PFHT350_v 1 0.0
21 HLT_Ele105_CaloIdVT_GsfTrkIdT_v 1 0.0
22 HLT_Ele115_CaloIdVT_GsfTrkIdT_v 1 0.0
23 HLT_Ele135_CaloIdVT_GsfTrkIdT_v 1 0.0
24 HLT_Ele145_CaloIdVT_GsfTrkIdT_v 1 0.0
25 HLT_Ele15_IsoVVVL_PFHT350_PFMET50_v 1 0.0
26 HLT_Ele15_IsoVVVL_PFHT350_v 1 0.0
27 HLT_Ele15_IsoVVVL_PFHT400_v 1 0.0
28 HLT_Ele15_IsoVVVL_PFHT450_CaloBTagCSV_4p5_v 1 0.0
29 HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v 1 0.0
30 HLT_Ele15_IsoVVVL_PFHT450_v 1 0.0
31 HLT_Ele15_IsoVVVL_PFHT600_v 1 0.0
32 HLT_Ele20_WPLoose_Gsf_v 1 0.0
33 HLT_Ele20_eta2p1_WPLoose_Gsf_v 1 0.0
34 HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v 1 0.0
35 HLT_Ele25_eta2p1_WPTight_Gsf_v 1 0.0
36 HLT_Ele27_WPTight_Gsf_v 1 0.0
37 HLT_Ele27_eta2p1_WPLoose_Gsf_v 1 0.0
38 HLT_Ele28_eta2p1_WPTight_Gsf_HT150_v 1 0.0
39 HLT_Ele32_WPTight_Gsf_v 1 0.0
40 HLT_Ele35_WPTight_Gsf_v 1 0.0
41 HLT_Ele45_WPLoose_Gsf_v 1 0.0
42 HLT_Ele50_IsoVVVL_PFHT400_v 1 0.0
43 HLT_Ele50_IsoVVVL_PFHT450_v 1 0.0
44 HLT_IsoMu16_eta2p1_MET30_v 1 0.0
45 HLT_IsoMu20_v 1 0.0
46 HLT_IsoMu22_eta2p1_v 1 0.0
47 HLT_IsoMu22_v 1 0.0
48 HLT_IsoMu24_eta2p1_v 1 0.0
49 HLT_IsoMu24_v 1 0.0
50 HLT_IsoMu27_v 1 0.0
51 HLT_IsoTkMu22_v 1 0.0
52 HLT_IsoTkMu24_v 1 0.0
53 HLT_Mu15_IsoVVVL_PFHT350_PFMET50_v 1 0.0
54 HLT_Mu15_IsoVVVL_PFHT350_v 1 0.0
55 HLT_Mu15_IsoVVVL_PFHT400_v 1 0.0
56 HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5_v 1 0.0
57 HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v 1 0.0
58 HLT_Mu15_IsoVVVL_PFHT450_v 1 0.0
59 HLT_Mu15_IsoVVVL_PFHT600_v 1 0.0
60 HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v 1 0.0
61 HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v 1 0.0
62 HLT_Mu45_eta2p1_v 1 0.0
63 HLT_Mu50_IsoVVVL_PFHT400_v 1 0.0
64 HLT_Mu50_IsoVVVL_PFHT450_v 1 0.0
65 HLT_Mu50_v 1 0.0
66 HLT_Mu55_v 1 0.0
67 HLT_PFHT1050_v 1 0.0
68 HLT_PFHT180_v 1 0.0
69 HLT_PFHT200_v 1 0.0
70 HLT_PFHT250_v 1 0.0
71 HLT_PFHT300_PFMET100_v 1 0.0
72 HLT_PFHT300_PFMET110_v 1 0.0
73 HLT_PFHT300_v 512 0.0
74 HLT_PFHT350_v 256 0.0
75 HLT_PFHT370_v 1 0.0
76 HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2_v 1 0.0
77 HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2_v 1 0.0
78 HLT_PFHT380_SixPFJet32_v 1 0.0
79 HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v 1 0.0
80 HLT_PFHT400_SixJet30_v 2 0.0
81 HLT_PFHT400_v 128 0.0
82 HLT_PFHT430_SixJet40_BTagCSV_p056_v 1 0.0
83 HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5_v 1 0.0
84 HLT_PFHT430_SixPFJet40_v 1 0.0
85 HLT_PFHT430_v 1 0.0
86 HLT_PFHT450_SixJet40_BTagCSV_p056_v 1 0.0
87 HLT_PFHT450_SixJet40_v 1 0.0
88 HLT_PFHT450_SixPFJet40_PFBTagCSV_1p5_v 1 0.0
89 HLT_PFHT475_v 64 0.0
90 HLT_PFHT500_PFMET100_PFMHT100_IDTight_v 1 0.0
91 HLT_PFHT500_PFMET110_PFMHT110_IDTight_v 1 0.0
92 HLT_PFHT510_v 1 0.0
93 HLT_PFHT590_v 1 0.0
94 HLT_PFHT600_v 16 0.0
95 HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v 1 0.0
96 HLT_PFHT650_v 8 0.0
97 HLT_PFHT680_v 1 0.0
98 HLT_PFHT700_PFMET85_PFMHT85_IDTight_v 1 0.0
99 HLT_PFHT700_PFMET95_PFMHT95_IDTight_v 1 0.0
100 HLT_PFHT780_v 1 0.0
101 HLT_PFHT800_PFMET75_PFMHT75_IDTight_v 1 0.0
102 HLT_PFHT800_PFMET85_PFMHT85_IDTight_v 1 0.0
103 HLT_PFHT800_v 1 0.0
104 HLT_PFHT890_v 1 0.0
105 HLT_PFHT900_v 1 0.0
106 HLT_PFJet450_v 1 0.0
107 HLT_PFJet500_v 1 0.0
108 HLT_PFJet550_v 1 0.0
109 HLT_PFMET100_PFMHT100_IDTight_PFHT60_v 1 0.0
110 HLT_PFMET100_PFMHT100_IDTight_v 1 0.0
111 HLT_PFMET110_PFMHT110_IDTight_PFHT60_v 1 0.0
112 HLT_PFMET110_PFMHT110_IDTight_v 1 0.0
113 HLT_PFMET120_PFMHT120_IDTight_HFCleaned_v 1 0.0
114 HLT_PFMET120_PFMHT120_IDTight_PFHT60_HFCleaned_v 1 0.0
115 HLT_PFMET120_PFMHT120_IDTight_PFHT60_v 1 0.0
116 HLT_PFMET120_PFMHT120_IDTight_v 1 0.0
117 HLT_PFMET130_PFMHT130_IDTight_PFHT60_v 1 0.0
118 HLT_PFMET130_PFMHT130_IDTight_v 1 0.0
119 HLT_PFMET140_PFMHT140_IDTight_PFHT60_v 1 0.0
120 HLT_PFMET140_PFMHT140_IDTight_v 1 0.0
121 HLT_PFMET500_PFMHT500_IDTight_CalBTagCSV_3p1_v 1 0.0
122 HLT_PFMET700_PFMHT700_IDTight_CalBTagCSV_3p1_v 1 0.0
123 HLT_PFMET800_PFMHT800_IDTight_CalBTagCSV_3p1_v 1 0.0
124 HLT_PFMET90_PFMHT90_IDTight_v 1 0.0
125 HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60_v 1 0.0
126 HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v 1 0.0
127 HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_PFHT60_v 1 0.0
128 HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v 1 0.0
129 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_HFCleaned_v 1 0.0
130 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v 1 0.0
131 HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v 1 0.0
132 HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_PFHT60_v 1 0.0
133 HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v 1 0.0
134 HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_PFHT60_v 1 0.0
135 HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v 1 0.0
136 HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v 1 0.0
137 HLT_Photon135_PFMET100_v 1 0.0
138 HLT_Photon165_HE10_v 1 0.0
139 HLT_Photon165_R9Id90_HE10_IsoM_v 1 0.0
140 HLT_Photon175_v 1 0.0
141 HLT_Photon200_v 1 0.0
142 HLT_Photon300_NoHE_v 1 0.0
143 HLT_Photon90_CaloIdL_PFHT500_v 1 0.0
144 HLT_Photon90_CaloIdL_PFHT600_v 1 0.0
145 HLT_Photon90_CaloIdL_PFHT700_v 1 0.0
146 HLT_TkMu100_v 1 0.0
147 HLT_TkMu50_v 1 0.0

2016: HLT_Ele27_WPTight_Gsf_v* 2017: HLT_Ele32_WPTight* (&& hltEGL1SingleEGOrFilter) 2018: HLT_Ele32_WPTight_Gsf_v*
'''
