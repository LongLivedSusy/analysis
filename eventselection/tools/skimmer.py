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
    
    correction_values = shared_utils.datacalibdict
    correction_value = 1.0
    for label in correction_values:
        if label in filename:
            correction_value = correction_values[label]
    return correction_value * dedx


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
    

def get_disappearing_track_score(label, event, iCand, readers):

    # check TMVA preselection and evaluate BDT score
    if event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
        category = "long"
        is_pixel_track = False
    else:
        category = "short"
        is_pixel_track = True

    if label == "looseloose":
        use_dxy = False
        use_dz = False
        bdt = readers["bdt_looseloose-%s" % category]
    elif label == "loose":
        use_dxy = False
        use_dz = True
        bdt = readers["bdt_loose-%s" % category]
    elif label == "tight":
        use_dxy = True
        use_dz = True
        bdt = readers["bdt-%s" % category]
    else:
        print "no BDT found"
        return -10
                  
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
    if not is_pixel_track:
        bdt["tmva_variables"]["nMissingOuterHits"][0] = event.tracks_nMissingOuterHits[iCand]
    bdt["tmva_variables"]["ptErrOverPt2"][0] = ptErrOverPt2           
    
    score = bdt["reader"].EvaluateMVA("BDT")
    
    return score
    

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


def main(event_tree_filenames, track_tree_output, nevents = -1, treename = "TreeMaker2/PreSelection", only_tagged_events = False, save_cleaned_variables = False, only_json = False, check_file_exists = True, mask_file_name = "", fakerate_filename = ""):

    print "Input:  %s" % event_tree_filenames
    print "Output: %s" % track_tree_output
    print "n_ev:   %s" % nevents

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    # check if output file exists:
    if check_file_exists and os.path.exists(track_tree_output):
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

    if mask_file_name:
        print "Loaded mask histograms: %s" % mask_file_name
    if fakerate_filename:
        print "Loaded fakerate histograms: %s" % fakerate_filename

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

    # load and configure data mask:
    if mask_file_name and phase == 0:
        mask_file = TFile(mask_file_name, "open")
        if is_data:
            h_mask = mask_file.Get("hEtaVsPhiDT_maskData-2016Data-2016")
        else:
            h_mask = mask_file.Get("hEtaVsPhiDT_maskMC-2016MC-2016")
        h_mask.SetDirectory(0)
        mask_file.Close()
        print "Loaded mask:", h_mask
    else:
        h_mask = ""

    ## load fakerate histograms:
    #h_fakerate = {}
    #fakerate_variables = [
    #             "HT",
    #             "n_goodjets",
    #             "n_allvertices",
    #             "n_btags",
    #             "MinDeltaPhiMhtJets",
    #             "HT:n_allvertices",
    #            ]
    #fakerate_regions = ["FakeRateDet"]
    #    
    #if fakerate_filename:
    #    fakerate_branchlabels = []
    #    tfile_fakerate = TFile(fakerate_filename, "open")
    #    for variable in fakerate_variables:
    #        variable = variable.replace(":", "_")
    #        for region in fakerate_regions:
    #            for fakeratetype in ["fakerate", "fakerateIso"]:
    #                for category in ["short", "long"]:
    #                    label = "%s_%s_%s_%s_%s" % (variable, region, data_period, fakeratetype, category)
    #                    branchlabel = "%s_%s_%s_%s" % (variable, region, fakeratetype, category)
    #                    h_fakerate[label] = tfile_fakerate.Get(label)
    #                    h_fakerate[label].SetDirectory(0)
    #                    fakerate_branchlabels.append(branchlabel)
    #    tfile_fakerate.Close()
                

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
        "CR_short": "",
        "CR_long": "",
           }

    # load BDTs and fetch list of DT tag labels
    readers = load_tmva_readers(phase)

    tout = TTree("Events", "tout")

    # prepare variables for output tree   
    float_branches = ["weight", "MET", "MHT", "HT", "MinDeltaPhiMhtJets", "PFCaloMETRatio", "dilepton_invmass", "event", "run", "lumisec", "chargino_parent_mass", "region", "region_sideband", "regionCorrected", "regionCorrected_sideband", "signal_gluino_mass", "signal_lsp_mass", "leadinglepton_pt", "leadinglepton_mt", "leadinglepton_eta", "leadinglepton_phi", "leadinglepton_charge", "leadinglepton_dedx", "leadinglepton_dedxCorrected"]
    integer_branches = ["n_jets", "n_goodjets", "n_btags", "n_leptons", "n_goodleptons", "n_goodelectrons", "n_goodmuons", "n_allvertices", "n_NVtx", "dilepton_leptontype",  "n_genLeptons", "n_genElectrons", "n_genMuons", "n_genTaus", "triggered_met", "triggered_singleelectron", "triggered_singlemuon", "leadinglepton_id"]

    for tag in tags:
        integer_branches.append("n_tracks_%s" % tag)

    #if fakerate_filename:
    #    for label in fakerate_branchlabels:
    #        float_branches.append("fakerate_%s" % label)

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

    vector_int_branches = ['tracks_is_pixel_track', 'tracks_pixelLayersWithMeasurement', 'tracks_trackerLayersWithMeasurement', 'tracks_nMissingInnerHits', 'tracks_nMissingMiddleHits', 'tracks_nMissingOuterHits', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_fake', 'tracks_prompt_electron', 'tracks_prompt_muon', 'tracks_prompt_tau', 'tracks_prompt_tau_widecone', 'tracks_prompt_tau_leadtrk', 'tracks_prompt_tau_hadronic', 'tracks_pass_reco_lepton', 'tracks_passPFCandVeto', 'tracks_charge', 'leptons_id', 'tracks_passpionveto', 'tracks_passjetveto', 'tracks_basecuts']

    for tag in tags:
        vector_int_branches += ["tracks_%s" % tag]
    
    for branch in vector_int_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<int>', tree_branch_values[branch])

    vector_float_branches = ['tracks_dxyVtx', 'tracks_dzVtx', 'tracks_matchedCaloEnergy', 'tracks_trkRelIso', 'tracks_ptErrOverPt2', 'tracks_pt', 'tracks_eta', 'tracks_phi', 'tracks_trkMiniRelIso', 'tracks_trackJetIso', 'tracks_ptError', 'tracks_neutralPtSum', 'tracks_neutralWithoutGammaPtSum', 'tracks_minDrLepton', 'tracks_matchedCaloEnergyJets', 'tracks_deDxHarmonic2pixel', 'tracks_deDxHarmonic2pixelCorrected', 'tracks_deDxHarmonic2strips', 'tracks_massfromdeDxPixel', 'tracks_massfromdeDxStrips', 'tracks_chi2perNdof', 'tracks_chargedPtSum', 'tracks_chiCandGenMatchingDR', 'tracks_mt', 'tracks_invmass', 'tracks_mva_tight', 'tracks_mva_loose', 'leptons_pt', 'leptons_iso', 'leptons_mt', 'leptons_eta', 'leptons_charge', 'leptons_phi', 'leptons_dedx', 'leptons_dedxCorrected']

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

        # count number of good leptons:
        lepton_level_output = []
        goodleptons = []
        n_goodelectrons = 0
        n_goodmuons = 0
        for i, electron in enumerate(event.Electrons):
            if electron.Pt() > 30 and abs(electron.Eta()) < 2.4 and bool(event.Electrons_tightID[i]):

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
            if muon.Pt() > 30 and abs(muon.Eta()) < 2.4 and bool(event.Muons_tightID[i]):

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
               
        # check z peak:
        dilepton_invariant_mass = -1
        dilepton_leptontype = -1
        if n_goodelectrons==2 and n_goodmuons==0:
            if lepton_level_output[0]["leptons_charge"] * lepton_level_output[1]["leptons_charge"] < 0:
                if lepton_level_output[0]["leptons_iso"] and lepton_level_output[1]["leptons_iso"]:
                    dilepton_invariant_mass = (goodleptons[0] + goodleptons[1]).M()
                    dilepton_leptontype = 11
        elif n_goodelectrons==0 and n_goodmuons==2:
            if lepton_level_output[0]["leptons_charge"] * lepton_level_output[1]["leptons_charge"] < 0:
                if lepton_level_output[0]["leptons_iso"] and lepton_level_output[1]["leptons_iso"]:
                    dilepton_invariant_mass = (goodleptons[0] + goodleptons[1]).M()
                    dilepton_leptontype = 13

        # FIXME: keep only single-electron events or dielectron events:
        if not ( n_goodelectrons==1 or (dilepton_leptontype==11 and dilepton_invariant_mass>71 and dilepton_invariant_mass<111) ):
            continue

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

        ## reset tagged tracks counter to zero:
        for tag in tags:
            tree_branch_values["n_tracks_%s" % tag][0] = 0
     
        # for each event, first fill this list for each track         
        tagged_tracks = []

        for iCand, track in enumerate(event.tracks):

            # basic track selection:
            if track.Pt() < 30 or not shared_utils.isBaselineTrack(track, iCand, event, h_mask):
                continue

            # check for nearby pions:
            passpionveto = True
            for k in range(len(event.TAPPionTracks)):
                if event.tracks[iCand].DeltaR(event.TAPPionTracks[k]) < 0.1:
                    passpionveto = False
                    break

            # veto DTs too close to jets
            track_jet_mindeltaR = 9999
            for jet in event.Jets:
                deltaR = jet.DeltaR(track)
                if deltaR < track_jet_mindeltaR:
                    track_jet_mindeltaR = deltaR
            if track_jet_mindeltaR<0.4:
                passjetveto = False
            else:
                passjetveto = True
            
            passrecolepton = True
            for lepton in list(event.Muons) + list(event.Electrons):
                if track.DeltaR(lepton) < 0.1:
                    passrecolepton = False

            ptErrOverPt2 = event.tracks_ptError[iCand] / (track.Pt()**2)

            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            elif event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = False

            base_cuts = passrecolepton and bool(event.tracks_passPFCandVeto[iCand]) and event.tracks_nValidPixelHits[iCand]>=3 and passpionveto and passjetveto

            # keep only candidate tracks:
            if not base_cuts: continue

            # check disappearing track tags:
            mva_tight = get_disappearing_track_score("tight", event, iCand, readers)
            mva_loose = get_disappearing_track_score("loose", event, iCand, readers)
                                                                
            tags["SR_short"] = base_cuts and is_pixel_track and mva_loose>(event.tracks_dxyVtx[iCand]*(0.65/0.01) - 0.5) and event.tracks_trkRelIso[iCand]<0.01
            tags["SR_long"] = base_cuts and not is_pixel_track and mva_loose>(event.tracks_dxyVtx[iCand]*(0.7/0.01) - 0.05) and event.tracks_trkRelIso[iCand]<0.01
            #tags["CR_short"] = base_cuts and is_pixel_track and mva_loose<(event.tracks_dxyVtx[iCand]*(0.65/0.01) - 0.5) and event.tracks_dxyVtx[iCand]>0.02
            #tags["CR_long"] = base_cuts and not is_pixel_track and mva_loose<(event.tracks_dxyVtx[iCand]*(0.7/0.01) - 0.5) and event.tracks_dxyVtx[iCand]>0.02
            tags["CR_short"] = base_cuts and event.tracks_dxyVtx[iCand]>0.02 and is_pixel_track
            tags["CR_long"] = base_cuts and event.tracks_dxyVtx[iCand]>0.02 and not is_pixel_track
                            
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
            
            # if leptons in the event, calculate invariant mass:
            if len(goodleptons) > 0:
                invariant_mass = (track + goodleptons[0]).M()
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

            #if tags["SR_short"] or tags["SR_long"] or tags["CR_short"] or tags["CR_long"]:
            #    print "iEv, iCand", iEv, iCand
            #    print "  \_tags", tags
            #    print "  \_is_pixel_track", is_pixel_track
            #    print "  \_mva_tight, mva_loose", mva_tight, mva_loose
            #    print "  \_is_fake_track", is_fake_track
            #    print "  \_weight = event.puWeight * event.CrossSection =", weight
            
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
                                     "tracks_deDxHarmonic2pixelCorrected": correct_dedx_intercalibration(event.tracks_deDxHarmonic2pixel[iCand], current_file_name),
                                     "tracks_deDxHarmonic2strips": event.tracks_deDxHarmonic2strips[iCand],
                                     "tracks_massfromdeDxPixel": tracks_massfromdeDxPixel,
                                     "tracks_massfromdeDxStrips": tracks_massfromdeDxStrips,
                                     "tracks_chi2perNdof": event.tracks_chi2perNdof[iCand],
                                     "tracks_mt": event.tracks[iCand].Mt(),
                                     "tracks_mva_tight": mva_tight,
                                     "tracks_mva_loose": mva_loose,
                                     "tracks_chargedPtSum": event.tracks_chargedPtSum[iCand],
                                     "tracks_charge": event.tracks_charge[iCand],
                                     "tracks_invmass": invariant_mass,
                                     "tracks_chiCandGenMatchingDR": chiCandGenMatchingDR,
                                     "tracks_passpionveto": passpionveto,
                                     "tracks_passjetveto": passjetveto,
                                     "tracks_basecuts": base_cuts,
                                   }
                                  )
                                       
            for tag in tags:
                tagged_tracks[-1]["tracks_%s" % tag] = tags[tag]
  
        # FIXME: keep only events with candidate tracks
        #if len(tagged_tracks)==0:
        #    continue

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
                tree_branch_values[label][i] = track_output_dict[label]

        # save lepton properties vector:
        if n_goodleptons > 0:
            highest_lepton_pt = 0
            highest_lepton_index = 0
            for i, lepton_output_dict in enumerate(lepton_level_output):
                for label in lepton_output_dict:
                    tree_branch_values[label][i] = lepton_output_dict[label]
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

        tout.Fill()
                         
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
    (options, args) = parser.parse_args()
    
    options.inputfiles = options.inputfiles.split(",")
       
    main(
         options.inputfiles,
         options.outputfiles,
         nevents = int(options.nev),
         mask_file_name = False,
        )

