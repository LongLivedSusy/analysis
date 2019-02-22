from ROOT import *
from utils import *
from random import shuffle
gROOT.SetBatch(1)
gStyle.SetOptStat(0)

#create dictionaries of event types pointing to files:
execfile('tools/EventCategories.py')


UseOptimizedCuts = True
dolog = True
lumi = 35900.#
lumi = 150000.#/pb

nsigs = 5
	
fnew = TFile('canvases.root','recreate')

#this code combines events stored in trees in many files such as
#/nfs/dust/cms/user/beinsam/CMSDAS2018b/Skims/Background/skim_TTJets_HT-600to800.root 
#the list of braches can be shown by opening a file and using the TTree::Show(0) method
show=1

cutsets = {}
cutsets['PromptNoCuts'] = 'Met>200 && NJets>=1'
cutsets['PromptLowMhtBaseline']  = 'Ht>250 && Mht >250 && NJets>=1 && NLeptons == 0 && BTags >= 0 && MinDeltaPhiMhtJets > 0.28 && NTags>0'
cutsets['PromptVLowMhtBaseline']  = 'Ht>250 && Mht >150 && NJets>=1 && NLeptons == 0 && BTags >= 0 && MinDeltaPhiMhtJets > 0.28 && NTags>0'
#cutsets['OptimumT1qqqq']  = 'Ht>322 && Mht >322 && NJets>=1 && NLeptons == 0 && BTags == 0 && MinDeltaPhiMhtJets > 0.28 && NTags>0'
#can add 

histframes = {}
histframes['Mht'] = TH1F('Mht','',7,250,950)
histframes['Ht'] = TH1F('Ht','',5,100,3100)
histframes['NJets'] = TH1F('NJets','',9,0,9)
histframes['BTags'] = TH1F('BTags','',5,0,5)
histframes['NLeptons'] = TH1F('NLeptons','',4,0,4)
histframes['NTags'] = TH1F('NTags','',4,0,4)
histframes['MinDeltaPhiMhtJets'] = TH1F('MinDeltaPhiMhtJets','',10,0,3.2)
histframes['Track1MassFromDedx'] = TH1F('Track1MassFromDedx','',20,0,1000)
histframes['Track1Pt'] = TH1F('Track1Pt','',20,0,1000)

for selectionkey in cutsets:
 hists = {}
 histsStack = {}
 for histkey in histframes:
	cwaste = TCanvas('cwaste')
	growinghist = histframes[histkey].Clone(histkey)
	histframes[histkey].GetXaxis().SetTitle(namewizard(histframes[histkey].GetName()))
	growinghist.GetXaxis().SetTitle(namewizard(histkey))	
	histoStyler(growinghist, kGray+1)
	growinghist.SetFillStyle(1001)	
	nbins = histframes[histkey].GetXaxis().GetNbins()
	xlow, xhigh = histframes[histkey].GetXaxis().GetBinLowEdge(1), histframes[histkey].GetXaxis().GetBinUpEdge(nbins)
	drawarg = 'max(%f+0.001,min(%f-0.001,%s))>>hadc(%d,%f,%f)'%(xlow,xhigh,histkey,nbins,xlow,xhigh)
	weightstring = '('+cutsets[selectionkey]+')*weight*'+str(lumi)	
	if UseOptimizedCuts: weightstring+='*('+'1'+')'		
	for category in CategoryKeysSmallToBig:
		hCategory = histframes[histkey].Clone(histkey+'_cat')
		histoStyler(hCategory,ColorsByCategory[category])
		hCategory.SetFillColor(ColorsByCategory[category])
		hCategory.SetFillStyle(1001)
		histoStyler(growinghist,ColorsByCategory[category])
		growinghist.SetFillColor(ColorsByCategory[category])
		growinghist.SetFillStyle(1001)			
		for subcategory in SubcategoryChainDictsByCategoryDict[category]:
			if show==1:
				SubcategoryChainDictsByCategoryDict[category][subcategory].Show(0)
				show=0
			SubcategoryChainDictsByCategoryDict[category][subcategory].Draw(drawarg,weightstring)
			h = SubcategoryChainDictsByCategoryDict[category][subcategory].GetHistogram()
			#if histkey==histframes.keys()[0]: print 'drawing', subcategory, 'with integral', h.Integral()			
			hCategory.Add(h)
		growinghist.Add(hCategory)			
		hists[category] = hCategory.Clone(category)
		histsStack[category] = growinghist.Clone(category+'_stack')
	sighists = []
	for key in SignalChainDict:
		SignalChainDict[key].Draw(drawarg+' text',weightstring.replace(' && NPrompt>0', '').replace('&& NPrompt==0','').replace('&& NPrompt==1',''))
		hsig = SignalChainDict[key].GetHistogram()
		if histkey==histframes.keys()[0]: print 'drawing', key, 'with', hsig.Integral()
		hsig.SetDirectory(0)
		hsig.SetTitle(key)
		sighists.append(hsig)
		histoStyler(sighists[-1],ColorsBySignal[key])
		sighists[-1].SetLineStyle(kDashed)
		sighists[-1].SetLineWidth(3)		
		sighists[-1].SetLineColor(sighists[-1].GetMarkerColor())
		if len(sighists)==nsigs: break				
	c1 = mkcanvas('c_'+histkey)
	if dolog: c1.SetLogy()
	histsStack[CategoryKeysBigToSmall[0]].SetLineColor(kGray+1)		
	if dolog:
		histsStack[CategoryKeysBigToSmall[0]].GetYaxis().SetRangeUser(0.1,300*histsStack[CategoryKeysBigToSmall[0]].GetMaximum())
	else:
		histsStack[CategoryKeysBigToSmall[0]].GetYaxis().SetRangeUser(0,1.3*histsStack[CategoryKeysBigToSmall[0]].GetMaximum())
	legBkg = mklegend(x1=.61, y1=.56, x2=.95, y2=.88, color=kWhite)
	arg = ''
	for category in CategoryKeysBigToSmall:
		histsStack[category].Draw('hist '+arg)
		legBkg.AddEntry(histsStack[category],category,'f')
		arg = 'same'
	histsStack[CategoryKeysBigToSmall[0]].Draw('same E0')
	legSig = mklegend(x1=.16, y1=.7, x2=.6, y2=.88, color=kWhite)	
	for sighist in sighists:
		sighist.Draw('hist same')
		legSig.AddEntry(sighist,sighist.GetTitle().replace('_MCMC1',''),'l')
	histsStack[CategoryKeysBigToSmall[0]].Draw('axis same')	
	legBkg.Draw()
	legSig.Draw()
	stamp(round(1.0*lumi/1000,1), True)
	c1.Update()
	fnew.cd()	
	c1.Write('c_'+histkey+'_'+selectionkey)
	c1.Print('pdfs/kinematics/'+histkey+'_'+selectionkey+'.pdf')
	del cwaste
print 'just created', fnew.GetName()
fnew.Close()
			
			
#cutsets['hmmm'] = 'Mht > 327.216 && NJets>=6 && NLeptons == 0 && BTags == 0 && MinDeltaPhiMetJets > 0.369945'
			
