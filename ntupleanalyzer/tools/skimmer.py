#!/bin/env python
from __future__ import division
import commands
import shared_utils
import ROOT
from ROOT import *
from array import array
from optparse import OptionParser
import collections
import json
import math
import xsections
import os, sys
import glob
import numpy as np
import pipes
from natsort import natsorted, ns
import lib_systematics

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def correct_dedx_intercalibration(dedx, filename, abseta, phase, is_data, fsmear_barrel, fsmear_endcap):

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
    elif 'Fall17' in filename or 'Autumn18' in filename: 
    	dedxcalib_barrel = shared_utils.DedxCorr_Pixel_barrel['Fall17']
    	dedxcalib_endcap = shared_utils.DedxCorr_Pixel_endcap['Fall17']
    else:
    	dedxcalib_barrel = 1.0
    	dedxcalib_endcap = 1.0	    
        
    #smearing with smear factor:
    if not is_data:
        dedxcalib_barrel += fsmear_barrel.GetRandom()
        dedxcalib_endcap += fsmear_endcap.GetRandom()

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
        

def get_BDT_score(label, event, iCand, readers, is_pixel_track, phase, ptErrOverPt2, tracks_dxyVtxCorrected, tracks_dzVtxCorrected):
    
    if is_pixel_track:
        category = "short"
    else:
        category = "long"
    category += "_phase" + str(phase)
       
    for var in readers[label + "_" + category]["tmva_variables"]:
                
        if "ptErrOverPt2" in var:
            readers[label + "_" + category]["tmva_variables"][var][0] = ptErrOverPt2
        elif var == "tracks_dxyVtxCorrected":
            # dxy-dz-transform:
            readers[label + "_" + category]["tmva_variables"]["tracks_dxyVtxCorrected"][0] = tracks_dxyVtxCorrected
        elif var == "tracks_dzVtxCorrected":
            # dxy-dz-transform:
            readers[label + "_" + category]["tmva_variables"]["tracks_dzVtxCorrected"][0] = tracks_dzVtxCorrected
        elif var == "tracks_dxyVtx":
            # dxy-dz-transform:
            readers[label + "_" + category]["tmva_variables"]["tracks_dxyVtx"][0] = tracks_dxyVtxCorrected
        elif var == "tracks_dzVtx":
            # dxy-dz-transform:
            readers[label + "_" + category]["tmva_variables"]["tracks_dzVtx"][0] = tracks_dzVtxCorrected
        elif "tracks_" in var:
            readers[label + "_" + category]["tmva_variables"][var][0] = eval("event.%s[%s]" % (var, iCand))
        else:
            readers[label + "_" + category]["tmva_variables"][var][0] = eval("event.tracks_%s[%s]" % (var, iCand))
       
    bdtscore = readers[label + "_" + category]["reader"].EvaluateMVA("BDT")
    return bdtscore 


def get_signal_region(HT, MHT, NJets, n_btags, MinDeltaPhiMhtJets, n_DT, is_pixel_track, DeDxAverage, n_goodelectrons, n_goodmuons, filename):
  
    is_tracker_track = not is_pixel_track
    dedxcutLow = shared_utils.dedxcutLow
    dedxcutMid = shared_utils.dedxcutMid
    binnumbers = shared_utils.binnumbers

    # example
    # listagain = ['Ht',     'HardMet','NJets',  'BTags', 'NTags','TrkLength','MdpMetJets','DeDx',              'NElectrons','NMuons', 'InvMass', 'LepMT', 'TrkPt',        'TrkEta',  'MatchedCalo', 'DtLength', 'DPhiMhtDt',     'TrkMva',    'BinNumber', 'MinDPhiMhtHemJet','Met','Log10DedxMass']
    # binnumbers[((0,inf),    (150,300),(1,2),    (0,0),   (1,1), (1,1),     (0.0,inf),    (dedxcutLow,dedxcutMid),(0,0),   (0,0))] = 1
    #MinDeltaPhiMhtJets >= binkey[7][0] and MinDeltaPhiMhtJets <= binkey[7][1] and \
    

    region = 0
    for binkey in binnumbers:
        if HT >= binkey[0][0] and HT <= binkey[0][1] and \
           MHT >= binkey[1][0] and MHT <= binkey[1][1] and \
           NJets >= binkey[2][0] and NJets <= binkey[2][1] and \
           n_btags >= binkey[3][0] and n_btags <= binkey[3][1] and \
           n_DT >= binkey[4][0] and n_DT <= binkey[4][1] and \
           is_tracker_track >= binkey[5][0] and is_tracker_track <= binkey[5][1] and \
           DeDxAverage >= binkey[7][0] and DeDxAverage <= binkey[7][1] and \
           n_goodelectrons >= binkey[8][0] and n_goodelectrons <= binkey[8][1] and \
           n_goodmuons >= binkey[9][0] and n_goodmuons <= binkey[9][1]:
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


def fill_sparse(event, signal_region, weight, hnsparseobj):

    pMSSMid1 = event.SusyMotherMass
    pMSSMid2 = event.SusyLSPMass
    coordinates = np.float64([pMSSMid1, pMSSMid2, signal_region])
    hnsparseobj.Fill(coordinates, weight)


def main(event_tree_filenames, track_tree_output, nevents = -1, only_tagged_events = False, overwrite = True, debug = False, trigger_study = False, cutflow_study = False, syst = "", lumi_report = False, write_only_sparse = False):

    # clean up output filename
    track_tree_output = track_tree_output.replace(";", "")

    print "Input: %s \nOutput: %s \n n_ev: %s" % (event_tree_filenames, track_tree_output, nevents)

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    # check if output file exists:
    if lumi_report and not overwrite and os.path.exists(track_tree_output.replace(".root", ".json")):
        print "Already done, file ok"
        return()
    elif write_only_sparse and not overwrite and os.path.exists(track_tree_output.replace(".root", "_sparse.root")):
        print "Already done, file ok"
        return()

    if not lumi_report and not overwrite and os.path.exists(track_tree_output):
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

    if lumi_report:
        is_data = True

    # store runs for JSON output:
    runs = {}
    runs_fileinfo = {}

    # load tree
    tree = TChain("TreeMaker2/PreSelection")
    for iFile in event_tree_filenames:

        ## ignore list: broken/corrupt files
        if "Run2018A-17Sep2018-v1.JetHTAOD_270000-DDC26769-F24F-F64B-B83E-0AB519FF9B4F_RA2AnalysisTree.root" in iFile or \
           "Run2018D-PromptReco-v2.SingleMuonAOD4_00000-B6FEAD33-1AB0-E811-AC2D-FA163EC57F99_RA2AnalysisTree.root" in iFile or \
           "Run2017E-31Mar2018-v1.SingleElectronAOD_20000-DC2DA888-5805-E811-B181-7CD30ACE1239_RA2AnalysisTree.root" in iFile or \
           "Run2017B-31Mar2018-v1.SingleElectronAOD_70001-78C69E02-C1DE-E711-857E-FA163E6659D1_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3/Run2017B-31Mar2018-v1.SingleElectronAOD_70001-78C69E02-C1DE-E711-857E-FA163E6659D1_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3/Run2017E-31Mar2018-v1.SingleElectronAOD_20000-DC2DA888-5805-E811-B181-7CD30ACE1239_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2018A-17Sep2018-v1.JetHTAOD_270000-DDC26769-F24F-F64B-B83E-0AB519FF9B4F_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3_jsonneve/Run2018D-PromptReco-v2.SingleMuonAOD4_00000-B6FEAD33-1AB0-E811-AC2D-FA163EC57F99_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3/Run2017B-31Mar2018-v1.SingleElectronAOD_70001-78C69E02-C1DE-E711-857E-FA163E6659D1_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3/Run2017E-31Mar2018-v1.SingleElectronAOD_20000-DC2DA888-5805-E811-B181-7CD30ACE1239_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2018A-17Sep2018-v1.JetHTAOD_270000-DDC26769-F24F-F64B-B83E-0AB519FF9B4F_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3_jsonneve/Run2018D-PromptReco-v2.SingleMuonAOD4_00000-B6FEAD33-1AB0-E811-AC2D-FA163EC57F99_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3/Run2017B-31Mar2018-v1.SingleElectronAOD_70001-78C69E02-C1DE-E711-857E-FA163E6659D1_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3/Run2017E-31Mar2018-v1.SingleElectronAOD_20000-DC2DA888-5805-E811-B181-7CD30ACE1239_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2018A-17Sep2018-v1.JetHTAOD_270000-DDC26769-F24F-F64B-B83E-0AB519FF9B4F_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3_jsonneve/Run2018D-PromptReco-v2.SingleMuonAOD4_00000-B6FEAD33-1AB0-E811-AC2D-FA163EC57F99_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3/Run2017B-31Mar2018-v1.SingleElectronAOD_70001-78C69E02-C1DE-E711-857E-FA163E6659D1_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3/Run2017E-31Mar2018-v1.SingleElectronAOD_20000-DC2DA888-5805-E811-B181-7CD30ACE1239_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2018A-17Sep2018-v1.JetHTAOD_270000-DDC26769-F24F-F64B-B83E-0AB519FF9B4F_RA2AnalysisTree.root" in iFile or \
        "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3_jsonneve/Run2018D-PromptReco-v2.SingleMuonAOD4_00000-B6FEAD33-1AB0-E811-AC2D-FA163EC57F99_RA2AnalysisTree.root" in iFile:
            continue

        iFile = iFile.replace("'", "")
        if not "root.mimes" in iFile:
            try:
                tree.Add(iFile)
            except:
                print "Problem adding file:", iFile
                #os.system("echo %s >> files_with_issues" % iFile)

    nev = tree.GetEntries()       

    # check if data:
    phase = 0
    year = 0
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
                year = 2016
            elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
                phase = 1
                if label == "Run2017" or label == "Fall17":
                    year = 2017
                else:
                    year = 2018

    if year == 0:
        quit("Wrong filename convention")
         
    if data_period == "RunIISummer16MiniAODv3":
        data_period = "Summer16"
        
    if "FastSim" in event_tree_filenames[0] or "FS" in event_tree_filenames[0]:
        is_fastsim = True

    if "_chi" in event_tree_filenames[0] or "SMS" in event_tree_filenames[0] or "PMSSM" in event_tree_filenames[0]:
        is_signal = True
        
    if "PMSSM" in event_tree_filenames[0]:
        is_pmssm = True
    else:
        is_pmssm = False        

    print "Signal: %s, phase: %s, is_pmssm: %s, year: %s" % (is_signal, phase, is_pmssm, year)


    if not lumi_report:
       
        blockhem = False
        partiallyblockhem = False
        if "Run2018B" in event_tree_filenames[0]:
            partiallyblockhem = True
        if "Run2018C" in event_tree_filenames[0] or "Run2018D" in event_tree_filenames[0]:
            blockhem = True
        
        # load dxy-dz-transform:
        infile = TFile("../../disappearing-track-tag/dxydzcalibration.root")
        g_calibratedxy = infile.Get("g_calibratedxy")
        g_calibratedz = infile.Get("g_calibratedz")
        infile.Close()

        # load masks:
        fMask = TFile('../../disappearing-track-tag/Masks_mcal13to30_Data2016.root')
        hMask = fMask.Get('h_Mask_allyearsLongBaseline_EtaVsPhiDT')
        hMask.SetDirectory(0)
        fMask.Close()

        # load signal systematic scale factor:
        fsyst = TFile('../../systematics/signal_scalefactor.root')
        h_short = fsyst.Get('fit_sf_short')
        h_long = fsyst.Get('fit_sf_long')
        if year == 2016:
            signal_sf_short = h_short.GetBinContent(1)
            signal_sf_long = h_long.GetBinContent(1)
        elif year == 2017:
            signal_sf_short = h_short.GetBinContent(2)
            signal_sf_long = h_long.GetBinContent(2)
        elif year == 2018:
            signal_sf_short = h_short.GetBinContent(3)
            signal_sf_long = h_long.GetBinContent(3)
        fsyst.Close()

        # load trigger efficiencies:
        fsyst = TFile('../../triggerefficiency/trigger-efficiencies.root')
        h_triggereff_mht_highjets = fsyst.Get('mht_SingleEl_highjets/h_triggereff_MHT_MHT_%s' % year)
        h_triggereff_mht_highjets.SetDirectory(0)
        h_triggereff_mht_lowjets = fsyst.Get('mht_SingleEl_lowjets/h_triggereff_MHT_MHT_%s' % year)
        h_triggereff_mht_lowjets.SetDirectory(0)
        h_triggereff_sel = fsyst.Get('sel_switchdenom/h_triggereff_SEl_leadingelectron_pt_MHT_%s' % year)
        h_triggereff_sel.SetDirectory(0)
        h_triggereff_smu = fsyst.Get('smu_switchdenom/h_triggereff_SMu_leadingmuon_pt_MHT_%s' % year)
        h_triggereff_smu.SetDirectory(0)
        fsyst.Close()
        #h_triggereff_sel = fsyst.Get('sel_switchdenom/h_triggereff_SEl_leadinglepton_pt_MHT_%s' % year)
        #h_triggereff_smu = fsyst.Get('smu_switchdenom/h_triggereff_SMu_leadinglepton_pt_MHT_%s' % year)

        if not (lumi_report or write_only_sparse):
            fout = TFile(track_tree_output, "recreate")
        
        # write number of events to histogram:
        h_nev = TH1F("nev", "nev", 2, 0, 2)
        h_nev.Fill(0, nev)

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
        if data_period == "Run2018" or data_period == "Autumn18":
            BTAG_deepCSV = 0.4184
        btag_cut = BTAG_deepCSV

        # load BDTs and fetch list of DT tag label:
        bdts = {
            #"nov20_noEdep": {
            #            "short_phase0": ["../../disappearing-track-tag/2016-short-tracks-nov20-noEdep/dataset/weights/TMVAClassification_BDT.weights.xml",     ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #            "short_phase1": ["../../disappearing-track-tag/2017-short-tracks-nov20-noEdep/dataset/weights/TMVAClassification_BDT.weights.xml",     ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #            "long_phase0":  ["../../disappearing-track-tag/2016-long-tracks-nov20-noEdep/dataset/weights/TMVAClassification_BDT.weights.xml",      ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #            "long_phase1":  ["../../disappearing-track-tag/2017-long-tracks-nov20-noEdep/dataset/weights/TMVAClassification_BDT.weights.xml",      ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #         },
            "sep21v1_baseline": {
                        "short_phase0": ["../../disappearing-track-tag/2016-short-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                        "short_phase1": ["../../disappearing-track-tag/2017-short-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
                        "long_phase0":  ["../../disappearing-track-tag/2016-long-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                        "long_phase1":  ["../../disappearing-track-tag/2017-long-tracks-sep21v1-baseline/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
                     },
            #"sep21v3_baseline": {
            #            "short_phase0": ["../../disappearing-track-tag/2016-short-tracks-sep21v2-baseline/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #            "short_phase1": ["../../disappearing-track-tag/2017-short-tracks-sep21v3-baseline/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #            "long_phase0":  ["../../disappearing-track-tag/2016-long-tracks-sep21v2-baseline/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #            "long_phase1":  ["../../disappearing-track-tag/2017-long-tracks-sep21v2-baseline/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #         },
            #"sep21v3_corrected": {
            #            "short_phase0": ["../../disappearing-track-tag/2016-short-tracks-sep21v2-corrected/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #            "short_phase1": ["../../disappearing-track-tag/2017-short-tracks-sep21v3-corrected/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtxCorrected", "tracks_dzVtxCorrected", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #            "long_phase0":  ["../../disappearing-track-tag/2016-long-tracks-sep21v2-corrected/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #            "long_phase1":  ["../../disappearing-track-tag/2017-long-tracks-sep21v2-corrected/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #         },
            #"sep21v1_baselinecheck": {
            #        "short_phase0": ["../../disappearing-track-tag/2016-short-tracks-sep21v1-baselinecheck/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #        "short_phase1": ["../../disappearing-track-tag/2017-short-tracks-sep21v1-baselinecheck/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #        "long_phase0":  ["../../disappearing-track-tag/2016-long-tracks-sep21v1-baselinecheck/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #        "long_phase1":  ["../../disappearing-track-tag/2017-long-tracks-sep21v1-baselinecheck/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #     },
            #"sep21v1_omega": {
            #        "short_phase0": ["../../disappearing-track-tag/2016-short-tracks-sep21v1-omega/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #        "short_phase1": ["../../disappearing-track-tag/2017-short-tracks-sep21v1-omega/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #        "long_phase0":  ["../../disappearing-track-tag/2016-long-tracks-sep21v1-omega/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #        "long_phase1":  ["../../disappearing-track-tag/2017-long-tracks-sep21v1-omega/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #     },
            #"sep21v1_omega2": {
            #        "short_phase0": ["../../disappearing-track-tag/2016-short-tracks-sep21v1-omega2/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #        "short_phase1": ["../../disappearing-track-tag/2017-short-tracks-sep21v1-omega2/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #        "long_phase0":  ["../../disappearing-track-tag/2016-long-tracks-sep21v1-omega2/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #        "long_phase1":  ["../../disappearing-track-tag/2017-long-tracks-sep21v1-omega2/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #     },
            #"sep21v1_omega3": {
            #        "short_phase0": ["../../disappearing-track-tag/2016-short-tracks-sep21v1-omega3/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #        "short_phase1": ["../../disappearing-track-tag/2017-short-tracks-sep21v1-omega3/dataset/weights/TMVAClassification_BDT.weights.xml", ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],
            #        "long_phase0":  ["../../disappearing-track-tag/2016-long-tracks-sep21v1-omega3/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #        "long_phase1":  ["../../disappearing-track-tag/2017-long-tracks-sep21v1-omega3/dataset/weights/TMVAClassification_BDT.weights.xml",  ["tracks_dxyVtx", "tracks_dzVtx", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"] ],          
            #     },
               }

        if is_pmssm:
            # only evaluate one BDT for this
            bdts = {"sep21v1_baseline": dict(bdts["sep21v1_baseline"])}

        readers = {}
        for label in bdts:
            for category in ["short", "long"]:
                for i_phase in ["phase0", "phase1"]:
            
                    readers[label + "_" + category + "_" + i_phase] = {}
                    readers[label + "_" + category + "_" + i_phase]["tmva_variables"] = {}
                    readers[label + "_" + category + "_" + i_phase]["reader"] = TMVA.Reader()
                    
                    for var in bdts[label][category + "_" + i_phase][1]:
                        readers[label + "_" + category + "_" + i_phase]["tmva_variables"][var] = array('f',[0])
                        readers[label + "_" + category + "_" + i_phase]["reader"].AddVariable(var, readers[label + "_" + category + "_" + i_phase]["tmva_variables"][var])
                            
                    readers[label + "_" + category + "_" + i_phase]["reader"].BookMVA("BDT", bdts[label][category + "_" + i_phase][0])
        
        tout = TTree("Events", "tout")

        # prepare variables for output tree   
        float_branches = [
                          "EvtNum",
                          "weight",
                          "MET",
                          "MHT",
                          "HT",
                          "PFCaloMETRatio",
                          "leadinglepton_pt",
                          "leadinglepton_mt",
                          "leadinglepton_eta",
                          "leadinglepton_phi",
                          "leadinglepton_charge",
                          "leadinglepton_dedx",
                          "leadingelectron_pt",
                          "leadingelectron_mt",
                          "leadingelectron_eta",
                          "leadingelectron_phi",
                          "leadingelectron_charge",
                          "leadingelectron_dedx",
                          "leadingmuon_pt",
                          "leadingmuon_mt",
                          "leadingmuon_eta",
                          "leadingmuon_phi",
                          "leadingmuon_charge",
                          "leadingmuon_dedx",
                          "MinDeltaPhiMhtJets",
                          "chargino_parent_mass",
                          "signal_stop_mass",
                          "signal_gluino_mass",
                          "signal_lsp_mass",
                          "leading_bjet_pt",
                          "leading_bjet_genpt",
                          "leading_bjet_btagcut",
                          "met_genpt",
                          "leadingDT_mva",
                          "leadingDT_Edep",
                          "leadingDT_EdepByP",
                          "invmass",
                          "leptonmt",
                          "mtautau",
                          "dphiMhtDt",
                          "mtDtMht",
                          "FastSimWeightPR31285To36122",
                        ]
                                        
        if is_signal:
            float_branches += [
                          "SusyCTau",
                          "SusyLSPMass",
                          "SusyMotherMass",
                        ]
                         
        integer_branches = [
                          "RunNum",
                          "LumiBlockNum",
                          "pass_baseline",
                          "n_goodjets",
                          "n_btags",
                          "n_goodelectrons",
                          "n_goodmuons",
                          "n_allvertices",
                          "leadinglepton_type",
                          "leading_bjet_hadronFlavor",
                          "triggered_met",
                          "triggered_singleelectron",
                          "triggered_singlemuon",
                          "triggered_ht",
                          "leadingDT_pixeltrack",
                          "sr",
                          "analysisregion",
                          "n_tags",
                          "n_DTShort",
                          "n_DTLong",
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

        tree_branch_values = {}
        for variable in float_branches:
            tree_branch_values[variable] = array( 'f', [ -1 ] )
            tout.Branch( variable, tree_branch_values[variable], '%s/F' % variable )
        for variable in integer_branches:
            tree_branch_values[variable] = array( 'i', [ -1 ] )
            tout.Branch( variable, tree_branch_values[variable], '%s/I' % variable )

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
                               'tracks_trackQualityHighPurity',                           
                               'tracks_charge', 
                               'tracks_passmask', 
                               'tracks_passleptonveto',
                               'tracks_passpionveto',
                               'tracks_passjetveto',
                               'tracks_baseline',
                               'tracks_category',
                               'tracks_mt2',                           
                               'tracks_mt2_trackiso',
                               'tracks_mt2_leptoniso',
                               'tracks_exo',
                               'tracks_exo_leptoniso',
                               'tracks_exo_trackiso',
                               'tracks_exo_jetiso',
                               'tracks_chiLeading',
                               'tracks_analysisregion',
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
                
        if not trigger_study:
            for branch in vector_int_branches:
                tree_branch_values[branch] = 0
                tout.Branch(branch, 'std::vector<int>', tree_branch_values[branch])

        vector_float_branches = [
                                 'tracks_dxyVtx',
                                 'tracks_dzVtx',
                                 'tracks_dxyVtxCorrected',
                                 'tracks_dzVtxCorrected',
                                 'tracks_matchedCaloEnergy',
                                 'tracks_trkRelIso',
                                 'tracks_ptErrOverPt2',
                                 'tracks_p',
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
                                 #'tracks_invmass',
                                 'tracks_chiCandGenMatchingDR',
                                 'tracks_chiLabXY',
                                 'tracks_chiGamma',
                                 'tracks_chiBeta',
                                 'tracks_chiEta',
                                 'tracks_chiPt',
                                 'tracks_DrJetDt',
                                 'tracks_fastsimweight_LowLabXYAndDeDx',
                                 'tracks_signalsf',
                                 'tracks_weightOmega',
                                ]

        for label in bdts:
            vector_float_branches += ["tracks_mva_%s" % label]
            vector_float_branches += ["tracks_mva_%s_corrdxydz" % label]

        if not trigger_study:
            for branch in vector_float_branches:
                tree_branch_values[branch] = 0
                tout.Branch(branch, 'std::vector<double>', tree_branch_values[branch])   
        
        if is_pmssm and write_only_sparse:
            pMSSMid1_max = 600
            pMSSMid1_low = 0.5
            pMSSMid1_up = pMSSMid1_max + 0.5
            pMSSMid2_max = 144855
            pMSSMid2_low = 0.5
            pMSSMid2_up = pMSSMid2_max + 0.5
            #sr_max = 51+1
            sr_max = 49+1
            sr_low = 0.5-1
            #sr_up = 51.5
            sr_up = 49.5
            bins = np.intc([pMSSMid1_max, pMSSMid2_max, sr_max])
            low = np.float64([pMSSMid1_low, pMSSMid2_low, sr_low])
            high = np.float64([pMSSMid1_up, pMSSMid2_up, sr_up])
            hnsparse = THnSparseF("disappearingtracks", "disappearingtracks", 3, bins, low, high)
            hnsparse_fastSimWeightPR31285To36122 = THnSparseF("disappearingtracks_fastSimWeightPR31285To36122", "disappearingtracks_fastSimWeightPR31285To36122", 3, bins, low, high)
            hnsparse_fastsimweightLowLabXYAndDeDx = THnSparseF("disappearingtracks_fastsimweightLowLabXYAndDeDx", "disappearingtracks_fastsimweightLowLabXYAndDeDx", 3, bins, low, high)
            hnsparse_triggerweight = THnSparseF("disappearingtracks_triggerweight", "disappearingtracks_triggerweight", 3, bins, low, high)
            hnsparse_signalscalefactor = THnSparseF("disappearingtracks_signalscalefactor", "disappearingtracks_signalscalefactor", 3, bins, low, high)
            hnsparse_btaggingSF = THnSparseF("disappearingtracks_btaggingSF", "disappearingtracks_btaggingSF", 3, bins, low, high)
            hnsparse_ISRSF = THnSparseF("disappearingtracks_ISRSF", "disappearingtracks_ISRSF", 3, bins, low, high)
            hnsparse_allweights = THnSparseF("disappearingtracks_allweights", "disappearingtracks_allweights", 3, bins, low, high)

        # load smearing functions
        if not is_data:
            fsmear_barrel, fsmear_endcap = shared_utils.Load_DedxSmear(phase)
        else:
            fsmear_barrel = False
            fsmear_endcap = False

        # region definitions:
        # ===================

        event_selections = collections.OrderedDict()
        event_selections["analysis"] = collections.OrderedDict()
        event_selections["fakerate"] = collections.OrderedDict()
        event_selections["kappa"] = collections.OrderedDict()
        event_selections["mukappa"] = collections.OrderedDict()

        event_selections["analysis"]["HadBaseline"] = "event.MHT>30 and \
                                                       event.MinDeltaPhiMhtJets>0.4 and \
                                                       event.n_goodjets>=1 and \
                                                       event.n_goodelectrons==0 and \
                                                       event.n_goodmuons==0 and \
                                                       event.mtDtMht>20"
        event_selections["analysis"]["SMuBaseline"] = "event.MHT>30 and \
                                                       event.MinDeltaPhiMhtJets>0.4 and \
                                                       event.n_goodjets>=1 and \
                                                       event.n_goodmuons>=1 and \
                                                       event.n_goodelectrons==0 and \
                                                       event.invmass>140 and \
                                                       event.leadinglepton_mt>110 and \
                                                       event.mtDtMht>20"
        event_selections["analysis"]["SElBaseline"] = "event.MHT>30 and \
                                                       event.MinDeltaPhiMhtJets>0.4 and \
                                                       event.n_goodjets>=1 and \
                                                       event.n_goodelectrons>=1 and \
                                                       event.invmass>140 and \
                                                       event.leadinglepton_mt>110 and \
                                                       event.mtDtMht>20"
        event_selections["fakerate"]["QCDLowMHT"] =   "event.MHT>30 and \
                                                       event.MHT<60 and \
                                                       event.n_goodjets>=1 and \
                                                       event.MinDeltaPhiMhtJets>0.4 and \
                                                       event.n_goodelectrons==0 and \
                                                       event.n_goodmuons==0 and \
                                                       event.n_btags==0 and \
                                                       event.mtDtMht>20"
        event_selections["kappa"]["PromptDYEl"] =     "event.n_goodelectrons==1 and \
                                                       event.n_goodmuons==0 and \
                                                       event.MinDeltaPhiMhtJets>0.4 and \
                                                       event.leadinglepton_mt<100"
        event_selections["mukappa"]["PromptDYMu"] =   "event.n_goodelectrons==0 and \
                                                       event.n_goodmuons==1 and \
                                                       event.MinDeltaPhiMhtJets>0.4 and \
                                                       event.leadinglepton_mt<100"

        replacevars = collections.OrderedDict()
        replacevars['pixeltrack'] =   'event.tracks_is_pixel_track[i_track]'
        replacevars['baseline'] =     'event.tracks_baseline[i_track]'
        replacevars['BDT'] =          'event.tracks_mva_sep21v1_baseline_corrdxydz[i_track]'
        replacevars['EDep'] =         'event.tracks_matchedCaloEnergy[i_track]'
        replacevars['dphiMhtDt'] =    'event.dphiMhtDt'
        replacevars['trackp'] =       'event.tracks_p[i_track]'
        replacevars['leptonveto'] =   'event.tracks_passleptonveto[i_track]'
        replacevars['pfveto'] =       'event.tracks_passPFCandVeto[i_track]'
        replacevars['invmass'] =      'event.invmass'
        replacevars['DrJetDt'] =      'event.tracks_DrJetDt[i_track]'

        baselineShort =             "baseline==1 and pixeltrack==1 and "
        baselineLong =              "baseline==1 and pixeltrack==0 and "

        if phase == 0:
            SignalShort =           "BDT>0.1 and EDep<15 and DrJetDt>0.2" 
            SignalLong =            "BDT>0.12 and EDep/trackp<0.2 and DrJetDt>0.2" 
            PromptSidebandShort =   "BDT>0.1 and EDep>30 and EDep<300 and DrJetDt>0.1" 
            PromptSidebandLong =    "BDT>0.1 and EDep/trackp>0.30 and EDep/trackp<1.20 and DrJetDt>0.1" 
            PromptSidebandCRShort =  PromptSidebandShort 
            PromptSidebandCRLong =   PromptSidebandLong
            FakeSidebandShort =     "BDT>-0.1 and BDT<-0.05 and EDep<15 and DrJetDt>0.2"   
            FakeSidebandLong =      "BDT>-0.1 and BDT<0.0 and EDep/trackp<0.2 and DrJetDt>0.2"    
            FakeSidebandCRShort =   FakeSidebandShort
            FakeSidebandCRLong =    FakeSidebandLong
        else:
            SignalShort =           "BDT>0.15 and EDep<15 and DrJetDt>0.2"          
            SignalLong =            "BDT>0.08 and EDep/trackp<0.2 and DrJetDt>0.2" 
            PromptSidebandShort =   "BDT>0.05 and EDep>30 and EDep<300 and DrJetDt>0.1" 
            PromptSidebandLong =    "BDT>0.08 and EDep/trackp>0.30 and EDep/trackp<1.20 and DrJetDt>0.1" 
            PromptSidebandCRShort =  PromptSidebandShort
            PromptSidebandCRLong =   PromptSidebandLong
            FakeSidebandShort =     "BDT>-0.1 and BDT<0.0 and EDep<15 and DrJetDt>0.2"                 
            FakeSidebandLong =      "BDT>-0.1 and BDT<0.0 and EDep/trackp<0.2 and DrJetDt>0.2"                  
            FakeSidebandCRShort =    FakeSidebandShort               
            FakeSidebandCRLong =     FakeSidebandLong             

        regions = collections.OrderedDict()

        regions["kappa_sr_short"] = baselineShort + SignalShort + " and dphiMhtDt<3.14/4 and invmass>70 and invmass<105"
        regions["kappa_promptSideband_short"] = baselineShort + PromptSidebandShort + " and dphiMhtDt<3.14/4 and invmass>70 and invmass<105"
        regions["kappa_sr_long"] = baselineLong + SignalLong + " and dphiMhtDt<3.14/2 and invmass>75 and invmass<100 and event.MHT>30"
        regions["kappa_promptSideband_long"] = baselineLong + PromptSidebandLong + " and dphiMhtDt<3.14/2 and invmass>75 and invmass<100 and event.MHT>30"

        regions["mukappa_sr_short"] = "pixeltrack==1 and " + SignalShort + " and dphiMhtDt<3.14/4 and invmass>70 and invmass<105 and event.MHT>30"
        regions["mukappa_sr_long"] = "pixeltrack==0 and " + SignalLong + " and dphiMhtDt<3.14/2 and invmass>75 and invmass<100"
        regions["mukappa_promptSideband_short"] = "pixeltrack==1 and " + PromptSidebandShort + " and dphiMhtDt<3.14/4 and invmass>70 and invmass<105 and event.MHT>30"
        regions["mukappa_promptSideband_long"] = "pixeltrack==0 and " + PromptSidebandLong + " and dphiMhtDt<3.14/2 and invmass>75 and invmass<100"

        regions["theta_sr_short"] = baselineShort + SignalShort
        regions["theta_sr_long"] = baselineLong + SignalLong
        regions["theta_fakeSideband_short"] = baselineShort + FakeSidebandShort
        regions["theta_fakeSideband_long"] = baselineLong + FakeSidebandLong    

        regions["sr_short"] = baselineShort + SignalShort
        regions["sr_long"] = baselineLong + SignalLong
        #regions["sr"] = "(%s) or (%s)" % (SignalShort, SignalLong)
        regions["promptSideband_short"] = baselineShort + PromptSidebandShort
        regions["promptSideband_long"] = baselineLong + PromptSidebandLong    
        regions["fakeSideband_short"] = baselineShort + FakeSidebandShort
        regions["fakeSideband_long"] = baselineLong + FakeSidebandLong    
        regions["promptcr_short"] = baselineShort + PromptSidebandCRShort
        regions["promptcr_long"] = baselineLong + PromptSidebandCRLong
        regions["fakecr_short"] = baselineShort + FakeSidebandCRShort
        regions["fakecr_long"] = baselineLong + FakeSidebandCRLong
        
        for regionlabel in regions.keys():
            for shortvar in replacevars:
                regions[regionlabel] = regions[regionlabel].replace(shortvar, replacevars[shortvar])
       
        # b-tagging SF:
        #FIXME
        readerBtag = lib_systematics.prepareReaderBtagSF()

    # load JSON files:
    if is_data and year == 2016:
        with open("../../../treemaker/CMSSW_10_2_7/src/TreeMaker/Production/test/data/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt", "r") as fjson:
            goldenJSON = json.load(fjson)
    if is_data and year == 2017:
        with open("../../../treemaker/CMSSW_10_2_7/src/TreeMaker/Production/test/data/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt", "r") as fjson:
            goldenJSON = json.load(fjson)
    if is_data and year == 2018:
        with open("../../../treemaker/CMSSW_10_2_7/src/TreeMaker/Production/test/data/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt", "r") as fjson:
            goldenJSON = json.load(fjson)
        
    mixed_masked_file = False

    print "Looping over %s events" % nev
    for iEv, event in enumerate(tree):
        
        if nevents > 0 and iEv > nevents: break      
        if (iEv+1) % 10000 == 0:
            print "event %s / %s" % (iEv + 1, nev)

        current_file_name = tree.GetFile().GetName()
       
        # calculate weight and collect lumisections:
        if is_data:

            runnum = event.RunNum
            lumisec = event.LumiBlockNum
            
            #check if in golden JSON:
            keep_processing = False
            if str(runnum) in goldenJSON:
                lumiblocks = goldenJSON[str(runnum)]
                for lumiblock in lumiblocks:
                    if lumisec >= lumiblock[0] and lumisec <= lumiblock[1]:
                        keep_processing = True
                        break
            if not keep_processing:
                mixed_masked_file = True
                continue
            
            if runnum not in runs:
                runs[runnum] = []
            if lumisec not in runs[runnum]:
                runs[runnum].append(lumisec)

            #per-file lumisecs:
            if current_file_name not in runs_fileinfo:
                runs_fileinfo[current_file_name] = {}
            if runnum not in runs_fileinfo[current_file_name]:
                runs_fileinfo[current_file_name][runnum] = []
            if lumisec not in runs_fileinfo[current_file_name][runnum]:
                runs_fileinfo[current_file_name][runnum].append(lumisec)

            weight = 1.0
        else:
            weight = 1.0 * event.puWeight * event.CrossSection

        if lumi_report:
            continue

        if is_pmssm and write_only_sparse:
            # fill zero bin with weight=1.0 (unweighted)
            fill_sparse(event, 0, 1.0, hnsparse)
            fill_sparse(event, 0, 1.0, hnsparse_fastSimWeightPR31285To36122)
            fill_sparse(event, 0, 1.0, hnsparse_fastsimweightLowLabXYAndDeDx)
            fill_sparse(event, 0, 1.0, hnsparse_triggerweight)
            fill_sparse(event, 0, 1.0, hnsparse_signalscalefactor)
            fill_sparse(event, 0, 1.0, hnsparse_btaggingSF)
            fill_sparse(event, 0, 1.0, hnsparse_ISRSF)
            fill_sparse(event, 0, 1.0, hnsparse_allweights)

        # ISR weight:
        weight_isrnom = lib_systematics.get_isr_weight(event, 0)
        #FIXME
        #weight_isrnom = 1.0

        # reset all branch values:
        for label in tree_branch_values:
            if "tracks_" in label or "leptons_" in label:
                continue
            tree_branch_values[label][0] = -1

        if is_signal:
            signal_stop_mass = -1
            signal_gluino_mass = -1
            signal_lsp_mass = -1
            for i_genParticle, genParticle in enumerate(event.GenParticles):
                if abs(event.GenParticles_PdgId[i_genParticle]) == 1000021:
                    signal_gluino_mass = round(genParticle.M())
                elif abs(event.GenParticles_PdgId[i_genParticle]) == 1000022:
                    signal_lsp_mass = round(genParticle.M())
                elif abs(event.GenParticles_PdgId[i_genParticle]) == 1000006 or abs(event.GenParticles_PdgId[i_genParticle]) == 2000006:
                    signal_stop_mass = round(genParticle.M())

            if "ctau" in event_tree_filenames[0]:
                try:
                    tree_branch_values["SusyCTau"][0] = event.SusyCTau
                except:
                    pass
            tree_branch_values["SusyLSPMass"][0] = event.SusyLSPMass
            tree_branch_values["SusyMotherMass"][0] = event.SusyMotherMass
        
        if is_signal:
            tree_branch_values["met_genpt"][0] = event.GenMET
            for ijet, jet in enumerate(event.Jets):
                if jet.Pt() > 15:
                    if abs(jet.Eta()) < 2.4:
                        for i_genJet, genJet in enumerate(event.GenJets):
                            if genJet.DeltaR(jet) < 0.4:
                                tree_branch_values["leading_bjet_btagcut"][0] = event.Jets_bJetTagDeepCSVBvsAll[ijet]
                                tree_branch_values["leading_bjet_hadronFlavor"][0] = event.Jets_hadronFlavor[ijet]
                                tree_branch_values["leading_bjet_pt"][0] = jet.Pt()
                                tree_branch_values["leading_bjet_genpt"][0] = genJet.Pt()        
                                tree_branch_values["MET"][0] = event.MET
                                break
                        break            

        # check trigger:
        tree_branch_values["triggered_met"][0] = 0
        tree_branch_values["triggered_ht"][0] = 0
        tree_branch_values["triggered_singleelectron"][0] = 0
        tree_branch_values["triggered_singlemuon"][0] = 0

        if shared_utils.PassTrig(event, 'MhtMet6pack'):
            tree_branch_values["triggered_met"][0] = 1
        if shared_utils.PassTrig(event, 'SingleElectron'):
            tree_branch_values["triggered_singleelectron"][0] = 1
        if shared_utils.PassTrig(event, 'SingleMuon'):
            tree_branch_values["triggered_singlemuon"][0] = 1
        if shared_utils.PassTrig(event, 'HtTrain'):
            tree_branch_values["triggered_ht"][0] = 1

        if not trigger_study:
            if "MET" in current_file_name and not tree_branch_values["triggered_met"][0]:
                continue
            if "SingleElectron" in current_file_name and not tree_branch_values["triggered_singleelectron"][0]:
                continue
            if "SingleMuon" in current_file_name and not tree_branch_values["triggered_singlemuon"][0]:
                continue
            if "JetHT" in current_file_name and not tree_branch_values["triggered_ht"][0]:
                continue

        # basic event selection:
        passed_baseline_selection = True
        FastSimWeightPR31285To36122 = 1.0
        if is_fastsim:
            try:
                FastSimWeightPR31285To36122 = event.FastSimWeightPR31285To36122
            except:
                FastSimWeightPR31285To36122 = 1.0
            if not shared_utils.passesUniversalSelectionFastSim(event):
                passed_baseline_selection = False
        else:
            if not is_data and not shared_utils.passesUniversalSelection(event):
                passed_baseline_selection = False
            elif is_data and not shared_utils.passesUniversalDataSelection(event):
                passed_baseline_selection = False

        if not cutflow_study and not passed_baseline_selection:
        #if not cutflow_study and not passed_baseline_selection and not is_signal:
            continue

        # select good leptons:
        goodelectrons_info = []
        goodmuons_info = []
        goodelectrons = []
        goodmuons = []
        n_goodelectrons = 0
        n_goodmuons = 0

        leadingelectron = 0
        leadingmuon = 0
        
        for i, electron in enumerate(event.Electrons):
            if electron.Pt() > 30 and abs(electron.Eta()) < 2.4 and bool(event.Electrons_passIso[i]) and bool(event.Electrons_tightID[i]):

                if blockhem:
                    if -3.2<electron.Eta() and electron.Eta()<-1.2 and -1.77<electron.Phi() and electron.Phi()<-0.67:
                        continue
                if partiallyblockhem:
                    if event.RunNum>=319077:
                        if -3.2<electron.Eta() and electron.Eta()<-1.2 and -1.77<electron.Phi() and electron.Phi()<-0.67: 
                            continue

                goodelectrons.append(electron)
                n_goodelectrons += 1
                
                matched_dedx = -1.0
                for iCand, track in enumerate(event.tracks):
                    if track.DeltaR(electron) < 0.02:
                        matched_dedx = event.tracks_deDxHarmonic2pixel[iCand]
                
                goodelectrons_info.append({"leptons_pt": electron.Pt(),
                                         "leptons_eta": electron.Eta(),
                                         "leptons_mt": event.Electrons_MTW[i],
                                         "leptons_phi": electron.Phi(),
                                         "leptons_charge": event.Electrons_charge[i],                                         
                                         "leptons_dedx": correct_dedx_intercalibration(matched_dedx, current_file_name, electron.Eta(), phase, is_data, fsmear_barrel, fsmear_endcap),
                                         "leptons_type": 11,
                                        })
                                             
        for i, muon in enumerate(event.Muons):
            if muon.Pt() > 30 and abs(muon.Eta()) < 2.4 and bool(event.Muons_passIso[i]) and bool(event.Muons_mediumID[i]):

                goodmuons.append(muon)
                n_goodmuons += 1
                                
                matched_dedx = -1.0
                for iCand, track in enumerate(event.tracks):
                    if track.DeltaR(muon) < 0.02:
                        matched_dedx = event.tracks_deDxHarmonic2pixel[iCand]
                
                goodmuons_info.append({"leptons_pt": muon.Pt(),
                                         "leptons_eta": muon.Eta(),
                                         "leptons_mt": event.Muons_MTW[i],
                                         "leptons_phi": muon.Phi(),
                                         "leptons_charge": event.Muons_charge[i],
                                         "leptons_dedx": correct_dedx_intercalibration(matched_dedx, current_file_name, muon.Eta(), phase, is_data, fsmear_barrel, fsmear_endcap),
                                         "leptons_type": 13,
                                        })


        goodleptons = goodelectrons + goodmuons
        goodleptons_info = goodelectrons_info + goodmuons_info
        n_goodleptons = n_goodelectrons + n_goodmuons
                
        # get leading lepton:
        highest_lepton_pt = 0
        highest_lepton_pt_index = 0
        highest_electron_pt = 0
        highest_electron_pt_index = 0
        highest_muon_pt = 0
        highest_muon_pt_index = 0

        for i, lepton_output_dict in enumerate(goodleptons_info):
                        
            if lepton_output_dict["leptons_pt"] > highest_lepton_pt:
                highest_lepton_pt = lepton_output_dict["leptons_pt"]
                highest_lepton_pt_index = i
            if lepton_output_dict["leptons_pt"] > highest_electron_pt and lepton_output_dict["leptons_type"] == 11:
                highest_electron_pt = lepton_output_dict["leptons_pt"]
                highest_electron_pt_index = i
            if lepton_output_dict["leptons_pt"] > highest_muon_pt and lepton_output_dict["leptons_type"] == 13:
                highest_muon_pt = lepton_output_dict["leptons_pt"]
                highest_muon_pt_index = i
                
        if len(goodleptons)>0:
            leading_lepton = goodleptons[highest_lepton_pt_index]

            # save leading lepton:
            tree_branch_values["leadinglepton_pt"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_pt"]
            tree_branch_values["leadinglepton_mt"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_mt"]
            tree_branch_values["leadinglepton_eta"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_eta"]
            tree_branch_values["leadinglepton_charge"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_charge"]
            tree_branch_values["leadinglepton_phi"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_phi"]
            tree_branch_values["leadinglepton_dedx"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_dedx"]
            tree_branch_values["leadinglepton_type"][0] = goodleptons_info[highest_lepton_pt_index]["leptons_type"]
        else:
            leading_lepton = 0

        if highest_electron_pt>0:
            leadingelectron = goodleptons[highest_electron_pt_index]
            tree_branch_values["leadingelectron_pt"][0] = goodleptons_info[highest_electron_pt_index]["leptons_pt"]
            tree_branch_values["leadingelectron_mt"][0] = goodleptons_info[highest_electron_pt_index]["leptons_mt"]
            tree_branch_values["leadingelectron_eta"][0] = goodleptons_info[highest_electron_pt_index]["leptons_eta"]
            tree_branch_values["leadingelectron_charge"][0] = goodleptons_info[highest_electron_pt_index]["leptons_charge"]
            tree_branch_values["leadingelectron_phi"][0] = goodleptons_info[highest_electron_pt_index]["leptons_phi"]
            tree_branch_values["leadingelectron_dedx"][0] = goodleptons_info[highest_electron_pt_index]["leptons_dedx"]
        
        if highest_muon_pt>0:
            leadingmuon = goodleptons[highest_muon_pt_index]
            tree_branch_values["leadingmuon_pt"][0] = goodleptons_info[highest_muon_pt_index]["leptons_pt"]
            tree_branch_values["leadingmuon_mt"][0] = goodleptons_info[highest_muon_pt_index]["leptons_mt"]
            tree_branch_values["leadingmuon_eta"][0] = goodleptons_info[highest_muon_pt_index]["leptons_eta"]
            tree_branch_values["leadingmuon_charge"][0] = goodleptons_info[highest_muon_pt_index]["leptons_charge"]
            tree_branch_values["leadingmuon_phi"][0] = goodleptons_info[highest_muon_pt_index]["leptons_phi"]
            tree_branch_values["leadingmuon_dedx"][0] = goodleptons_info[highest_muon_pt_index]["leptons_dedx"]
                             
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
                            # update event variable:
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
                            # update event variable:
                            event.CrossSection = xsections.get_T1_xsection(parent_mass)
                            chargino_parent_mass = parent_mass
                            break
            elif "g1800_chi1400_27_200970" in current_file_name:
                # update event variable:
                event.CrossSection = 0.00276133 #pb
            else:
                event.CrossSection = 1.0
                if iEv < 1:
                    print "Signal xsection undefined..."

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
        for i_jet, jet in enumerate(event.Jets):
            if bool(event.Jets_ID[i_jet]) and jet.Pt() > 30 and abs(jet.Eta()) < 2.4:
                ignore_jet = False
                for lepton in goodleptons:
                    if jet.DeltaR(lepton) < 0.4:
                        ignore_jet = True
                        break
                if ignore_jet:
                    continue
                n_goodjets += 1
                goodjets.append(jet)
                if jet.Pt() > leading_jet_pt:
                    leading_jet_pt = jet.Pt()
                    leading_jet = jet

        mva_scores = {}
        tagged_tracks = []

        # adjust some variables:        
        if data_period == "Run2016" or data_period == "Summer16":
            BTAG_deepCSV = 0.6324
        if data_period == "Run2017" or data_period == "Fall17":
            BTAG_deepCSV = 0.4941
        if data_period == "Run2018":
            BTAG_deepCSV = 0.4184
        btag_cut = BTAG_deepCSV

        #FIXME
        # get b-tagging efficiency:
        try:
            weight_sfbtagnom = lib_systematics.get_btag_weight(event, nSigmaBtagSF = 0, nSigmaBtagFastSimSF = 0, isFastSim = is_fastsim, readerBtag = readerBtag)
        except:
            weight_sfbtagnom = -1

        if debug:
            track_debug_output = ""

        for iCand, track in enumerate(event.tracks):

            # basic track pt cut for cutflow study:
            if track.Pt() < 25: continue

            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            elif event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = False

            if is_pixel_track and track.Pt() > 25:
                pass_category = True
            elif not is_pixel_track and track.Pt() > 40 and event.tracks_nMissingOuterHits[iCand]>=2:
                pass_category = True
            else:
                pass_category = False
                                                                       
            if not cutflow_study and not pass_category:
                continue            

            # HEM:
            if blockhem:
                if -3.2<track.Eta() and track.Eta()<-1.2 and -1.77<track.Phi() and track.Phi()<-0.67:
                    continue
            if partiallyblockhem:
                if event.RunNum>=319077:
                    if -3.2<track.Eta() and track.Eta()<-1.2 and -1.77<track.Phi() and track.Phi()<-0.67: 
                        continue
            
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
                    if deltaR < 0.04:
                        if gen_track_cone_pdgid == 11:
                            is_prompt_electron = True
                        if gen_track_cone_pdgid == 13:
                            is_prompt_muon = True
                        if gen_track_cone_pdgid == 15:
                            is_prompt_tau = True
                
                for k in range(len(event.GenTaus)):
                    deltaR = track.DeltaR(event.GenTaus[k])
                    is_hadronic = bool(event.GenTaus_had[k])
                    if deltaR < 0.04 and is_hadronic:
                        is_prompt_tau_hadronic = True

                # for hadronic taus, check GenTaus_LeadTrk tracks:
                for l in range(len(event.GenTaus_LeadTrk)):
                    deltaR = track.DeltaR(event.GenTaus_LeadTrk[l])
                    is_hadronic = bool(event.GenTaus_had[l])
                    if is_hadronic:
                        if deltaR < 0.04:
                            is_prompt_tau_leadtrk = True
                        if deltaR < 0.4:
                            is_prompt_tau_widecone = True

            # if signal, do chargino matching:
            chiCandGenMatchingDR = 100
            chi_isLeading = False
            chi_LabXY = -1
            chi_Gamma = -1
            chi_Beta = -1
            chi_Eta = -1
            chi_Pt = -1
            if is_signal:

                try:
                    highest_chargino_pt = 0
                    
                    for k in range(len(event.GenParticles)):
                        if abs(event.GenParticles_PdgId[k]) == 1000024:
                            deltaR = track.DeltaR(event.GenParticles[k])
                            if deltaR < chiCandGenMatchingDR:
                                chiCandGenMatchingDR = deltaR
                                if event.GenParticles[k].Pt() > highest_chargino_pt:
                                    highest_chargino_pt = event.GenParticles[k].Pt()
                                chi_LabXY = event.GenParticles_LabXYmm[k]
                                chi_Gamma = event.GenParticles[k].Gamma()
                                chi_Beta = event.GenParticles[k].Beta()
                                chi_Eta = event.GenParticles[k].Eta()
                                chi_Pt = event.GenParticles[k].Pt()
                    
                    # check if chargino is pT-leading chargino
                    if highest_chargino_pt == chi_Pt: 
                        chi_isLeading = True
                    else:
                        chi_isLeading = False

                except:
                    pass

            is_fake_track = not (is_prompt_electron or is_prompt_muon or is_prompt_tau or is_prompt_tau_leadtrk)
                    
            if chiCandGenMatchingDR<0.04:
                is_fake_track = False

            # dxy-dz-transform:
            if phase == 1 and "Run201" not in data_period and is_pixel_track and not is_fake_track:

                # only apply stretching to short prompt tracks (phase 1)

                if event.tracks_dxyVtx[iCand]<0.02:
                    tracks_dxyVtxCorrected = g_calibratedxy.Eval(event.tracks_dxyVtx[iCand])
                else:
                    tracks_dxyVtxCorrected = event.tracks_dxyVtx[iCand]

                if event.tracks_dzVtx[iCand]<0.02:
                    tracks_dzVtxCorrected = g_calibratedz.Eval(event.tracks_dzVtx[iCand])
                else:
                    tracks_dzVtxCorrected = event.tracks_dzVtx[iCand]

            else:
                tracks_dxyVtxCorrected = event.tracks_dxyVtx[iCand]
                tracks_dzVtxCorrected = event.tracks_dzVtx[iCand]

            if cutflow_study:
                # MT2-DT-tag-specifics: other leptons and tracks:
                mt2_leptoniso = True
                mt2_trackiso = True
                for collection in [event.Electrons, event.Muons]:
                    for obj in collection:
                        if track.DeltaR(obj) < 0.2:
                            mt2_leptoniso = False
                for i_track in event.tracks:
                    if i_track.Pt()>15 and track.DeltaR(i_track) < 0.1:
                        mt2_trackiso = False
                        
                # EXO-DT-tag-specifics: other tracks
                exo_trackiso = False
                ptsum = 0
                for i_track in event.tracks:
                    deltaR = track.DeltaR(i_track)
                    if deltaR > 0 and deltaR < 0.3:
                        ptsum += i_track.Pt()
                if ptsum/track.Pt() < 0.05:
                    exo_trackiso = True
                
                # EXO-DT-tag-specifics: other jets
                exo_jetiso = False
                exo_track_jet_mindeltaR = 9999
                for jet in event.Jets:
                    if jet.Pt() > 30 and abs(jet.Eta()) < 2.4:
                        deltaR = jet.DeltaR(track)
                        if deltaR < exo_track_jet_mindeltaR:
                            exo_track_jet_mindeltaR = deltaR
                if exo_track_jet_mindeltaR > 0.5:
                    exo_jetiso = True
                    
                # EXO-DT-tag-specifics: other leptons
                exo_leptoniso = True    
                for i, obj in enumerate(event.Electrons):
                    if track.DeltaR(obj) < 0.15:
                        exo_leptoniso = False
                for i, obj in enumerate(event.Muons):
                    if track.DeltaR(obj) < 0.15:
                        exo_leptoniso = False

            else:
                mt2_leptoniso = False
                mt2_trackiso = False
                exo_trackiso = False
                exo_jetiso = False
                exo_leptoniso = False    
            
            # check for nearby leptons and pions:
            pass_leptonveto = True
            for lep in goodleptons: 
                if lep.DeltaR(track)<0.1:
                    pass_leptonveto = False
                    break            

            pass_pionveto = True
            for pion in event.TAPPionTracks: 
                if pion.DeltaR(track)<0.1:
                    pass_pionveto = False
                    break            
            
            pass_jetveto = True
            for jet in goodjets:
                if not jet.Pt()>25: continue
                if jet.DeltaR(track)<0.4: 
                    pass_jetveto = False
                    break
                
            ptErrOverPt2 = event.tracks_ptError[iCand] / (track.Pt()**2)

            pass_mask = True
            if hMask!='':
                xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
                ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
                if hMask.GetBinContent(ibinx, ibiny)==0: 
                    pass_mask = False

            pass_basecuts_apart_from_leptonveto_and_PFCandVeto = pass_category and \
                        bool(event.tracks_trackQualityHighPurity[iCand]) and \
                        abs(track.Eta())<2.0 and \
                        ptErrOverPt2<10 and \
                        abs(event.tracks_dxyVtx[iCand])<0.1 and \
                        abs(event.tracks_dzVtx[iCand])<0.1 and \
                        event.tracks_trkRelIso[iCand]<0.2 and \
                        event.tracks_trackerLayersWithMeasurement[iCand]>=2 and \
                        event.tracks_nValidTrackerHits[iCand]>=2 and \
                        event.tracks_nMissingInnerHits[iCand]==0 and \
                        event.tracks_nValidPixelHits[iCand]>=2 and \
                        pass_pionveto and \
                        pass_jetveto and \
                        pass_mask
                                                
            pass_basecuts = pass_basecuts_apart_from_leptonveto_and_PFCandVeto and pass_leptonveto and bool(event.tracks_passPFCandVeto[iCand])

            # attention, skim will contain tracks with/without lepton veto, PF cand veto
            if n_goodmuons != 1 and not pass_basecuts:

                if chiCandGenMatchingDR>0.01:
                    continue
          
            # FastSim:
            fastsim_weight = 1.0
            if is_fastsim:
                # FastSim weight: apply for displacements < 30 cm
                if chi_LabXY>-1 and chi_LabXY<300:
                    fastsim_weight = 0.75
                else:
                    fastsim_weight = 1.0

                #calibfactor_dedx_fastsim
                if signal_lsp_mass > 0:
                    fastsim_dedx_factor = shared_utils.calibfactor_dedx_fastsim(int(signal_lsp_mass))
                    if fastsim_dedx_factor > 0:
                        fastsim_weight *= fastsim_dedx_factor

            # DT scale factor
            if is_pixel_track:
                signal_sf = signal_sf_short
            else:
                signal_sf = signal_sf_long

            for label in bdts:
                mva_scores[label] = get_BDT_score(label, event, iCand, readers, is_pixel_track, phase, ptErrOverPt2, event.tracks_dxyVtx[iCand], event.tracks_dzVtx[iCand])
                mva_scores[label + "_corrdxydz"] = get_BDT_score(label, event, iCand, readers, is_pixel_track, phase, ptErrOverPt2, tracks_dxyVtxCorrected, tracks_dzVtxCorrected)

            # discard tracks with BDT<-0.1:
            #if mva_scores["sep21v1_baseline_corrdxydz"]<-0.1:
            #    continue

            # if we're in either the muon TF measurement region or the prompt mu CR,
            # we want to keep tracks which fail pass_leptonveto and bool(event.tracks_passPFCandVeto[iCand])

            if n_goodmuons == 1:
                keep_this_track = False
                if pass_basecuts or (pass_basecuts_apart_from_leptonveto_and_PFCandVeto and mva_scores["sep21v1_baseline_corrdxydz"]>-0.1):
                    keep_this_track = True
                if not keep_this_track:
                    if chiCandGenMatchingDR>0.01:
                        continue
           
            tracks_massfromdeDxPixel = TMath.Sqrt((event.tracks_deDxHarmonic2pixel[iCand]-2.557)*pow(track.P(),2)/2.579)
            tracks_massfromdeDxStrips = TMath.Sqrt((event.tracks_deDxHarmonic2strips[iCand]-2.557)*pow(track.P(),2)/2.579)
            
            ## if leptons in the event, calculate invariant mass w.r.t. to leading lepton:
            #if len(goodleptons) > 0:
            #    if event.tracks_charge[iCand] * goodleptons_info[highest_lepton_pt_index]["leptons_charge"] == -1:
            #        invariant_mass = (track + goodleptons[highest_lepton_pt_index]).M()
            #    else:
            #        invariant_mass = -1
            #else:
            #    invariant_mass = -1
                                       
            DeDxCorrected = correct_dedx_intercalibration(event.tracks_deDxHarmonic2pixel[iCand], current_file_name, abs(track.Eta()), phase, is_data, fsmear_barrel, fsmear_endcap)
            
            weightOmega = weight
            if not is_data and is_fake_track:
                if is_pixel_track and phase == 0:
                    weightOmega *= 1.57
                if not is_pixel_track and phase == 0:
                    weightOmega *= 3.18
                if is_pixel_track and phase == 1:
                    weightOmega *= 6.22
                if not is_pixel_track and phase == 1:
                    weightOmega *= 11.50
                          
            tagged_tracks.append(
                                   {
                                     "tracks_is_pixel_track": is_pixel_track,
                                     "tracks_baseline": pass_basecuts,
                                     "tracks_category": pass_category,
                                     "tracks_pixelLayersWithMeasurement": event.tracks_pixelLayersWithMeasurement[iCand],
                                     "tracks_trackerLayersWithMeasurement": event.tracks_trackerLayersWithMeasurement[iCand],
                                     "tracks_nMissingInnerHits": event.tracks_nMissingInnerHits[iCand],
                                     "tracks_nMissingMiddleHits": event.tracks_nMissingMiddleHits[iCand],
                                     "tracks_nMissingOuterHits": event.tracks_nMissingOuterHits[iCand],
                                     "tracks_nValidPixelHits": event.tracks_nValidPixelHits[iCand],
                                     "tracks_nValidTrackerHits": event.tracks_nValidTrackerHits[iCand],
                                     "tracks_dxyVtx": event.tracks_dxyVtx[iCand],
                                     "tracks_dzVtx": event.tracks_dzVtx[iCand],
                                     "tracks_dxyVtxCorrected": tracks_dxyVtxCorrected,
                                     "tracks_dzVtxCorrected": tracks_dzVtxCorrected,
                                     "tracks_matchedCaloEnergy": event.tracks_matchedCaloEnergy[iCand],
                                     "tracks_trkRelIso": event.tracks_trkRelIso[iCand],
                                     "tracks_ptErrOverPt2": ptErrOverPt2,
                                     "tracks_pt": track.Pt(),
                                     "tracks_p": track.P(),
                                     "tracks_eta": track.Eta(),
                                     "tracks_phi": track.Phi(),
                                     "tracks_trkMiniRelIso": event.tracks_trkMiniRelIso[iCand],
                                     "tracks_ptError": event.tracks_ptError[iCand],
                                     "tracks_passPFCandVeto": bool(event.tracks_passPFCandVeto[iCand]),
                                     "tracks_trackQualityHighPurity": bool(event.tracks_trackQualityHighPurity[iCand]),
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
                                     #"tracks_invmass": invariant_mass,
                                     "tracks_passmask": pass_mask,
                                     "tracks_passleptonveto": pass_leptonveto,
                                     "tracks_passpionveto": pass_pionveto,
                                     "tracks_passjetveto": pass_jetveto,
                                     "tracks_mt2_trackiso": mt2_trackiso,
                                     "tracks_mt2_leptoniso": mt2_leptoniso,
                                     "tracks_exo_leptoniso": exo_leptoniso,
                                     "tracks_exo_trackiso": exo_trackiso,
                                     "tracks_exo_jetiso": exo_jetiso,
                                     "tracks_DrJetDt": event.tracks_trackJetIso[iCand],                     #trackIsoDR = getParticleIsolation(track, jets); // gets minimum deltaR
                                     "tracks_fastsimweight_LowLabXYAndDeDx": fastsim_weight,
                                     "tracks_signalsf": signal_sf,
                                     "tracks_weightOmega": weightOmega,
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

            if is_signal:
                tagged_tracks[-1]["tracks_chiCandGenMatchingDR"] = chiCandGenMatchingDR
                tagged_tracks[-1]["tracks_chiLeading"] = chi_isLeading
                tagged_tracks[-1]["tracks_chiLabXY"] = chi_LabXY
                tagged_tracks[-1]["tracks_chiGamma"] = chi_Gamma
                tagged_tracks[-1]["tracks_chiBeta"] = chi_Beta
                tagged_tracks[-1]["tracks_chiEta"] = chi_Eta
                tagged_tracks[-1]["tracks_chiPt"] = chi_Pt
                                       
            for label in mva_scores:
                tagged_tracks[-1]["tracks_mva_%s" % label] = mva_scores[label]
                
            tagged_tracks[-1]["object"] = track

            if debug:
                track_output_dict = tagged_tracks[-1]
                if track_output_dict["tracks_is_pixel_track"]:
                    if track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"] > -0.1:
                        track_debug_output += "%s short tracks_mva_sep21v1_baseline_corrdxydz %s tracks_pt %s; " % (iEv, track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"], track_output_dict["tracks_pt"])
                else:
                    if track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"] > -0.1:
                        track_debug_output += "%s long tracks_mva_sep21v1_baseline_corrdxydz %s tracks_pt %s; " % (iEv, track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"], track_output_dict["tracks_pt"])
                                               
        # keep only events with candidate tracks
        #if not trigger_study and len(tagged_tracks)==0:
        if len(tagged_tracks)==0:
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
       
        # track-level variables:
        n_tracks = len(tagged_tracks)

        # evaluate disappearing track tag:   
        n_DTShort = 0
        n_DTLong = 0
        track_pt = 0
        dedx_short = 0
        dedx_long = 0
        leadingDT_mva = -1
        leadingDT_mva_index = -1           
        weight_fastsim = 1.0
        weight_signalsf = 1.0

        for i_tagged, track_output_dict in enumerate(tagged_tracks):
            
            if track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"] > leadingDT_mva:
                leadingDT_mva = track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"]
                leadingDT_mva_index = i_tagged
            
            if track_output_dict["tracks_is_pixel_track"] and track_output_dict["tracks_baseline"]:
                if (phase == 0 and track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"] > 0.1) or (phase == 1 and track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"] > 0.15):
                    if track_output_dict["tracks_matchedCaloEnergy"] < 15 and track_output_dict["tracks_DrJetDt"]>0.2:
                        if is_signal:
                            #ignore non-chargino-matched signal tracks:
                            if track_output_dict["tracks_chiCandGenMatchingDR"]>0.01: continue

                        n_DTShort += 1
                        dedx_short = track_output_dict["tracks_deDxHarmonic2pixel"]
                        track_pt = track_output_dict["tracks_pt"]
                        if is_signal:
                            weight_fastsim *= track_output_dict["tracks_fastsimweight_LowLabXYAndDeDx"]
                        weight_signalsf *= track_output_dict["tracks_signalsf"]

            elif not track_output_dict["tracks_is_pixel_track"] and track_output_dict["tracks_baseline"]:
                if (phase == 0 and track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"] > 0.12) or (phase == 1 and track_output_dict["tracks_mva_sep21v1_baseline_corrdxydz"] > 0.08):
                    if track_output_dict["tracks_matchedCaloEnergy"]/track_output_dict["tracks_p"] < 0.20 and track_output_dict["tracks_DrJetDt"]>0.2:
                        if is_signal:
                            #ignore non-chargino-matched signal tracks:
                            if track_output_dict["tracks_chiCandGenMatchingDR"]>0.01: continue

                        n_DTLong += 1
                        dedx_long = track_output_dict["tracks_deDxHarmonic2pixel"]
                        track_pt = track_output_dict["tracks_pt"]
                        if is_signal:
                            weight_fastsim *= track_output_dict["tracks_fastsimweight_LowLabXYAndDeDx"]
                        weight_signalsf *= track_output_dict["tracks_signalsf"]


        tree_branch_values["n_DTShort"][0] = n_DTShort
        tree_branch_values["n_DTLong"][0] = n_DTLong
        tree_branch_values["n_tags"][0] = len(tagged_tracks)
        
        if leadingDT_mva_index >= 0:
            tree_branch_values["leadingDT_mva"][0] = leadingDT_mva
            tree_branch_values["leadingDT_pixeltrack"][0] = tagged_tracks[leadingDT_mva_index]["tracks_is_pixel_track"]
            tree_branch_values["leadingDT_Edep"][0] = tagged_tracks[leadingDT_mva_index]["tracks_matchedCaloEnergy"]
            tree_branch_values["leadingDT_EdepByP"][0] = tagged_tracks[leadingDT_mva_index]["tracks_matchedCaloEnergy"]/tagged_tracks[leadingDT_mva_index]["tracks_p"]
        else:
            tree_branch_values["leadingDT_mva"][0] = -1
            tree_branch_values["leadingDT_pixeltrack"][0] = -1
            tree_branch_values["leadingDT_Edep"][0] = -1
            tree_branch_values["leadingDT_EdepByP"][0] = -1
            

        if not trigger_study:
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
        
        # recalculate some event variables (Sam):
        dt = tagged_tracks[leadingDT_mva_index]["object"]
        adjustedBTags = 0
        adjustedJets = []
        adjustedHt = 0
        adjustedMht = TLorentzVector()
        adjustedMht.SetPxPyPzE(0,0,0,0)
        passJetID = True
        for ijet, jet in enumerate(event.Jets):
            if not jet.Pt()>30: continue            
            if not abs(jet.Eta())<5.0: continue###update to 2.4
            if not jet.DeltaR(dt)>0.4: continue###update to include second disappearing track
            someoverlap = False
            for jtrack in range(len(tagged_tracks)):          #with loosened BDT cut of BDT>-0.1
                dt_ = tagged_tracks[jtrack]["object"]
                if jet.DeltaR(dt_)<0.4: 
                     someoverlap = True
                     break
            if someoverlap: continue        
            adjustedMht-=jet        
            if not abs(jet.Eta())<2.4: continue###this was sitting at 2.5 until June 17, 2022, yikes. 2.4 is in TheAnalyzer.
            adjustedHt+=jet.Pt()        
            islep = False
            drlep = 99
            for ilep, lep in enumerate(goodmuons + goodelectrons):
                drlep = min(drlep, lep.DeltaR(jet))
                if drlep<0.4: 
                    islep = True
                    break
            if islep: continue
            passJetID = event.Jets_ID[ijet]
            if not passJetID: break        
            adjustedJets.append(jet)            
            if event.Jets_bJetTagDeepCSVBvsAll[ijet]>btag_cut: adjustedBTags+=1

        if not passJetID: continue

        adjustedNJets = len(adjustedJets)
            
        MinDeltaPhiMhtJets = 4
        for jet in adjustedJets:
            MinDeltaPhiMhtJets = min(MinDeltaPhiMhtJets, abs(jet.DeltaPhi(adjustedMht)))
        pt = dt.Pt()
        eta = abs(dt.Eta())
        phi = dt.Phi()
        dedxPixel = tagged_tracks[leadingDT_mva_index]["tracks_deDxHarmonic2pixel"]
                
        DedxMass = TMath.Sqrt((dedxPixel-3.01)*pow(pt*TMath.CosH(eta),2)/1.74)
        if DedxMass!=DedxMass: DedxMass = -10    

        # recalculate lepton MT:
        metvec = TLorentzVector()
        metvec.SetPtEtaPhiE(event.MET, 0, event.METPhi, event.MET) #check out feature vector in case of ttbar control region
        newmetvec = metvec.Clone()
        newmetvec -= dt
        if n_goodelectrons>0:
            mT = TMath.Sqrt(2*goodelectrons[0].Pt()*adjustedMht.Pt()*(1-TMath.Cos(goodelectrons[0].DeltaPhi(adjustedMht))))
            dt__ = dt.Clone()
            #DrJetDt = abs(goodelectrons[0].DeltaR(dt__))
            mtautau = shared_utils.mttsam1(newmetvec, goodelectrons[0], dt__)
            if goodelectrons_info[0]["leptons_charge"] * tagged_tracks[leadingDT_mva_index]["tracks_charge"] == -1:
                invmass = (goodelectrons[0] + dt__).M()
            else:
                invmass = 999        
            leppt = goodelectrons[0].Pt()
        elif n_goodmuons>0: 
            mT = TMath.Sqrt(2*goodmuons[0].Pt()*adjustedMht.Pt()*(1-TMath.Cos(goodmuons[0].DeltaPhi(adjustedMht))))
            dt__ = dt.Clone()
            #DrJetDt = abs(goodmuons[0].DeltaR(dt__))
            mtautau = shared_utils.mttsam1(newmetvec, goodmuons[0], dt__)
            if goodmuons_info[0]["leptons_charge"] * tagged_tracks[leadingDT_mva_index]["tracks_charge"] == -1:
                invmass = (goodmuons[0] + dt__).M()
            else:
                invmass = 999
            leppt = goodmuons[0].Pt()
        else: 
            mT = 999
            invmass = -1
            #DrJetDt = 999
            mtautau = 999
            leppt = 999

        #DrJetDt = tagged_tracks[leadingDT_mva_index]["tracks_DrJetDt"]

        dphiMhtDt = abs(adjustedMht.DeltaPhi(dt))
        mhtWithTrack = adjustedMht.Clone()
        mhtWithTrack-=dt
        mtDtMht = TMath.Sqrt(2*dt.Pt()*mhtWithTrack.Pt()*(1-TMath.Cos(mhtWithTrack.DeltaPhi(dt))))

        # determine SR bin using the recalculated variables:
        if n_DTShort==1 and n_DTLong==0:
            sr_bin = get_signal_region(adjustedHt, adjustedMht.Pt(), adjustedNJets, adjustedBTags, MinDeltaPhiMhtJets, 1, True, dedx_short, n_goodelectrons, n_goodmuons, current_file_name)
        elif n_DTShort==0 and n_DTLong==1:
            sr_bin = get_signal_region(adjustedHt, adjustedMht.Pt(), adjustedNJets, adjustedBTags, MinDeltaPhiMhtJets, 1, False, dedx_long, n_goodelectrons, n_goodmuons, current_file_name)
        elif (n_DTShort + n_DTLong)>=2:
            sr_bin = get_signal_region(adjustedHt, adjustedMht.Pt(), adjustedNJets, adjustedBTags, MinDeltaPhiMhtJets, n_DTShort+n_DTLong, False, dedx_long, n_goodelectrons, n_goodmuons, current_file_name)
        else:
            sr_bin = 0

        # determine extra event cuts:
        if sr_bin>0:
            if not (MinDeltaPhiMhtJets>0.4 and mtDtMht>20):
                sr_bin = 0
            elif (n_goodelectrons+n_goodmuons)>0 and not mT>110:
                sr_bin = 0
            elif (n_goodelectrons+n_goodmuons)>0 and not invmass>140:
                sr_bin = 0
            elif (n_goodelectrons+n_goodmuons)>0 and not tree_branch_values["leadinglepton_pt"][0]>40:
                sr_bin = 0

        if debug and track_debug_output != "":
            print "%s sr=%s" % (track_debug_output, sr_bin)

        if sr_bin > 0 and not is_signal:
            print "DTSR", sr_bin, current_file_name, event.RunNum, event.LumiBlockNum, event.EvtNum, track_pt
                   
        # calculate trigger efficiency with adjustedMht.Pt():
        weight_trigger = -1
        if n_goodleptons>=1:
            if tree_branch_values["leadinglepton_type"][0] == 11:
                #weight_trigger = h_triggereff_sel.GetBinContent(h_triggereff_sel.FindBin(adjustedMht.Pt()))
                xax, yax = h_triggereff_sel.GetXaxis(), h_triggereff_sel.GetYaxis()
                ibinx, ibiny = xax.FindBin(adjustedMht.Pt()), yax.FindBin(tree_branch_values["leadinglepton_pt"][0])
                weight_trigger = h_triggereff_sel.GetBinContent(ibinx, ibiny)
            elif tree_branch_values["leadinglepton_type"][0] == 13:
                #weight_trigger = h_triggereff_smu.GetBinContent(h_triggereff_smu.FindBin(adjustedMht.Pt()))
                xax, yax = h_triggereff_smu.GetXaxis(), h_triggereff_smu.GetYaxis()
                ibinx, ibiny = xax.FindBin(adjustedMht.Pt()), yax.FindBin(tree_branch_values["leadinglepton_pt"][0])
                weight_trigger = h_triggereff_smu.GetBinContent(ibinx, ibiny)
        else:
            if adjustedNJets <= 2:
                weight_trigger = h_triggereff_mht_lowjets.GetBinContent(h_triggereff_mht_lowjets.FindBin(adjustedMht.Pt()))
            if adjustedNJets >= 3:
                weight_trigger = h_triggereff_mht_highjets.GetBinContent(h_triggereff_mht_highjets.FindBin(adjustedMht.Pt()))

        if n_DTShort+n_DTLong>=2:
            print "n_DT=", n_DTShort+n_DTLong, sr_bin
            print adjustedHt, adjustedMht.Pt(), adjustedNJets, adjustedBTags, MinDeltaPhiMhtJets, n_DTShort+n_DTLong, False, dedx_long, n_goodelectrons, n_goodmuons, current_file_name
            print "MinDeltaPhiMhtJets, mtDtMht", MinDeltaPhiMhtJets, mtDtMht
            print "sr_bin", sr_bin 


        if is_pmssm and write_only_sparse and sr_bin>0:
                                    
            fill_sparse(event, sr_bin, event.puWeight, hnsparse)
            fill_sparse(event, sr_bin, event.puWeight * FastSimWeightPR31285To36122, hnsparse_fastSimWeightPR31285To36122)
            fill_sparse(event, sr_bin, event.puWeight * weight_fastsim, hnsparse_fastsimweightLowLabXYAndDeDx)
            fill_sparse(event, sr_bin, event.puWeight * weight_trigger, hnsparse_triggerweight)
            fill_sparse(event, sr_bin, event.puWeight * weight_signalsf, hnsparse_signalscalefactor)
            fill_sparse(event, sr_bin, event.puWeight * weight_sfbtagnom, hnsparse_btaggingSF)
            fill_sparse(event, sr_bin, event.puWeight * weight_isrnom, hnsparse_ISRSF)
            weight_combined = event.puWeight * weight_fastsim * FastSimWeightPR31285To36122 * weight_trigger * weight_signalsf * weight_isrnom * weight_sfbtagnom
            fill_sparse(event, sr_bin, weight_combined, hnsparse_allweights)


        # save event-level variables:
        if is_data:
            tree_branch_values["RunNum"][0] = event.RunNum
            tree_branch_values["LumiBlockNum"][0] = event.LumiBlockNum
            tree_branch_values["EvtNum"][0] = event.EvtNum
        tree_branch_values["pass_baseline"][0] = passed_baseline_selection
        tree_branch_values["n_goodelectrons"][0] = n_goodelectrons
        tree_branch_values["n_goodmuons"][0] = n_goodmuons
        #tree_branch_values["n_btags"][0] = event.BTags
        #tree_branch_values["n_goodjets"][0] = n_goodjets
        #tree_branch_values["MHT"][0] = event.MHT
        #tree_branch_values["HT"][0] = event.HT
        tree_branch_values["n_btags"][0] = adjustedBTags
        tree_branch_values["n_goodjets"][0] = adjustedNJets
        tree_branch_values["MHT"][0] = adjustedMht.Pt()
        tree_branch_values["HT"][0] = adjustedHt
        tree_branch_values["n_allvertices"][0] = event.nAllVertices
        tree_branch_values["PFCaloMETRatio"][0] = event.PFCaloMETRatio
        tree_branch_values["MET"][0] = event.MET
        tree_branch_values["weight"][0] = weight
        tree_branch_values["sr"][0] = sr_bin
        tree_branch_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets
        tree_branch_values["invmass"][0] = invmass
        tree_branch_values["leptonmt"][0] = mT
        tree_branch_values["mtautau"][0] = mtautau
        tree_branch_values["dphiMhtDt"][0] = dphiMhtDt
        tree_branch_values["mtDtMht"][0] = mtDtMht
        tree_branch_values["FastSimWeightPR31285To36122"][0] = FastSimWeightPR31285To36122

        if not is_data:
            tree_branch_values["madHT"][0] = madHT
            tree_branch_values["CrossSection"][0] = event.CrossSection
            tree_branch_values["puWeight"][0] = event.puWeight
            tree_branch_values["n_genLeptons"][0] = n_genLeptons
            tree_branch_values["n_genElectrons"][0] = n_genElectrons
            tree_branch_values["n_genMuons"][0] = n_genMuons
            tree_branch_values["n_genTaus"][0] = n_genTaus
        if is_signal:
            tree_branch_values["signal_stop_mass"][0] = signal_stop_mass
            tree_branch_values["signal_gluino_mass"][0] = signal_gluino_mass
            tree_branch_values["signal_lsp_mass"][0] = signal_lsp_mass
            tree_branch_values["chargino_parent_mass"][0] = chargino_parent_mass        
       
        # update event vector and check event selection regions:
        if False:
            for tree_branch_value_label in tree_branch_values:
                if "tracks_" not in tree_branch_value_label and "leptons_" not in tree_branch_value_label:
                    value = tree_branch_values[tree_branch_value_label][0]
                    exec("event.%s=%s" % (tree_branch_value_label, value) )

            # loop over all event selections:
            analysisregion = 0
            for mode in event_selections:
                for event_selection in event_selections[mode]:
                    for region in regions:
                        analysisregion += 1

                        if "gen" in region and is_data: continue

                        # build cutstring
                        cutstring = event_selections[mode][event_selection] + " and " + regions[region]
                        for tagged_track_label in tagged_tracks[0]:
                            cutstring = cutstring.replace("event." + tagged_track_label + "[i_track]", "tagged_tracks[i_track]['%s']" % tagged_track_label)

                        # check
                        for i_track in range(len(tagged_tracks)):
                            if eval(cutstring):
                                #print current_file_name, iEv, event_selection, region, "sr=%s" % sr_bin, "pt=%s" % tagged_tracks[i_track]['tracks_pt']
                                # save track-level properties again:
                                tree_branch_values["tracks_analysisregion"][i_track] = analysisregion

        tout.Fill()

    if mixed_masked_file:
        print "mixed_masked_file"

    if not (lumi_report or write_only_sparse):
        fout.cd()
        h_nev.Write()
        fout.Write()
        fout.Close()
                            
    # write JSON containing lumisections:
    json_compact = True
    json_filename = track_tree_output.replace(".root", ".json")

    #sort lumisection blocks:
    for run in runs:
        runs[run] = natsorted(runs[run])

    if json_compact:
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

            runs = runs_compacted

        #json_content = json.dumps(runs_compacted)

    if lumi_report:
        #if json_compact:
        #    json_content = json.dumps(runs_compacted)
        #else:
        json_content = json.dumps(runs)
        with open(json_filename, "w") as fo:
            fo.write(json_content)

        if lumi_report:
            with open(json_filename.replace(".json", ".dat"), "w") as fo:
                content = ""
                for i_file in runs_fileinfo:
                    content += "%s: %s\n" % (i_file.split("/")[-1], str(runs_fileinfo[i_file]).replace("L", ""))
                fo.write(content)

        #if False:
        #    processed_files = "\n".join(event_tree_filenames) + "\n"
        #    for run in runs:
        #        lumis = runs[run]
        #        lumis_string = ""
        #        for lumi in lumis:
        #            lumis_string += str(int(lumi)) + ","
        #        lumis_string = lumis_string[:-2]
        #        processed_files += "%s:%s\n" % (run, lumis_string)
        #    print "@@@@@@@"
        #    print processed_files
        #    print "@@@@@@@"

    if not lumi_report and is_pmssm and write_only_sparse:
        sparse_filename = track_tree_output.replace(".root", "_sparse.root")
        fout = TFile(sparse_filename, "recreate")
        fout.cd()
        hnsparse.Write()
        hnsparse_fastSimWeightPR31285To36122.Write()
        hnsparse_fastsimweightLowLabXYAndDeDx.Write()
        hnsparse_triggerweight.Write()
        hnsparse_signalscalefactor.Write()
        hnsparse_btaggingSF.Write()
        hnsparse_ISRSF.Write()
        hnsparse_allweights.Write()
        fout.Close()

    print "Finished"


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles")
    parser.add_option("--output", dest = "outputfiles")
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--test", dest = "test", action = "store_true")
    parser.add_option("--debug", dest = "debug", action = "store_true")
    parser.add_option("--overwrite", dest = "overwrite", action = "store_true")
    parser.add_option("--cutflow", dest = "cutflow_study", action = "store_true")
    parser.add_option("--trigger_study", dest = "trigger_study", action = "store_true")
    parser.add_option("--lumi_report", dest = "lumi_report", action = "store_true")
    parser.add_option("--sparse", dest = "sparse_only", action = "store_true")
    parser.add_option("--syst", dest = "syst", default = "")    
    (options, args) = parser.parse_args()
    
    print sys.argv[0], ' '.join( [pipes.quote(s) for s in sys.argv[1:]] )

    if not options.test:
        main(
             options.inputfiles.split(","),
             options.outputfiles,
             nevents = int(options.nev),
             overwrite = options.overwrite,
             cutflow_study = options.cutflow_study,
             debug = options.debug,
             syst = options.syst,
             trigger_study = options.trigger_study,
             lumi_report = options.lumi_report,
             write_only_sparse = options.sparse_only,
            )

    else:
        inputfiles = [
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2016B-17Jul2018_ver2-v1.METAOD_90000-BCA4BDEF-639F-E711-97DF-008CFAE45430_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2016B-17Jul2018_ver2-v1.METAOD_90000-BCA4BDEF-639F-E711-97DF-008CFAE45430_RA2AnalysisTree.root",
                      # "/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2017B-31Mar2018-v1.METAOD_50000-1CAE1898-3EE4-E711-9332-B083FED13C9E_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2018A-17Sep2018-v1.EGammaAOD0_100000-1C45FE2D-8A85-DD43-95F6-1EF8F880B71B_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/ProductionRun2v3/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_120000-40EE4B49-34BB-E611-A332-001E674FB2D4_RA2AnalysisTree.root"],
                      #['/pnfs/desy.de/cms/tier2/store/user/tokramer/NtupleHub/ProductionRun2v3/Run2016F-17Jul2018-v1.JetHTAOD_70000-001A7F04-DE7C-E711-95AA-0025905D1E08_RA2AnalysisTree.root', '/pnfs/desy.de/cms/tier2/store/user/tokramer/NtupleHub/ProductionRun2v3/Run2016F-17Jul2018-v1.JetHTAOD_110000-E81D89E0-097F-E711-B8EB-0025905A48F2_RA2AnalysisTree.root'],
                      #["/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/ProductionRun2v3/Run2017B-31Mar2018-v1.SingleMuonAOD0_60000-C6289DD6-95D7-E711-B4E1-02163E01A723_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/tokramer/NtupleHub/ProductionRun2v3/Run2016F-17Jul2018-v1.SingleElectronAOD_10000-9416936D-D78E-E711-AD34-E0DB55FC1055_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/tokramer/NtupleHub/ProductionRun2v3/RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8AOD_10000-F8CE1FD1-D253-E811-A8C1-0242AC130002_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIAutumn18FSv3.SMS-T2tb-LLChipm-ctau10to200-mStop-400to1750-mLSP0to1650_test1-211121_205321-0001-SUS-RunIIAutumn18FSPremix-00156_1040_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8-AOD_110000-6C09F057-3A3B-E911-98B8-FA163E453D6D_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_240000-043F9F4D-DA87-E911-A393-0242AC1C0502_RA2AnalysisTree.root"],
                      ["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIAutumn18FS.PMSSM_set_1_LL_TuneCP2_13TeV-pythia8-AOD0_00000-02A2CB75-DFA0-1E49-8D7E-699CD06E1182_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIAutumn18FS.PMSSM_set_1_LL_TuneCP2_13TeV-pythia8-AOD0_00000-02A2CB75-DFA0-1E49-8D7E-699CD06E1182_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIAutumn18FS.SMS-T1btbt-LLC1_ctau10to200-mGluino-1000to2800-mLSP0to2800_TuneCP2_13TeV-madgraphMLM-pythia8-AOD_2510000-97E47666-139B-454F-8CC0-97767A14F1FF_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_260000-665AE9C6-5DA5-E911-AF5E-B499BAAC0626_RA2AnalysisTree.root"],
                      #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8-AOD_110000-18089184-3A3B-E911-936C-0025905A60BC_RA2AnalysisTree.root"],
                     #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3_SMS2/RunIIAutumn18FSv3.SMS-T2bt-LLChipm-ctau10to200-mStop-400to1750-mLSP0to1650_test1-211116_013727-0005-SUS-RunIIAutumn18FSPremix-00155_5340_RA2AnalysisTree.root"],
                     #["/pnfs/desy.de/cms/tier2/store/user/vkutzner/NtupleHub/ProductionRun2v3/Run2018A-17Sep2018-v1.METAOD_60000-F8C6C719-37E2-864D-8ADE-58CC8AF130C1_RA2AnalysisTree.root"],
                     ]
         
        # ROC curve tests:
        #inputfiles = [glob.glob("/pnfs/desy.de/cms/tier2/store/user/ynissan/NtupleHub/ProductionRun2v3/Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8AOD_*root")[:10]]
        #options.cutflow_study = True
        
        for inputfile in inputfiles: 
            outputfile = inputfile[0].split("/")[-1]
            print "Testing file:\n%s" % inputfile
            main(
                 inputfile,
                 outputfile,
                 nevents = int(options.nev),
                 overwrite = True,
                 debug = options.debug,
                 syst = options.syst,
                 cutflow_study = options.cutflow_study,
                 trigger_study = options.trigger_study,
                 lumi_report = options.lumi_report,
                 write_only_sparse = options.sparse_only,
                )
