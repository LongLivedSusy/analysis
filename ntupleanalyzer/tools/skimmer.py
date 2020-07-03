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

def correct_dedx_intercalibration(dedx, filename):
    
    correction_values = {'Run2016H': 1.0, 'Run2016D': 0.9110228586038934,\
    				'Run2016E': 0.9172251497168261, 'Run2016F': 0.9866513309729763, \
    				'Run2016G': 1.0051360517782837, 'Run2016B': 0.9089157247376515, \
    				'Run2016C': 0.9037296677386634, 'Summer16': 0.744690871542444, \
    				'Run2017F': 0.8834783199828424, 'Run2018D': 0.9343114197729864, \
    				'Run2017D': 0.8871578228655626, 'Run2017C': 0.8824631824088149, \
    				'Run2017B': 0.7753458186951745, 'Run2018A': 0.8748729581145911, \
    				'Run2018C': 0.9106488664283063, 'Run2017E': 0.8455468376019104}
    
    correction_value = 1.0
    for label in correction_values:
        if label in filename:
            correction_value = correction_values[label]
    return correction_value * dedx


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


def check_exo_tag(event, track, iCand, h_cutflow_exo):

    # Disappearing track tag from EXO-19-010 search ("EXO tag"):
    
    score = 0
    h_cutflow_exo.Fill(score)
    
    if abs(track.Eta()) < 2.1                                          : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    if not (abs(track.Eta()) > 0.15 and abs(track.Eta()) < 0.35)       : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    if not (abs(track.Eta()) > 1.42 and abs(track.Eta()) < 1.65)       : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    if not (abs(track.Eta()) > 1.55 and abs(track.Eta()) < 1.85)       : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    if event.tracks_nValidPixelHits[iCand] >= 3                        : score+=1; h_cutflow_exo.Fill(score)        # change from 4 to 3
    else: return score
    if event.tracks_nMissingInnerHits[iCand] == 0                      : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    if event.tracks_nMissingMiddleHits[iCand] == 0                     : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    if event.tracks_trkRelIso[iCand] < 0.05                            : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    if abs(event.tracks_dxyVtx[iCand]) < 0.02                          : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    if abs(event.tracks_dzVtx[iCand]) < 0.5                            : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    
    exo_track_jet_mindeltaR = 9999
    for jet in event.Jets:
        if jet.Pt() > 30 and abs(jet.Eta()) < 4.5:
            deltaR = jet.DeltaR(track)
            if deltaR < exo_track_jet_mindeltaR:
                exo_track_jet_mindeltaR = deltaR
    if exo_track_jet_mindeltaR > 0.5                                   : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    
    if bool(event.tracks_passPFCandVeto[iCand])                        : score+=1; h_cutflow_exo.Fill(score)
    else: return score
        
    pass_iso_electrons = True    
    for i, obj in enumerate(event.Electrons):
        if obj.Pt() > 35 and abs(obj.Eta()) < 2.1 and bool(event.Electrons_tightID[i]):
            if track.DeltaR(obj) < 0.15:
                pass_iso_electrons = False
    if pass_iso_electrons                                              : score+=1; h_cutflow_exo.Fill(score)
    else: return score
        
    pass_iso_muons = True    
    for i, obj in enumerate(event.Muons):
        if obj.Pt() > 35 and abs(obj.Eta()) < 2.1 and bool(event.Muons_tightID[i]):
            if track.DeltaR(obj) < 0.15:
                pass_iso_muons = False
    if pass_iso_muons                                                  : score+=1; h_cutflow_exo.Fill(score)
    else: return score
        
    pass_iso_pions = True    
    for i, obj in enumerate(event.TAPPionTracks):
        if track.DeltaR(obj) < 0.15:
            pass_iso_pions = False
    if pass_iso_pions                                                  : score+=1; h_cutflow_exo.Fill(score)
    else: return score
        
    if event.tracks_matchedCaloEnergy[iCand] < 10                      : score+=1; h_cutflow_exo.Fill(score)
    else: return score
    if event.tracks_nMissingOuterHits[iCand] >= 3                      : score+=1; h_cutflow_exo.Fill(score)
    else: return score    
    if track.Pt() > 55                                                 : score+=1; h_cutflow_exo.Fill(score)
    else: return score


def check_mt2_tag(event, track, iCand, h_cutflow_mt2):
    
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

        score = 100
        h_cutflow_mt2.Fill(score)
        
        if track.Pt() > 15                                             : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if abs(track.Eta()) < 2.4                                      : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if not (abs(track.Eta()) > 1.38 and abs(track.Eta()) < 1.6)    : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if ptErrOverPt2 < 0.2                                          : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if abs(event.tracks_dxyVtx[iCand]) < 0.02                      : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if abs(event.tracks_dzVtx[iCand]) < 0.05                       : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand] < 10                       : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand]/track.Pt() < 0.1           : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand] < 10                       : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand]/track.Pt() < 0.2           : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_pixelLayersWithMeasurement[iCand] >= 3         : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_nMissingInnerHits[iCand] == 0                  : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_nMissingOuterHits[iCand] >= 2                  : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if bool(event.tracks_passPFCandVeto[iCand])                    : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if pass_mt2_pass_iso                                           : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if pass_mt2_pass_track_iso                                     : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        
    elif event.tracks_trackerLayersWithMeasurement[iCand] < 7:
        
        score = 200
        h_cutflow_mt2.Fill(score)
        
        if track.Pt() > 15                                             : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if abs(track.Eta()) < 2.4                                      : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if not (abs(track.Eta()) > 1.38 and abs(track.Eta()) < 1.6)    : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if ptErrOverPt2 < 0.02                                         : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if abs(event.tracks_dxyVtx[iCand]) < 0.01                      : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if abs(event.tracks_dzVtx[iCand]) < 0.05                       : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand] < 10                       : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand]/track.Pt() < 0.1           : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand] < 10                       : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand]/track.Pt() < 0.2           : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_pixelLayersWithMeasurement[iCand] >= 2         : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_nMissingInnerHits[iCand] == 0                  : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_nMissingOuterHits[iCand] >= 2                  : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if bool(event.tracks_passPFCandVeto[iCand])                    : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if pass_mt2_pass_iso                                           : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if pass_mt2_pass_track_iso                                     : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        
    elif event.tracks_trackerLayersWithMeasurement[iCand] >= 7:
        
        score = 300
        h_cutflow_mt2.Fill(score)
        
        if track.Pt() > 15                                             : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if abs(track.Eta()) < 2.4                                      : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if not (abs(track.Eta()) > 1.38 and abs(track.Eta()) < 1.6)    : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if ptErrOverPt2 < 0.005                                        : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if abs(event.tracks_dxyVtx[iCand]) < 0.01                      : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if abs(event.tracks_dzVtx[iCand]) < 0.05                       : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand] < 10                       : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_neutralPtSum[iCand]/track.Pt() < 0.1           : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand] < 10                       : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_chargedPtSum[iCand]/track.Pt() < 0.2           : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_pixelLayersWithMeasurement[iCand] >= 2         : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_nMissingInnerHits[iCand] == 0                  : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if event.tracks_nMissingOuterHits[iCand] >= 2                  : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if bool(event.tracks_passPFCandVeto[iCand])                    : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if pass_mt2_pass_iso                                           : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if ((track.Pt()<150 and event.MT2>100) or track.Pt()>150)      : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
        if pass_mt2_pass_track_iso                                     : score+=1; h_cutflow_mt2.Fill(score)
        else: return score
                
    else:
        return 0
        

def get_BDT_score(label, event, iCand, readers, is_pixel_track, ptErrOverPt2, sideband = False):
    
    if is_pixel_track:
        category = "short"
    else:
        category = "long"
    
    for var in readers[label + "_" + category]["tmva_variables"]:
        
        if sideband and "matchedCaloEnergy" in var:
            readers[label + "_" + category]["tmva_variables"][var][0] = 0
        elif "ptErrOverPt2" in var:
            readers[label + "_" + category]["tmva_variables"][var][0] = ptErrOverPt2
        elif "tracks_" in var:
            readers[label + "_" + category]["tmva_variables"][var][0] = eval("event.%s[%s]" % (var, iCand))
        else:
            readers[label + "_" + category]["tmva_variables"][var][0] = eval("event.tracks_%s[%s]" % (var, iCand))
    
    return readers[label + "_" + category]["reader"].EvaluateMVA("BDT")
        

def main(event_tree_filenames, track_tree_output, nevents = -1, treename = "TreeMaker2/PreSelection", only_tagged_events = False, save_cleaned_variables = True, only_json = False, fakerate_filename = "", overwrite = False):

    print "Input:  %s" % event_tree_filenames
    print "Output: %s" % track_tree_output
    print "n_ev:   %s" % nevents

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    # check if output file exists:
    if not overwrite and os.path.exists(track_tree_output):
        print "Already done, do file check"
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

    if "_chi" in event_tree_filenames[0] or "SMS-" in event_tree_filenames[0]:
        is_signal = True

    print "Signal:", is_signal
    print "Phase:", phase

    fMask = TFile('../../disappearing-track-tag/Masks_mcal10to15.root')
    hMask = fMask.Get('h_Mask_allyearsLongSElValidationZLLCaloSideband_EtaVsPhiDT')

    # load tree
    tree = TChain(treename)
    for iFile in event_tree_filenames:
        if not "root.mimes" in iFile:
            tree.Add(iFile)
   
    if not only_json:
        fout = TFile(track_tree_output, "recreate")

    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_cutflow_exo = TH1F("cutflow_exo", "cutflow_exo", 20, 0, 20)
    h_cutflow_mt2 = TH1F("cutflow_mt2", "cutflow_mt2", 400, 0, 400)

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

    tags = {
        "SR_short": "",
        "SR_long": "",
        "SREC_short": "",
        "SREC_long": "",
        "CR_short": "",
        "CR_long": "",
        "SR2_short": "",
        "SR2_long": "",
        "SREC2_short": "",
        "SREC2_long": "",
        "CR2_short": "",
        "CR2_long": "",
        "SR3_short": "",
        "SR3_long": "",
        "SREC3_short": "",
        "SREC3_long": "",
        "CR3_short": "",
        "CR3_long": "",
           }

    # load BDTs and fetch list of DT tag labels
    bdts = {
        "tight": {
                    "short": ["../../disappearing-track-tag/2016-short-tracks/weights/TMVAClassification_BDT.weights.xml",                         ["dxyVtx", "dzVtx", "matchedCaloEnergy", "trkRelIso", "nValidPixelHits", "nValidTrackerHits", "ptErrOverPt2"] ],
                    "long":  ["../../disappearing-track-tag/2016-long-tracks/weights/TMVAClassification_BDT.weights.xml",                          ["dxyVtx", "dzVtx", "matchedCaloEnergy", "trkRelIso", "nValidPixelHits", "nValidTrackerHits", "nMissingOuterHits", "ptErrOverPt2"] ],          
                 },                                                                                                                                
        "loose": {                                                                                                                                 
                    "short": ["../../disappearing-track-tag/2016-short-tracks-loose/weights/TMVAClassification_BDT.weights.xml",                   ["dzVtx", "matchedCaloEnergy", "trkRelIso", "nValidPixelHits", "nValidTrackerHits", "ptErrOverPt2"] ],
                    "long":  ["../../disappearing-track-tag/2016-long-tracks-loose/weights/TMVAClassification_BDT.weights.xml",                    ["dzVtx", "matchedCaloEnergy", "trkRelIso", "nValidPixelHits", "nValidTrackerHits", "nMissingOuterHits", "ptErrOverPt2"] ],          
                 },                                                                             
        "tight_may20": {                                                                       
                    "short": ["../../disappearing-track-tag/2016-short-tracks-may20-dxy/dataset/weights/TMVAClassification_BDT.weights.xml",       ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2"] ],
                    "long":  ["../../disappearing-track-tag/2016-long-tracks-may20-dxy/dataset/weights/TMVAClassification_BDT.weights.xml",        ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2"] ],          
                 },                                                                             
        "loose_may20": {                                                                       
                    "short": ["../../disappearing-track-tag/2016-short-tracks-may20/dataset/weights/TMVAClassification_BDT.weights.xml",           ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2"] ],
                    "long":  ["../../disappearing-track-tag/2016-long-tracks-may20/dataset/weights/TMVAClassification_BDT.weights.xml",            ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2"] ],          
                 },
        "tight_may20_chi2": {
                    "short": ["../../disappearing-track-tag/2016-short-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                    "long":  ["../../disappearing-track-tag/2016-long-tracks-may20-dxy-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",   ["tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                 },
        "loose_may20_chi2": {
                    "short": ["../../disappearing-track-tag/2016-short-tracks-may20-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",      ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                    "long":  ["../../disappearing-track-tag/2016-long-tracks-may20-chi2/dataset/weights/TMVAClassification_BDT.weights.xml",       ["tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
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
                readers[label + "_" + category]["reader"].BookMVA("BDT", bdts[label][category][0])
            else:    
                readers[label + "_" + category]["reader"].BookMVA("BDT", bdts[label][category][0].replace("2016", "2017"))
    
    tout = TTree("Events", "tout")

    # prepare variables for output tree   
    float_branches = ["weight", "MET", "MHT", "HT", "MinDeltaPhiMhtJets", "PFCaloMETRatio", "dilepton_invmass", "event", "run", "lumisec", "chargino_parent_mass", "region", "region_sideband", "regionCorrected", "regionCorrected_sideband", "signal_gluino_mass", "signal_lsp_mass", "leadinglepton_pt", "leadinglepton_mt", "leadinglepton_eta", "leadinglepton_phi", "leadinglepton_charge", "leadinglepton_dedx", "leadinglepton_dedxCorrected"]
    integer_branches = ["n_jets", "n_goodjets", "n_btags", "n_leptons", "n_goodleptons", "n_goodelectrons", "n_goodmuons", "n_allvertices", "n_NVtx", "dilepton_leptontype",  "n_genLeptons", "n_genElectrons", "n_genMuons", "n_genTaus", "triggered_met", "triggered_singleelectron", "triggered_singlemuon", "triggered_ht", "leadinglepton_id"]

    for tag in tags:
        integer_branches.append("n_tracks_%s" % tag)

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

    vector_int_branches = ['tracks_is_pixel_track', 'tracks_pixelLayersWithMeasurement', 'tracks_trackerLayersWithMeasurement', 'tracks_nMissingInnerHits', 'tracks_nMissingMiddleHits', 'tracks_nMissingOuterHits', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_fake', 'tracks_prompt_electron', 'tracks_prompt_muon', 'tracks_prompt_tau', 'tracks_prompt_tau_widecone', 'tracks_prompt_tau_leadtrk', 'tracks_prompt_tau_hadronic', 'tracks_pass_reco_lepton', 'tracks_passPFCandVeto', 'tracks_charge', 'leptons_id', 'tracks_passpionveto', 'tracks_passjetveto', 'tracks_basecuts', 'tracks_baseline', 'tracks_passmask', 'tracks_highpurity', 'tracks_region', 'tracks_passexotag', 'tracks_passmt2tag']

    for tag in tags:
        vector_int_branches += ["tracks_%s" % tag]
    
    for branch in vector_int_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<int>', tree_branch_values[branch])

    vector_float_branches = ['tracks_dxyVtx', 'tracks_dzVtx', 'tracks_matchedCaloEnergy', 'tracks_trkRelIso', 'tracks_ptErrOverPt2', 'tracks_pt', 'tracks_eta', 'tracks_phi', 'tracks_trkMiniRelIso', 'tracks_trackJetIso', 'tracks_ptError', 'tracks_neutralPtSum', 'tracks_neutralWithoutGammaPtSum', 'tracks_minDrLepton', 'tracks_matchedCaloEnergyJets', 'tracks_deDxHarmonic2pixel', 'tracks_deDxHarmonic2pixelCorrected', 'tracks_deDxHarmonic2strips', 'tracks_massfromdeDxPixel', 'tracks_massfromdeDxStrips', 'tracks_chi2perNdof', 'tracks_chargedPtSum', 'tracks_chiCandGenMatchingDR', 'tracks_mt', 'tracks_invmass', 'leptons_pt', 'leptons_iso', 'leptons_mt', 'leptons_eta', 'leptons_charge', 'leptons_phi', 'leptons_dedx', 'leptons_dedxCorrected']

    for label in bdts:
        vector_float_branches += ["tracks_mva_%s" % label]
        vector_float_branches += ["tracks_mva_%s_sideband" % label]

    for branch in vector_float_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<double>', tree_branch_values[branch])
            
    print "Looping over %s events" % nev

    for iEv, event in enumerate(tree):
                  
        if nevents > 0 and iEv > nevents: break      
        if (iEv+1) % 10000 == 0:
            print "event %s / %s" % (iEv + 1, nev)

        # calculate weight and collect lumisections:
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

        if only_json:
            continue

        current_file_name = tree.GetFile().GetName()

        # reset all branch values:
        for label in tree_branch_values:
            if "tracks_" in label or "leptons_" in label:
                continue
            tree_branch_values[label][0] = -1

        if is_signal:
            # output gluino mass histogram:
            signal_gluino_mass = -1
            signal_lsp_mass = -1
            for i_genParticle, genParticle in enumerate(event.GenParticles):
                if abs(event.GenParticles_PdgId[i_genParticle]) == 1000021:
                    signal_gluino_mass = round(genParticle.M())
                elif abs(event.GenParticles_PdgId[i_genParticle]) == 1000022:
                    signal_lsp_mass = round(genParticle.M())
        
        # basic event selection:
        if not is_data and not shared_utils.passesUniversalSelection(event):
            continue
        if is_data and not shared_utils.passesUniversalDataSelection(event):
            continue

        # check trigger:
        triggered_met = shared_utils.PassTrig(event, 'MhtMet6pack')
        triggered_singleelectron = shared_utils.PassTrig(event, 'SingleElectron')
        triggered_singlemuon = shared_utils.PassTrig(event, 'SingleMuon')
        triggered_ht = shared_utils.PassTrig(event, 'HtTrain')

        # count number of good leptons:
        lepton_level_output = []
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
                                
                lepton_level_output.append({"leptons_pt": electron.Pt(),
                                            "leptons_eta": electron.Eta(),
                                            "leptons_mt": event.Electrons_MTW[i],
                                            "leptons_phi": electron.Phi(),
                                            "leptons_iso": bool(event.Electrons_passIso[i]),
                                            "leptons_charge": event.Electrons_charge[i],
                                            "leptons_dedx": matched_dedx,
                                            "leptons_dedxCorrected": correct_dedx_intercalibration(matched_dedx, current_file_name),
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
                
                lepton_level_output.append({"leptons_pt": muon.Pt(),
                                            "leptons_eta": muon.Eta(),
                                            "leptons_mt": event.Muons_MTW[i],
                                            "leptons_phi": muon.Phi(),
                                            "leptons_iso": bool(event.Muons_passIso[i]),
                                            "leptons_charge": event.Muons_charge[i],
                                            "leptons_dedx": matched_dedx,
                                            "leptons_dedxCorrected": correct_dedx_intercalibration(matched_dedx, current_file_name),
                                            "leptons_id": 13,
                                            })

        n_goodleptons = n_goodelectrons + n_goodmuons
               
        # save lepton properties vector:
        dilepton_invariant_mass = 0
        dilepton_leptontype = 0
        if n_goodleptons > 0:
            highest_lepton_pt = 0
            highest_lepton_index = 0
            for i, lepton_output_dict in enumerate(lepton_level_output):
                for label in lepton_output_dict:
                    #tree_branch_values[label][i] = lepton_output_dict[label]
                    if lepton_output_dict["leptons_pt"] > highest_lepton_pt:
                        highest_lepton_pt = lepton_output_dict["leptons_pt"]
                        highest_lepton_index = i
                
            # save leading lepton:
            tree_branch_values["leadinglepton_pt"][0] = lepton_level_output[highest_lepton_index]["leptons_pt"]
            tree_branch_values["leadinglepton_mt"][0] = lepton_level_output[highest_lepton_index]["leptons_mt"]
            tree_branch_values["leadinglepton_eta"][0] = lepton_level_output[highest_lepton_index]["leptons_eta"]
            tree_branch_values["leadinglepton_charge"][0] = lepton_level_output[highest_lepton_index]["leptons_charge"]
            tree_branch_values["leadinglepton_phi"][0] = lepton_level_output[highest_lepton_index]["leptons_phi"]
            tree_branch_values["leadinglepton_dedx"][0] = lepton_level_output[highest_lepton_index]["leptons_dedx"]
            tree_branch_values["leadinglepton_dedxCorrected"][0] = lepton_level_output[highest_lepton_index]["leptons_dedxCorrected"]
            tree_branch_values["leadinglepton_id"][0] = lepton_level_output[highest_lepton_index]["leptons_id"]

            # find a matching lepton within the z peak:
            if n_goodleptons > 1:
                dilepton_mass = 0                
                for i, lepton_output_dict in enumerate(lepton_level_output):
                    if i == highest_lepton_index:
                        continue
                    if lepton_output_dict["leptons_id"] == lepton_level_output[highest_lepton_index]["leptons_id"]:
                        if lepton_output_dict["leptons_charge"] != lepton_level_output[highest_lepton_index]["leptons_charge"]:
                            if lepton_output_dict["leptons_iso"] and lepton_level_output[highest_lepton_index]["leptons_iso"]:
                                i_invmass = (goodleptons[i] + goodleptons[highest_lepton_index]).M()
                                if abs(i_invmass-91) < abs(dilepton_mass-91):
                                    dilepton_mass = i_invmass
            
                dilepton_invariant_mass = dilepton_mass
                dilepton_leptontype = lepton_level_output[highest_lepton_index]["leptons_id"]

        if save_cleaned_variables and dilepton_invariant_mass>0:
        
            # recalculate HT, MHT, n_Jets without the two leptons:
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
        goodjets = []
        for jet in event.Jets:
            if jet.Pt() > 30 and abs(jet.Eta()) < 2.4:
                for lepton in list(event.Muons) + list(event.Electrons):
                    if jet.DeltaR(lepton) < 0.5:
                        continue
                n_goodjets += 1
                goodjets.append(jet)
        event.n_goodjets = n_goodjets

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
        event.MinDeltaPhiMhtJets = MinDeltaPhiMhtJets

        mva_scores = {}

        ## reset tagged tracks counter to zero:
        for tag in tags:
            tree_branch_values["n_tracks_%s" % tag][0] = 0
     
        # for each event, first fill this list for each track         
        tagged_tracks = []

        for iCand, track in enumerate(event.tracks):

            #pass_exo_tag = check_exo_tag(event, track, iCand, h_cutflow_exo)
            #pass_mt2_tag = check_mt2_tag(event, track, iCand, h_cutflow_mt2)
            #            
            #if not pass_exo_tag:
            #    pass_exo_tag = 0
            #if not pass_mt2_tag:
            #    pass_mt2_tag = 0
             
            pass_exo_tag = 0
            pass_mt2_tag = 0
                        
            # basic track selection:
            if track.Pt() < 30:
                continue

            # check for nearby pions:
            passpionveto = True
            for k in range(len(event.TAPPionTracks)):
                if event.tracks[iCand].DeltaR(event.TAPPionTracks[k]) < 0.1:
                    passpionveto = False
                    break

            # veto DTs too close to jets
            track_jet_mindeltaR = 9999
            for jet in goodjets:
                deltaR = jet.DeltaR(track)
                if deltaR < track_jet_mindeltaR:
                    track_jet_mindeltaR = deltaR
            if track_jet_mindeltaR < 0.4:
                passjetveto = False
            else:
                passjetveto = True
            
            passrecolepton = True
            for lepton in goodleptons:
                if track.DeltaR(lepton) < 0.1:
                    passrecolepton = False

            ptErrOverPt2 = event.tracks_ptError[iCand] / (track.Pt()**2)

            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            elif event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = False

            #base_cuts = shared_utils.isBaselineTrack(track, iCand, event, hMask) and passrecolepton and bool(event.tracks_passPFCandVeto[iCand]) and event.tracks_nValidPixelHits[iCand]>=2 and passpionveto and passjetveto
            #base_cuts =  passrecolepton and bool(event.tracks_passPFCandVeto[iCand]) and event.tracks_nValidPixelHits[iCand]>=2 and passpionveto and passjetveto

            base_cuts = abs(track.Eta())<2.4 and \
                        bool(event.tracks_trackQualityHighPurity[iCand]) and \
                        ptErrOverPt2<10 and \
                        event.tracks_dzVtx[iCand]<0.1 and \
                        event.tracks_trkRelIso[iCand]<0.2 and \
                        event.tracks_trackerLayersWithMeasurement[iCand]>=2 and \
                        event.tracks_nValidTrackerHits[iCand]>=2 and \
                        event.tracks_nMissingInnerHits[iCand]==0 and \
                        event.tracks_nValidPixelHits[iCand]>=2 and \
                        bool(event.tracks_passPFCandVeto[iCand]) and \
                        passrecolepton
            
            if not is_pixel_track:
                base_cuts = base_cuts and event.tracks_nMissingOuterHits[iCand]>=2 
            
            # keep only baseline tracks:
            if not base_cuts:
                continue

            #pass_baseline = shared_utils.isBaselineTrack(track, iCand, event, hMask)
            pass_mask = True
            if hMask!='':
        		xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
        		ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
        		if hMask.GetBinContent(ibinx, ibiny)==0: 
        			pass_mask = False
                    
            for label in bdts:
                mva_scores[label] = get_BDT_score(label, event, iCand, readers, is_pixel_track, ptErrOverPt2)
                mva_scores[label + "_sideband"] = get_BDT_score(label, event, iCand, readers, is_pixel_track, ptErrOverPt2, sideband = True)
                                      
            tags["SR_short"] = base_cuts and is_pixel_track and mva_scores["loose"]>(event.tracks_dxyVtx[iCand]*(0.65/0.01) - 0.5) and event.tracks_trkRelIso[iCand]<0.01
            tags["SR_long"] = base_cuts and not is_pixel_track and mva_scores["loose"]>(event.tracks_dxyVtx[iCand]*(0.7/0.01) - 0.05) and event.tracks_trkRelIso[iCand]<0.01
            tags["SR2_short"] = base_cuts and is_pixel_track and mva_scores["loose_may20_chi2"]>-0.05 and event.tracks_dxyVtx[iCand]<0.02 and event.tracks_trkRelIso[iCand]<0.01
            tags["SR2_long"] = base_cuts and not is_pixel_track and mva_scores["loose_may20_chi2"]>-0.15 and event.tracks_dxyVtx[iCand]<0.02 and event.tracks_trkRelIso[iCand]<0.01
            tags["SR3_short"] = base_cuts and is_pixel_track and mva_scores["loose_may20_chi2"]>(event.tracks_dxyVtx[iCand]*(0.65/0.01) - 0.5) and event.tracks_trkRelIso[iCand]<0.01
            tags["SR3_long"] = base_cuts and not is_pixel_track and mva_scores["loose_may20_chi2"]>(event.tracks_dxyVtx[iCand]*(0.7/0.01) - 0.05) and event.tracks_trkRelIso[iCand]<0.01

            tags["SREC_short"] = base_cuts and is_pixel_track and mva_scores["loose_sideband"]>(event.tracks_dxyVtx[iCand]*(0.65/0.01) - 0.5) and event.tracks_trkRelIso[iCand]<0.01
            tags["SREC_long"] = base_cuts and not is_pixel_track and mva_scores["loose_sideband"]>(event.tracks_dxyVtx[iCand]*(0.7/0.01) - 0.05) and event.tracks_trkRelIso[iCand]<0.01
            tags["SREC2_short"] = base_cuts and is_pixel_track and mva_scores["loose_may20_chi2_sideband"]>-0.05 and event.tracks_dxyVtx[iCand]<0.02 and event.tracks_trkRelIso[iCand]<0.01
            tags["SREC2_long"] = base_cuts and not is_pixel_track and mva_scores["loose_may20_chi2_sideband"]>-0.15 and event.tracks_dxyVtx[iCand]<0.02 and event.tracks_trkRelIso[iCand]<0.01
            tags["SREC3_short"] = base_cuts and is_pixel_track and mva_scores["loose_may20_chi2_sideband"]>(event.tracks_dxyVtx[iCand]*(0.65/0.01) - 0.5) and event.tracks_trkRelIso[iCand]<0.01
            tags["SREC3_long"] = base_cuts and not is_pixel_track and mva_scores["loose_may20_chi2_sideband"]>(event.tracks_dxyVtx[iCand]*(0.7/0.01) - 0.05) and event.tracks_trkRelIso[iCand]<0.01
            
            tags["CR_short"] = base_cuts and is_pixel_track and event.tracks_dxyVtx[iCand]>0.02
            tags["CR_long"] = base_cuts and not is_pixel_track and event.tracks_dxyVtx[iCand]>0.02
            tags["CR2_short"] = base_cuts and is_pixel_track and event.tracks_dxyVtx[iCand]>0.02
            tags["CR2_long"] = base_cuts and not is_pixel_track and event.tracks_dxyVtx[iCand]>0.02
            tags["CR3_short"] = base_cuts and is_pixel_track and event.tracks_dxyVtx[iCand]>0.02
            tags["CR3_long"] = base_cuts and not is_pixel_track and event.tracks_dxyVtx[iCand]>0.02
            
            #track_is_tagged = False
            #for label in tags:
            #    if tags[label]: track_is_tagged = True
            #if not track_is_tagged:
            #    continue
            
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
                if event.tracks_charge[iCand] * lepton_level_output[highest_lepton_index]["leptons_charge"] == -1:
                    invariant_mass = (track + goodleptons[highest_lepton_index]).M()
                else:
                    invariant_mass = -1
            else:
                invariant_mass = -1

            # if signal, do chargino matching:
            chiCandGenMatchingDR = 100
            if is_signal:
                min_deltaR = 100
                for k in range(len(event.GenParticles)):
                    if abs(event.GenParticles_PdgId[k]) == 1000024:
                        deltaR = track.DeltaR(event.GenParticles[k])
                        if deltaR < min_deltaR:
                            chiCandGenMatchingDR = deltaR
            
            #if tags["SR_short"] or tags["SR_long"]:
                #print "iEv, iCand, SR_short, SR_long", iEv, iCand, tags["SR_short"], tags["SR_long"]
                #print "  \_tags", tags
                #print "  \_is_pixel_track", is_pixel_track
                #print "  \_mva_tight, mva_loose", mva_tight, mva_loose
                #print "  \_is_fake_track", is_fake_track
                #print "  \_weight = event.puWeight * event.CrossSection =", weight

            DeDxCorrected = correct_dedx_intercalibration(event.tracks_deDxHarmonic2pixel[iCand], current_file_name)
            current_region = get_signal_region(event.HT, event.MHT, n_goodjets, event.BTags, MinDeltaPhiMhtJets, 1, is_pixel_track, DeDxCorrected, n_goodelectrons, n_goodmuons, event_tree_filenames[0])
            
            tagged_tracks.append(
                                   {
                                     "tracks_is_pixel_track": is_pixel_track,
                                     "tracks_pixelLayersWithMeasurement": event.tracks_pixelLayersWithMeasurement[iCand],
                                     "tracks_trackerLayersWithMeasurement": event.tracks_trackerLayersWithMeasurement[iCand],
                                     "tracks_fake": is_fake_track,
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
                                     "tracks_prompt_electron": is_prompt_electron,
                                     "tracks_prompt_muon": is_prompt_muon,
                                     "tracks_prompt_tau": is_prompt_tau,
                                     "tracks_prompt_tau_hadronic": is_prompt_tau_hadronic,
                                     "tracks_prompt_tau_leadtrk": is_prompt_tau_leadtrk,
                                     "tracks_prompt_tau_widecone": is_prompt_tau_widecone,
                                     "tracks_pass_reco_lepton": passrecolepton,
                                     "tracks_trkMiniRelIso": event.tracks_trkMiniRelIso[iCand],
                                     "tracks_trackJetIso": track_jet_mindeltaR,
                                     "tracks_ptError": event.tracks_ptError[iCand],
                                     "tracks_passPFCandVeto": bool(event.tracks_passPFCandVeto[iCand]),
                                     "tracks_neutralPtSum": event.tracks_neutralPtSum[iCand],
                                     "tracks_neutralWithoutGammaPtSum": event.tracks_neutralWithoutGammaPtSum[iCand],
                                     "tracks_minDrLepton": event.tracks_minDrLepton[iCand],
                                     "tracks_matchedCaloEnergyJets": event.tracks_matchedCaloEnergyJets[iCand],
                                     "tracks_deDxHarmonic2pixel": event.tracks_deDxHarmonic2pixel[iCand],
                                     "tracks_deDxHarmonic2pixelCorrected": DeDxCorrected,
                                     "tracks_deDxHarmonic2strips": event.tracks_deDxHarmonic2strips[iCand],
                                     "tracks_massfromdeDxPixel": tracks_massfromdeDxPixel,
                                     "tracks_massfromdeDxStrips": tracks_massfromdeDxStrips,
                                     "tracks_chi2perNdof": event.tracks_chi2perNdof[iCand],
                                     "tracks_mt": event.tracks[iCand].Mt(),
                                     "tracks_chargedPtSum": event.tracks_chargedPtSum[iCand],
                                     "tracks_charge": event.tracks_charge[iCand],
                                     "tracks_invmass": invariant_mass,
                                     "tracks_chiCandGenMatchingDR": chiCandGenMatchingDR,
                                     "tracks_passpionveto": passpionveto,
                                     "tracks_passjetveto": passjetveto,
                                     "tracks_basecuts": base_cuts,
                                     "tracks_passexotag": pass_exo_tag,
                                     "tracks_passmt2tag": pass_mt2_tag,
                                     #"tracks_baseline": pass_baseline,
                                     "tracks_passmask": pass_mask,
                                     "tracks_highpurity": bool(event.tracks_trackQualityHighPurity[iCand]),
                                     "tracks_region": current_region,
                                   }
                                  )
                                       
            for tag in tags:
               tagged_tracks[-1]["tracks_%s" % tag] = tags[tag]

            for label in mva_scores:
                tagged_tracks[-1]["tracks_mva_%s" % label] = mva_scores[label]
                
            tagged_tracks[-1]["object"] = track
  
        # FIXME: keep only events with candidate tracks
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
            if not jet.Pt()>30: continue            
            if not abs(jet.Eta())<5.0: continue
            someoverlap = False
            for dt in tagged_tracks:
                if dt["tracks_SR_short"]+dt["tracks_SR_long"]>0: 
                    if jet.DeltaR(dt["object"])<0.4: 
                        someoverlap = True
                        break
            if someoverlap: continue
            adjustedMht-=jet        
            if not abs(jet.Eta())<2.4: continue
            adjustedJets.append(jet)            
            if event.Jets_bJetTagDeepCSVBvsAll[ijet]>btag_cut: adjustedBTags+=1 ####hellooo
            adjustedHt+=jet.Pt()
        adjustedNJets = len(adjustedJets)
        mindphi = 4
        for jet in adjustedJets: mindphi = min(mindphi, abs(jet.DeltaPhi(adjustedMht))) 
            
        # update variables:
        event.BTags = adjustedBTags
        n_goodjets = adjustedNJets
        event.HT = adjustedHt
        event.MHT = adjustedMht.Pt()
        MinDeltaPhiMhtJets = mindphi
        
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
                    

        # save region number depending on track tag:
        n_DT_SR = 0
        DeDxAverage_SR = -1
        DeDxAverageCorrected_SR = -1
        is_pixel_track_SR = False
        for tag in tags:
            n_DT = 0
            for tagged_track in tagged_tracks:
                if tagged_track["tracks_%s" % tag] == 1:
                    n_DT += 1
                    if "SR" in tag:
                        n_DT_SR += 1
                        DeDxAverage_SR = tagged_track["tracks_deDxHarmonic2pixel"]
                        DeDxAverageCorrected_SR = correct_dedx_intercalibration(tagged_track["tracks_deDxHarmonic2pixel"], current_file_name)
                        is_pixel_track_SR = tagged_track["tracks_is_pixel_track"]
        
            tree_branch_values["n_tracks_%s" % tag][0] = n_DT
        
        region = get_signal_region(event.HT, event.MHT, n_goodjets, event.BTags, MinDeltaPhiMhtJets, n_DT_SR, is_pixel_track_SR, DeDxAverage_SR, n_goodelectrons, n_goodmuons, event_tree_filenames[0])
        region_sideband = get_signal_region(event.HT, event.MHT, n_goodjets, event.BTags, MinDeltaPhiMhtJets, n_DT_SR, is_pixel_track_SR, DeDxAverage_SR, n_goodelectrons, n_goodmuons, event_tree_filenames[0], sideband = True)
        
        regionCorrected = get_signal_region(event.HT, event.MHT, n_goodjets, event.BTags, MinDeltaPhiMhtJets, n_DT_SR, is_pixel_track_SR, DeDxAverageCorrected_SR, n_goodelectrons, n_goodmuons, event_tree_filenames[0])
        regionCorrected_sideband = get_signal_region(event.HT, event.MHT, n_goodjets, event.BTags, MinDeltaPhiMhtJets, n_DT_SR, is_pixel_track_SR, DeDxAverageCorrected_SR, n_goodelectrons, n_goodmuons, event_tree_filenames[0], sideband = True)

        # save event-level variables:
        try:
            tree_branch_values["run"][0] = event.RunNum
            tree_branch_values["lumisec"][0] = event.LumiBlockNum
        except:
            print "Error while saving event number info"
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
        tree_branch_values["triggered_met"][0] = triggered_met
        tree_branch_values["triggered_singleelectron"][0] = triggered_singleelectron
        tree_branch_values["triggered_singlemuon"][0] = triggered_singlemuon
        tree_branch_values["triggered_ht"][0] = triggered_ht
        tree_branch_values["dilepton_invmass"][0] = dilepton_invariant_mass
        tree_branch_values["dilepton_leptontype"][0] = dilepton_leptontype
        tree_branch_values["region"][0] = region
        tree_branch_values["regionCorrected"][0] = regionCorrected
        tree_branch_values["region_sideband"][0] = region_sideband
        tree_branch_values["regionCorrected_sideband"][0] = regionCorrected_sideband
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

        if n_goodleptons > 0:
            for i, lepton_output_dict in enumerate(lepton_level_output):
                for label in lepton_output_dict:
                    tree_branch_values[label][i] = lepton_output_dict[label]

        tout.Fill()
    
    h_cutflow_exo.Write()
    h_cutflow_mt2.Write()
                         
    if not only_json:
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
    parser.add_option("--overwrite", dest = "overwrite", action = "store_true")
    (options, args) = parser.parse_args()
    
    options.inputfiles = options.inputfiles.split(",")
       
    main(
         options.inputfiles,
         options.outputfiles,
         nevents = int(options.nev),
         overwrite = options.overwrite,
        )

