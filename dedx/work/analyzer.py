import os,sys
import argparse
import json
from ROOT import *
from shared_utils import *

def prepareReader(xmlfilename, vars_training, vars_spectator, tmva_variables):

    # general set up training/spectator variables for TMVA

    reader = TMVA.Reader()
    for label in vars_training + vars_spectator:
        if label not in tmva_variables:
            tmva_variables[label] = array('f',[0])

    for label in vars_training:
        reader.AddVariable(label, tmva_variables[label])
    for label in vars_spectator:
        reader.AddSpectator(label, tmva_variables[label])
    reader.BookMVA("BDT", xmlfilename)

    return reader


def get_tmva_info(path):

    # get information about a TMVA macro

    training_variables = []
    spectator_variables = []
    preselection = ""
    method = ""
    configuration = ""
    count_mycutb = 0
    
    with open(path + "/tmva.cxx", 'r') as tmva_macro:
        for line in tmva_macro.readlines():
            if "AddVariable" in line and "//" not in line.split()[0]:
                variable = line.split('"')[1]
                training_variables.append(variable)
            elif "AddSpectator" in line and "//" not in line.split()[0]:
                spectator_variables.append(line.split('"')[1])
            elif 'mycutb=("' in line and "Entry" not in line and "//" not in line.split()[0]:
                preselection = line.split('"')[1]
            elif "BookMethod" in line and "//" not in line.split()[0]:
                method = line.split('"')[1]
                configuration = line.split('"')[3]
                configuration = configuration.replace(":", ", ")

    return {"method": method, "configuration": configuration, "variables": training_variables, "spectators": spectator_variables, "preselection": preselection}


def pass_background_stitching(current_file_name, madHT, phase):
    if (madHT>0) and \
       ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
       ("WJetsToLNu_TuneCUETP8M1_13TeV" in current_file_name and madHT>100) or \
       (phase == 1 and "TTJets_Tune" in current_file_name and madHT>600) or \
       ("HT-100to200_" in current_file_name and (madHT<100 or madHT>200)) or \
       ("HT-200to300_" in current_file_name and (madHT<200 or madHT>300)) or \
       ("HT-200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
       ("HT-300to500_" in current_file_name and (madHT<300 or madHT>500)) or \
       ("HT-400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
       ("HT-600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
       ("HT-800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
       ("HT-1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
       ("HT-2500toInf_" in current_file_name and madHT<2500) or \
       ("HT-500to700_" in current_file_name and (madHT<500 or madHT>700)) or \
       ("HT-700to1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
       ("HT-1000to1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
       ("HT-1500to2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
       ("HT-100To200_" in current_file_name and (madHT<100 or madHT>200)) or \
       ("HT-200To300_" in current_file_name and (madHT<200 or madHT>300)) or \
       ("HT-200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
       ("HT-300To500_" in current_file_name and (madHT<300 or madHT>500)) or \
       ("HT-400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
       ("HT-500To700_" in current_file_name and (madHT<500 or madHT>700)) or \
       ("HT-600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
       ("HT-700To1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
       ("HT-800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
       ("HT-1000To1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
       ("HT-1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
       ("HT-1500To2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
       ("HT-2500ToInf_" in current_file_name and madHT<2500):
        return False
    else:
        return True
                

def particle_is_in_HEM_failure_region(particle):

    eta = particle.Eta()
    phi = particle.Phi()

    if -3.2<eta and eta<-1.2 and -1.77<phi and phi<-0.67:
        return True
    else:
        return False


def get_highest_HEM_object_pt(objects):

    # check HEM failure for electrons and jets:
    highestPt = 0
    for particle in objects:
        if particle_is_in_HEM_failure_region(particle):
            if particle.Pt()>highestPt:
                highestPt = particle.Pt()
    return highestPt


def get_minDeltaPhi_MHT_HEMJets(objects, MHT):

    lowestDPhi = 10
    for jet in objects:
        if not jet.Pt()>30: continue
        if particle_is_in_HEM_failure_region(jet):
            if abs(jet.DeltaPhi(mht))<lowestDPhi:
                lowestDPhi = abs(jet.DeltaPhi(mht))
    if lowestDPhi<0:
        return 10
    else:
        return lowestDPhi


def load_tmva_readers(phase):
    
    readers = {}
    if phase == 0:
        bdts = {
                #"bdt-short": "../../disappearing-track-tag/2016-short-tracks",
                #"bdt-long": "../../disappearing-track-tag/2016-long-tracks",
                "bdt_loose-short": "../../disappearing-track-tag/2016-short-tracks-loose",
                "bdt_loose-long": "../../disappearing-track-tag/2016-long-tracks-loose",
               }
               
    elif phase == 1:
        bdts = {
                #"bdt-short": "../../disappearing-track-tag/2017-short-tracks",
                #"bdt-long": "../../disappearing-track-tag/2017-long-tracks",
                "bdt_loose-short": "../../disappearing-track-tag/2017-short-tracks-loose",
                "bdt_loose-long": "../../disappearing-track-tag/2017-long-tracks-loose",
               }
    
    for label in bdts:
        readers[label] = {}
        readers[label]["tmva_variables"] = {}
        readers[label]["info"] = get_tmva_info(bdts[label])
        readers[label]["reader"] = prepareReader(bdts[label] + '/weights/TMVAClassification_BDT.weights.xml', readers[label]["info"]["variables"], readers[label]["info"]["spectators"], readers[label]["tmva_variables"])

    return readers
    

def get_disappearing_track_score(dt_tag_label, event, itrack, readers, loose = False):
    
    # check TMVA preselection and evaluate BDT score
    
    category = "short"
    is_pixel_track = True
    if event.tracks_trackerLayersWithMeasurement[itrack] > event.tracks_pixelLayersWithMeasurement[itrack]:
        category = "long"
        is_pixel_track = False

    if "loose" in dt_tag_label:
	use_dxy = False
	use_dz = True
	bdt = readers["bdt_loose-%s" % category]
    else:
	use_dxy = True
	use_dz = True
	bdt = readers["bdt-%s" % category]
                
    ptErrOverPt2 = event.tracks_ptError[itrack] / (event.tracks[itrack].Pt()**2)
    
    # check TMVA preselection:
    if is_pixel_track and not (event.tracks[itrack].Pt() > 30 and \
        abs(event.tracks[itrack].Eta()) < 2.4 and \
        event.tracks_trkRelIso[itrack] < 0.2 and \
        (not use_dxy or event.tracks_dxyVtx[itrack] < 0.1) and \
        (not use_dz or event.tracks_dzVtx[itrack] < 0.1) and \
        ptErrOverPt2 < 10 and \
        event.tracks_nMissingMiddleHits[itrack] == 0 and \
        bool(event.tracks_trackQualityHighPurity[itrack]) == 1):
            return -10

    if not is_pixel_track and not (event.tracks[itrack].Pt() > 30 and \
        abs(event.tracks[itrack].Eta()) < 2.4 and \
        event.tracks_trkRelIso[itrack] < 0.2 and \
        (not use_dxy or event.tracks_dxyVtx[itrack] < 0.1) and \
        (not use_dz or event.tracks_dzVtx[itrack] < 0.1) and \
        ptErrOverPt2 < 10 and \
        event.tracks_nMissingOuterHits[itrack] >= 2 and \
        event.tracks_nMissingMiddleHits[itrack] == 0 and \
        bool(event.tracks_trackQualityHighPurity[itrack]) == 1):
            return -10
    
    if not loose:
        bdt = readers["bdt-%s" % category]
    else:
        bdt = readers["bdt_loose-%s" % category]

    if use_dxy:
        bdt["tmva_variables"]["dxyVtx"][0] = event.tracks_dxyVtx[itrack]
    if use_dz:
        bdt["tmva_variables"]["dzVtx"][0] = event.tracks_dzVtx[itrack]
    bdt["tmva_variables"]["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[itrack]
    bdt["tmva_variables"]["trkRelIso"][0] = event.tracks_trkRelIso[itrack]
    bdt["tmva_variables"]["nValidPixelHits"][0] = event.tracks_nValidPixelHits[itrack]
    bdt["tmva_variables"]["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[itrack]
    bdt["tmva_variables"]["ptErrOverPt2"][0] = ptErrOverPt2           

    score = bdt["reader"].EvaluateMVA("BDT")
    
    return score
    
    
def check_is_reco_lepton(event, itrack, deltaR = 0.01):

    reco_lepton = False
    for k in range(len(event.Muons)):
        if event.tracks[itrack].DeltaR(event.Muons[k]) < deltaR:
            reco_lepton = True
    for k in range(len(event.Electrons)):
        if event.tracks[itrack].DeltaR(event.Electrons[k]) < deltaR:
            reco_lepton = True
    return reco_lepton


def pass_pion_veto(event, itrack, deltaR = 0.03):

    # check for nearby pions:
    passpionveto = True
    for k in range(len(event.TAPPionTracks)):
        if event.tracks[itrack].DeltaR(event.TAPPionTracks[k]) < deltaR:
            passpionveto = False
            break
    return passpionveto

def myround(x, base=5):
    return int(base * round(float(x)/base))


def main(inputfiles,output_folder):
    
    # Adding Trees
    c = TChain("TreeMaker2/PreSelection")
    with open(inputfiles,'r') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
           print 'adding %sth file:'%i, line
    	   c.Add(line.rstrip('\n'))
    
    nentries = c.GetEntries()
    print "Total Entries : ",nentries 
    #c.Show(0)
    
    # check if data:
    phase = 0
    data_period = ""
    is_data = False
    for label in ["Run2016", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18"]:
        if label in inputfiles.split('/')[-1]:
            data_period = label
            if "Run201" in label:
                is_data = True
            if label == "Run2016" or label == "Summer16":
                phase = 0
            elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
                phase = 1
    print "Phase:", phase

    #FIXME: no special handling for Autumn18 yet
    if data_period == "Autumn18":
        data_period == "Fall17" 

    if data_period != "":
        print "data_period: %s, phase: %s" % (data_period, phase)
    else:
        print "Can't determine data/MC era!"
        quit(1)

    # load BDTs and fetch list of DT tag labels
    readers = load_tmva_readers(phase)
    
    # load and configure data mask:
    if phase == 0:
        mask_file= TFile("../../tools/usefulthings/Masks.root")
        if is_data : 
            hMask = mask_file.Get("hEtaVsPhiDT_maskData-2016Data-2016")
        else :
            hMask = mask_file.Get("hEtaVsPhiDT_maskMC-2016MC-2016")
        print "Loaded mask:", hMask
    else:
        hMask = '' 
    
    # Output file
    output = inputfiles.split('/')[-1]+".root" 
    fout = TFile(output_folder+'/'+output, "recreate")

    # write number of events to histogram:
    nev = c.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()


    # Histograms
    hHT_unweighted = TH1F('hHT_unweighted','hHT_unweighted',200,0,10000)
    hHT = TH1F('hHT','hHT',200,0,10000)


    # Event loop
    updateevery = 10000
    #for ientry in range(nentries):
    for ientry in range(100):
	
	if ientry%updateevery==0:
    	    print 'now processing event number', ientry, 'of', nentries
	
	c.GetEntry(ientry)
	
	# Counting histogram
	hHT_unweighted.Fill(c.HT)
    
	# madHT check
	current_file_name = c.GetFile().GetName()
        if c.GetBranch("madHT"):
            madHT = c.madHT
            if not pass_background_stitching(current_file_name, madHT, phase): continue
        else:
            madHT = -10
    
	if not passesUniversalSelection(c): continue

	basicTracks = []
	disappearingTracks = []
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.trakcs):
	    if not track.Pt()>30 : continue
	    if not abs(track.Eta()) < 2.4 : continue
	    if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
	    if not isBaselineTrack(track, itrack, c, hMask): continue
	    basicTracks.append([track,itrack])



	RecoElectrons = []
	for iele, ele in enumerate(c.Electrons):
	    if not (ele.Pt()>30): continue
	    if not abs(ele.Eta())<2.4: continue
	    if not (abs(ele.Eta()) > 1.566 and abs(ele.Eta()) < 1.4442): continue
	    if not c.Electrons_passIso[iele]: continue
	    if not c.Electrons_tightID[iele]: continue
	    RecoElectrons.append([ele, iele])

	RecoMuons = []
	for imu, mu in enumerate(c.Muons):
	    if not (mu.Pt()>30): continue
	    if not abs(mu.Eta())<2.4: continue
	    if not (abs(mu.Eta()) > 1.566 and abs(mu.Eta()) < 1.4442): continue
	    if not c.Muons_passIso[imu]: continue
	    if not c.Muons_tightID[imu]: continue
	    RecoMuons.append([mu,imu])

	RecoJets = []
	for ijet, jet in enumerate(c.Jets):
	    if not abs(jet.Eta())<2.4: continue
	    if not (jet.Pt()>30): continue
	    if not c.Jets_ID[ijet]: continue
	    RecoJets.append([jet,ijet])

    fout.Write()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",dest="inputfiles")
    parser.add_argument("--output_folder",default="outputs_smallchunks",dest="output_folder")

    args = parser.parse_args()
    inputfiles = args.inputfiles
    output_folder = args.output_folder

    main(inputfiles,output_folder)

    
    
    
    '''	
    orderedmasses = []
    newfname = ''
    print nentries, 'events to be analyzed'
    for ientry in range(nentries):
    	if ientry%updateevery==0:
    		print 'now processing event number', ientry, 'of', nentries
    		if ientry==0: 
    			for itrig, trigname in enumerate(c.TriggerNames):
    				print itrig, trigname, c.TriggerPass[itrig], c.TriggerPrescales[itrig]
    
    	if verbose: print 'getting entry', ientry
    	c.GetEntry(ientry) 
    	if newfileEachsignal:
    		susymasses = []
    		susies = []
    		for igp, gp in enumerate(c.GenParticles):		
    			if not abs(c.GenParticles_PdgId[igp])>1000000: continue
    			#if c.GenParticles_Status[igp]==23: continue
    			pid = abs(c.GenParticles_PdgId[igp])
    			if not pid in susies:				
    				susies.append(pid)
    				susymasses.append([pid,round(gp.M(),2)])
    						
    		orderedmasses_ = sorted(susymasses, key=lambda x: x[1], reverse=True)
    		orderedmasses_ = [orderedmasses_[0], orderedmasses_[-1]]
    		
    		if not orderedmasses==orderedmasses_:
    			print 'failed comparison between', orderedmasses, 'and', orderedmasses_
    			orderedmasses = orderedmasses_
    			if not newfname=='':
    				fnew_.cd()
    				hHt.Write()
    				hHtWeighted.Write()
    				writeHistoStruct(histoStructDict, 'truth')
    				print 'just created', fnew_.GetName()
    				fnew_.Close()
    			print 'creating new file based on', orderedmasses
    			newfname = 'Hists'
    			for ip, susypid in enumerate(orderedmasses):
    				print susybypdg[orderedmasses[ip][0]], orderedmasses[ip][1]
    				newfname+='_'+susybypdg[orderedmasses[ip][0]]+str(orderedmasses[ip][1]).split('.')[0]
    			newfname+='_time'+str(round(time.time(),4)).replace('.','p')+'.root'
    			fnew_ = TFile(newfname,'recreate')
    			print 'creating file', fnew_.GetName()				
    			hHt = TH1F('hHt','hHt',200,0,10000)
    			hHtWeighted = TH1F('hHtWeighted','hHtWeighted',200,0,10000)
    			indexVar = {}
    			for ivar, var in enumerate(varlist_): indexVar[var] = ivar
    			histoStructDict = {}
    			for region in regionCuts:
    				for var in varlist_:
    					histname = region+'_'+var
    					histoStructDict[histname] = mkHistoStruct(histname, thebinning)
    					
    			if 'Higgsino' in inputFileNames: 
    				mothermass = float(inputFileNames.split('/')[-1].split('mChipm')[-1].split('GeV')[0])
    				xsecpb = CrossSectionsPb[model]['graph'].Eval(mothermass)
    				print 'xsec was', xsecpb
    				exit(0)			
    			elif 'T1' in model:
    				mothermass = orderedmasses[0][1]#inputFileNames.split('/')[-1].split('_')[0].replace('Higgsino','PLACEHOLDER').replace('g','').replace('*','').replace('PLACEHOLDER','Higgsino')
    				xsecpb = CrossSectionsPb[model][str(int(mothermass))]
    				print 'got xsec', xsecpb, 'for mothermass', mothermass					
    			else:
    				xsecpb = 1
    			signalweight = xsecpb
    						
    	hHt.Fill(c.HT)		
    				
    	basicTracks = []
    	disappearingTracks = []    
    	nShort, nLong = 0, 0
    	for itrack, track in enumerate(c.tracks):
    		if not track.Pt() > 10 : continue
    		if not abs(track.Eta()) < 2.4: continue
    		if  not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
    		if not isBaselineTrack(track, itrack, c, hMask): continue
    		basicTracks.append([track,c.tracks_charge[itrack], itrack])		
    		if not (track.Pt() > candPtCut and track.Pt()<candPtUpperCut): continue     
    		dtstatus, mva = isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips)
    		
    		if not dtstatus>0: continue
    		drlep = 99
    		passeslep = True
    		for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)+list(c.TAPPionTracks)): 
    			drlep = min(drlep, lep.DeltaR(track))
    			if drlep<0.1: 
    				passeslep = False
    				break            
    		if not passeslep: continue
    		isjet = False
    		for jet in c.Jets:
    			if jet.DeltaR(track)<0.4: 
    				isjet = True
    				break
    		if isjet:  continue		
    		dedx = -1
    		if dtstatus==1: 
    			nShort+=1
    			dedx = c.tracks_deDxHarmonic2pixel[itrack]
    		if dtstatus==2: 
    			nLong+=1			
    			dedx = c.tracks_deDxHarmonic2pixel[itrack]
    		disappearingTracks.append([track,dtstatus,dedx, itrack])
    
    	RecoElectrons = []
    	for iel, ele in enumerate(c.Electrons):
    		if debugmode: print ientry, iel,'ele with Pt' , ele.Pt()
    		if (abs(ele.Eta()) < 1.566 and abs(ele.Eta()) > 1.4442): continue
    		if not abs(ele.Eta())<2.4: continue
    		if debugmode: print 'passed eta and Pt'
    		if not c.Electrons_passIso[iel]: continue
    		if not c.Electrons_tightID[iel]: continue
    		if ele.Pt()>candPtCut: RecoElectrons.append([ele, iel])
    
    
    	RecoMuons = []
    	for ilep, lep in enumerate(c.Muons):
    		if verbose: print ientry, ilep,'mu with Pt' , lep.Pt()
    		if (abs(lep.Eta()) < 1.566 and abs(lep.Eta()) > 1.4442): continue
    		if not abs(lep.Eta())<2.4: continue
    		if verbose: print 'passed eta and Pt'
    		if not c.Muons_passIso[ilep]: continue
    		if not c.Muons_tightID[ilep]: continue
    		if lep.Pt()>candPtCut: RecoMuons.append([lep,ilep])    
    
    
    	#print 'len(RecoMuons)', len(RecoMuons)
    	SmearedPions = []
    	for ipi, pi in enumerate(c.TAPPionTracks):
    		if (abs(pi.Eta()) < 1.566 and abs(pi.Eta()) > 1.4442): continue
    		if not abs(pi.Eta())<2.4: continue
    		if not c.TAPPionTracks_trkiso[ipi]<0.2: continue  	   		
    		if pi.Pt()>candPtCut: SmearedPions.append([pi,ipi])    
    		
    	#print 'len(disappearingTracks)', len(disappearingTracks)
    	presentDisTrkEvent = len(disappearingTracks) >=1
    
    	if not presentDisTrkEvent: continue
    
    	metvec = TLorentzVector()
    	metvec.SetPtEtaPhiE(c.MET, 0, c.METPhi, c.MET) #check out feature vector in case of ttbar control region
    				  
    	if len(disappearingTracks)>0: 
    		dt = disappearingTracks[0][0]
    		pt = dt.Pt()
    		eta = abs(dt.Eta()) 
    		dedx = disappearingTracks[0][2] 
    		Log10DedxMass = TMath.Log10(TMath.Sqrt((dedx-3.01)*pow(c.tracks[disappearingTracks[0][3]].P(),2)/1.74))
    	else: 
    		print 'should never see this'
    		dt = TLorentzVector()
    		pt = -1
    		eta = -1
    		dedx = -1
    		Log10DedxMass = 0.01
    		
    	adjustedBTags = 0        
    	adjustedJets = []
    	adjustedHt = 0
    	adjustedMht = TLorentzVector()
    	adjustedMht.SetPxPyPzE(0,0,0,0)
    	for ijet, jet in enumerate(c.Jets):
    		if not jet.Pt()>30: continue			
    		if not abs(jet.Eta())<5.0: continue###update to 2.4
    		someoverlap = False
    		for dt_ in disappearingTracks: 
    			if jet.DeltaR(dt_[0])<0.4: 
    				someoverlap = True
    				break
    		if someoverlap: continue
    		adjustedMht-=jet		
    		if not abs(jet.Eta())<2.4: continue###update to 2.4            
    		adjustedJets.append(jet)			
    		if c.Jets_bDiscriminatorCSV[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
    		adjustedHt+=jet.Pt()
    	adjustedNJets = len(adjustedJets)
    	mindphi = 4
    	for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht))) 
    	
    	if len(RecoElectrons)>0: 
    		mT = c.Electrons_MTW[RecoElectrons[0][1]]
    		if c.Electrons_charge[RecoElectrons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoElectrons[0][0]+dt).M()
    		else: invmass = 999			
    	elif len(RecoMuons)>0: 
    		mT = c.Muons_MTW[RecoMuons[0][1]]
    		if c.Muons_charge[RecoMuons[0][1]]*c.tracks_charge[itrack]==-1: invmass = (RecoMuons[0][0]+dt).M()
    		else: invmass = 999			
    	else: 
    		mT = 999
    		invmass = 999	
    	
    	fv = [adjustedHt,adjustedMht.Pt(),adjustedNJets,adjustedBTags,len(disappearingTracks), nShort, nLong, mindphi,dedx, len(RecoElectrons), len(RecoMuons), invmass, mT, len(SmearedPions), pt, eta, Log10DedxMass]
    	fv.append(getBinNumber(fv))
    	
    	if isdata: weight = 1
    	elif len(RecoElectrons)+len(RecoMuons)>0: 
    		weight = signalweight*c.puWeight
    	else: 
    		weight = signalweight*c.puWeight*gtrig.Eval(c.MHT)
    		#weight = 1.0
    	hHtWeighted.Fill(c.HT,signalweight)
    		
    	#print fv
    	#for ifv in range(len(fv)): print ifv, varlist_[ifv], fv[ifv]	
    	for regionkey in regionCuts:
    		for ivar, varname in enumerate(varlist_):
    			if selectionFeatureVector(fv,regionkey,varname):
    				fillth1(histoStructDict[regionkey+'_'+varname].Truth,fv[ivar], weight)
    fnew_.cd()
    hHt.Write()
    hHtWeighted.Write()
    writeHistoStruct(histoStructDict, 'truth')
    print 'just created', fnew_.GetName()
    fnew_.Close()	
    fMask.Close()
    '''		
