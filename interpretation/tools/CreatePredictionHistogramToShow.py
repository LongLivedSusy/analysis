from ROOT import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
gROOT.SetBatch(1)

from CrossSectionDictionary import *
loadCrossSections('T1')
lumi = 35.9
#fpred = TFile('HistsBkgObsSig/WithDeDx/Background/prompt-bg-results.root')
#fpred = TFile('HistsBkgObsSig/WithDeDx/Background/prompt-bg-results_data.root')
fpred = TFile('/nfs/dust/cms/user/beinsam/LongLiveTheChi/Analyzer/CMSSW_10_1_0/src/analysis/background-estimation/prompt/prompt-bg-results_repaired.root')
fpred.ls()
fFake = TFile('/nfs/dust/cms/user/kutznerv/shorttrack/analysis/bg-non-prompt/closure_Run2016_v6.root')
fFake.ls()

mode = "ShowMuVetoEffect"
mode = "DeDxEffect"
muveto = 'MuVeto'
muveto = ''
njetstatus = 'HighNJet'
njetstatus = ''

#					'HistsBkgObsSig/WithDeDx/Signal/T1qqqq_CTau50_BR100/AnalysisHistsDedx_g1700_chi1550_27_200970_step4_50miniAODSIM_6_.root',\
linearscale = True


if mode=='ShowMuVetoEffect':
	signalfilenames = [	
						'HistsBkgObsSig/WithDeDxLowMet/Signal/T1qqqq_CTau200_BR67/AnalysisHistsDedxLowMht_g2400_chi200_27_200970_step4_50miniAODSIM_82_.root'
						]
elif mode=='DeDxEffect':
	signalfilenames = [
						'HistsBkgObsSig/WithDeDxLowMet/Signal/T1qqqq_CTau50_BR67/AnalysisHistsDedxLowMht_g1700_chi1550_27_200970_step4_50miniAODSIM_6_.root',\
				   		]
signalfiles = []					
for sfname in signalfilenames:
	signalfiles.append(TFile(sfname))

print 'hello'

fnew_ = TFile('plot'+mode+'_'+muveto+'.root', 'recreate')
c1 = mkcanvas()
vars = ['BinNumber', 'Log10DedxMass', 'NJets', 'Mht', 'DeDxAverage']
for var in vars:
	print 'doing', var
	hElBaseline_VarMethod = fpred.Get('hEl'+njetstatus+'Baseline'+muveto+'_'+var+'Method')
	hMuBaseline_VarMethod = fpred.Get('hMu'+njetstatus+'Baseline'+muveto+'_'+var+'Method')
	hPiBaseline_VarMethod = fpred.Get('hPi'+njetstatus+'Baseline'+muveto+'_'+var+'Method')
	if njetstatus=='' or True: 
		hFkBaseline_VarMethod = fFake.Get('hFk'+njetstatus+'Baseline'+muveto+'_'+var+'Method')
		if 'BinNumber' in var: hFkBaseline_VarMethod.SetBinContent(1,0)

	hElBaseline_VarMethod.SetFillColor(kGreen+1); hElBaseline_VarMethod.SetFillStyle(1001); 
	hPiBaseline_VarMethod.SetFillColor(kOrange+1); hPiBaseline_VarMethod.SetFillStyle(1001); 
	hMuBaseline_VarMethod.SetFillColor(kViolet); hMuBaseline_VarMethod.SetFillStyle(1001); 
	if njetstatus=='' or True: hFkBaseline_VarMethod.SetFillColor(kGray+1); hFkBaseline_VarMethod.SetFillStyle(1001); 
	
	hElBaseline_VarMethod.SetLineColor(kGreen+1); hElBaseline_VarMethod.SetTitle('e background')
	hMuBaseline_VarMethod.SetLineColor(kViolet); hMuBaseline_VarMethod.SetTitle('#mu background')	
	hPiBaseline_VarMethod.SetLineColor(kOrange+1); hPiBaseline_VarMethod.SetTitle('#pi background')
	if njetstatus=='' or True: hFkBaseline_VarMethod.SetLineColor(kGray+1); hFkBaseline_VarMethod.SetTitle('fake background')
	

			
	hdata = hElBaseline_VarMethod.Clone('hdata_'+var)
	hdata.SetDirectory(0)
	hdata.Add(hPiBaseline_VarMethod)
	hdata.Add(hMuBaseline_VarMethod)
	if njetstatus=='' or True:  hdata.Add(hFkBaseline_VarMethod)
	hdata.SetTitle('observed')
	histoStyler(hdata, kBlack)
	
	
	if linearscale:
		hElBaseline_VarMethod.GetYaxis().SetRangeUser(0, 1.5*hdata.GetMaximum())
		hPiBaseline_VarMethod.GetYaxis().SetRangeUser(0, 1.5*hdata.GetMaximum())
		hMuBaseline_VarMethod.GetYaxis().SetRangeUser(0, 1.5*hdata.GetMaximum())
		hdata.GetYaxis().SetRangeUser(0, 1.5*hdata.GetMaximum())
	
	else:
		hElBaseline_VarMethod.GetYaxis().SetRangeUser(0.001, 100*hdata.GetMaximum())
		hPiBaseline_VarMethod.GetYaxis().SetRangeUser(0.001, 100*hdata.GetMaximum())
		hMuBaseline_VarMethod.GetYaxis().SetRangeUser(0.001, 100*hdata.GetMaximum())
		hdata.GetYaxis().SetRangeUser(0.001, 1000*hdata.GetMaximum())


	c1 = mkcanvas()
	leg = mklegend(x1=.2, y1=.45, x2=.5, y2=.7, color=kWhite)
	backs = [hMuBaseline_VarMethod, hElBaseline_VarMethod, hPiBaseline_VarMethod]
	backs = [hFkBaseline_VarMethod]+backs	
	
	hratio = FabDraw(c1,leg,hdata,backs,datamc='Data',lumi=str(lumi), title = '', LinearScale=linearscale, fractionthing='observed / predicted')
	hratio.GetYaxis().SetRangeUser(0, 2)
	hratio.GetXaxis().SetTitle(var)

	colors = [kBlue, kRed, kTeal-5]
	sigleg = mklegend(x1=.43, y1=.42, x2=.88, y2=.7, color=kWhite)
	for isig, sigfile in enumerate(signalfiles):
		sighist = sigfile.Get('h'+njetstatus+'Baseline'+muveto+'_'+var+'Truth')
		sighist.SetLineWidth(3)
		sighist.SetLineColor(colors[isig])
		sighist.Scale(1000*lumi)
		#sighist.Scale(CrossSectionsPb["T1"]["2150"]/CrossSectionsPb["T1"]["1700"])
		br = sigfile.GetName().split('_BR')[-1].split('/')[0]+'%'
		smodel = sigfile.GetName().split('Dedx_')[-1].split('_27')[0]
		sigleg.AddEntry(sighist, smodel+' BR(#tilde{g}#rightarrow #tilde{#chi}^{#pm},q#bar{q})='+br)
		sighist.Draw('same hist text')
		sighist.Write()
	sigleg.Draw()
	fnew_.cd()
	print 'writing', var
	c1.Write('Prediction2016_'+var)
	hdata.Write()
print 'just created', fnew_.GetName()
fnew_.Close()