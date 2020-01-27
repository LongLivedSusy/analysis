import os,sys
import argparse
import json
from ROOT import *
from shared_utils import *

TH1.SetDefaultSumw2()

def FillHisto(h, valx, weight=1.0):
    nbinsx = h.GetNbinsX()
    minvalx=h.GetXaxis().GetBinCenter(1)
    maxvalx=h.GetXaxis().GetBinCenter(nbinsx)

    newvalx=valx
    if valx<minvalx : newvalx=minvalx
    elif valx>maxvalx : newvalx=maxvalx

    h.Fill(newvalx,weight)
    return h



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


def main(inputfiles,output_folder,nev):
    
    # Adding Trees
    c = TChain("TreeMaker2/PreSelection")
    with open(inputfiles,'r') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
           print 'adding %sth file:'%i, line
    	   c.Add(line.rstrip('\n'))
    
    nentries = c.GetEntries()
    if nev != -1: nentries = nev
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
    #readers = load_tmva_readers(phase)
    if phase==0:
    	pixelXml = '../../disappearing-track-tag/2016-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
    	pixelstripsXml = '../../disappearing-track-tag/2016-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
    else:
    	pixelXml = '../../disappearing-track-tag/2017-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml'
    	pixelstripsXml = '../../disappearing-track-tag/2017-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml'	

    readerPixelOnly = TMVA.Reader()
    readerPixelStrips = TMVA.Reader()
    prepareReaderPixelStrips_loose(readerPixelStrips, pixelstripsXml)
    prepareReaderPixel_loose(readerPixelOnly, pixelXml)
    
    # load and configure data mask:
    if phase == 0:
        mask_file= TFile("../../tools/usefulthings/Masks.root")
        if is_data : 
            hMask = mask_file.Get("hEtaVsPhiDT_maskData-2016Data-2016")
        else :
            #hMask = mask_file.Get("hEtaVsPhiDT_maskMC-2016MC-2016")
            hMask = ''
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
    hMET = TH1F('hMET','hMET',100,0,1000)
    hMHT = TH1F('hMHT','hMHT',100,0,1000)
    hHT = TH1F('hHT','hHT',100,0,1000)
    hTrkPt = TH1F('hTrkPt','hTrkPt',100,0,1000)
    hTrkPt_mumatch = TH1F('hTrkPt_mumatch','hTrkPt_mumatch',100,0,1000)
    hTrkDedx_lepmatch = TH1F('hTrkDedx_lepmatch','hTrkDedx_lepmatch',100,0,10)
    hTrkDedx_mumatch = TH1F('hTrkDedx_mumatch','hTrkDedx_mumatch',100,0,10)
    hMuPt = TH1F('hMuPt','hMuPt',100,0,1000)
    hMuEta = TH1F('hMuEta','hMuEta',100,-3,3)
    hMuPhi = TH1F('hMuPhi','hMuPhi',100,-3.14,3.14)
    hElePt = TH1F('hElePt','hElePt',100,0,1000)
    hEleEta = TH1F('hEleEta','hEleEta',100,-3,3)
    hElePhi = TH1F('hElePhi','hElePhi',100,-3.14,3.14)

    # Event loop
    updateevery = 10000
    for ientry in range(nentries):
	
	if ientry%updateevery==0:
    	    print 'now processing event number', ientry, 'of', nentries
	
	c.GetEntry(ientry)
	
	# Counting histogram
	FillHisto(hHT_unweighted,c.HT)

	# Weight
	if is_data:
	    weight = 1.0
	else : 
	    weight = c.CrossSection * c.puWeight

	# madHT check
	current_file_name = c.GetFile().GetName()
        if c.GetBranch("madHT"):
            madHT = c.madHT
            if not pass_background_stitching(current_file_name, madHT, phase): continue
        else:
            madHT = -10
	
	#if is_data and not PassTrig(c,'MhtMet6pack') : continue
	#if is_data and not PassTrig(c,'SingleMuon') : continue
	if not passesUniversalSelection(c): continue
	#print 'is_data:%s, passTrig:%s, passUniversalSelection:%s'%(is_data,PassTrig(c,'SingleMuon'),passesUniversalSelection(c))

	if not c.MET>280 : continue

	FillHisto(hMET,c.MET,weight)
	FillHisto(hMHT,c.MHT,weight)
	FillHisto(hHT,c.HT,weight)
   
	# Track
	basicTracks = []
	lepmatchedTracks = []
	disappearingTracks = []
	nShort, nLong = 0, 0
	for itrack, track in enumerate(c.tracks):
	    if not track.Pt()>20 : continue
	    if not abs(track.Eta()) < 2.4 : continue
	    if not (abs(track.Eta()) > 1.566 or abs(track.Eta()) < 1.4442): continue
	    if not isBaselineTrack(track, itrack, c, hMask): continue
	    FillHisto(hTrkPt,track.Pt(),weight)

	    drlep = 99
	    lepmatch = False
	    for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)):
                drlep = min(drlep, lep.DeltaR(track))
                if drlep<0.1: 
                    lepmatch = True
		    dedx = c.tracks_deDxHarmonic2pixel[itrack]
		    lepmatchedTracks.append([track,dedx,itrack])

	    drmu = 99
	    mumatch = False
	    for imu, mu in enumerate(list(c.Muons)):
		if not mu.Pt()>30:continue
                drmu = min(drmu, mu.DeltaR(track))
                if drmu<0.01: 
                    mumatch = True
		    dedx = c.tracks_deDxHarmonic2pixel[itrack]
		    FillHisto(hTrkPt_mumatch,track.Pt(),weight)
		    FillHisto(hTrkDedx_mumatch,dedx,weight)

	    dtstatus, mva = isDisappearingTrack_(track, itrack, c, readerPixelOnly, readerPixelStrips)
	    #if not dtstatus>0: continue
            #drlep = 99
            #passeslep = True
            #for ilep, lep in enumerate(list(c.Electrons)+list(c.Muons)+list(c.TAPPionTracks)): 
            #        drlep = min(drlep, lep.DeltaR(track))
            #        if drlep<0.1: 
            #                passeslep = False
            #                break    
            #if not passeslep: continue
            #isjet = False
            #for jet in c.Jets:
            #        if jet.DeltaR(track)<0.4: 
            #                isjet = True
            #                break
            #if isjet:  continue    
            #dedx = -1
            #if dtstatus==1: 
            #        nShort+=1
            #        dedx = c.tracks_deDxHarmonic2pixel[itrack]
            #if dtstatus==2: 
            #        nLong+=1    
            #        dedx = c.tracks_deDxHarmonic2pixel[itrack]
            #disappearingTracks.append([track,dtstatus,dedx, itrack])

	RecoElectrons = []
	for iele, ele in enumerate(c.Electrons):
	    if not (ele.Pt()>30): continue
	    if not abs(ele.Eta())<2.4: continue
	    if not (abs(ele.Eta()) > 1.566 or abs(ele.Eta()) < 1.4442): continue
	    if not c.Electrons_passIso[iele]: continue
	    if not c.Electrons_tightID[iele]: continue
	    FillHisto(hElePt,ele.Pt(),weight)
	    FillHisto(hEleEta,ele.Eta(),weight)
	    FillHisto(hElePhi,ele.Phi(),weight)

	RecoMuons = []
	for imu, mu in enumerate(c.Muons):
	    if not (mu.Pt()>30): continue
	    if not abs(mu.Eta())<2.4: continue
	    if not (abs(mu.Eta()) > 1.566 or abs(mu.Eta()) < 1.4442): continue
	    if not c.Muons_passIso[imu]: continue
	    if not c.Muons_tightID[imu]: continue
	    FillHisto(hMuPt,mu.Pt(),weight)
	    FillHisto(hMuEta,mu.Eta(),weight)
	    FillHisto(hMuPhi,mu.Phi(),weight)

	RecoJets = []
	for ijet, jet in enumerate(c.Jets):
	    if not abs(jet.Eta())<2.4: continue
	    if not (jet.Pt()>30): continue
	    if not c.Jets_ID[ijet]: continue
	    RecoJets.append([jet,ijet])

    fout.Write()
    fout.Close()
    print("DONE")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",dest="inputfiles")
    parser.add_argument("--output_folder",default="outputs_smallchunks",dest="output_folder")
    parser.add_argument("--nev",default=-1,dest="nev")

    args = parser.parse_args()
    inputfiles = args.inputfiles
    output_folder = args.output_folder
    nev = int(args.nev)

    main(inputfiles,output_folder,nev)
