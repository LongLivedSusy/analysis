#!/bin/env python
from __future__ import division
from ROOT import *
from optparse import OptionParser
import math, os, glob
from GridEngineTools import runParallel
import collections
from array import array
import tools.tags as tags

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


def get_signal_region(HT, MHT, NJets, n_btags, MinDeltaPhiMhtJets, n_DT, is_pixel_track, DeDxAverage, n_goodelectrons, n_goodmuons, filename):
  
    is_tracker_track = not is_pixel_track
    inf = 9999
    binnumbers = collections.OrderedDict()

    ldedxcutLlow = 3.0
    ldedxcutLmid = 5.0
    ldedxcutSlow = 2.1
    ldedxcutSmid = 4.0
    binnumbers = {}
    listagain = ['Ht',  'Mht',    'NJets',  'BTags','NTags','NPix', 'NPixStrips', 'MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
    binnumbers[((0,inf),(150,300),(1,1),    (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 1
    binnumbers[((0,inf),(150,300),(1,1),    (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 2
    binnumbers[((0,inf),(150,300),(1,1),    (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 3
    binnumbers[((0,inf),(150,300),(1,1),    (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 4

    binnumbers[((0,inf),(150,300),(2,4),    (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 5
    binnumbers[((0,inf),(150,300),(2,4),    (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 6
    binnumbers[((0,inf),(150,300),(2,4),    (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 7
    binnumbers[((0,inf),(150,300),(2,4),    (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 8


    binnumbers[((0,inf),(150,300),(2,4),    (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 9
    binnumbers[((0,inf),(150,300),(2,4),    (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 10
    binnumbers[((0,inf),(150,300),(2,4),    (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 11
    binnumbers[((0,inf),(150,300),(2,4),    (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 12


    binnumbers[((0,inf),(150,300),(5,inf),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 13
    binnumbers[((0,inf),(150,300),(5,inf),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 14
    binnumbers[((0,inf),(150,300),(5,inf),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 15
    binnumbers[((0,inf),(150,300),(5,inf),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 16

    binnumbers[((0,inf),(150,300),(5,inf),  (1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 17
    binnumbers[((0,inf),(150,300),(5,inf),  (1,inf),(1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 18
    binnumbers[((0,inf),(150,300),(5,inf),  (1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 19
    binnumbers[((0,inf),(150,300),(5,inf),  (1,inf),(1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 20

    binnumbers[((0,inf),(300,inf),(1,1),    (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 21
    binnumbers[((0,inf),(300,inf),(1,1),    (0,inf),(1,1),  (0,0),  (1,1),      (0.0,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 22
    binnumbers[((0,inf),(300,inf),(1,1),    (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 23
    binnumbers[((0,inf),(300,inf),(1,1),    (0,inf),(1,1),  (1,1),  (0,0),      (0.0,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 24

    binnumbers[((0,inf),(300,inf),(2,4),    (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 25
    binnumbers[((0,inf),(300,inf),(2,4),    (0,0),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 26
    binnumbers[((0,inf),(300,inf),(2,4),    (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 27
    binnumbers[((0,inf),(300,inf),(2,4),    (0,0),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 28

    binnumbers[((0,inf),(300,inf),(2,4),    (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),   (0,0))] = 29
    binnumbers[((0,inf),(300,inf),(2,4),    (1,5),  (1,1),  (0,0),  (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),   (0,0))] = 30
    binnumbers[((0,inf),(300,inf),(2,4),    (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),   (0,0))] = 31
    binnumbers[((0,inf),(300,inf),(2,4),    (1,5),  (1,1),  (1,1),  (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),   (0,0))] = 32


    binnumbers[((0,1000),(300,inf),(5,inf), (0,0),  (1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),    (0,0))] = 33
    binnumbers[((0,1000),(300,inf),(5,inf), (0,0),  (1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),    (0,0))] = 34
    binnumbers[((0,1000),(300,inf),(5,inf), (0,0),  (1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),    (0,0))] = 35
    binnumbers[((0,1000),(300,inf),(5,inf), (0,0),  (1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),    (0,0))] = 36

    binnumbers[((0,1000),(300,inf),(5,inf), (1,inf),(1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),    (0,0))] = 37
    binnumbers[((0,1000),(300,inf),(5,inf), (1,inf),(1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),    (0,0))] = 38
    binnumbers[((0,1000),(300,inf),(5,inf), (1,inf),(1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),    (0,0))] = 39
    binnumbers[((0,1000),(300,inf),(5,inf), (1,inf),(1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),    (0,0))] = 40

    binnumbers[((1000,inf),(300,inf),(5,inf),(0,0), (1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),    (0,0))] = 41
    binnumbers[((1000,inf),(300,inf),(5,inf),(0,0), (1,1),  (0,0), (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),    (0,0))] = 42
    binnumbers[((1000,inf),(300,inf),(5,inf),(0,0), (1,1),  (1,1), (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),    (0,0))] = 43
    binnumbers[((1000,inf),(300,inf),(5,inf),(0,0),  (1,1), (1,1), (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),    (0,0))] = 44

    binnumbers[((1000,inf),(300,inf),(5,inf),(1,inf),(1,1), (0,0), (1,1),      (0.3,inf),          (ldedxcutLlow,ldedxcutLmid),(0,0),    (0,0))] = 45
    binnumbers[((1000,inf),(300,inf),(5,inf),(1,inf),(1,1), (0,0), (1,1),      (0.3,inf),          (ldedxcutLmid,inf),         (0,0),    (0,0))] = 46
    binnumbers[((1000,inf),(300,inf),(5,inf),(1,inf),(1,1), (1,1), (0,0),      (0.3,inf),          (ldedxcutSlow,ldedxcutSmid),(0,0),    (0,0))] = 47
    binnumbers[((1000,inf),(300,inf),(5,inf),(1,inf),(1,1), (1,1), (0,0),      (0.3,inf),          (ldedxcutSmid,inf),         (0,0),    (0,0))] = 48


    #listagain =  ['Ht',  'Mht',    'NJets','BTags','NTags','NPix','NPixStrips', 'MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
    binnumbers[((0,inf), (0,150),   (0,inf), (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLlow,ldedxcutLmid), (0,0), (1,inf))] = 49
    binnumbers[((0,inf), (0,150),   (0,inf), (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLmid,inf),          (0,0), (1,inf))] = 50
    binnumbers[((0,inf), (0,150),   (0,inf), (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSlow,ldedxcutSmid), (0,0), (1,inf))] = 51
    binnumbers[((0,inf), (0,150),   (0,inf), (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSmid,inf),          (0,0), (1,inf))] = 52


    binnumbers[((0,inf), (150,inf), (0,inf), (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLlow,ldedxcutLmid), (0,0), (1,inf))] = 53
    binnumbers[((0,inf), (150,inf), (0,inf), (0,0),  (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLmid,inf),          (0,0), (1,inf))] = 54
    binnumbers[((0,inf), (150,inf), (0,inf), (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSlow,ldedxcutSmid), (0,0), (1,inf))] = 55
    binnumbers[((0,inf), (150,inf), (0,inf), (0,0),  (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSmid,inf),          (0,0), (1,inf))] = 56

    binnumbers[((0,inf), (0,150),   (0,inf),(1,inf), (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLlow,ldedxcutLmid), (0,0), (1,inf))] = 57
    binnumbers[((0,inf), (0,150),   (0,inf),(1,inf), (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLmid,inf),          (0,0), (1,inf))] = 58
    binnumbers[((0,inf), (0,150),   (0,inf),(1,inf), (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSlow,ldedxcutSmid), (0,0), (1,inf))] = 59
    binnumbers[((0,inf), (0,150),   (0,inf),(1,inf), (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSmid,inf),          (0,0), (1,inf))] = 60

    binnumbers[((0,inf), (150,inf), (0,inf),(1,inf), (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLlow,ldedxcutLmid), (0,0), (1,inf))] = 61
    binnumbers[((0,inf), (150,inf), (0,inf),(1,inf), (1,1), (0,0),  (1,1),     (0.0,inf),          (ldedxcutLmid,inf),          (0,0), (1,inf))] = 62
    binnumbers[((0,inf), (150,inf), (0,inf),(1,inf), (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSlow,ldedxcutSmid), (0,0), (1,inf))] = 63
    binnumbers[((0,inf), (150,inf), (0,inf),(1,inf), (1,1), (1,1),  (0,0),     (0.0,inf),          (ldedxcutSmid,inf),          (0,0), (1,inf))] = 64
    #listagain =  ['Ht',  'Mht',    'NJets','BTags','NTags','NPix','NPixStrips', 'MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']
    binnumbers[((0,inf),  (150,300), (0,inf),(0,inf),(2,inf),(0,inf),(0,inf),  (0.0,inf),          (ldedxcutSlow,inf),          (0,0), (0,0))]   = 65
    binnumbers[((0,inf),  (300,inf), (0,inf),(0,inf),(2,inf),(0,inf),(0,inf),  (0.0,inf),          (ldedxcutSlow,inf),          (0,0), (0,0))]   = 66
    binnumbers[((0,inf),  (0,inf),   (0,inf),(0,inf),(2,inf),(0,inf),(0,inf),  (0.0,inf),          (ldedxcutSlow,inf),          (0,0), (1,inf))] = 67 

    #listagain = ['Ht',  'Mht',    'NJets',  'BTags','NTags','NPix', 'NPixStrips', 'MinDPhiMhtJets',  'DeDxAverage',        'NElectrons', 'NMuons', 'NPions', 'TrkPt',        'TrkEta',    'Log10DedxMass','BinNumber']

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
           DeDxAverage >= binkey[8][0] and DeDxAverage <= binkey[8][1] and \
           n_goodelectrons >= binkey[9][0] and n_goodelectrons <= binkey[9][1] and \
           n_goodmuons >= binkey[10][0] and n_goodmuons <= binkey[10][1]:
              region = binnumbers[binkey]
              break

    if region>0 and "Run201" in filename and "MET" in filename:
        if region<=48 or region==65 or region==66:
            return region
        else:
            return 0
    elif region>0 and "Run201" in filename and "SingleMuon" in filename:
        if region>=49 or region<=64 or region==67:
            return region
        else:
            return 0
    else:
        return region
    
    


def main(input_filenames, output_file, nevents = -1, treename = "Events", event_start = 0, fakerate_file = "fakerate.root", unweighted = False, vetocuts = ""):

    # check if data:
    phase = 0
    data_period = ""
    is_data = False
    for label in ["Run2016", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18"]:
        if label in input_filenames[0]:
            data_period = label
            if "Run201" in label:
                is_data = True
            if label == "Run2016" or label == "Summer16":
                phase = 0
            elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
                phase = 1

    # load tree
    tree = TChain(treename)

    nev = 0
    ignore_files =  []
    for tree_file in input_filenames:
        try:
            fin = TFile(tree_file)
            fin.Get("nev")
            fin.Get(treename)
        except:
            fin.Close()
            "Ignoring file: %s" % tree_file
            ignore_files.append(ignore_files)
            print "Ignoring", tree_file
            continue

        if not is_data:
            #fin = TFile(tree_file)
            h_nev = fin.Get("nev")
            nev += h_nev.GetBinContent(1)
            fin.Close()

    tree = TChain(treename)       
    for i, tree_file in enumerate(input_filenames):
        if not tree_file in ignore_files:
            tree.Add(tree_file)
   
    # output histograms
    histos = {
                "HT": TH1F("HT", "HT", 10, 0, 2000),
                "MET": TH1F("MET", "MET", 15, 0, 1200),
                "MHT": TH1F("MHT", "MHT", 15, 0, 1200),
                "n_goodjets": TH1F("n_goodjets", "n_goodjets", 10, 0, 10),
                "n_goodelectrons": TH1F("n_goodelectrons", "n_goodelectrons", 5, 0, 5),
                "n_goodmuons": TH1F("n_goodmuons", "n_goodmuons", 5, 0, 5),
                "MinDeltaPhiMhtJets": TH1F("MinDeltaPhiMhtJets", "MinDeltaPhiMhtJets", 16, 0, 3.2),
                "n_btags": TH1F("n_btags", "n_btags", 4, 0, 4),
                "Track1MassFromDedx": TH1F("Track1MassFromDedx", "Track1MassFromDedx", 25, 0, 1000),
                "Log10DedxMass": TH1F("Log10DedxMass", "Log10DedxMass", 10, 0, 5),
                "DeDxAverage": TH1F("DeDxAverage", "DeDxAverage", 20, 0, 10),
                "n_tags": TH1F("n_tags", "n_tags", 3, 0, 3),
                "region": TH1F("region", "region", 68, 0, 68),
             }

    event_selection = {
                #"baseline":         "(event.n_loose8_SR_short + event.n_loose8_CR_short + event.n_loose8_SR_long + event.n_loose8_CR_long)>0 and event.MinDeltaPhiMhtJets>0.3 and event.n_goodelectrons==0",
                #"baseline_noveto":  "(event.n_loose8_SR_short + event.n_loose8_CR_short + event.n_loose8_SR_long + event.n_loose8_CR_long)>0 and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0",
                #"baseline_muveto":  "(event.n_loose8_SR_short + event.n_loose8_CR_short + event.n_loose8_SR_long + event.n_loose8_CR_long)>0 and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0 and event.n_goodmuons==0",
                #"baseline_mu":      "(event.n_loose8_SR_short + event.n_loose8_CR_short + event.n_loose8_SR_long + event.n_loose8_CR_long)>0 and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0 and event.n_goodmuons>0",
                "baseline_singlemu":      "(event.n_loose8_SR_short + event.n_loose8_CR_short + event.n_loose8_SR_long + event.n_loose8_CR_long)>0 and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0 and event.n_goodmuons==1"

                      }

    output_variables = histos.keys()

    h_fakerates = {}
    
    for tag in tags.tags:
        fakerate_variable = "HT:n_allvertices"
        fakerate_maptag = "qcd_lowMHT_%s" % tag
        tfile_fakerate = TFile(fakerate_file, "open")
        h_fakerates["%s-short" % tag] = tfile_fakerate.Get("%s_short/%s/fakerate_%s" % (fakerate_maptag, data_period, fakerate_variable.replace(":", "_")))
        h_fakerates["%s-long" % tag] = tfile_fakerate.Get("%s_long/%s/fakerate_%s" % (fakerate_maptag, data_period, fakerate_variable.replace(":", "_")))

    # add more histograms
    for variable in output_variables:               
        for category in ["short", "long", "multi"]:
            for cr in event_selection:
                    for itype in ["signalfake", "signalprompt", "control", "controlfake", "controlprompt", "signal", "prediction"]:
                        h_name = "%s_%s_%s_%s" % (variable, itype, category, cr)
                        histos[h_name] = histos[variable].Clone()
                        histos[h_name].SetName(h_name)
    
    if nevents > 0:
        nev = nevents
        print "Using fixed number of events"

    print "Looping over %s events" % nev

    for iEv, event in enumerate(tree):

        if iEv < event_start: continue
        if nevents > 0 and iEv > nevents + event_start: break
        
        if (iEv+1) % 10000 == 0:
            print "Processing event %s / %s" % (iEv + 1, nev)

        if is_data:
            weight = 1.0
        else:
            weight = 1.0 * event.CrossSection * event.puWeight / nev

        # check if event passes control region
        pass_cr = {}    
        for cr in event_selection:
            pass_cr[cr] = eval(event_selection[cr])
        
        passes_cr = False
        for cr in pass_cr:
            if pass_cr[cr]:
                passes_cr = True
                break
        if not passes_cr: continue
        
        for tag in tags.tags:

            good_track = tags.convert_cut_string(tags.good_track)

            for cr in pass_cr:
                
                # check if event passes this control region:
                if not pass_cr[cr]: continue
                        
                # count DTs in signal and control regions:
                is_short_signal = 0
                is_short_signal_fake = 0
                is_short_signal_prompt = 0
                is_short_control = 0
                is_long_signal = 0
                is_long_signal_fake = 0
                is_long_signal_prompt = 0
                is_long_control = 0
                dedx_signal = 0
                dedx_control = 0
                log10dedxmass_signal = 0
                log10dedxmass_control = 0
                region_signal = 0
                region_control = 0
                is_pixel_track_signal = False
                is_pixel_track_control = False
            
                for i in range(len(event.tracks_pt)):
                
                    is_prompt_track = event.tracks_prompt_electron[i]==1 or event.tracks_prompt_muon[i]==1 or event.tracks_prompt_tau[i]==1 or event.tracks_prompt_tau_leadtrk[i]==1
                    is_fake_track = event.tracks_fake[i]==1

                    log10dedxmass = TMath.Log10(TMath.Sqrt((event.tracks_deDxHarmonic2pixel[i]-3.01) * pow(event.tracks_pt[i] * TMath.CosH(event.tracks_eta[i]),2)/1.74))
                    dedx = event.tracks_deDxHarmonic2pixel[i]

                    # short:
                    if eval(tags.convert_cut_string(tags.tags[tag]["SR_short"])) and eval(good_track):
                        log10dedxmass_signal = log10dedxmass
                        dedx_signal = dedx
                        is_pixel_track_signal = True
                        is_short_signal += 1
                        if is_fake_track:
                            is_short_signal_fake += 1
                        elif is_prompt_track:
                            is_short_signal_prompt += 1                        
                    elif eval(tags.convert_cut_string(tags.tags[tag]["CR_short"])) and eval(good_track):
                        log10dedxmass_control = log10dedxmass
                        dedx_control = dedx
                        is_pixel_track_control = True
                        is_short_control += 1
                    
                    # long:
                    if eval(tags.convert_cut_string(tags.tags[tag]["SR_long"])) and eval(good_track):
                        log10dedxmass_signal = log10dedxmass
                        dedx_signal = dedx
                        is_pixel_track_signal = False
                        is_long_signal += 1
                        if is_fake_track:
                            is_long_signal_fake += 1
                        elif is_prompt_track:
                            is_long_signal_prompt += 1                        
                    elif eval(tags.convert_cut_string(tags.tags[tag]["CR_long"])) and eval(good_track):
                        log10dedxmass_control = log10dedxmass
                        dedx_control = dedx
                        is_pixel_track_control = False
                        is_long_control += 1
                    
                n_DT_signal = is_short_signal + is_long_signal
                n_DT_control = is_short_control + is_long_control
                    
                # get region bin:
                if n_DT_signal > 0:
                    region_signal = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT_signal, is_pixel_track_signal, dedx_signal, event.n_goodelectrons, event.n_goodmuons, input_filenames[0])
                if n_DT_control > 0:
                    region_control = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT_control, is_pixel_track_control, dedx_control, event.n_goodelectrons, event.n_goodmuons, input_filenames[0])

                # get fake rate for event:
                fakerate_short = -1
                fakerate_long = -1
                if ":" in fakerate_variable:
                    xvalue = eval("event.%s" % fakerate_variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[1])
                    yvalue = eval("event.%s" % fakerate_variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[0])                
                    fakerate_short = getBinContent_with_overflow(h_fakerates["%s-short" % tag], xvalue, yval = yvalue)
                    fakerate_long = getBinContent_with_overflow(h_fakerates["%s-long" % tag], xvalue, yval = yvalue)
                else:                
                    xvalue = eval("event.%s" % fakerate_variable)
                    fakerate_short = getBinContent_with_overflow(h_fakerates["%s-short" % tag], xvalue)
                    fakerate_long = getBinContent_with_overflow(h_fakerates["%s-long" % tag], xvalue)

                # fill histograms:    
                for variable in output_variables:

                    if variable == "region":
                        value = region_signal                
                    elif variable == "Track1MassFromDedx":
                        value = 10**log10dedxmass_signal
                    elif variable == "Log10DedxMass":
                        value = log10dedxmass_signal
                    elif variable == "DeDxAverage":
                        value = dedx_signal
                    elif variable == "n_tags":
                        value = is_short_signal + is_long_signal
                    else:
                        value = eval("event.%s" % variable)

                    if n_DT_signal == 1:
                        if is_short_signal == 1:
                            histos[variable + "_signal_short_" + cr].Fill(value, weight)
                        if is_short_signal_fake == 1:
                            histos[variable + "_signalfake_short_" + cr].Fill(value, weight)
                        if is_short_signal_prompt == 1:
                            histos[variable + "_signalprompt_short_" + cr].Fill(value, weight)
                        if is_long_signal == 1:
                            histos[variable + "_signal_long_" + cr].Fill(value, weight)
                        if is_long_signal_fake == 1:
                            histos[variable + "_signalfake_long_" + cr].Fill(value, weight)
                        if is_long_signal_prompt == 1:
                            histos[variable + "_signalprompt_long_" + cr].Fill(value, weight)
                    elif n_DT_signal >= 2:
                        if (is_short_signal + is_long_signal) >= 2:
                            histos[variable + "_signal_multi_" + cr].Fill(value, weight)
                        if (is_short_signal_fake + is_long_signal_fake) >= 2: 
                            histos[variable + "_signalfake_multi_" + cr].Fill(value, weight)
                        if (is_short_signal_prompt + is_long_signal_prompt) >= 2: 
                            histos[variable + "_signalprompt_multi_" + cr].Fill(value, weight)

                    if variable == "region":
                        value = region_control
                    elif variable == "Track1MassFromDedx":
                        value = 10**log10dedxmass_control
                    elif variable == "Log10DedxMass":
                        value = log10dedxmass_control
                    elif variable == "DeDxAverage":
                        value = dedx_control
                    elif variable == "n_tags":
                        value = is_short_control + is_long_control

                    if n_DT_control == 1:
                        if is_short_control == 1:
                            histos[variable + "_control_short_" + cr].Fill(value, weight)
                            histos[variable + "_prediction_short_" + cr].Fill(value, weight * fakerate_short)
                        if is_long_control == 1:
                            histos[variable + "_control_long_" + cr].Fill(value, weight)
                            histos[variable + "_prediction_long_" + cr].Fill(value, weight * fakerate_long)
                    elif n_DT_control >= 2:
                        if is_short_control >= 2 and is_long_control == 0:
                            histos[variable + "_prediction_multi_" + cr].Fill(value, weight * fakerate_short * fakerate_short)
                        elif is_short_control == 0 and is_long_control >= 2:
                            histos[variable + "_prediction_multi_" + cr].Fill(value, weight * fakerate_long * fakerate_long)
                        else:
                            histos[variable + "_prediction_multi_" + cr].Fill(value, weight * fakerate_short * fakerate_long)

    if event_start>0:
        output_file = output_file.replace(".root", "_%s.root" % event_start)

    fout = TFile(output_file, "recreate")
    for var in histos:
        histos[var].Write()

    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles")
    parser.add_option("--output", dest = "outputfiles")
    parser.add_option("--folder", dest = "prediction_folder", default="prediction")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--unweighted", dest="unweighted", action="store_true")
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--jobs_per_file", dest = "jobs_per_file", default = 50)
    parser.add_option("--event_start", dest = "event_start", default = 0)
    parser.add_option("--fakerate_file", dest = "fakerate_file", default = "fakerate.root")
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--start", dest="start", action="store_true")
    (options, args) = parser.parse_args()
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    if options.hadd:
        os.system("hadd -f %s/prediction_Summer16-all.root %s/Summer16*.root" % (options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Summer16-DY.root %s/Summer16.DY*.root" % (options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Summer16-WJets.root %s/Summer16.WJets*.root" % (options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Summer16-TT.root %s/Summer16.TT*.root" % (options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Summer16-QCD.root %s/Summer16.QCD*.root" % (options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Summer16-ZJets.root %s/Summer16.ZJets*.root" % (options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Summer16-WJets+TT.root %s/Summer16.WJets*.root %s/Summer16.TT*.root" % (options.prediction_folder, options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Summer16-QCD+ZJets.root %s/Summer16.QCD*.root %s/Summer16.ZJets*.root" % (options.prediction_folder, options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Run2016_MET.root %s/Run2016*MET*.root" % (options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Run2016_SingleMuon.root %s/Run2016*SingleMuon*.root" % (options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Run2016_SingleMuonMET.root %s/Run2016*SingleMuon*.root %s/Run2016*SingleMuon*.root" % (options.prediction_folder, options.prediction_folder, options.prediction_folder))
        quit()

    # run parallel if input is a folder:
    if options.inputfiles[-1] == "/":
        print "Got input folder, running in batch mode (%s)" % options.runmode
       
        input_files = glob.glob(options.inputfiles + "/*.root")
        os.system("mkdir -p %s" % options.prediction_folder)
        commands = []
        
        for input_file in input_files:

            use_file = False

            if "Summer16.DYJetsToLL" in input_file: use_file = True
            if "Summer16.QCD" in input_file: use_file = True
            if "Summer16.WJetsToLNu" in input_file: use_file = True
            if "Summer16.ZJetsToNuNu_HT" in input_file: use_file = True
            if "Summer16.WW_TuneCUETP8M1" in input_file: use_file = True
            if "Summer16.WZ_TuneCUETP8M1" in input_file: use_file = True
            if "Summer16.ZZ_TuneCUETP8M1" in input_file: use_file = True
            #if "Summer16.TTJets_TuneCUETP8M1" in input_file: use_file = True
            if "Summer16.TT" in input_file: use_file = True
            if "Run2016" in input_file and "MET" in input_file: use_file = True
            if "Run2016" in input_file and "SingleMuon" in input_file: use_file = True
            if not use_file: continue
            
            # get nev:
            tree = TChain("Events")
            tree.Add(input_file)
            nev = tree.GetEntries()
            
            nev_per_interval = int(nev/int(options.jobs_per_file))
            
            for i in range(int(options.jobs_per_file)):
                
                event_start = i * nev_per_interval
                
                commands.append("./get_prediction.py --input %s --output %s/%s --nev %s --fakerate_file %s --event_start %s --unweighted %s" % (input_file, options.prediction_folder, input_file.split("/")[-1], nev_per_interval, options.fakerate_file, event_start, options.unweighted))
        
        runParallel(commands, options.runmode, condorDir = "get_prediction.condor", use_more_mem=False, use_more_time=False, confirm=not options.start)

    # otherwise run locally:
    else:
        options.inputfiles = options.inputfiles.split(",")

        main(options.inputfiles,
             options.outputfiles,
             nevents = int(options.nev),
             fakerate_file = options.fakerate_file,
             event_start = int(options.event_start),
             unweighted = options.unweighted,
            )
