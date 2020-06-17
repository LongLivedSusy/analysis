#!/usr/bin/env python
import glob
from ROOT import *
from optparse import OptionParser

def train(skim_folder, category, is_dxyinformed, use_chi2, n_ntuple_files_sg = 1, n_ntuple_files_bg = 20):

    # in order to start TMVA
    TMVA.Tools.Instance()
        
    # open input file, get trees, create output file
    weights = {} 
    trees = {} 
    
    def add_tree(trees, weights, label, globstring):
        
        # automated lines such as:
        #trees["signal"] = TChain("Events")
        #trees["signal"].Add(skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-AOD_130000-0012E188-47A6-E911-8452-0CC47A78A456_skim.root")
        #weights["signal"] = 1.0
        
        nev = 0
        samplefiles = glob.glob(globstring)
        for samplefile in samplefiles:
            ifin = TFile(samplefile, "read")
            h_nev = ifin.Get("nev")
            nev += h_nev.GetBinContent(1)
            ifin.Close()
        
        xsecPuWeight = -1
        for i in range(1):
            ifin = TFile(samplefiles[i], "read")
            tree = ifin.Get("Events")
            for event in tree:
                xsecPuWeight = event.weight
                break
            ifin.Close()
            if xsecPuWeight>-1: break
        
        weights[label] = 1.0 * xsecPuWeight / nev
        print "weights[%s]=%s" % (label, weights[label])
        
        trees[label] = TChain("Events")
        for i, samplefile in enumerate(samplefiles):
            if "Signal" in label and i>=n_ntuple_files_sg: break
            if "Signal" not in label and i>=n_ntuple_files_bg: break
            trees[label].Add(samplefile)
    
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1000", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1075", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1075_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1175", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1175_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1200", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1275", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1275_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1300", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1375", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1375_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1475", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1475_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1500", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-150", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1575", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1575_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1600", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1675", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1675_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1700", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1775", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1775_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1800", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1875", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1875_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1900", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1900_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1975", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1975_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2000", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-200", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2075", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2075_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2100", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2100_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2175", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2175_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2275", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2275_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2300", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2300_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2375", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2375_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2400", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2400_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2475", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2475_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2575", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2575_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-25", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-25_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2600", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2600_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2675", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2675_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2700", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2700_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2775", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2775_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-400", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-50", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-600", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-75", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-75_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-800", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-900", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-975", skim_folder + "/RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-975_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1000", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1100", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1200", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1300", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1400", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1500", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-150", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1600", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1700", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1800", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1900", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1900_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-1", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-2000", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-200", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-50", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-600", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-800", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV*.root")
    add_tree(trees, weights, "Signal_ctau-200_mLSP-900", skim_folder + "/RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV*.root")
    
    add_tree(trees, weights, "WJetsToLNu_TuneCUETP8M1", skim_folder + "/Summer16.WJetsToLNu_TuneCUETP8M1*.root")
    add_tree(trees, weights, "WJetsToLNu_HT-200To400_TuneCUETP8M1", skim_folder + "/Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1*.root")
    add_tree(trees, weights, "WJetsToLNu_HT-600To800_TuneCUETP8M1", skim_folder + "/Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1*.root")
    add_tree(trees, weights, "WJetsToLNu_HT-800To1200_TuneCUETP8M1", skim_folder + "/Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1*.root")
    add_tree(trees, weights, "WJetsToLNu_HT-1200To2500_TuneCUETP8M1", skim_folder + "/Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1*.root")
    add_tree(trees, weights, "WJetsToLNu_HT-2500ToInf_TuneCUETP8M1", skim_folder + "/Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1*.root")
    add_tree(trees, weights, "DYJetsToLL_M-50_TuneCUETP8M1", skim_folder + "/Summer16.DYJetsToLL_M-50_TuneCUETP8M1*.root")
    add_tree(trees, weights, "DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1", skim_folder + "/Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1*.root")
    add_tree(trees, weights, "DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1", skim_folder + "/Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1*.root")
    add_tree(trees, weights, "DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1", skim_folder + "/Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1*.root")
    add_tree(trees, weights, "DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1", skim_folder + "/Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1*.root")
    add_tree(trees, weights, "DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1", skim_folder + "/Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1*.root")
    add_tree(trees, weights, "DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1", skim_folder + "/Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1*.root")
    add_tree(trees, weights, "DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1", skim_folder + "/Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1*.root")
    add_tree(trees, weights, "TTJets_DiLept", skim_folder + "/Summer16.TTJets_DiLept*.root")
    add_tree(trees, weights, "TTJets_SingleLeptFromT", skim_folder + "/Summer16.TTJets_SingleLeptFromT*.root")
    add_tree(trees, weights, "TTJets_SingleLeptFromTbar", skim_folder + "/Summer16.TTJets_SingleLeptFromTbar*.root")
    #add_tree(trees, weights, "QCD_HT200to300_TuneCUETP8M1", skim_folder + "/QCD_HT200to300_TuneCUETP8M1*.root")
    #add_tree(trees, weights, "QCD_HT300to500_TuneCUETP8M1", skim_folder + "/QCD_HT200to300_TuneCUETP8M1*.root")
    #add_tree(trees, weights, "QCD_HT500to700_TuneCUETP8M1", skim_folder + "/QCD_HT500to700_TuneCUETP8M1*.root")
    #add_tree(trees, weights, "QCD_HT700to1000_TuneCUETP8M1", skim_folder + "/QCD_HT700to1000_TuneCUETP8M1*.root")
    #add_tree(trees, weights, "QCD_HT1000to1500_TuneCUETP8M1", skim_folder + "/QCD_HT1000to1500_TuneCUETP8M1*.root")
    #add_tree(trees, weights, "QCD_HT1500to2000_TuneCUETP8M1", skim_folder + "/QCD_HT1500to2000_TuneCUETP8M1*.root")
    #add_tree(trees, weights, "QCD_HT2000toInf_TuneCUETP8M1", skim_folder + "/QCD_HT2000toInf_TuneCUETP8M1*.root")
    add_tree(trees, weights, "ZZ_TuneCUETP8M1", skim_folder + "/Summer16.ZZ_TuneCUETP8M1*.root")
    add_tree(trees, weights, "WW_TuneCUETP8M1", skim_folder + "/Summer16.WW_TuneCUETP8M1*.root")
    add_tree(trees, weights, "WZ_TuneCUETP8M1", skim_folder + "/Summer16.WZ_TuneCUETP8M1*.root")
    
    fout = TFile("output.root", "recreate")
    
    # define factory with options
    factory = TMVA.Factory("TMVAClassification", fout,
                                ":".join([    "!V",
                                              "!Silent",
                                              "Color",
                                              "DrawProgressBar",
                                              "Transformations=I;D;P;G,D",
                                              "AnalysisType=Classification"]
                                         ))
                                         
    # add discriminating variables for training
    dataloader = TMVA.DataLoader("dataset")
    if is_dxyinformed:
        dataloader.AddVariable("tracks_dxyVtx", "F")
    dataloader.AddVariable("tracks_dzVtx", "F")
    dataloader.AddVariable("tracks_matchedCaloEnergy", "F")
    dataloader.AddVariable("tracks_trkRelIso", "F")
    dataloader.AddVariable("tracks_nValidPixelHits", "I")
    if category == "long":
        dataloader.AddVariable("tracks_nValidTrackerHits", "I")
    if category == "long":
        dataloader.AddVariable("tracks_nMissingOuterHits", "I")
    dataloader.AddVariable("tracks_ptErrOverPt2", "F")
    if use_chi2:
        dataloader.AddVariable("tracks_chi2perNdof", "F")
    
    # define signal and background trees
    for label in trees:
        if "Signal" in label:
            dataloader.AddSignalTree(trees[label], weights[label])
        else:
            dataloader.AddBackgroundTree(trees[label], weights[label])
    
    # define additional cuts 
    baseline_selection = [
        "abs(tracks_eta)<2.4",   
        "!(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566)",                              
        "tracks_highpurity==1",  
        "tracks_ptErrOverPt2<10",
        "tracks_dzVtx<0.1",      
        "tracks_trkRelIso<0.2",  
        "tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2",           
        "tracks_nMissingInnerHits==0",                                                     
        "tracks_nValidPixelHits>=3",    
        #"tracks_nMissingMiddleHits==0",
        #"tracks_chi2perNdof<2.88",
        #"tracks_pixelLayersWithMeasurement>=2",
        #"tracks_passmask==1",
        "tracks_pass_reco_lepton==1",
        "tracks_passPFCandVeto==1",                                   
        #"tracks_passpionveto==1",
        #"tracks_passjetveto==1",
             ]
             
    ##old_baseline_selection:
    #baseline_selection = [
    #    "abs(tracks_eta)<2.4",   
    #    "tracks_highpurity==1",  
    #    "tracks_ptErrOverPt2<10",
    #    "tracks_dzVtx<0.1",      
    #    "tracks_trkRelIso<0.2",  
    #    "tracks_nMissingMiddleHits==0",                                                     
    #    "tracks_passPFCandVeto==1",                                                        
    #         ]
    
    if is_dxyinformed:
        baseline_selection.append("tracks_dxyVtx<0.1")
    
    if category == "short":
        cuts = "tracks_is_pixel_track==1 && " + " && ".join(baseline_selection)
    elif category == "long":
        cuts = "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && " + " && ".join(baseline_selection)
    
    if category == "short":
        sigCut = TCut("tracks_chiCandGenMatchingDR<0.01 && " + cuts)
    elif category == "long":
        sigCut = TCut("tracks_chiCandGenMatchingDR<0.01 && " + cuts)
    
    bgCut = TCut(cuts)
    
    # set options for trainings
    dataloader.PrepareTrainingAndTestTree(sigCut, 
                                       bgCut, 
                                       ":".join(["nTrain_Signal=0",
                                                 "nTrain_Background=0",
                                                 "SplitMode=Random",
                                                 "NormMode=NumEvents",
                                                 "!V"
                                                 ]))
    
    ## book and define methods that should be trained
    method = factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT",
                                ":".join([ "!H",
                                           "!V",
                                           "NTrees=200",
                                           "MaxDepth=4",
                                           "BoostType=AdaBoost",
                                           "AdaBoostBeta=0.5",
                                           "SeparationType=GiniIndex",
                                           #"nCuts=20",
                                           "PruneMethod=NoPruning",
                                           ]))
    
    # self-explaining
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--skim_folder", dest = "skim_folder", default = "/afs/desy.de/user/k/kutznerv/dust/shorttrack/analysis/ntupleanalyzer/skim_19")
    parser.add_option("--category", dest = "category")
    parser.add_option("--dxyinformed", dest = "dxyinformed", action = "store_true")
    parser.add_option("--use_chi2", dest = "use_chi2", action = "store_true")
    (options, args) = parser.parse_args()
    
    train(options.skim_folder,
          options.category,
          options.dxyinformed,
          options.use_chi2,
         )
