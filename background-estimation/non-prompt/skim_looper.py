#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import tmva_tools
import numpy as np

def get_signal_region(event, MinDeltaPhiMhtJets, n_DT, is_pixel_track, ignoreDT = False):
  
    NJets = len(event.Jets)
    MHT = event.MHT
    n_btags = event.BTags
    is_tracker_track = not is_pixel_track

    binnumbers = {}
    binkey =  [ 'Ht',             'Mht',                'NJets',            'BTags',            'NTags',            'NPix',             'NPixStrips',       'MinDPhiMhtJets' ]
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
           (ignoreDT or (n_DT >= binkey[4][0] and n_DT <= binkey[4][1])) and \
           (ignoreDT or (is_pixel_track >= binkey[5][0] and is_pixel_track <= binkey[5][1])) and \
           (ignoreDT or (is_tracker_track >= binkey[6][0] and is_tracker_track <= binkey[6][1])) and \
           MinDeltaPhiMhtJets >= binkey[7][0] and MinDeltaPhiMhtJets <= binkey[7][1]:
            region = binnumbers[binkey]
            break

    return region


def loop(event_tree_filenames, track_tree_output, nevents = -1, treename = "TreeMaker2/PreSelection", maskfile = "Masks.root"):

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
    h_region                    = TH1F("h_region", "h_region", 40, 0, 40)
    h_region_prompt             = TH1F("h_region_prompt", "h_region_prompt", 40, 0, 40)
    h_region_actualfakes        = TH1F("h_region_actualfakes", "h_region_actualfakes", 40, 0, 40)
    h_region_xFR_dilepton       = TH1F("h_region_xFR_dilepton", "h_region_xFR_dilepton", 40, 0, 40)
    h_region_xFR_qcd            = TH1F("h_region_xFR_qcd", "h_region_xFR_qcd", 40, 0, 40)
    h_region_noDT               = TH1F("h_region_noDT", "h_region_noDT", 40, 0, 40)
    h_region_noDT_xFR_dilepton  = TH1F("h_region_noDT_xFR_dilepton", "h_region_noDT_xFR_dilepton", 40, 0, 40)
    h_region_noDT_xFR_qcd       = TH1F("h_region_noDT_xFR_qcd", "h_region_noDT_xFR_qcd", 40, 0, 40)

    tout = TTree("Events", "tout")
 
    # get variables of tree
    variables = []
    for i in range(len(tree.GetListOfBranches())):
        label = tree.GetListOfBranches()[i].GetName()
        if "tracks_" in label:
            label = label.replace("tracks_", "")
            variables.append(label)

    # prepare variables for output tree
    tree_branch_values = {}
    for variable in [
                      "MET",
                      "MHT",
                      "HT",
                      "MinDeltaPhiMhtJets",
                      "PFCaloMETRatio",
                      "fakerate_dilepton",
                      "fakerate_qcd",
                      "region",
                      "region_prompt",
                      "region_actualfakes",
                      "region_xFR_dilepton",
                      "region_xFR_qcd",
                      "region_noDT",
                      "region_noDT_xFR_dilepton",
                      "region_noDT_xFR_qcd",

                    ]:
        tree_branch_values[variable] = array( 'f', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/F' % variable )

    for variable in [
                      "n_DT",
                      "n_DT_actualfake",
                      "n_jets",
                      "n_btags",
                      "n_leptons",
                      "n_allvertices",
                      "n_NVtx",
                      "EvtNumEven",
                    ]:
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

    # load mask file:
    if maskfile:
        mask_file = TFile(maskfile, "open")
        if "Run2016" in event_tree_filenames[0]:
            h_mask = mask_file.Get("hEtaVsPhiDT_maskedData-2016Data-2016")
        elif "Summer16" in event_tree_filenames[0]:
            h_mask = mask_file.Get("hEtaVsPhiDT_maskedMC-2016MC-2016")
        else:
            h_mask = False
    else:
        h_mask = False

    # load fakerate maps:
    fakerate_file = TFile("fakerate.root", "open")
    h_fakerate_dilepton_bg = fakerate_file.Get("dilepton/dilepton_fake_rate_bg")
    h_fakerate_dilepton_data = fakerate_file.Get("dilepton/dilepton_fake_rate_%s" % data_period)
    h_fakerate_qcd_bg = fakerate_file.Get("qcd/qcd_fake_rate_bg")
    h_fakerate_qcd_data = fakerate_file.Get("qcd/qcd_fake_rate_%s" % data_period)

    # not all JetHT data finished, revert to 2016C map if run map is empty:
    try:
        test = h_fakerate_qcd_data.GetEntries()
    except:
        h_fakerate_qcd_data = fakerate_file.Get("qcd/qcd_fake_rate_2016C")

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

        # speed things up (low MHT without jets don't fall into any signal region):
        if event.MHT<250 or len(event.Jets) == 0:
            continue

        # do HT-binned background stitching:
        current_file_name = tree.GetFile().GetName()
        if tree.GetBranch("madHT"):
            madHT = event.madHT
            if (madHT>0) and \
               ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
               ("TTJets_Tune" in current_file_name and madHT>600) or \
               ("100to200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("100To200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("2500toInf_" in current_file_name and madHT<2500) or \
               ("2500ToInf_" in current_file_name and madHT<2500):
                continue
                        
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

        # check for inclusive signal region:
        region_noDT = get_signal_region(event, MinDeltaPhiMhtJets, 0, False, ignoreDT = True)     
        if region_noDT == 0:
            continue

        # reset all branch values:
        for label in tree_branch_values:
            tree_branch_values[label][0] = -1

        # loop over tracks (tracks):
        nevents_total += 1
        n_DT = 0
        n_DT_actualfake = 0
        is_pixel_track = False

        for i_iCand, iCand in enumerate(xrange(len(event.tracks))):

            # set up booleans
            is_pixel_track = False
            is_tracker_track = False
            genparticle_in_track_cone = False
            is_disappearing_track = False
            is_a_PF_lepton = False

            # re-check PF lepton veto:
            for k in range(len(event.Muons)):
                deltaR = event.tracks[iCand].DeltaR(event.Muons[k])
                if deltaR < 0.01:
                    is_a_PF_lepton = True
                    break

            for k in range(len(event.Electrons)):
                deltaR = event.tracks[iCand].DeltaR(event.Electrons[k])
                if deltaR < 0.01:
                    is_a_PF_lepton = True
                    break

            if is_a_PF_lepton: continue

            # fill custom variables:
            ptErrOverPt2 = event.tracks_ptError[iCand] / (event.tracks[iCand].Pt()**2)

            # check for category:
            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            if event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_tracker_track = True

            # apply TMVA preselection:
            if is_pixel_track and not (event.tracks[iCand].Pt() > 15 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1 and \
                bool(event.tracks_passPFCandVeto[iCand]) == 1):
                    continue

            if is_tracker_track and not (event.tracks[iCand].Pt() > 15 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingOuterHits[iCand] >= 2 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1 and \
                bool(event.tracks_passPFCandVeto[iCand]) == 1):
                    continue

            # evalulate BDT:
            tmva_variables["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
            tmva_variables["dzVtx"][0] = event.tracks_dzVtx[iCand]
            tmva_variables["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
            tmva_variables["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
            tmva_variables["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
            tmva_variables["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
            tmva_variables["nMissingOuterHits"][0] = event.tracks_nMissingOuterHits[iCand]
            tmva_variables["ptErrOverPt2"][0] = ptErrOverPt2

            if is_pixel_track:
                mva = readerPixelOnly.EvaluateMVA("BDT")
                if mva > bdt_cut_pixelonly:
                    is_disappearing_track = True
            elif is_tracker_track:
                mva = readerPixelStrips.EvaluateMVA("BDT")
                if mva > bdt_cut_pixelstrips:
                    is_disappearing_track = True

            # check if "real" fake (no genparticle around track):            
            if is_disappearing_track and tree.GetBranch("GenParticles"):
                for k in range(len(event.GenParticles)):

                    deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                    if deltaR < 0.01:

                        # we only need genparticles with status 1:
                        if event.GenParticles_Status[k] != 1:
                            continue
                            
                        # ignore certain non-charged genparticles (neutrinos, gluons and photons):
                        gen_track_cone_pdgid = event.GenParticles_PdgId[k]
                        if abs(gen_track_cone_pdgid) == 12 or abs(gen_track_cone_pdgid) == 14 or abs(gen_track_cone_pdgid) == 16 or abs(gen_track_cone_pdgid) == 21 or abs(gen_track_cone_pdgid) == 22:
                            continue

                        # if genTau, check if the track matches with a GenTaus_LeadTrk track:
                        if abs(gen_track_cone_pdgid) == 15 and tree.GetBranch("GenTaus_LeadTrk"):
                            tau_leading_track = False
                            for l in range(len(event.GenTaus_LeadTrk)):
                                deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.01:
                                    print "That's a tau leading track"
                                    tau_leading_track = True
                                    break
                            
                            if not tau_leading_track:
                                continue
                                        
                        genparticle_in_track_cone = True
                        break
                
            if is_disappearing_track:

                # check eta/phi mask:
                if h_mask:
                    masked = h_mask.GetBinContent(h_mask.GetXaxis().FindBin(event.tracks[iCand].Phi()), h_mask.GetYaxis().FindBin(event.tracks[iCand].Eta()))
                    if masked > 0:
                        n_DT += 1
                        if not genparticle_in_track_cone and not is_data:
                            n_DT_actualfake += 1

                else:
                    n_DT += 1
                    if not genparticle_in_track_cone and not is_data:
                        n_DT_actualfake += 1
 
        # before filling tree, check if event in signal region:
        region = get_signal_region(event, MinDeltaPhiMhtJets, n_DT, is_pixel_track)

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

            # get fake rate from map:
            if is_data:
                fakerate_dilepton = getBinContent_with_overflow(h_fakerate_dilepton_data, event.nAllVertices, event.HT)
                fakerate_qcd = getBinContent_with_overflow(h_fakerate_qcd_data, event.nAllVertices, event.HT)
            else:
                fakerate_dilepton = getBinContent_with_overflow(h_fakerate_dilepton_bg, event.nAllVertices, event.HT)
                fakerate_qcd = getBinContent_with_overflow(h_fakerate_qcd_bg, event.nAllVertices, event.HT)

            # fill histograms:
            if n_DT > 0:
                h_region.Fill(region, weight)
                h_region_xFR_dilepton.Fill(region, fakerate_dilepton * weight)
                h_region_xFR_qcd.Fill(region, fakerate_qcd * weight)
                if n_DT == n_DT_actualfake: 
                    h_region_actualfakes.Fill(region, weight)
                else:
                    h_region_prompt.Fill(region, weight)
            else:
                h_region_noDT.Fill(region_noDT, weight)
                h_region_noDT_xFR_dilepton.Fill(region_noDT, fakerate_dilepton * weight)
                h_region_noDT_xFR_qcd.Fill(region_noDT, fakerate_qcd * weight)

            # fill tree branches:
            tree_branch_values["region"][0] = region
            tree_branch_values["region_noDT"][0] = region_noDT
            tree_branch_values["fakerate_dilepton"][0] = fakerate_dilepton
            tree_branch_values["fakerate_qcd"][0] = fakerate_qcd
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
            
            if event.EvtNum % 2 == 0:
                tree_branch_values["EvtNumEven"][0] = 1
            else:
                tree_branch_values["EvtNumEven"][0] = 0
            
            tout.Fill()
     
    fout.cd()
    fout.Write()

    h_xsec.Write()
    h_region.Write()
    h_region_prompt.Write()
    h_region_actualfakes.Write()
    h_region_xFR_dilepton.Write()
    h_region_xFR_qcd.Write()
    h_region_noDT.Write()
    h_region_noDT_xFR_dilepton.Write()
    h_region_noDT_xFR_qcd.Write()

    fout.Close()
    mask_file.Close()
    fakerate_file.Close()


if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    iFile = args[0].split(",")
    out_tree = args[1]
    if len(args)>2 and args[2]>0:
        nev = int(args[2])
    else:
        nev = -1

    loop(iFile, out_tree, nevents=nev)

