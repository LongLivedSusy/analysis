from ROOT import *
from utils import *


lep = 'Mu'
sample = 'Run2016'
sample = 'Summer16.DYJets'
fNonSmeared = TFile('RawKappaMaps/RawKapps_'+sample+'_PixAndStrips_NoZSmear.root')
fSmeared = TFile('RawKappaMaps/RawKapps_'+sample+'_PixAndStrips_YesZSmear.root')
fNonSmeared.ls()
c1 = mkcanvas()
c1.SetLogy()
hDTNonSmeared = fNonSmeared.Get('h'+lep+'ProbePtDT_eta0to2.4_num')
hRLNonSmeared = fNonSmeared.Get('h'+lep+'ProbePtRECO_eta0to2.4_den')
hDTSmeared = fSmeared.Get('h'+lep+'ProbePtDT_eta0to2.4_num')
hRLSmeared = fSmeared.Get('h'+lep+'ProbePtRECO_eta0to2.4_den')
hRLNonSmeared.GetYaxis().SetRangeUser(0.001,1000000)
hRLNonSmeared.Draw()
hDTNonSmeared.Draw('same')
hRLSmeared.Draw('same hist l')
hDTSmeared.Draw('same hist l')
c1.Update()
pause()