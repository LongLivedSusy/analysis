from ROOT import *
#from utilsII import *
import os, sys
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
#gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep
lumi = 35.9 #just for labeling. this weightw as already applied
#must agree with lumi in merged...py!
#lumi = 137.

makepdfs = True
datamc = 'data'# should pretty much always be this way
doblinding = True
dofakesidebandsubtraction = False

makePredictionMode = False
extrascale = 1.0
#extrascale = 137./35.9


grabasignal = False

tag = 'MaxAwesTrkEnPt30'
tag = '2ndTestPt10Short'
tag = 'ShortPt10NoDPhi'
tag = 'StraightenedOut'
tag = 'ViktorsLong'
tag = 'ClassicReversion'
tag = 'TryAgainJ2MakeSure'
tag = 'ClassicBut20'
tag = 'BabyStepAcrsTheRoom'
tag = 'SplitLSLowMvaMp5'
tag = 'ViktorAtLast'
tag = 'ViktorTighterPh0L'
tag = 'VikTighterPh0LBmp6'
tag = 'VikTighterPh0LBmp5'
tag = 'VikTighterEdP5FxSb'
tag = 'KlassikP5FxSb'
tag = 'KlassikKlassic'
tag = 'FirstWithCharged'
tag = 'TryPiOver2'
tag = 'TightViktorPiO2'
tag = 'TightViktorEdep18'
tag = 'AataViktorEdep20'
tag = 'LooserBdtViktorEdep20'
tag = 'ReLsrBdtViktorEdep20'
tag = 'SmFxLsrBdtVikEdep20'
tag = 'BkToDp23LBdtVEdep20'
tag = 'BasicFixDp23LBVdep20'
tag = 'ViktagDp23LBVdep12'
tag = 'ViktagDp23LBVdep10'
tag = 'VtgDp23MBVdep15Sbt'
tag = 'Exo'
tag = 'LoosePlus10ECal15'
tag = 'Lp10Lmp1ECal15'
tag = 'Lpp1Lmp1ECal15P'
tag = 'BdtNoEdepECal15'
tag = '1BdtNoEdep4pECal15'
tag = '1BdtNoed4prECal15Pt'
tag = '1BdtNoed4prEc15PtLfb'
tag = '1BdtNoedEc15Pt40'
tag = '1BdtNoedE15Pt40Loose'
tag = '1BNoedPt40LsnLsr'
tag = 'Intuitive1Dedx5Pt40'
tag = 'Intuitive1Dedx5Pt75'
tag = 'BackHomeDedx4Pt30'
tag = 'BHoDx4p5Pt100TFkDphi'
tag = 'Dx4p5Pt100TFkDphiPrEta'
tag = 'Dx45Pt100DphiPrEtaJV'
tag = 'Dx45Pt100DphiPrEtaMoPt'
tag = 'Dx45Pt100MoPtNrmBNpu'
tag = 'Dx45Pt100MoPtNrmBNumsk'
tag = 'Dx45Pt75MoPtNrmBNumsk'
tag = 'Dx45Pt75MoPtNrmBEta2p2'
tag = 'Dx45Pt30MoPtNrmBEta2p2'
tag = 'Dx45Pt30MoPtJVEta2p2'
tag = 'Dx45Pt30MoPtJVEta2p2Mu'
tag = 'Dx45Pt30JVEta2p2Mu2'
tag = 'Dx45Pt30JVEt2p2Mu2WdMv'
tag = 'Dx45Pt30JVEt2p2MuFlgen'
tag = 'Dx45Pt30JVEt2p2ExclMu'
tag = 'Dx45Pt30MoPtJVEta2p1'
tag = 'Dx45Pt40MoPtJVEta2p1'
tag = 'Dx4Pt40MoPtJVEt2p1Nopi'
tag = 'Dx4Pt40MoPtJVEt2p1Pi'
tag = 'Dx4Pt40MoPtJVEt2p1Gfx'
tag = 'Dx4Pt40MoPtJV2p1Nopimu'
tag = 'Dx4Pt40Et2p1onlFJV10p6'
tag = 'Dx4Pt40Et2p1onlFJV15p6'
tag = 'Dx4Pt40Et2p1JV10p6'
tag = 'Dx4Pt40Et2p1JV10p6NoTrw'
tag = 'Dx4Pt40Et2p1JVFkVsEt'
tag = 'Dx4Pt40Et2p1JVFkVfewEt'
tag = 'Dx4Pt40Et2p4JVFkVfewEt'
tag = 'Dx4Pt40Et2p2JVFkVfewEt'
tag = 'Dx4Pt40Et2p2JVPrVfewPt'
tag = 'Dx4Pt40Et2p2JVDdxMin'
tag = 'Dx4Pt40Et22JVDxmnNuMsk'
tag = 'Dx4Pt40Et22JVCoarsrFR'
tag = 'Dx4Pt40Et22JVMindphib'
tag = 'Dx4Pt40Et22JVMindphij'
tag = 'Dx4Pt40Et22NoJV'
tag = 'Dx4Pt40Et22NoJVTtnShrt'
tag = 'Dx4Pt40Et22JVdnTtnShrt'
tag = 'Dx4Pt40Et22JVdnTtShrt'
tag = 'Dx4Pt40Et22JVdnTtShPdf'
tag = 'Dx4Pt40Et22JVdnTShPdf'
tag = 'Dx4Pt40Et22Jan2021b'
tag = 'Dx4Pt40Jan2021geq1b'
tag = 'Dx4Pt40J21geq1bLsrEdp'
tag = 'Dx4Pt40J21LsrEdpJndPt'
tag = 'J21LsrEdpJndPtLsrb4Mc'
tag = 'J21LsrEdpLsrbd4mcNow'
tag = 'J21LsrEdpLsrb4mcFkhlf'
tag = 'J21LsrEdpLsrb4mcFkonly'
tag = 'J21LsrEdpLsrb4mcFkonly'
tag = 'J21LsrEdpLssrb4mcFknly'
tag = 'J21LsrEdpLssrb4mc'
tag = 'J21LsrEdpLssrb4mcFo2'
tag = 'J21LsrEdpLssrb4mcBk2b'
tag = 'Dx4Pt40Et22LsrEdpJndPt'
tag = 'Dx4Pt40Et22LsrEdpMrPtaf'
tag = 'Dx4Pt40Et22LsrEdMrMcwts'
tag = 'Dx4Pt40Et22Calm40MrMcwts'
tag = 'Dx4Pt40Et22Calm40MrMcnow'
tag = 'Dx4Pt40Et22ed40Two2bins'
tag = 'Dx4Pt40Et22ed40TwobinMnb'
tag = 'Dx4Pt40Et22ed40Two2Nof2'
tag = 'Dx4Pt40Et22ed40Two2sampt'
tag = 'Dx4Et22ed40Two2actsampt'
tag = 'Dx4Et22ed40Two3Hemv'
tag = 'Dx4Et22ed40Two3HvIronout'
tag = 'Dx4Et22ed40Two3HvIronagn'
tag = 'Dx4Et22ed40Two3HvIron3'
tag = 'Dx4Et22ed40Two3HvPinPt'
tag = 'Dx4Et22ed40Two3Hv2bin'
tag = 'Dx4Et22Two3Hv2bin2'
tag = 'Dx4Et22Two3Hv2bin2chns'
tag = 'Dx4Et22Two3Hv2bin2numsk'
tag = 'Dx4Et22SmearPhase1nom'
tag = 'Dx4Et22SmearPhase1drop1'
tag = 'Dx4Et22SmearPhase1nomagain'
tag = '2021_02_23bweights'
tag = '2021_02_23a_ttbar'
tag = '2021_02_23c_tightenFbdt'
tag = '2021_02_23d_tightenFbdtmore'
tag = '2021_02_23d_tightenBoth'
tag = '2021_02_23d_loosenMainBdt'
tag = '2021_02_23e_lsnMainBMore'
tag = '2021_02_23f_lsnMnCnsntBning'
tag = '2021_02_23g_lsnMnEvnLsr'
tag = '2021_02_23g_1morePtBin'
tag = '2021_02_23h_evenhigherpt'
tag = '2021_02_24h_highnreal'
tag = '2021_02_24h_etaLT2p0'
tag = '2021_02_24h_etaLT2p0Pt225'
tag = '2021_02_24h_etaLT2p0Met250'
tag = '2021_02_24h_eta2Met150WHnj'
tag = '2021_02_24h_etaStraightJacket1p8'
tag = '2021_02_25h_etaStrtJckt1p8HiMet'
tag = '2021_02_25h_etaStrtJcktOpnUpFk'
tag = '2021_02_26a_etaStrtJcktOpnMorePt'
tag = '2021_02_26b_etaStrtJcktOpnMorePt'
tag = '2021_02_26b_fakeonly'
tag = '2021_02_26b_nomuonnopi'
tag = '2021_02_26b_jetpt15'
tag = '2021_02_28a_nopion'
tag = '2021_02_28a_justpion'
tag = '2021_02_28a_justpion2'
tag = '2021_02_28b_stdMtautau'
tag = '2021_03_1a_includeInclusive'
tag = '2021_03_1b_nomuon'
tag = '2021_03_1b_pipi'
tag = '2021_03_1b_isgenpi'
tag = '2021_03_2_matchedjeten'
tag = '2021_03_2_mcalo30to200mdpGTp3'
tag = '2021_03_2_mcalo30to200ttnMvaL'
tag = '2021_03_2_mcalo30to300EdgeUpPrMva'
tag = '2021_03_2_mcalo30to300tweak2'
tag = '2021_03_2_mcalo30to300Ege2'
tag = '2021_03_2_finededx'
tag = '2021_03_2_moreThanEdge'
tag = '2021_03_2_justTry2makesense'
tag = '2021_03_2_vlooseMcal'
tag = '2021_03_4_tweakMva'
tag = '2021_03_4_tightenPromptMva'
tag = '2021_03_4_flushPromptLsEta'
tag = '2021_03_4_lsnMcal4fksLsnBdt4fks'
tag = '2021_03_4_fixshorthighnjet'
tag = '2021_03_4_deanglifyPromptFake'
tag = '2021_03_4_update2dedx'
tag = '2021_03_4_try4ratioerror'
tag = '2021_03_5_frankensteinEmerges2'
tag = '2021_03_5_mcmcalh80'
tag = '2021_03_5_mcmcalh40'
tag = '2021_03_5_afterMcmcalh40'
tag = '2021_03_5_mcmcalh60'
tag = '2021_03_5_mcmcalh40again'
tag = '2021_03_5_mcmcalh60again'
tag = '2021_03_5_mcmcal20to80'
tag = '2021_03_8_mcmcal20to60'
tag = '2021_03_8_mcmcal20to60crsept'
tag = '2021_03_8_mcmcal23to60'
tag = '2021_03_8_mcal23to60flush'
tag = '2021_03_8_mcal30to60flush'
tag = '2021_03_8_mcal25to60flush'
tag = '2021_03_8_mcal25to60pio3'
tag = '2021_03_9_mcal25to60LsnLsBmcp5'
tag = '2021_03_9_mcal25to60LsnFlnP'
tag = '2021_03_9_mcal60to150'
tag = '2021_03_10_do2mcAs2data'
tag = '2021_03_9_mcal25to150LsnFlnP'
tag = '2021_03_11_mcal25to90LsnFlnP'
tag = '2021_03_11_mcal30to90LsnFlnP'
tag = '2021_03_11_mcal30to60tttf1bs'
tag = '2021_03_11_mcal30to60tweakin'
tag = '2021_03_15_mcal30to60revamp'
tag = '2021_03_15_mcal30to60revamp3'
tag = '2021_03_15_mcal25to90revamp'
tag = '2021_03_15_mcal25to80pt60'
tag = '2021_03_16_mcl25to80pt60bfkmc'
tag = '2021_03_17_mcl30_reprocess'
tag = '2021_03_18_mcl30_mcdatasame'
tag = '2021_03_18_mcl30_afterspotbug'
tag = '2021_03_19_narrowworld'
tag = '2021_03_19_narrow4quality'
tag = '2021_03_19_narrow4qualLssfFxMet'
tag = '2021_03_19_narrow4qual2ddx0'
tag = '2021_03_23_mcal35hcal80'
tag = '2021_03_23_mcal30hcal80'
tag = '2021_03_23_mcal30hcal90'
tag = '2021_03_23_mcal30hcal80'
tag = '2021_03_23_mcal25hcal75'
tag = '2021_03_23_mcal25hcal60'
tag = '2021_03_23_mcal25hcal50'
tag = '2021_03_23_mcal25hcal50TtnFklBdt'
tag = '2021_03_23_mcal25hcal40'
tag = '2021_03_23_mcal23hcal30'
tag = '2021_03_23_mcal18hcal25'
tag = '2021_03_23_mcal18hcal25ttnall'
tag = '2021_03_23_mcal18hcal25tnlndphiph1'
tag = '2021_03_25_exploreMc'
tag = '2021_03_25_exploreMcNoPi'
tag = '2021_03_25_exploreMcNoPiNoMu'
tag = '2021_03_25_exploreBuildUpPt'
tag = '2021_03_25_exploreAdjustDatMht'
tag = '2021_03_25_explorAdjstLsnFkLng'
tag = '2021_03_25_explorJuiceFkLng'
tag = '2021_03_25_explorMcWeights'
tag = '2021_03_25_explorMcNoWNj3'
tag = '2021_03_25_Nj3_mcm25tomch40'
tag = '2021_03_25_Nj3_mcm30tomch60'
tag = '2021_03_25_Nj3_mcm40tomch70'
tag = '2021_03_25_Nj3_mcm50tomch120'
tag = '2021_03_25_Nj3_mcm40tomch100'
tag = '2021_03_25_Nj3_mcm40mch100lsnFs'
tag = '2021_03_25_Nj3_mcm40mch90lsnFs'
tag = '2021_03_25_Nj3_mcm40mch90ttns'
tag = '2021_03_25_Nj3_mcm40mch90tnlnfs'
tag = '2021_03_25_Nj3_mcm40mch90linShort'
tag = '2021_03_25_Nj3_mcm40mch90linrzed'
tag = '2021_03_25_Nj3_mcm40mch90lin2'
tag = '2021_03_25_Nj3_mcm40mch90lin3'
tag = '2021_03_29_Nj3_mcm40mch90lin4'
tag = '2021_03_29_Nj3_mcm40mch90lin5'
tag = '2021_03_30_l61stw2thrds'
tag = '2021_03_29_Nj3_mcm40mch90lin6'
tag = '2021_03_30_Nj3_mcm40mch90lin7'
tag = '2021_03_30_Nj3_newloose2'
tag = '2021_03_30_Nj3_newloose3'
tag = '2021_03_30_Nj3_newloose4'
tag = '2021_03_30_Nj3_newloose5'
tag = '2021_03_30_Nj3_newloose6'
tag = '2021_03_30_Nj3_newloose8'
tag = '2021_03_30_Nj3_newloose10'
tag = '2021_03_30_Nj3_newloose11'
tag = '2021_03_30_Nj3_NoResetPh1'
tag = '2021_03_30_Nj3_YesResetPh1'
tag = '2021_03_30_Nj3_55to105'
tag = '2021_03_30_Nj3_55to105ttn17'
tag = '2021_03_30_Nj3_55to105ttn2'
tag = '2021_03_30_Nj3_55to105ttn3'
tag = '2021_04_10_Nj3_45to85'
tag = '2021_04_10_Nj3_45to65'
tag = '2021_04_10_Nj3_homeAtLast'
tag = '2021_04_10_Nj3_thiknup'
tag = '2021_04_10_Nj3_ripen4mc1'
tag = '2021_04_10_Nj3_reskim'
tag = '2021_04_11_Nj3_makeDPhiSmler'
tag = '2021_04_11_Nj3_makeCrBigr2'
tag = '2021_04_11_Nj3_lrgCrLsnSr'
tag = '2021_04_11_Nj3_LsnSrRdcCnt'
tag = '2021_04_11_Nj3_LsnSrCmprms'
tag = '2021_04_11_Nj3_Comp2'
tag = '2021_04_11_Nj3_Comp3'
tag = '2021_04_11_Nj3_Comp4'
tag = '2021_04_11_Nj3_Comp5b'
tag = '2021_04_11_Nj3_Comp6'
tag = '2021_04_11_Nj3_Comp7'
tag = '2021_04_11_Nj3_Comp8'
tag = '2021_04_11_Nj3_Comp9'
tag = '2021_04_14_Tbdt0p5'
tag = '2021_04_14_Tbdt0p1'
tag = '2021_04_14_Tbdt0p15'
tag = '2021_04_15_Try2MaxOnp7'
tag = '2021_04_15_LsnLngsAgn'
tag = '2021_04_15_BrngBalance'
tag = '2021_04_16_TtnShrtAbit'
tag = '2021_04_16_Titrate'
tag = '2021_04_16_Titrate2'
tag = '2021_04_16_SupposedBest'
tag = '2021_04_16_BestBut0p1'
tag = '2021_04_16_0p1GetTight'
tag = '2021_04_16_0p1GetTighten2'
tag = '2021_04_16_0p05GetTighten2'#JUST SET THIS	 up for tomorrow
tag = '2021_04_16_0p05Mc40to60'
tag = '2021_04_16_0p05Mc45to75'
tag = '2021_04_16_0p05Mc45to95'
tag = '2021_04_16_0p05Mc45to100'
tag = '2021_04_19_0p05Mc45to95'
tag = '2021_04_19_0p05Mc45to90'
tag = '2021_04_20_Mc45to90mvaLm1'
tag = '2021_04_21_0p0Mc45to90Lmvm1'
tag = '2021_04_21_0p0Mc35to90Lmvm1'
tag = '2021_04_21_0p0Mc30to90Lmvm1'
tag = '2021_04_21_0p0Mc30to90tryagain'
tag = '2021_04_21_TghtMc25to50'
tag = '2021_04_21_TghtMc25to50ttnfk'
tag = '2021_04_21_TghtMc25to50taf'
tag = '2021_04_21_TghtMc25to50tbl'
tag = '2021_04_21_TghtMc25to50twk'
tag = '2021_04_21_Bk2bestAttemptFail1'
tag = '2021_04_21_Bk2bestAttempt2'
tag = '2021_04_21_Bk2bestAttempt2p0'
tag = '2021_04_21_BgrStepMc25to90'
tag = '2021_04_21_BgrStepMc25to90wts'
tag = '2021_04_21_TghtMc15to25to90'
tag = '2021_04_21_TghterMc15to25to90'
tag = '2021_04_22_RefineMc15to25to90'
tag = '2021_04_22_B4teachMc15to25to90'
tag = '2021_04_22_PostmeetMc15to25to90'
tag = '2021_04_22_TUpTfMc15to25to90'
tag = '2021_04_22_MkPredMc15to25to90'
tag = '2021_04_22_Mc15to50toUp'
tag = '2021_04_22_Mc15to30toUp'
tag = '2021_04_22_Mc15to60for16'
tag = '2021_04_22_Mc15to60for16finegrain'
tag = '2021_04_22_Mc15to60for16Short25'
tag = '2021_04_29_Short25lottaeta'
tag = '2021_04_29_Shortfrptbinned'
tag = '2021_04_29_Shortfrfineptbinned'
tag = '2021_04_29_ShortfrfineHighPt3'
tag = '2021_04_29_ShortfrfineHighPt4'
tag = '2021_04_29_ShortfrfineHighPt5'
tag = '2021_04_29_ShortfrfineHighPt6'
tag = '2021_05_1_Back2Sea'
tag = '2021_05_1_QuarterPrompt'
tag = '2021_05_1_QuarterPromptEtafk'
tag = '2021_05_1_Enlarge2016FakeCr'
tag = '2021_05_1_EdgeFakeCr'
tag = '2021_05_1_EdgeFakeCrHalfPrshrt'
tag = '2021_05_1_EdgeFakeCrQuarterPrshrt'
tag = '2021_05_1_EdgeFakeSmash'
tag = '2021_05_3_EdgeFakeQuarter'
tag = '2021_05_3_EdgeFkThrdPurifyMc'
tag = '2021_05_3_EdgeFkReallyPurifyMc'
tag = '2021_05_3_EdgeFkReallyPurMc55'
tag = '2021_05_3_EdgeFkReallyPurMc60to75'
tag = '2021_05_3_EdgeFkReallyPurMc65to110'
tag = '2021_05_3_EdgeFkMc65to110NoPiNoMu'
tag = '2021_05_3_EdgeFkMc65to110Add25'
tag = '2021_05_3_EdgeFkMc65to110Add25b'
tag = '2021_05_3_EdgeFkMc65to110Rummage'
tag = '2021_05_3_EdgeFkMc65to110ot2twot'
tag = '2021_05_3_EdgeFkMc65to110LooseFk'
tag = '2021_05_3_EdgeFkMc65to110PtDep'
tag = '2021_05_3_EdgeFkMc65to110MinDrJet'
tag = '2021_05_6_MinDrLJetTfkL2' ##to dooooo
tag = '2021_05_6_MinDrLJetTfkL20'
tag = '2021_05_6_MinDrLJetTfkL15'
tag = '2021_05_6_NotJet15'
tag = '2021_05_6_NotJet15mc20forLs'
tag = '2021_05_6_TightJetIsoCombMc20forLs'
tag = '2021_05_6_TighterJetIsoCombMc20forLs'
tag = '2021_05_6_TighterJetIsoCombFkEta'
tag = '2021_05_6_TighterJetIsoCombTtrFkEta'
tag = '2021_05_6_TighterJetIsoComb2TtrFkEta'
tag = '2021_05_6_TighterJetIsoComb2TtrFkEtaNoPr'
tag = '2021_05_7_TtrJetIsoTwkThtaKpaAdd19rc1'
tag = '2021_05_7_TtrJetIsoTwkThtaKpa2'
tag = '2021_05_7_TtrJetIsoTwkThtaKpaPuweights'
tag = '2021_05_8_TtrJetIsoTwkThtaKpaPuwtsFkEta'
tag = '2021_05_8_TtrJetIsoTwkShortFrac'
tag = '2021_05_8_TtrJetIsoTwkShortFracTt'
tag = '2021_05_9_LsrJetIsoTtnShortFrac'
tag = '2021_05_9_LsrJetIsoTtnDropSmDr'
tag = '2021_05_9_LsrJetIsoTtnPrmptShrt'
tag = '2021_05_9_LsrNarrowJetVeto10TtnPs'
tag = '2021_05_9_PureStat'
tag = '2021_05_9_LsrNrw0p3JetVeto10Mtv1'
tag = '2021_05_9_LsrNrw0p3JetVeto10Mtv2'
tag = '2021_05_9_LsrNrw0p3JetVeto10Mtv3'
tag = '2021_05_10_ReinstateDphi2'
tag = '2021_05_10_ReinstateDphi3'
tag = '2021_05_10_ReinstateDphi3TuneUp'
tag = '2021_05_10_ReinstateDphi4TuneUpNoPrompt'
tag = '2021_05_10_ReinstateDphi4TuneUpEta2p0'
tag = '2021_05_11_IncludeBin47Eta2p0'
tag = '2021_05_11_IncludeBin47Eta2p0NoPrompt'
tag = '2021_05_11_ReinstatePromptPt'
tag = '2021_05_11_ReinstatePromptPtTtn1'
tag = '2021_05_11_ReinstatePromptPtTtn2'
tag = '2021_05_11_ReremovePromptPt'
tag = '2021_05_11_ThatTookAWhileDropShrtFrac'
tag = '2021_05_11_ThatTookAWhileDropShrtFrac2'
tag = '2021_05_12_ReinstateShrtFrac0p05'
tag = '2021_05_12_ReinstateShrtFrac15b'
tag = '2021_05_12_ReinstateShrtFrac15wB23'
tag = '2021_05_12_ReinstateShrtFrac15ttn'
tag = '2021_05_12_RemoveFracTrimShortPr'
tag = '2021_05_12_RemoveFracTrimShortPr2'
tag = '2021_05_13_MCalFracHybridMax'
tag = '2021_05_13_ReinstateNonFrac15'
tag = '2021_05_13_RereinstateHybrid15'
tag = '2021_05_13_RereinstateHybrid15Flushish'
tag = '2021_05_13_ReHyb15FlushishDPhi0p3thingB'
tag = '2021_05_13_ReHyb15TightenFakeCrsB'
tag = '2021_05_13_RestoreHybrid15Attempt1'
tag = '2021_05_13_Hybrid20'
tag = '2021_05_13_Hybrid20b'
tag = '2021_05_13_Hybrid20Eta2p2'
tag = '2021_05_13_Hybrid20EtaTtnMtDt'
tag = '2021_05_13_Hybrid15Eta2p2'
tag = '2021_05_13_Hybrid15Eta2p1Ht0'
tag = '2021_05_13_Hybrid15Eta2p1Ht0TtnFkPh1'
tag = '2021_05_13_Hybrid15Eta2p1Ht0TtnFkPh1JI'
tag = '2021_05_13_Hybrid15Eta2p1Ht0JI0p2Still2lse'
tag = '2021_05_13_Hybrid15Eta2p1Ht0JI0p2Rfnd3'
tag = '2021_05_13_Hybrid15Eta2p1Prize'
tag = '2021_05_13_Hybrid15Eta2p1Lsn2Accomodate1'
tag = '2021_05_13_Hybrid15Eta2p1Ht0JI0p2Rfnd2'
tag = '2021_05_13_Hybrid15Eta2p1Ht0JI0p2Rfnd1'
tag = '2021_05_17_Hybrid15Eta2p1Prize'
tag = '2021_05_17_Hybrid15Eta2p1Ht0JI0p2'
tag = '2021_05_17_Hybrid15Eta2p0JI0p3'
tag = '2021_05_17_Hybrid15Eta2p0JI0p3NoDphiTwk'
tag = '2021_05_17_Hybrid15Eta2p0JI0p3TtnPh1Sh'
tag = '2021_05_17_Hybrid15Eta2p0JI0p3TtnPh1ShNoStat'
tag = '2021_05_17_Hybrid15Eta2p0JI0p3TtnPh1ShMcal'
tag = '2021_05_19_Hybrid15Eta2p0OldJITtnPh1ShMcal'
tag = '2021_05_17_Hybrid15Eta2p0JI0p3TtnPh1ShMt10'
tag = '2021_05_17_Hybrid15Eta2p0dddLs16PshJI30b'
tag = '2021_05_17_Hybrid15Eta2p0dddLs16PshJI30d'
tag = '2021_05_17_MaxHybridJILowKappaNoStat'
tag = '2021_05_21_MaxHybridLowKappaAllNoStat'
tag = '2021_05_21_MaxHybridLowKappaLongNoStat'
tag = '2021_05_21_MaxHybridLowKappaLongWithStat'
tag = '2021_05_21_MaxHybridLowKappaLongEta2p2' 
tag = '2021_05_21_MaxHybridEta2p0StatBox'
tag = '2021_05_21_MaxHybridEta2p0LepPt40'
tag = '2021_05_21_MaxHybridEta2p0LepPt40Met30'
tag = '2021_05_21_MaxHybridEta2p0LepPt40NoJetOnLL'
tag = '2021_05_21_MaxHybridEta2p0LepPt40NoJetOnLL5bins'
tag = '2021_05_21_MaxHybridEta2p0LepPt40TtnUp'
tag = '2021_05_21_MaxHybridEta2p0LepPt40Ht60NoJet'
tag = '2021_05_21_MaxHybridEta2p0LepPt40Ht60Dagger'
tag = '2021_05_21_MaxHybridEta2p0LepPt40Ht60DaggerNoMu'
tag = '2021_05_21_MaxHybridEta2p0LepPt40Ht60McalShort20'
tag = '2021_05_21_MaxHybridEta2p0_2020RmvContam2'
tag = '2021_05_21_MaxHybridEta2p0_2020RmvContam3Stat'
tag = '2021_05_21_MaxHybrid_2010RmvContam3LowerThtaL'
tag = '2021_05_21_MaxHybrid_2010RmvContam3MtGt30b'
tag = '2021_05_21_MaxHybrid_2020RmvCntm3Mdp0p3'
tag = '2021_05_21_MaxHybrid_2020RmvCntm3Mdp0p0'
tag = '2021_05_21_MaxHybrid_2020RmvCntm3HotSpot2'
tag = '2021_05_21_MaxHybrid_2020RmvCntm3Pt60'
tag = '2021_05_21_MaxHybrid_2020RmvCntm3PtLrgKpa'
tag = '2021_05_21_MaxHybrid_2020RmvCntm3PtSmallKpa2'
tag = '2021_05_21_MaxHybrid_2020RmvCntm3PtSmallKpa2Mdp0p3'
tag = '2021_05_21_MaxHybrid_2020RmvCntm3PtSmallKpa2Mdp0p0'
tag = '2021_05_30_NewBdtNoSigWeithgs'
tag = '2021_05_30_NewBdtNoSigWeithgs2'
tag = '2021_05_30_NewBdtNoSigWeithgs2NoMu'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4NoPrompt'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4InvertStack'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4LsnFall17b'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4PtFR'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4OneBinFrTtn'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4EtaFR'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4TidyUp'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4WideBveto'
tag = '2021_05_30_NewBdtNoSigWeightsHardDr0p4LepDr'
tag = '2021_06_2_NewBdtNoSigWeightsHardDr0p4Tune'
tag = '2021_06_2_NewBdtNoSigWeightsHardDr0p4FinePt'
tag = '2021_06_2_NewBdtNoSigWeightsHardDr0p4FlushFk'
tag = '2021_06_4_BdtNoWghtsNoNPix4Short'
tag = '2021_06_4_BdtNoWghtsNoNPix4ShortGiveAShot'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortFewBins'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortManyEtaBins'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullBkP1Fk'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullBkP1Fk2'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullBkP1Fk3'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullBkP1Fk4'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullFkPt'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullFkPt2'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullFkPt3'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullFkPt4'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullLoosePrmpt'
tag = '2021_08_4_BdtNoWghtsNoNPix4ShortOneBinPullVVLoosePrmpt'
tag = '2021_13_6_Use2016PixelBdt42017b'
tag = '2021_13_6_Use2016PixelBdt42017c'
tag = '2021_13_6_Use2016PixelBdt42017d'
tag = '2021_17_6_Use2016PixelBdta'
tag = '2021_17_6_Use2016PixelBdtFakeHt'
tag = '2021_17_6_Use2016PixelBdtFakeHtMoveSB'
tag = '2021_17_6_Use2016PixelBdtFakeHtThrowADPhiOnThere'
tag = '2021_17_6_Use2016PixelBdtFakeHtThrowADPhiOnThereb'
tag = '2021_17_6_Use2016PixelBdtFakeHtThrowADPhiOnTherec'
tag = '2021_17_6_Use2016PixelBdtFakeHtMoveCloser'
tag = '2021_17_6_Use2016PixelBdtFakeHtMoveEvenCloser'
tag = '2021_20_7_Jun20b'
tag = '2021_20_7_Jun20bnomu'
tag = '2021_20_7_Jun20EtaFixNoMu'
tag = '2021_20_7_Jun20TuneStuff'
tag = '2021_28_7_jul21Ootb'
tag = '2021_28_7_jul21OHighMet16'
tag = '2021_28_7_jul21NewMask'
tag = '2021_28_7_jul21NewMaskMet450'
tag = '2021_28_7_jul21NewMaskMet450NoPi'
tag = '2021_28_7_jul21NewMaskMet450NoPiNoMu'
tag = '2021_28_7_jul21NewMaskMet450NoPiNoMuNoE'
tag = '2021_28_7_jul21NewMaskMet450OnlyFake'
tag = '2021_28_7_jul21NewMaskMet450OnlyFakeM2'
tag = '2021_28_7_jul21NewMaskMet450OnlyFakeM3'
tag = '2021_28_7_jul21NewMaskMtDtMet20'
tag = '2021_28_7_jul21NewMaskMtDtMet20NoMu'
tag = '2021_28_7_jul21NewMaskMtDtMet20NoShrtPrmpt2'
tag = '2021_28_7_jul21NewMaskMtDtMet20ReinstatePrmpt'
tag = '2021_28_7_jul21NewMaskMtDtMet20MtDtMht40'
tag = '2021_28_7_jul21NewMaskMtDtMet40AdjstFkSh'
tag = '2021_28_7_jul21NewMaskMtDtMet40AdjstBoth'

tag = '2021_28_7_24Oct2021'
tag = '2021_28_7_25Oct2021'
tag = '2021_28_7_26Oct2021'
tag = '2021_28_7_26Oct2021b'
tag = '2021_28_7_26Oct2021c'
tag = '2021_28_7_27Oct2021'
tag = '2021_28_7_27Oct2021b'
tag = '2021_27_7_Oct2021c'
tag = '2021_31_Oct2021'
tag = '2021_31_Oct2021b'
tag = '2021_31_Oct2021c'
tag = '2021_31_Oct2021d'
tag = '2021_1_Nov2021'
tag = '2021_1_Nov2021b'
tag = '2021_1_Nov2021c'
tag = '2021_2_Nov2021'
tag = '2021_2_Nov2021b'
tag = '2021_2_Nov2021c'
tag = '2021_3_Nov2021'
tag = '2021_3_Nov2021b'
tag = '2021_3_Nov2021c'
tag = '2021_4_Nov2021'
tag = '2021_4_Nov2021b'
tag = '2021_5_Nov2021'
tag = '2021_5_Nov2021b'
tag = '2021_8_Nov2021b'
tag = '2021_8_Nov2021bad'
tag = '2021_10_Nov2021'
tag = '2021_12_Nov2021'
tag = '2021_13_Nov2021'
tag = '2021_13_Nov2021b'
tag = '2021_14_Nov2021'
tag = '2021_15_Nov2021e'
tag = '2021_15_Nov2021f'
tag = '2021_16_Nov2021'
tag = '2021_16_Nov2021b'


'''
rm -rf pdfs/Validation/prompt-bkg/* 
python tools/makeValidationPlots2methods.py Summer16 MC & 
python tools/makeValidationPlots2methods.py Phase1 &
python tools/makeValidationPlots2methods.py Fall17 MC &
python tools/makeValidationPlots2methods.py Run2016 &



python tools/makeValidationPlots2methods.py 2017
python tools/makeValidationPlots2methods.py 2018

#after all this, you can do
hadd -f predictionRun2.root Valid_yearRun2016.root Valid_yearPhase1.root
cp predictionRun2.root /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v4PtDe75dx5twoNoJV/Background
'''

try: year = sys.argv[1]
except:
	year = 'Run2016'
	year = 'Run2017'
	year = 'Run2018'
	year = 'RunPhase1'	
	year = 'Summer16'	
	
try: datamc = sys.argv[2].lower()
except: datamc = 'data'

isdata = bool(datamc=='data')
if not isdata: doblinding = False


#binning['MatchedCalo'] = [120,0,60]
binning['DtStatus'] = [6,-3,3]
binning['FakeCrNr'] = [6,-3,3]

redoBinning = binning
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
#redoBinning['DeDxAverage'] = [1.999999999,2,3.0,4.0,5.0,6.0,7.0]
#redoBinning['DeDxAverage'] = [1.999999999,2,4.0,10.0]
redoBinning['DeDxAverage'] = [-0.000001,0,4.0,10.0]
#redoBinning['InvMass'] = [15,50,170]
##redoBinning['InvMass'] = [50,0,200]
#redoBinning['InvMass'] = [24,60,180]
redoBinning['ElPt'] = [30,0,300]
redoBinning['Ht']=[5,0,2000]
redoBinning['Met'] = [20,0,600]
redoBinning['Mht'] = redoBinning['Met']
redoBinning['TrkEta']=[30,0,3]
#redoBinning['NJets'] = [6,1,7]
#redoBinning['NJets'] = [0.999999,1,3,6]
redoBinning['BTags'] = [-0.0000000001,0,1,4]
#redoBinning['LepMT'] = [7,15,150]
redoBinning['BinNumber'] = binningAnalysis['BinNumber']
#redoBinning['MatchedCalo'] = [0,10,13,23,40]
#redoBinning['InvMass'] = [25,0,200]#same as analysis

makefolders = False


calm = 20
calh = 25

calm = 10
calh = 15

calm = 17
calh = 27

calm = 20
calh = 60

calm = 20
calh = 80

call = 12
calm = 12
calh = 80

#calm = 20
#calh = 30


if year=='Run2017': lumi = 41.8
if year=='Run2018': lumi = 55.0
if year=='Phase1': lumi = 41.8+55.0

mainfilename = 'rootfiles/PromptBkgTree_promptDataDriven'+year+'_mcal'+str(calm)+'to'+str(calh)+'.root'
if datamc=='mc': mainfilename = mainfilename.replace('DataDriven','DataDrivenMC')

print 'opening', mainfilename
infile = TFile(mainfilename)
keys = infile.GetListOfKeys()

hShapeShort = infile.Get('hPromptShortSElValidZLL_MatchedCaloTruth').Clone('hShapeShort')##
shax = hShapeShort.GetXaxis()
binm = shax.FindBin(calm)
binh = shax.FindBin(calh)


if grabasignal: 
	fsignal = TFile('/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v11/Signal/T2btLL//Stop1100_Chi1ne1000.root')

fout = 'Valid_year'+str(year)+'.root'
fnew = TFile(fout,'recreate')


searchbinresults = {}
hratios = []
clist = []
directories = []
print 'len(keys)', len(keys)
for key in sorted(keys):#[:241]:
	infile.cd()
	name = key.GetName()
	
	
	if 'hFake' in name: continue
	
	if not ('Low' in name or 'Valid' in name or 'MhtSideband' in name or 'Baseline' in name or 'Bin23' in name): continue#): continue# 
	
	
	if not 'Truth' in name: continue
	#if 'Baseline' in name: continue
	if not 'CaloSideband' in name: continue
	if not 'hPrompt' in name: continue
	if 'FakeCr' in name: continue
	print 'still taking', name
	
	if makePredictionMode:
		if not 'BinNumber' in name: continue

	print 'name', name
	kinvar = name.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
	kinvar = kinvar[kinvar.find('_')+1:]
	print 'got kinvar', kinvar, 'name', name
	
	hsideband =   infile.Get(name).Clone()
	hsideband.Scale(extrascale)
	
	htruth =                  infile.Get(name.replace('CaloSideband','')).Clone()
	#htruth.Reset()##this gets rid true prompt
	if not isdata: htruth.Add(infile.Get(name.replace('CaloSideband','').replace('hPrompt','hFake')))
	
	htruth.Scale(extrascale)
	

	
	if isdata:
		if 'Baseline' in name:
			for ibin in range(1,htruth.GetXaxis().GetNbins()+1):
				htruth.SetBinContent(ibin, 0)
	
	if doblinding and 'ZLL' in name:
		if kinvar=='InvMass':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: htruth.SetBinContent(ibin, 0)
	if doblinding and 'ValidMT' in name:			
		if kinvar=='LepMT':
			xaxt = htruth.GetXaxis()
			for ibin in range(1,xaxt.GetNbins()+1):
				if xaxt.GetBinLowEdge(ibin)>=110: htruth.SetBinContent(ibin, 0)	
			
			
	
	hpromptmethod = infile.Get(name.replace('Truth','Method2')).Clone()###then for MC complete totals:
	if not isdata: hpromptmethod.Add(infile.Get(name.replace('Truth','Method2').replace('hPrompt','hFake')))
	
	hpromptmethod.Scale(extrascale)
	if dofakesidebandsubtraction: 
		fakecontrib2sub_name = name.replace('hPrompt','hFake').replace('Truth','Method3').replace('_','FakeCr_')
		print 'fakecontrib2sub_name', fakecontrib2sub_name	
		hfakecontrib2sub = infile.Get(fakecontrib2sub_name).Clone()
		if not isdata: hfakecontrib2sub.Add(infile.Get(fakecontrib2sub_name.replace('Prompt','Fake')))
		hfakecontrib2sub.Scale(extrascale)	
		hpromptmethod.Add(hfakecontrib2sub,-1)	
		for ibin in range(1,hpromptmethod.GetXaxis().GetNbins()+1):
			if hpromptmethod.GetBinContent(ibin)<0: hpromptmethod.SetBinContent(ibin, 0) ## needs a systematic?		
	

	hfakemethod =                  infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_')) ###
	if not isdata: hfakemethod.Add(infile.Get(name.replace('hPrompt','hFake').replace('Truth','Method1').replace('CaloSideband','').replace('_','FakeCr_').replace('hFake','hPrompt')))
	hfakemethod.Scale(extrascale)
	histoStyler(hfakemethod,38) ###
	hfakemethod.SetFillColor(38)
	hfakemethod.SetFillStyle(1001)
		
	if 'BinNumber' in name and False:
		hpromptmethod = merge2dtbinsIndium(hpromptmethod)
		hfakemethod = merge2dtbinsIndium(hfakemethod)
		hsideband = merge2dtbinsIndium(hsideband)
		htruth = merge2dtbinsIndium(htruth)
		

	if 'MatchedCalo' in name and False:
		dintHigh, dintLow = Double(), Double()
		integ_high = hpromptmethod.IntegralAndError(binm,binh-1,dintHigh)
		hspecialAux = TH1F('hspecialMethod','hspecialMethod',1,0,1)
		hspecialAux.SetBinContent(1,integ_high)
		hspecialAux.SetBinError(1,dintHigh)		

		

	if len(redoBinning[kinvar])!=3: 
		nbins = len(redoBinning[kinvar])-1
		newxs = array('d',redoBinning[kinvar])
	else:
		newbinning = []
		print kinvar, name
		stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
		for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
		nbins = len(newbinning)-1
		newxs = array('d',newbinning)
	htruth = htruth.Rebin(nbins,'',newxs)
	hpromptmethod = hpromptmethod.Rebin(nbins,'',newxs)
	
	hfakemethod = hfakemethod.Rebin(nbins,'',newxs)####
	
	for ibin in range(1,hfakemethod.GetXaxis().GetNbins()+1):
	  if isdata or True:
		if 'Short' in name:
			binc = hpromptmethod.GetBinContent(ibin)
			bine = hpromptmethod.GetBinError(ibin)
			hpromptmethod.SetBinError(ibin, TMath.Sqrt(pow(binc,2)))
			#hpromptmethod.SetBinContent(ibin, 0)
			
			
			hpromptmethod.SetBinError(ibin, binc)
			#hpromptmethod.SetBinContent(ibin, 0)
			

			
			binc = hfakemethod.GetBinContent(ibin)
			bine = hfakemethod.GetBinError(ibin)
			hfakemethod.SetBinError(ibin, TMath.Sqrt(pow(0.3*binc,2)+pow(bine,2)))
				
		if 'Long' in name:
			binc = hfakemethod.GetBinContent(ibin)
			bine = hfakemethod.GetBinError(ibin)
			###hfakemethod.SetBinError(ibin, TMath.Sqrt(pow(0.5*binc,2)+pow(bine,2)))			
			
			binc = hpromptmethod.GetBinContent(ibin)
			bine = hpromptmethod.GetBinError(ibin)
			###hpromptmethod.SetBinError(ibin, TMath.Sqrt(pow(0.2*binc,2)+pow(bine,2)))				
			
		if hfakemethod.GetBinContent(ibin)<=0: 
			hfakemethod.SetBinContent(ibin, 0)
			hfakemethod.SetBinError(ibin, 1)			
			

		
	if year=='Run2016':
			htruth.SetTitle('data (2016)')
			hpromptmethod.SetTitle('prompt prediction (2016)')
			hfakemethod.SetTitle('fake pred. (2016)')
	if year == 'Summer16':			
			htruth.SetTitle('obs. (Summer16 MC)')	
			hpromptmethod.SetTitle('prompt pred. (Summer16 MC)')
			hfakemethod.SetTitle('fake pred. (Summer16 MC)')			
	if year=='Run2017':
			htruth.SetTitle('data (2017)')
			hpromptmethod.SetTitle('prompt prediction (2017)')
			hfakemethod.SetTitle('fake pred. (2017)')	
	if year == 'Fall17':			
			htruth.SetTitle('obs. (Fall17 MC)')	
			hpromptmethod.SetTitle('prompt pred. (Fall17 MC)')
			hfakemethod.SetTitle('prompt pred. (Fall17 MC)')			
	if year=='Run2018':
			htruth.SetTitle('data (2018)')
			hpromptmethod.SetTitle('prompt prediction (2018)')
			hfakemethod.SetTitle('fake pred. (2018)')	
	if year == 'Autumn18':
			htruth.SetTitle('obs. (Autumn18 MC)')	
			hpromptmethod.SetTitle('prompt pred. (Autumn18 MC)')
			hfakemethod.SetTitle('prompt pred. (Autumn18 MC)')			
	if year=='Phase1':
			htruth.SetTitle('data (Phase 1)')
			hpromptmethod.SetTitle('prompt prediction (Phase 1)')
			hfakemethod.SetTitle('fake pred. (Phase 1)')			
						
			

	
	c1 = mkcanvas('c1')
	shortname = name.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
	directory = shortname.split('_')[0].replace('hPrompt','').replace('CaloSideband','')
	if not directory in directories:
		directories.append(directory)
		if not os.path.exists('pdfs/Validation/prompt-bkg/'+year+'/'+directory):
			os.system('mkdir -p pdfs/Validation/prompt-bkg/'+year+'/'+directory)	

	varname = shortname.split('_')[-1]
	htruth.GetXaxis().SetTitle(namewizard(varname))
	hpromptmethod.GetXaxis().SetTitle(namewizard(varname))    
	#leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)


	themax = 150*max([hpromptmethod.GetMaximum(),htruth.GetMaximum()])

	hpromptmethod.SetLineColor(kTeal-5)
	hpromptmethod.SetFillStyle(1001)
	hpromptmethod.SetFillColor(hpromptmethod.GetLineColor()-1)	
	fnew.cd()
	plotname = shortname.replace('_','').replace('CaloSideband','')
	
	if 'BinNumber' in name:
		hpromptmethod.Write(hpromptmethod.GetName().replace('CaloSideband','').replace('Method2','Method'))
		hfakemethod.Write(hfakemethod.GetName().replace('FakeCr','').replace('Method1','Method'))
		if 'Short' in name or 'Long' in name:
			regionkey = name.split('_')[0].replace('hPrompt','').replace('Long','').replace('Short','')
			if not regionkey in searchbinresults.keys(): searchbinresults[regionkey] = {}
			if 'Long' in name: searchbinresults[regionkey]['Long'] = [htruth.Clone(), hpromptmethod.Clone(),hfakemethod.Clone()]
			if 'Short' in name: searchbinresults[regionkey]['Short'] = [htruth.Clone(), hpromptmethod.Clone(), hfakemethod.Clone()]
				
	hratio, hpromptmethodsyst = FabDrawSystyRatio(c1,leg,htruth,[hfakemethod, hpromptmethod],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	
			
	pad1, pad2 = hpromptmethodsyst[-2:]
	hratio.GetYaxis().SetRangeUser(0.0,2.125)	
	hratio.GetYaxis().SetTitle('data/pred.')
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	
	pad1.cd()
	print 'comparing Baseline with', name
	if grabasignal and ('Baseline' in name or 'ValidZLL' in name or 'MhtSideband' in name) and not ('HighMT' in name ) and not ('LepPt' in name): 
		#fsignal.ls()
		sname = name.replace('CaloSideband','').replace('_','SystNom_').replace('Prompt','')
		print 'looking for signal name', sname
		hsignal = fsignal.Get(sname)
		hsignal = hsignal.Rebin(nbins,'',newxs)
		histoStyler(hsignal, kRed)
		hsignal.Draw('hist same')
		leg.AddEntry(hsignal, 'T2bt g1100, chi1000)')
	fnew.cd()			

	pad2.cd()
	leg2 = mklegend(x1=.68, y1=.85, x2=.94, y2=.965, color=kWhite)
	leg2.Draw()	

	pad1.cd()
	htruth.GetYaxis().SetRangeUser(0.09,themax)
	hfakemethod.GetYaxis().SetRangeUser(0.01,themax)
	hpromptmethod.GetYaxis().SetRangeUser(0.09,themax)		
	hpromptmethod.SetTitle('')
	htruth.SetTitle('')	
	hpromptmethod.SetLineWidth(3)


	#p1 = c1.FindObject('pad1')
	#p2 = c1.FindObject('pad2')	
	#for p in p1.GetListOfPrimitives():
	#	print p.GetName()
		
	#pave = p1.FindObject('TPave')
	#pave.Delete()
	#c1.Update()

	c1.Write('c_'+plotname)
		
	shortname = shortname.replace('CaloSideband','')
	pdfname = 'pdfs/Validation/prompt-bkg/'+year+'/'+directory+'/'+shortname.replace('_','')+'.png'
	c1.Print(pdfname)
	if makepdfs: c1.Print(pdfname.replace('.png','.pdf'))
	
	#clist.append(c1)
	c1.Delete()
	hratios.append([hratio, hpromptmethodsyst])


print 'searchbinresults', searchbinresults.keys()
for regionkey in searchbinresults:
	print 'doing regionkey', regionkey
	htruthLong, hpromptmethodLong, hfakemethodLong = searchbinresults[regionkey]['Long']
	htruthShort, hpromptmethodShort, hfakemethodShort = searchbinresults[regionkey]['Short']	
	htruthLong.Add(htruthShort)
	
	for ibin in range(1, htruthLong.GetXaxis().GetNbins()+1):
		if htruthLong.GetBinContent(ibin)==0:
			htruthLong.SetBinError(ibin, 1)
				
	hpromptmethodLong.Add(hpromptmethodShort)
	hfakemethodLong.Add(hfakemethodShort)	
	
	
	if year=='Run2016':
			htruthLong.SetTitle('data (2016)')
			hpromptmethodLong.SetTitle('prompt prediction (2016)')
			hfakemethodLong.SetTitle('fake prediction (2016)')			
	if year == 'Summer16':
			htruthLong.SetTitle('obs. (Summer16 MC)')	
			hpromptmethodLong.SetTitle('prompt pred. (Summer16 MC)')
			hfakemethodLong.SetTitle('fake pred. (Summer16 MC)')				
	if year=='Run2017':
			htruthLong.SetTitle('data (2017)')
			hpromptmethodLong.SetTitle('prompt prediction (2017)')
			hfakemethodLong.SetTitle('fake prediction (2017)')	
	if year == 'Fall17':
			htruthLong.SetTitle('obs. (Fall17 MC)')	
			hpromptmethodLong.SetTitle('prompt pred. (Fall17 MC)')
			hfakemethodLong.SetTitle('fake pred. (Fall17 MC)')	
	if year=='Run2018':
			htruthLong.SetTitle('data (2018)')
			hpromptmethodLong.SetTitle('prompt prediction (2018)')
			hfakemethodLong.SetTitle('fake prediction (2018)')
	if year=='Phase1':
			htruthLong.SetTitle('data (Phase 1)')
			hpromptmethodLong.SetTitle('prompt prediction (Phase 1)')
			hfakemethodLong.SetTitle('fake prediction (Phase 1)')
			

	themax = 500*max([htruthLong.GetMaximum(),hpromptmethodLong.GetMaximum()])
		
	fnew.cd()
	hpromptmethodLong.Write(hpromptmethodLong.GetName().replace('CaloSideband','MASTER'))
	hfakemethodLong.Write(hfakemethodLong.GetName().replace('FakeCr','MASTER'))	

	plotname = regionkey.replace('_','').replace('CaloSideband','')
	c1 = mkcanvas('c1')
	leg = mklegend(x1=.49, y1=.54, x2=.91, y2=.78, color=kWhite)
	hrattot = htruthLong.Clone()
	hdenom = hpromptmethodLong.Clone()
	hdenom.Add(hfakemethodLong)
	hrattot.Add(hdenom, -1)
	hratio, hpromptmethodsyst = FabDrawSystyRatio(c1,leg,htruthLong,[hpromptmethodLong,hfakemethodLong],datamc=datamc,lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')
	pad1, pad2 = hpromptmethodsyst[-2:]
	hratio.GetYaxis().SetRangeUser(0.0,3.4)	
	hratio.GetYaxis().SetTitle('(B/A*C)/D')
	hratio.SetLineColor(kBlack)
	for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
		if hratio.GetBinContent(ibin)==0:
			hratio.SetBinContent(ibin,-999)
	hratio.SetMarkerColor(kBlack)
	hratio.SetDirectory(0)
	
	pad2.cd()
	leg2 = mklegend(x1=.68, y1=.85, x2=.94, y2=.965, color=kWhite)

	leg2.Draw()
	pad1.cd()
	hpromptmethodLong.GetYaxis().SetRangeUser(0.01,themax)
	hfakemethodLong.GetYaxis().SetRangeUser(0.01,themax)	
	htruthLong.GetYaxis().SetRangeUser(0.01,themax)	
	hpromptmethod.SetTitle('')
	htruth.SetTitle('')	
	hpromptmethod.SetLineWidth(3)
			
			
	c1.Update()
	
	c1.Write('c_'+plotname+'BinNumber_merged')
	

	hres = TH1F('resid_'+plotname+'BinNumber_merged','resid_'+plotname+'BinNumber_merged',32,-4,4)
	hres.GetYaxis().SetTitle('number of signal regions')
	hres.GetXaxis().SetTitle('pull')
	for ibin in range(1,hrattot.GetXaxis().GetNbins()+1):
		print ibin, 'doing residuals', hrattot.GetBinContent(ibin)
		if hrattot.GetBinError(ibin)>0:
			hres.Fill(hrattot.GetBinContent(ibin)/hrattot.GetBinError(ibin))
				
	
	directory_ = 'SearchBins'
	if not directory_ in directories:
		directories.append(directory_)
	if not os.path.exists('pdfs/Validation/prompt-bkg/'+str(year)+'/'+directory_):
		os.system('mkdir pdfs/Validation/prompt-bkg/'+str(year)+'/'+directory_)
		
	shortname = regionkey.replace('Control','').replace('Truth','').replace('Method1','').replace('Method2','')
	shortname = shortname.replace('CaloSideband','')
	pdfname = 'pdfs/Validation/prompt-bkg/'+str(year)+'/'+directory_+'/'+str(year)+'_'+shortname.replace('_','')+'.png'
	c1.Print(pdfname)	
	if makepdfs: c1.Print(pdfname.replace('.png','.pdf'))
	

	#gStyle.SetOptFit(1111)	
	c2 = mkcanvas('c2')
	hres.Draw('hist e')
	#hres.Fit('gaus')
	c2.Update()

	c2.Print(pdfname.replace('.png','Pull.png'))
	c2.Delete()
		
	c1.Delete()
	
	
import os, sys
whippyname = 'htmlwhippy'+year+'.sh'
os.system('echo echo hello > '+whippyname)
pipe = '>'
print 'reached the end of things'
for directory_ in directories:
	os.system('echo python tools/whiphtml.py \\"pdfs/Validation/prompt-bkg/'+year+'/'+directory_+'/*.png\\" '+pipe+' '+whippyname)
	pipe = '>>'
os.system('bash '+whippyname)
thename = fnew.GetName()
print 'just created', os.getcwd()+'/'+thename
fnew.Close()
print 'now do'
copycommand = 'cp -r pdfs/Validation/prompt-bkg/'+year+' /afs/desy.de/user/b/beinsam/www/DisappearingTracks/Validation/'+tag+'_'+year
print copycommand
os.system(copycommand)


if True: 
	print 'you might want to hadd these end products together', thename
	print 'a la'
	print 'hadd -f predictionRun2.root Valid_yearRun2016.root Valid_yearPhase1.root'
	print 'cp predictionRun2.root /afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Indium/v9/'
	print 'cp predictionRun2.root /afs/desy.de/user/b/beinsam/www/DisappearingTracks/Validation/'+tag+'_'+year
	

