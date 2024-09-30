#this ones real important!
'''
---------------------BR: 100%-----------------------
/pnfs/desy.de/cms/tier2/store/user/aksingh/SignalMC/LLChargino/BR100/Lifetime_10cm/*/*.root
#/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-FEE6C100-4AA5-E911-9CD0-B496910A9A28_RA2AnalysisTree.root
#python tools/TheAnalyzerWithDeDxLowMht.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_40000-*.root"

#higgsino file
compare fast and full for higgsinos

/nfs/dust/cms/user/beinsam/CommonSamples/MC_BSM/CompressedHiggsino/RadiativeMu_2016Full/ntuple_sidecar/higgsino94xfull_susyall_mChipm115GeV_dm0p268GeV_pu35_part27of100_RA2AnalysisTree.root 
'''
import os, sys
import time as time_
import numpy as np
from ROOT import *
execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/shared_utils.py')
from glob import glob
import random
from array import array
gROOT.SetStyle('Plain')
#gROOT.SetBatch(1)

#for q quick higgsino test run:
'''
python tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/sbein/CommonSamples/RadiativeMu_2017Fast/ntuple_sidecarv3/higgsino_Fall17_susyall_mChipm160GeV_dm0p287GeV_part2of25_RA2AnalysisTree.root" --nfpj 999 --outdir bay_PureHiggsino
python tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIAutumn18FSv3.SMS-T2tb-LLChipm-ctau10to200-mStop-400to1750-mLSP0to1650*.root" --nfpj 10 --outdir bay_T2tb_2018

#new
python tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/sbein/CommonSamples/RadiativeMu_2017Fast/ntuple_sidecarv3c/higgsino_Fall17_susyall_mChipm160GeV_dm0p287GeV*.root" --nfpj 999 --outdir bay_PureHiggsino #/nfs/dust/cms/user/beinsam/CommonSamples/NtupleMaker/3March2020/CMSSW_9_4_11/src/TreeMaker/Production/test/
python tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/sbein/CommonSamples/RadiativeMu_2018Fast/ntuple_sidecarv3c/higgsino_Autumn18_susyall_mChipm160GeV_dm0p287GeV*.root" --nfpj 999 --outdir bay_PureHiggsino #/nfs/dust/cms/user/beinsam/CommonSamples/NtupleMaker/3March2020/CMSSW_10_2_7/src/TreeMaker/Production/test/

python tools/TheAnalyzerSystematics.py --fnamekeyword "python tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIAutumn18FS.PMSSM_set_1_LL_TuneCP2_13TeV-pythia8-AOD0_00000-02A2CB75-DFA0-1E49-8D7E-699CD06E1182_RA2AnalysisTree.root" --nfpj 1 --outdir test
Input: ['/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIAutumn18FS.PMSSM_set_1_LL_TuneCP2_13TeV-pythia8-AOD0_00000-02A2CB75-DFA0-1E49-8D7E-699CD06E1182_RA2AnalysisTree.root'] 
Output: RunIIAutumn18FS.PMSSM_set_1_LL_TuneCP2_13TeV-pythia8-AOD0_00000-02A2CB75-DFA0-1E49-8D7E-699CD06E1182_RA2AnalysisTree.root
#set up systematics

#Viktor SM sample
python tools/TheAnalyzerSystematics.py --fnamekeyword "/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/ProductionRun2v3/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_120000-40EE4B49-34BB-E611-A332-001E674FB2D4_RA2AnalysisTree.root" --nfpj 1 --outdir test
'''

#follow this up with mergymovey.sh, then ...

#re-weight ctau from Viktor
def reweight_ctau(ctauIn, ctauOut, list_of_labXY):
    output = 1
    for labXY in list_of_labXY:
        t0 = labXY / 10.0          # convert to cm
        if ctauIn>0:
            output *= ctauIn/ctauOut * TMath.Exp(t0/ctauIn - t0/ctauOut)   
    return output
#'''

#doControlRegions = True

thebinning = binning
thebinning['MatchedCalo'] = [100,0,100]
binning['FakeCrNr'] = [6,-3,3]
debugmode = False
exomode = False
fnameprefire = 'usefulthings/Map_Jet_L1IsoEG30eff_bxm1_looseJet_SingleMuon_Run2017F.root'

defaultInfile = "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-FEE6C100-4AA5-E911-9CD0-B496910A9A28_RA2AnalysisTree.root"#"/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-975_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_230000-FCD9083D-3E88-E911-B3D1-0CC47A7EEE76_RA2AnalysisTree.root"#"/pnfs/desy.de/cms/tier2/store/user/aksingh/SignalMC/LLChargino/BR100/Lifetime_50cm/July5-SUMMER19sig/g1700_chi1550_27_200970_step4_50miniAODSIM_*_RA2AnalysisTree.root"
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--updateevery", type=int, default=10000,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile,help="file")
parser.add_argument("-jecvar", "--jecvar", type=str, default='Nom',help="")
parser.add_argument("-numberOfFilesPerJob", "--nfpj", type=int, default=100)
parser.add_argument("-outdir", "--outdir", type=str, default='testout')
parser.add_argument("-targetctau", "--targetctau", type=int, default=-1)
args = parser.parse_args()
nfpj = args.nfpj
filenamestring = args.fnamekeyword
if ',' in filenamestring: inputFiles = filenamestring.split(',')
else: inputFiles = glob(filenamestring)
analyzer = args.analyzer
updateevery = args.updateevery
targetctau = args.targetctau
verbose = True
outdir = args.outdir

is2016, is2017, is2018 = True, False, False
isdata = 'Run20' in filenamestring
if 'Run2016' in filenamestring or 'Summer16' in filenamestring or 'aksingh' in filenamestring or '2016Fast' in filenamestring: 
    is2016, is2017, is2018 = True, False, False
    year = '2016'
elif 'Run2017' in filenamestring or 'Fall17' in filenamestring or '2017Fast' in filenamestring: 
    is2016, is2017, is2018 = False, True, False
    year = '2017'    
elif 'Run2018' in filenamestring or 'Autumn18' in filenamestring or '2018Fast' in filenamestring: 
    is2016, is2017, is2018 = False, True, True
    year = '2018'    

if is2016: phase = 0
else: phase = 1


loptcut = 25
hiptcut = 40
leppt = 40

if is2016: 
    BTAG_deepCSV = 0.6321
if is2017: 
    BTAG_deepCSV = 0.4941
if is2018: 
    BTAG_deepCSV = 0.4184
btag_cut = BTAG_deepCSV

execfile(os.environ['CMSSW_BASE']+'/src/analysis/tools/lib_systematics.py')
readerBtag = prepareReaderBtagSF()


eleReco, eleIdiso, eleIdFastFull, muIdiso, muIdFastFull = getRecoIdisoFastfullLeptonSFhistos(year)

from CrossSectionDictionary import *
ispmssm = False
if 'Lifetime_' in filenamestring or 'Signal' in filenamestring or 'T1' in filenamestring: model_ = 'T1'
elif 'iggsino' in outdir:  model_ = 'PureHiggsino'
elif 'wino' in outdir.lower():  model_ = 'PureWino'
elif 'T2bt' in filenamestring or 'T2tb' in filenamestring: model_ = 'T2tt'
elif 'PMSSM' in filenamestring: 
    model_ = 'pMSSM'
    ispmssm = True
elif 'tchiwz' in outdir.lower(): model_ = 'TChiWZ'
elif 'tchiww' in outdir.lower(): model_ = 'TChiWW'
else: model_ = 'Other'
print 'were considering model_', model_
loadCrossSections(model_)
#oldWayHiggsino = False #pretty sure this has been off since v3c
#if oldWayHiggsino: hard_coded_higgsino_events_per_file = 20000# shoot, can't get this info from the ntuple
makeNewfileEachSignal = True
if model_ in ['PureHiggsino','pMSSM','PureWino','TChiWW', 'TChiWZ']: 
    makeNewfileEachSignal = False

proccodes = {(1000023, 1000024, 1000022):1, (1000023, 1000022):2, (1000024, 1000022):3}
procfilters = []
if model_ == 'PureWino': procfilters = [1,3]
if model_ == 'PureHiggsino': procfilters = [1,2,3]

prodpairs = {(1000024,1000023):1, (1000024,1000022):2,(1000023,1000022):3, (1000024,1000024):4}
prodfilters = []
if model_ == 'TChiWZ': prodfilters = [1]
if model_ == 'TChiWW': prodfilters = [4]

if 'WJets' in filenamestring: 
    makeNewfileEachSignal = False
    issignal = False
else: issignal = True

if outdir=='': outdir = 'bay_'+model_

identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('Summer16.','').replace('RA2AnalysisTree','')
print 'Identifier', identifier

calib_version = '-SingleMuon'
calib_version = ''# Sang-Il's new key names
if 'Run20' in identifier: 
    keyforcalibs = identifier.split('-')[0].replace('skims','').replace('skim','')+calib_version
    dedxcalib_barrel = DedxCorr_Pixel_barrel[keyforcalibs]
    dedxcalib_endcap = DedxCorr_Pixel_endcap[keyforcalibs]
elif 'Summer16' in identifier: 
    dedxcalib_barrel = DedxCorr_Pixel_barrel['Summer16']
    dedxcalib_endcap = DedxCorr_Pixel_endcap['Summer16']
elif 'Fall17' in identifier: 
    dedxcalib_barrel = DedxCorr_Pixel_barrel['Fall17']
    dedxcalib_endcap = DedxCorr_Pixel_endcap['Fall17']
else: 
    dedxcalib_barrel = 1.0
    dedxcalib_endcap = 1.0    


doDedxSmear = False
if not isdata :
    doDedxSmear = True
    fsmear_barrel, fsmear_endcap = Load_DedxSmear(phase)
    
    
f_dxydzcalibration = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/dxydzcalibration.root')
if 'Fall17' in identifier or 'Autumn18' in identifier:
        vtx_calibs = [f_dxydzcalibration.Get('g_calibratedxy'), f_dxydzcalibration.Get('g_calibratedz')]
else:
    vtx_calibs = []
    

fcorrectionFastSim = TFile('usefulthings/dedxFastSimCorrection.root')
p_dedxFastCorrection = fcorrectionFastSim.Get('p_dedxFastCorrection')

rndgen = TRandom3()
hPtResVsGenFull_ProfileX = fcorrectionFastSim.Get('hPtResVsGenFull_ProfileX')
pxax_ = hPtResVsGenFull_ProfileX.GetXaxis()
def getPtSmear(val):
    pbin = pxax_.FindBin(val)
    sigma = hPtResVsGenFull_ProfileX.GetBinError(pbin)
    smearval = rndgen.Gaus(1,sigma)
    return smearval
    
    

thejet = TLorentzVector()


ftrig = TFile(os.environ['CMSSW_BASE']+'/src/analysis/triggerefficiency/susy-trig-plots_amag.root')#triggersRa2bRun2_v4_withTEffs.root')
ttrig = ftrig.Get('tEffhMetMhtRealXMht_run2;1')
hpass = ttrig.GetPassedHistogram().Clone('hpass')
htotal = ttrig.GetTotalHistogram().Clone('htotal')
gtrig   = TEfficiency(hpass, htotal)
gtrigDown = TEfficiency(hpass, htotal)


ftrig = TFile(os.environ['CMSSW_BASE']+'/src/analysis/triggerefficiency/trigger-efficiencies.root')

htrigmht    = ftrig.Get('mht_SingleEl_lowjets/h_triggereff_MHT_MHT_'+year)
htrigmht_up = ftrig.Get('mht_SingleEl_highjets/h_triggereff_MHT_MHT_'+year)

htrigel   = ftrig.Get('sel_switchdenom/h_triggereff_SEl_leadingelectron_pt_MHT_'+year)
htrigelUp = ftrig.Get('sel_JetHT/h_triggereff_SEl_leadingelectron_pt_MHT_'+year)

htrigmu   = ftrig.Get('smu_switchdenom/h_triggereff_SMu_leadingmuon_pt_MHT_'+year)
htrigmuUp = ftrig.Get('smu_JetHT/h_triggereff_SMu_leadingmuon_pt_MHT_'+year)


if not makeNewfileEachSignal:
    newfname = 'Hists_'+identifier+'.root'
    if not os.path.isdir(outdir):     
        os.system('mkdir '+outdir)
    fnew_ = TFile(outdir+'/'+newfname,'recreate')
    print 'creating file', fnew_.GetName()


fdtscalefactor = TFile(os.environ['CMSSW_BASE']+'/src/analysis/systematics/signal_scalefactor.root')
hdtscalefactor_long = fdtscalefactor.Get('fit_sf_long')
hdtscalefactor_short = fdtscalefactor.Get('fit_sf_short')
dtsfbin_ = int(year)%2015


mdp= 0.4
inf = 9999999
lowht = 0

callShort = 15 
callLong = 20



if is2016: 

    mvaPromptLongLoose = 0.1#<==0.1 ##this is good May21
    mvaPromptShortLoose = 0.05#<==#-0.05

    mvaFakeShortLoose = -0.1    
    mvaFakeShortMedium = -0.05#could try this next 4.08.21
    
    mvaFakeLongLoose = -0.1
    mvaFakeLongMedium = 0.0
    mvaShortTight = 0.1
    mvaLongTight = 0.12

    calmShort, calhShort = 30, 300 #works well in data        
    calmLong, calhLong = 30, 120
else:

    mvaPromptShortLoose = 0.05
    mvaPromptLongLoose = 0.08
    
    mvaFakeShortLoose = -0.1#==-0.1#-0.1#-0.3
    mvaFakeShortMedium = 0.05
        
    mvaFakeLongLoose = -0.1#<==-0.05#<==-0.15 #tuesday earlymorning    
    mvaFakeLongMedium = 0.0    
    
    
    mvaShortTight = 0.15#was feeling good about this after shower, but it was a bit loose########
    mvaLongTight = 0.08#Tuesday earlymorning
    
    calmShort, calhShort = 30, 300 #works well in data        
    calmLong, calhLong = 30, 120
    
    
    
print 'calhLong, calmLong', calhLong, calmLong
mvaminShort = min([mvaPromptShortLoose, mvaFakeShortLoose])
mvaminLong  = min([mvaPromptLongLoose,  mvaFakeLongLoose] )
    

#                                                   1        2          3        4       5         6       7               8           9                    10          11       12        13           14           15          16              17             18             19           20             21             22                23        24.......25
regionCuts = {}
varlist_                                       = ['Ht',  'HardMet','NJets',  'BTags','NTags', 'TrkLength','MdpMetJets','DeDx',  'NElectrons','NMuons', 'InvMass', 'LepMT',   'TrkPt',      'TrkEta',  'MatchedCalo','IsMuMatched','DPhiMhtDt', 'TrkMva',           '2ndTrkMva','MtDtMht',  'MissingOuterHits','LepPt',  'DrJetDt', 'BinNumber','MinDPhiMhtHemJet','MTauTau', 'NVtx','DedxMass']
regionCuts['ShortBaselineSystNom']             = [(0,inf), (30,inf),(1,inf), (0,inf), (1,inf),  (0,0),    (mdp,inf),   (0,inf),   (0,inf),   (0,inf),  (140,inf),  (110,inf),(loptcut,inf),    (0,2.4),  (0,callShort),(0,0),      (0,inf),    (mvaShortTight,inf),(-0.1,inf), (20,inf),   (-inf,inf),        (40,inf),  (0.2,inf)]
regionCuts['LongBaselineSystNom']              = [(0,inf), (30,inf),(1,inf), (0,inf), (1,inf),  (1,1),    (mdp,inf),   (0,inf),   (0,inf),   (0,inf),  (140,inf),  (110,inf),(hiptcut,inf),   (0,2.4),  (0,callLong),  (0,0),      (0,inf),    (mvaLongTight,inf), (-0.1,inf), (20,inf),   (2,inf),           (40,inf),  (0.2,inf)]
   
if 'T1btbt' in filenamestring or 'T2tb' in filenamestring or 'iggsino' in filenamestring:  vars2draw = ['HardMet','NJets','BinNumber','DedxMass','BTags', 'TrkLength','TrkPt','TrkMva','NElectrons','NMuons']
else: vars2draw = ['HardMet','BinNumber','DedxMass','BTags','NElectrons','NMuons']

dedxidx = varlist_.index('DeDx')
srindex = varlist_.index('BinNumber')
mcalidx = varlist_.index('MatchedCalo')
dphiidx = varlist_.index('DPhiMhtDt')
mvaidx = varlist_.index('TrkMva')

regionkeys = regionCuts.keys()
for key in regionkeys:
    break

    #for bkg control regions
    '''
    newlist2 = list(regionCuts[key])
    newlist2[mcalidx] = (calm,calh)
    newlist2[mvaidx] = (mvaLoose,inf)        
    newkey = key.replace('SystNom','CaloSidebandSystNom')
    regionCuts[newkey] = newlist2
    '''

weightsysts = ['BTagUp','BTagDown','IsrUp','IsrDown','JecUp','Prefire', 'PuUp', 'PuDown', 'ScaleUp', 'ScaleDown', 'DedxUp', 'TrigUp', 'DtSfShortUp','DtSfLongUp']
for key in regionkeys:
    for syst in weightsysts:
        newkey = key.replace('Nom',syst)
        regionCuts[newkey] = list(regionCuts[key])


#print 'regionCuts', regionCuts

ncuts = 23
def selectionFeatureVector(fvector, regionkey='', omitcuts=''):
    if not fvector[0]>=fvector[1]: return False
    iomits = []
    for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
    for i, feature in enumerate(fvector):
        if i>=ncuts: continue
        if i in iomits: continue
        if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]):
            return False
    return True


def getBinNumber(fv):
    for binkey in binnumbers:
        foundbin = True
        for iwindow, window in enumerate(binkey):
            if not (fv[iwindow]>=window[0] and fv[iwindow]<=window[1]): foundbin = False
        if foundbin: return binnumbers[binkey]
    return -1
    

#counter histogram:
hHt = TH1F('hHt','hHt',200,0,10000)
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',200,0,10000)

hScaleTotUpDown = TH1F('hScaleTotUpDown','hScaleTotUpDown',3,0,3)

indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
for region in regionCuts:
    for ivar, var in enumerate(varlist_):
        if not var in vars2draw: continue
        if (not srindex==ivar) and (not 'SystNom' in region): continue
        histname = region+'_'+var
        histoStructDict[histname] = mkHistoStruct(histname, thebinning)
    
#print 'histoStructDict', histoStructDict.keys()
def getCTauCmChi1pmHiggsinoFromMassGeV(dmchipmchi10):
    #https://arxiv.org/pdf/1410.4549.pdf
    mpi = 0.135
    ctau = 1.1*pow(dmchipmchi10*1000./300,-3)*pow(1-pow(mpi/dmchipmchi10,2),-0.5)
    return ctau	
    
def getCTauCmChi1pmWinoFromMassGeV(dmchipmchi10, mass):
    #https://arxiv.org/pdf/1410.4549.pdf
    fwino = TFile('usefulthings/WinoCtauVsDmVsM.root')
    hctau = fwino.Get('hwinoctaucm')
    #winoctau = hctau.GetBinContent(hctau.GetXaxis().FindBin(mass), hctau.GetYaxis().FindBin(dmchipmchi10))
    winoctau = hctau.Interpolate(mass, dmchipmchi10)
    fwino.Close()
    return winoctau
    
if model_ in ['PureHiggsino','PureWino', 'TChiWZ', 'TChiWW']:
    islopythia8 = True
    print 'filenamestring', inputFiles[0]
    print 'last thing', inputFiles[0].split('/')[-1].split('mChipm')[-1]    
    mothermass = float(inputFiles[0].split('/')[-1].split('mChipm')[-1].split('GeV')[0])
    dm = float(inputFiles[0].split('/')[-1].split('_dm')[-1].split('GeV')[0].replace('p','.'))
    xfiles = []
    higgsinoxsecfile = TFile('usefulthings/CN_hino_13TeV.root')
    winoxsecfile_cn = TFile('usefulthings/C1N2_wino_13TeV.root'); winoxsecfile_cc = TFile('usefulthings/C1C1_wino_13TeV.root')
    if model_== 'PureWino': xfiles.extend([winoxsecfile_cn,winoxsecfile_cc])    
    else: xfiles.append(higgsinoxsecfile) #this had if model_== 'PureHiggsino': but now we want this as default for TChiWZ
    xsecpb = 0
    if mothermass<150:
        for xfile in xfiles: xsecpb += 0.001*xfile.Get('fit_nom_0').Eval(max(100,mothermass))
    elif mothermass>=150 and mothermass<200:
        for xfile in xfiles: xsecpb += 0.001*xfile.Get('fit_nom_1').Eval(mothermass)
    elif mothermass>=200 and mothermass<300:
        for xfile in xfiles: xsecpb += 0.001*xfile.Get('fit_nom_2').Eval(mothermass)    
    elif mothermass>=300 and mothermass<400:
        for xfile in xfiles: xsecpb += 0.001*xfile.Get('fit_nom_3').Eval(mothermass)    
    elif mothermass>=400 and mothermass<600:
        for xfile in xfiles: xsecpb += 0.001*xfile.Get('fit_nom_4').Eval(mothermass)
    elif mothermass>=600 and mothermass<800:
        for xfile in xfiles: xsecpb += 0.001*xfile.Get('fit_nom_5').Eval(mothermass)
    elif mothermass>=800 and mothermass<1000:
        for xfile in xfiles: xsecpb += 0.001*xfile.Get('fit_nom_6').Eval(mothermass)                
    elif mothermass>=1000 and mothermass<1200:
        for xfile in xfiles: xsecpb += 0.001*xfile.Get('fit_nom_7').Eval(mothermass)        
    elif mothermass>=1200 and mothermass<1500:
        for xfile in xfiles: xsecpb += 0.001*xfile.Get('fit_nom_8').Eval(mothermass)        
    print 'xsec was', xsecpb
    higgsinoxsecfile.Close()
    if model_== 'PureWino':
        rawctau = getCTauCmChi1pmHiggsinoFromMassGeV(dm)
        targetctau = getCTauCmChi1pmWinoFromMassGeV(dm, mothermass)
        print ('ctaus in out:', rawctau, targetctau)
    
elif model_=='pMSSM':
    islopythia8 = True
    xsecpb = 1.0
else: 
    islopythia8 = False
    xsecpb = -1
filesarectaubinary = 'ctau10to200' in filenamestring

c = TChain("TreeMaker2/PreSelection")
print 'inputFiles', inputFiles
for ifile, f in enumerate(inputFiles):
    if ifile>=nfpj: break
    print 'adding file:', f
    c.Add(f)

nentries = c.GetEntries()
#nentries = 100

c.Show(0)


fMask = TFile(os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/Masks_mcal13to30_Data2016.root')
hMask = fMask.Get('h_Mask_allyearsLongBaseline_EtaVsPhiDT')

if exomode: hMask = ''


fprefiring = TFile(fnameprefire)
hprefiring = fprefiring.Get('prefireEfficiencyMap')
hprefireDerived = hprefiring.GetPassedHistogram()
xaxprefiring = hprefireDerived.GetXaxis()
yaxprefiring = hprefireDerived.GetYaxis()
    

import os
if phase==0:
    pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-short-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml'
    pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2016-long-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml'    
else:
    pixelXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-short-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml'
    pixelstripsXml = os.environ['CMSSW_BASE']+'/src/analysis/disappearing-track-tag/2017-long-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml'    

readerPixelOnly = TMVA.Reader("")
readerPixelOnly.SetName('Reader1')
readerPixelStrips_ = TMVA.Reader("")
readerPixelStrips_.SetName('Reader2')

print 'going to process', pixelXml
prepareReaderPixel_fullyinformed(readerPixelOnly, pixelXml)

print 'going to process', pixelstripsXml
prepareReaderPixelStrips_fullyinformed_(readerPixelStrips_, pixelstripsXml)


import time
t1 = time_.time()
i0=0

nnotjet, totdt, totmt, passmt, passdt = 0, 0, 0, 0, 0

mcpass, mctot = 0, 0

orderedmasses = []
newfname = ''
print nentries, 'events to be analyzed'
for ientry in range(nentries):
    if ientry%updateevery==0:
        print 'now processing event number', ientry, 'of', nentries

    if debugmode:
        if not ientry in [4151]: continue
    c.GetEntry(ientry) 


    labxymmlist = []
    chilist = []
    susymasses = []
    susies = []
    top2susies = []
    for igp, gp in enumerate(c.GenParticles):        
        if not abs(c.GenParticles_PdgId[igp])>1000000: continue
        #if c.GenParticles_Status[igp]==23: continue
        if abs(c.GenParticles_PdgId[igp])==1000024:
            labxymmlist.append(c.GenParticles_LabXYmm[igp])
            chilist.append(c.GenParticles[igp])
        pid = abs(c.GenParticles_PdgId[igp])
        if pid==1000022 and not (c.GenParticles_Status[igp]==1): continue
        if len(top2susies)<2: top2susies.append(pid)
        if not pid in susies:                
            susies.append(pid)
            susymasses.append([pid,round(gp.M(),2)])
                
    top2susies_ = tuple(sorted(top2susies, reverse=True))
    orderedmasses_ = sorted(susymasses, key=lambda x: x[1], reverse=True)
    baremasses = tuple(sublist[0] for sublist in orderedmasses_)
    if len(prodfilters)>0:
        if not prodpairs[top2susies_] in prodfilters:
            continue    
    if len(procfilters)>0:
        if not baremasses in proccodes:
            print('whoa nelly! This code appeared!', baremasses)
            continue
        proccode = proccodes[baremasses]
        passpfilter = False
        for particlefilter in procfilters:
            if proccode==particlefilter: passpfilter = True; break
        if not passpfilter: continue
    orderedmasses_ = [orderedmasses_[0], orderedmasses_[-1]]
    if filesarectaubinary:
        rawctau=c.SusyCTau
        if targetctau>0: orderedmasses_.append([-1, targetctau])
        else: orderedmasses_.append( [-1, rawctau] )
        if (targetctau>0 and targetctau<10) and rawctau!=10: 
            continue    
    
    if ispmssm:
        id1, id2 = c.SusyLSPMass, c.SusyMotherMass
    elif makeNewfileEachSignal and not orderedmasses_==orderedmasses:
        print 'looks like a model_ transition from', orderedmasses, 'to', orderedmasses_
        orderedmasses = orderedmasses_
        if not newfname=='':
            fnew_.cd()
            hHt.Write()
            hHtWeighted.Write()
            hScaleTotUpDown.Write()
            writeHistoStruct(histoStructDict, 'truth')
            itsname = fnew_.GetName()
            print 'just created', itsname
            fnew_.Close()
            if int(os.path.getsize(itsname))<10000:
                print "removing because its a zombie"
                os.system('rm '+itsname)
            fcheck = TFile(itsname)
            if fcheck.IsZombie() or fcheck.GetNkeys()==0: 
                fcheck.Close()
                os.system('rm '+itsname)
            else: fcheck.Close()
        print 'creating new file based on', orderedmasses
        newfname = 'Hists'
        for ip, susypid in enumerate(orderedmasses):
            print susybypdg[orderedmasses[ip][0]], orderedmasses[ip][1]
            newfname+='_'+susybypdg[orderedmasses[ip][0]]+str(orderedmasses[ip][1]).split('.')[0]
        newfname+='_time'+str(round(time_.time(),6)).replace('.','p').replace('Chi1pm','Chi1ne')+'.root'
        if not os.path.isdir(outdir): os.system('mkdir '+outdir)
        fnew_ = TFile(outdir+'/'+newfname,'recreate')
        print 'creating file', fnew_.GetName()        
        print 'from', susymasses
        hHt.Reset()
        hHtWeighted.Reset()
        hScaleTotUpDown.Reset()# = TH1F('hScaleTotUpDown','hScaleTotUpDown',3,0,3)
        clearHistoStruct(histoStructDict,'truth')
        if 'T1' in model_ or 'T2tt' in model_:
            mothermass = orderedmasses[0][1]#filenames.split('/')[-1].split('_')[0].replace('Higgsino','PLACEHOLDER').replace('g','').replace('*','').replace('PLACEHOLDER','Higgsino')
            xsecpb = CrossSectionsPb[model_][str(int(5*round(mothermass/5)))]
            
            print 'got xsec', xsecpb, 'for mothermass', str(int(5*round(mothermass/5)))
        else:
            xsecpb = 1
            
    if islopythia8:
        scaleup, scaledown = 1, 1
    else:
        scaleweights = c.ScaleWeights
        if(scaleweights.size()>7): scaleweights.erase(scaleweights.begin()+7);
        if(scaleweights.size()>5): scaleweights.erase(scaleweights.begin()+5);
        if(scaleweights.size()>0): scaleweights.erase(scaleweights.begin());
        scaleup = max(scaleweights)
        scaledown = min(scaleweights)
        hScaleTotUpDown.Fill(0.5, 1)
        hScaleTotUpDown.Fill(1.5, scaleup)
        hScaleTotUpDown.Fill(2.5, scaledown)
        
        
    if targetctau>0:
        ctauweight = reweight_ctau(rawctau, targetctau, labxymmlist)
        #print('ctauweight, rawctau, targetctau, labxymmlist', ctauweight, rawctau, targetctau, labxymmlist)
    else: ctauweight = 1.0
            
    #nothing is skipped at this point yet!
    fillth1(hHt,c.HT)
    fillth1(hHtWeighted, c.HT, ctauweight)
    
    #now start physics cuts
    if issignal:
        if not passesUniversalSelectionFastSim(c): continue
        a = 1
    else: 
        if not passesUniversalSelection(c): continue
        a = 1
        if not c.JetID: continue
        
    #can't we just put a loop here?
    for jecup in [False, True]:
                
        disappearingTracks = []    
        nShort, nLong = 0, 0
        for itrack, track in enumerate(c.tracks):
            if not track.Pt() > 15 : continue        
            #if not abs(track.Eta()) < 2.4: continue
            #if not abs(track.Eta()) < 2.2: continue
            if not abs(track.Eta()) < 2.0: continue        
            
            if issignal: ischargino = False
            else: ischargino = True
            gpt = track.Pt()
            for igp, gp in enumerate(chilist):   
                if not abs(labxymmlist[igp]>25): continue
                dr = gp.DeltaR(track)            
                if dr<0.04:
                    ischargino = True
                    gpt = gp.Pt()
                    break
            if not ischargino: continue    
            #if verbose: print 'we at least got a chimatched track'
            totdt+=1
            if gpt>1100: track.SetPtEtaPhiE(gp.Pt()*getPtSmear(gpt), track.Eta(), track.Phi(), track.P())
                
                                    
            if not isBaselineTrackLoosetag(track, itrack, c, hMask):  continue
            #if verbose: print 'found', ientry, itrack, 'pt', track.Pt(), 'eta', track.Eta()
            
            if not (track.Pt() > loptcut): continue
            if debugmode: print 'we at least got a baseline track'
            dtlength, mva = isDisappearingTrack_FullyInformed(track, itrack, c, readerPixelOnly, readerPixelStrips_, [mvaminShort,mvaminLong], vtx_calibs)
            if dtlength==0: continue
        
            if debugmode: print 'and it even disappears!'    
            drlep = 99
            islep = False
            for ilep, lep in enumerate(list(c.Electrons)+list(c.TAPPionTracks)): #+list(c.Muons)
                drlep = min(drlep, lep.DeltaR(track))
                if drlep<0.1: 
                    islep = True
                    break            
            if islep: continue 
            dtisrecomu = False    
            for ilep, lep in enumerate(list(c.Muons)):
                dr = lep.DeltaR(track)
                if dr<0.1: 
                    dtisrecomu = True
                    break
                
            isjet = False
            if dtlength==1: ##short track
                jt = 30
                drcut=0.4
            else: ##long track
                jt = 30
                drcut=0.4
            for ijet, jet_ in enumerate(c.Jets):
                jet = jet_.Clone()
                if jecup: jet*=1.0/(1-c.Jets_jecUnc[ijet])
                if (jet.Pt()>jt and jet.DeltaR(track)<drcut):
                    isjet = True
                    break    
        
            dtisrecomu = dtisrecomu and isjet
            if isjet and not dtisrecomu: continue
            if not (c.tracks_passPFCandVeto[itrack] or dtisrecomu): continue
        
            #if c.tracks_trackJetIso[itrack]<0.2: 
            #    continue        
        
            dedxRaw = c.tracks_deDxHarmonic2pixel[itrack]
            isfast = True
            if isfast:
                if dedxRaw>4: dedxRaw = p_dedxFastCorrection.Interpolate(min(99,dedxRaw))
                else: dedxRaw = dedxRaw
            if dtlength==1: 
                nShort+=1
            if dtlength==2: 
                nLong+=1            
            if abs(track.Eta())<1.5: dedxcalib = dedxcalib_barrel
            else: dedxcalib = dedxcalib_endcap
    
            if exomode:
                print 'here we are'
                if not passesExtraExoCuts(track, itrack, c): continue
                print 'we made it'
          
            
            
            dedx = dedxcalib*dedxRaw
            if (not isdata) and doDedxSmear:
                smearfactor = fsmear_barrel.GetRandom()
                dedx = dedx + smearfactor
                dedxUp= dedx + 2*smearfactor
        
            passdt+=1
            #print 'got one! bringing the total up to', 1.0*passdt/totdt            
            disappearingTracks.append([track,dtlength,dedx, mva, dtisrecomu, c.tracks_nMissingOuterHits[itrack], itrack])        


        if not len(disappearingTracks)>0: continue

        RecoElectrons = []
        for iel, ele in enumerate(c.Electrons):
            if debugmode: print ientry, iel,'ele with Pt' , ele.Pt()
            if not abs(ele.Eta())<2.4: continue
            if debugmode: print 'passed eta and Pt'
            if not c.Electrons_passIso[iel]: continue
            if not c.Electrons_tightID[iel]: continue
            if ele.Pt()>40: RecoElectrons.append([ele, iel])


        RecoMuons = []
        for imu, lep in enumerate(c.Muons):
            if not abs(lep.Eta())<2.4: continue
            if not c.Muons_passIso[imu]: continue
            if not c.Muons_mediumID[imu]: continue
            if lep.Pt()>40: RecoMuons.append([lep,imu])    


        metvec = TLorentzVector()
        metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region
              
              
        dt, length1, dedxPixel, mvascore, dtisrecomu, MOH, itrack = disappearingTracks[0]
        if len(disappearingTracks)>1:
            dt2, length2, dedxPixel2, mvascore2, dtisrecomu2, MOH2, itrack2 = disappearingTracks[1]
        else: dt2, length2, dedxPixel2, mvascore2, dtisrecomu2, MOH2, itrack2 = -1, -1, -1, 99, -1, -1, -1

        pt = dt.Pt()
        eta = abs(dt.Eta()) 
        DedxMass = TMath.Sqrt((dedxPixel-3.01)*pow(pt*TMath.CosH(eta),2)/1.74)#TMath.Log10(...)
                      

        adjustedBTags = 0        
        adjustedJets = []
        adjustedHt = 0
        adjustedMht = TLorentzVector()
        adjustedMht.SetPxPyPzE(0,0,0,0)
        passJetID = True
        for ijet, jet_ in enumerate(c.Jets):
            jet = jet_.Clone()
            if jecup: jet*=1.0/(1-c.Jets_jecUnc[ijet])
            if not jet.Pt()>30: continue            
            if not abs(jet.Eta())<5.0: continue
            someoverlap = False
            for dt_ in disappearingTracks: 
                if jet.DeltaR(dt_[0])<0.4: 
                    someoverlap = True
                    break
            if someoverlap: continue
            adjustedMht-=jet        
            if not abs(jet.Eta())<2.4: continue
            adjustedHt+=jet.Pt()
            islep = False
            for ilep, lep in enumerate(RecoMuons+RecoElectrons):
                drlep = min(drlep, lep[0].DeltaR(jet))
                if drlep<0.4: 
                    islep = True
                    break
            if islep: continue           
            passJetID = c.Jets_ID[ijet]
            if not passJetID: break
            adjustedJets.append(jet)            
            if c.Jets_bJetTagDeepCSVBvsAll[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
            
        if not passJetID: continue
        adjustedNJets = len(adjustedJets)
        mindphi = 4
        for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht))) 

        newmetvec = metvec.Clone()
        newmetvec-=dt
        if len(RecoElectrons)>0: 
            #mT = c.Electrons_MTW[RecoElectrons[0][1]]
            mT = TMath.Sqrt(2*RecoElectrons[0][0].Pt()*adjustedMht.Pt()*(1-TMath.Cos(RecoElectrons[0][0].DeltaPhi(adjustedMht))))
            dt__ = dt.Clone()
            mtautau = mttsam1_(newmetvec, RecoElectrons[0][0], dt__)
            if c.Electrons_charge[RecoElectrons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoElectrons[0][0]+dt__).M()
            else: invmass = 999        
            leppt = RecoElectrons[0][0].Pt()
        elif len(RecoMuons)>0: 
            #mT = c.Muons_MTW[RecoMuons[0][1]]
            mT = TMath.Sqrt(2*RecoMuons[0][0].Pt()*adjustedMht.Pt()*(1-TMath.Cos(RecoMuons[0][0].DeltaPhi(adjustedMht))))
            dt__ = dt.Clone()
            mtautau = mttsam1_(newmetvec, RecoMuons[0][0], dt__)
            if c.Muons_charge[RecoMuons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoMuons[0][0]+dt__).M()
            else: invmass = 999
            leppt = RecoMuons[0][0].Pt()
        else: 
            mT = 999
            invmass = 999
            DrJetDt = 999
            mtautau = 999
            leppt = 999    

        DrJetDt = c.tracks_trackJetIso[itrack]
        matchedcalo = c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]#/TMath.CosH(c.tracks[disappearingTracks[0][-1]].Eta())
        #matchedcalofrac = 100*c.tracks_matchedCaloEnergy[disappearingTracks[0][-1]]/(dt.P())
    
        if abs(disappearingTracks[0][1])==1: matchedcalofrac = max(matchedcalo,100*matchedcalo/(dt.P()))
        else: matchedcalofrac = 100*matchedcalo/(dt.P())

        dphiMhtDt = abs(adjustedMht.DeltaPhi(dt))
        mhtWithTrack = adjustedMht.Clone()
        mhtWithTrack-=dt
        mtDtMht = TMath.Sqrt(2*dt.Pt()*mhtWithTrack.Pt()*(1-TMath.Cos(mhtWithTrack.DeltaPhi(dt))))
    
        if adjustedMht.Pt()>100:
            totmt+=1
            #if dphiMhtDt>0.05: passmt+=1
            #if c.tracks_trackJetIso[itrack]>0.3: passmt+=1
            if bool(c.tracks_trackJetIso[itrack]>0.2): passmt+=1
    
    
        
        fv = [adjustedHt, adjustedMht.Pt(), adjustedNJets,adjustedBTags, len(disappearingTracks), abs(length1)-1, mindphi, dedxPixel, len(RecoElectrons), len(RecoMuons), invmass, mT, pt, eta, matchedcalofrac, dtisrecomu, dphiMhtDt, mvascore,  mvascore2,  mtDtMht, MOH, leppt, DrJetDt]#'''*TMath.CosH(eta)
        fv.append(getBinNumber(fv))
        fv.extend([GetMinDeltaPhiMhtHemJets(adjustedJets,adjustedMht),mtautau,c.NVtx, DedxMass])
        
        if debugmode and (not jecup):
            if dtlength==1: print ientry, 'short track_mva_sep21v1_baseline', mvascore, 'pT =', dt.Pt(), 'bin number =', getBinNumber(fv)
            if dtlength==2: print ientry, 'long  track_mva_sep21v1_baseline', mvascore, 'pT =', dt.Pt(), 'bin number =', getBinNumber(fv)    
    
        if abs(disappearingTracks[0][1])==1:
            mctot+=1
            if matchedcalofrac<15: mcpass+=1
            

        lepsf = 1.0
        if isdata: 
            weight = 1
        else:
            if dtlength==1: weight = 0.8*xsecpb # fastsim scale factor
            else: weight = 0.95*xsecpb
            weight*=ctauweight
            if len(RecoElectrons)>0: 
                leppt, lepeta = RecoElectrons[0][0].Pt(), RecoElectrons[0][0].Eta()
                binmet, binpt = htrigel.GetXaxis().FindBin(adjustedMht.Pt()), htrigel.GetYaxis().FindBin(leppt)
                wtrignom = htrigel.GetBinContent(binmet, binpt)
                wtrigup = htrigelUp.GetBinContent(binmet, binpt)
                
                yax = eleReco.GetYaxis()
                binpt = min(yax.FindBin(leppt), yax.GetNbins())
                xax = eleReco.GetXaxis()
                bineta = min(xax.FindBin(lepeta), xax.GetNbins())
                lepsf*=eleReco.GetBinContent(bineta, binpt)
                
                yax = eleIdiso.GetYaxis()
                binpt = min(yax.FindBin(leppt), yax.GetNbins())
                xax = eleIdiso.GetXaxis()
                bineta = min(xax.FindBin(lepeta), xax.GetNbins())
                lepsf*=eleIdiso.GetBinContent(bineta, binpt)    
                
                yax = eleIdFastFull.GetYaxis()
                binpt = min(yax.FindBin(leppt), yax.GetNbins())
                xax = eleIdFastFull.GetXaxis()
                bineta = min(xax.FindBin(lepeta), xax.GetNbins())
                lepsf*=eleIdFastFull.GetBinContent(bineta, binpt)
                                
        
            elif len(RecoMuons)>0:
            
                leppt, lepeta = RecoMuons[0][0].Pt(), RecoMuons[0][0].Eta()
                
                binmet, binpt = htrigmu.GetXaxis().FindBin(adjustedMht.Pt()), htrigmu.GetYaxis().FindBin(leppt)
                wtrignom = htrigmu.GetBinContent(binmet, binpt)
                wtrigup = htrigmuUp.GetBinContent(binmet, binpt)
                
                xax = muIdiso.GetXaxis()
                binpt = min(xax.FindBin(leppt), xax.GetNbins())
                yax = muIdiso.GetYaxis()
                bineta = min(yax.FindBin(lepeta), yax.GetNbins())
                lepsf*=muIdiso.GetBinContent(binpt, bineta)    
                
                xax = muIdFastFull.GetXaxis()
                binpt = min(xax.FindBin(leppt), xax.GetNbins())
                yax = muIdFastFull.GetYaxis()
                bineta = min(yax.FindBin(lepeta), yax.GetNbins())
                lepsf*=muIdFastFull.GetBinContent(binpt, bineta)
                                    
            else: 
                wtrignom = gtrig.GetEfficiency(gtrig.FindFixBin(c.MHT))
                wtrigup = wtrignom-gtrigDown.GetEfficiencyErrorLow(gtrig.FindFixBin(c.MHT))
                binmht = htrigmht.GetXaxis().FindBin(adjustedMht.Pt())
                wtrignom = htrigmht.GetBinContent(binmht)
                wtrigup = htrigmht_up.GetBinContent(binmht)                
                
        weight*=lepsf
    
        pfweight = 1.0
        for jet in c.Jets:
            pt, eta = xaxprefiring.FindBin(jet.Pt()), yaxprefiring.FindBin(abs(jet.Eta()))
            gbin = hprefireDerived.GetBin(pt, eta, -1)
            pfweight*=(1-hprefiring.GetEfficiency(gbin))
    
        #print fv
        #for ifv in range(len(fv)): print ifv, varlist_[ifv], fv[ifv]    
        
        if issignal:
           sfbtagnom = get_btag_weight(c,nSigmaBtagSF=0,nSigmaBtagFastSimSF=0,isFastSim=1,readerBtag=readerBtag)
           sfbtagup = get_btag_weight(c,nSigmaBtagSF=1,nSigmaBtagFastSimSF=0,isFastSim=1,readerBtag=readerBtag)
           sfbtagdown = get_btag_weight(c,nSigmaBtagSF=-1,nSigmaBtagFastSimSF=0,isFastSim=1,readerBtag=readerBtag)
        else: sfbtagnom, sfbtagup, sfbtagdown = 1,1,1
        
        sfpunom = c.puWeight
        sfpuup = c.puSysUp
        sfpudown = c.puSysDown
    
        isrnom, isrup, isrdown = get_isr_weight(c)
        
        if dtlength==1:
            sfdtnom = hdtscalefactor_short.GetBinContent(dtsfbin_)
            sfdtshortup = hdtscalefactor_short.GetBinContent(dtsfbin_)+hdtscalefactor_short.GetBinError(dtsfbin_)
            sfdtlongup = hdtscalefactor_short.GetBinContent(dtsfbin_) #wrong length variation should just be nominal
        else:
            sfdtnom = hdtscalefactor_long.GetBinContent(dtsfbin_)
            sfdtshortup = hdtscalefactor_long.GetBinContent(dtsfbin_) #wrong length variation should just be nominal
            sfdtlongup = hdtscalefactor_long.GetBinContent(dtsfbin_)+hdtscalefactor_long.GetBinError(dtsfbin_)            

        for regionkey in regionCuts:
            if not 'Nom' in regionkey: continue
            for ivar, varname in enumerate(varlist_):
                if not varname in vars2draw: continue
                if selectionFeatureVector(fv,regionkey,varname):
                    if 'Baseline' in regionkey and varname=='BinNumber': print 'were in the SR hist', ientry, regionkey
                    #weightsysts = ['Nom','BTagUp','BTagDown','IsrUp','IsrDown']            
                    if ivar==srindex and jecup: 
                        fillth1(histoStructDict[regionkey.replace('Nom','JecUp')+'_'+varname].Truth,fv[ivar], sfbtagnom*isrnom*sfpunom*wtrignom*sfdtnom*weight)
                        continue
                    fillth1(histoStructDict[regionkey+'_'+varname].Truth,fv[ivar], sfbtagnom*isrnom*sfpunom*wtrignom*sfdtnom*weight)
                    if not srindex==ivar: continue
                    fillth1(histoStructDict[regionkey.replace('Nom','BTagUp')+'_'+varname].Truth,fv[ivar],      sfbtagup   *isrnom  *sfpunom  *wtrignom *sfdtnom     *weight)
                    fillth1(histoStructDict[regionkey.replace('Nom','BTagDown')+'_'+varname].Truth,fv[ivar],    sfbtagdown *isrnom  *sfpunom  *wtrignom *sfdtnom     *weight)
                    fillth1(histoStructDict[regionkey.replace('Nom','IsrUp')+'_'+varname].Truth,fv[ivar],       sfbtagnom  *isrup   *sfpunom  *wtrignom *sfdtnom     *weight)
                    fillth1(histoStructDict[regionkey.replace('Nom','IsrDown')+'_'+varname].Truth,fv[ivar],     sfbtagnom  *isrdown *sfpunom  *wtrignom *sfdtnom     *weight)
                    fillth1(histoStructDict[regionkey.replace('Nom','PuUp')+'_'+varname].Truth,fv[ivar],        sfbtagnom  *isrnom  *sfpuup   *wtrignom *sfdtnom     *weight)
                    fillth1(histoStructDict[regionkey.replace('Nom','PuDown')+'_'+varname].Truth,fv[ivar],      sfbtagnom  *isrnom  *sfpudown *wtrignom *sfdtnom     *weight)
                    fillth1(histoStructDict[regionkey.replace('Nom','TrigUp')+'_'+varname].Truth,fv[ivar],      sfbtagnom  *isrnom  *sfpunom  *wtrigup  *sfdtnom     *weight)
                    fillth1(histoStructDict[regionkey.replace('Nom','DtSfShortUp')+'_'+varname].Truth,fv[ivar], sfbtagnom  *isrnom  *sfpunom  *wtrignom *sfdtshortup *weight)                    
                    fillth1(histoStructDict[regionkey.replace('Nom','DtSfLongUp')+'_'+varname].Truth,fv[ivar],  sfbtagnom  *isrnom  *sfpunom  *wtrignom *sfdtlongup  *weight )
                    fillth1(histoStructDict[regionkey.replace('Nom','Prefire')+'_'+varname].Truth,fv[ivar],     sfbtagnom  *isrnom  *sfpunom  *wtrignom *sfdtnom     *weight *pfweight)
                    fillth1(histoStructDict[regionkey.replace('Nom','ScaleUp')+'_'+varname].Truth,fv[ivar],     sfbtagnom  *isrnom  *sfpunom  *wtrignom *sfdtnom     *weight *scaleup)
                    fillth1(histoStructDict[regionkey.replace('Nom','ScaleDown')+'_'+varname].Truth,fv[ivar],   sfbtagnom  *isrnom  *sfpunom  *wtrignom *sfdtnom     *weight*scaledown)                                                        
                fv[dedxidx] = dedxUp
                if selectionFeatureVector(fv,regionkey,varname):    
                    if jecup: continue        
                    fillth1(histoStructDict[regionkey.replace('Nom','DedxUp')+'_'+varname].Truth,fv[ivar],    sfbtagnom*isrnom*sfpunom*wtrignom*weight)
                
                
fnew_.cd()
hHt.Write()
hHtWeighted.Write()
writeHistoStruct(histoStructDict, 'truth')
print 'we done! just created', fnew_.GetName()
fnew_.Close()    
fMask.Close()
os.abort()



