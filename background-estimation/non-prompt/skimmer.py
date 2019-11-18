#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import collections
import json
import math
import tools.tags as tags

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
                

def isBaselineTrack(track, itrack, c):
    if not abs(track.Eta())< 2.4 : return False
    if not (abs(track.Eta()) < 1.4442 or abs(track.Eta()) > 1.566): return False
    if not bool(c.tracks_trackQualityHighPurity[itrack]) : return False
    if not (c.tracks_ptError[itrack]/(track.Pt()*track.Pt()) < 10): return False
    #if not ignore_dxy and (not abs(c.tracks_dxyVtx[itrack]) < 0.1): return False
    #if not ignore_dxy and (not abs(c.tracks_dzVtx[itrack]) < 0.1): return False
    if not c.tracks_trkRelIso[itrack] < 0.2: return False
    if not (c.tracks_trackerLayersWithMeasurement[itrack] >= 2 and c.tracks_nValidTrackerHits[itrack] >= 2): return False
    if not c.tracks_nMissingInnerHits[itrack]==0: return False
    if not c.tracks_nMissingMiddleHits[itrack]==0: return False    
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


def load_tmva_readers(phase):   
    readers = {}
    if phase == 0:
        bdts = {
                "bdt-short": "../disappearing-track-tag/2016-short-tracks",
                "bdt-long": "../disappearing-track-tag/2016-long-tracks",
                "bdt_loose-short": "../disappearing-track-tag/2016-short-tracks-loose",
                "bdt_loose-long": "../disappearing-track-tag/2016-long-tracks-loose",
                "bdt_looseloose-short": "../disappearing-track-tag/2016-short-tracks-looseloose",
                "bdt_looseloose-long": "../disappearing-track-tag/2016-long-tracks-looseloose",
               }
               
    elif phase == 1:
        bdts = {
                "bdt-short": "../disappearing-track-tag/2017-short-tracks",
                "bdt-long": "../disappearing-track-tag/2017-long-tracks",
                "bdt_loose-short": "../disappearing-track-tag/2017-short-tracks-loose",
                "bdt_loose-long": "../disappearing-track-tag/2017-long-tracks-loose",
                "bdt_looseloose-short": "../disappearing-track-tag/2017-short-tracks-looseloose",
                "bdt_looseloose-long": "../disappearing-track-tag/2017-long-tracks-looseloose",
               }
    
    for label in bdts:
        readers[label] = {}
        readers[label]["tmva_variables"] = {}
        readers[label]["info"] = get_tmva_info(bdts[label])
        readers[label]["reader"] = prepareReader(bdts[label] + '/weights/TMVAClassification_BDT.weights.xml', readers[label]["info"]["variables"], readers[label]["info"]["spectators"], readers[label]["tmva_variables"])

    return readers
    

def get_disappearing_track_score(dt_tag_label, event, iCand, readers):
    # check TMVA preselection and evaluate BDT score
    category = "short"
    is_pixel_track = True
    if event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
        category = "long"
        is_pixel_track = False

    if "looseloose" in dt_tag_label:
        use_dxy = False
        use_dz = False
        bdt = readers["bdt_looseloose-%s" % category]
    elif "loose" in dt_tag_label:
        use_dxy = False
        use_dz = True
        bdt = readers["bdt_loose-%s" % category]
    else:
        use_dxy = True
        use_dz = True
        bdt = readers["bdt-%s" % category]
                  
    ptErrOverPt2 = event.tracks_ptError[iCand] / (event.tracks[iCand].Pt()**2)
    
    # check TMVA preselection:
    if is_pixel_track and not (event.tracks[iCand].Pt() > 30 and \
        abs(event.tracks[iCand].Eta()) < 2.4 and \
        event.tracks_trkRelIso[iCand] < 0.2 and \
        (not use_dxy or event.tracks_dxyVtx[iCand] < 0.1) and \
        (not use_dz or event.tracks_dzVtx[iCand] < 0.1) and \
        ptErrOverPt2 < 10 and \
        event.tracks_nMissingMiddleHits[iCand] == 0 and \
        bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
            return -10

    if not is_pixel_track and not (event.tracks[iCand].Pt() > 30 and \
        abs(event.tracks[iCand].Eta()) < 2.4 and \
        event.tracks_trkRelIso[iCand] < 0.2 and \
        (not use_dxy or event.tracks_dxyVtx[iCand] < 0.1) and \
        (not use_dz or event.tracks_dzVtx[iCand] < 0.1) and \
        ptErrOverPt2 < 10 and \
        event.tracks_nMissingOuterHits[iCand] >= 2 and \
        event.tracks_nMissingMiddleHits[iCand] == 0 and \
        bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
            return -10
    
    if use_dxy:
        bdt["tmva_variables"]["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
    if use_dz:
        bdt["tmva_variables"]["dzVtx"][0] = event.tracks_dzVtx[iCand]
    bdt["tmva_variables"]["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
    bdt["tmva_variables"]["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
    bdt["tmva_variables"]["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
    bdt["tmva_variables"]["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
    bdt["tmva_variables"]["ptErrOverPt2"][0] = ptErrOverPt2           

    score = bdt["reader"].EvaluateMVA("BDT")
    
    return score
    
    
def check_is_reco_lepton(event, track, deltaR = 0.01):
    for lepton in list(event.Muons) + list(event.Electrons):
        if track.DeltaR(lepton) < deltaR:
            return True
    return False


def pass_pion_veto(event, iCand, deltaR = 0.03):
    # check for nearby pions:
    passpionveto = True
    for k in range(len(event.TAPPionTracks)):
        if event.tracks[iCand].DeltaR(event.TAPPionTracks[k]) < deltaR:
            passpionveto = False
            break
    return passpionveto


def pass_mask(h_mask, track):
    # check mask:
    if h_mask:
        ibinx, ibiny = h_mask.GetXaxis().FindBin(track.Phi()), h_mask.GetYaxis().FindBin(track.Eta())
        if h_mask.GetBinContent(ibinx, ibiny) == 0:
            return 0
        else:
            return 1
    else:
        return -1


def get_signal_region(HT, MHT, NJets, n_btags, MinDeltaPhiMhtJets, n_DT, is_pixel_track, DeDxAverage, n_goodelectrons, n_goodmuons, filename):
  
    is_tracker_track = not is_pixel_track
    inf = 9999
    binnumbers = collections.OrderedDict()

    ldedxcutLlow = 3.0
    ldedxcutLmid = 5.0
    ldedxcutSlow = 2.1
    ldedxcutSmid = 4.0
    binnumbers = {}
    listagain = ['Ht',  'Mht',    'NJets',  'BTags','NTags','NPix', 'NPixStrips', 'MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
    binnumbers[((0,inf),(150,300),(1,1),    (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 1
    binnumbers[((0,inf),(150,300),(1,1),    (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 2
    binnumbers[((0,inf),(150,300),(1,1),    (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 3
    binnumbers[((0,inf),(150,300),(1,1),    (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 4

    binnumbers[((0,inf),(150,300),(2,4),    (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 5
    binnumbers[((0,inf),(150,300),(2,4),    (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 6
    binnumbers[((0,inf),(150,300),(2,4),    (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 7
    binnumbers[((0,inf),(150,300),(2,4),    (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 8


    binnumbers[((0,inf),(150,300),(2,4),    (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 9
    binnumbers[((0,inf),(150,300),(2,4),    (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 10
    binnumbers[((0,inf),(150,300),(2,4),    (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 11
    binnumbers[((0,inf),(150,300),(2,4),    (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 12


    binnumbers[((0,inf),(150,300),(5,inf),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 13
    binnumbers[((0,inf),(150,300),(5,inf),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 14
    binnumbers[((0,inf),(150,300),(5,inf),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 15
    binnumbers[((0,inf),(150,300),(5,inf),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 16

    binnumbers[((0,inf),(150,300),(5,inf),  (1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 17
    binnumbers[((0,inf),(150,300),(5,inf),  (1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 18
    binnumbers[((0,inf),(150,300),(5,inf),  (1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 19
    binnumbers[((0,inf),(150,300),(5,inf),  (1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 20

    binnumbers[((0,inf),(300,inf),(1,1),    (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 21
    binnumbers[((0,inf),(300,inf),(1,1),    (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 22
    binnumbers[((0,inf),(300,inf),(1,1),    (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 23
    binnumbers[((0,inf),(300,inf),(1,1),    (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 24

    binnumbers[((0,inf),(300,inf),(2,4),    (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 25
    binnumbers[((0,inf),(300,inf),(2,4),    (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 26
    binnumbers[((0,inf),(300,inf),(2,4),    (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 27
    binnumbers[((0,inf),(300,inf),(2,4),    (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 28

    binnumbers[((0,inf),(300,inf),(2,4),    (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 29
    binnumbers[((0,inf),(300,inf),(2,4),    (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 30
    binnumbers[((0,inf),(300,inf),(2,4),    (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 31
    binnumbers[((0,inf),(300,inf),(2,4),    (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 32


    binnumbers[((0,1000),(300,inf),(5,inf), (0,0),  (1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),    (0,0))] = 33
    binnumbers[((0,1000),(300,inf),(5,inf), (0,0),  (1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),    (0,0))] = 34
    binnumbers[((0,1000),(300,inf),(5,inf), (0,0),  (1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),    (0,0))] = 35
    binnumbers[((0,1000),(300,inf),(5,inf), (0,0),  (1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),    (0,0))] = 36

    binnumbers[((0,1000),(300,inf),(5,inf), (1,inf),(1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),    (0,0))] = 37
    binnumbers[((0,1000),(300,inf),(5,inf), (1,inf),(1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),    (0,0))] = 38
    binnumbers[((0,1000),(300,inf),(5,inf), (1,inf),(1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),    (0,0))] = 39
    binnumbers[((0,1000),(300,inf),(5,inf), (1,inf),(1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),    (0,0))] = 40

    binnumbers[((1000,inf),(300,inf),(5,inf),(0,0), (1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),    (0,0))] = 41
    binnumbers[((1000,inf),(300,inf),(5,inf),(0,0), (1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),    (0,0))] = 42
    binnumbers[((1000,inf),(300,inf),(5,inf),(0,0), (1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),    (0,0))] = 43
    binnumbers[((1000,inf),(300,inf),(5,inf),(0,0),  (1,1), (1,1), (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),    (0,0))] = 44

    binnumbers[((1000,inf),(300,inf),(5,inf),(1,inf),(1,1), (0,0), (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),    (0,0))] = 45
    binnumbers[((1000,inf),(300,inf),(5,inf),(1,inf),(1,1), (0,0), (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),    (0,0))] = 46
    binnumbers[((1000,inf),(300,inf),(5,inf),(1,inf),(1,1), (1,1), (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),    (0,0))] = 47
    binnumbers[((1000,inf),(300,inf),(5,inf),(1,inf),(1,1), (1,1), (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),    (0,0))] = 48


    #listagain =  ['Ht',  'Mht',    'NJets','BTags','NTags','NPix','NPixStrips', 'MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
    binnumbers[((0,inf), (0,150),   (0,inf), (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLlow,ldedxcutLmid), (0,0), (1,inf))] = 49
    binnumbers[((0,inf), (0,150),   (0,inf), (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLmid,inf),          (0,0), (1,inf))] = 50
    binnumbers[((0,inf), (0,150),   (0,inf), (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSlow,ldedxcutSmid), (0,0), (1,inf))] = 51
    binnumbers[((0,inf), (0,150),   (0,inf), (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSmid,inf),          (0,0), (1,inf))] = 52


    binnumbers[((0,inf), (150,inf), (0,inf), (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLlow,ldedxcutLmid), (0,0), (1,inf))] = 53
    binnumbers[((0,inf), (150,inf), (0,inf), (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLmid,inf),          (0,0), (1,inf))] = 54
    binnumbers[((0,inf), (150,inf), (0,inf), (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSlow,ldedxcutSmid), (0,0), (1,inf))] = 55
    binnumbers[((0,inf), (150,inf), (0,inf), (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSmid,inf),          (0,0), (1,inf))] = 56

    binnumbers[((0,inf), (0,150),   (0,inf),(1,inf), (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLlow,ldedxcutLmid), (0,0), (1,inf))] = 57
    binnumbers[((0,inf), (0,150),   (0,inf),(1,inf), (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLmid,inf),          (0,0), (1,inf))] = 58
    binnumbers[((0,inf), (0,150),   (0,inf),(1,inf), (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSlow,ldedxcutSmid), (0,0), (1,inf))] = 59
    binnumbers[((0,inf), (0,150),   (0,inf),(1,inf), (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSmid,inf),          (0,0), (1,inf))] = 60

    binnumbers[((0,inf), (150,inf), (0,inf),(1,inf), (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLlow,ldedxcutLmid), (0,0), (1,inf))] = 61
    binnumbers[((0,inf), (150,inf), (0,inf),(1,inf), (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLmid,inf),          (0,0), (1,inf))] = 62
    binnumbers[((0,inf), (150,inf), (0,inf),(1,inf), (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSlow,ldedxcutSmid), (0,0), (1,inf))] = 63
    binnumbers[((0,inf), (150,inf), (0,inf),(1,inf), (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSmid,inf),          (0,0), (1,inf))] = 64

    #listagain =  ['Ht',  'Mht',    'NJets','BTags','NTags','NPix','NPixStrips', 'MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
    binnumbers[((0,inf),  (150,300), (0,inf),(0,inf),(2,inf),(0,inf),(0,inf),  (0.0,inf),          (ldedxcutSlow,inf),          (0,0), (0,0))]   = 65
    binnumbers[((0,inf),  (300,inf), (0,inf),(0,inf),(2,inf),(0,inf),(0,inf),  (0.0,inf),          (ldedxcutSlow,inf),          (0,0), (0,0))]   = 66
    binnumbers[((0,inf),  (0,inf),   (0,inf),(0,inf),(2,inf),(0,inf),(0,inf),  (0.0,inf),          (ldedxcutSlow,inf),          (0,0), (1,inf))] = 67 

    #listagain = ['Ht',  'Mht',    'NJets',  'BTags','NTags','NPix', 'NPixStrips', 'MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']

    region = 0
    for binkey in binnumbers:
        if HT >= binkey[0][0] and HT <= binkey[0][1] and \
           MHT >= binkey[1][0] and MHT <= binkey[1][1] and \
           NJets >= binkey[2][0] and NJets <= binkey[2][1] and \
           n_btags >= binkey[3][0] and n_btags <= binkey[3][1] and \
           n_DT >= binkey[4][0] and n_DT <= binkey[4][1] and \
           is_pixel_track >= binkey[5][0] and is_pixel_track <= binkey[5][1] and \
           is_tracker_track >= binkey[6][0] and is_tracker_track <= binkey[6][1] and \
           MinDeltaPhiMhtJets >= binkey[7][0] and MinDeltaPhiMhtJets <= binkey[7][1] and \
           DeDxAverage >= binkey[8][0] and DeDxAverage <= binkey[8][1] and \
           n_goodelectrons >= binkey[9][0] and n_goodelectrons <= binkey[9][1] and \
           n_goodmuons >= binkey[10][0] and n_goodmuons <= binkey[10][1]:
              region = binnumbers[binkey]
              break

    if region>0 and "Run201" in filename and "MET" in filename:
        if region<=48 or region==65 or region==66:
            return region
        else:
            return 0
    elif region>0 and "Run201" in filename and "SingleMuon" in filename:
        if region>=49 or region<=64 or region==67:
            return region
        else:
            return 0
    else:
        return region


def myround(x, base=5):
    return int(base * round(float(x)/base))


def get_sbottom_antisbottom_cross_section(mass):

    # xsections in pb from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVstopsbottom

    xsections = {
        100: "0.177E+04 pm 6.77",
        105: "0.145E+04 pm 6.74",
        110: "0.120E+04 pm 6.71",
        115: "0.998E+03 pm 6.69",
        120: "0.832E+03 pm 6.67",
        125: "0.697E+03 pm 6.65",
        130: "0.586E+03 pm 6.63",
        135: "0.495E+03 pm 6.61",
        140: "0.419E+03 pm 6.59",
        145: "0.357E+03 pm 6.58",
        150: "0.304E+03 pm 6.57",
        155: "0.261E+03 pm 6.55",
        160: "0.224E+03 pm 6.54",
        165: "0.194E+03 pm 6.53",
        170: "0.168E+03 pm 6.52",
        175: "0.146E+03 pm 6.52",
        180: "0.127E+03 pm 6.51",
        185: "0.111E+03 pm 6.51",
        190: "0.973E+02 pm 6.5",
        195: "0.856E+02 pm 6.5",
        200: "0.755E+02 pm 6.5",
        205: "0.668E+02 pm 6.5",
        210: "0.593E+02 pm 6.5",
        215: "0.527E+02 pm 6.5",
        220: "0.470E+02 pm 6.5",
        225: "0.420E+02 pm 6.51",
        230: "0.377E+02 pm 6.51",
        235: "0.338E+02 pm 6.52",
        240: "0.305E+02 pm 6.52",
        245: "0.275E+02 pm 6.53",
        250: "0.248E+02 pm 6.54",
        255: "0.225E+02 pm 6.54",
        260: "0.204E+02 pm 6.55",
        265: "0.186E+02 pm 6.56",
        270: "0.169E+02 pm 6.57",
        275: "0.155E+02 pm 6.58",
        280: "0.141E+02 pm 6.6",
        285: "0.129E+02 pm 6.61",
        290: "0.119E+02 pm 6.62",
        295: "0.109E+02 pm 6.63",
        300: "0.100E+02 pm 6.65",
        305: "0.918E+01 pm 6.66",
        310: "0.843E+01 pm 6.67",
        315: "0.775E+01 pm 6.69",
        320: "0.713E+01 pm 6.7",
        325: "0.657E+01 pm 6.71",
        330: "0.606E+01 pm 6.73",
        335: "0.559E+01 pm 6.74",
        340: "0.517E+01 pm 6.76",
        345: "0.478E+01 pm 6.78",
        350: "0.443E+01 pm 6.79",
        355: "0.410E+01 pm 6.81",
        360: "0.381E+01 pm 6.83",
        365: "0.354E+01 pm 6.85",
        370: "0.329E+01 pm 6.87",
        375: "0.306E+01 pm 6.89",
        380: "0.285E+01 pm 6.91",
        385: "0.265E+01 pm 6.93",
        390: "0.247E+01 pm 6.95",
        395: "0.231E+01 pm 6.97",
        400: "0.215E+01 pm 6.99",
        405: "0.201E+01 pm 7.01",
        410: "0.188E+01 pm 7.04",
        415: "0.176E+01 pm 7.06",
        420: "0.164E+01 pm 7.09",
        425: "0.154E+01 pm 7.11",
        430: "0.144E+01 pm 7.14",
        435: "0.135E+01 pm 7.16",
        440: "0.126E+01 pm 7.19",
        445: "0.119E+01 pm 7.22",
        450: "0.111E+01 pm 7.25",
        455: "0.105E+01 pm 7.27",
        460: "0.983E+00 pm 7.3",
        465: "0.925E+00 pm 7.33",
        470: "0.870E+00 pm 7.36",
        475: "0.819E+00 pm 7.38",
        480: "0.771E+00 pm 7.41",
        485: "0.727E+00 pm 7.44",
        490: "0.685E+00 pm 7.47",
        495: "0.646E+00 pm 7.5",
        500: "0.609E+00 pm 7.53",
        505: "0.575E+00 pm 7.56",
        510: "0.543E+00 pm 7.58",
        515: "0.513E+00 pm 7.61",
        520: "0.484E+00 pm 7.64",
        525: "0.458E+00 pm 7.67",
        530: "0.433E+00 pm 7.7",
        535: "0.409E+00 pm 7.73",
        540: "0.387E+00 pm 7.75",
        545: "0.367E+00 pm 7.78",
        550: "0.347E+00 pm 7.81",
        555: "0.329E+00 pm 7.84",
        560: "0.312E+00 pm 7.87",
        565: "0.296E+00 pm 7.9",
        570: "0.280E+00 pm 7.93",
        575: "0.266E+00 pm 7.96",
        580: "0.252E+00 pm 7.99",
        585: "0.240E+00 pm 8.02",
        590: "0.228E+00 pm 8.05",
        595: "0.216E+00 pm 8.08",
        600: "0.205E+00 pm 8.12",
        605: "0.195E+00 pm 8.15",
        610: "0.186E+00 pm 8.18",
        615: "0.177E+00 pm 8.21",
        620: "0.168E+00 pm 8.25",
        625: "0.160E+00 pm 8.28",
        630: "0.152E+00 pm 8.31",
        635: "0.145E+00 pm 8.35",
        640: "0.138E+00 pm 8.38",
        645: "0.131E+00 pm 8.42",
        650: "0.125E+00 pm 8.45",
        655: "0.119E+00 pm 8.49",
        660: "0.114E+00 pm 8.52",
        665: "0.108E+00 pm 8.56",
        670: "0.103E+00 pm 8.59",
        675: "0.987E-01 pm 8.63",
        680: "0.942E-01 pm 8.66",
        685: "0.899E-01 pm 8.7",
        690: "0.858E-01 pm 8.73",
        695: "0.820E-01 pm 8.77",
        700: "0.783E-01 pm 8.8",
        705: "0.748E-01 pm 8.84",
        710: "0.715E-01 pm 8.88",
        715: "0.683E-01 pm 8.91",
        720: "0.653E-01 pm 8.95",
        725: "0.624E-01 pm 8.98",
        730: "0.597E-01 pm 9.02",
        735: "0.571E-01 pm 9.05",
        740: "0.546E-01 pm 9.09",
        745: "0.523E-01 pm 9.13",
        750: "0.500E-01 pm 9.16",
        755: "0.479E-01 pm 9.2",
        760: "0.459E-01 pm 9.24",
        765: "0.439E-01 pm 9.27",
        770: "0.421E-01 pm 9.31",
        775: "0.403E-01 pm 9.35",
        780: "0.386E-01 pm 9.38",
        785: "0.370E-01 pm 9.42",
        790: "0.355E-01 pm 9.46",
        795: "0.340E-01 pm 9.5",
        800: "0.326E-01 pm 9.53",
        805: "0.313E-01 pm 9.57",
        810: "0.300E-01 pm 9.61",
        815: "0.288E-01 pm 9.65",
        820: "0.276E-01 pm 9.69",
        825: "0.265E-01 pm 9.73",
        830: "0.254E-01 pm 9.77",
        835: "0.244E-01 pm 9.81",
        840: "0.234E-01 pm 9.85",
        845: "0.225E-01 pm 9.89",
        850: "0.216E-01 pm 9.93",
        855: "0.208E-01 pm 9.97",
        860: "0.199E-01 pm 10.01",
        865: "0.192E-01 pm 10.05",
        870: "0.184E-01 pm 10.09",
        875: "0.177E-01 pm 10.13",
        880: "0.170E-01 pm 10.17",
        885: "0.164E-01 pm 10.21",
        890: "0.157E-01 pm 10.25",
        895: "0.151E-01 pm 10.29",
        900: "0.145E-01 pm 10.33",
        905: "0.140E-01 pm 10.38",
        910: "0.135E-01 pm 10.42",
        915: "0.129E-01 pm 10.46",
        920: "0.125E-01 pm 10.5",
        925: "0.120E-01 pm 10.54",
        930: "0.115E-01 pm 10.59",
        935: "0.111E-01 pm 10.63",
        940: "0.107E-01 pm 10.67",
        945: "0.103E-01 pm 10.71",
        950: "0.991E-02 pm 10.76",
        955: "0.954E-02 pm 10.8",
        960: "0.919E-02 pm 10.84",
        965: "0.885E-02 pm 10.89",
        970: "0.853E-02 pm 10.93",
        975: "0.822E-02 pm 10.97",
        980: "0.792E-02 pm 11.02",
        985: "0.763E-02 pm 11.06",
        990: "0.735E-02 pm 11.11",
        995: "0.709E-02 pm 11.15",
        1000: "0.683E-02 pm 11.2",
        1005: "0.659E-02 pm 11.24",
        1010: "0.635E-02 pm 11.29",
        1015: "0.613E-02 pm 11.33",
        1020: "0.591E-02 pm 11.38",
        1025: "0.570E-02 pm 11.42",
        1030: "0.550E-02 pm 11.47",
        1035: "0.530E-02 pm 11.51",
        1040: "0.511E-02 pm 11.56",
        1045: "0.493E-02 pm 11.6",
        1050: "0.476E-02 pm 11.65",
        1055: "0.460E-02 pm 11.7",
        1060: "0.444E-02 pm 11.74",
        1065: "0.428E-02 pm 11.79",
        1070: "0.413E-02 pm 11.84",
        1075: "0.399E-02 pm 11.88",
        1080: "0.385E-02 pm 11.93",
        1085: "0.372E-02 pm 11.98",
        1090: "0.359E-02 pm 12.03",
        1095: "0.347E-02 pm 12.07",
        1100: "0.335E-02 pm 12.12",
        1105: "0.324E-02 pm 12.17",
        1110: "0.313E-02 pm 12.22",
        1115: "0.302E-02 pm 12.27",
        1120: "0.292E-02 pm 12.32",
        1125: "0.282E-02 pm 12.37",
        1130: "0.272E-02 pm 12.42",
        1135: "0.263E-02 pm 12.47",
        1140: "0.254E-02 pm 12.52",
        1145: "0.246E-02 pm 12.57",
        1150: "0.238E-02 pm 12.62",
        1155: "0.230E-02 pm 12.67",
        1160: "0.222E-02 pm 12.72",
        1165: "0.215E-02 pm 12.77",
        1170: "0.208E-02 pm 12.82",
        1175: "0.201E-02 pm 12.87",
        1180: "0.194E-02 pm 12.93",
        1185: "0.188E-02 pm 12.98",
        1190: "0.182E-02 pm 13.03",
        1195: "0.176E-02 pm 13.08",
        1200: "0.170E-02 pm 13.13",
        1205: "0.164E-02 pm 13.19",
        1210: "0.159E-02 pm 13.24",
        1215: "0.154E-02 pm 13.29",
        1220: "0.149E-02 pm 13.34",
        1225: "0.144E-02 pm 13.4",
        1230: "0.139E-02 pm 13.45",
        1235: "0.135E-02 pm 13.5",
        1240: "0.131E-02 pm 13.55",
        1245: "0.126E-02 pm 13.61",
        1250: "0.122E-02 pm 13.66",
        1255: "0.118E-02 pm 13.72",
        1260: "0.115E-02 pm 13.77",
        1265: "0.111E-02 pm 13.82",
        1270: "0.107E-02 pm 13.88",
        1275: "0.104E-02 pm 13.93",
        1280: "0.101E-02 pm 13.99",
        1285: "0.976E-03 pm 14.04",
        1290: "0.945E-03 pm 14.1",
        1295: "0.915E-03 pm 14.15",
        1300: "0.887E-03 pm 14.21",
        1305: "0.859E-03 pm 14.26",
        1310: "0.832E-03 pm 14.32",
        1315: "0.806E-03 pm 14.38",
        1320: "0.781E-03 pm 14.43",
        1325: "0.756E-03 pm 14.49",
        1330: "0.733E-03 pm 14.55",
        1335: "0.710E-03 pm 14.61",
        1340: "0.688E-03 pm 14.66",
        1345: "0.667E-03 pm 14.72",
        1350: "0.646E-03 pm 14.78",
        1355: "0.626E-03 pm 14.84",
        1360: "0.607E-03 pm 14.9",
        1365: "0.588E-03 pm 14.95",
        1370: "0.570E-03 pm 15.01",
        1375: "0.553E-03 pm 15.07",
        1380: "0.536E-03 pm 15.13",
        1385: "0.519E-03 pm 15.19",
        1390: "0.503E-03 pm 15.25",
        1395: "0.488E-03 pm 15.31",
        1400: "0.473E-03 pm 15.37",
        1405: "0.459E-03 pm 15.43",
        1410: "0.445E-03 pm 15.49",
        1415: "0.431E-03 pm 15.55",
        1420: "0.418E-03 pm 15.62",
        1425: "0.406E-03 pm 15.68",
        1430: "0.393E-03 pm 15.74",
        1435: "0.382E-03 pm 15.8",
        1440: "0.370E-03 pm 15.86",
        1445: "0.359E-03 pm 15.93",
        1450: "0.348E-03 pm 15.99",
        1455: "0.338E-03 pm 16.05",
        1460: "0.328E-03 pm 16.11",
        1465: "0.318E-03 pm 16.18",
        1470: "0.308E-03 pm 16.24",
        1475: "0.299E-03 pm 16.31",
        1480: "0.290E-03 pm 16.37",
        1485: "0.282E-03 pm 16.43",
        1490: "0.273E-03 pm 16.5",
        1495: "0.265E-03 pm 16.56",
        1500: "0.257E-03 pm 16.63",
        1505: "0.250E-03 pm 16.69",
        1510: "0.242E-03 pm 16.76",
        1515: "0.235E-03 pm 16.82",
        1520: "0.228E-03 pm 16.89",
        1525: "0.222E-03 pm 16.95",
        1530: "0.215E-03 pm 17.02",
        1535: "0.209E-03 pm 17.08",
        1540: "0.203E-03 pm 17.15",
        1545: "0.197E-03 pm 17.21",
        1550: "0.191E-03 pm 17.28",
        1555: "0.185E-03 pm 17.35",
        1560: "0.180E-03 pm 17.41",
        1565: "0.175E-03 pm 17.48",
        1570: "0.170E-03 pm 17.55",
        1575: "0.165E-03 pm 17.62",
        1580: "0.160E-03 pm 17.68",
        1585: "0.155E-03 pm 17.75",
        1590: "0.151E-03 pm 17.82",
        1595: "0.146E-03 pm 17.89",
        1600: "0.142E-03 pm 17.96",
        1605: "0.138E-03 pm 18.03",
        1610: "0.134E-03 pm 18.1",
        1615: "0.130E-03 pm 18.17",
        1620: "0.127E-03 pm 18.24",
        1625: "0.123E-03 pm 18.31",
        1630: "0.119E-03 pm 18.38",
        1635: "0.116E-03 pm 18.45",
        1640: "0.113E-03 pm 18.52",
        1645: "0.109E-03 pm 18.59",
        1650: "0.106E-03 pm 18.67",
        1655: "0.103E-03 pm 18.74",
        1660: "0.100E-03 pm 18.81",
        1665: "0.974E-04 pm 18.88",
        1670: "0.946E-04 pm 18.96",
        1675: "0.920E-04 pm 19.03",
        1680: "0.893E-04 pm 19.1",
        1685: "0.868E-04 pm 19.18",
        1690: "0.843E-04 pm 19.25",
        1695: "0.819E-04 pm 19.33",
        1700: "0.796E-04 pm 19.4",
        1705: "0.774E-04 pm 19.48",
        1710: "0.752E-04 pm 19.55",
        1715: "0.731E-04 pm 19.63",
        1720: "0.710E-04 pm 19.7",
        1725: "0.690E-04 pm 19.78",
        1730: "0.671E-04 pm 19.85",
        1735: "0.652E-04 pm 19.93",
        1740: "0.633E-04 pm 20.01",
        1745: "0.616E-04 pm 20.08",
        1750: "0.598E-04 pm 20.16",
        1755: "0.582E-04 pm 20.24",
        1760: "0.565E-04 pm 20.31",
        1765: "0.550E-04 pm 20.39",
        1770: "0.534E-04 pm 20.47",
        1775: "0.519E-04 pm 20.55",
        1780: "0.505E-04 pm 20.63",
        1785: "0.491E-04 pm 20.71",
        1790: "0.477E-04 pm 20.79",
        1795: "0.464E-04 pm 20.86",
        1800: "0.451E-04 pm 20.94",
        1805: "0.438E-04 pm 21.02",
        1810: "0.426E-04 pm 21.1",
        1815: "0.414E-04 pm 21.19",
        1820: "0.403E-04 pm 21.27",
        1825: "0.392E-04 pm 21.35",
        1830: "0.381E-04 pm 21.43",
        1835: "0.370E-04 pm 21.51",
        1840: "0.360E-04 pm 21.59",
        1845: "0.350E-04 pm 21.68",
        1850: "0.340E-04 pm 21.76",
        1855: "0.331E-04 pm 21.84",
        1860: "0.322E-04 pm 21.92",
        1865: "0.313E-04 pm 22.01",
        1870: "0.304E-04 pm 22.09",
        1875: "0.296E-04 pm 22.18",
        1880: "0.288E-04 pm 22.26",
        1885: "0.280E-04 pm 22.34",
        1890: "0.272E-04 pm 22.43",
        1895: "0.265E-04 pm 22.52",
        1900: "0.258E-04 pm 22.6",
        1905: "0.250E-04 pm 22.69",
        1910: "0.244E-04 pm 22.77",
        1915: "0.237E-04 pm 22.86",
        1920: "0.230E-04 pm 22.95",
        1925: "0.224E-04 pm 23.03",
        1930: "0.218E-04 pm 23.12",
        1935: "0.212E-04 pm 23.21",
        1940: "0.206E-04 pm 23.3",
        1945: "0.201E-04 pm 23.38",
        1950: "0.195E-04 pm 23.47",
        1955: "0.190E-04 pm 23.56",
        1960: "0.185E-04 pm 23.65",
        1965: "0.180E-04 pm 23.74",
        1970: "0.175E-04 pm 23.83",
        1975: "0.170E-04 pm 23.92",
        1980: "0.165E-04 pm 24.01",
        1985: "0.161E-04 pm 24.1",
        1990: "0.157E-04 pm 24.2",
        1995: "0.152E-04 pm 24.29",
        2000: "0.148E-04 pm 24.38",
        2005: "0.144E-04 pm 24.47",
        2010: "0.140E-04 pm 24.56",
        2015: "0.137E-04 pm 24.66",
        2020: "0.133E-04 pm 24.75",
        2025: "0.129E-04 pm 24.84",
        2030: "0.126E-04 pm 24.94",
        2035: "0.122E-04 pm 25.03",
        2040: "0.119E-04 pm 25.13",
        2045: "0.116E-04 pm 25.22",
        2050: "0.113E-04 pm 25.32",
        2055: "0.110E-04 pm 25.42",
        2060: "0.107E-04 pm 25.51",
        2065: "0.104E-04 pm 25.61",
        2070: "0.101E-04 pm 25.71",
        2075: "0.984E-05 pm 25.8",
        2080: "0.957E-05 pm 25.9",
        2085: "0.931E-05 pm 26.0",
        2090: "0.906E-05 pm 26.1",
        2095: "0.882E-05 pm 26.2",
        2100: "0.858E-05 pm 26.3",
        2105: "0.835E-05 pm 26.4",
        2110: "0.813E-05 pm 26.5",
        2115: "0.791E-05 pm 26.6",
        2120: "0.770E-05 pm 26.7",
        2125: "0.749E-05 pm 26.8",
        2130: "0.729E-05 pm 26.9",
        2135: "0.710E-05 pm 27.01",
        2140: "0.691E-05 pm 27.11",
        2145: "0.672E-05 pm 27.21",
        2150: "0.655E-05 pm 27.32",
        2155: "0.637E-05 pm 27.42",
        2160: "0.620E-05 pm 27.52",
        2165: "0.604E-05 pm 27.63",
        2170: "0.587E-05 pm 27.73",
        2175: "0.572E-05 pm 27.84",
        2180: "0.557E-05 pm 27.95",
        2185: "0.542E-05 pm 28.05",
        2190: "0.527E-05 pm 28.16",
        2195: "0.513E-05 pm 28.27",
        2200: "0.500E-05 pm 28.38",
        2205: "0.486E-05 pm 28.48",
        2210: "0.473E-05 pm 28.59",
        2215: "0.461E-05 pm 28.7",
        2220: "0.449E-05 pm 28.81",
        2225: "0.437E-05 pm 28.92",
        2230: "0.425E-05 pm 29.03",
        2235: "0.414E-05 pm 29.14",
        2240: "0.403E-05 pm 29.25",
        2245: "0.392E-05 pm 29.36",
        2250: "0.382E-05 pm 29.47",
        2255: "0.372E-05 pm 29.58",
        2260: "0.362E-05 pm 29.7",
        2265: "0.352E-05 pm 29.81",
        2270: "0.343E-05 pm 29.92",
        2275: "0.334E-05 pm 30.04",
        2280: "0.325E-05 pm 30.15",
        2285: "0.316E-05 pm 30.27",
        2290: "0.308E-05 pm 30.38",
        2295: "0.300E-05 pm 30.5",
        2300: "0.292E-05 pm 30.62",
        2305: "0.284E-05 pm 30.74",
        2310: "0.277E-05 pm 30.85",
        2315: "0.269E-05 pm 30.97",
        2320: "0.262E-05 pm 31.09",
        2325: "0.255E-05 pm 31.21",
        2330: "0.249E-05 pm 31.33",
        2335: "0.242E-05 pm 31.46",
        2340: "0.236E-05 pm 31.58",
        2345: "0.229E-05 pm 31.7",
        2350: "0.223E-05 pm 31.82",
        2355: "0.217E-05 pm 31.95",
        2360: "0.212E-05 pm 32.07",
        2365: "0.206E-05 pm 32.2",
        2370: "0.201E-05 pm 32.32",
        2375: "0.195E-05 pm 32.45",
        2380: "0.190E-05 pm 32.58",
        2385: "0.185E-05 pm 32.7",
        2390: "0.180E-05 pm 32.83",
        2395: "0.176E-05 pm 32.96",
        2400: "0.171E-05 pm 33.09",
        2405: "0.166E-05 pm 33.22",
        2410: "0.162E-05 pm 33.35",
        2415: "0.158E-05 pm 33.48",
        2420: "0.154E-05 pm 33.61",
        2425: "0.150E-05 pm 33.75",
        2430: "0.146E-05 pm 33.88",
        2435: "0.142E-05 pm 34.01",
        2440: "0.138E-05 pm 34.15",
        2445: "0.135E-05 pm 34.28",
        2450: "0.131E-05 pm 34.42",
        2455: "0.128E-05 pm 34.55",
        2460: "0.124E-05 pm 34.69",
        2465: "0.121E-05 pm 34.83",
        2470: "0.118E-05 pm 34.97",
        2475: "0.115E-05 pm 35.11",
        2480: "0.112E-05 pm 35.25",
        2485: "0.109E-05 pm 35.39",
        2490: "0.106E-05 pm 35.53",
        2495: "0.103E-05 pm 35.67",
        2500: "0.100E-05 pm 35.82",
        2505: "0.977E-06 pm 35.96",
        2510: "0.952E-06 pm 36.1",
        2515: "0.927E-06 pm 36.25",
        2520: "0.902E-06 pm 36.4",
        2525: "0.879E-06 pm 36.54",
        2530: "0.856E-06 pm 36.69",
        2535: "0.833E-06 pm 36.84",
        2540: "0.811E-06 pm 36.99",
        2545: "0.790E-06 pm 37.14",
        2550: "0.769E-06 pm 37.29",
        2555: "0.749E-06 pm 37.45",
        2560: "0.730E-06 pm 37.6",
        2565: "0.710E-06 pm 37.76",
        2570: "0.692E-06 pm 37.91",
        2575: "0.674E-06 pm 38.07",
        2580: "0.656E-06 pm 38.23",
        2585: "0.639E-06 pm 38.39",
        2590: "0.622E-06 pm 38.55",
        2595: "0.606E-06 pm 38.71",
        2600: "0.590E-06 pm 38.87",
        2605: "0.574E-06 pm 39.04",
        2610: "0.559E-06 pm 39.2",
        2615: "0.545E-06 pm 39.37",
        2620: "0.530E-06 pm 39.54",
        2625: "0.516E-06 pm 39.71",
        2630: "0.503E-06 pm 39.88",
        2635: "0.490E-06 pm 40.05",
        2640: "0.477E-06 pm 40.23",
        2645: "0.464E-06 pm 40.4",
        2650: "0.452E-06 pm 40.58",
        2655: "0.440E-06 pm 40.75",
        2660: "0.429E-06 pm 40.93",
        2665: "0.418E-06 pm 41.11",
        2670: "0.407E-06 pm 41.29",
        2675: "0.396E-06 pm 41.47",
        2680: "0.386E-06 pm 41.65",
        2685: "0.375E-06 pm 41.83",
        2690: "0.366E-06 pm 42.01",
        2695: "0.356E-06 pm 42.2",
        2700: "0.347E-06 pm 42.38",
        2705: "0.338E-06 pm 42.57",
        2710: "0.329E-06 pm 42.76",
        2715: "0.320E-06 pm 42.95",
        2720: "0.312E-06 pm 43.14",
        2725: "0.304E-06 pm 43.33",
        2730: "0.296E-06 pm 43.53",
        2735: "0.288E-06 pm 43.72",
        2740: "0.280E-06 pm 43.91",
        2745: "0.273E-06 pm 44.11",
        2750: "0.266E-06 pm 44.3",
        2755: "0.259E-06 pm 44.5",
        2760: "0.252E-06 pm 44.69",
        2765: "0.246E-06 pm 44.89",
        2770: "0.239E-06 pm 45.09",
        2775: "0.233E-06 pm 45.28",
        2780: "0.227E-06 pm 45.48",
        2785: "0.221E-06 pm 45.68",
        2790: "0.215E-06 pm 45.88",
        2795: "0.209E-06 pm 46.08",
        2800: "0.204E-06 pm 46.27",
        2805: "0.199E-06 pm 46.46",
        2810: "0.193E-06 pm 46.65",
        2815: "0.188E-06 pm 46.85",
        2820: "0.183E-06 pm 47.04",
        2825: "0.179E-06 pm 47.23",
        2830: "0.174E-06 pm 47.42",
        2835: "0.169E-06 pm 47.61",
        2840: "0.165E-06 pm 47.8",
        2845: "0.161E-06 pm 48.0",
        2850: "0.157E-06 pm 48.19",
        2855: "0.152E-06 pm 48.39",
        2860: "0.148E-06 pm 48.58",
        2865: "0.145E-06 pm 48.78",
        2870: "0.141E-06 pm 48.98",
        2875: "0.137E-06 pm 49.18",
        2880: "0.134E-06 pm 49.38",
        2885: "0.130E-06 pm 49.58",
        2890: "0.127E-06 pm 49.78",
        2895: "0.123E-06 pm 49.98",
        2900: "0.120E-06 pm 50.19",
        2905: "0.117E-06 pm 50.4",
        2910: "0.114E-06 pm 50.6",
        2915: "0.111E-06 pm 50.81",
        2920: "0.108E-06 pm 51.02",
        2925: "0.105E-06 pm 51.24",
        2930: "0.103E-06 pm 51.45",
        2935: "0.999E-07 pm 51.67",
        2940: "0.972E-07 pm 51.89",
        2945: "0.947E-07 pm 52.11",
        2950: "0.922E-07 pm 52.33",
        2955: "0.898E-07 pm 52.56",
        2960: "0.875E-07 pm 52.79",
        2965: "0.852E-07 pm 53.02",
        2970: "0.830E-07 pm 53.25",
        2975: "0.808E-07 pm 53.48",
        2980: "0.787E-07 pm 53.72",
        2985: "0.766E-07 pm 53.96",
        2990: "0.746E-07 pm 54.2",
        2995: "0.727E-07 pm 54.45",
        3000: "0.708E-07 pm 54.7"
    }

    for i_mass in xsections:
        xsections[i_mass] = float(xsections[i_mass].split()[0])

    mass = myround(int(mass), base=5)

    if mass in xsections:
        return xsections[mass]
    else:
        return -1

def get_T1_xsection(mass):

    xsections = {
        500: 0.338E+02,
        505: 0.319E+02,
        510: 0.301E+02,
        515: 0.284E+02,
        520: 0.268E+02,
        525: 0.253E+02,
        530: 0.240E+02,
        535: 0.227E+02,
        540: 0.214E+02,
        545: 0.203E+02,
        550: 0.192E+02,
        555: 0.182E+02,
        560: 0.172E+02,
        565: 0.163E+02,
        570: 0.155E+02,
        575: 0.147E+02,
        580: 0.139E+02,
        585: 0.132E+02,
        590: 0.126E+02,
        595: 0.119E+02,
        600: 0.113E+02,
        605: 0.108E+02,
        610: 0.102E+02,
        615: 0.974E+01,
        620: 0.926E+01,
        625: 0.881E+01,
        630: 0.839E+01,
        635: 0.799E+01,
        640: 0.761E+01,
        645: 0.725E+01,
        650: 0.690E+01,
        655: 0.658E+01,
        660: 0.627E+01,
        665: 0.598E+01,
        670: 0.571E+01,
        675: 0.544E+01,
        680: 0.520E+01,
        685: 0.496E+01,
        690: 0.474E+01,
        695: 0.452E+01,
        700: 0.432E+01,
        705: 0.413E+01,
        710: 0.395E+01,
        715: 0.377E+01,
        720: 0.361E+01,
        725: 0.345E+01,
        730: 0.330E+01,
        735: 0.316E+01,
        740: 0.302E+01,
        745: 0.289E+01,
        750: 0.277E+01,
        755: 0.265E+01,
        760: 0.254E+01,
        765: 0.243E+01,
        770: 0.233E+01,
        775: 0.223E+01,
        780: 0.214E+01,
        785: 0.205E+01,
        790: 0.197E+01,
        795: 0.188E+01,
        800: 0.181E+01,
        805: 0.173E+01,
        810: 0.166E+01,
        815: 0.160E+01,
        820: 0.153E+01,
        825: 0.147E+01,
        830: 0.141E+01,
        835: 0.136E+01,
        840: 0.130E+01,
        845: 0.125E+01,
        850: 0.120E+01,
        855: 0.115E+01,
        860: 0.111E+01,
        865: 0.107E+01,
        870: 0.103E+01,
        875: 0.986E+00,
        880: 0.948E+00,
        885: 0.912E+00,
        890: 0.877E+00,
        895: 0.844E+00,
        900: 0.812E+00,
        905: 0.781E+00,
        910: 0.752E+00,
        915: 0.723E+00,
        920: 0.696E+00,
        925: 0.670E+00,
        930: 0.646E+00,
        935: 0.622E+00,
        940: 0.599E+00,
        945: 0.577E+00,
        950: 0.556E+00,
        955: 0.535E+00,
        960: 0.516E+00,
        965: 0.497E+00,
        970: 0.479E+00,
        975: 0.462E+00,
        980: 0.445E+00,
        985: 0.430E+00,
        990: 0.414E+00,
        995: 0.399E+00,
        1000: 0.385E+00,
        1005: 0.372E+00,
        1010: 0.359E+00,
        1015: 0.346E+00,
        1020: 0.334E+00,
        1025: 0.322E+00,
        1030: 0.311E+00,
        1035: 0.300E+00,
        1040: 0.290E+00,
        1045: 0.280E+00,
        1050: 0.270E+00,
        1055: 0.261E+00,
        1060: 0.252E+00,
        1065: 0.243E+00,
        1070: 0.235E+00,
        1075: 0.227E+00,
        1080: 0.219E+00,
        1085: 0.212E+00,
        1090: 0.205E+00,
        1095: 0.198E+00,
        1100: 0.191E+00,
        1105: 0.185E+00,
        1110: 0.179E+00,
        1115: 0.173E+00,
        1120: 0.167E+00,
        1125: 0.162E+00,
        1130: 0.156E+00,
        1135: 0.151E+00,
        1140: 0.146E+00,
        1145: 0.141E+00,
        1150: 0.137E+00,
        1155: 0.132E+00,
        1160: 0.128E+00,
        1165: 0.124E+00,
        1170: 0.120E+00,
        1175: 0.116E+00,
        1180: 0.112E+00,
        1185: 0.109E+00,
        1190: 0.105E+00,
        1195: 0.102E+00,
        1200: 0.985E-01,
        1205: 0.953E-01,
        1210: 0.923E-01,
        1215: 0.894E-01,
        1220: 0.866E-01,
        1225: 0.838E-01,
        1230: 0.812E-01,
        1235: 0.786E-01,
        1240: 0.762E-01,
        1245: 0.738E-01,
        1250: 0.715E-01,
        1255: 0.692E-01,
        1260: 0.671E-01,
        1265: 0.650E-01,
        1270: 0.630E-01,
        1275: 0.610E-01,
        1280: 0.591E-01,
        1285: 0.573E-01,
        1290: 0.556E-01,
        1295: 0.539E-01,
        1300: 0.522E-01,
        1305: 0.506E-01,
        1310: 0.491E-01,
        1315: 0.476E-01,
        1320: 0.461E-01,
        1325: 0.447E-01,
        1330: 0.434E-01,
        1335: 0.421E-01,
        1340: 0.408E-01,
        1345: 0.396E-01,
        1350: 0.384E-01,
        1355: 0.372E-01,
        1360: 0.361E-01,
        1365: 0.350E-01,
        1370: 0.340E-01,
        1375: 0.330E-01,
        1380: 0.320E-01,
        1385: 0.310E-01,
        1390: 0.301E-01,
        1395: 0.292E-01,
        1400: 0.284E-01,
        1405: 0.275E-01,
        1410: 0.267E-01,
        1415: 0.259E-01,
        1420: 0.252E-01,
        1425: 0.244E-01,
        1430: 0.237E-01,
        1435: 0.230E-01,
        1440: 0.224E-01,
        1445: 0.217E-01,
        1450: 0.211E-01,
        1455: 0.205E-01,
        1460: 0.199E-01,
        1465: 0.193E-01,
        1470: 0.187E-01,
        1475: 0.182E-01,
        1480: 0.177E-01,
        1485: 0.172E-01,
        1490: 0.167E-01,
        1495: 0.162E-01,
        1500: 0.157E-01,
        1505: 0.153E-01,
        1510: 0.148E-01,
        1515: 0.144E-01,
        1520: 0.140E-01,
        1525: 0.136E-01,
        1530: 0.132E-01,
        1535: 0.128E-01,
        1540: 0.125E-01,
        1545: 0.121E-01,
        1550: 0.118E-01,
        1555: 0.115E-01,
        1560: 0.111E-01,
        1565: 0.108E-01,
        1570: 0.105E-01,
        1575: 0.102E-01,
        1580: 0.993E-02,
        1585: 0.966E-02,
        1590: 0.939E-02,
        1595: 0.912E-02,
        1600: 0.887E-02,
        1605: 0.862E-02,
        1610: 0.838E-02,
        1615: 0.815E-02,
        1620: 0.792E-02,
        1625: 0.770E-02,
        1630: 0.749E-02,
        1635: 0.728E-02,
        1640: 0.708E-02,
        1645: 0.689E-02,
        1650: 0.670E-02,
        1655: 0.651E-02,
        1660: 0.633E-02,
        1665: 0.616E-02,
        1670: 0.599E-02,
        1675: 0.583E-02,
        1680: 0.567E-02,
        1685: 0.551E-02,
        1690: 0.536E-02,
        1695: 0.521E-02,
        1700: 0.507E-02,
        1705: 0.493E-02,
        1710: 0.480E-02,
        1715: 0.467E-02,
        1720: 0.454E-02,
        1725: 0.442E-02,
        1730: 0.430E-02,
        1735: 0.418E-02,
        1740: 0.407E-02,
        1745: 0.396E-02,
        1750: 0.385E-02,
        1755: 0.375E-02,
        1760: 0.365E-02,
        1765: 0.355E-02,
        1770: 0.345E-02,
        1775: 0.336E-02,
        1780: 0.327E-02,
        1785: 0.318E-02,
        1790: 0.310E-02,
        1795: 0.301E-02,
        1800: 0.293E-02,
        1805: 0.286E-02,
        1810: 0.278E-02,
        1815: 0.271E-02,
        1820: 0.263E-02,
        1825: 0.256E-02,
        1830: 0.249E-02,
        1835: 0.243E-02,
        1840: 0.236E-02,
        1845: 0.230E-02,
        1850: 0.224E-02,
        1855: 0.218E-02,
        1860: 0.212E-02,
        1865: 0.207E-02,
        1870: 0.201E-02,
        1875: 0.196E-02,
        1880: 0.191E-02,
        1885: 0.186E-02,
        1890: 0.181E-02,
        1895: 0.176E-02,
        1900: 0.171E-02,
        1905: 0.167E-02,
        1910: 0.163E-02,
        1915: 0.158E-02,
        1920: 0.154E-02,
        1925: 0.150E-02,
        1930: 0.146E-02,
        1935: 0.142E-02,
        1940: 0.139E-02,
        1945: 0.135E-02,
        1950: 0.131E-02,
        1955: 0.128E-02,
        1960: 0.125E-02,
        1965: 0.121E-02,
        1970: 0.118E-02,
        1975: 0.115E-02,
        1980: 0.112E-02,
        1985: 0.109E-02,
        1990: 0.106E-02,
        1995: 0.104E-02,
        2000: 0.101E-02,
        2005: 0.983E-03,
        2010: 0.957E-03,
        2015: 0.933E-03,
        2020: 0.908E-03,
        2025: 0.885E-03,
        2030: 0.862E-03,
        2035: 0.840E-03,
        2040: 0.818E-03,
        2045: 0.797E-03,
        2050: 0.776E-03,
        2055: 0.756E-03,
        2060: 0.737E-03,
        2065: 0.718E-03,
        2070: 0.699E-03,
        2075: 0.681E-03,
        2080: 0.664E-03,
        2085: 0.647E-03,
        2090: 0.630E-03,
        2095: 0.614E-03,
        2100: 0.598E-03,
        2105: 0.583E-03,
        2110: 0.568E-03,
        2115: 0.553E-03,
        2120: 0.539E-03,
        2125: 0.525E-03,
        2130: 0.512E-03,
        2135: 0.499E-03,
        2140: 0.486E-03,
        2145: 0.473E-03,
        2150: 0.461E-03,
        2155: 0.449E-03,
        2160: 0.438E-03,
        2165: 0.427E-03,
        2170: 0.416E-03,
        2175: 0.405E-03,
        2180: 0.395E-03,
        2185: 0.385E-03,
        2190: 0.375E-03,
        2195: 0.365E-03,
        2200: 0.356E-03,
        2205: 0.347E-03,
        2210: 0.338E-03,
        2215: 0.330E-03,
        2220: 0.321E-03,
        2225: 0.313E-03,
        2230: 0.305E-03,
        2235: 0.297E-03,
        2240: 0.290E-03,
        2245: 0.283E-03,
        2250: 0.275E-03,
        2255: 0.268E-03,
        2260: 0.262E-03,
        2265: 0.255E-03,
        2270: 0.248E-03,
        2275: 0.242E-03,
        2280: 0.236E-03,
        2285: 0.230E-03,
        2290: 0.224E-03,
        2295: 0.219E-03,
        2300: 0.213E-03,
        2305: 0.208E-03,
        2310: 0.202E-03,
        2315: 0.197E-03,
        2320: 0.192E-03,
        2325: 0.187E-03,
        2330: 0.183E-03,
        2335: 0.178E-03,
        2340: 0.174E-03,
        2345: 0.169E-03,
        2350: 0.165E-03,
        2355: 0.161E-03,
        2360: 0.157E-03,
        2365: 0.153E-03,
        2370: 0.149E-03,
        2375: 0.145E-03,
        2380: 0.142E-03,
        2385: 0.138E-03,
        2390: 0.134E-03,
        2395: 0.131E-03,
        2400: 0.128E-03,
        2405: 0.125E-03,
        2410: 0.121E-03,
        2415: 0.118E-03,
        2420: 0.115E-03,
        2425: 0.113E-03,
        2430: 0.110E-03,
        2435: 0.107E-03,
        2440: 0.104E-03,
        2445: 0.102E-03,
        2450: 0.991E-04,
        2455: 0.966E-04,
        2460: 0.941E-04,
        2465: 0.918E-04,
        2470: 0.895E-04,
        2475: 0.872E-04,
        2480: 0.850E-04,
        2485: 0.829E-04,
        2490: 0.808E-04,
        2495: 0.788E-04,
        2500: 0.768E-04,
        2505: 0.749E-04,
        2510: 0.730E-04,
        2515: 0.712E-04,
        2520: 0.694E-04,
        2525: 0.677E-04,
        2530: 0.660E-04,
        2535: 0.643E-04,
        2540: 0.627E-04,
        2545: 0.611E-04,
        2550: 0.596E-04,
        2555: 0.581E-04,
        2560: 0.566E-04,
        2565: 0.552E-04,
        2570: 0.538E-04,
        2575: 0.525E-04,
        2580: 0.512E-04,
        2585: 0.499E-04,
        2590: 0.486E-04,
        2595: 0.474E-04,
        2600: 0.462E-04,
        2605: 0.451E-04,
        2610: 0.439E-04,
        2615: 0.428E-04,
        2620: 0.418E-04,
        2625: 0.407E-04,
        2630: 0.397E-04,
        2635: 0.387E-04,
        2640: 0.377E-04,
        2645: 0.368E-04,
        2650: 0.359E-04,
        2655: 0.350E-04,
        2660: 0.341E-04,
        2665: 0.332E-04,
        2670: 0.324E-04,
        2675: 0.316E-04,
        2680: 0.308E-04,
        2685: 0.300E-04,
        2690: 0.293E-04,
        2695: 0.285E-04,
        2700: 0.278E-04,
        2705: 0.271E-04,
        2710: 0.265E-04,
        2715: 0.258E-04,
        2720: 0.251E-04,
        2725: 0.245E-04,
        2730: 0.239E-04,
        2735: 0.233E-04,
        2740: 0.227E-04,
        2745: 0.221E-04,
        2750: 0.216E-04,
        2755: 0.211E-04,
        2760: 0.205E-04,
        2765: 0.200E-04,
        2770: 0.195E-04,
        2775: 0.190E-04,
        2780: 0.185E-04,
        2785: 0.181E-04,
        2790: 0.176E-04,
        2795: 0.172E-04,
        2800: 0.168E-04,
        2805: 0.163E-04,
        2810: 0.159E-04,
        2815: 0.155E-04,
        2820: 0.151E-04,
        2825: 0.148E-04,
        2830: 0.144E-04,
        2835: 0.140E-04,
        2840: 0.137E-04,
        2845: 0.133E-04,
        2850: 0.130E-04,
        2855: 0.127E-04,
        2860: 0.124E-04,
        2865: 0.121E-04,
        2870: 0.118E-04,
        2875: 0.115E-04,
        2880: 0.112E-04,
        2885: 0.109E-04,
        2890: 0.106E-04,
        2895: 0.104E-04,
        2900: 0.101E-04,
        2905: 0.986E-05,
        2910: 0.961E-05,
        2915: 0.937E-05,
        2920: 0.914E-05,
        2925: 0.891E-05,
        2930: 0.869E-05,
        2935: 0.848E-05,
        2940: 0.827E-05,
        2945: 0.806E-05,
        2950: 0.786E-05,
        2955: 0.767E-05,
        2960: 0.748E-05,
        2965: 0.729E-05,
        2970: 0.711E-05,
        2975: 0.694E-05,
        2980: 0.677E-05,
        2985: 0.660E-05,
        2990: 0.644E-05,
        2995: 0.628E-05,
        3000: 0.612E-05,
    }

    mass = myround(int(mass), base=5)

    if mass in xsections:
        return xsections[mass]
    else:
        return -1


def main(event_tree_filenames, track_tree_output, nevents = -1, treename = "TreeMaker2/PreSelection", verbose = False, iEv_start = False, only_tagged_tracks = True, debug = False, save_cleaned_variables = False, update_gluino_masses = False):
    print "Input: %s" % event_tree_filenames
    print "Output: %s" % track_tree_output
    print "nevents: %s" % nevents
    print "iEv_start: %s" % iEv_start

    # store runs for JSON output:
    runs = {}

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
    print "Phase:", phase

    # load and configure data mask:
    if phase == 0:
        mask_file = TFile("Masks.root", "open")
        if is_data:
            h_mask = mask_file.Get("hEtaVsPhiDT_maskData-2016Data-2016")
        else:
            h_mask = mask_file.Get("hEtaVsPhiDT_maskMC-2016MC-2016")
        h_mask.SetDirectory(0)
        mask_file.Close()
        print "Loaded mask:", h_mask
    else:
        h_mask = False

    # load tree
    tree = TChain(treename)
    for iFile in event_tree_filenames:
        if "root.mimes" in iFile:
            continue
        tree.Add(iFile)
   
    fout = TFile(track_tree_output, "recreate")

    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()

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
    disappearing_track_tags = {"bdt": -10, "bdt_loose": -10, "bdt_looseloose": -10}

    tout = TTree("Events", "tout")

    # prepare variables for output tree   
    float_branches = ["weight", "MET", "MHT", "HT", "MinDeltaPhiMhtJets", "PFCaloMETRatio", "dilepton_invmass", "event", "run", "lumisec"]
    integer_branches = ["n_jets", "n_goodjets", "n_btags", "n_leptons", "n_goodleptons", "n_goodelectrons", "n_goodmuons", "n_allvertices", "n_NVtx", "dilepton_CR", "qcd_CR", "qcd_sideband_CR", "dilepton_leptontype", "passesUniversalSelection", "n_genLeptons", "n_genElectrons", "n_genMuons", "n_genTaus"]

    for tag in tags.tags:
        for region in tags.tags[tag]:
            integer_branches.append("n_%s_%s" % (tag, region))
        integer_branches.append("region_%s" % (tag))

    if not is_data:
        float_branches.append("madHT")
        float_branches.append("CrossSection")
        float_branches.append("puWeight")
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

    # get variables of treeUrlaubs
    track_variables = []
    for i in range(len(tree.GetListOfBranches())):
        label = tree.GetListOfBranches()[i].GetName()
        if "tracks_" in label:
            track_variables.append(label)

    vector_int_branches = ['tracks_is_pixel_track', 'tracks_pixelLayersWithMeasurement', 'tracks_trackerLayersWithMeasurement', 'tracks_nMissingInnerHits', 'tracks_nMissingMiddleHits', 'tracks_nMissingOuterHits', 'tracks_trackQualityHighPurity', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_fake', 'tracks_prompt_electron', 'tracks_prompt_muon', 'tracks_prompt_tau', 'tracks_prompt_tau_widecone', 'tracks_prompt_tau_leadtrk', 'tracks_passpionveto', 'tracks_passmask', 'tracks_is_reco_lepton', 'tracks_passPFCandVeto', 'tracks_charge', 'leptons_id']

    for dt_tag_label in disappearing_track_tags:
        vector_int_branches += ["tracks_tagged_%s" % dt_tag_label]

    for track_tag in tags.tags:
        vector_int_branches += ["tracks_%s" % track_tag]
    
    for branch in vector_int_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<int>', tree_branch_values[branch])

    vector_float_branches = ['tracks_dxyVtx', 'tracks_dzVtx', 'tracks_matchedCaloEnergy', 'tracks_trkRelIso', 'tracks_ptErrOverPt2', 'tracks_pt', 'tracks_eta', 'tracks_phi', 'tracks_trkMiniRelIso', 'tracks_trackJetIso', 'tracks_ptError', 'tracks_neutralPtSum', 'tracks_neutralWithoutGammaPtSum', 'tracks_minDrLepton', 'tracks_matchedCaloEnergyJets', 'tracks_deDxHarmonic2pixel', 'tracks_deDxHarmonic2strips', 'tracks_massfromdeDxPixel', 'tracks_massfromdeDxStrips', 'tracks_massfromdeDxWeightedByValidHits', 'tracks_chi2perNdof', 'tracks_chargedPtSum', 'tracks_chiCandGenMatchingDR', 'tracks_LabXYcm', 'leptons_pt', 'leptons_eta', 'leptons_phi']
    for dt_tag_label in disappearing_track_tags:
        vector_float_branches += ["tracks_mva_%s" % dt_tag_label]
    for branch in vector_float_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<double>', tree_branch_values[branch])
    
    # configure some histograms:
    histograms = {}
    if update_gluino_masses:
        histograms["gluino_mass"] = TH1D("h_gluino_mass", "h_gluino_mass", 4000, 0, 4000)
        histograms["chargino_mass"] = TH1D("h_chargino_mass", "h_chargino_mass", 4000, 0, 4000)    
        histograms["neutralino_mass"] = TH1D("h_neutralino_mass", "h_neutralino_mass", 4000, 0, 4000)    
    
    print "Looping over %s events" % nev

    for iEv, event in enumerate(tree):

        if iEv_start and iEv < begin_event: continue
        if nevents > 0 and iEv > nevents: break      
        if (iEv+1) % 1000 == 0:
            print "event %s / %s" % (iEv + 1, nev)

        if update_gluino_masses:
            # output gluino mass histogram:
            def fill_mass_histograms(label, pdgId):
                masses = []
                for i_genParticle, genParticle in enumerate(event.GenParticles):
                    if abs(event.GenParticles_PdgId[i_genParticle]) == pdgId:
                        masses.append( round(genParticle.M()) )
                for mass in list(set(masses)):
                    histograms[label].Fill(mass)

            fill_mass_histograms("gluino_mass", 1000021)
            fill_mass_histograms("chargino_mass", 1000022)
            fill_mass_histograms("neutralino_mass", 1000024)
        
        # basic event selection:
        passed_UniversalSelection = passesUniversalSelection(event)
        if not passed_UniversalSelection: continue

        # count number of good leptons:
        lepton_level_output = []
        n_goodelectrons = 0
        n_goodmuons = 0
        for i, electron in enumerate(event.Electrons):
            if electron.Pt() > 30 and abs(electron.Eta()) < 2.4 and bool(event.Electrons_mediumID[i]):

                # check for jets:
                for jet in event.Jets:
                    if jet.DeltaR(electron) < 0.1: continue

                n_goodelectrons += 1
                lepton_level_output.append({"leptons_pt": electron.Pt(),
                                             "leptons_eta": electron.Eta(),
                                             "leptons_phi": electron.Phi(),
                                             "leptons_id": 11,
                                             })
        for i, muon in enumerate(event.Muons):
            if muon.Pt() > 30 and abs(muon.Eta()) < 2.4 and bool(event.Muons_tightID[i]):

                # check for jets:
                for jet in event.Jets:
                    if jet.DeltaR(muon) < 0.1: continue

                n_goodmuons += 1
                lepton_level_output.append({"leptons_pt": muon.Pt(),
                                             "leptons_eta": muon.Eta(),
                                             "leptons_phi": muon.Phi(),
                                             "leptons_id": 13,
                                             })

        n_goodleptons = n_goodelectrons + n_goodmuons

        # throw away low-MHT events for zero good leptons:
        if n_goodleptons==0 and event.MHT<50: continue

        # get T2bt and T1qqqq xsections
        current_file_name = tree.GetFile().GetName()
        if "T2bt" in current_file_name:
            for i_genParticle, genParticle in enumerate(event.GenParticles):
                if abs(event.GenParticles_PdgId[i_genParticle]) == 1000024:
                    parent_id = event.GenParticles_ParentIdx[i_genParticle]
                    parent_pdgid = abs(event.GenParticles_PdgId[parent_id])
                    if parent_pdgid == 1000005 or parent_pdgid == 1000006:
                        parent_mass = event.GenParticles[parent_id].M()
                        xsection = get_sbottom_antisbottom_cross_section(parent_mass)
                        event.CrossSection = xsection
        elif "g1800_chi1400_27_200970" in current_file_name:
            event.CrossSection = 0.00276133 #pb
        elif "T1qqqq" in current_file_name:
            for i_genParticle, genParticle in enumerate(event.GenParticles):
                if abs(event.GenParticles_PdgId[i_genParticle]) == 1000024:
                    parent_id = event.GenParticles_ParentIdx[i_genParticle]
                    parent_pdgid = abs(event.GenParticles_PdgId[parent_id])
                    if parent_pdgid == 1000021:
                        parent_mass = event.GenParticles[parent_id].M()
                        xsection = get_T1_xsection(parent_mass)
                        event.CrossSection = xsection

        # collect lumisections:
        if is_data:
            runnum = event.RunNum
            lumisec = event.LumiBlockNum
            if runnum not in runs:
                runs[runnum] = []
            if lumisec not in runs[runnum]:
                runs[runnum].append(lumisec)
            weight = event.PrescaleWeightHT
        else:
            weight = 1.0 * event.puWeight * event.CrossSection

        if tree.GetBranch("madHT"):
            madHT = event.madHT
            if not pass_background_stitching(current_file_name, madHT, phase): continue
        else:
            madHT = -1

        # reset all branch values:
        for label in tree_branch_values:
            if "tracks_" in label or "leptons_" in label:
                continue
            tree_branch_values[label][0] = -1

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
                if lepton.Pt() > min_lepton_pt:
                    if lepton_type == "Electrons": selected_e_indices.append(i)
                    elif lepton_type == "Muons": selected_mu_indices.append(i)                

        if (len(selected_e_indices) == 2 and len(selected_mu_indices) == 0):
            if bool(event.Electrons_mediumID[selected_e_indices[0]]) and bool(event.Electrons_mediumID[selected_e_indices[1]]):
                if (event.Electrons_charge[selected_e_indices[0]] * event.Electrons_charge[selected_e_indices[1]] < 0):
                    invariant_mass = (event.Electrons[selected_e_indices[0]] + event.Electrons[selected_e_indices[1]]).M()
                    if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                        if bool(event.Electrons_passIso[selected_e_indices[0]]) and bool(event.Electrons_passIso[selected_e_indices[1]]):
                            if abs(event.Electrons[selected_e_indices[0]].Eta()) < 2.4 and abs(event.Electrons[selected_e_indices[1]].Eta()) < 2.4:
                                tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                tree_branch_values["dilepton_leptontype"][0] = 11
                                tree_branch_values["dilepton_CR"][0] = 1
                                dilepton_CR = True       

        elif (len(selected_mu_indices) == 2 and len(selected_e_indices) == 0):
            if (bool(event.Muons_tightID[selected_mu_indices[0]]) and bool(event.Muons_tightID[selected_mu_indices[1]])):
                if (event.Muons_charge[selected_mu_indices[0]] * event.Muons_charge[selected_mu_indices[1]] < 0):
                    invariant_mass = (event.Muons[selected_mu_indices[0]] + event.Muons[selected_mu_indices[1]]).M()            
                    if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                        if bool(event.Muons_passIso[selected_mu_indices[0]]) and bool(event.Muons_passIso[selected_mu_indices[1]]):
                            if abs(event.Muons[selected_mu_indices[0]].Eta()) < 2.4 and abs(event.Muons[selected_mu_indices[1]].Eta()) < 2.4:
                                tree_branch_values["dilepton_invmass"][0] = invariant_mass
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
        
        # count number of good jets:
        n_goodjets = 0
        goodjets = []
        for jet in event.Jets:
            if jet.Pt() > 30 and abs(jet.Eta()) < 2.4:
                for lepton in list(event.Muons) + list(event.Electrons):
                    if jet.DeltaR(lepton) < 0.5:
                        continue
                n_goodjets += 1
                goodjets.append(jet)

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

        ## reset tagged tracks counter to zero:
        for tag in tags.tags:
            for region in tags.tags[tag]:
                tree_branch_values["n_%s_%s" % (tag, region)][0] = 0
     
        # for each event, first fill this list for each track         
        track_level_output = []
        event_contains_tagged_tracks = False

        for iCand, track in enumerate(event.tracks):

            # basic track selection:
            if track.Pt() < 30 or not isBaselineTrack(track, iCand, event) or not pass_mask(h_mask, track) or not pass_pion_veto(event, iCand, deltaR=0.03):
                continue

            is_reco_lepton = check_is_reco_lepton(event, track, deltaR = 0.01)
            ptErrOverPt2 = event.tracks_ptError[iCand] / (track.Pt()**2)

            # check disappearing track tags:
            min_score = 0
            for dt_tag_label in disappearing_track_tags:                              
                disappearing_track_tags[dt_tag_label] = get_disappearing_track_score(dt_tag_label, event, iCand, readers)
                if disappearing_track_tags[dt_tag_label] < min_score:
                    min_score = disappearing_track_tags[dt_tag_label]
            if min_score == -10:
                continue

            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            elif event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = False

            # recalculate track-jet-DR:
            track_jet_mindeltaR = 9999
            for jet in goodjets:
                deltaR = jet.DeltaR(track)
                if deltaR < track_jet_mindeltaR:
                    track_jet_mindeltaR = deltaR
            

            # evaluate tags:
            track_is_tagged_as_label = []
            track_is_tagged = False
            for tag in tags.tags:

                # veto DTs too close to jets
                if track_jet_mindeltaR<0.4: continue

                for region in tags.tags[tag]:
                    input_variables = {"tracks_is_pixel_track": is_pixel_track,
                                       "tracks_mva_bdt_loose": disappearing_track_tags["bdt_loose"],
                                       "tracks_dxyVtx": event.tracks_dxyVtx[iCand],
                                       "tracks_trkRelIso": event.tracks_trkRelIso[iCand],
                                      }
                    if tags.convert_cut_string(tags.tags[tag][region], input_variables = input_variables):
                        tree_branch_values["n_%s_%s" % (tag, region)][0] += 1
                        track_is_tagged = True
                        event_contains_tagged_tracks = True
                        if "SR" in region:
                            track_is_tagged_as_label.append(tag)
            if only_tagged_tracks and not track_is_tagged:
                continue

            track_is_tagged_as_label = sorted(list(set(track_is_tagged_as_label)))

            # check if actual fake track (no genparticle in cone around track):
            is_prompt_electron = False
            is_prompt_muon = False
            is_prompt_tau = False
            is_prompt_tau_leadtrk = False
            is_prompt_tau_widecone = False

            if not is_data:
                for k in range(len(event.GenParticles)):
                    deltaR = track.DeltaR(event.GenParticles[k])
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
                                deltaR = track.DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.04:
                                    is_prompt_tau_leadtrk = True
                                if deltaR < 0.4:
                                    is_prompt_tau_widecone = True

            is_fake_track = not (is_prompt_electron or is_prompt_muon or is_prompt_tau or is_prompt_tau_leadtrk)

            tracks_massfromdeDxPixel = TMath.Sqrt((event.tracks_deDxHarmonic2pixel[iCand]-2.557)*pow(track.P(),2)/2.579)
            tracks_massfromdeDxStrips = TMath.Sqrt((event.tracks_deDxHarmonic2strips[iCand]-2.557)*pow(track.P(),2)/2.579)
            
            if not tracks_massfromdeDxPixel > 0: tracks_massfromdeDxPixel = -1
            if not tracks_massfromdeDxStrips > 0: tracks_massfromdeDxStrips = -1

            # disappearing track counters:
            if debug: print "Found disappearing track in event %s, charged genLeptons in cone: %s" % (iEv, charged_genlepton_in_track_cone)

            track_level_output.append(
                                   {
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
                                     "tracks_pt": track.Pt(),
                                     "tracks_eta": track.Eta(),
                                     "tracks_phi": track.Phi(),
                                     "tracks_prompt_electron": is_prompt_electron,
                                     "tracks_prompt_muon": is_prompt_muon,
                                     "tracks_prompt_tau": is_prompt_tau,
                                     "tracks_prompt_tau_leadtrk": is_prompt_tau_leadtrk,
                                     "tracks_prompt_tau_widecone": is_prompt_tau_widecone,
                                     "tracks_passpionveto": True,
                                     "tracks_passmask": True,
                                     "tracks_is_reco_lepton": is_reco_lepton,
                                     "tracks_trkMiniRelIso": event.tracks_trkMiniRelIso[iCand],
                                     #"tracks_trackJetIso": event.tracks_trackJetIso[iCand],
                                     "tracks_trackJetIso": track_jet_mindeltaR,
                                     "tracks_ptError": event.tracks_ptError[iCand],
                                     "tracks_passPFCandVeto": bool(event.tracks_passPFCandVeto[iCand]),
                                     "tracks_neutralPtSum": event.tracks_neutralPtSum[iCand],
                                     "tracks_neutralWithoutGammaPtSum": event.tracks_neutralWithoutGammaPtSum[iCand],
                                     "tracks_minDrLepton": event.tracks_minDrLepton[iCand],
                                     "tracks_matchedCaloEnergyJets": event.tracks_matchedCaloEnergyJets[iCand],
                                     "tracks_deDxHarmonic2pixel": event.tracks_deDxHarmonic2pixel[iCand],
                                     "tracks_deDxHarmonic2strips": event.tracks_deDxHarmonic2strips[iCand],
                                     "tracks_massfromdeDxPixel": tracks_massfromdeDxPixel,
                                     "tracks_massfromdeDxStrips": tracks_massfromdeDxStrips,
                                     "tracks_chi2perNdof": event.tracks_chi2perNdof[iCand],
                                     "tracks_chargedPtSum": event.tracks_chargedPtSum[iCand],
                                     "tracks_charge": event.tracks_charge[iCand],
                                   }
                                  )
                                  
            # add track tag information:
            for dt_tag_label in disappearing_track_tags:

                # veto DTs too close to jets
                if track_jet_mindeltaR<0.4: continue

                track_level_output[-1]["tracks_mva_%s" % dt_tag_label] = disappearing_track_tags[dt_tag_label]
                if disappearing_track_tags[dt_tag_label] > -10:
                    track_level_output[-1]["tracks_tagged_%s" % dt_tag_label] = 1
                else:
                    track_level_output[-1]["tracks_tagged_%s" % dt_tag_label] = 0

            for tag in tags.tags:
                if tag in track_is_tagged_as_label:
                    track_level_output[-1]["tracks_%s" % tag] = 1
                else:
                    track_level_output[-1]["tracks_%s" % tag] = 0

            # if signal, do chargino matching:
            if tree.GetBranch("GenParticles") and ("g1800" in event_tree_filenames[0] or "SMS-" in event_tree_filenames[0]):
                deltaR = 0
                for k in range(len(event.GenParticles)):
                    if abs(event.GenParticles_PdgId[k]) == 1000024 and event.GenParticles_Status[k] == 1:
                        deltaR = track.DeltaR(event.GenParticles[k])
                        if deltaR < 0.01:
                            track_level_output[-1]["tracks_chiCandGenMatchingDR"] = deltaR
                            break

            if debug:
                for line in sorted(track_level_output[-1].keys()):
                    print "%s: %s" %(line, track_level_output[-1][line])

        if only_tagged_tracks and not event_contains_tagged_tracks:
            continue

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

        # save region number depending on track tag:
        for tag in tags.tags:

            n_DT = 0
            is_pixel_track = False
            DeDxAverage = -1
    
            for i in range(len(track_level_output)):
                if track_level_output[i]["tracks_%s" % tag] == 1:
                    n_DT += 1
                    DeDxAverage = track_level_output[i]["tracks_deDxHarmonic2pixel"]
                    is_pixel_track = track_level_output[i]["tracks_is_pixel_track"]

            region = get_signal_region(event.HT, event.MHT, n_goodjets, event.BTags, MinDeltaPhiMhtJets, n_DT, is_pixel_track, DeDxAverage, n_goodelectrons, n_goodmuons, event_tree_filenames[0])
            tree_branch_values["region_%s" % tag][0] = region

        # save event-level variables:
        try:
            tree_branch_values["run"][0] = event.RunNum
            tree_branch_values["lumisec"][0] = event.LumiBlockNum
        except:
            print "Error while saving event number info"
        tree_branch_values["passesUniversalSelection"][0] = passed_UniversalSelection
        tree_branch_values["n_leptons"][0] = len(event.Electrons) + len(event.Muons)
        tree_branch_values["n_goodleptons"][0] = n_goodleptons
        tree_branch_values["n_goodelectrons"][0] = n_goodelectrons
        tree_branch_values["n_goodmuons"][0] = n_goodmuons
        tree_branch_values["n_btags"][0] = event.BTags
        tree_branch_values["n_jets"][0] = len(event.Jets)
        tree_branch_values["n_goodjets"][0] = n_goodjets
        tree_branch_values["n_allvertices"][0] = event.nAllVertices
        tree_branch_values["PFCaloMETRatio"][0] = event.PFCaloMETRatio
        tree_branch_values["MET"][0] = event.MET
        tree_branch_values["MHT"][0] = event.MHT
        tree_branch_values["HT"][0] = event.HT
        tree_branch_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets
        tree_branch_values["n_NVtx"][0] = event.NVtx
        tree_branch_values["weight"][0] = weight
        if not is_data:
            tree_branch_values["madHT"][0] = madHT
            tree_branch_values["CrossSection"][0] = event.CrossSection
            tree_branch_values["puWeight"][0] = event.puWeight
         
        # track-level variables:
        n_tracks = len(track_level_output)
        #tree_branch_values["tracks"] = ROOT.std.vector(TLorentzVector)(n_tracks)
      
        for branch in vector_int_branches:
            if "tracks_" in branch:
                tree_branch_values[branch] = ROOT.std.vector(int)(n_tracks)
            elif "leptons_" in branch:
                tree_branch_values[branch] = ROOT.std.vector(int)(n_goodleptons)
        for branch in vector_float_branches:
            if "tracks_" in branch:
                tree_branch_values[branch] = ROOT.std.vector(double)(n_tracks)
            elif "leptons_" in branch:
                tree_branch_values[branch] = ROOT.std.vector(double)(n_goodleptons)

        # register track-level branches:
        for label in tree_branch_values:
            if "tracks_" in label or "leptons_" in label:
                tout.SetBranchAddress(label, tree_branch_values[label])

        # save track-level properties:
        for i, track_output_dict in enumerate(track_level_output):
            for label in track_output_dict:
                tree_branch_values[label][i] = track_output_dict[label]

        # save lepton properties vector:
        for i, lepton_output_dict in enumerate(lepton_level_output):
            for label in lepton_output_dict:
                tree_branch_values[label][i] = lepton_output_dict[label]

        tout.Fill()
             
    for label in histograms:
        histograms[label].Write()
             
    fout.cd()

    if h_mask:
        mask_file.Close()

    fout.cd()
    fout.Write()
    fout.Close()

    # write histograms:
    #fout = TFile(track_tree_output, "open")
    #print h_gluino_mass
    #h_gluino_mass.Write()
    #fout.Close()
    
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
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--iEv_start", dest = "iEv_start", default = 0)
    parser.add_option("--debug", dest = "debug", action = "store_true")
    parser.add_option("--tags", dest = "only_tagged_tracks", action = "store_true")
    (options, args) = parser.parse_args()
    
    options.inputfiles = options.inputfiles.split(",")
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
    
    main(options.inputfiles,
         options.outputfiles,
         nevents = int(options.nev),
         iEv_start = int(options.iEv_start),
         only_tagged_tracks = False,
         debug = options.debug)
