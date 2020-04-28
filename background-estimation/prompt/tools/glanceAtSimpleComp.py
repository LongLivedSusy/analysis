from ROOT import *
from utils import *


fsimple = TFile('testWJ.root')
fcomp = TFile('output/bigchunks/WJetsNoZSmear.root')



lumi = 35.6
htsimpleCount = fsimple.Get('hHt')
nsimple = htsimpleCount.GetEntries()

hHtWeightedSimple = fsimple.Get('hHtWeighted').Clone('hHtWeightedSimple')
hHtWeightedSimple.Scale(1000.*lumi/nsimple)

hHtWeightedComplex = fcomp.Get('hHtWeighted').Clone('hHtWeightedComplex')

hHtWeightedComplex.SetLineColor(kRed)

hHtWeightedSimple.Draw('hist')
c1.SetLogy()
c1.Update()
hHtWeightedComplex.Draw('histe same')
c1.SetLogy()
c1.Update()
pause()

