from ROOT import *
from array import array

r'''
of the barrel (|eta| < 1.4442). The outer circumferences of the endcaps are obscured by services passing between the barrel and the endcaps, and this area is removed from the fiducial region by excluding the first ring of trigger towers of the endcaps (|eta| > 1.566). The fiducial region terminates at |eta| = 2.5 where the tracker coverage ends.


PtBinEdges = [15, 30, 50, 70, 90, 120, 200, 300, 310]#for Akshansh
EtaBinEdges = [0,1.4442,1.566,2.4]# for Akshansh

PtBinEdges = [20, 30, 60, 120, 200, 220]#try squat little bins
EtaBinEdges = [0,1.4442,1.566,2.4]
'''

#PtBinEdges = [0,20, 30,40, 50, 60, 90, 120, 180, 250, 350, 400,500,600,700]
PtBinEdges = [0,20,24,27,30,31,32,34,36,38,40,45,50,60,90,120,180, 250]#best
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
binning['Met']=[24,0,1200]
binning['Mht']=binning['Met']
#binning['TrkPt']=[15,30,50,100,300]
#binning['TrkPt']=[15,30,50,70,90,120,200,300,400,410]#good for gen check, and two eta bins
#binning['TrkPt']=[15,30,50,70,90,120,200,300,310]
binning['TrkPt']=PtBinEdges#[15, 30, 60, 120, 130]#just seemed to work very well
#binning['TrkEta']=[0,1.4442,1.566,2.4]
binning['TrkEta']=EtaBinEdges
binning['TrkLen']=[2, 1, 3]
binning['NJets']=[10,0,10]
binning['NLeptons']=[5,0,5]
binning['NElectrons']=binning['NLeptons']
binning['NMuons']=binning['NLeptons']
binning['NPions']=binning['NLeptons']
binning['NTags']=[3,0,3]
binning['NPix']=binning['NTags']
binning['NPixStrips']=binning['NTags']
binning['BTags']=[4,0,4]
binning['Ht']=[10,0,2000]
binning['MinDPhiMhtJets'] = [16,0,3.2]
binning['DeDxAverage'] = [20,0,10]
binning['Log10DedxMass'] = [10,0,5]
binning['BinNumber'] = [64,0,64]

binningAnalysis = {}
binningAnalysis['Met']=[150,200,250,400,700,900]
binningAnalysis['Mht']=binningAnalysis['Met']
binningAnalysis['TrkPt']=PtBinEdges#[15, 30, 60, 120, 130]#just seemed to work very well
binningAnalysis['TrkEta']=EtaBinEdges
binningAnalysis['TrkLen']=[2, 1, 3]
binningAnalysis['NJets']=[1,2,4,8]
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
binningAnalysis['Log10DedxMass'] = [10,0,5]
binningAnalysis['DeDxAverage'] = [20,0,10]
binningAnalysis['BinNumber'] = [62,1,63]


def histoStyler(h,color=kBlack):
	h.SetLineWidth(2)
	h.SetLineColor(color)
	h.SetMarkerColor(color)
	#h.SetFillColor(color)
	size = 0.059
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
	c1.SetBottomMargin(.15)
	c1.SetLeftMargin(.14)
	#c1.SetTopMargin(.13)
	#c1.SetRightMargin(.04)
	return c1

def mkcanvas_wide(name):
	c1 = TCanvas(name,name,1200,700)
	c1.Divide(2,1)
	c1.GetPad(1).SetBottomMargin(.14)
	c1.GetPad(1).SetLeftMargin(.14)
	c1.GetPad(2).SetBottomMargin(.14)
	c1.GetPad(2).SetLeftMargin(.14)    
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




inf = 9999


def namewizard(name):
	if 'Mht' == name:
		return r'H_{T}^{miss} [GeV]'
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
		return r'n_{#ell}'
	if 'NMuons' == name:
		return r'n(#mu)'
	if 'NTags' == name:
		return r'n_{DT}'
	if 'SumTagPtOverMet' == name:
		return r'R^{*}'
	if 'DPhiMetSumTags' == name:
		return r'#Delta#phi^{*}'
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


def mkHistoStruct(hname):
	if '_' in hname: var = hname[hname.find('_')+1:]
	else: var =  hname
	histoStruct = Struct('Truth','Control','Method')
	if len(binning[var])==3:
		nbins = binning[var][0]
		low = binning[var][1]
		high = binning[var][2]
		histoStruct.Truth = TH1F('h'+hname+'Truth',hname+'Truth',nbins,low,high)
		histoStruct.Control = TH1F('h'+hname+'Control',hname+'Control',nbins,low,high)
		histoStruct.Method = TH1F('h'+hname+'Method',hname+'Method',nbins,low,high)

	else:
		nBin = len(binning[var])-1
		binArr = array('d',binning[var])
		histoStruct.Truth = TH1F('h'+hname+'Truth',hname+'Truth',nBin,binArr)
		histoStruct.Control = TH1F('h'+hname+'Control',hname+'Control',nBin,binArr)
		histoStruct.Method = TH1F('h'+hname+'Method',hname+'Method',nBin,binArr)
	histoStyler(histoStruct.Truth,kBlack)
	histoStyler(histoStruct.Control,kTeal-1)
	histoStyler(histoStruct.Method,kAzure-2)
	histoStruct.Method.SetFillStyle(1001)
	histoStruct.Method.SetFillColor(histoStruct.Method.GetLineColor()+1)
	return histoStruct


def writeHistoStruct(hStructDict):
	for key in hStructDict:
		#print 'writing histogram structure:', key
		hStructDict[key].Truth.Write()
		hStructDict[key].Control.Write()
		hStructDict[key].Method.Write()
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


def stamp2(lumi='35.9', showlumi = False):    
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(0.98*tl.GetTextSize())
	tl.DrawLatex(0.1,0.91, 'CMS')
	tl.SetTextFont(extraTextFont)
	tl.SetTextSize(1.0/0.98*tl.GetTextSize())
	xlab = 0.213
	tl.DrawLatex(xlab,0.91, ('MC' in datamc)*' simulation '+'preliminary')
	tl.SetTextFont(regularfont)
	tl.SetTextSize(0.81*tl.GetTextSize())    
	thingy = ''
	if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
	xthing = 0.6202
	if not showlumi: xthing+=0.13
	tl.DrawLatex(xthing,0.91,thingy)
	tl.SetTextSize(1.0/0.81*tl.GetTextSize()) 




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

def isMatched(obj, col, dR=0.02, verbose = False):
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

def FabDrawSystyRatio(cGold,leg,hTruth,hComponents,datamc='mc',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
	cGold.cd()
	pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
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
	else: hComponents[0].GetYaxis().SetTitle('#Events')
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

	#hComponents[0].Draw('hist')
	hComponentsUp.Draw('hist')
	hComponents[0].Draw('hist same')	
	hComponentsDown.Draw('hist same')
	for h in hComponents[1:]: 
		print 'there are actually components here!'
		h.Draw('hist same')
		cGold.Update()
		print 'updating stack', h
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
	pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
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


	histoMethodFracErrorNom = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystNom')
	histoMethodFracErrorNom.SetLineColor(kBlack)
	histoMethodFracErrorNom.SetFillStyle(1)
	histoMethodFracErrorUp = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystUp')
	histoMethodFracErrorUp.SetFillStyle(3001)
	histoMethodFracErrorUp.SetLineColor(kWhite)	
	histoMethodFracErrorUp.SetFillColor(hComponents[0].GetFillColor())	
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

	return hRatio, [histoMethodFracErrorNom, histoMethodFracErrorUp, histoMethodFracErrorDown, hComponentsUp, hComponentsDown]


def FabDraw(cGold,leg,hObserved,hComponents,datamc='mc',lumi='arbitrary', title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
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
	else: hComponents[0].GetYaxis().SetTitle('Events/GeV')
	cGold.Update()
	hObserved.GetYaxis().SetTitle('Normalized')
	hObserved.GetYaxis().SetTitleOffset(1.15)
	hObserved.SetMarkerStyle(20)
	histheight = 1.5*max(hComponents[0].GetMaximum(),hObserved.GetMaximum())
	if LinearScale: low, high = 0, histheight
	else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hObserved.GetMinimum())), 1000*histheight
	
	title0 = hObserved.GetTitle()
	if datamc=='MC':
		for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
		leg.AddEntry(hObserved,hObserved.GetTitle(),'lpf')        
	else:
		for ihComp, hComp in enumerate(hComponents):
			leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
		leg.AddEntry(hObserved,title0,'lp')    
	hObserved.SetTitle('')
	hComponents[0].SetTitle('')	
	hComponents[0].Draw('hist')
	for h in hComponents[1:]: 
		h.Draw('hist same')
		cGold.Update()
		print 'updating stack', h
	hComponents[0].Draw('same') 
	hObserved.Draw('p same')
	hObserved.Draw('e same')    
	cGold.Update()
	hComponents[0].Draw('axis same')           
	leg.Draw()        
	cGold.Update()
	stampFab(lumi,datamc)
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
	hObservedCopy = hObserved.Clone('hObservedClone'+hComponents[0].GetName())
	hRatio = hObservedCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
	hRatio.SetMarkerStyle(20)
	#hFracDiff = hComponents[0].Clone('hFracDiff')
	#hFracDiff.SetMarkerStyle(20)
	hObservedCopy.SetMarkerStyle(20)
	hObservedCopy.SetMarkerColor(1) 
	#histoStyler(hFracDiff, 1)
	histoStyler(hObservedCopy, 1)
	#hFracDiff.Add(hObservedCopy,-1)
	#hFracDiff.Divide(hObservedCopy)
	#hRatio.Divide(hObservedCopy)
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
	hRatio.GetXaxis().SetTitle(hObserved.GetXaxis().GetTitle())
	hRatio.Draw()
	hRatio.Draw('e0')    
	pad1.cd()
	hComponents.reverse()
	hObserved.SetTitle(title0)
	return hRatio
	
	
def stampFab(lumi,datamc='MC'):
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(1.6*tl.GetTextSize())
	tl.DrawLatex(0.152,0.82, 'CMS')
	tl.SetTextFont(extraTextFont)
	tl.DrawLatex(0.14,0.74, ('MC' in datamc)*' simulation'+' preliminary')
	tl.SetTextFont(regularfont)
	if lumi=='': tl.DrawLatex(0.62,0.82,'#sqrt{s} = 13 TeV')
	else: tl.DrawLatex(0.5,0.82,'#sqrt{s} = 13 TeV, L = '+str(lumi)+' fb^{-1}')
	#tl.DrawLatex(0.64,0.82,'#sqrt{s} = 13 TeV')#, L = '+str(lumi)+' fb^{-1}')	
	tl.SetTextSize(tl.GetTextSize()/1.6)


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


def prepareReaderPixelStrips(reader, xmlfilename):
		reader.AddVariable("dxyVtx",_dxyVtx_)      
		reader.AddVariable("dzVtx",_dzVtx_)          
		reader.AddVariable("matchedCaloEnergy",_matchedCaloEnergy_)
		reader.AddVariable("trkRelIso",_trkRelIso_)
		reader.AddVariable("nValidPixelHits",_nValidPixelHits_)
		reader.AddVariable("nValidTrackerHits",_nValidTrackerHits_)
		reader.AddVariable("nMissingOuterHits",_nMissingOuterHits_)
		reader.AddVariable("ptErrOverPt2",_ptErrOverPt2_)
		reader.BookMVA("BDT", xmlfilename)
	
def prepareReaderPixel(reader, xmlfilename):
		reader.AddVariable("dxyVtx",_dxyVtx_)     
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
		return  reader.EvaluateMVA("BDT")
	
def prepareReaderPixelStrips_loose(reader, xmlfilename):
		reader.AddVariable("dzVtx",_dzVtx_)          
		reader.AddVariable("matchedCaloEnergy",_matchedCaloEnergy_)
		reader.AddVariable("trkRelIso",_trkRelIso_)
		reader.AddVariable("nValidPixelHits",_nValidPixelHits_)
		reader.AddVariable("nValidTrackerHits",_nValidTrackerHits_)
		reader.AddVariable("nMissingOuterHits",_nMissingOuterHits_)
		reader.AddVariable("ptErrOverPt2",_ptErrOverPt2_)
		reader.BookMVA("BDT", xmlfilename)
	
def prepareReaderPixel_loose(reader, xmlfilename):
		reader.AddVariable("dzVtx",_dzVtx_)           
		reader.AddVariable("matchedCaloEnergy",_matchedCaloEnergy_)
		reader.AddVariable("trkRelIso",_trkRelIso_)
		reader.AddVariable("nValidPixelHits",_nValidPixelHits_)
		reader.AddVariable("nValidTrackerHits",_nValidTrackerHits_)
		reader.AddVariable("ptErrOverPt2",_ptErrOverPt2_)
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
		if not (c.tracks_trkRelIso[itrack]<0.2 and dzVtx<0.1 and pterr<10): return 0, -11
		if not c.tracks_nMissingMiddleHits[itrack]==0: return 0,-11
		if not (c.tracks_trackQualityHighPurity[itrack]): return 0,-11
		nhits = c.tracks_nValidTrackerHits[itrack]
		nlayers = c.tracks_trackerLayersWithMeasurement[itrack]
		if not (nlayers>=2 and nhits>=2): return 0,-11
		matchedCalo = c.tracks_matchedCaloEnergy[itrack]
		if not c.tracks_chi2perNdof[itrack]<2.88: return 0,-11
		if not dxyVtx < 0.1: return 0,-11
		trackfv = [dxyVtx, dzVtx, matchedCalo, c.tracks_trkRelIso[itrack], phits, thits, moh_, pterr]
		shortmvathresh, longmvathresh = threshes
		if pixelOnly:
				mva_ = evaluateBDT(readerPixelOnly, trackfv)
				if mva_ > (dxyVtx*0.65/0.01-0.25) and c.tracks_trkRelIso[itrack]<0.01: return 1, mva_      #tightening if not mva_ > dxyVtx*0.5/0.01-0.3: return 0 in any fashion tended to kill the electron and pion, but only with dphileps
				elif mva_ < (dxyVtx*0.65/0.01-0.5) and dxyVtx>0.02: return -1, mva_
				else: return 0, mva_
		elif pixelStrips:
				mva_ = evaluateBDT(readerPixelStrips, trackfv) 
				if mva_>(dxyVtx*0.7/0.01+0.05) and c.tracks_trkRelIso[itrack]<0.01: return 2, mva_# this made the MC "happy": if not (mva_>dxyVtx*0.6/0.01+0.05): return 0					
				elif mva_<(dxyVtx*0.7/0.01-0.5) and dxyVtx>0.02: return -2, mva_
				else: return 0, mva_
		else:
				return 0, mva_
							 
def isBaselineTrack(track, itrack, c, hMask):
	if not abs(track.Eta())< 2.4 : return False
	if not (abs(track.Eta()) < 1.4442 or abs(track.Eta()) > 1.566): return False
	if not bool(c.tracks_trackQualityHighPurity[itrack]) : return False
	if not (c.tracks_ptError[itrack]/(track.Pt()*track.Pt()) < 10): return False
	if not abs(c.tracks_dxyVtx[itrack]) < 0.1: return False    ##################hello, this should be synchronized with Viktor
	if not abs(c.tracks_dzVtx[itrack]) < 0.1 : return False
	if not c.tracks_trkRelIso[itrack] < 0.2: return False
	if not (c.tracks_trackerLayersWithMeasurement[itrack] >= 2 and c.tracks_nValidTrackerHits[itrack] >= 2): return False
	if not c.tracks_nMissingInnerHits[itrack]==0: return False
	if not c.tracks_nMissingMiddleHits[itrack]==0: return False
	if not c.tracks_chi2perNdof[itrack]<2.88: return 0
	if hMask!='':
		xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
		ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
		if hMask.GetBinContent(ibinx, ibiny)==0: return False
	return True
				
