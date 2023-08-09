import os, sys
from ROOT import *

def read_sigmas(sigmas_txt):
    sigmas_dict = {}

    with open (sigmas_txt, 'r') as fsyst:
        while True :
            line = fsyst.readline().strip()
            if not line : break
            if line.startswith('#') : continue #To ignore commented line in txt file
            line = line.split()
            
            sigmas_dict[line[0]] = [int(line[1]), int(line[2]), int(line[3]), int(line[4])]
    
    return sigmas_dict

def prepareReaderBtagSF():
    # load b tag sf from csv file
    import ROOT
    
    ## from within CMSSW:
    ROOT.gSystem.Load('libCondFormatsBTauObjects') 
    ROOT.gSystem.Load('libCondToolsBTau') 

    # OR using standalone code:
    #ROOT.gROOT.ProcessLine('.L ./BTagCalibrationStandalone.cpp+')
    
    # get the sf data loaded 
    calib = ROOT.BTagCalibration('deepcsv', '../../systematics/DeepCSV_Moriond17_B_H.csv')

    # making a std::vector<std::string>> in python is a bit awkward, 
    # but works with root (needed to load other sys types):
    v_sys = getattr(ROOT, 'std::vector<string>')()
    v_sys.push_back('up')
    v_sys.push_back('down')
    
    # make a reader instance and load the sf data
    readerBtag = ROOT.BTagCalibrationReader(
        1,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
        "central",      # central systematic type
        v_sys,          # vector of other sys. types
    ) 
    
    readerBtag.load(
        calib, 
        0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
        "comb"      # measurement type
    )
    
    readerBtag.load(
        calib, 
        1,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
        "comb"      # measurement type
    )
    
    readerBtag.load(
        calib, 
        2,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
        "incl"      # measurement type
    )

    return readerBtag
    

def get_btag_weight(tree,nSigmaBtagSF,nSigmaBtagFastSimSF,isFastSim,readerBtag):
    
    ## Get Btagging efficiency map for signal sample
    if 'T1' in tree.GetFile().GetName() : 
        fbeff = TFile("../../systematics/BtagEffMaps/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_merged.root")
    elif 'T2' in tree.GetFile().GetName() or 'iggsino' in tree.GetFile().GetName() or 'T2tb' in tree.GetFile().GetName() or 'PMSSM' in tree.GetFile().GetName():
        fbeff = TFile("../../systematics/BtagEffMaps/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_merged.root")
    else : 
        print 'Cannot choose efficiency map for this sample, quit'
        abc = abc
        quit()
        
    pMC = 1.0
    pData = 1.0

    csv_b = 0.6324 # 2016 DeepCSVM
    
    # jet loop start here
    for ijet, jet in enumerate(tree.Jets):
        if not tree.Jets_ID[ijet] : continue
        if not (abs(jet.Eta())<2.4 and jet.Pt()>30): continue
        
        eff = 1.0
        # b tag efficiency
        if tree.Jets_hadronFlavor[ijet]== 5: # truth b particle
            heff = fbeff.Get("efficiency_b")
            binx = heff.GetXaxis().FindBin(min(999,jet.Pt()))
            biny = heff.GetYaxis().FindBin(jet.Eta())
            eff = heff.GetBinContent(binx,biny)
            FLAV = 0
            #print 'b jetpt : ', jet.Pt(), "jeteta:",jet.Eta()," binx:",binx,", biny:",biny,"eff:",eff
        elif tree.Jets_hadronFlavor[ijet]== 4: # truth c particle
            heff = fbeff.Get("efficiency_c")
            binx = heff.GetXaxis().FindBin(min(999,jet.Pt()))
            biny = heff.GetYaxis().FindBin(jet.Eta())
            eff = heff.GetBinContent(binx,biny)
            FLAV = 1
            #print 'c jetpt : ', jet.Pt(), "jeteta:",jet.Eta()," binx:",binx,", biny:",biny,"eff:",eff
        elif tree.Jets_hadronFlavor[ijet]== 0: # truth udsg particle
            heff = fbeff.Get("efficiency_udsg")
            binx = heff.GetXaxis().FindBin(min(999,jet.Pt()))
            biny = heff.GetYaxis().FindBin(jet.Eta())
            eff = heff.GetBinContent(binx,biny)
            FLAV = 2  
            #print 'udsg jetpt : ', jet.Pt(), "jeteta:",jet.Eta()," binx:",binx,", biny:",biny,"eff:",eff
        else : print 'wired Jets_hadronFlavor : ', tree.Jets_hadronFlavor[ijet]
           
        sf_cen = readerBtag.eval_auto_bounds(
            'central',      # systematic (here also 'up'/'down' possible)
            FLAV,              # jet flavor
            abs(jet.Eta()),      # absolute value of eta
            jet.Pt()        # pt
        )
        sf_up = readerBtag.eval_auto_bounds(
            'up',           # systematic (here also 'up'/'down' possible)
            FLAV,              # jet flavor
            abs(jet.Eta()),      # absolute value of eta
            jet.Pt()        # pt
        )
        sf_down = readerBtag.eval_auto_bounds(
            'down',         # systematic (here also 'up'/'down' possible)
            FLAV,              # jet flavor
            abs(jet.Eta()),      # absolute value of eta
            jet.Pt()        # pt
        )
        #print '%sth jet pt : %.2f, eta : %.2f, flavor : %s, sf_cen : %.2f, sf_up : %.2f, sf_down : %.2f'%(ijet,jet.Pt(),jet.Eta(),tree.Jets_hadronFlavor[ijet],sf_cen,sf_up,sf_down)
        
        if nSigmaBtagSF>0.0001: sf = sf_up
        elif nSigmaBtagSF<0.0001: sf = sf_down
        else: sf = sf_cen

        if tree.Jets_bDiscriminatorCSV[ijet]>csv_b :
            pMC *= eff
            pData *= eff*sf
        else :
            pMC *= 1 - eff
            pData *= 1 - eff*sf
    
    try:weight = pData / pMC
    except:
            print 'pMC was 0', pMC
            print tree.BTags
            weight = pData / pMC
    return weight


def get_syst_jes(weight_nominal,uncertainty,nSigma):
    w = weight_nominal
    if not nSigma==0.: 
        w*= 1.0 + nSigma*uncertainty
    return w

def jets_rescale_smear(tree,applySmearing,nSigmaJES,nSigmaJER):
    jets_syst = []
    for ijet, jet in enumerate(tree.Jets):
        newjet = jet.Clone()
        scaleJES = get_syst_jes(1.0,tree.Jets_jecUnc[ijet],nSigmaJES)
        newjet_Pt = jet.Pt() * scaleJES
        newjet_E = jet.E() * scaleJES
        if applySmearing : 
            if nSigmaJER>0.001: scaleJER = tree.Jets_jerFactorUp[ijet]
            elif nSigmaJER<0.001: scaleJER = tree.Jets_jerFactorDown[ijet]
            else: scaleJER = tree.Jets_jerFactor[ijet]
            newjet_Pt *= scaleJER
            newjet_E *= scaleJER
        newjet.SetPtEtaPhiE(newjet_Pt, jet.Eta(), jet.Phi(), newjet_E)
        jets_syst.append(newjet)
    return jets_syst

def get_isr_weight(tree):
    # Ana's talk : https://indico.cern.ch/event/592621/contributions/2398559/attachments/1383909/2105089/16-12-05_ana_manuelf_isr.pdf
    isewk = True    
    w = 1
    fname = tree.GetFile().GetName()
    #d = 1.0        # Before determine D value
    #if 'g1800_chi1400' in fname : d = 1.15598 # g1800_chi1400
    if 'T1' in fname : 
        isewk = False
        d = 1.123 # T1qqqq
    elif 'T2' in fname: 
        isewk = False
        d = 1.121 # T2tt
    else : d = 0.928 # assume electroweak SUSY model
    
    if isewk:
        ptisr = (tree.GenParticles[2]+tree.GenParticles[3]).Pt()
        if ptisr in [0,50]: w_nom = d
        elif ptisr<100: w_nom = d * 1.052
        elif ptisr<150: w_nom = d * 1.179
        elif ptisr<200: w_nom = d * 1.150
        elif ptisr<300: w_nom = d * 1.057
        elif ptisr<400: w_nom = d * 1.000 
        elif ptisr<600: w_nom = d * 0.912 
        else: w_nom = d * 0.783
        
    else:
        n = tree.NJetsISR
        w_nom = 0.0
        if   n==0 : w_nom = d
        elif n==1 : w_nom = d * 0.920
        elif n==2 : w_nom = d * 0.821
        elif n==3 : w_nom = d * 0.715
        elif n==4 : w_nom = d * 0.662
        elif n==5 : w_nom = d * 0.561
        elif n>=6 : w_nom = d * 0.511
        else : print 'Invalid NISR?' 

    err = (1-w_nom)/2
    w_isr_up   = w_nom + err
    w_isr      = w_nom
    w_isr_down = w_nom - err
    return w_isr, w_isr_up, w_isr_down
    
    
#time to add some systmatics stuff
def getRecoIdisoFastfullLeptonSFhistos(year='2017'):
        yearmodthou = year.replace('20','')
        f = TFile('../../systematics/leptonscalefactors/egammaEffi.txt_EGM2D_RECO'+year+'.root')
        eleReco = f.Get('EGamma_EffMC2D')
        print 'eleReco.GetBinContent(1,1)', eleReco.GetBinContent(1,1)
        eleReco.SetDirectory(0)
        f.Close()
        
        f = TFile('../../systematics/leptonscalefactors/ElectronScaleFactors_Run'+year+'.root')
        eleIdiso = f.Get('Run'+year+'_CutBasedTightNoIso94XV2')
        print 'eleIdiso.GetBinContent(1,1)', eleIdiso.GetBinContent(1,1)        
        eleIdiso.SetDirectory(0)
        f.Close()
        
        
        f = TFile('../../systematics/leptonscalefactors/detailed_ele_full_fast_sf_'+yearmodthou+'.root')
        eleIdFastFull = f.Get('CutBasedTightNoIso94XV2_sf')
        print 'eleIdiso.GetBinContent(1,1)', eleIdFastFull.GetBinContent(1,1)        
        eleIdFastFull.SetDirectory(0)
        f.Close()
        
        
        f = TFile('../../systematics/leptonscalefactors/'+year+'_MuonMediumIdIso_SUS.root')
        if year=='2016': muIdIso = f.Get('SF')
        else: muIdIso = f.Get('TnP_MC_NUM_MiniIso02Cut_DEN_MediumID_PAR_pt_eta')
        print 'muIdIso.GetBinContent(1,1)', muIdIso.GetBinContent(1,1)        
        muIdIso.SetDirectory(0)
        f.Close()
        
        f = TFile('../../systematics/leptonscalefactors/detailed_mu_full_fast_sf_'+yearmodthou+'.root')
        muIdFastFull = f.Get('miniIso02_MediumId_sf')
        print 'muIdFastFull.GetBinContent(1,1)', muIdFastFull.GetBinContent(1,1)        
        muIdFastFull.SetDirectory(0)
        f.Close()
                                                
        return eleReco, eleIdiso, eleIdFastFull, muIdIso, muIdFastFull
        
        
                
        




