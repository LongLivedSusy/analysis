from ROOT import *
from utils import *



chain = TChain('TreeMaker2/PreSelection')
chain.Add('/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Summer16.ZJetsToNuNu_Zpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_120000-B044CEA0-F8C9-E611-8F67-0CC47AD990C4_RA2AnalysisTree.root')

chain.Show(0)
chain.Draw('MET','Jets[0].Pt()>100')

c1.Update()
pause()


nentries = chain.GetEntries()
print 'n(entries)', nentries

for ientry in range(5):
	chain.GetEntry(ientry)
	
	print 'processing event', ientry
	print 'slimmedMET', chain.MET
	
	print 'jets:'
	for ijet, jet in enumerate(chain.Jets):
		print ijet, jet.Pt(), jet.Eta(), jet.Phi()