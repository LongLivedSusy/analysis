from ROOT import *

def prepareReaderBtagSF():
    # load b tag sf from csv file
    import ROOT
    
    ## from within CMSSW:
    ROOT.gSystem.Load('libCondFormatsBTauObjects') 
    ROOT.gSystem.Load('libCondToolsBTau') 

    # OR using standalone code:
    #ROOT.gROOT.ProcessLine('.L ./BTagCalibrationStandalone.cpp+')
    
    # get the sf data loaded 
    calib = ROOT.BTagCalibration('deepcsv', './DeepCSV_Moriond17_B_H.csv')

    # making a std::vector<std::string>> in python is a bit awkward, 
    # but works with root (needed to load other sys types):
    v_sys = getattr(ROOT, 'std::vector<string>')()
    v_sys.push_back('up')
    v_sys.push_back('down')
    
    # make a reader instance and load the sf data
    global readerBtag
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

def calc_btag_weight(tree,nSigmaBtagSF,nSigmaBtagFastSimSF,isFastSim):
    #fbeff = TFile("./BTagEfficiency_Summer16_TTJets.root")
    fbeff = TFile("./g1800_chi1400_27_200970_step4_100_DeepCSVM_bTaggingEfficiencyMap.root")
    pMC = 1.0
    pData = 1.0
    
    # jet loop start here
    for ijet, jet in enumerate(tree.Jets):
	if not (abs(jet.Eta())<2.4 and jet.Pt()>30): continue
	
	if jet.Pt() >= 1000 : JetPt = 999.
	else : JetPt = jet.Pt()
       
        eff = 1.0
	# b tag efficiency
	if tree.Jets_hadronFlavor[ijet]== 5: # truth b particle
	    heff = fbeff.Get("eff_b")
	    binx = heff.GetXaxis().FindBin(JetPt)
	    biny = heff.GetYaxis().FindBin(jet.Eta())
	    eff = heff.GetBinContent(binx,biny)
	    FLAV = 0
	    #print 'b jetpt : ', JetPt, "jeteta:",jet.Eta()," binx:",binx,", biny:",biny,"eff:",eff
        elif tree.Jets_hadronFlavor[ijet]== 4: # truth c particle
	    heff = fbeff.Get("eff_c")
	    binx = heff.GetXaxis().FindBin(JetPt)
            biny = heff.GetYaxis().FindBin(jet.Eta())
	    eff = heff.GetBinContent(binx,biny)
	    FLAV = 1
	    #print 'c jetpt : ', JetPt, "jeteta:",jet.Eta()," binx:",binx,", biny:",biny,"eff:",eff
        else : # truth udsg particle
	    heff = fbeff.Get("eff_udsg")
	    binx = heff.GetXaxis().FindBin(JetPt)
	    biny = heff.GetYaxis().FindBin(jet.Eta())
	    eff = heff.GetBinContent(binx,biny)
	    FLAV = 2
	    #print 'udsg jetpt : ', JetPt, "jeteta:",jet.Eta()," binx:",binx,", biny:",biny,"eff:",eff
	    
	sf_cen = readerBtag.eval_auto_bounds(
	    'central',      # systematic (here also 'up'/'down' possible)
	    FLAV,              # jet flavor
	    abs(jet.Eta()),      # absolute value of eta
	    JetPt        # pt
	)
	sf_up = readerBtag.eval_auto_bounds(
	    'up',           # systematic (here also 'up'/'down' possible)
	    FLAV,              # jet flavor
	    abs(jet.Eta()),      # absolute value of eta
	    JetPt        # pt
	)
	sf_down = readerBtag.eval_auto_bounds(
	    'down',         # systematic (here also 'up'/'down' possible)
	    FLAV,              # jet flavor
	    abs(jet.Eta()),      # absolute value of eta
	    JetPt        # pt
	)
	#print '%sth jet pt : %.2f, eta : %.2f, flavor : %s, sf_cen : %.2f, sf_up : %.2f, sf_down : %.2f'%(ijet,JetPt,jet.Eta(),tree.Jets_hadronFlavor[ijet],sf_cen,sf_up,sf_down)
	
	sf = get_syst(sf_cen, sf_up, sf_down, nSigmaBtagSF)

	if tree.Jets_bDiscriminatorCSV[ijet]>csv_b :
	    pMC *= eff
	    pData *= eff*sf
        else :
	    pMC *= 1 - eff
	    pData *= 1 - eff*sf
    
    weight = pData / pMC
    return weight

def get_syst(weight_nominal,weight_up,weight_down,nSigma):
    w = weight_nominal
    if nSigma==0 : return w
    else :
	dw_up = weight_up - weight_nominal
	dw_down = weight_nominal - weight_down
	if nSigma >= 0. :
	    w += nSigma*dw_up
	else : w += nSigma*dw_down
    return w

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
	    scaleJER = get_syst(tree.Jets_jerFactor[ijet],tree.Jets_jerFactorUp[ijet],tree.Jets_jerFactorDown[ijet],nSigmaJER)
	    newjet_Pt *= scaleJER
	    newjet_E *= scaleJER
	newjet.SetPtEtaPhiE(newjet_Pt, jet.Eta(), jet.Phi(), newjet_E)
	jets_syst.append(newjet)
    return jets_syst

def get_isr_weight(tree,nSigmaISR):
    w = 1
    fname = tree.GetFile().GetName()
    #d = 1.0	# Before determine D value
    #d = 1.121	# T2tt
    if 'g1800_chi1400' in fname : d = 1.15598 # g1800_chi1400
    else : d = 1
    n = tree.NJetsISR
    w_nom = 0
    
    if   n==0 : w_nom = d
    elif n==1 : w_nom = d * 0.920
    elif n==2 : w_nom = d * 0.821
    elif n==3 : w_nom = d * 0.715
    elif n==4 : w_nom = d * 0.662
    elif n==5 : w_nom = d * 0.561
    else      : w_nom = d * 0.511
    err = (1-w_nom)/2
    w_isr_up   = w_nom + err
    w_isr      = w_nom
    w_isr_down = w_nom - err
    w = get_syst(w_isr, w_isr_up, w_isr_down, nSigmaISR)
    return w
