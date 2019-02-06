#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import tmva_tools
import os
import numpy as np
import collections

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

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

def isBaselineTrack(track, itrack, c, hMask):
	if not abs(track.Eta())< 2.4 : return False
	if not (abs(track.Eta()) < 1.4442 or abs(track.Eta()) > 1.566): return False
	if not bool(c.tracks_trackQualityHighPurity[itrack]) : return False
	if not (c.tracks_ptError[itrack]/(track.Pt()*track.Pt()) < 10): return False
	if not abs(c.tracks_dxyVtx[itrack]) < 0.1: return False
	if not abs(c.tracks_dzVtx[itrack]) < 0.1 : return False
	if not c.tracks_trkRelIso[itrack] < 0.2: return False
	if not (c.tracks_trackerLayersWithMeasurement[itrack] >= 2 and c.tracks_nValidTrackerHits[itrack] >= 2): return False
	if not c.tracks_nMissingInnerHits[itrack]==0: return False
	if not c.tracks_nMissingMiddleHits[itrack]==0: return False	
	if hMask!='':
		xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
		ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
		if hMask.GetBinContent(ibinx, ibiny)==0: return False
	return True

def loop(event_tree_filenames, track_tree_output, nevents = -1, treename = "TreeMaker2/PreSelection", maskfile = "Masks.root", region_fakerate = False, region_SRCR = True, verbose = True):

    if region_SRCR:
        print "\nConfigured for inclusive SR / CR!\n"
    if region_fakerate:
        print "\nConfigured for fake rate estimation region!\n"

    tree = TChain(treename)
    for iFile in event_tree_filenames:
        tree.Add(iFile)
    
    fout = TFile(track_tree_output, "recreate")

    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()
    xsec_written = False

    # prepare histograms:
    if region_SRCR:
        histos = collections.OrderedDict()
        for lepton_region in ["", "zeroleptons_", "onelepton_"]:
            histos["h_" + lepton_region + "region"]                    = TH1F("h_" + lepton_region + "region", "h_" + lepton_region + "region", 40, 0, 40)
            histos["h_" + lepton_region + "region_prompt"]             = TH1F("h_" + lepton_region + "region_prompt", "h_" + lepton_region + "region_prompt", 40, 0, 40)
            histos["h_" + lepton_region + "region_actualfakes"]        = TH1F("h_" + lepton_region + "region_actualfakes", "h_" + lepton_region + "region_actualfakes", 40, 0, 40)
            histos["h_" + lepton_region + "region_xFR_dilepton"]       = TH1F("h_" + lepton_region + "region_xFR_dilepton", "h_" + lepton_region + "region_xFR_dilepton", 40, 0, 40)
            histos["h_" + lepton_region + "region_xFR_qcd"]            = TH1F("h_" + lepton_region + "region_xFR_qcd", "h_" + lepton_region + "region_xFR_qcd", 40, 0, 40)
            histos["h_" + lepton_region + "region_noDT"]               = TH1F("h_" + lepton_region + "region_noDT", "h_" + lepton_region + "region_noDT", 40, 0, 40)
            histos["h_" + lepton_region + "region_noDT_xFR_dilepton"]  = TH1F("h_" + lepton_region + "region_noDT_xFR_dilepton", "h_" + lepton_region + "region_noDT_xFR_dilepton", 40, 0, 40)
            histos["h_" + lepton_region + "region_noDT_xFR_qcd"]       = TH1F("h_" + lepton_region + "region_noDT_xFR_qcd", "h_" + lepton_region + "region_noDT_xFR_qcd", 40, 0, 40)

    tout = TTree("Events", "tout")
 
    # get variables of tree
    variables = []
    for i in range(len(tree.GetListOfBranches())):
        label = tree.GetListOfBranches()[i].GetName()
        if "tracks_" in label:
            label = label.replace("tracks_", "")
            variables.append(label)

    # prepare variables for output tree
   
    float_branches = []
    float_branches.append("MET")
    float_branches.append("MHT")
    float_branches.append("HT")
    float_branches.append("MinDeltaPhiMhtJets")
    float_branches.append("PFCaloMETRatio")
    float_branches.append("weight")
    if region_fakerate:
        float_branches.append("dilepton_invmass")
        float_branches.append("MHT_cleaned")
        float_branches.append("HT_cleaned")
        float_branches.append("MinDeltaPhiMhtJets_cleaned")
    if region_SRCR: 
        float_branches.append("region")
        float_branches.append("region_prompt")
        float_branches.append("region_actualfakes")
        float_branches.append("region_xFR_dilepton")
        float_branches.append("region_xFR_qcd")
        float_branches.append("region_noDT")
        float_branches.append("region_noDT_xFR_dilepton")
        float_branches.append("region_noDT_xFR_qcd")

    integer_branches = []
    integer_branches.append("n_DT")
    integer_branches.append("n_DT_actualfake")
    integer_branches.append("n_jets")
    integer_branches.append("n_btags")
    integer_branches.append("n_leptons")
    integer_branches.append("n_allvertices")
    integer_branches.append("n_NVtx")
    integer_branches.append("EvtNumEven")
    integer_branches.append("DT1_is_pixel_track")
    integer_branches.append("DT2_is_pixel_track")
    integer_branches.append("DT3_is_pixel_track")
    integer_branches.append("DT1_trackerLayersWithMeasurement")
    integer_branches.append("DT2_trackerLayersWithMeasurement")
    integer_branches.append("DT3_trackerLayersWithMeasurement")
    integer_branches.append("DT1_actualfake")
    integer_branches.append("DT2_actualfake")
    integer_branches.append("DT3_actualfake")
    if region_fakerate:
        integer_branches.append("n_jets_cleaned")
        integer_branches.append("n_btags_cleaned")
        integer_branches.append("dilepton_CR")
        integer_branches.append("qcd_CR")
        integer_branches.append("lepton_type")

    tree_branch_values = {}
    for variable in float_branches:
        tree_branch_values[variable] = array( 'f', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/F' % variable )
    for variable in integer_branches:
        tree_branch_values[variable] = array( 'i', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/I' % variable )
        
    # BDT configuration:
    readerPixelOnly = 0
    readerPixelStrips = 0
    preselection_pixelonly = ""
    preselection_pixelstrips = ""

    tmva_variables = {}
    bdt_folders = ["../../disappearing-track-tag/short-tracks", "../../disappearing-track-tag/long-tracks"]

    for i_category, category in enumerate(["pixelonly", "pixelstrips"]):

        bdt_infos = tmva_tools.get_tmva_info(bdt_folders[i_category])

        if category == "pixelonly":
            readerPixelOnly = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelonly = bdt_infos["preselection"]
            bdt_cut_pixelonly = 0.1
        elif category == "pixelstrips":
            readerPixelStrips = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelstrips = bdt_infos["preselection"]
            bdt_cut_pixelstrips = 0.25

    # check if data:
    if "Run201" in event_tree_filenames[0]:
        is_data = True
        data_period = event_tree_filenames[0].split("Run")[-1][:5]
        print "data_period", data_period
    else:
        is_data = False
        data_period = False

    # load data mask file:
    mask = ""
    if maskfile:
        mask_file = TFile(maskfile, "open")
        if "Run2016" in event_tree_filenames[0]:
            mask = mask_file.Get("hEtaVsPhiDT_maskedData-2016Data-2016")

    if region_SRCR:
        # load fakerate maps:
        fakerate_file = TFile("fakerate.root", "open")
        h_fakerate_dilepton_bg = fakerate_file.Get("dilepton/dilepton_fake_rate_bg")
        h_fakerate_dilepton_bg_short = fakerate_file.Get("dilepton/dilepton_fake_rate_bg_short")
        h_fakerate_dilepton_bg_long = fakerate_file.Get("dilepton/dilepton_fake_rate_bg_long")
        h_fakerate_dilepton_data = fakerate_file.Get("dilepton/dilepton_fake_rate_%s" % data_period)
        h_fakerate_dilepton_data_short = fakerate_file.Get("dilepton/dilepton_fake_rate_%s_short" % data_period)
        h_fakerate_dilepton_data_long = fakerate_file.Get("dilepton/dilepton_fake_rate_%s_long" % data_period)
        
        # use 2016C map for all qcd
        if data_period == "2016D":
            data_period = "2016C"
        
        h_fakerate_qcd_bg = fakerate_file.Get("qcd/qcd_fake_rate_bg")
        h_fakerate_qcd_bg_short = fakerate_file.Get("qcd/qcd_fake_rate_bg_short")
        h_fakerate_qcd_bg_long = fakerate_file.Get("qcd/qcd_fake_rate_bg_long")
        h_fakerate_qcd_data = fakerate_file.Get("qcd/qcd_fake_rate_%s" % data_period)
        h_fakerate_qcd_data_short = fakerate_file.Get("qcd/qcd_fake_rate_%s_short" % data_period)
        h_fakerate_qcd_data_long = fakerate_file.Get("qcd/qcd_fake_rate_%s_long" % data_period)

    # some loop variables:
    nevents_total = 0
    nevents_tagged = 0
    nevents_tagged_actualfake = 0

    weight = 1
    h_xsec = TH1F("xsec", "xsec", 1, 0, 1)

    # loop over events
    for iEv, event in enumerate(tree):

        if not xsec_written and not is_data:
            if tree.GetBranch("CrossSection"):
                xsec = event.CrossSection
            else:
                xsec = -1
            h_xsec.Fill(0, xsec)
            weight = xsec/nev
            xsec_written = True

        if nevents > 0 and iEv > nevents:
            break
        
        if (iEv+1) % 500 == 0:
            print "Processing event %s / %s" % (iEv + 1, nev)

        if region_SRCR:
            # speed things up (low MHT without jets don't fall into any signal region):
            if event.MHT<250 or len(event.Jets) == 0: continue

        # do HT-binned background stitching:
        current_file_name = tree.GetFile().GetName()
        if tree.GetBranch("madHT"):
            madHT = event.madHT
            if (madHT>0) and \
               ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
               ("TTJets_Tune" in current_file_name and madHT>600) or \
               ("100to200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("100To200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("200to300_" in current_file_name and (madHT<200 or madHT>300)) or \
               ("200To300_" in current_file_name and (madHT<200 or madHT>300)) or \
               ("200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("300to500_" in current_file_name and (madHT<300 or madHT>500)) or \
               ("300To500_" in current_file_name and (madHT<300 or madHT>500)) or \
               ("400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("500to700_" in current_file_name and (madHT<500 or madHT>700)) or \
               ("500To700_" in current_file_name and (madHT<500 or madHT>700)) or \
               ("600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("700to1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
               ("700To1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
               ("800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("1000to1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
               ("1000To1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
               ("1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("1500to2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
               ("1500To2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
               ("2500toInf_" in current_file_name and madHT<2500) or \
               ("2500ToInf_" in current_file_name and madHT<2500):
                continue
                  
        # reset all branch values:
        for label in tree_branch_values:
            tree_branch_values[label][0] = -1

        if region_fakerate:

            # to get the fake rate, consider dilepton region or QCD-only events. Check which applies for this event

            # set selection flags (veto event later if it does not fit into any selection):
            dilepton_CR = False
            qcd_CR = False

            if "Run" not in current_file_name or "SingleElectron" in current_file_name or "SingleMuon" in current_file_name:
                min_lepton_pt = 30.0
                invariant_mass = 0
                if (len(event.Electrons) == 2 and len(event.Muons) == 0):
                    if (event.Electrons[0].Pt() > min_lepton_pt):
                        if bool(event.Electrons_mediumID[0]) and bool(event.Electrons_mediumID[1]):
                            if (event.Electrons_charge[0] * event.Electrons_charge[1] < 0):
                                invariant_mass = (event.Electrons[0] + event.Electrons[1]).M()
                                if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                                    if bool(event.Electrons_passIso[0]) and bool(event.Electrons_passIso[1]):
                                        tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                        tree_branch_values["lepton_type"][0] = 11
                                        tree_branch_values["dilepton_CR"][0] = 1
                                        dilepton_CR = True       
                elif (len(event.Muons) == 2 and len(event.Electrons) == 0):
                    if (event.Muons[0].Pt() > min_lepton_pt):
                        if (bool(event.Muons_tightID[0]) and bool(event.Muons_tightID[1])):
                            if (event.Muons_charge[0] * event.Muons_charge[1] < 0):
                                invariant_mass = (event.Muons[0] + event.Muons[1]).M()            
                                if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                                    if bool(event.Muons_passIso[0]) and bool(event.Muons_passIso[1]):
                                        tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                        tree_branch_values["lepton_type"][0] = 13
                                        tree_branch_values["dilepton_CR"][0] = 1
                                        dilepton_CR = True

            # check if low-MHT, QCD-only samples:
            if ("QCD" in current_file_name or "JetHT" in current_file_name) and event.MHT < 200:
                tree_branch_values["qcd_CR"][0] = 1
                qcd_CR = True

            # CHECK: event selection
            if not dilepton_CR and not qcd_CR: continue
                
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
     
        # loop over tracks (tracks):
        nevents_total += 1
        n_DT = 0
        n_DT_actualfake = 0

        for iCand in xrange(len(event.tracks)):

            # set up booleans
            charged_genparticle_in_track_cone = False
            is_disappearing_track = False
            is_a_PF_lepton = False

            # re-check PF lepton veto:
            for k in range(len(event.Muons)):
                deltaR = event.tracks[iCand].DeltaR(event.Muons[k])
                if deltaR < 0.01:
                    is_a_PF_lepton = True
            for k in range(len(event.Electrons)):
                deltaR = event.tracks[iCand].DeltaR(event.Electrons[k])
                if deltaR < 0.01:
                    is_a_PF_lepton = True

            if is_a_PF_lepton: continue

            # fill custom variables:
            ptErrOverPt2 = event.tracks_ptError[iCand] / (event.tracks[iCand].Pt()**2)

            # check for category:
            is_pixel_track = False
            is_tracker_track = False
            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            elif event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_tracker_track = True
                            
            # apply TMVA preselection:
            if is_pixel_track and not (event.tracks[iCand].Pt() > 30 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
                    continue

            if is_tracker_track and not (event.tracks[iCand].Pt() > 30 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingOuterHits[iCand] >= 2 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
                    continue

            # evaluate BDT:
            if is_pixel_track:
                tmva_variables["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
                tmva_variables["dzVtx"][0] = event.tracks_dzVtx[iCand]
                tmva_variables["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
                tmva_variables["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
                tmva_variables["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
                tmva_variables["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
                tmva_variables["ptErrOverPt2"][0] = ptErrOverPt2

                mva = readerPixelOnly.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelonly:
                    is_disappearing_track = True

            elif is_tracker_track:
                tmva_variables["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
                tmva_variables["dzVtx"][0] = event.tracks_dzVtx[iCand]
                tmva_variables["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
                tmva_variables["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
                tmva_variables["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
                tmva_variables["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
                tmva_variables["nMissingOuterHits"][0] = event.tracks_nMissingOuterHits[iCand]
                tmva_variables["ptErrOverPt2"][0] = ptErrOverPt2

                mva = readerPixelStrips.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelstrips:
                    is_disappearing_track = True

            # apply baseline DT selection:
            if is_disappearing_track and not isBaselineTrack(event.tracks[iCand], iCand, event, mask):
                print "Failed baseline DT selection"
                is_disappearing_track = False

            # check if actual fake track (no genparticle in cone around track):
            charged_genparticle_in_track_cone = False
            if is_disappearing_track and tree.GetBranch("GenParticles"):
                for k in range(len(event.GenParticles)):

                    deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                    if deltaR < 0.02 and event.GenParticles_Status[k] != 1:
                           
                        gen_track_cone_pdgid = abs(event.GenParticles_PdgId[k])
                        if gen_track_cone_pdgid == 11 or gen_track_cone_pdgid == 13:
                            charged_genparticle_in_track_cone = True
                            break
                        elif gen_track_cone_pdgid == 15 and tree.GetBranch("GenTaus_LeadTrk"):
                            # if genTau, check if the track matches with a GenTaus_LeadTrk track:
                            for l in range(len(event.GenTaus_LeadTrk)):
                                deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.01:
                                    print "That's a tau leading track"
                                    charged_genparticle_in_track_cone = True
                                    break
                
            if is_disappearing_track:
               
                n_DT += 1
                if not charged_genparticle_in_track_cone:
                    n_DT_actualfake += 1

                # save track-level properties:
                tree_branch_values["DT%s_is_pixel_track" % n_DT][0] = is_pixel_track
                tree_branch_values["DT%s_trackerLayersWithMeasurement" % n_DT][0] = event.tracks_trackerLayersWithMeasurement[iCand]
                tree_branch_values["DT%s_actualfake" % n_DT][0] = not charged_genparticle_in_track_cone

                if verbose:
                    print "**************** DT track info ****************"
                    print "file name =", current_file_name
                    print "event number =", iEv
                    print "mva =", mva
                    print "is_pixel_track =", is_pixel_track
                    print "is_tracker_track =", is_tracker_track
                    print "pt =", event.tracks[iCand].Pt()
                    print "eta =", abs(event.tracks[iCand].Eta())
                    print "nMissingInnerHits =", event.tracks_nMissingInnerHits[iCand]
                    print "nMissingMiddleHits =", event.tracks_nMissingMiddleHits[iCand]
                    print "trackQualityHighPurity =", bool(event.tracks_trackQualityHighPurity[iCand])
                    print "dxyVtx =", event.tracks_dxyVtx[iCand]
                    print "dzVtx =", event.tracks_dzVtx[iCand]
                    print "matchedCaloEnergy =", event.tracks_matchedCaloEnergy[iCand]
                    print "trkRelIso =", event.tracks_trkRelIso[iCand]
                    print "nValidPixelHits =", event.tracks_nValidPixelHits[iCand]
                    print "nValidTrackerHits =", event.tracks_nValidTrackerHits[iCand]
                    print "nMissingOuterHits =", event.tracks_nMissingOuterHits[iCand]
                    print "ptErrOverPt2 =", ptErrOverPt2
                    print "charged_genparticle_in_track_cone", charged_genparticle_in_track_cone
                    print "***********************************************"

        if region_SRCR:

            # before filling tree, check if event in signal or control region:
            if n_DT > 0:
                #FIXME: event with two DTs 
                is_pixel_track = tree_branch_values["DT1_is_pixel_track"][0]
                region = get_signal_region(event, MinDeltaPhiMhtJets, n_DT, is_pixel_track)
            else:
                region = 0

            if n_DT == 0:
                region_noDT = get_signal_region(event, MinDeltaPhiMhtJets, 1, False)
            else:
                region_noDT = 0

            # fill tree only for control regions:
            if region_noDT > 0 or region > 0:

                # get bin content from 2D histogram with overflows:
                def getBinContent_with_overflow(histo, xval, yval):
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

                # get fake rate from maps:
                fakerate_dilepton_short = False
                fakerate_qcd_short = False
                fakerate_dilepton_long = False
                fakerate_qcd_long = False
                
                if is_data:
                    fakerate_dilepton_short = getBinContent_with_overflow(h_fakerate_dilepton_data_short, event.nAllVertices, event.HT)
                    fakerate_qcd_short = getBinContent_with_overflow(h_fakerate_qcd_data_short, event.nAllVertices, event.HT)
                    fakerate_dilepton_long = getBinContent_with_overflow(h_fakerate_dilepton_data_long, event.nAllVertices, event.HT)
                    fakerate_qcd_long = getBinContent_with_overflow(h_fakerate_qcd_data_long, event.nAllVertices, event.HT)
                else:
                    fakerate_dilepton_short = getBinContent_with_overflow(h_fakerate_dilepton_bg_short, event.nAllVertices, event.HT)
                    fakerate_qcd_short = getBinContent_with_overflow(h_fakerate_qcd_bg_short, event.nAllVertices, event.HT)                    
                    fakerate_dilepton_long = getBinContent_with_overflow(h_fakerate_dilepton_bg_long, event.nAllVertices, event.HT)
                    fakerate_qcd_long = getBinContent_with_overflow(h_fakerate_qcd_bg_long, event.nAllVertices, event.HT)

                # fill histograms:
                for lepton_region in ["", "zeroleptons_", "onelepton_"]:
                    n_leptons = len(event.Electrons) + len(event.Muons)
                    if lepton_region == "zeroleptons_" and n_leptons != 0: continue
                    if lepton_region == "onelepton_" and n_leptons != 1: continue

                    if n_DT > 0:
                        histos["h_" + lepton_region + "region"].Fill(region, weight)
                        
                        # regions up to 30 are with one DT:
                        if region <= 15:
                            histos["h_" + lepton_region + "region_xFR_dilepton"].Fill(region, fakerate_dilepton_short * weight)
                            histos["h_" + lepton_region + "region_xFR_qcd"].Fill(region, fakerate_qcd_short * weight)
                        elif region >= 16 and region <= 30:
                            histos["h_" + lepton_region + "region_xFR_dilepton"].Fill(region, fakerate_dilepton_long * weight)
                            histos["h_" + lepton_region + "region_xFR_qcd"].Fill(region, fakerate_qcd_long * weight)
                        elif region >= 31:
                            # events with two DTs:
                            if tree_branch_values["DT1_is_pixel_track" % n_DT][0] == 1 and tree_branch_values["DT2_is_pixel_track" % n_DT][0] == 1:
                                # both are short
                                histos["h_" + lepton_region + "region_xFR_dilepton"].Fill(region, fakerate_dilepton_short**2 * weight)
                                histos["h_" + lepton_region + "region_xFR_qcd"].Fill(region, fakerate_qcd_short**2 * weight)
                            elif tree_branch_values["DT1_is_pixel_track" % n_DT][0] == 0 and tree_branch_values["DT2_is_pixel_track" % n_DT][0] == 0:
                                # both are long
                                histos["h_" + lepton_region + "region_xFR_dilepton"].Fill(region, fakerate_dilepton_long**2 * weight)
                                histos["h_" + lepton_region + "region_xFR_qcd"].Fill(region, fakerate_qcd_long**2 * weight)
                            else:
                                # one is short, other is long
                                histos["h_" + lepton_region + "region_xFR_dilepton"].Fill(region, fakerate_dilepton_short * fakerate_dilepton_long * weight)
                                histos["h_" + lepton_region + "region_xFR_qcd"].Fill(region, fakerate_qcd_short * fakerate_qcd_long * weight)
                        if n_DT == n_DT_actualfake: 
                            histos["h_" + lepton_region + "region_actualfakes"].Fill(region, weight)
                        else:
                            histos["h_" + lepton_region + "region_prompt"].Fill(region, weight)

                    else:
                        # fill first region bins for long tracks:
                        histos["h_" + lepton_region + "region_noDT"].Fill(region_noDT, weight)
                        histos["h_" + lepton_region + "region_noDT_xFR_dilepton"].Fill(region_noDT, fakerate_dilepton_long * weight)
                        histos["h_" + lepton_region + "region_noDT_xFR_qcd"].Fill(region_noDT, fakerate_qcd_long * weight)

                        # also fill region bins for short tracks:
                        histos["h_" + lepton_region + "region_noDT"].Fill(region_noDT + 15, weight)
                        histos["h_" + lepton_region + "region_noDT_xFR_dilepton"].Fill(region_noDT + 15, fakerate_dilepton_short * weight)
                        histos["h_" + lepton_region + "region_noDT_xFR_qcd"].Fill(region_noDT + 15, fakerate_qcd_short * weight)

                        # fill last two region bins:
                        # FIXME: assume one short and one long DT for events with 2 DTs. This is likely to change
                        if event.MHT >= 250 and event.MHT < 400 and len(event.Jets) > 0:
                            histos["h_" + lepton_region + "region_noDT"].Fill(31, weight)
                            histos["h_" + lepton_region + "region_noDT_xFR_dilepton"].Fill(31, fakerate_dilepton_short * fakerate_dilepton_long * weight)
                            histos["h_" + lepton_region + "region_noDT_xFR_qcd"].Fill(31, fakerate_qcd_short * fakerate_qcd_long * weight)
                        elif event.MHT >= 400 and len(event.Jets) > 0:
                            histos["h_" + lepton_region + "region_noDT"].Fill(32, weight)
                            histos["h_" + lepton_region + "region_noDT_xFR_dilepton"].Fill(31, fakerate_dilepton_short * fakerate_dilepton_long * weight)
                            histos["h_" + lepton_region + "region_noDT_xFR_qcd"].Fill(31, fakerate_qcd_short * fakerate_qcd_long * weight)

            tree_branch_values["region"][0] = region
            tree_branch_values["region_noDT"][0] = region_noDT

        # event-level variables:
        tree_branch_values["n_leptons"][0] = len(event.Electrons) + len(event.Muons)
        tree_branch_values["n_btags"][0] = event.BTags
        tree_branch_values["n_DT"][0] = n_DT
        tree_branch_values["n_DT_actualfake"][0] = n_DT_actualfake
        tree_branch_values["n_jets"][0] = len(event.Jets)
        tree_branch_values["n_allvertices"][0] = event.nAllVertices
        tree_branch_values["PFCaloMETRatio"][0] = event.PFCaloMETRatio
        tree_branch_values["MET"][0] = event.MET
        tree_branch_values["MHT"][0] = event.MHT
        tree_branch_values["HT"][0] = event.HT
        tree_branch_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets
        tree_branch_values["n_NVtx"][0] = event.NVtx
        tree_branch_values["weight"][0] = weight
               
        if event.EvtNum % 2 == 0:
            tree_branch_values["EvtNumEven"][0] = 1
        else:
            tree_branch_values["EvtNumEven"][0] = 0
     
        tout.Fill()
     
    fout.cd()
    fout.Write()
    h_xsec.Write()

    if region_SRCR:
        for label in histos:
            histos[label].Write()
        fakerate_file.Close()
    if mask != "":
        mask_file.Close()
        
    fout.Close()

if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    iFile = args[0].split(",")
    out_tree = args[1]
    nev = int(args[2])
    region = int(args[3])

    if nev == 0:
        nev = -1

    region_fakerate = False
    region_SRCR = False
    if region == 0:
        region_fakerate = True
    elif region == 1:
        region_SRCR = True

    loop(iFile, out_tree, nevents = nev, region_fakerate = region_fakerate, region_SRCR = region_SRCR)
