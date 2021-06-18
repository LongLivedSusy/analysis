#!/usr/bin/env python
import glob
from ROOT import *
from optparse import OptionParser
import os

def add_tree(trees, weights, skim_folder, label, n_ntuple_files_sg, n_ntuple_files_bg, equalSgXsec = False, xsecinv = False):
            
    globstring = skim_folder + "/" + label + "*.root"
    
    print globstring
    
    nev = 0
    samplefiles = glob.glob(globstring)
    for samplefile in samplefiles:
        ifin = TFile(samplefile, "read")
        h_nev = ifin.Get("nev")
        nev += h_nev.GetBinContent(1)
        ifin.Close()
    
    xsecPuWeight = -1
    ifin = TFile(samplefiles[0], "read")
    tree = ifin.Get("Events")
    for event in tree:
        xsecPuWeight = event.CrossSection
        #xsecPuWeight = event.weight
        break
    ifin.Close()
    
    label = label.split(".")[-1]

    if equalSgXsec:
        weights[label] = 1.0 / nev
        print "Using equal signal xsection (=1pb)"
    elif xsecinv:
        weights[label] = 1.0 / (xsecPuWeight * nev)
        #weights[label] = "puWeight/(CrossSection*%s)" % nev
        print "Using inverted signal xsections"
    else:
        weights[label] = 1.0 * xsecPuWeight / nev
        #weights[label] = "puWeight*CrossSection/%s" % nev
    print "weights[%s]=%s" % (label, weights[label])
    
    trees[label] = TChain("Events")
    for i, samplefile in enumerate(samplefiles):
        if n_ntuple_files_sg>0 and "SMS" in label and i>=n_ntuple_files_sg: break
        if n_ntuple_files_sg>0 and "SMS" not in label and i>=n_ntuple_files_bg: break
        trees[label].Add(samplefile)


def train(skim_folder, category, is_dxyinformed, use_chi2, phase, equalSgXsec = False, noVetoes = False, n_ntuple_files_sg = -1, n_ntuple_files_bg = -1):

    cwd = os.getcwd()

    output_filename = "output.root"
    #if os.stat(output_filename).st_size>1e6:
    #    print "Already done"
    #    quit(0)
        
    # in order to start TMVA
    TMVA.Tools.Instance()
        
    # open input file, get trees, create output file
    weights = {} 
    trees = {} 

    print "Training BDT for phase %s..." % phase
        
    if phase == 0:
    
        labels = [
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1075_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1275_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1375_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1475_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1575_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1675_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1775_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1875_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1975_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2075_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2275_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2375_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2475_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2575_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-25_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2675_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-2775_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-75_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "RunIISummer16MiniAODv3.SMS-T1qqqq-LLChipm_ctau-200_mLSP-975_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            "Summer16.WJetsToLNu_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1",
            "Summer16.TTJets_DiLept",
            "Summer16.TTJets_SingleLeptFromT",
            "Summer16.TTJets_SingleLeptFromTbar",
            "Summer16.ZZ_TuneCUETP8M1",
            "Summer16.WW_TuneCUETP8M1",
            "Summer16.WZ_TuneCUETP8M1",
            ]
        
    if phase == 1:
        
        labels = [
            "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-10_TuneCP2_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-50_TuneCP2_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV-madgraphMLM-pythia8ext1",
            #"RunIIFall17MiniAODv2.GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",
            #"RunIIFall17MiniAODv2.QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",
            #"RunIIFall17MiniAODv2.QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",
            #"RunIIFall17MiniAODv2.QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8",
            #"RunIIFall17MiniAODv2.QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",
            #"RunIIFall17MiniAODv2.QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",
            #"RunIIFall17MiniAODv2.QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",
            #"RunIIFall17MiniAODv2.TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
            #"RunIIFall17MiniAODv2.TTGamma_Dilept_TuneCP5_PSweights_13TeV_madgraph_pythia8",
            #"RunIIFall17MiniAODv2.TTGamma_SingleLeptFromT_TuneCP5_PSweights_13TeV_madgraph_pythia8",
            #"RunIIFall17MiniAODv2.TTGamma_SingleLeptFromTbar_TuneCP5_PSweights_13TeV_madgraph_pythia8",
            #"RunIIFall17MiniAODv2.TTHH_TuneCP5_13TeV-madgraph-pythia8",
            "RunIIFall17MiniAODv2.TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.TTJets_DiLept_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.TTJets_SingleLeptFromT_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.TTJets_SingleLeptFromTbar_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.TTJets_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",
            #"RunIIFall17MiniAODv2.TTTW_TuneCP5_13TeV-madgraph-pythia8",
            #"RunIIFall17MiniAODv2.TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8",
            #"RunIIFall17MiniAODv2.TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8",
            #"RunIIFall17MiniAODv2.TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8",
            #"RunIIFall17MiniAODv2.TTWZ_TuneCP5_13TeV-madgraph-pythia8",
            #"RunIIFall17MiniAODv2.TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
            #"RunIIFall17MiniAODv2.TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8",
            #"RunIIFall17MiniAODv2.TTZZ_TuneCP5_13TeV-madgraph-pythia8",
            "RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
            "RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",
            #"RunIIFall17MiniAODv2.WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
            #"RunIIFall17MiniAODv2.WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
            #"RunIIFall17MiniAODv2.WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_v2",
            #"RunIIFall17MiniAODv2.WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
            #"RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
            #"RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
            #"RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400_13TeV-madgraph",
            #"RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
            #"RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
            #"RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800_13TeV-madgraph",
            #"RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
            #"RunIIFall17MiniAODv2.ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8.root",
            ]
        
    if "-inverted" in cwd:
        xsecinv = True
        equalSgXsec = False
    else:
        xsecinv = False        
    
        
    for label in labels:
        if "SMS" in label:
            add_tree(trees, weights, skim_folder, label, n_ntuple_files_sg, n_ntuple_files_bg, equalSgXsec = equalSgXsec, xsecinv = xsecinv)    
        else:
            add_tree(trees, weights, skim_folder, label, n_ntuple_files_sg, n_ntuple_files_bg)    

    fout = TFile(output_filename, "recreate")
    
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
    #dataloader.AddVariable("tracks_matchedCaloEnergy", "F")
    dataloader.AddVariable("tracks_trkRelIso", "F")
    if category == "long":
        dataloader.AddVariable("tracks_nValidPixelHits", "I")
        dataloader.AddVariable("tracks_nValidTrackerHits", "I")
    if category == "long":
        dataloader.AddVariable("tracks_nMissingOuterHits", "I")
    dataloader.AddVariable("tracks_ptErrOverPt2", "F")
    if use_chi2:
        dataloader.AddVariable("tracks_chi2perNdof", "F")
    
    # define signal and background trees
    signal_added = False
    for label in trees:
        if "SMS" in label:
            print "adding signal tree:", label
            dataloader.AddSignalTree(trees[label], weights[label])
            signal_added = True
        else:
            print "adding background tree:", label
            dataloader.AddBackgroundTree(trees[label], weights[label])
    
    if not signal_added:
        print "?"
        quit()

    # baseline selection as applied in skim    

    #pass_basecuts = bool(event.tracks_trackQualityHighPurity[iCand]) and \
    #            abs(track.Eta())<2.0 and \
    #            ptErrOverPt2<10 and \
    #            abs(event.tracks_dzVtx[iCand])<0.1 and \
    #            event.tracks_trkRelIso[iCand]<0.2 and \
    #            event.tracks_trackerLayersWithMeasurement[iCand]>=2 and \
    #            event.tracks_nValidTrackerHits[iCand]>=2 and \
    #            event.tracks_nMissingInnerHits[iCand]==0 and \
    #            bool(event.tracks_passPFCandVeto[iCand]) and \
    #            event.tracks_nValidPixelHits[iCand]>=2
    
    if noVetoes:
        vetoes = ""
        print "Ignoring vetoes..."
    else:
        vetoes = " && tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_passleptonveto==1 "
    
    if category == "short":
        #cuts = "tracks_pt>15 && tracks_is_pixel_track==1 && tracks_chi2perNdof>0 && tracks_chi2perNdof<999999"
        cuts = "tracks_pt>15 && tracks_is_pixel_track==1 && tracks_chi2perNdof>0 && tracks_chi2perNdof<999999" + vetoes
    elif category == "long":
        #cuts = "tracks_pt>30 && tracks_is_pixel_track==0 && tracks_passjetveto==1 && tracks_chi2perNdof>0 && tracks_chi2perNdof<999999"
        cuts = "tracks_pt>40 && tracks_is_pixel_track==0 && tracks_chi2perNdof>0 && tracks_chi2perNdof<999999" + vetoes

    if is_dxyinformed:
        cuts += " && tracks_dxyVtx<0.1"
    
    # signal test:
    if "-compressed" in cwd:
        extra_sig_cuts = " signal_gluino_mass==2400 && signal_lsp_mass==2000 && "     #Glu1000_Chi1ne600.root
    elif "-boosted" in cwd:
        extra_sig_cuts = " signal_gluino_mass==1000 && signal_lsp_mass==600 && "      #Glu1000_Chi1ne600.root
    elif "-corner" in cwd:
        extra_sig_cuts = " signal_gluino_mass==2400 && signal_lsp_mass==600 && "      #Glu2400_Chi1ne600.root
    else:
        extra_sig_cuts = ""
        
    if category == "short":
        sigCut = TCut(extra_sig_cuts + "tracks_chiCandGenMatchingDR<0.01 && " + cuts)
    elif category == "long":
        sigCut = TCut(extra_sig_cuts + "tracks_chiCandGenMatchingDR<0.01 && " + cuts)

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

    # try to get ntrees and ndepth from folder name
    if "ntrees" in cwd and "ndepth" in cwd:
        ntrees = cwd.split("ntrees")[1]
        ndepth = cwd.split("ndepth")[1].split("-")[0]
    else:
        ntrees = 200
        ndepth = 4

    print "Using ntrees=%s, %s" % (ntrees, ndepth)

    ## book and define methods that should be trained
    method = factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT",
                                ":".join([ "!H",
                                           "!V",
                                           "NTrees=%s" % ntrees,
                                           "MaxDepth=%s" % ndepth,
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
    parser.add_option("--path", dest = "skim_folder")
    parser.add_option("--category", dest = "category")
    parser.add_option("--dxyinformed", dest = "dxyinformed", action = "store_true")
    parser.add_option("--use_chi2", dest = "use_chi2", action = "store_true")
    parser.add_option("--equalSgXsec", dest = "equalSgXsec", action = "store_true")
    parser.add_option("--noVetoes", dest = "noVetoes", action = "store_true")
    parser.add_option("--phase", dest = "phase", default = 0)
    (options, args) = parser.parse_args()
    
    train(options.skim_folder,
          options.category,
          options.dxyinformed,
          options.use_chi2,
          int(options.phase),
          equalSgXsec = options.equalSgXsec,
          noVetoes = options.noVetoes,
         )
