from ROOT import *

fofinterest = TFile('output/totalweightedbkgsDataDrivenMC.root')
fofinterest.ls()


hElectron = fofinterest.Get('hElBaseline_BinNumberMethod')
hMuon = fofinterest.Get('hMuBaseline_BinNumberMethod')
hPion = fofinterest.Get('hPiBaseline_BinNumberMethod')
hTruth = fofinterest.Get('hElBaseline_BinNumberTruth')

hists = [hElectron, hMuon, hPion]
for hist in hists:
	xax = hist.GetXaxis()
	hist.SetBinContent(xax.FindBin(0.5), 0)

fnew = TFile('prompt-bg-results.root','recreate')

hElectron.Write()
hMuon.Write()
hPion.Write()
#hTruth.Write()


print 'just created', fnew.GetName()

fnew.Close()