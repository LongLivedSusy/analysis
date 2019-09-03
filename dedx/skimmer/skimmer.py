#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import collections
import json
import math

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


def get_signal_region(event, MinDeltaPhiMhtJets, n_DT, is_pixel_track):
  
    NJets = len(event.Jets)
    MHT = event.MHT
    n_btags = event.BTags
    is_tracker_track = not is_pixel_track

    binnumbers = collections.OrderedDict()
    #           'Ht',             'Mht',                'NJets',            'BTags',            'NTags',            'NPix',             'NPixStrips',       'MinDPhiMhtJets'
    binnumbers[((0,float("inf")), (250,400),            (1,1),              (0,float("inf")),   (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 1
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (0,0),              (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 2
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (1,5),              (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 3
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (0,0),              (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 4
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (1,float("inf")),   (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 5
    binnumbers[((0,float("inf")), (400,700),            (1,1),              (0,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 6
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 7
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (1,5),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 8
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 9
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (1,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 10
    binnumbers[((0,float("inf")), (700,float("inf")),   (1,1),              (0,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 11
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 12
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (1,5),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 13
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 14
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (1,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 15
    binnumbers[((0,float("inf")), (250,400),            (1,1),              (0,float("inf")),   (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 16
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (0,0),              (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 17
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (1,5),              (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 18
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (0,0),              (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 19
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (1,float("inf")),   (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 20
    binnumbers[((0,float("inf")), (400,700),            (1,1),              (0,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 21
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 22
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (1,5),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 23
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 24
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (1,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 25
    binnumbers[((0,float("inf")), (700,float("inf")),   (1,1),              (0,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 26
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 27
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (1,5),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 28
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 29
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (1,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 30
    binnumbers[((0,float("inf")), (250,400),            (1,float("inf")),   (0,float("inf")),   (2,float("inf")),   (0,float("inf")),   (0,float("inf")),   (0.0,float("inf")))] = 31
    binnumbers[((0,float("inf")), (400,float("inf")),   (1,float("inf")),   (0,float("inf")),   (2,float("inf")),   (0,float("inf")),   (0,float("inf")),   (0.0,float("inf")))] = 32

    region = 0
    for binkey in binnumbers:
        if MHT >= binkey[1][0] and MHT <= binkey[1][1] and \
           NJets >= binkey[2][0] and NJets <= binkey[2][1] and \
           n_btags >= binkey[3][0] and n_btags <= binkey[3][1] and \
           n_DT >= binkey[4][0] and n_DT <= binkey[4][1] and \
           is_pixel_track >= binkey[5][0] and is_pixel_track <= binkey[5][1] and \
           is_tracker_track >= binkey[6][0] and is_tracker_track <= binkey[6][1] and \
           MinDeltaPhiMhtJets >= binkey[7][0] and MinDeltaPhiMhtJets <= binkey[7][1]:
            region = binnumbers[binkey]
            break

    #print "MinDeltaPhiMhtJets, n_DT, is_pixel_track, NJets, MHT, n_btags, is_tracker_track, region:", MinDeltaPhiMhtJets, n_DT, is_pixel_track, NJets, MHT, n_btags, is_tracker_track, region

    return region


def pass_background_stitching(current_file_name, madHT):
    if (madHT>0) and \
       ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
       ("WJetsToLNu_TuneCUETP8M1_13TeV" in current_file_name and madHT>100) or \
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
                

def isBaselineTrack(track, itrack, c, hMask, loose = False):

	if not abs(track.Eta())< 2.4 : return False
	if not (abs(track.Eta()) < 1.4442 or abs(track.Eta()) > 1.566): return False
	if not bool(c.tracks_trackQualityHighPurity[itrack]) : return False
	if not (c.tracks_ptError[itrack]/(track.Pt()*track.Pt()) < 10): return False
	if not loose and (not abs(c.tracks_dxyVtx[itrack]) < 0.1): return False
	if not abs(c.tracks_dzVtx[itrack]) < 0.1 : return False
	if not c.tracks_trkRelIso[itrack] < 0.2: return False
	if not (c.tracks_trackerLayersWithMeasurement[itrack] >= 2 and c.tracks_nValidTrackerHits[itrack] >= 2): return False
	if not c.tracks_nMissingInnerHits[itrack]==0: return False
	if not c.tracks_nMissingMiddleHits[itrack]==0: return False	
	if hMask:
		xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
    		ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
		if hMask.GetBinContent(ibinx, ibiny)==0: return False
	return True


def mkmet(metPt, metPhi):

    met = TLorentzVector()
    met.SetPtEtaPhiE(metPt, 0, metPhi, metPt)
    return met


def passQCDHighMETFilter(t):
    
    metvec = mkmet(t.MET, t.METPhi)
    for ijet, jet in enumerate(t.Jets):
        if not (jet.Pt() > 200): continue
        if not (t.Jets_muonEnergyFraction[ijet]>0.5):continue 
        if (abs(jet.DeltaPhi(metvec)) > (3.14159 - 0.4)): return False
    return True  
    

def passesUniversalSelection(t):
    
    if not (bool(t.JetID) and  t.NVtx>0): return False
    if not  passQCDHighMETFilter(t): return False
    if not t.PFCaloMETRatio<2: return False
    if not t.globalTightHalo2016Filter: return False
    if not t.HBHEIsoNoiseFilter: return False
    if not t.HBHENoiseFilter: return False
    if not t.BadPFMuonFilter: return False
    if not t.CSCTightHaloFilter: return False
    if not t.EcalDeadCellTriggerPrimitiveFilter: return False
    if not t.eeBadScFilter: return False 
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


def getBinContent_with_overflow(histo, xval, yval = False):
    
    if not yval:
        # overflow for TH1Fs:
        if xval >= histo.GetXaxis().GetXmax():
            value = histo.GetBinContent(histo.GetXaxis().GetNbins())
        else:
            value = histo.GetBinContent(histo.GetXaxis().FindBin(xval))
        return value
    else:
        # overflow for TH2Fs:
        if xval >= histo.GetXaxis().GetXmax() and yval < histo.GetYaxis().GetXmax():
            xbins = histo.GetXaxis().GetNbins()
            value = histo.GetBinContent(xbins, histo.GetYaxis().FindBin(yval))
        elif xval < histo.GetXaxis().GetXmax() and yval >= histo.GetYaxis().GetXmax():
            ybins = histo.GetYaxis().GetNbins()
            value = histo.GetBinContent(histo.GetXaxis().FindBin(xval), ybins)
        elif xval >= histo.GetXaxis().GetXmax() or yval >= histo.GetYaxis().GetXmax():
            xbins = histo.GetXaxis().GetNbins()
            ybins = histo.GetYaxis().GetNbins()
            value = histo.GetBinContent(xbins, ybins)
        else:
            value = histo.GetBinContent(histo.GetXaxis().FindBin(xval), histo.GetYaxis().FindBin(yval))
        return value
    

def load_tmva_readers(phase):
    
    readers = {}
    if phase == 0:
        bdts = {
                "bdt-short": "../../disappearing-track-tag/2016-short-tracks",
                "bdt-long": "../../disappearing-track-tag/2016-long-tracks",
                "bdt_loose-short": "../../disappearing-track-tag/2016-short-tracks-loose",
                "bdt_loose-long": "../../disappearing-track-tag/2016-long-tracks-loose",
               }
               
    elif phase == 1:
        bdts = {
                "bdt-short": "../../disappearing-track-tag/2017-short-tracks",
                "bdt-long": "../../disappearing-track-tag/2017-long-tracks",
                "bdt_loose-short": "../../disappearing-track-tag/2017-short-tracks-loose",
                "bdt_loose-long": "../../disappearing-track-tag/2017-long-tracks-loose",
               }
    
    for label in bdts:
        readers[label] = {}
        readers[label]["tmva_variables"] = {}
        readers[label]["info"] = get_tmva_info(bdts[label])
        readers[label]["reader"] = prepareReader(bdts[label] + '/weights/TMVAClassification_BDT.weights.xml', readers[label]["info"]["variables"], readers[label]["info"]["spectators"], readers[label]["tmva_variables"])

    return readers
    

def get_disappearing_track_score(event, iCand, readers, loose = False):
    
    # check TMVA preselection and evaluate BDT score
    
    category = "short"
    is_pixel_track = True
    if event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
        category = "long"
        is_pixel_track = False
                
    ptErrOverPt2 = event.tracks_ptError[iCand] / (event.tracks[iCand].Pt()**2)
    
    # check TMVA preselection:
    if is_pixel_track and not (event.tracks[iCand].Pt() > 30 and \
        abs(event.tracks[iCand].Eta()) < 2.4 and \
        event.tracks_trkRelIso[iCand] < 0.2 and \
        (loose or event.tracks_dxyVtx[iCand] < 0.1) and \
        event.tracks_dzVtx[iCand] < 0.1 and \
        ptErrOverPt2 < 10 and \
        event.tracks_nMissingMiddleHits[iCand] == 0 and \
        bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
            return -10

    if not is_pixel_track and not (event.tracks[iCand].Pt() > 30 and \
        abs(event.tracks[iCand].Eta()) < 2.4 and \
        event.tracks_trkRelIso[iCand] < 0.2 and \
        (loose or event.tracks_dxyVtx[iCand] < 0.1) and \
        event.tracks_dzVtx[iCand] < 0.1 and \
        ptErrOverPt2 < 10 and \
        event.tracks_nMissingOuterHits[iCand] >= 2 and \
        event.tracks_nMissingMiddleHits[iCand] == 0 and \
        bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
            return -10
    
    if not loose:
        bdt = readers["bdt-%s" % category]
    else:
        bdt = readers["bdt_loose-%s" % category]

    if not loose: bdt["tmva_variables"]["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
    bdt["tmva_variables"]["dzVtx"][0] = event.tracks_dzVtx[iCand]
    bdt["tmva_variables"]["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
    bdt["tmva_variables"]["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
    bdt["tmva_variables"]["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
    bdt["tmva_variables"]["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
    bdt["tmva_variables"]["ptErrOverPt2"][0] = ptErrOverPt2           

    score = bdt["reader"].EvaluateMVA("BDT")
    
    #if is_pixel_track and score > 0.1:
    #    return score
    #elif not is_pixel_track and score > 0.25:
    #    return score
    #else:
    #    return -10

    return score
    
    
def check_is_reco_lepton(event, iCand, deltaR = 0.01):

    reco_lepton = False
    for k in range(len(event.Muons)):
        if event.tracks[iCand].DeltaR(event.Muons[k]) < deltaR:
            reco_lepton = True
    for k in range(len(event.Electrons)):
        if event.tracks[iCand].DeltaR(event.Electrons[k]) < deltaR:
            reco_lepton = True
    return reco_lepton


def pass_pion_veto(event, iCand, deltaR = 0.03):

    # check for nearby pions:
    passpionveto = True
    for k in range(len(event.TAPPionTracks)):
        if event.tracks[iCand].DeltaR(event.TAPPionTracks[k]) < deltaR:
            passpionveto = False
            break
    return passpionveto


def main(event_tree_filenames, track_tree_output, fakerate_file = False, nevents = -1, treename = "TreeMaker2/PreSelection", mask_file = False, only_fakerate = False, verbose = False, iEv_start = False, debug = True, save_cleaned_variables = True):

    # store runs for JSON output:
    runs = {}

    # load tree
    tree = TChain(treename)
    for iFile in event_tree_filenames:
        tree.Add(iFile)
   
    fout = TFile(track_tree_output, "recreate")

    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()

    # check if data:
    phase = 0
    data_period = ""
    is_data = False
    for label in ["Run2016", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18"]:
        if label in event_tree_filenames[0]:
            data_period = label
            if "Run201" in label:
                is_data = True
            if label == "Run2016" or label == "Summer16":
                phase = 0
            elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
                phase = 1

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
    disappearing_track_tags = {"bdt": -10, "bdt_loose": -10}

    tout = TTree("Events", "tout")

    # prepare variables for output tree   
    float_branches = ["MET", "MHT", "HT", "MinDeltaPhiMhtJets", "PFCaloMETRatio", "dilepton_invmass", "dilepton_pt1", "dilepton_pt2"]
    integer_branches = ["n_jets", "n_btags", "n_leptons", "n_allvertices", "n_NVtx", "EvtNumEven", "dilepton_CR", "qcd_CR", "qcd_sideband_CR", "dilepton_leptontype", "passesUniversalSelection", "n_genLeptons", "n_genElectrons", "n_genMuons", "n_genTaus"]

    if not is_data:
        float_branches.append("madHT")
        float_branches.append("CrossSection")
        float_branches.append("puWeight")
        float_branches.append("NumInteractions")
    if save_cleaned_variables:
        float_branches.append("MHT_cleaned")
        float_branches.append("HT_cleaned")
        float_branches.append("MinDeltaPhiMhtJets_cleaned")
        integer_branches.append("n_jets_cleaned")
        integer_branches.append("n_btags_cleaned")

    tree_branch_values = {}
    for variable in float_branches:
        tree_branch_values[variable] = array( 'f', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/F' % variable )
    for variable in integer_branches:
        tree_branch_values[variable] = array( 'i', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/I' % variable )

    # add regions vector:
    tree_branch_values["region"] = 0
    tout.Branch("region", 'std::vector<int>', tree_branch_values["region"])    

    # get variables of tree
    track_variables = []
    for i in range(len(tree.GetListOfBranches())):
        label = tree.GetListOfBranches()[i].GetName()
        if "tracks_" in label:
            track_variables.append(label)

    # todo: use track_variables to get all track properties automatically

    # add our track vectors:
    tree_branch_values["tracks"] = 0
    tout.Branch('tracks', 'std::vector<TLorentzVector>', tree_branch_values["tracks"])

    vector_int_branches = ['tracks_is_pixel_track', 'tracks_pixelLayersWithMeasurement', 'tracks_trackerLayersWithMeasurement', 'tracks_nMissingInnerHits', 'tracks_nMissingMiddleHits', 'tracks_nMissingOuterHits', 'tracks_trackQualityHighPurity', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_fake', 'tracks_prompt_electron', 'tracks_prompt_muon', 'tracks_prompt_tau', 'tracks_prompt_tau_widecone', 'tracks_prompt_tau_leadtrk', 'tracks_passpionveto', 'tracks_is_baseline_track', 'tracks_is_reco_lepton', 'tracks_passPFCandVeto', 'tracks_charge']
    for dt_tag_label in disappearing_track_tags:
        vector_int_branches += ["tracks_tagged_%s" % dt_tag_label]
    
    for branch in vector_int_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<int>', tree_branch_values[branch])

    vector_float_branches = ['tracks_dxyVtx', 'tracks_dzVtx', 'tracks_matchedCaloEnergy', 'tracks_trkRelIso', 'tracks_ptErrOverPt2', 'tracks_pt', 'tracks_P', 'tracks_GenChi_pt', 'tracks_GenChi_P', 'tracks_eta', 'tracks_phi', 'tracks_trkMiniRelIso', 'tracks_trackJetIso', 'tracks_ptError', 'tracks_neutralPtSum', 'tracks_neutralWithoutGammaPtSum', 'tracks_minDrLepton', 'tracks_matchedCaloEnergyJets', 'tracks_deDxHarmonic2pixel', 'tracks_deDxHarmonic2strips', 'tracks_deDxHarmonic2weighted', 'tracks_massfromdeDxPixel', 'tracks_massfromdeDxPixel_GenChiMomentum', 'tracks_massfromdeDxStrips', 'tracks_massfromdeDxStrips_GenChiMomentum', 'tracks_massfromdeDx_weightedDeDx', 'tracks_massfromdeDx_weightedPixelStripsMass', 'tracks_chi2perNdof', 'tracks_chargedPtSum', 'tracks_chiCandGenMatchingDR', 'tracks_LabXYcm']
    for dt_tag_label in disappearing_track_tags:
        vector_float_branches += ["tracks_mva_%s" % dt_tag_label]
    for branch in vector_float_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<double>', tree_branch_values[branch])

    # load and configure data mask:
    if mask_file:
        mask_file = TFile(mask_file, "open")
    else:
        h_mask = False

    '''
    # load fake rate histograms:
    fakerate_regions = []
    for i_region in ["dilepton", "qcd", "qcd_sideband"]:
        for i_cond in ["tight", "loose1", "loose2", "loose3", "combined"]:
            for i_cat in ["_short", "_long"]:
                fakerate_regions.append(i_region + "_" + i_cond + i_cat)

    fakerate_variables = ["HT", "n_allvertices", "HT:n_allvertices", "HT:n_allvertices_interpolated"]
    if fakerate_file:
        
        # load fakerate maps:
        fakerate_file = TFile(fakerate_file, "open")

        # get all fakerate histograms:
        h_fakerates = {}
        for region in fakerate_regions:
            for variable in fakerate_variables:                   
                hist_name = region + "/" + data_period + "/fakerate_" + variable.replace(":", "_")
                
                hist_name = hist_name.replace("//", "/")
                try:
                    h_fakerates[hist_name] = fakerate_file.Get(hist_name)
                except:
                    print "Error reading fakerate:", hist_name

        # add all raw fakerate branches:        
        for region in fakerate_regions:
            for variable in fakerate_variables:
                branch_name = "fakerate_%s_%s" % (region, variable.replace(":", "_"))
                tree_branch_values[branch_name] = array( 'f', [ 0 ] )
                tout.Branch( branch_name, tree_branch_values[branch_name], '%s/F' % branch_name )
    '''

    print "Looping over %s events" % nev

    # main loop over events:
    for iEv, event in enumerate(tree):

        if iEv_start and iEv < begin_event: continue

        if nevents > 0 and iEv > nevents: break
        
        if (iEv+1) % 1000 == 0:
            PercentProcessed = int( 20 * iEv / nev )
            line = "[" + PercentProcessed*"#" + (20-PercentProcessed)*" " + "]\t" + "Processing event %s / %s" % (iEv + 1, nev)
            print line

        # collect lumisections:
        if is_data:
            runnum = event.RunNum
            lumisec = event.LumiBlockNum
            if runnum not in runs:
                runs[runnum] = []
            if lumisec not in runs[runnum]:
                runs[runnum].append(lumisec)
                
        current_file_name = tree.GetFile().GetName()
        if tree.GetBranch("madHT"):
            madHT = event.madHT
            if not pass_background_stitching(current_file_name, madHT): continue
                  
        # reset all branch values:
        for label in tree_branch_values:
            if "tracks" in label or "region" in label:
                continue
            if "fakerate" in label:
                tree_branch_values[label][0] = 0
            else:
                tree_branch_values[label][0] = -1

        region = []

        # set selection flags (veto event later if it does not fit into any selection):
        dilepton_CR = False
        qcd_CR = False
        qcd_sideband_CR = False

        min_lepton_pt = 30.0
        invariant_mass = 0

        # z mass peak: select two leptons with same flavour and pt>30
        selected_e_indices = []
        selected_mu_indices = []
        for lepton_type in ["Electrons", "Muons"]:
            for i, lepton in enumerate(eval("event.%s" % lepton_type)):
                if lepton.Pt() > 30:
                    if lepton_type == "Electrons": selected_e_indices.append(i)
                    elif lepton_type == "Muons": selected_mu_indices.append(i)                

        if (len(selected_e_indices) == 2 and len(selected_mu_indices) == 0):
            if bool(event.Electrons_mediumID[selected_e_indices[0]]) and bool(event.Electrons_mediumID[selected_e_indices[1]]):
                if (event.Electrons_charge[selected_e_indices[0]] * event.Electrons_charge[selected_e_indices[1]] < 0):
                    invariant_mass = (event.Electrons[selected_e_indices[0]] + event.Electrons[selected_e_indices[1]]).M()
                    if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                        if bool(event.Electrons_passIso[selected_e_indices[0]]) and bool(event.Electrons_passIso[selected_e_indices[1]]):
                            if abs(event.Electrons[selected_e_indices[0]].Eta()) < 2.4 and abs(event.Electrons[selected_e_indices[1]].Eta()):
                                tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                tree_branch_values["dilepton_pt1"][0] = event.Electrons[selected_e_indices[0]].Pt()
                                tree_branch_values["dilepton_pt2"][0] = event.Electrons[selected_e_indices[1]].Pt()                                    
                                tree_branch_values["dilepton_leptontype"][0] = 11
                                tree_branch_values["dilepton_CR"][0] = 1
                                dilepton_CR = True       

        elif (len(selected_mu_indices) == 2 and len(selected_e_indices) == 0):
            if (bool(event.Muons_tightID[selected_mu_indices[0]]) and bool(event.Muons_tightID[selected_mu_indices[1]])):
                if (event.Muons_charge[selected_mu_indices[0]] * event.Muons_charge[selected_mu_indices[1]] < 0):
                    invariant_mass = (event.Muons[selected_mu_indices[0]] + event.Muons[selected_mu_indices[1]]).M()            
                    if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                        if bool(event.Muons_passIso[selected_mu_indices[0]]) and bool(event.Muons_passIso[selected_mu_indices[1]]):
                            if abs(event.Muons[selected_mu_indices[0]].Eta()) < 2.4 and abs(event.Muons[selected_mu_indices[1]].Eta()):
                                tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                tree_branch_values["dilepton_pt1"][0] = event.Muons[selected_mu_indices[0]].Pt()
                                tree_branch_values["dilepton_pt2"][0] = event.Muons[selected_mu_indices[1]].Pt()                                    
                                tree_branch_values["dilepton_leptontype"][0] = 13
                                tree_branch_values["dilepton_CR"][0] = 1
                                dilepton_CR = True

        # check if low-MHT, QCD-only samples:
        if "QCD" in current_file_name or "JetHT" in current_file_name:
            if event.MHT < 200:
                tree_branch_values["qcd_CR"][0] = 1
                qcd_CR = True
            if event.MHT > 100 and event.MHT < 200:
                tree_branch_values["qcd_sideband_CR"][0] = 1
                qcd_sideband_CR = True

        if only_fakerate and (not dilepton_CR and not qcd_CR and not qcd_sideband_CR):
            continue

        # event selection for fake rate determination
        if save_cleaned_variables:
               
            # for the dilepton CR, clean event (recalculate HT, MHT, n_Jets without the two leptons):
            if dilepton_CR:
                csv_b = 0.8838
                metvec = TLorentzVector()
                metvec.SetPtEtaPhiE(event.MET, 0, event.METPhi, event.MET)
                mhtvec = TLorentzVector()
                mhtvec.SetPtEtaPhiE(0, 0, 0, 0)
                jets = []
                nb = 0
                HT_cleaned = 0
                
                for ijet, jet in enumerate(event.Jets):
                    
                    if not (abs(jet.Eta()) < 5 and jet.Pt() > 30): continue
                    
                    # check if lepton is in jet, and veto jet if that is the case
                    lepton_is_in_jet = False
                    for leptons in [event.Electrons, event.Muons]:
                        for lepton in leptons:
                            if jet.DeltaR(lepton) < 0.05:
                                lepton_is_in_jet = True
                    if lepton_is_in_jet: continue
                    
                    mhtvec-=jet
                    if not abs(jet.Eta()) < 2.4: continue

                    jets.append(jet)
                    HT_cleaned+=jet.Pt()        
                    if event.Jets_bDiscriminatorCSV[ijet] > csv_b: nb+=1
                    
                n_btags_cleaned = nb        
                n_jets_cleaned = len(jets)
                MHT_cleaned = mhtvec.Pt()

                MinDeltaPhiMhtJets_cleaned = 9999   
                for jet in jets: 
                    if abs(jet.DeltaPhi(mhtvec)) < MinDeltaPhiMhtJets_cleaned:
                        MinDeltaPhiMhtJets_cleaned = abs(jet.DeltaPhi(mhtvec))

                tree_branch_values["n_btags_cleaned"][0] = n_btags_cleaned
                tree_branch_values["n_jets_cleaned"][0] = n_jets_cleaned
                tree_branch_values["MHT_cleaned"][0] = MHT_cleaned
                tree_branch_values["HT_cleaned"][0] = HT_cleaned
                tree_branch_values["MinDeltaPhiMhtJets_cleaned"][0] = MinDeltaPhiMhtJets_cleaned

        # calculate MinDeltaPhiMhtJets:
        csv_b = 0.8838
        mhtvec = TLorentzVector()
        mhtvec.SetPtEtaPhiE(event.MHT, 0, event.MHTPhi, event.MHT)
        MinDeltaPhiMhtJets = 9999
        nj = 0
        nb = 0
        for ijet, jet in enumerate(event.Jets):
            if not (abs(jet.Eta())<2.4 and jet.Pt()>30): continue
            nj+=1
            if event.Jets_bDiscriminatorCSV[ijet]>csv_b: nb+=1
            if abs(jet.DeltaPhi(mhtvec))<MinDeltaPhiMhtJets:
                MinDeltaPhiMhtJets = abs(jet.DeltaPhi(mhtvec))
        
	# check if genLeptons are present in event:
        if not is_data:

            n_genLeptons = 0
            n_genElectrons = 0
            n_genMuons = 0
            n_genTaus = 0
            for k in range(len(event.GenParticles)):

                absPdgId = abs(event.GenParticles_PdgId[k])
                
                if absPdgId == 11:
                    n_genElectrons += 1
                    n_genLeptons += 1
                elif absPdgId == 13:
                    n_genMuons += 1
                    n_genLeptons += 1
                elif absPdgId == 15:
                    n_genTaus += 1
                    n_genLeptons += 1
                    
                tree_branch_values["n_genLeptons"][0] = n_genLeptons
                tree_branch_values["n_genElectrons"][0] = n_genElectrons
                tree_branch_values["n_genMuons"][0] = n_genMuons
                tree_branch_values["n_genTaus"][0] = n_genTaus

     
        # for each event, first fill this list for each track         
        track_level_output = []

        for iCand in range(len(event.tracks)):

            baseline = isBaselineTrack(event.tracks[iCand], iCand, event, h_mask, loose = True)
            if not baseline: continue
            
	    is_reco_lepton = check_is_reco_lepton(event, iCand, deltaR = 0.02)
            if is_reco_lepton: continue
            
            passpionveto = pass_pion_veto(event, iCand, deltaR = 0.03)        
            if not passpionveto: continue
            
            ptErrOverPt2 = event.tracks_ptError[iCand] / (event.tracks[iCand].Pt()**2)

            # check disappearing track tags:
            for dt_tag_label in disappearing_track_tags:                              
                loose = False
                if "loose" in dt_tag_label:
                    loose = True                   
                disappearing_track_tags[dt_tag_label] = get_disappearing_track_score(event, iCand, readers, loose = loose)

            #keep_track = False
            #for dt_tag_label in disappearing_track_tags:
            #    if disappearing_track_tags[dt_tag_label] > -10:
            #        keep_track = True
            #if not keep_track: continue

            is_pixel_track = True
            if event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = False
             
            # check if actual fake track (no genparticle in cone around track):
            is_prompt_electron = False
            is_prompt_muon = False
            is_prompt_tau = False
            is_prompt_tau_leadtrk = False
            is_prompt_tau_widecone = False

            if not is_data:
                for k in range(len(event.GenParticles)):
                    deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                    gen_track_cone_pdgid = abs(event.GenParticles_PdgId[k])

                    if deltaR < 0.02:
                        if gen_track_cone_pdgid == 11:
                            is_prompt_electron = True
                        if gen_track_cone_pdgid == 13:
                            is_prompt_muon = True
                        if gen_track_cone_pdgid == 15:
                            is_prompt_tau = True
                            # if genTau, check if the track matches with a GenTaus_LeadTrk track:
                            for l in range(len(event.GenTaus_LeadTrk)):
                                deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.04:
                                    is_prompt_tau_leadtrk = True
                                if deltaR < 0.4:
                                    is_prompt_tau_widecone = True
            
	    is_fake_track = is_prompt_electron or is_prompt_muon or is_prompt_tau or is_prompt_tau_leadtrk
            
	    # Track mass calculation using pixel and strips dE/dx
	    if is_pixel_track==True and not event.tracks_deDxHarmonic2pixel[iCand] > 2.557 : continue
	    if is_pixel_track==False and not event.tracks_deDxHarmonic2strips[iCand] > 2.557 : continue
            
            tracks_massfromdeDxPixel = TMath.Sqrt((event.tracks_deDxHarmonic2pixel[iCand]-2.557)*pow(event.tracks[iCand].P(),2)/2.579)
            tracks_massfromdeDxStrips = TMath.Sqrt((event.tracks_deDxHarmonic2strips[iCand]-2.557)*pow(event.tracks[iCand].P(),2)/2.579)
	    
	    tracks_deDxHarmonic2weighted = (event.tracks_deDxHarmonic2pixel[iCand]*event.tracks_nValidPixelHits[iCand] + event.tracks_deDxHarmonic2strips[iCand]*event.tracks_nValidTrackerHits[iCand])/(event.tracks_nValidPixelHits[iCand] + event.tracks_nValidTrackerHits[iCand])
	    tracks_massfromdeDx_weightedDeDx = TMath.Sqrt((tracks_deDxHarmonic2weighted-2.557)*pow(event.tracks[iCand].P(),2)/2.579)
	    tracks_massfromdeDx_weightedPixelStripsMass = (tracks_massfromdeDxPixel * event.tracks_nValidPixelHits[iCand] + tracks_massfromdeDxStrips*event.tracks_nValidTrackerHits[iCand])/(event.tracks_nValidPixelHits[iCand] + event.tracks_nValidTrackerHits[iCand])
            
	    #print '%d \t %d \t %s \t %.2f \t %.2f \t %.2f \t %.2f \t %.2f \t %.2f \t %.2f \t %.2f'%(iEv,iCand, is_pixel_track, event.tracks_deDxHarmonic2pixel[iCand], tracks_massfromdeDxPixel, event.tracks_deDxHarmonic2strips[iCand], tracks_massfromdeDxStrips, tracks_deDxHarmonic2weighted,tracks_massfromdeDx_weightedDeDx, tracks_massfromdeDx_weightedPixelStripsMass, event.tracks[iCand].P())


            # disappearing track counters:
            if debug: print "Found disappearing track in event %s, charged genLeptons in cone: %s" % (iEv, charged_genlepton_in_track_cone)

            track_level_output.append(
                                   {
                                     "tracks": event.tracks[iCand],
                                     "tracks_is_pixel_track": is_pixel_track,
                                     "tracks_pixelLayersWithMeasurement": event.tracks_pixelLayersWithMeasurement[iCand],
                                     "tracks_trackerLayersWithMeasurement": event.tracks_trackerLayersWithMeasurement[iCand],
                                     "tracks_fake": is_fake_track,
                                     "tracks_nMissingInnerHits": event.tracks_nMissingInnerHits[iCand],
                                     "tracks_nMissingMiddleHits": event.tracks_nMissingMiddleHits[iCand],
                                     "tracks_nMissingOuterHits": event.tracks_nMissingOuterHits[iCand],
                                     "tracks_trackQualityHighPurity": bool(event.tracks_trackQualityHighPurity[iCand]),
                                     "tracks_nValidPixelHits": event.tracks_nValidPixelHits[iCand],
                                     "tracks_nValidTrackerHits": event.tracks_nValidTrackerHits[iCand],
                                     "tracks_dxyVtx": event.tracks_dxyVtx[iCand],
                                     "tracks_dzVtx": event.tracks_dzVtx[iCand],
                                     "tracks_matchedCaloEnergy": event.tracks_matchedCaloEnergy[iCand],
                                     "tracks_trkRelIso": event.tracks_trkRelIso[iCand],
                                     "tracks_ptErrOverPt2": ptErrOverPt2,
                                     "tracks_pt": event.tracks[iCand].Pt(),
                                     "tracks_P": event.tracks[iCand].P(),
                                     "tracks_eta": event.tracks[iCand].Eta(),
                                     "tracks_phi": event.tracks[iCand].Phi(),
                                     "tracks_prompt_electron": is_prompt_electron,
                                     "tracks_prompt_muon": is_prompt_muon,
                                     "tracks_prompt_tau": is_prompt_tau,
                                     "tracks_prompt_tau_leadtrk": is_prompt_tau_leadtrk,
                                     "tracks_prompt_tau_widecone": is_prompt_tau_widecone,
                                     "tracks_passpionveto": passpionveto,
                                     "tracks_is_reco_lepton": is_reco_lepton,
                                     "tracks_trkMiniRelIso": event.tracks_trkMiniRelIso[iCand],
                                     "tracks_trackJetIso": event.tracks_trackJetIso[iCand],
                                     "tracks_ptError": event.tracks_ptError[iCand],
                                     "tracks_passPFCandVeto": bool(event.tracks_passPFCandVeto[iCand]),
                                     "tracks_neutralPtSum": event.tracks_neutralPtSum[iCand],
                                     "tracks_neutralWithoutGammaPtSum": event.tracks_neutralWithoutGammaPtSum[iCand],
                                     "tracks_minDrLepton": event.tracks_minDrLepton[iCand],
                                     "tracks_matchedCaloEnergyJets": event.tracks_matchedCaloEnergyJets[iCand],
                                     "tracks_deDxHarmonic2pixel": event.tracks_deDxHarmonic2pixel[iCand],
                                     "tracks_deDxHarmonic2strips": event.tracks_deDxHarmonic2strips[iCand],
                                     "tracks_deDxHarmonic2weighted": tracks_deDxHarmonic2weighted,
                                     "tracks_massfromdeDxPixel": tracks_massfromdeDxPixel,
                                     "tracks_massfromdeDxStrips": tracks_massfromdeDxStrips,
                                     "tracks_massfromdeDx_weightedDeDx": tracks_massfromdeDx_weightedDeDx,
                                     "tracks_massfromdeDx_weightedPixelStripsMass": tracks_massfromdeDx_weightedPixelStripsMass,
                                     "tracks_chi2perNdof": event.tracks_chi2perNdof[iCand],
                                     "tracks_chargedPtSum": event.tracks_chargedPtSum[iCand],
                                     "tracks_charge": event.tracks_charge[iCand],
                                   }
                                  )
                                  
            # add track tag information:
            for dt_tag_label in disappearing_track_tags:
                track_level_output[-1]["tracks_mva_%s" % dt_tag_label] = disappearing_track_tags[dt_tag_label]
                if disappearing_track_tags[dt_tag_label] > -10:
                    track_level_output[-1]["tracks_tagged_%s" % dt_tag_label] = 1
                else:
                    track_level_output[-1]["tracks_tagged_%s" % dt_tag_label] = 0

            # if signal, do chargino matching:
            if tree.GetBranch("GenParticles") and "g1800" in event_tree_filenames[0]:

                deltaR = 999.
		tracks_GenChi_P = 0.
		tracks_GenChi_pt = 0.
		tracks_massfromdeDxPixel_GenChiMomentum = 0.

                # track matching with closest gen-level chargino:
                for k in range(len(event.GenParticles)):
                    if abs(event.GenParticles_PdgId[k]) == 1000024 and event.GenParticles_Status[k] == 1:
			deltaR_tmp = event.tracks[iCand].DeltaR(event.GenParticles[k])
			if deltaR_tmp < deltaR :
			    deltaR = deltaR_tmp
			    tracks_GenChi_P = event.GenParticles[k].P()
			    tracks_GenChi_pt = event.GenParticles[k].Pt()
			    tracks_massfromdeDxPixel_GenChiMomentum = TMath.Sqrt((event.tracks_deDxHarmonic2pixel[iCand]-2.557)*pow(event.GenParticles[k].P(),2)/2.579)
			    tracks_massfromdeDxStrips_GenChiMomentum = TMath.Sqrt((event.tracks_deDxHarmonic2strips[iCand]-2.557)*pow(event.GenParticles[k].P(),2)/2.579)

                track_level_output[-1]["tracks_chiCandGenMatchingDR"] = deltaR
                track_level_output[-1]["tracks_GenChi_P"] = tracks_GenChi_P
                track_level_output[-1]["tracks_GenChi_pt"] = tracks_GenChi_pt
		
                track_level_output[-1]["tracks_massfromdeDxPixel_GenChiMomentum"] = tracks_massfromdeDxPixel_GenChiMomentum
                track_level_output[-1]["tracks_massfromdeDxStrips_GenChiMomentum"] = tracks_massfromdeDxStrips_GenChiMomentum

                ## chargino matching with GenParticlesGeant collection:
                #for k in range(len(event.GenParticlesGeant)):
                #    if abs(event.GenParticlesGeant_PdgId[k]) == 1000024 and event.GenParticlesGeant_Status[k] == 1:
                #        new_deltaR = event.tracks[iCand].DeltaR(event.GenParticlesGeant[k])
                #        if new_deltaR == deltaR:
                #            track_level_output[-1]["tracks_LabXYcm"] = event.GenParticlesGeant_LabXYcm[k]
                #            break

            if debug:
                for line in sorted(track_level_output[-1].keys()):
                    print "%s: %s" %(line, track_level_output[-1][line])

	'''
        # evaluate fake rate for each event:
        if fakerate_file:

            # fill all fakerate branches:
            for variable in fakerate_variables:
                for fr_region in fakerate_regions:
                    
                    hist_name = fr_region + "/" + data_period + "/fakerate_" + variable.replace(":", "_")
                    
                    if ":" in variable:
                        xvalue = eval("event.%s" % variable.replace("_interpolated", "").replace("_cleaned", "").replace("n_allvertices", "nAllVertices").replace("n_NVtx", "NVtx").split(":")[1])
                        yvalue = eval("event.%s" % variable.replace("_interpolated", "").replace("_cleaned", "").replace("n_allvertices", "nAllVertices").replace("n_NVtx", "NVtx").split(":")[0])
                                                
                        #FIXME:
                        if "interpolated" in hist_name: continue

                        FR = getBinContent_with_overflow(h_fakerates[hist_name], xvalue, yval = yvalue)
                    else:
                        value = eval("event.%s" % variable.replace("n_allvertices", "nAllVertices").replace("n_NVtx", "NVtx"))
                        FR = getBinContent_with_overflow(h_fakerates[hist_name], value)
                    
                    branch_name = "fakerate_%s_%s" % (fr_region, variable.replace(":", "_"))
                    tree_branch_values[branch_name][0] = FR
	'''

        # check if genLeptons are present in event:
        if not is_data:

            n_genLeptons = 0
            n_genElectrons = 0
            n_genMuons = 0
            n_genTaus = 0
            for k in range(len(event.GenParticles)):

                absPdgId = abs(event.GenParticles_PdgId[k])
                
                if absPdgId == 11:
                    n_genElectrons += 1
                    n_genLeptons += 1
                elif absPdgId == 13:
                    n_genMuons += 1
                    n_genLeptons += 1
                elif absPdgId == 15:
                    n_genTaus += 1
                    n_genLeptons += 1
                    
                tree_branch_values["n_genLeptons"][0] = n_genLeptons
                tree_branch_values["n_genElectrons"][0] = n_genElectrons
                tree_branch_values["n_genMuons"][0] = n_genMuons
                tree_branch_values["n_genTaus"][0] = n_genTaus

        # check if in meta CR:
        #meta_CR = False
        #if event.BTags >= 1 and event.MHT>100 and event.MHT<300:
        #    # check for well-reconstructed electron:
        #    if (len(event.Electrons)>0 and (event.Electrons[0].Pt() > 30) and bool(event.Electrons_mediumID[0]) and bool(event.Electrons_passIso[0])) or \
        #       (len(event.Muons)>0 and (event.Muons[0].Pt() > 30) and bool(event.Muons_tightID[0]) and bool(event.Muons_passIso[0])):
        #       meta_CR = True
        #       tree_branch_values["meta_CR"][0] = meta_CR

        # save event-level variables:
        tree_branch_values["passesUniversalSelection"][0] = passesUniversalSelection(event)
        tree_branch_values["n_leptons"][0] = len(event.Electrons) + len(event.Muons)
        tree_branch_values["n_btags"][0] = event.BTags
        tree_branch_values["n_jets"][0] = len(event.Jets)
        tree_branch_values["n_allvertices"][0] = event.nAllVertices
        tree_branch_values["PFCaloMETRatio"][0] = event.PFCaloMETRatio
        tree_branch_values["MET"][0] = event.MET
        tree_branch_values["MHT"][0] = event.MHT
        tree_branch_values["HT"][0] = event.HT
        tree_branch_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets
        tree_branch_values["n_NVtx"][0] = event.NVtx
        if not is_data:
            tree_branch_values["madHT"][0] = madHT
            tree_branch_values["CrossSection"][0] = event.CrossSection
            tree_branch_values["puWeight"][0] = event.puWeight
            tree_branch_values["NumInteractions"][0] = event.NumInteractions
        if event.EvtNum % 2 == 0:
            tree_branch_values["EvtNumEven"][0] = 1
        else:
            tree_branch_values["EvtNumEven"][0] = 0
         
        # track-level variables:
        n_tracks = len(track_level_output)
        tree_branch_values["tracks"] = ROOT.std.vector(TLorentzVector)(n_tracks)
      
        for branch in vector_int_branches:
            tree_branch_values[branch] = ROOT.std.vector(int)(n_tracks)
        for branch in vector_float_branches:
            tree_branch_values[branch] = ROOT.std.vector(double)(n_tracks)

        # register track-level branches:
        for label in tree_branch_values:
            if "tracks" in label:
                tout.SetBranchAddress(label, tree_branch_values[label])

        # save track-level properties:
        for i, track_output_dict in enumerate(track_level_output):
            for label in track_output_dict:
                tree_branch_values[label][i] = track_output_dict[label]

        # get signal region information:
        if event.MHT>250 and len(event.Jets)>0:
            region.append(get_signal_region(event, MinDeltaPhiMhtJets, 1, True))
            region.append(get_signal_region(event, MinDeltaPhiMhtJets, 1, False))
            region.append(get_signal_region(event, MinDeltaPhiMhtJets, 2, True))
            region = filter(lambda a: a != 0, region)
            tree_branch_values["region"] = ROOT.std.vector(int)(len(region))
            tout.SetBranchAddress("region", tree_branch_values["region"])
            for i in range(len(region)):
                tree_branch_values["region"][i] = region[i]
        
        tout.Fill()
     
    fout.cd()

    if fakerate_file:
        fakerate_file.Close()
    if mask_file:
        mask_file.Close()

    fout.cd()
    fout.Write()
    fout.Close()

    # write JSON containing lumisections:
    if len(runs) > 0:
        runs_compacted = {}
        for run in runs:
            if run not in runs_compacted:
                runs_compacted[run] = []
            for lumisec in runs[run]:
                if len(runs_compacted[run]) > 0 and lumisec == runs_compacted[run][-1][-1]+1:
                    runs_compacted[run][-1][-1] = lumisec
                else:
                    runs_compacted[run].append([lumisec, lumisec])

        json_content = json.dumps(runs_compacted)
        with open(track_tree_output.replace(".root", ".json"), "w") as fo:
            fo.write(json_content)


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles")
    parser.add_option("--output", dest = "outputfiles")
    parser.add_option("--only_fakerate", dest="only_fakerate", action = "store_true")
    parser.add_option("--debug", dest = "debug", action = "store_true")
    parser.add_option("--mask", dest = "maskfile", default = False)
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--fakerate_file", dest = "fakerate_file", default = False)
    parser.add_option("--iEv_start", dest = "iEv_start", default = 0)
    (options, args) = parser.parse_args()
    
    options.inputfiles = options.inputfiles.split(",")
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
    
    main(options.inputfiles,
         options.outputfiles,
         nevents = int(options.nev),
         only_fakerate = options.only_fakerate,
         mask_file = options.maskfile,
         iEv_start = int(options.iEv_start),
         fakerate_file = options.fakerate_file,
         debug = options.debug)
