from ROOT import *
import os, sys
gROOT.SetBatch(1)
lumi = 35.9
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
gStyle.SetOptStat(0)

fPrompt = TFile('/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Background/prompt-bg-results.root')
fFake = TFile('/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Background/fake-bg-results.root')
sigfilenames = ['/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Signal/T1qqqqLL/Glu2000_Chi1ne1800.root',\
				'/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Signal/T1qqqqLL/Glu2000_Chi1ne150.root',\
				'/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Signal/T2btLL/Stop1350_Chi1ne1200.root',\
					]

stuff = 'Zone3p4To6p0'
stuff = ''
hElectron = fPrompt.Get('hElBaseline'+stuff+'_BinNumberMethod')
hMuon = fPrompt.Get('hMuBaseline'+stuff+'_BinNumberMethod')
hPion = fPrompt.Get('hPiBaseline'+stuff+'_BinNumberMethod')
hFake_ = fFake.Get('hFkBaseline_BinNumberMethod')

hFake = hElectron.Clone('hFake')
xax = hFake.GetXaxis()
for ibin in range(1,xax.GetNbins()+1):
	hFake.SetBinContent(ibin,hFake_.GetBinContent(ibin))
	hFake.SetBinError(ibin,hFake_.GetBinError(ibin))

histoStyler(hFake, kGray+1)
hFake.SetFillColor(kGray+1)
hFake.SetFillStyle(3001)
hFake.SetTitle('fake DT')

hElectron.SetTitle('DT from el.')
hMuon.SetTitle('DT from #mu')
hPion.SetTitle('DT from #pi')

print 'cloning muon'
hTruth = hMuon.Clone('hObserved')
hTruth.SetTitle('Observed')
print 'adding electron'
hTruth.Add(hElectron)
hTruth.Add(hFake)
print 'adding pion'
hTruth.Add(hPion)
hTruth.SetLineColor(kBlack)
hTruth.SetMarkerColor(kBlack)


c1 = mkcanvas_wide('c1')
c1.SetLeftMargin(0.02)
colors = [2,4, kTeal-5, kYellow, kOrange+1, kGreen-2, kGreen-1, kGreen, kGreen+1, kGreen+2]
	
	
leg = mklegend(x1=.24, y1=.62, x2=.5, y2=.86, color=kWhite)
hratio, pad1, pad2 = FabDraw(c1,leg,hTruth,[hMuon,hPion,hElectron,hFake],datamc='data',lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
hElectron.GetYaxis().SetTitle("Events/bin")
hElectron.GetYaxis().SetTitleOffset(0.59)
hElectron.GetYaxis().SetTitleSize(0.075)
hratio.GetYaxis().SetRangeUser(0.2,1.8)
hratio.GetYaxis().SetTitleOffset(0.37)

pad1.cd()
sigfiles = []
sighists = []
leg2 = mklegend(x1=.45, y1=.61, x2=.69, y2=.82, color=kWhite)
for isig, sigfile in enumerate(sigfilenames):
	fsig = TFile(sigfile)
	sigfiles.append(fsig)
	hsig = sigfiles[-1].Get('hBaseline_BinNumberTruth')
	sighists.append(hsig)	
	sighists[-1].SetDirectory(0)
	histoStyler(sighists[-1], colors[isig])	
	print isig, 'drawing', sigfile
	sighists[-1].Draw('same hist')
	leg2.AddEntry(sighists[-1], sigfile.split('/')[-1].replace('.root',''),'l')
	
leg2.Draw()
c1.Update()

fnew = TFile('binplot.root','recreate')
c1.Write()
print 'just created', fnew.GetName()
fnew.Close()







