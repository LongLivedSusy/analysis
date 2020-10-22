#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import collections
import json
import math
import shared_utils
import xsections
import os

gROOT.SetBatch(True)
#gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def correct_dedx_intercalibration(dedx, filename, abseta):

    if 'Run20' in filename: 
    	keyforcalibs = filename.split("/")[-1].split('-')[0]
    	dedxcalib_barrel = shared_utils.DedxCorr_Pixel_barrel[keyforcalibs]
    	dedxcalib_endcap = shared_utils.DedxCorr_Pixel_endcap[keyforcalibs]
    elif 'Summer16FastSim' in filename:
    	dedxcalib_barrel = shared_utils.DedxCorr_Pixel_barrel['Summer16FastSim']
    	dedxcalib_endcap = shared_utils.DedxCorr_Pixel_endcap['Summer16FastSim']
    elif 'Summer16' in filename: 
    	dedxcalib_barrel = shared_utils.DedxCorr_Pixel_barrel['Summer16']
    	dedxcalib_endcap = shared_utils.DedxCorr_Pixel_endcap['Summer16']
    elif 'Fall17' in filename: 
    	dedxcalib_barrel = shared_utils.DedxCorr_Pixel_barrel['Fall17']
    	dedxcalib_endcap = shared_utils.DedxCorr_Pixel_endcap['Fall17']
    else: 
    	dedxcalib_barrel = 1.0
    	dedxcalib_endcap = 1.0	    

    if abseta < 1.5:
        return dedxcalib_barrel * dedx
    else:
        return dedxcalib_endcap * dedx
    

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
    

def get_signal_region(HT, MHT, NJets, n_btags, MinDeltaPhiMhtJets, n_DT, is_pixel_track, DeDxAverage, n_goodelectrons, n_goodmuons, filename, sideband = False):
  
    is_tracker_track = not is_pixel_track
    dedxcutLow = shared_utils.dedxcutLow
    dedxcutMid = shared_utils.dedxcutMid
    binnumbers = shared_utils.binnumbers

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
           ( (not sideband and DeDxAverage >= binkey[8][0] and DeDxAverage <= binkey[8][1]) or (sideband and DeDxAverage < dedxcutLow) ) and \
           n_goodelectrons >= binkey[9][0] and n_goodelectrons <= binkey[9][1] and \
           n_goodmuons >= binkey[10][0] and n_goodmuons <= binkey[10][1]:
              region = binnumbers[binkey]
              break
    
    if "Run201" in filename:
        # running on data, need to check datastream:
        if "MET" in filename and (n_goodelectrons + n_goodmuons) != 0:
            return 0
        elif "SingleMuon" in filename and (n_goodmuons==0 or n_goodelectrons>0):
            return 0
        elif "SingleElectron" in filename and (n_goodmuons>0 or n_goodelectrons==0):
            return 0
        else:
            return region
    else:
        return region


def get_exo_tag_stage(event, track, iCand, is_pixel_track, histos):

    # Disappearing track tag from EXO-19-010 search ("EXO tag"):
    
    if is_pixel_track:
        hlabel = "cutflow_exo_short"
    else:
        hlabel = "cutflow_exo_long"
    
    score = 0
    histos[hlabel].Fill(score)
    
    if track.Pt() > 55                                                 : score+=1; histos[hlabel].Fill(score)
    else: return score
    if abs(track.Eta()) < 2.1                                          : score+=1; histos[hlabel].Fill(score)
    else: return score

    # other tracks:
    ptsum_tracks = 0
    for i_track in event.tracks:
        deltaR = track.DeltaR(i_track)
        if deltaR > 0 and deltaR < 0.3:
            ptsum_tracks += i_track.Pt()
    if ptsum_tracks/track.Pt() < 0.05                                  : score+=1; histos[hlabel].Fill(score)
    else: return score

    # other jets:
    exo_track_jet_mindeltaR = 9999
    for jet in event.Jets:
        if jet.Pt() > 30 and abs(jet.Eta()) < 2.4:
            deltaR = jet.DeltaR(track)
            if deltaR < exo_track_jet_mindeltaR:
                exo_track_jet_mindeltaR = deltaR
    if exo_track_jet_mindeltaR > 0.5                                   : score+=1; histos[hlabel].Fill(score)
    else: return score

    if abs(event.tracks_dxyVtx[iCand]) < 0.02                          : score+=1; histos[hlabel].Fill(score)
    else: return score
    if abs(event.tracks_dzVtx[iCand]) < 0.5                            : score+=1; histos[hlabel].Fill(score)
    else: return score

    if event.tracks_nMissingInnerHits[iCand] == 0                      : score+=1; histos[hlabel].Fill(score)
    else: return score
    if event.tracks_nMissingMiddleHits[iCand] == 0                     : score+=1; histos[hlabel].Fill(score)
    else: return score

    if event.tracks_nValidPixelHits[iCand] >= 3                        : score+=1; histos[hlabel].Fill(score)
    else: return score

    # veto electrons:
    pass_iso_electrons = True    
    for i, obj in enumerate(event.Electrons):
        if track.DeltaR(obj) < 0.15:
            pass_iso_electrons = False
    if pass_iso_electrons                                              : score+=1; histos[hlabel].Fill(score)
    else: return score
            
    # veto muons:
    pass_iso_muons = True    
    for i, obj in enumerate(event.Muons):
        if track.DeltaR(obj) < 0.15:
            pass_iso_muons = False
    if pass_iso_muons                                                  : score+=1; histos[hlabel].Fill(score)
    else: return score
    
    # inefficiencies:
    if not (abs(track.Eta()) > 0.15 and abs(track.Eta()) < 0.35)       : score+=1; histos[hlabel].Fill(score)
    else: return score
    if not (abs(track.Eta()) > 1.42 and abs(track.Eta()) < 1.65)       : score+=1; histos[hlabel].Fill(score)
    else: return score
    if not (abs(track.Eta()) > 1.55 and abs(track.Eta()) < 1.85)       : score+=1; histos[hlabel].Fill(score)
    else: return score
    if event.tracks_trkRelIso[iCand] < 0.05                            : score+=1; histos[hlabel].Fill(score)
    else: return score

    #if bool(event.tracks_passPFCandVeto[iCand])                        : score+=1; histos[hlabel].Fill(score)
    #else: return score
               
    #pass_iso_pions = True    
    #for i, obj in enumerate(event.TAPPionTracks):
    #    if track.DeltaR(obj) < 0.15:
    #        pass_iso_pions = False
    #if pass_iso_pions                                                  : score+=1; histos[hlabel].Fill(score)
    #else: return score
        
    if event.tracks_nMissingOuterHits[iCand] >= 3                      : score+=1; histos[hlabel].Fill(score)
    else: return score    
    if event.tracks_matchedCaloEnergy[iCand] < 10                      : score+=1; histos[hlabel].Fill(score)
    else: return score

    return score


def get_mt2_tag_stage(event, track, iCand, is_pixel_track, histos):
    
    pass_mt2_pass_iso = True
    pass_mt2_pass_track_iso = True
    for collection in [event.Electrons, event.Muons]:
        for obj in collection:
            if track.DeltaR(obj) < 0.2:
                pass_mt2_pass_iso = False
    for i_track in event.tracks:
        if track.DeltaR(i_track) < 0.1:
            pass_mt2_pass_track_iso = False

    ptErrOverPt2 = event.tracks_ptError[iCand] / (track.Pt()**2)

    # pixel tracks:
    if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:

        score = 0
        histos["cutflow_mt2_short"].Fill(score)
        
        if track.Pt() > 15                                             : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if abs(track.Eta()) < 2.4                                      : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if not (abs(track.Eta()) > 1.38 and abs(track.Eta()) < 1.6)    : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if ptErrOverPt2 < 0.2                                          : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if abs(event.tracks_dxyVtx[iCand]) < 0.02                      : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if abs(event.tracks_dzVtx[iCand]) < 0.05                       : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand] < 10                       : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand]/track.Pt() < 0.1           : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand] < 10                       : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand]/track.Pt() < 0.2           : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if event.tracks_pixelLayersWithMeasurement[iCand] >= 3         : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if event.tracks_nMissingInnerHits[iCand] == 0                  : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if event.tracks_nMissingOuterHits[iCand] >= 2                  : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if bool(event.tracks_passPFCandVeto[iCand])                    : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if pass_mt2_pass_iso                                           : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        if pass_mt2_pass_track_iso                                     : score+=1; histos["cutflow_mt2_short"].Fill(score)
        else: return score
        
    elif event.tracks_trackerLayersWithMeasurement[iCand] < 7:
        
        score = 0
        histos["cutflow_mt2_medium"].Fill(score)
        
        if track.Pt() > 15                                             : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if abs(track.Eta()) < 2.4                                      : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if not (abs(track.Eta()) > 1.38 and abs(track.Eta()) < 1.6)    : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if ptErrOverPt2 < 0.02                                         : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if abs(event.tracks_dxyVtx[iCand]) < 0.01                      : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if abs(event.tracks_dzVtx[iCand]) < 0.05                       : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand] < 10                       : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand]/track.Pt() < 0.1           : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand] < 10                       : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand]/track.Pt() < 0.2           : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if event.tracks_pixelLayersWithMeasurement[iCand] >= 2         : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if event.tracks_nMissingInnerHits[iCand] == 0                  : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if event.tracks_nMissingOuterHits[iCand] >= 2                  : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if bool(event.tracks_passPFCandVeto[iCand])                    : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if pass_mt2_pass_iso                                           : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        if pass_mt2_pass_track_iso                                     : score+=1; histos["cutflow_mt2_medium"].Fill(score)
        else: return score
        
    elif event.tracks_trackerLayersWithMeasurement[iCand] >= 7:
        
        score = 0
        histos["cutflow_mt2_long"].Fill(score)
        
        if track.Pt() > 15                                             : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if abs(track.Eta()) < 2.4                                      : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if not (abs(track.Eta()) > 1.38 and abs(track.Eta()) < 1.6)    : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if ptErrOverPt2 < 0.005                                        : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if abs(event.tracks_dxyVtx[iCand]) < 0.01                      : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if abs(event.tracks_dzVtx[iCand]) < 0.05                       : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand] < 10                       : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand]/track.Pt() < 0.1           : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand] < 10                       : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand]/track.Pt() < 0.2           : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if event.tracks_pixelLayersWithMeasurement[iCand] >= 2         : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if event.tracks_nMissingInnerHits[iCand] == 0                  : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if event.tracks_nMissingOuterHits[iCand] >= 2                  : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if bool(event.tracks_passPFCandVeto[iCand])                    : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if pass_mt2_pass_iso                                           : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if ((track.Pt()<150 and event.MT2>100) or track.Pt()>150)      : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
        if pass_mt2_pass_track_iso                                     : score+=1; histos["cutflow_mt2_long"].Fill(score)
        else: return score
                
    else:
        return 0
        

def get_BDT_score(label, event, iCand, readers, is_pixel_track, ptErrOverPt2):
    
    if is_pixel_track:
        category = "short"
    else:
        category = "long"
    
    for var in readers[label + "_" + category]["tmva_variables"]:
        
        if "ptErrOverPt2" in var:
            readers[label + "_" + category]["tmva_variables"][var][0] = ptErrOverPt2
        elif "tracks_" in var:
            readers[label + "_" + category]["tmva_variables"][var][0] = eval("event.%s[%s]" % (var, iCand))
        else:
            readers[label + "_" + category]["tmva_variables"][var][0] = eval("event.tracks_%s[%s]" % (var, iCand))
    
    return readers[label + "_" + category]["reader"].EvaluateMVA("BDT")


def reweight_ctau(ctauIn, ctauOut, LabXY_list, mode = 0):
        
    output = 1
    for i_LabXY in LabXY_list:
        
        t0 = i_LabXY[0] / 10.0
        boost = i_LabXY[1]

        # ct0 saved as mm, need in cm for formula:
        if mode == 0:
            t0 = t0
        elif mode == 1:
            t0 = t0 * boost
        elif mode == 2:
            t0 = t0 / boost
        
        output *= ctauIn/ctauOut * math.exp(t0/ctauIn - t0/ctauOut)
    
    return output


def main(event_tree_filenames, track_tree_output, nevents = -1, only_tagged_events = False, save_cleaned_variables = False, overwrite = False, debug = False, keep_all_tracks = False, cutflow_study = True):

    print "Input: %s \nOutput: %s \n n_ev: %s" % (event_tree_filenames, track_tree_output, nevents)

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    if cutflow_study:
        keep_all_tracks = True

    # check if output file exists:
    if not overwrite and os.path.exists(track_tree_output):
        try:
            test = TFile(track_tree_output)
            test.Get("nev")
            test.Get("Events")
            if not (test.IsZombie() or test.TestBit(TFile.kRecovered)):
                print "Already done, file ok"
                test.Close()
                return()
            test.Close()
        except:
            print "Need to redo file"

    # store runs for JSON output:
    runs = {}

    # check if data:
    phase = 0
    data_period = ""
    is_signal = False
    is_data = False
    is_fastsim = False
    for label in ["Run2016", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18", "RunIISummer16MiniAODv3"]:
        if label in event_tree_filenames[0]:
            data_period = label
            if "Run201" in label:
                is_data = True
            if label == "Run2016" or label == "Summer16" or label == "RunIISummer16MiniAODv3":
                phase = 0
            elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
                phase = 1
         
    if data_period == "RunIISummer16MiniAODv3":
        data_period = "Summer16"

    if "FastSim" in event_tree_filenames[0]:
        is_fastsim = True

    if "_chi" in event_tree_filenames[0] or "SMS-" in event_tree_filenames[0]:
        is_signal = True

    print "Signal: %s, phase: %s" % (is_signal, phase)

    #fMask = TFile('../../disappearing-track-tag/Masks_mcal10to15.root')
    #hMask = fMask.Get('h_Mask_allyearsLongSElValidationZLLCaloSideband_EtaVsPhiDT')
    #hMask.SetDirectory(0)
    #fMask.Close()
    hMask = ''
    
    # load tree
    tree = TChain("TreeMaker2/PreSelection")
    for iFile in event_tree_filenames:
        if not "root.mimes" in iFile:
            tree.Add(iFile)
   
    fout = TFile(track_tree_output, "recreate")
    
    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    histos = {}
    histos["cutflow_exo_short"] = TH1F("cutflow_exo_short", "cutflow_exo_short", 20, 0, 20)
    histos["cutflow_exo_long"] = TH1F("cutflow_exo_long", "cutflow_exo_long", 20, 0, 20)
    histos["cutflow_mt2_short"] = TH1F("cutflow_mt2_short", "cutflow_mt2_short", 20, 0, 20)
    histos["cutflow_mt2_medium"] = TH1F("cutflow_mt2_medium", "cutflow_mt2_medium", 20, 0, 20)
    histos["cutflow_mt2_long"] = TH1F("cutflow_mt2_long", "cutflow_mt2_long", 20, 0, 20)

    h_nev.Fill(0, nev)
    h_nev.Write()

    # no special handling for Autumn18 yet, so use Fall17
    if data_period == "Autumn18":
        data_period == "Fall17"

    if data_period != "":
        print "data_period: %s, phase: %s" % (data_period, phase)
    else:
        print "Can't determine data/MC era!"
        quit(1)

    # adjust some variables:        
    if data_period == "Run2016" or data_period == "Summer16":
        BTAG_deepCSV = 0.6324
    if data_period == "Run2017" or data_period == "Fall17":
        BTAG_deepCSV = 0.4941
    if data_period == "Run2018":
        BTAG_deepCSV = 0.4184
    btag_cut = BTAG_deepCSV

    # load BDTs and fetch list of DT tag label:
    bdts = {
        "tight_may20_chi2": {
                    "short": ["../../disappearing-track-tag/201X-short-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                    "long":  ["../../disappearing-track-tag/201X-long-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",   ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                 },
        "loose_may20_chi2": {
                    "short": ["../../disappearing-track-tag/201X-short-tracks-may20-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",      ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                    "long":  ["../../disappearing-track-tag/201X-long-tracks-may20-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",       ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                 },
        "tight_may20_chi2_phase0": {
                    "short": ["../../disappearing-track-tag/2016-short-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                    "long":  ["../../disappearing-track-tag/2016-long-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",   ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                 },
        "loose_may20_chi2_phase0": {
                    "short": ["../../disappearing-track-tag/2016-short-tracks-may20-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",      ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                    "long":  ["../../disappearing-track-tag/2016-long-tracks-may20-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",       ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                 },
        "tight_may20_chi2_phase1": {
                    "short": ["../../disappearing-track-tag/2017-short-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                    "long":  ["../../disappearing-track-tag/2017-long-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",   ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                 },
        "loose_may20_chi2_phase1": {
                    "short": ["../../disappearing-track-tag/2017-short-tracks-may20-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",      ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                    "long":  ["../../disappearing-track-tag/2017-long-tracks-may20-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",       ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                 },
        "tight_may20_chi2_phase1_v2": {
                    "short": ["../../disappearing-track-tag/2017-short-tracks-may20-dxy-chi2-v2/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                    "long":  ["../../disappearing-track-tag/2017-long-tracks-may20-dxy-chi2-v2/dataset/weights/TMVAClassification_BDT.weights.xml",   ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                 },
           }

    readers = {}
    for label in bdts:
        for category in ["short", "long"]:
        
            readers[label + "_" + category] = {}
            readers[label + "_" + category]["tmva_variables"] = {}
            readers[label + "_" + category]["reader"] = TMVA.Reader()
            
            for var in bdts[label][category][1]:
                readers[label + "_" + category]["tmva_variables"][var] = array('f',[0])
                readers[label + "_" + category]["reader"].AddVariable(var, readers[label + "_" + category]["tmva_variables"][var])

            if phase == 0:
                readers[label + "_" + category]["reader"].BookMVA("BDT", bdts[label][category][0].replace("201X", "2016"))
            else:
                readers[label + "_" + category]["reader"].BookMVA("BDT", bdts[label][category][0].replace("201X", "2017"))
    
    tout = TTree("Events", "tout")

    # prepare variables for output tree   
    float_branches = [
                      "weight",
                      "MET",
                      "MHT",
                      "HT",
                      "PFCaloMETRatio",
                      "event",
                      "run",
                      "lumisec",
                      "leadinglepton_pt",
                      "leadinglepton_mt",
                      "leadinglepton_eta",
                      "leadinglepton_phi",
                      "leadinglepton_charge",
                      "leadinglepton_dedx",
                      "MinDeltaPhiMhtJets",
                      "MinDeltaPhiLeptonMht",
                      "MinDeltaPhiLeptonJets",
                      "ptRatioMhtJets",
                      "ptRatioLeptonMht",
                      "ptRatioLeptonJets",
                     ]
    
    if is_signal:
        float_branches += [
                      "chargino_parent_mass",
                      "signal_gluino_mass",
                      "signal_lsp_mass",
                      "reweightTo10",
                      "reweightTo30",
                      "reweightTo50",
                      "reweightTo100",
                      "reweightTo200",
                    ]
                     
    integer_branches = [
                        "pass_baseline",
                        "n_goodjets",
                        "n_btags",
                        "n_goodelectrons",
                        "n_goodmuons",
                        "n_allvertices",
                        "leadinglepton_id",
                       ]

    if not is_data:
        integer_branches += [
                        "n_genLeptons",
                        "n_genElectrons",
                        "n_genMuons",
                        "n_genTaus",
                            ]

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

    vector_int_branches = [
                           'tracks_is_pixel_track', 
                           'tracks_pixelLayersWithMeasurement', 
                           'tracks_trackerLayersWithMeasurement', 
                           'tracks_nMissingInnerHits', 
                           'tracks_nMissingMiddleHits', 
                           'tracks_nMissingOuterHits', 
                           'tracks_nValidPixelHits', 
                           'tracks_nValidTrackerHits', 
                           'tracks_nValidPixelHits', 
                           'tracks_nValidTrackerHits', 
                           'tracks_passPFCandVeto', 
                           'tracks_charge', 
                           'tracks_passmask', 
                           'tracks_region',
                           'tracks_mt2tag',
                           'tracks_exotag',
                           'tracks_baseline',
                          ]
                          
    if not is_data:
        vector_int_branches += [
                            'tracks_fake',
                            'tracks_prompt_electron', 
                            'tracks_prompt_muon', 
                            'tracks_prompt_tau', 
                            'tracks_prompt_tau_widecone', 
                            'tracks_prompt_tau_leadtrk', 
                            'tracks_prompt_tau_hadronic', 
                            ]
            
    for branch in vector_int_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<int>', tree_branch_values[branch])

    vector_float_branches = [
                             'tracks_dxyVtx',
                             'tracks_dzVtx',
                             'tracks_matchedCaloEnergy',
                             'tracks_trkRelIso',
                             'tracks_ptErrOverPt2',
                             'tracks_pt',
                             'tracks_eta',
                             'tracks_phi',
                             'tracks_trkMiniRelIso',
                             'tracks_trackJetIso',
                             'tracks_ptError',
                             'tracks_neutralPtSum',
                             'tracks_neutralWithoutGammaPtSum',
                             'tracks_minDrLepton',
                             'tracks_matchedCaloEnergyJets',
                             'tracks_deDxHarmonic2pixel',
                             'tracks_deDxHarmonic2strips',
                             'tracks_massfromdeDxPixel',
                             'tracks_massfromdeDxStrips',
                             'tracks_chi2perNdof',
                             'tracks_chargedPtSum',
                             'tracks_mt',
                             'tracks_invmass',
                             'tracks_MinDeltaPhiTrackMht',
                             'tracks_MinDeltaPhiTrackLepton',
                             'tracks_MinDeltaPhiTrackJets',
                             'tracks_ptRatioTrackMht',
                             'tracks_ptRatioTrackLepton',
                             'tracks_ptRatioTrackJets',
                            ]

    if True:
        vector_float_branches += [
                            'tracks_chiCandGenMatchingDR',
                            'tracks_chiLabXY',
                            'tracks_chiGamma',
                            'tracks_chiBeta',
                            'tracks_chiEta',
                            'tracks_chiPt',
                                ]

    for label in bdts:
        vector_float_branches += ["tracks_mva_%s" % label]

    for branch in vector_float_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<double>', tree_branch_values[branch])
            
    print "Looping over %s events" % nev

    for iEv, event in enumerate(tree):
        
        if nevents > 0 and iEv > nevents: break      
        if (iEv+1) % 1000 == 0:
            print "event %s / %s" % (iEv + 1, nev)

        # calculate weight and collect lumisections:
        if is_data:
            runnum = event.RunNum
            lumisec = event.LumiBlockNum
            if runnum not in runs:
                runs[runnum] = []
            if lumisec not in runs[runnum]:
                runs[runnum].append(lumisec)
            weight = 1.0
        else:
            weight = 1.0 * event.puWeight * event.CrossSection

        current_file_name = tree.GetFile().GetName()

        # reset all branch values:
        for label in tree_branch_values:
            if "tracks_" in label or "leptons_" in label:
                continue
            tree_branch_values[label][0] = -1

        if is_signal:
            signal_gluino_mass = -1
            signal_lsp_mass = -1
            for i_genParticle, genParticle in enumerate(event.GenParticles):
                if abs(event.GenParticles_PdgId[i_genParticle]) == 1000021:
                    signal_gluino_mass = round(genParticle.M())
                elif abs(event.GenParticles_PdgId[i_genParticle]) == 1000022:
                    signal_lsp_mass = round(genParticle.M())
                
        # basic event selection:
        passed_baseline_selection = True
        if is_fastsim:
            if not shared_utils.passesUniversalSelectionFastSim(event):
                passed_baseline_selection = False
        else:
            if not is_data and not shared_utils.passesUniversalSelection(event):
                passed_baseline_selection = False
            elif is_data and not shared_utils.passesUniversalDataSelection(event):
                passed_baseline_selection = False

        if not keep_all_tracks and not passed_baseline_selection:
            continue

        # check trigger:
        if is_data:            
            if "MET" in current_file_name and not shared_utils.PassTrig(event, 'MhtMet6pack'):
                continue
            elif "SingleElectron" in current_file_name and not shared_utils.PassTrig(event, 'SingleElectron'):
                continue
            elif "SingleMuon" in current_file_name and not shared_utils.PassTrig(event, 'SingleMuon'):
                continue
            elif "JetHT" in current_file_name and not shared_utils.PassTrig(event, 'HtTrain'):
                continue

        # select good leptons:
        goodleptons_info = []
        goodleptons = []
        n_goodelectrons = 0
        n_goodmuons = 0
        for i, electron in enumerate(event.Electrons):
            if electron.Pt() > 30 and abs(electron.Eta()) < 2.4 and bool(event.Electrons_passIso[i]) and bool(event.Electrons_tightID[i]):

                # check for jets:
                for jet in event.Jets:
                    if jet.DeltaR(electron) < 0.1: continue

                goodleptons.append(electron)
                n_goodelectrons += 1
                
                matched_dedx = -1.0
                for iCand, track in enumerate(event.tracks):
                    if track.DeltaR(electron) < 0.02:
                        matched_dedx = event.tracks_deDxHarmonic2pixel[iCand]
                                
                goodleptons_info.append({"leptons_pt": electron.Pt(),
                                            "leptons_eta": electron.Eta(),
                                            "leptons_mt": event.Electrons_MTW[i],
                                            "leptons_phi": electron.Phi(),
                                            "leptons_iso": bool(event.Electrons_passIso[i]),
                                            "leptons_charge": event.Electrons_charge[i],
                                            "leptons_dedx": correct_dedx_intercalibration(matched_dedx, current_file_name, electron.Eta()),
                                            "leptons_id": 11,
                                            })
                                             
        for i, muon in enumerate(event.Muons):
            if muon.Pt() > 30 and abs(muon.Eta()) < 2.4 and bool(event.Muons_passIso[i]) and bool(event.Muons_tightID[i]):

                # check for jets:
                for jet in event.Jets:
                    if jet.DeltaR(muon) < 0.1: continue

                goodleptons.append(muon)
                n_goodmuons += 1
                
                matched_dedx = -1.0
                for iCand, track in enumerate(event.tracks):
                    if track.DeltaR(muon) < 0.02:
                        matched_dedx = event.tracks_deDxHarmonic2pixel[iCand]
                
                goodleptons_info.append({"leptons_pt": muon.Pt(),
                                            "leptons_eta": muon.Eta(),
                                            "leptons_mt": event.Muons_MTW[i],
                                            "leptons_phi": muon.Phi(),
                                            "leptons_iso": bool(event.Muons_passIso[i]),
                                            "leptons_charge": event.Muons_charge[i],
                                            "leptons_dedx": correct_dedx_intercalibration(matched_dedx, current_file_name, muon.Eta()),
                                            "leptons_id": 13,
                                            })

        n_goodleptons = n_goodelectrons + n_goodmuons
        
        # get leading lepton:
        highest_lepton_pt = 0
        highest_lepton_pt_index = 0
        for i, lepton_output_dict in enumerate(goodleptons_info):
            for label in lepton_output_dict:
                if lepton_output_dict["leptons_pt"] > highest_lepton_pt:
                    highest_lepton_pt_index = i
        if len(goodleptons) > 0:
            leading_lepton = goodleptons[highest_lepton_pt_index]

            # save leading lepton:
            tree_branch_values["leadinglepton_pt"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_pt"]
            tree_branch_values["leadinglepton_mt"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_mt"]
            tree_branch_values["leadinglepton_eta"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_eta"]
            tree_branch_values["leadinglepton_charge"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_charge"]
            tree_branch_values["leadinglepton_phi"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_phi"]
            tree_branch_values["leadinglepton_dedx"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_dedx"]
            tree_branch_values["leadinglepton_id"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_id"]

        else:
            leading_lepton = 0
               
        # get T2bt and T1qqqq xsections:
        if is_signal:
            chargino_parent_mass = -1.0
            parent_mass = -1.0
            if "T2bt" in current_file_name:
                for i_genParticle, genParticle in enumerate(event.GenParticles):
                    if abs(event.GenParticles_PdgId[i_genParticle]) == 1000024:
                        parent_id = event.GenParticles_ParentIdx[i_genParticle]
                        parent_pdgid = event.GenParticles_PdgId[parent_id]
                        if abs(parent_pdgid) == 1000005 or abs(parent_pdgid) == 1000006:
                            parent_mass = event.GenParticles[parent_id].M()
                            event.CrossSection = xsections.get_sbottom_antisbottom_cross_section(parent_mass)
                            chargino_parent_mass = parent_mass
                            break
            elif "T1qqqq" in current_file_name:
                for i_genParticle, genParticle in enumerate(event.GenParticles):
                    if abs(event.GenParticles_PdgId[i_genParticle]) == 1000024:
                        parent_id = event.GenParticles_ParentIdx[i_genParticle]
                        parent_pdgid = event.GenParticles_PdgId[parent_id]
                        if abs(parent_pdgid) == 1000021:
                            parent_mass = event.GenParticles[parent_id].M()
                            event.CrossSection = xsections.get_T1_xsection(parent_mass)
                            chargino_parent_mass = parent_mass
                            break
            elif "g1800_chi1400_27_200970" in current_file_name:
                event.CrossSection = 0.00276133 #pb
            else:
                print "signal xsection undefined!"
                quit()

        if tree.GetBranch("madHT"):
            madHT = event.madHT
            if not pass_background_stitching(current_file_name, madHT, phase): continue
        else:
            madHT = -1
        
        # count number of good jets:
        n_goodjets = 0
        leading_jet = 0
        leading_jet_pt = 0
        goodjets = []
        for jet in event.Jets:
            if jet.Pt() > 30 and abs(jet.Eta()) < 2.4:
                for lepton in list(event.Muons) + list(event.Electrons):
                    if jet.DeltaR(lepton) < 0.5:
                        continue
                n_goodjets += 1
                goodjets.append(jet)
                if jet.Pt() > leading_jet_pt:
                    leading_jet_pt = jet.Pt()
                    leading_jet = jet
        event.n_goodjets = n_goodjets

        # event topologies (Mht + Jets):
        MinDeltaPhiMhtJets = 9999
        ptRatioMhtJets = 0
        mhtvec = TLorentzVector()
        mhtvec.SetPtEtaPhiE(event.MHT, 0, event.MHTPhi, event.MHT)
        for ijet, jet in enumerate(event.Jets):
            if not (abs(jet.Eta())<2.4 and jet.Pt()>30):
                continue
            if abs(jet.DeltaPhi(mhtvec)) < MinDeltaPhiMhtJets:
                MinDeltaPhiMhtJets = abs(jet.DeltaPhi(mhtvec))
                if event.MHT>0:
                    ptRatioMhtJets = jet.Pt() / event.MHT
                else:
                    ptRatioMhtJets = 0

        # event topologies (leadinglepton + MHT):
        if len(goodleptons) > 0:    
            if abs(leading_lepton.DeltaPhi(mhtvec))>0:
                MinDeltaPhiLeptonMht = abs(leading_lepton.DeltaPhi(mhtvec))
            else:
                MinDeltaPhiLeptonMht = 0

            if event.MHT>0:
                ptRatioLeptonMht = leading_lepton.Pt() / event.MHT
            else:
                ptRatioLeptonMht = 0

        if len(goodleptons) > 0 and n_goodjets > 0:    

            if abs(leading_jet.DeltaPhi(leading_lepton))>0:
                MinDeltaPhiLeptonJets = abs(leading_jet.DeltaPhi(leading_lepton))
            else:
                MinDeltaPhiLeptonJets = 0

            if leading_jet.Pt()>0:
                ptRatioLeptonJets = leading_lepton.Pt() / leading_jet.Pt()
            else:
                ptRatioLeptonJets = 0
        else:
            MinDeltaPhiLeptonMht = 0
            ptRatioLeptonMht = 0
            MinDeltaPhiLeptonJets = 0
            ptRatioLeptonJets = 0
            
        mva_scores = {}
        tagged_tracks = []

        for iCand, track in enumerate(event.tracks):
                        
            # basic track selection:
            if track.Pt() < 30: continue

            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            elif event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = False

            if keep_all_tracks:
                exo_tag_score = get_exo_tag_stage(event, track, iCand, is_pixel_track, histos)
                mt2_tag_score = get_mt2_tag_stage(event, track, iCand, is_pixel_track, histos)
            else:
                exo_tag_score = 0
                mt2_tag_score = 0

            pass_baseline_track_selection = True

            # check for nearby leptons and pions:
            drlep = 99
            islep = False
            for ilep, lep in enumerate(list(event.Electrons) + list(event.Muons) + list(event.TAPPionTracks)): 
                drlep = min(drlep, lep.DeltaR(track))
                if drlep<0.1:
                    islep = True
                    break            
            if islep:
                pass_baseline_track_selection = False

            if not keep_all_tracks and not pass_baseline_track_selection:
                continue             

            # veto DTs too close to jets
            isjet = False
            for jet in event.Jets:
                if not jet.Pt()>25: continue
                if jet.DeltaR(track)<0.4: 
                    isjet = True
                    break
            if isjet:
                pass_baseline_track_selection = False

            if not keep_all_tracks and not pass_baseline_track_selection:
                continue
                
            ptErrOverPt2 = event.tracks_ptError[iCand] / (track.Pt()**2)

            # speed things up!
            if not keep_all_tracks and event.tracks_trkRelIso[iCand]>0.01:
                continue
            if not keep_all_tracks and event.tracks_deDxHarmonic2pixel[iCand]<2.0:
                continue

            base_cuts = bool(event.tracks_trackQualityHighPurity[iCand]) and \
                        abs(track.Eta())<2.4 and \
                        ptErrOverPt2<10 and \
                        event.tracks_dzVtx[iCand]<0.1 and \
                        event.tracks_trkRelIso[iCand]<0.2 and \
                        event.tracks_trackerLayersWithMeasurement[iCand]>=2 and \
                        event.tracks_nValidTrackerHits[iCand]>=2 and \
                        event.tracks_nMissingInnerHits[iCand]==0 and \
                        event.tracks_nValidPixelHits[iCand]>=2 and \
                        bool(event.tracks_passPFCandVeto[iCand])
                                                
            if not is_pixel_track:
                base_cuts = base_cuts and event.tracks_nMissingOuterHits[iCand]>=2 
            
            # keep only baseline tracks:
            if not base_cuts:
                pass_baseline_track_selection = False

            if not keep_all_tracks and not pass_baseline_track_selection:
                continue

            pass_mask = True
            if hMask!='':
                xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
                ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
                if hMask.GetBinContent(ibinx, ibiny)==0: 
                    pass_mask = False
                    
            for label in bdts:
                mva_scores[label] = get_BDT_score(label, event, iCand, readers, is_pixel_track, ptErrOverPt2)
                        
            # check if actual fake track (no genparticle in cone around track):
            is_prompt_electron = False
            is_prompt_muon = False
            is_prompt_tau = False
            is_prompt_tau_hadronic = False
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
                
                for k in range(len(event.GenTaus)):
                    deltaR = track.DeltaR(event.GenTaus[k])
                    is_hadronic = bool(event.GenTaus_had[k])
                    if deltaR < 0.02 and is_hadronic:
                        is_prompt_tau_hadronic = True

                # for hadronic taus, check GenTaus_LeadTrk tracks:
                for l in range(len(event.GenTaus_LeadTrk)):
                    deltaR = track.DeltaR(event.GenTaus_LeadTrk[l])
                    is_hadronic = bool(event.GenTaus_had[l])
                    if is_hadronic:
                        if deltaR < 0.02:
                            is_prompt_tau_leadtrk = True
                        if deltaR < 0.4:
                            is_prompt_tau_widecone = True

            is_fake_track = not (is_prompt_electron or is_prompt_muon or is_prompt_tau or is_prompt_tau_leadtrk)

            tracks_massfromdeDxPixel = TMath.Sqrt((event.tracks_deDxHarmonic2pixel[iCand]-2.557)*pow(track.P(),2)/2.579)
            tracks_massfromdeDxStrips = TMath.Sqrt((event.tracks_deDxHarmonic2strips[iCand]-2.557)*pow(track.P(),2)/2.579)
            
            # if leptons in the event, calculate invariant mass w.r.t. to leading lepton:
            if len(goodleptons) > 0:
                if event.tracks_charge[iCand] * goodleptons_info[highest_lepton_pt_index]["leptons_charge"] == -1:
                    invariant_mass = (track + goodleptons[highest_lepton_pt_index]).M()
                else:
                    invariant_mass = -1
            else:
                invariant_mass = -1

            # if signal, do chargino matching:
            chiCandGenMatchingDR = 100
            chi_LabXY = -1
            chi_Gamma = -1
            chi_Beta = -1
            chi_Eta = -1
            chi_Pt = -1
            if is_signal:
                min_deltaR = 100
                for k in range(len(event.GenParticles)):
                    if abs(event.GenParticles_PdgId[k]) == 1000024:
                        deltaR = track.DeltaR(event.GenParticles[k])
                        if deltaR < min_deltaR:
                            chiCandGenMatchingDR = deltaR
                            try:
                                chi_LabXY = event.GenParticles_LabXYmm[k]
                                chi_Gamma = event.GenParticles[k].Gamma()
                                chi_Beta = event.GenParticles[k].Beta()
                                chi_Eta = event.GenParticles[k].Eta()
                                chi_Pt = event.GenParticles[k].Pt()
                            except:
                                pass
                         
            # some debug info:       
            #if chiCandGenMatchingDR<0.01:
            #    print "Chargino found in event", iEv
            #    print "mt2_tag_score", mt2_tag_score
            #    print "exo_tag_score", exo_tag_score
            
            DeDxCorrected = correct_dedx_intercalibration(event.tracks_deDxHarmonic2pixel[iCand], current_file_name, abs(track.Eta()))
            region = get_signal_region(event.HT, event.MHT, n_goodjets, event.BTags, MinDeltaPhiMhtJets, 1, is_pixel_track, DeDxCorrected, n_goodelectrons, n_goodmuons, event_tree_filenames[0])
            
            MinDeltaPhiTrackMht = abs(track.DeltaPhi(mhtvec))
            if track.Pt()>0:
                ptRatioTrackMht = event.MHT / track.Pt()
            else:
                ptRatioTrackMht = 0
            
            if leading_lepton:
                MinDeltaPhiTrackLepton = abs(track.DeltaPhi(leading_lepton))
                if track.Pt()>0:
                    ptRatioTrackLepton = leading_lepton.Pt() / track.Pt()
                else:
                    ptRatioTrackLepton = 0
            else:
                MinDeltaPhiTrackLepton = -1
                ptRatioTrackLepton = -1
                
            if leading_jet:
                MinDeltaPhiTrackJets = abs(track.DeltaPhi(leading_jet))
                if track.Pt()>0:
                    ptRatioTrackJets = leading_jet.Pt() / track.Pt()
                else:
                    ptRatioTrackJets = 0
            else:
                MinDeltaPhiTrackJets = -1
                ptRatioTrackJets = -1
            
            tagged_tracks.append(
                                   {
                                     "tracks_is_pixel_track": is_pixel_track,
                                     "tracks_baseline": pass_baseline_track_selection,
                                     "tracks_pixelLayersWithMeasurement": event.tracks_pixelLayersWithMeasurement[iCand],
                                     "tracks_trackerLayersWithMeasurement": event.tracks_trackerLayersWithMeasurement[iCand],
                                     "tracks_nMissingInnerHits": event.tracks_nMissingInnerHits[iCand],
                                     "tracks_nMissingMiddleHits": event.tracks_nMissingMiddleHits[iCand],
                                     "tracks_nMissingOuterHits": event.tracks_nMissingOuterHits[iCand],
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
                                     "tracks_trkMiniRelIso": event.tracks_trkMiniRelIso[iCand],
                                     "tracks_ptError": event.tracks_ptError[iCand],
                                     "tracks_passPFCandVeto": bool(event.tracks_passPFCandVeto[iCand]),
                                     "tracks_neutralPtSum": event.tracks_neutralPtSum[iCand],
                                     "tracks_neutralWithoutGammaPtSum": event.tracks_neutralWithoutGammaPtSum[iCand],
                                     "tracks_minDrLepton": event.tracks_minDrLepton[iCand],
                                     "tracks_matchedCaloEnergyJets": event.tracks_matchedCaloEnergyJets[iCand],
                                     "tracks_deDxHarmonic2pixel": DeDxCorrected,
                                     "tracks_deDxHarmonic2strips": event.tracks_deDxHarmonic2strips[iCand],
                                     "tracks_massfromdeDxPixel": tracks_massfromdeDxPixel,
                                     "tracks_massfromdeDxStrips": tracks_massfromdeDxStrips,
                                     "tracks_chi2perNdof": event.tracks_chi2perNdof[iCand],
                                     "tracks_mt": event.tracks[iCand].Mt(),
                                     "tracks_chargedPtSum": event.tracks_chargedPtSum[iCand],
                                     "tracks_charge": event.tracks_charge[iCand],
                                     "tracks_invmass": invariant_mass,
                                     "tracks_exotag": exo_tag_score,
                                     "tracks_mt2tag": mt2_tag_score,
                                     "tracks_passmask": pass_mask,
                                     "tracks_region": region,
                                     'tracks_MinDeltaPhiTrackMht': MinDeltaPhiTrackMht,
                                     'tracks_MinDeltaPhiTrackLepton': MinDeltaPhiTrackLepton,
                                     'tracks_MinDeltaPhiTrackJets': MinDeltaPhiTrackJets,
                                     'tracks_ptRatioTrackMht': ptRatioTrackMht,
                                     'tracks_ptRatioTrackLepton': ptRatioTrackLepton,
                                     'tracks_ptRatioTrackJets': ptRatioTrackJets,
                                   }
                                  )
                                  
            if not is_data:
                tagged_tracks[-1]["tracks_fake"] = is_fake_track
                tagged_tracks[-1]["tracks_prompt_electron"] = is_prompt_electron
                tagged_tracks[-1]["tracks_prompt_muon"] = is_prompt_muon
                tagged_tracks[-1]["tracks_prompt_tau"] = is_prompt_tau
                tagged_tracks[-1]["tracks_prompt_tau_hadronic"] = is_prompt_tau_hadronic
                tagged_tracks[-1]["tracks_prompt_tau_leadtrk"] = is_prompt_tau_leadtrk
                tagged_tracks[-1]["tracks_prompt_tau_widecone"] = is_prompt_tau_widecone

            if True:
                tagged_tracks[-1]["tracks_chiCandGenMatchingDR"] = chiCandGenMatchingDR
                tagged_tracks[-1]["tracks_chiLabXY"] = chi_LabXY
                tagged_tracks[-1]["tracks_chiGamma"] = chi_Gamma
                tagged_tracks[-1]["tracks_chiBeta"] = chi_Beta
                tagged_tracks[-1]["tracks_chiEta"] = chi_Eta
                tagged_tracks[-1]["tracks_chiPt"] = chi_Pt
                                       
            for label in mva_scores:
                tagged_tracks[-1]["tracks_mva_%s" % label] = mva_scores[label]
                
            tagged_tracks[-1]["object"] = track
            
            # some synchronization info:           
            if debug:
                if tagged_tracks[-1]["tracks_mva_tight_may20_chi2"]>-0.05 and tagged_tracks[-1]["tracks_trkRelIso"]<0.01:
                    print "****************"
                    print "track found in %s:%s:%s" % (event.RunNum, event.LumiBlockNum, event.EvtNum)
                    print mva_scores
                    print tagged_tracks[-1]
                    print "****************"
                    print event.EvtNum, tagged_tracks[-1]["tracks_pt"]
                
  
        # keep only events with candidate tracks
        if len(tagged_tracks)==0:
            continue
        
        # adjust some variables:        
        if data_period == "Run2016" or data_period == "Summer16":
            BTAG_deepCSV = 0.6324
        if data_period == "Run2017" or data_period == "Fall17":
            BTAG_deepCSV = 0.4941
        if data_period == "Run2018":
            BTAG_deepCSV = 0.4184
        btag_cut = BTAG_deepCSV
        
        adjustedBTags = 0
        adjustedJets = []
        adjustedHt = 0
        adjustedMht = TLorentzVector()
        adjustedMht.SetPxPyPzE(0,0,0,0)
        for ijet, jet in enumerate(event.Jets):
            if not jet.Pt() > 30: continue            
            if not abs(jet.Eta()) < 5.0: continue
            #someoverlap = False
            #for dt in tagged_tracks:
            #    if dt["tracks_SR_short"]+dt["tracks_SR_long"]>0: 
            #        if jet.DeltaR(dt["object"])<0.4: 
            #            someoverlap = True
            #            break
            #if someoverlap: continue
            adjustedMht -= jet        
            if not abs(jet.Eta()) < 2.4: continue
            adjustedJets.append(jet)            
            if event.Jets_bJetTagDeepCSVBvsAll[ijet] > btag_cut: adjustedBTags += 1 ####hellooo
            adjustedHt += jet.Pt()
        adjustedNJets = len(adjustedJets)
        mindphi = 4
        for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht))) 
            
        # update variables:
        event.BTags = adjustedBTags
        n_goodjets = adjustedNJets
        event.HT = adjustedHt
        event.MHT = adjustedMht.Pt()
        MinDeltaPhiMhtJets = mindphi
        
        # reweighting:
        if is_signal:
            LabXY_list = [] 
            for k, genparticle in enumerate(event.GenParticles):
                if abs(event.GenParticles_PdgId[k]) == 1000024:
                    try:
                        LabXY_list.append( [event.GenParticles_LabXYmm[k], event.GenParticles[k].Gamma() * event.GenParticles[k].Beta()] )
                    except:
                        pass
            
            if "T2bt" in event_tree_filenames[0]:
                ctauIn = 117
            elif "T1qqqq" in event_tree_filenames[0]:
                ctauIn = 86
            
            for ctauOut in [10, 30, 50, 100, 200]: 
                tree_branch_values["reweightTo%s" % ctauOut][0] = reweight_ctau(ctauIn, ctauOut, LabXY_list)
                
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

        # save event-level variables:
        try:
            tree_branch_values["run"][0] = event.RunNum
            tree_branch_values["lumisec"][0] = event.LumiBlockNum
        except:
            print "Error while saving event number info"
        tree_branch_values["pass_baseline"][0] = passed_baseline_selection
        tree_branch_values["n_goodelectrons"][0] = n_goodelectrons
        tree_branch_values["n_goodmuons"][0] = n_goodmuons
        tree_branch_values["n_btags"][0] = event.BTags
        tree_branch_values["n_goodjets"][0] = n_goodjets
        tree_branch_values["n_allvertices"][0] = event.nAllVertices
        tree_branch_values["PFCaloMETRatio"][0] = event.PFCaloMETRatio
        tree_branch_values["MET"][0] = event.MET
        tree_branch_values["MHT"][0] = event.MHT
        tree_branch_values["HT"][0] = event.HT
        tree_branch_values["weight"][0] = weight
        if not is_data:
            tree_branch_values["madHT"][0] = madHT
            tree_branch_values["CrossSection"][0] = event.CrossSection
            tree_branch_values["puWeight"][0] = event.puWeight
            tree_branch_values["n_genLeptons"][0] = n_genLeptons
            tree_branch_values["n_genElectrons"][0] = n_genElectrons
            tree_branch_values["n_genMuons"][0] = n_genMuons
            tree_branch_values["n_genTaus"][0] = n_genTaus
        if is_signal:
            tree_branch_values["signal_gluino_mass"][0] = signal_gluino_mass
            tree_branch_values["signal_lsp_mass"][0] = signal_lsp_mass
            tree_branch_values["chargino_parent_mass"][0] = chargino_parent_mass
        
        tree_branch_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets
        tree_branch_values["ptRatioMhtJets"][0] = ptRatioMhtJets
        tree_branch_values["MinDeltaPhiLeptonMht"][0] = MinDeltaPhiLeptonMht
        tree_branch_values["ptRatioLeptonMht"][0] = ptRatioLeptonMht
        tree_branch_values["MinDeltaPhiLeptonJets"][0] = MinDeltaPhiLeptonJets
        tree_branch_values["ptRatioLeptonJets"][0] = ptRatioLeptonJets

        # track-level variables:
        n_tracks = len(tagged_tracks)
      
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
        for i, track_output_dict in enumerate(tagged_tracks):
            for label in track_output_dict:
                if label != "object":
                    tree_branch_values[label][i] = track_output_dict[label]
                    
        tout.Fill()
    

    if cutflow_study:
        # save canvases:
        for search, histolist in [
                                   ("exo", ["cutflow_exo_long", "cutflow_exo_short"]),
                                   ("mt2", ["cutflow_mt2_long", "cutflow_mt2_medium", "cutflow_mt2_short"]),
                                 ]:
                                 
            c1 = shared_utils.mkcanvas()
            legend = shared_utils.mklegend(x1 = 0.65, y1 = 0.7, x2 = 0.9, y2 = 0.9)
            colors = [kBlue, kOrange, kGreen]
                                 
            for i_label, label in enumerate(histolist):
                shared_utils.histoStyler(histos[label])
                histos[label].SetTitle(";cut stage;Tracks")
                histos[label].SetLineColor(colors.pop(0))
                if i_label == 0:
                    histos[label].Draw("hist")
                else:
                    histos[label].Draw("same hist")
                legend.AddEntry(histos[label], label.replace("_", "").replace("exo", "EXO tag, ").replace("mt2", "MT2 tag, ").replace("cutflow", "") + " tracks")
                histos[label].Write()
            legend.Draw()
            c1.Print("cutflow_%s.pdf" % search)

    fout.cd()
    fout.Write()
    fout.Close()
    
                            
    # write JSON containing lumisections:
    json_filename = track_tree_output.replace(".root", ".json")

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
        with open(json_filename, "w") as fo:
            fo.write(json_content)


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles")
    parser.add_option("--output", dest = "outputfiles")
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--test", dest = "test", action = "store_true")
    parser.add_option("--overwrite", dest = "overwrite", action = "store_true")
    (options, args) = parser.parse_args()
    
    if not options.test:
      
        main(
             options.inputfiles.split(","),
             options.outputfiles,
             nevents = int(options.nev),
             overwrite = options.overwrite,
            )

    else:

        inputfiles = [
                      #"/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/ProductionRun2v3/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_120000-40EE4B49-34BB-E611-A332-001E674FB2D4_RA2AnalysisTree.root",
                      "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_70000-A2BE8E6F-B587-E911-9730-002590A36F46_RA2AnalysisTree.root",
                      #"/pnfs/desy.de/cms/tier2/store/user/tokramer/NtupleHub/ProductionRun2v3/RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8AOD_10000-F8CE1FD1-D253-E811-A8C1-0242AC130002_RA2AnalysisTree.root",
                      #"/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-665AE9C6-5DA5-E911-AF5E-B499BAAC0626_RA2AnalysisTree.root",
                      #"/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8-AOD_110000-18089184-3A3B-E911-936C-0025905A60BC_RA2AnalysisTree.root",
                      #"/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2016B-17Jul2018_ver2-v1.METAOD_90000-BCA4BDEF-639F-E711-97DF-008CFAE45430_RA2AnalysisTree.root",
                      #"/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2017B-31Mar2018-v1.METAOD_50000-1CAE1898-3EE4-E711-9332-B083FED13C9E_RA2AnalysisTree.root",
                      #"/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2018A-17Sep2018-v1.EGammaAOD0_100000-1C45FE2D-8A85-DD43-95F6-1EF8F880B71B_RA2AnalysisTree.root",
                      #"/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_240000-043F9F4D-DA87-E911-A393-0242AC1C0502_RA2AnalysisTree.root",
                     ]

        for inputfile in inputfiles: 

            outputfile = inputfile.split("/")[-1]

            print "Testing file:\n%s", inputfile
            main(
                 [inputfile],
                 outputfile,
                 nevents = -1,
                 overwrite = True,
                 debug = False,
                )

