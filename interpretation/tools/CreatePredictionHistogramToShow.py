from ROOT import *
from shared_utils import * #let's make one symlink for everything
gROOT.SetBatch(1)

lumi = 35.6
fpred = TFile('HistsBkgObsSig/WithDeDx/Background/prompt-bg-results.root')
fpred.ls()

signalfilenames = ['HistsBkgObsSig/WithDeDx/Signal/T1qqqq_CTau50_BR100/AnalysisHistsDedx_g1800_chi400_27_200970_step4_50miniAODSIM_99_.root',\
					'HistsBkgObsSig/WithDeDx/Signal/T1qqqq_CTau50_BR100/AnalysisHistsDedx_g1700_chi1550_27_200970_step4_50miniAODSIM_6_.root']
signalfiles = []					
for sfname in signalfilenames:
	signalfiles.append(TFile(sfname))


hElBaseline_BinNumberMethod = fpred.Get('hElBaseline_BinNumberMethod')
hMuBaseline_BinNumberMethod = fpred.Get('hMuBaseline_BinNumberMethod')
hPiBaseline_BinNumberMethod = fpred.Get('hPiBaseline_BinNumberMethod')

hElBaseline_BinNumberMethod.SetFillColor(kGreen+1); hElBaseline_BinNumberMethod.SetFillStyle(1001)
hPiBaseline_BinNumberMethod.SetFillColor(kOrange+1); hPiBaseline_BinNumberMethod.SetFillStyle(1001)
hMuBaseline_BinNumberMethod.SetFillColor(kViolet); hMuBaseline_BinNumberMethod.SetFillStyle(1001)

hdata = hElBaseline_BinNumberMethod.Clone('hdata')
hdata.Add(hPiBaseline_BinNumberMethod)
hdata.Add(hMuBaseline_BinNumberMethod)
hdata.SetTitle('observed')
histoStyler(hdata, kBlack)

hElBaseline_BinNumberMethod.GetYaxis().SetRangeUser(0.001, 100*hdata.GetMaximum())
hPiBaseline_BinNumberMethod.GetYaxis().SetRangeUser(0.001, 100*hdata.GetMaximum())
hMuBaseline_BinNumberMethod.GetYaxis().SetRangeUser(0.001, 100*hdata.GetMaximum())
hdata.GetYaxis().SetRangeUser(0.001, 1000*hdata.GetMaximum())

fnew = TFile('plot.root', 'recreate')
c1 = mkcanvas()
leg = mklegend(x1=.21, y1=.5, x2=.72, y2=.7, color=kWhite)
hratio = FabDraw(c1,leg,hdata,[hMuBaseline_BinNumberMethod, hPiBaseline_BinNumberMethod, hElBaseline_BinNumberMethod],datamc='MC',lumi=str(lumi), title = '', LinearScale=False, fractionthing='observed / predicted')
hratio.GetYaxis().SetRangeUser(0, 2)

#pad1 = c1.GetPad(1)
#pad1.cd()
colors = [kRed, kBlue, kYellow]
for isig, sigfile in enumerate(signalfiles):
	sighist = sigfile.Get('hBaseline_BinNumberTruth')
	sighist.SetLineColor(colors[isig])
	sighist.Scale(1000*lumi)
	sighist.Draw('same hist')

pad1.Update()


fnew.cd()
c1.Write('Prediction2016')
print 'just created', fnew.GetName()
fnew.Close()