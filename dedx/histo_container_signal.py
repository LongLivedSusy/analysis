##!/usr/bin/env python
from ROOT import *

# Histograms
h_nev = TH1F('h_nev','',1,0,1)
hHT_unweighted = TH1F('hHT_unweighted','hHT_unweighted',200,0,10000)
hMET = TH1F('hMET','hMET',100,0,1000)
hMHT = TH1F('hMHT','hMHT',100,0,1000)
hHT = TH1F('hHT','hHT',100,0,1000)
hNlepton = TH1F('Nlepton','Nlepton',10,0,10)

hGenGluinoMass = TH1F('hGenGluinoMass','Gen-gluino mass', 3000, 0, 3000)
hGenStopMass = TH1F('hGenStopMass','Gen-stop mass', 3000, 0, 3000)
hGenLSPMass = TH1F('hGenLSPMass','LSP mass', 3000, 0, 3000)

hGenCharginoP = TH1F('hGenCharginoP','Gen-chargino total momentum',1000,0,10000)
hGenCharginoPt = TH1F('hGenCharginoPt','Gen-chargino transverse momentum',1000,0,10000)
hGenCharginoEta = TH1F('hGenCharginoEta','Gen-chargino pseudo-rapidity',100,-2.5,2.5)
hGenCharginoPhi = TH1F('hGenCharginoPhi','Gen-chargino phi',100,-3.14,3.14)
hGenCharginoMass = TH1F('hGenCharginoMass','Gen-chargino mass',3000,0,3000)

hGenCharginoP_trackmatch = TH1F('hGenCharginoP_trackmatch','Gen-chargino total momentum',1000,0,10000)
hGenCharginoPt_trackmatch = TH1F('hGenCharginoPt_trackmatch','Gen-chargino transverse momentum',1000,0,10000)
hGenCharginoEta_trackmatch = TH1F('hGenCharginoEta_trackmatch','Gen-chargino pseudo-rapidity',100,-2.5,2.5)
hGenCharginoPhi_trackmatch = TH1F('hGenCharginoPhi_trackmatch','Gen-chargino phi',100,-3.14,3.14)

hTrkP = TH1F('hTrkP','hTrkP',1000,0,1000)
hTrkPt = TH1F('hTrkPt','pT of track',1000,0,1000)
hTrkEta = TH1F('hTrkEta','Track eta',100,-2.5,2.5)
hTrkPhi = TH1F('hTrkPhi','Track Phi',100,-3.14,3.14)

hTrkP_charginomatch = TH1F('hTrkP_charginomatch','Chargino-matched track total momentum',1000,0,10000)
hTrkPt_charginomatch = TH1F('hTrkPt_charginomatch','Chargino-matched track transverse momentum',1000,0,10000)
hTrkEta_charginomatch = TH1F('hTrkEta_charginomatch','Chargino-matched track pseudo-rapidity',100,-2.5,2.5)
hTrkPhi_charginomatch = TH1F('hTrkPhi_charginomatch','Chargino-matched track phi',100,-3.14,3.14)

hTrkPixelDedx_charginomatch = TH1F('hTrkPixelDedx_charginomatch','Chargino-matched track pixel dedx',300,0,30)
hTrkPixelDedx_charginomatch_barrel = TH1F('hTrkPixelDedx_charginomatch_barrel','Chargino-matched track pixel dedx at barrel region',300,0,30)
hTrkPixelDedx_charginomatch_endcap = TH1F('hTrkPixelDedx_charginomatch_endcap','Chargino-matched track pixel dedx at endcap region',300,0,30)
hTrkPixelDedx_charginomatch_SR = TH1F('hTrkPixelDedx_charginomatch_SR','Chargino-matched track pixel dedx',2,0,2)
hTrkPixelDedx_charginomatch_barrel_SR = TH1F('hTrkPixelDedx_charginomatch_barrel_SR','Chargino-matched track pixel dedx',2,0,2)
hTrkPixelDedx_charginomatch_endcap_SR = TH1F('hTrkPixelDedx_charginomatch_endcap_SR','Chargino-matched track pixel dedx',2,0,2)

hTrkPixelDedxScale_charginomatch = TH1F('hTrkPixelDedxScale_charginomatch','Chargino-matched track pixel dedx',2,0,1)
hTrkPixelDedxScale_charginomatch_barrel = TH1F('hTrkPixelDedxScale_charginomatch_barrel','Chargino-matched track pixel dedx at barrel region',300,0,30)
hTrkPixelDedxScale_charginomatch_endcap = TH1F('hTrkPixelDedxScale_charginomatch_endcap','Chargino-matched track pixel dedx at endcap region',300,0,30)
hTrkPixelDedxScale_charginomatch_SR = TH1F('hTrkPixelDedxScale_charginomatch_SR','Chargino-matched track pixel dedx',2,0,2)
hTrkPixelDedxScale_charginomatch_barrel_SR = TH1F('hTrkPixelDedxScale_charginomatch_barrel_SR','Chargino-matched track pixel dedx at barrel region',2,0,2)
hTrkPixelDedxScale_charginomatch_endcap_SR = TH1F('hTrkPixelDedxScale_charginomatch_endcap_SR','Chargino-matched track pixel dedx at endcap region',2,0,2)

hTrkStripsDedx_charginomatch = TH1F('hTrkStripsDedx_charginomatch','Chargino-matched track strips dedx',300,0,30)
hTrkStripsDedx_charginomatch_barrel = TH1F('hTrkStripsDedx_charginomatch_barrel','Chargino-matched track strips dedx at barrel region',300,0,30)
hTrkStripsDedx_charginomatch_endcap = TH1F('hTrkStripsDedx_charginomatch_endcap','Chargino-matched track strips dedx at endcap region',300,0,30)
hTrkStripsDedxCalib_charginomatch_barrel = TH1F('hTrkStripsDedxCalib_charginomatch_barrel','Chargino-matched track strips dedx at barrel region',300,0,30)
hTrkStripsDedxCalib_charginomatch_endcap = TH1F('hTrkStripsDedxCalib_charginomatch_endcap','Chargino-matched track strips dedx at endcap region',300,0,30)

h2_GenP_vs_PixelDedx = TH2F('h2_GenP_vs_PixelDedx','chargino P vs pixel dEdx', 100,0,10000,100,0,30)
