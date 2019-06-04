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
    #if not t.globalSuperTightHalo2016Filter: return False
    if not t.globalTightHalo2016Filter: return False
    if not t.HBHEIsoNoiseFilter: return False
    if not t.HBHENoiseFilter: return False
    if not t.BadChargedCandidateFilter: return False
    if not t.BadPFMuonFilter: return False
    if not t.CSCTightHaloFilter: return False
    #if not t.ecalBadCalibFilter: return False #this says it's deprecated
    if not t.EcalDeadCellTriggerPrimitiveFilter: return False
    if not t.eeBadScFilter: return False 
    return True


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
               }
    
    for label in bdts:
        readers[label] = {}
        readers[label]["tmva_variables"] = {}
        readers[label]["info"] = get_tmva_info(bdts[label])
        readers[label]["reader"] = prepareReader(bdts[label] + '/weights/TMVAClassification_BDT.weights.xml', readers[label]["info"]["variables"], readers[label]["info"]["spectators"], readers[label]["tmva_variables"])

    return readers
    

def check_is_disappearing_track(event, iCand, readers, loose = False):
    
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
    
    if is_pixel_track and score > 0.1:
        return score
    elif not is_pixel_track and score > 0.25:
        return score
    else:
        return -10
    
    
def check_is_reco_lepton(event, iCand, deltaR = 0.01):
    # re-check PF lepton veto:
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


def main(event_tree_filenames, track_tree_output, fakerate_file = False, nevents = -1, treename = "TreeMaker2/PreSelection", mask_file = False, only_fakerate = False, verbose = False, iEv_start = False, debug = False):

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
    for label in ["Summer16", "Fall17", "Autumn18", "Run2016", "Run2017", "Run2018"]:
        if label in event_tree_filenames[0]:
            data_period = label
            if "Run201" in label:
                is_data = True
            if label == "Summer16" or label == "Run2016":
                phase = 0
            elif label == "Fall17" or label == "Autumn18" or label == "Run2017" or label == "Run2018":
                phase = 1
    if len(data_period) == 0:
        print "Can't determine data/MC era"
        quit(1)
    print "data_period: %s, phase: %s" % (data_period, phase)

    # load BDTs and fetch list of DT tag labels
    readers = load_tmva_readers(phase)
    disappearing_track_tags = {"bdt": -10, "bdt_loose": -10}

    tout = TTree("Events", "tout")

    # prepare variables for output tree   
    float_branches = ["MET", "MHT", "HT", "MinDeltaPhiMhtJets", "PFCaloMETRatio", "dilepton_invmass"]
    integer_branches = ["n_jets", "n_btags", "n_leptons", "n_allvertices", "n_NVtx", "EvtNumEven", "dilepton_CR", "qcd_CR", "qcd_sideband_CR", "meta_CR", "dilepton_leptontype", "passesUniversalSelection", "n_genLeptons", "n_genElectrons", "n_genMuons", "n_genTaus"]

    for dt_tag_label in disappearing_track_tags:
        integer_branches += ["n_DT_%s" % dt_tag_label]
        integer_branches += ["n_DT_actualfake_%s" % dt_tag_label]

    if not is_data:
        float_branches.append("madHT")
        float_branches.append("CrossSection")
        float_branches.append("puWeight")
        float_branches.append("NumInteractions")
    if only_fakerate:
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
    region_output = []
    region_noDT_output = []
    tree_branch_values["region"] = 0
    tree_branch_values["region_noDT"] = 0
    tout.Branch("region", 'std::vector<int>', tree_branch_values["region"])
    tout.Branch("region_noDT", 'std::vector<int>', tree_branch_values["region_noDT"])


    # TODO
    #region_output = {}
    #for dt_tag_label in disappearing_track_tags:   
    #region_output = []
    #region_noDT_output = []
    #tree_branch_values["regio
    

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

    vector_int_branches = ['tracks_is_pixel_track', 'tracks_pixelLayersWithMeasurement', 'tracks_trackerLayersWithMeasurement', 'tracks_nMissingInnerHits', 'tracks_nMissingMiddleHits', 'tracks_nMissingOuterHits', 'tracks_trackQualityHighPurity', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_actualfake', 'tracks_promptbg', 'tracks_promptelectron', 'tracks_promptmuon', 'tracks_prompttau', 'tracks_prompttau_wideDR', 'tracks_passpionveto', 'tracks_is_baseline_track', 'tracks_is_reco_lepton', 'tracks_passPFCandVeto', 'tracks_charge']    
    for dt_tag_label in disappearing_track_tags:
        vector_int_branches += ["tracks_tagged_%s" % dt_tag_label]
    
    for branch in vector_int_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<int>', tree_branch_values[branch])

    vector_float_branches = ['tracks_dxyVtx', 'tracks_dzVtx', 'tracks_matchedCaloEnergy', 'tracks_trkRelIso', 'tracks_ptErrOverPt2', 'tracks_pt', 'tracks_P', 'tracks_eta', 'tracks_phi', 'tracks_trkMiniRelIso', 'tracks_trackJetIso', 'tracks_ptError', 'tracks_neutralPtSum', 'tracks_neutralWithoutGammaPtSum', 'tracks_minDrLepton', 'tracks_matchedCaloEnergyJets', 'tracks_deDxHarmonic2pixel', 'tracks_deDxHarmonic2strips', 'tracks_deDxHarmonics2WeightedByValidHits', 'tracks_massfromdeDxPixel', 'tracks_massfromdeDxStrips', 'tracks_massfromdeDxWeightedByValidHits', 'tracks_chi2perNdof', 'tracks_chargedPtSum']
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

    # load fake rate histograms:
    fakerate_regions = ["dilepton", "qcd", "qcd_sideband", "dilepton_short", "qcd_short", "qcd_sideband_short", "dilepton_long", "qcd_long", "qcd_sideband_long"]
    fakerate_variables = ["HT", "n_allvertices", "HT:n_allvertices", "HT:n_allvertices_interpolated"]
    if not only_fakerate and fakerate_file:
        
        # load fakerate maps:
        fakerate_file = TFile(fakerate_file, "open")

        # get all fakerate histograms:
        h_fakerates = {}
        for region in fakerate_regions:
                for variable in fakerate_variables:
                    if "dilepton" in region:
                        variable = variable.replace("HT", "HT_cleaned")
                    else:
                        variable = variable.replace("_cleaned", "")
                        
                    #hist_name = region + category + "/" + data_period + "/fakerate_" + variable.replace(":", "_")
                    hist_name = region + "/" + "Summer16" + "/fakerate_" + variable.replace(":", "_")
                    
                    hist_name = hist_name.replace("//", "/")
                    try:
                        h_fakerates[hist_name] = fakerate_file.Get(hist_name)
                    except:
                        print "Error reading fakerate:", hist_name

        # add all raw fakerate branches:        
        for region in fakerate_regions:
            for variable in fakerate_variables:
                if "dilepton" in region:
                    variable = variable.replace("HT", "HT_cleaned")
                else:
                    variable = variable.replace("_cleaned", "")

                branch_name = "fakerate_%s_%s" % (region, variable.replace(":", "_"))
                tree_branch_values[branch_name] = array( 'f', [ 0 ] )
                tout.Branch( branch_name, tree_branch_values[branch_name], '%s/F' % branch_name )


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

        # set selection flags (veto event later if it does not fit into any selection):
        dilepton_CR = False
        qcd_CR = False
        qcd_sideband_CR = False

        min_lepton_pt = 30.0
        invariant_mass = 0
        if (len(event.Electrons) == 2 and len(event.Muons) == 0):
            if (event.Electrons[0].Pt() > min_lepton_pt):
                if bool(event.Electrons_mediumID[0]) and bool(event.Electrons_mediumID[1]):
                    if (event.Electrons_charge[0] * event.Electrons_charge[1] < 0):
                        invariant_mass = (event.Electrons[0] + event.Electrons[1]).M()
                        if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                            if bool(event.Electrons_passIso[0]) and bool(event.Electrons_passIso[1]):
                                if abs(event.Electrons[0].Eta()) < 2.4 and abs(event.Electrons[1].Eta()):
                                    tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                    tree_branch_values["dilepton_leptontype"][0] = 11
                                    tree_branch_values["dilepton_CR"][0] = 1
                                    dilepton_CR = True       
        elif (len(event.Muons) == 2 and len(event.Electrons) == 0):
            if (event.Muons[0].Pt() > min_lepton_pt):
                if (bool(event.Muons_tightID[0]) and bool(event.Muons_tightID[1])):
                    if (event.Muons_charge[0] * event.Muons_charge[1] < 0):
                        invariant_mass = (event.Muons[0] + event.Muons[1]).M()            
                        if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                            if bool(event.Muons_passIso[0]) and bool(event.Muons_passIso[1]):
                                if abs(event.Muons[0].Eta()) < 2.4 and abs(event.Muons[1].Eta()):
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
        if only_fakerate:
            if not dilepton_CR and not qcd_CR and not qcd_sideband_CR: continue
                
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
     
        # for each event, first fill this list for each track         
        track_level_output = []

        for iCand in range(len(event.tracks)):

            is_reco_lepton = check_is_reco_lepton(event, iCand, deltaR = 0.01)
            if is_reco_lepton: continue
            
            passpionveto = pass_pion_veto(event, iCand, deltaR = 0.03)        
            if not passpionveto: continue
            
            ptErrOverPt2 = event.tracks_ptError[iCand] / (event.tracks[iCand].Pt()**2)

            # check disappearing track tags:
            for dt_tag_label in disappearing_track_tags:
                
                disappearing_track_tags[dt_tag_label] = -10
                
                loose = False
                if "loose" in dt_tag_label:
                    loose = True
                    
                if not isBaselineTrack(event.tracks[iCand], iCand, event, h_mask, loose = loose):
                    continue

                disappearing_track_tags[dt_tag_label] = check_is_disappearing_track(event, iCand, readers, loose = loose)

            keep_track = False
            for dt_tag_label in disappearing_track_tags:
                if disappearing_track_tags[dt_tag_label] > -10:
                    keep_track = True
            if not keep_track: continue

            is_pixel_track = True
            if event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = False
             
            # check if actual fake track (no genparticle in cone around track):
            charged_genlepton_in_track_cone = False
            is_prompt_bg = False
            is_prompt_electron = False
            is_prompt_muon = False
            is_tau_bg = False
            is_tau_bg_wideDR = False

            # check MC Truth for prompt/non-prompt background:
            if not is_data:
                for k in range(len(event.GenParticles)):

                    if charged_genlepton_in_track_cone: break

                    deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                    gen_track_cone_pdgid = abs(event.GenParticles_PdgId[k])

                    if deltaR < 0.02:
                          
                        if (gen_track_cone_pdgid == 11 or gen_track_cone_pdgid == 13) and event.GenParticles_Status[k] == 1:
                            charged_genlepton_in_track_cone = True
                            is_prompt_bg = True
                            if gen_track_cone_pdgid == 11: 
                                is_prompt_electron = True
                            if gen_track_cone_pdgid == 13: 
                                is_prompt_muon = True
                            break
                        elif gen_track_cone_pdgid == 15:
                            # if genTau, check if the track matches with a GenTaus_LeadTrk track:
                            for l in range(len(event.GenTaus_LeadTrk)):
                                deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.04:
                                    print "That's a tau leading track"
                                    charged_genlepton_in_track_cone = True
                                    is_tau_bg = True
                                    break

                    # if track seems to be fake, check again with wider DR for gentau:
                    if gen_track_cone_pdgid == 15 and deltaR < 0.4:
                        is_tau_bg_wideDR = True
                        print "Found tau within a wide cone"
                        charged_genlepton_in_track_cone = True
                        break

            tracks_massfromdeDxPixel = TMath.Sqrt((event.tracks_deDxHarmonic2pixel[iCand]-2.557)*pow(event.tracks[iCand].P(),2)/2.579)
            tracks_massfromdeDxStrips = TMath.Sqrt((event.tracks_deDxHarmonic2strips[iCand]-2.557)*pow(event.tracks[iCand].P(),2)/2.579)
            tracks_massfromdeDxWeightedByValidHits = (tracks_massfromdeDxStrips * event.tracks_nValidPixelHits[iCand] + tracks_massfromdeDxStrips*event.tracks_nValidTrackerHits[iCand])/(event.tracks_nValidPixelHits[iCand] + event.tracks_nValidTrackerHits[iCand])
            
            if not tracks_massfromdeDxPixel > 0: tracks_massfromdeDxPixel = -1
            if not tracks_massfromdeDxStrips > 0: tracks_massfromdeDxStrips = -1
            if not tracks_massfromdeDxWeightedByValidHits > 0: tracks_massfromdeDxWeightedByValidHits = -1

            # disappearing track counters:
            if debug: print "Found disappearing track in event %s, charged genLeptons in cone: %s" % (iEv, charged_genlepton_in_track_cone)

            track_level_output.append(
                                   {
                                     "tracks": event.tracks[iCand],
                                     "tracks_is_pixel_track": is_pixel_track,
                                     "tracks_pixelLayersWithMeasurement": event.tracks_pixelLayersWithMeasurement[iCand],
                                     "tracks_trackerLayersWithMeasurement": event.tracks_trackerLayersWithMeasurement[iCand],
                                     "tracks_actualfake": not charged_genlepton_in_track_cone,
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
                                     "tracks_promptbg": is_prompt_bg,
                                     "tracks_promptelectron": is_prompt_electron,
                                     "tracks_promptmuon": is_prompt_muon,
                                     "tracks_prompttau": is_tau_bg,
                                     "tracks_prompttau_wideDR": is_tau_bg_wideDR,
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
                                     "tracks_deDxHarmonics2WeightedByValidHits": (event.tracks_deDxHarmonic2pixel[iCand]*event.tracks_nValidPixelHits[iCand] + event.tracks_deDxHarmonic2strips[iCand]*event.tracks_nValidTrackerHits[iCand])/(event.tracks_nValidPixelHits[iCand] + event.tracks_nValidTrackerHits[iCand]),
                                     "tracks_massfromdeDxPixel": tracks_massfromdeDxPixel,
                                     "tracks_massfromdeDxStrips": tracks_massfromdeDxStrips,
                                     "tracks_massfromdeDxWeightedByValidHits": tracks_massfromdeDxWeightedByValidHits,
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

            if debug:
                for line in sorted(track_level_output[-1].keys()):
                    print "%s: %s" %(line, track_level_output[-1][line])

        # evaluate fake rate for each event:
        if not only_fakerate and fakerate_file:

            ## check signal/control region bin:
            #
            # TODO: must be specific for each track tag
            #
            #if n_DT > 0:
            #    is_pixel_track = track_level_output[0]["tracks_is_pixel_track"]
            #    region = get_signal_region(event, MinDeltaPhiMhtJets, n_DT, is_pixel_track)
            #    tree_branch_values["region"][0] = region
            #elif n_DT == 0:
            #    region_noDT = get_signal_region(event, MinDeltaPhiMhtJets, 1, False)
            #    if region_noDT > 0:
            #        region_noDT_output.append(region_noDT)
            #        region_noDT_output.append(region_noDT + 15)
            #    region_noDT_multiple = get_signal_region(event, MinDeltaPhiMhtJets, 2, False)
            #    if region_noDT_multiple > 0:
            #        region_noDT_output.append(region_noDT_multiple)

            # fill all fakerate branches:
            for variable in fakerate_variables:
                for fr_region in fakerate_regions:
                    if "dilepton" in fr_region:
                        variable = variable.replace("HT", "HT_cleaned")
                    else:
                        variable = variable.replace("_cleaned", "")
                    
                    #FIXME: no interpolation available for dilepton FRR
                    #if fr_region == "dilepton" and "interpolated" in variable:
                    #    continue
                    
                    #hist_name = fr_region + "/" + data_period + "/fakerate_" + variable.replace(":", "_")
                    hist_name = fr_region + "/Summer16/fakerate_" + variable.replace(":", "_")
                                        
                    if ":" in variable:
                        xvalue = eval("event.%s" % variable.replace("_interpolated", "").replace("n_allvertices", "nAllVertices").replace("_cleaned", "").replace("n_NVtx", "NVtx").split(":")[1])
                        yvalue = eval("event.%s" % variable.replace("_interpolated", "").replace("n_allvertices", "nAllVertices").replace("_cleaned", "").replace("n_NVtx", "NVtx").split(":")[0])
                                                
                        FR = getBinContent_with_overflow(h_fakerates[hist_name], xvalue, yval = yvalue)
                    else:
                        value = eval("event.%s" % variable.replace("n_allvertices", "nAllVertices").replace("_cleaned", "").replace("n_NVtx", "NVtx"))
                        FR = getBinContent_with_overflow(h_fakerates[hist_name], value)
                    
                    branch_name = "fakerate_%s_%s" % (fr_region, variable.replace(":", "_"))
                    tree_branch_values[branch_name][0] = FR

        # check if genLeptons are present in event:
        if not only_fakerate and not is_data:

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
        meta_CR = False
        if event.BTags >= 1 and event.MHT>100 and event.MHT<300:
            # check for well-reconstructed electron:
            if (len(event.Electrons)>0 and (event.Electrons[0].Pt() > 30) and bool(event.Electrons_mediumID[0]) and bool(event.Electrons_passIso[0])) or \
               (len(event.Muons)>0 and (event.Muons[0].Pt() > 30) and bool(event.Muons_tightID[0]) and bool(event.Muons_passIso[0])):
               meta_CR = True
               tree_branch_values["meta_CR"][0] = meta_CR

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
     
        # count number of DTs:    
        for dt_tag_label in disappearing_track_tags:
            
            n_DT = 0
            n_DT_actualfake = 0
            for i_track_level_output in track_level_output:
                if i_track_level_output["tracks_tagged_%s" % dt_tag_label] == 1:
                    n_DT += 1
                if i_track_level_output["tracks_tagged_%s" % dt_tag_label] == 1 and i_track_level_output["tracks_actualfake"] == 1:
                    n_DT_actualfake += 1

            tree_branch_values["n_DT_%s" % dt_tag_label][0] = n_DT
            tree_branch_values["n_DT_actualfake_%s" % dt_tag_label][0] = n_DT_actualfake
     
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

        tout.Fill()
     
    fout.cd()

    if not only_fakerate and fakerate_file:
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
    parser.add_option("--input", dest="inputfiles")
    parser.add_option("--output", dest="outputfiles")
    parser.add_option("--only_fakerate", dest="only_fakerate", action="store_true", default=False)
    parser.add_option("--mask", dest="maskfile", default=False)
    parser.add_option("--nev", dest="nev", default=-1)
    parser.add_option("--fakerate_file", dest="fakerate_file", default=False)
    parser.add_option("--iEv_start", dest="iEv_start", default=0)
    (options, args) = parser.parse_args()
    
    options.inputfiles = options.inputfiles.split(",")
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
    
    main(options.inputfiles,
         options.outputfiles,
         nevents = options.nev,
         only_fakerate = options.only_fakerate,
         mask_file = options.maskfile,
         iEv_start = options.iEv_start,
         fakerate_file = options.fakerate_file)
