#!/usr/bin/env python

from ROOT import *

# Histograms
hHT_unweighted = TH1F('hHT_unweighted','hHT_unweighted',200,0,10000)
hMET = TH1F('hMET','hMET',100,0,1000)
hMHT = TH1F('hMHT','hMHT',100,0,1000)
hHT = TH1F('hHT','hHT',100,0,1000)
hNlepton = TH1F('Nlepton','Nlepton',10,0,10)

hTrkP = TH1F('hTrkP','hTrkP',1000,0,10000)
hTrkP_tightmumatch =	TH1F('hTrkP_tightmumatch','P of track matched with tight muon',1000,0,10000)
hTrkP_tightmumatch_barrel = TH1F('hTrkP_tightmumatch_barrel','P of track matched with tight muon in barrel region',1000,0,10000)
hTrkP_tightmumatch_endcap = TH1F('hTrkP_tightmumatch_endcap','P of track matched with tight muon in endcap region',1000,0,10000)
hTrkP_tightgenmumatch =	TH1F('hTrkP_tightgenmumatch','P of track matched with gen-matched muon',1000,0,10000)
hTrkP_tightgenmumatch_barrel =  TH1F('hTrkP_tightgenmumatch_barrel','P of track matched with gen-matched muon in barrel region',1000,0,10000)
hTrkP_tightgenmumatch_endcap =  TH1F('hTrkP_tightgenmumatch_endcap','P of track matched with gen-matched muon in endcap region',1000,0,10000)
hTrkP_tightelematch =	TH1F('hTrkP_tightelematch','P of track matched with tight electron',1000,0,10000)
hTrkP_tightelematch_barrel = TH1F('hTrkP_tightelematch_barrel','P of track matched with tight electron in barrel region',1000,0,10000)
hTrkP_tightelematch_endcap = TH1F('hTrkP_tightelematch_endcap','P of track matched with tight electron in endcap region',1000,0,10000)
hTrkP_tightgenelematch = TH1F('hTrkP_tightgenelematch','P of track matched with gen-matched electron',1000,0,10000)
hTrkP_tightgenelematch_barrel = TH1F('hTrkP_tightgenelematch_barrel','P of track matched with gen-matched electron in barrel region',1000,0,10000)
hTrkP_tightgenelematch_endcap = TH1F('hTrkP_tightgenelematch_endcap','P of track matched with gen-matched electron in endcap region',1000,0,10000)

hTrkPt = TH1F('hTrkPt','pT of track',1000,0,10000)
hTrkPt_tightmumatch = TH1F('hTrkPt_tightmumatch','pT of track matched with tight muon',1000,0,10000)
hTrkPt_tightmumatch_barrel = TH1F('hTrkPt_tightmumatch_barrel','pT of track matched with tight muon in barrel region',1000,0,10000)
hTrkPt_tightmumatch_endcap = TH1F('hTrkPt_tightmumatch_endcap','hTrkPt_tightmumatch_endcap',1000,0,10000)
hTrkPt_tightgenmumatch = TH1F('hTrkPt_tightgenmumatch','hTrkPt_tightgenmumatch',1000,0,10000)
hTrkPt_tightgenmumatch_barrel = TH1F('hTrkPt_tightgenmumatch_barrel','hTrkPt_tightgenmumatch_barrel',1000,0,10000)
hTrkPt_tightgenmumatch_endcap = TH1F('hTrkPt_tightgenmumatch_endcap','hTrkPt_tightgenmumatch_endcap',1000,0,10000)

hTrkEta = TH1F('hTrkEta','Track eta',100,-2.5,2.5)
hTrkEta_tightmumatch = TH1F('hTrkEta_tightmumatch','hTrkEta_tightmumatch',100,-2.5,2.5)
hTrkEta_tightmumatch_barrel = TH1F('hTrkEta_tightmumatch_barrel','hTrkEta_tightmumatch_barrel',100,-2.5,2.5)
hTrkEta_tightmumatch_endcap = TH1F('hTrkEta_tightmumatch_endcap','hTrkEta_tightmumatch_endcap',100,-2.5,2.5)
hTrkEta_tightgenmumatch = TH1F('hTrkEta_tightgenmumatch','hTrkEta_tightgenmumatch',100,-2.5,2.5)
hTrkEta_tightgenmumatch_barrel = TH1F('hTrkEta_tightgenmumatch_barrel','hTrkEta_tightgenmumatch_barrel',100,-2.5,2.5)
hTrkEta_tightgenmumatch_endcap = TH1F('hTrkEta_tightgenmumatch_endcap','hTrkEta_tightgenmumatch_endcap',100,-2.5,2.5)

hTrkPhi = TH1F('hTrkPhi','Track Phi',100,-3.14,3.14)
hTrkPt_tightelematch = TH1F('hTrkPt_tightelematch','hTrkPt_tightelematch',1000,0,10000)
hTrkPt_tightelematch_barrel = TH1F('hTrkPt_tightelematch_barrel','hTrkPt_tightelematch_barrel',1000,0,10000)
hTrkPt_tightelematch_endcap = TH1F('hTrkPt_tightelematch_endcap','hTrkPt_tightelematch_endcap',1000,0,10000)
hTrkPt_tightgenelematch = TH1F('hTrkPt_tightgenelematch','hTrkPt_tightgenelematch',1000,0,10000)
hTrkPt_tightgenelematch_barrel = TH1F('hTrkPt_tightgenelematch_barrel','hTrkPt_tightgenelematch_barrel',1000,0,10000)
hTrkPt_tightgenelematch_endcap = TH1F('hTrkPt_tightgenelematch_endcap','hTrkPt_tightgenelematch_endcap',1000,0,10000)
hTrkEta_tightelematch = TH1F('hTrkEta_tightelematch','hTrkEta_tightelematch',100,-2.5,2.5)
hTrkEta_tightelematch_barrel = TH1F('hTrkEta_tightelematch_barrel','hTrkEta_tightelematch_barrel',100,-2.5,2.5)
hTrkEta_tightelematch_endcap = TH1F('hTrkEta_tightelematch_endcap','hTrkEta_tightelematch_endcap',100,-2.5,2.5)
hTrkEta_tightgenelematch = TH1F('hTrkEta_tightgenelematch','hTrkEta_tightgenelematch',100,-2.5,2.5)
hTrkEta_tightgenelematch_barrel = TH1F('hTrkEta_tightgenelematch_barrel','hTrkEta_tightgenelematch_barrel',100,-2.5,2.5)
hTrkEta_tightgenelematch_endcap = TH1F('hTrkEta_tightgenelematch_endcap','hTrkEta_tightgenelematch_endcap',100,-2.5,2.5)

hTrkPixelDedx_tightmumatch = TH1F('hTrkPixelDedx_tightmumatch','hTrkPixelDedx_tightmumatch',300,0,30)
hTrkPixelDedx_tightmumatch_barrel = TH1F('hTrkPixelDedx_tightmumatch_barrel','hTrkPixelDedx_tightmumatch_barrel',300,0,30)
hTrkPixelDedx_tightmumatch_endcap = TH1F('hTrkPixelDedx_tightmumatch_endcap','hTrkPixelDedx_tightmumatch_endcap',300,0,30)
hTrkPixelDedx_tightgenmumatch = TH1F('hTrkPixelDedx_tightgenmumatch','hTrkPixelDedx_tightgenmumatch',300,0,30)
hTrkPixelDedx_tightgenmumatch_barrel = TH1F('hTrkPixelDedx_tightgenmumatch_barrel','hTrkPixelDedx_tightgenmumatch_barrel',300,0,30)
hTrkPixelDedx_tightgenmumatch_endcap = TH1F('hTrkPixelDedx_tightgenmumatch_endcap','hTrkPixelDedx_tightgenmumatch_endcap',300,0,30)
hTrkPixelDedxCalib_tightmumatch = TH1F('hTrkPixelDedxCalib_tightmumatch','hTrkPixelDedxCalib_tightmumatch',300,0,30)
hTrkPixelDedxCalib_tightmumatch_barrel = TH1F('hTrkPixelDedxCalib_tightmumatch_barrel','hTrkPixelDedxCalib_tightmumatch_barrel',300,0,30)
hTrkPixelDedxCalib_tightmumatch_endcap = TH1F('hTrkPixelDedxCalib_tightmumatch_endcap','hTrkPixelDedxCalib_tightmumatch_endcap',300,0,30)
hTrkPixelDedxCalib_tightgenmumatch = TH1F('hTrkPixelDedxCalib_tightgenmumatch','hTrkPixelDedxCalib_tightgenmumatch',300,0,30)
hTrkPixelDedxCalib_tightgenmumatch_barrel = TH1F('hTrkPixelDedxCalib_tightgenmumatch_barrel','hTrkPixelDedxCalib_tightgenmumatch_barrel',300,0,30)
hTrkPixelDedxCalib_tightgenmumatch_endcap = TH1F('hTrkPixelDedxCalib_tightgenmumatch_endcap','hTrkPixelDedxCalib_tightgenmumatch_endcap',300,0,30)

hTrkPixelDedx_tightelematch = TH1F('hTrkPixelDedx_tightelematch','hTrkPixelDedx_tightelematch',300,0,30)
hTrkPixelDedx_tightelematch_barrel = TH1F('hTrkPixelDedx_tightelematch_barrel','hTrkPixelDedx_tightelematch_barrel',300,0,30)
hTrkPixelDedx_tightelematch_endcap = TH1F('hTrkPixelDedx_tightelematch_endcap','hTrkPixelDedx_tightelematch_endcap',300,0,30)
hTrkPixelDedx_tightgenelematch = TH1F('hTrkPixelDedx_tightgenelematch','hTrkPixelDedx_tightgenelematch',300,0,30)
hTrkPixelDedx_tightgenelematch_barrel = TH1F('hTrkPixelDedx_tightgenelematch_barrel','hTrkPixelDedx_tightgenelematch_barrel',300,0,30)
hTrkPixelDedx_tightgenelematch_endcap = TH1F('hTrkPixelDedx_tightgenelematch_endcap','hTrkPixelDedx_tightgenelematch_endcap',300,0,30)
hTrkPixelDedxCalib_tightelematch = TH1F('hTrkPixelDedxCalib_tightelematch','hTrkPixelDedxCalib_tightelematch',300,0,30)
hTrkPixelDedxCalib_tightelematch_barrel = TH1F('hTrkPixelDedxCalib_tightelematch_barrel','hTrkPixelDedxCalib_tightelematch_barrel',300,0,30)
hTrkPixelDedxCalib_tightelematch_endcap = TH1F('hTrkPixelDedxCalib_tightelematch_endcap','hTrkPixelDedxCalib_tightelematch_endcap',300,0,30)

hTrkStripsDedx_tightmumatch = TH1F('hTrkStripsDedx_tightmumatch','hTrkStripsDedx_tightmumatch',300,0,30)
hTrkStripsDedx_tightmumatch_barrel = TH1F('hTrkStripsDedx_tightmumatch_barrel','hTrkStripsDedx_tightmumatch_barrel',300,0,30)
hTrkStripsDedx_tightmumatch_endcap = TH1F('hTrkStripsDedx_tightmumatch_endcap','hTrkStripsDedx_tightmumatch_endcap',300,0,30)
hTrkStripsDedx_tightgenmumatch = TH1F('hTrkStripsDedx_tightgenmumatch','hTrkStripsDedx_tightgenmumatch',300,0,30)
hTrkStripsDedx_tightgenmumatch_barrel = TH1F('hTrkStripsDedx_tightgenmumatch_barrel','hTrkStripsDedx_tightgenmumatch_barrel',300,0,30)
hTrkStripsDedx_tightgenmumatch_endcap = TH1F('hTrkStripsDedx_tightgenmumatch_endcap','hTrkStripsDedx_tightgenmumatch_endcap',300,0,30)
hTrkStripsDedxCalib_tightmumatch = TH1F('hTrkStripsDedxCalib_tightmumatch','hTrkStripsDedxCalib_tightmumatch',300,0,30)
hTrkStripsDedxCalib_tightmumatch_barrel = TH1F('hTrkStripsDedxCalib_tightmumatch_barrel','hTrkStripsDedxCalib_tightmumatch_barrel',300,0,30)
hTrkStripsDedxCalib_tightmumatch_endcap = TH1F('hTrkStripsDedxCalib_tightmumatch_endcap','hTrkStripsDedxCalib_tightmumatch_endcap',300,0,30)

hTrkStripsDedx_tightelematch = TH1F('hTrkStripsDedx_tightelematch','hTrkStripsDedx_tightelematch',300,0,30)
hTrkStripsDedx_tightelematch_barrel = TH1F('hTrkStripsDedx_tightelematch_barrel','hTrkStripsDedx_tightelematch_barrel',300,0,30)
hTrkStripsDedx_tightelematch_endcap = TH1F('hTrkStripsDedx_tightelematch_endcap','hTrkStripsDedx_tightelematch_endcap',300,0,30)
hTrkStripsDedx_tightgenelematch = TH1F('hTrkStripsDedx_tightgenelematch','hTrkStripsDedx_tightgenelematch',300,0,30)
hTrkStripsDedx_tightgenelematch_barrel = TH1F('hTrkStripsDedx_tightgenelematch_barrel','hTrkStripsDedx_tightgenelematch_barrel',300,0,30)
hTrkStripsDedx_tightgenelematch_endcap = TH1F('hTrkStripsDedx_tightgenelematch_endcap','hTrkStripsDedx_tightgenelematch_endcap',300,0,30)
hTrkStripsDedxCalib_tightelematch = TH1F('hTrkStripsDedxCalib_tightelematch','hTrkStripsDedxCalib_tightelematch',300,0,30)
hTrkStripsDedxCalib_tightelematch_barrel = TH1F('hTrkStripsDedxCalib_tightelematch_barrel','hTrkStripsDedxCalib_tightelematch_barrel',300,0,30)
hTrkStripsDedxCalib_tightelematch_endcap = TH1F('hTrkStripsDedxCalib_tightelematch_endcap','hTrkStripsDedxCalib_tightelematch_endcap',300,0,30)

hMuP = TH1F('hMuP','hMuP',1000,0,10000)
hMuPt = TH1F('hMuPt','hMuPt',1000,0,10000)
hMuEta = TH1F('hMuEta','hMuEta',100,-3,3)
hMuPhi = TH1F('hMuPhi','hMuPhi',100,-3.14,3.14)
hMuGamma = TH1F('hMuGamma','Muon Gamma',100,0,10000)
hMuBetaGamma = TH1F('hMuBetaGamma','Muon BetaGamma',100,0,10000)

hMuP_genmatch = TH1F('hMuP_genmatch','hMuP_genmatch',1000,0,10000)
hMuPt_genmatch = TH1F('hMuPt_genmatch','hMuPt_genmatch',1000,0,10000)
hMuEta_genmatch = TH1F('hMuEta_genmatch','hMuEta_genmatch',100,-3,3)
hMuPhi_genmatch = TH1F('hMuPhi_genmatch','hMuPhi_genmatch',100,-3.14,3.14)
hMuGamma_genmatch = TH1F('hMuGamma_genmatch','genmatched Muon Gamma',100,0,10000)
hMuBetaGamma_genmatch = TH1F('hMuBetaGamma_genmatch','genmatched Muon BetaGamma',100,0,10000)

hEleP = TH1F('hEleP','hEleP',1000,0,10000)
hElePt = TH1F('hElePt','hElePt',1000,0,10000)
hEleEta = TH1F('hEleEta','hEleEta',100,-3,3)
hElePhi = TH1F('hElePhi','hElePhi',100,-3.14,3.14)
hEleGamma = TH1F('hEleGamma','Electron Gamma',100,0,200000)
hEleBetaGamma = TH1F('hEleBetaGamma','Electron BetaGamma',100,0,10000)

hEleP_genmatch = TH1F('hEleP_genmatch','hEleP_genmatch',1000,0,10000)
hElePt_genmatch = TH1F('hElePt_genmatch','hElePt_genmatch',1000,0,10000)
hEleEta_genmatch = TH1F('hEleEta_genmatch','hEleEta_genmatch',100,-3,3)
hElePhi_genmatch = TH1F('hElePhi_genmatch','hElePhi_genmatch',100,-3.14,3.14)
hEleGamma_genmatch = TH1F('hEleGamma_genmatch','genmatched Electron Gamma',100,0,10000)
hEleBetaGamma_genmatch = TH1F('hEleBetaGamma_genmatch','genmatched Electron BetaGamma',100,0,10000)

hTrkP_charginomatch = TH1F('hTrkP_charginomatch','Chargino-matched track total momentum',1000,0,10000)
hTrkPt_charginomatch = TH1F('hTrkPt_charginomatch','Chargino-matched track transverse momentum',1000,0,10000)
hTrkEta_charginomatch = TH1F('hTrkEta_charginomatch','Chargino-matched track pseudo-rapidity',100,-2.5,2.5)
hTrkPhi_charginomatch = TH1F('hTrkPhi_charginomatch','Chargino-matched track phi',100,-3.14,3.14)

hTrkPixelDedx_charginomatch = TH1F('hTrkPixelDedx_charginomatch','Chargino-matched track pixel dedx',300,0,30)
hTrkPixelDedx_charginomatch_barrel = TH1F('hTrkPixelDedx_charginomatch_barrel','Chargino-matched track pixel dedx at barrel region',300,0,30)
hTrkPixelDedx_charginomatch_endcap = TH1F('hTrkPixelDedx_charginomatch_endcap','Chargino-matched track pixel dedx at endcap region',300,0,30)
hTrkPixelDedxCalib_charginomatch_barrel = TH1F('hTrkPixelDedxCalib_charginomatch_barrel','Chargino-matched track pixel dedx at barrel region',300,0,30)
hTrkPixelDedxCalib_charginomatch_endcap = TH1F('hTrkPixelDedxCalib_charginomatch_endcap','Chargino-matched track pixel dedx at endcap region',300,0,30)
hTrkStripsDedx_charginomatch = TH1F('hTrkStripsDedx_charginomatch','Chargino-matched track strips dedx',300,0,30)
hTrkStripsDedx_charginomatch_barrel = TH1F('hTrkStripsDedx_charginomatch_barrel','Chargino-matched track strips dedx at barrel region',300,0,30)
hTrkStripsDedx_charginomatch_endcap = TH1F('hTrkStripsDedx_charginomatch_endcap','Chargino-matched track strips dedx at endcap region',300,0,30)
hTrkStripsDedxCalib_charginomatch_barrel = TH1F('hTrkStripsDedxCalib_charginomatch_barrel','Chargino-matched track strips dedx at barrel region',300,0,30)
hTrkStripsDedxCalib_charginomatch_endcap = TH1F('hTrkStripsDedxCalib_charginomatch_endcap','Chargino-matched track strips dedx at endcap region',300,0,30)

hGenGluinoMass = TH1F('hGenGluinoMass','Gen-gluino mass', 2500, 0, 2500)
hGenStopMass = TH1F('hGenStopMass','Gen-stop mass', 2500, 0, 2500)
hGenLSPMass = TH1F('hGenLSPMass','LSP mass', 2500, 0, 2500)

hGenCharginoP = TH1F('hGenCharginoP','Gen-chargino total momentum',1000,0,10000)
hGenCharginoPt = TH1F('hGenCharginoPt','Gen-chargino transverse momentum',1000,0,10000)
hGenCharginoEta = TH1F('hGenCharginoEta','Gen-chargino pseudo-rapidity',100,-2.5,2.5)
hGenCharginoPhi = TH1F('hGenCharginoPhi','Gen-chargino phi',100,-3.14,3.14)

h2_Trk_P_vs_PixelDedx_charginomatch = TH2F('h2_Trk_P_vs_PixelDedx_charginomatch','chargino P vs pixel dEdx', 100,0,10000,100,0,30)
h2_Trk_P_vs_StripsDedx_charginomatch = TH2F('h2_Trk_P_vs_StripsDedx_charginomatch','chargino P vs strips dEdx', 100,0,10000,100,0,30)

