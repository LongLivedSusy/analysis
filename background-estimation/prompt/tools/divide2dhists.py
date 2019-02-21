from ROOT import *
from utils import *

f1 = TFile('test.root')
f2 = TFile('RawKapps_WJets.root')

#f1 = TFile('output/smallchunks/PromptBkgHists_WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_3_nFiles1Truth.root')
#f2 = TFile('output/smallchunks/TagnProbeEleHists_WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_3_nFiles1.root')

#f1 = TFile('test0.root')
#f2 = TFile('test1.root')

keys = ['hGenPtvsEtaDT_num', 'hGenPtvsEtaRECO_den']
f1.ls()

for key in keys:
	h1 = f1.Get(key)
	h2 = f2.Get(key)
	hratio = h1.Clone()
	hratio.Divide(h2)
	hratio.Draw("colz text e")
	c1.Update()
	pause()

exit(0)