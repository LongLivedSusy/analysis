import os,sys
from ROOT import *
gROOT.SetBatch(1)

c=TCanvas('c','',800,600)

f = TFile('SV_rootfiles/vertex_Run2016G.root')

#h = f.Get('h2_P_protonVsDeDxPixelCalib')
h = f.Get('h2_P_protonVsDeDxStrips')

h.Draw('COLZ')

#c.SetLogz()
c.SaveAs('test.png')
