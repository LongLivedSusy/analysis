from ROOT import *

fofinterest = TFile('output/totalweightedbkgsDataDrivenDataNoSmear.root')
fofinterest.ls()

fnew = TFile('prompt-bg-results.root','recreate')
vars = ['BinNumber', 'Log10DedxMass', 'NJets', 'Mht', 'DeDxAverage']

for var in vars:

	hElectron = fofinterest.Get('hElBaseline_'+var+'Method')
	hMuon = fofinterest.Get('hMuBaseline_'+var+'Method')
	hPion = fofinterest.Get('hPiBaseline_'+var+'Method')
	hPion.Scale(0.5)
	hTruth = fofinterest.Get('hElBaseline_'+var+'Truth')
	hists = [hElectron, hMuon, hPion, hTruth]
	for hist in hists:
		xax = hist.GetXaxis()
		hist.SetBinContent(xax.FindBin(0.5), 0)

	hElectron.Write()
	hMuon.Write()
	hPion.Write()
	#hTruth.Write()
	
	
	hElectronMuVeto = fofinterest.Get('hElBaselineMuVeto_'+var+'Method')
	hMuonMuVeto = fofinterest.Get('hMuBaselineMuVeto_'+var+'Method')
	hPionMuVeto = fofinterest.Get('hPiBaselineMuVeto_'+var+'Method')
	hPionMuVeto.Scale(0.5)
	hTruthMuVeto = fofinterest.Get('hElBaselineMuVeto_'+var+'Truth')
	hists = [hElectronMuVeto, hMuonMuVeto, hPionMuVeto, hTruthMuVeto]
	for hist in hists:
		xax = hist.GetXaxis()
		hist.SetBinContent(xax.FindBin(0.5), 0)

	hElectronMuVeto.Write()
	hMuonMuVeto.Write()
	hPionMuVeto.Write()
	#hTruthMuVeto.Write()
	
	hElectronMuVeto = fofinterest.Get('hElHighNJetBaseline_'+var+'Method')
	hMuonMuVeto = fofinterest.Get('hMuHighNJetBaseline_'+var+'Method')
	hPionMuVeto = fofinterest.Get('hPiHighNJetBaseline_'+var+'Method')
	hPionMuVeto.Scale(0.5)
	hTruthMuVeto = fofinterest.Get('hElHighNJetBaseline_'+var+'Truth')
	hists = [hElectronMuVeto, hMuonMuVeto, hPionMuVeto, hTruthMuVeto]
	for hist in hists:
		xax = hist.GetXaxis()
		hist.SetBinContent(xax.FindBin(0.5), 0)

	hElectronMuVeto.Write()
	hMuonMuVeto.Write()
	hPionMuVeto.Write()
	#hTruthMuVeto.Write()
	
		

print 'just created', fnew.GetName()

fnew.Close()