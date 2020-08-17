from ROOT import *
from utils import *
from glob import glob

'''
    if not (bool(t.JetID) and  t.NVtx>0): return False
    if not  passQCDHighMETFilter(t): return False
    if not passQCDHighMETFilter2(t): return False
    if not t.PFCaloMETRatio<5: return False
    if not t.globalSuperTightHalo2016Filter: return False
    if not t.HBHENoiseFilter: return False    
    if not t.: return False
    if not t.: return False      
    if not t.: return False
    if not t.: return False
    if not t.: return False
    if not t.: return False    
'''
filters = 'JetID && globalSuperTightHalo2016Filter && HBHENoiseFilter && HBHEIsoNoiseFilter && eeBadScFilter && BadChargedCandidateFilter && BadPFMuonFilter && CSCTightHaloFilter && EcalDeadCellTriggerPrimitiveFilter'

chain = TChain('TreeMaker2/PreSelection')
#chain.Add('/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/Summer16.ZJetsToNuNu_Zpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_120000-B044CEA0-F8C9-E611-8F67-0CC47AD990C4_RA2AnalysisTree.root')

thelist = glob('/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/ProductionRun2v3/Run*2016C*MET*')
for filename in thelist: chain.Add(filename)

print 'entries', chain.GetEntries()

c1 = mkcanvas('c1')
chain.Show(0)
chain.Draw('MET>>hadc(30,200,500)','(MET>250 && Jets[0].Pt()>100 && DeltaPhi1>0.5 && DeltaPhi2>0.5 && DeltaPhi3>0.3 && DeltaPhi1>0.3 && NElectrons==0 && NMuons==0 && '+filters +')', 'hist text')
hist = chain.GetHistogram().Clone()
hist.SetDirectory(0)
print 'integral', hist.Integral()
fnew = TFile('liltest.root', 'recreate')
hist.Write()
print 'jut created', fnew.GetName()
fnew.Close()
c1.SetLogy()
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