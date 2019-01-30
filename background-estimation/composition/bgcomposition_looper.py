#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import tmva_tools
import os

# loop over all events and save events with n_DT>0 with added information about genparticles in cone around the DT track

def loop(event_tree_filenames, track_tree_output, bdt_folders, nevents = -1, treename = "TreeMaker2/PreSelection", maskfile = "Masks.root"):

    tree = TChain(treename)
    for iFile in event_tree_filenames:
        tree.Add(iFile)
    
    fout = TFile(track_tree_output, "recreate")

    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()

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
                      "CrossSection",
                      "taggedtrack1_pt",
                      "taggedtrack2_pt",
                      "taggedtrack3_pt",
                      "taggedtrack1_eta",
                      "taggedtrack2_eta",
                      "taggedtrack3_eta",
                      "taggedtrack1_phi",
                      "taggedtrack2_phi",
                      "taggedtrack3_phi",
                      "taggedtrack1_mask",
                      "taggedtrack2_mask",
                      "taggedtrack3_mask",
                      "taggedtrack1_gamma_DR",
                      "taggedtrack2_gamma_DR",
                      "taggedtrack3_gamma_DR",
                      "taggedtrack1_gamma_ptfraction",
                      "taggedtrack2_gamma_ptfraction",
                      "taggedtrack3_gamma_ptfraction",
                    ]:
        tree_branch_values[variable] = array( 'f', [ -1000 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/F' % variable )

    for variable in [
                      "n_DT",
                      "n_DT_realfake",
                      "n_jets",
                      "n_btags",
                      "n_leptons",
                      "n_allvertices",
                      "n_NVtx",
                      "n_sum_gen_particles_in_cone",
                      "n_sum_leading_tracks_in_cone",
                      "EvtNumEven",
                      "taggedtrack1_tagid",
                      "taggedtrack2_tagid",
                      "taggedtrack3_tagid",
                      "taggedtrack1_bgtype",
                      "taggedtrack2_bgtype",
                      "taggedtrack3_bgtype",
                      "taggedtrack1_mother",
                      "taggedtrack2_mother",
                      "taggedtrack3_mother",
                    ]:
        tree_branch_values[variable] = array( 'i', [ -1000 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/I' % variable )
        
    # BDT configuration:
    readerPixelOnly = 0
    readerPixelStrips = 0
    tmva_variables = {}

    for i_category, category in enumerate(["pixelonly", "pixelstrips"]):

        #bdt_bestcut = tmva_tools.get_get_bdt_cut_value(bdt_folders[i_category] + '/output.root')["best_cut_value"]
        bdt_infos = tmva_tools.get_tmva_info(bdt_folders[i_category])

        if category == "pixelonly":
            readerPixelOnly = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelonly = bdt_infos["preselection"]
            bdt_cut_pixelonly = 0.1
        elif category == "pixelstrips":
            readerPixelStrips = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelstrips = bdt_infos["preselection"]
            bdt_cut_pixelstrips = 0.25
    
    # some loop variables:
    nevents_total = 0

    # loop over events
    # ****************
    for iEv, event in enumerate(tree):

        if nevents > 0 and iEv > nevents:
            break
        
        if (iEv+1) % 500 == 0:
            print "Processing event %s / %s" % (iEv + 1, nev)

        # HT-binned background stitching:
        current_file_name = tree.GetFile().GetName()
        if tree.GetBranch("madHT"):
            madHT = event.madHT
            if "Run201" not in current_file_name:
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
                
        if maskfile:
            mask_file = TFile(maskfile, "open")
            if "Run2016" in current_file_name:
                mask = mask_file.Get("hEtaVsPhiDT_maskedData-2016Data-2016")
            elif "Summer16" in current_file_name:
                mask = mask_file.Get("hEtaVsPhiDT_maskedMC-2016MC-2016")
  
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
    
        nevents_total += 1
        n_DT = 0
        n_DT_realfake = 0
        n_sum_gen_particles_in_cone = 0
        n_sum_leading_tracks_in_cone = 0
        tagid_bdt = 0
        tagid_ptsum = 0
        tagid_ecalo = 0
    
        # for each event, reset all branch variables
        for label in tree_branch_values:
            tree_branch_values[label][0] = -1000
    
        # loop over tracks
        for i_iCand, iCand in enumerate(xrange(len(event.tracks))):

            gen_track_cone_pdgid = -1000
            n_gen_particles_in_cone = 0

            # set up booleans
            is_pixel_track = False
            is_tracker_track = False
            genparticle_in_track_cone = False
            tau_leadtrk_in_track_cone = False
            is_disappearing_track = False

            # fill custom variables:
            ptErrOverPt2 = event.tracks_ptError[iCand] / (event.tracks[iCand].Pt()**2)

            # check for category:
            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            if event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_tracker_track = True

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

                # apply TMVA preselection:
                if event.tracks[iCand].Pt() > 30 and \
                   abs(event.tracks[iCand].Eta()) < 2.4 and \
                   event.tracks_trkRelIso[iCand] < 0.2 and \
                   event.tracks_dxyVtx[iCand] < 0.1 and \
                   event.tracks_dzVtx[iCand] < 0.1 and \
                   ptErrOverPt2 < 10 and \
                   event.tracks_nMissingMiddleHits[iCand] == 0 and \
                   bool(event.tracks_trackQualityHighPurity[iCand]) == 1 and \
                   bool(event.tracks_passPFCandVeto[iCand]) == 1:
                        
                   mva = readerPixelOnly.EvaluateMVA("BDT")
                   if mva>bdt_cut_pixelonly:
                       is_disappearing_track = True
                       tagid_bdt = 1

            elif is_tracker_track:

                # apply TMVA preselection:
                if event.tracks[iCand].Pt() > 30 and \
                   abs(event.tracks[iCand].Eta()) < 2.4 and \
                   event.tracks_trkRelIso[iCand] < 0.2 and \
                   event.tracks_dxyVtx[iCand] < 0.1 and \
                   event.tracks_dzVtx[iCand] < 0.1 and \
                   ptErrOverPt2 < 10 and \
                   event.tracks_nMissingOuterHits[iCand] >= 2 and \
                   event.tracks_nMissingMiddleHits[iCand] == 0 and \
                   bool(event.tracks_trackQualityHighPurity[iCand]) == 1 and \
                   bool(event.tracks_passPFCandVeto[iCand]) == 1:
    
                   mva = readerPixelStrips.EvaluateMVA("BDT")
                   if mva>bdt_cut_pixelstrips:
                       is_disappearing_track = True
                       tagid_bdt = 2
            
            # check eta/phi mask:           
            if maskfile:
                masked = mask.GetBinContent(mask.GetXaxis().FindBin(event.tracks[iCand].Phi()), mask.GetYaxis().FindBin(event.tracks[iCand].Eta()))
            else:
                masked = -1.0
     
            # contains all pdgids for the track
            pdgids_in_cone = []

            # check if track is really a fake track (no genparticle around track):            
            if is_disappearing_track and tree.GetBranch("GenParticles"):
                for k in range(len(event.GenParticles)):
                    deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                    if deltaR < 0.01:

                        # we only need genparticles with status 1:
                        if event.GenParticles_Status[k] != 1:
                            continue

                        gen_track_cone_pdgid = event.GenParticles_PdgId[k]

                        # ignore certain non-charged genparticles (neutrinos, gluons and photons):
                        if abs(gen_track_cone_pdgid) == 12 or abs(gen_track_cone_pdgid) == 14 or abs(gen_track_cone_pdgid) == 16 or abs(gen_track_cone_pdgid) == 21 or abs(gen_track_cone_pdgid) == 22:
                            continue
                       
                        # don't use standard tau genparticles:
                        if abs(gen_track_cone_pdgid) == 15:
                            gen_track_cone_pdgid = 0

                        # use leading track taus:
                        if tree.GetBranch("GenTaus_LeadTrk"):
                            for l in range(len(event.GenTaus_LeadTrk)):
                                deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.01:
                                    print "That's a tau leading track"
                                    n_sum_leading_tracks_in_cone += 1

                                    if event.tracks_charge[iCand] > 0:
                                        gen_track_cone_pdgid = 15
                                    elif event.tracks_charge[iCand] < 0:
                                        gen_track_cone_pdgid = -15
                                    break
                                        
                        # fake track if no genparticles in cone:
                        if abs(gen_track_cone_pdgid) > 0:
                            genparticle_in_track_cone = True
                            
                        mother_pdgid = event.GenParticles_ParentId[k]
                        
                        pdgids_in_cone.append([abs(gen_track_cone_pdgid), abs(mother_pdgid)])
                        break

            # save DT track properties:                
            if is_disappearing_track:
                n_DT += 1

                # we've reserved three different branches for storing DT information per event
                if n_DT<=3:
                
                    tree_branch_values["taggedtrack%s_pt" % n_DT][0] = event.tracks[iCand].Pt()
                    tree_branch_values["taggedtrack%s_eta" % n_DT][0] = event.tracks[iCand].Eta()
                    tree_branch_values["taggedtrack%s_phi" % n_DT][0] = event.tracks[iCand].Phi()
                    tree_branch_values["taggedtrack%s_tagid" % n_DT][0] = tagid_bdt
                    tree_branch_values["taggedtrack%s_mask" % n_DT][0] = masked

                    for item in pdgids_in_cone:
                        if item[0] == 11:
                            tree_branch_values["taggedtrack%s_bgtype" % n_DT][0] = 11
                            tree_branch_values["taggedtrack%s_mother" % n_DT][0] = item[1]
                        if item[0] == 13:
                            tree_branch_values["taggedtrack%s_bgtype" % n_DT][0] = 13
                            tree_branch_values["taggedtrack%s_mother" % n_DT][0] = item[1]
                        if item[0] == 15:
                            tree_branch_values["taggedtrack%s_bgtype" % n_DT][0] = 15
                            tree_branch_values["taggedtrack%s_mother" % n_DT][0] = item[1]
                    
                    if not genparticle_in_track_cone:
                        n_DT_realfake += 1             
                        tree_branch_values["taggedtrack%s_bgtype" % n_DT][0] = 0
                        
                    # check for nearby photon (gamma conversion):
                    gamma_deltaR = 1000
                    gamma_ptfraction = 0
                    for k2 in range(len(event.GenParticles)):
                        if abs(event.GenParticles_PdgId[k2]) == 22 and event.tracks[iCand].Pt()>0:
                            deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k2])
                            if deltaR < gamma_deltaR:
                                gamma_deltaR = deltaR
                                gamma_ptfraction = event.GenParticles[k2].Pt() / event.tracks[iCand].Pt()
                    tree_branch_values["taggedtrack%s_gamma_DR" % n_DT][0] = gamma_deltaR
                    tree_branch_values["taggedtrack%s_gamma_ptfraction" % n_DT][0] = gamma_ptfraction
                    
 
        # event-level variables:
        tree_branch_values["CrossSection"][0] = event.CrossSection
        tree_branch_values["n_leptons"][0] = len(event.Electrons) + len(event.Muons)
        tree_branch_values["n_btags"][0] = event.BTags
        tree_branch_values["n_DT"][0] = n_DT
        tree_branch_values["n_DT_realfake"][0] = n_DT_realfake
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

        tree_branch_values["n_sum_gen_particles_in_cone"][0] = n_sum_gen_particles_in_cone
        tree_branch_values["n_sum_leading_tracks_in_cone"][0] = n_sum_leading_tracks_in_cone

        # write event to tree if it contains at least one DT:
        if n_DT > 0: 
            tout.Fill()
        
    fout.Write()
    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    iFile = args[0].split(",")
    out_tree = args[1]
    if len(args)>2:
        nev = int(args[2])
    else:
        nev = -1

    loop(iFile, out_tree, ["../cutoptimization/tmva/newpresel3-200-4-short", "../cutoptimization/tmva/newpresel2-200-4-medium"], nevents=nev )

