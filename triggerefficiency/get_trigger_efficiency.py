#!/bin/env python
from __future__ import division
from ROOT import *
from optparse import OptionParser
import math, os, glob
from GridEngineTools import runParallel
import collections
import array
import shared_utils

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
    

def passesUniversalSelection(t):
    if not (bool(t.JetID) and  t.NVtx>0): return False
    if not  passQCDHighMETFilter(t): return False
    if not t.PFCaloMETRatio<2: return False
    if not t.globalTightHalo2016Filter: return False
    if not t.HBHEIsoNoiseFilter: return False
    if not t.HBHENoiseFilter: return False
    if not t.BadPFMuonFilter: return False
    if not t.CSCTightHaloFilter: return False
    if not t.EcalDeadCellTriggerPrimitiveFilter: return False
    if not t.eeBadScFilter: return False 
    return True


def main(input_filenames, output_file, nevents = -1, event_start = 0, treename = "TreeMaker2/PreSelection"):

    tree = TChain(treename)
    for tree_file in input_filenames:
        tree.Add(tree_file)
   
    ###################################################################################################
    # output histograms

    pt_binning = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 250, 300, 350, 400, 450, 500, 750, 1000]

    histos = {
        "pt_singleelectron_mettrigger": TH1F("pt_singleelectron_mettrigger", "pt_singleelectron_mettrigger", len(pt_binning)-1, array.array('d', pt_binning)),
        "pt_singleelectron_eltrigger": TH1F("pt_singleelectron_eltrigger", "pt_singleelectron_eltrigger", len(pt_binning)-1, array.array('d', pt_binning)),
        "pt_singlemuon_mettrigger": TH1F("pt_singlemuon_mettrigger", "pt_singlemuon_mettrigger", len(pt_binning)-1, array.array('d', pt_binning)),
        "pt_singlemuon_mutrigger": TH1F("pt_singlemuon_mutrigger", "pt_singlemuon_mutrigger", len(pt_binning)-1, array.array('d', pt_binning)),
             }

    ###################################################################################################

    if nevents == -1:
        nevents = tree.GetEntries()

    print "Looping over %s events" % nevents

    for iEv, event in enumerate(tree):

        #if iEv < event_start: continue
        #if nevents > 0 and iEv > nevents + event_start: break
        
        if (iEv+1) % 10000 == 0:
            print "Processing event %s / %s" % (iEv + 1, event_start + nevents)

        weight = 1.0

        ###################################################################################################

        # basic event selection:
        passed_UniversalSelection = passesUniversalSelection(event)
        if not passed_UniversalSelection: continue

        # check trigger:
        triggered_met = shared_utils.PassTrig(event, 'MhtMet6pack')
        triggered_singleelectron = shared_utils.PassTrig(event, 'SingleElectron')
        triggered_singlemuon = shared_utils.PassTrig(event, 'SingleMuon')

        goodleptons = {"electrons": [], "muons": []}

        for i, electron in enumerate(event.Electrons):
            if abs(electron.Eta()) < 2.4 and bool(event.Electrons_mediumID[i]):
                goodleptons["electrons"].append(electron)
        for i, muon in enumerate(event.Muons):
            if abs(muon.Eta()) < 2.4 and bool(event.Muons_tightID[i]):
                goodleptons["muons"].append(muon)

        if len(goodleptons["electrons"]) == 1:
            pt_lepton = goodleptons["electrons"][0].Pt()
            if triggered_singleelectron == 1 and triggered_met == 1:
                histos["pt_singleelectron_mettrigger"].Fill(pt_lepton, weight)
            if triggered_singleelectron == 1:
                histos["pt_singleelectron_eltrigger"].Fill(pt_lepton, weight)

        if len(goodleptons["muons"]) == 1:
            pt_lepton = goodleptons["muons"][0].Pt()
            if triggered_singlemuon == 1 and triggered_met == 1:
                histos["pt_singlemuon_mettrigger"].Fill(pt_lepton, weight)
            if triggered_singlemuon == 1:
                histos["pt_singlemuon_mutrigger"].Fill(pt_lepton, weight)

        ###################################################################################################

    if event_start>0:
        output_file = output_file.replace(".root", "_%s.root" % event_start)

    fout = TFile(output_file, "recreate")
    for var in histos:
        histos[var].Write()

    fout.Close()


def get_and_plot_ratio(hadded_file):

    fin = TFile(hadded_file, "open")

    pt_singleelectron_mettrigger = fin.Get("pt_singleelectron_mettrigger")
    pt_singleelectron_eltrigger = fin.Get("pt_singleelectron_eltrigger")
    pt_singlemuon_mettrigger = fin.Get("pt_singlemuon_mettrigger")
    pt_singlemuon_mutrigger = fin.Get("pt_singlemuon_mutrigger")

    pt_singleelectron_mettrigger.SetDirectory(0)
    pt_singleelectron_eltrigger.SetDirectory(0)
    pt_singlemuon_mettrigger.SetDirectory(0)
    pt_singlemuon_mutrigger.SetDirectory(0)

    fin.Close()

    pt_electron_trigger_efficiency = pt_singleelectron_eltrigger.Clone()
    pt_electron_trigger_efficiency.Divide(pt_singleelectron_mettrigger)

    pt_singlemuon_trigger_efficiency = pt_singlemuon_mutrigger.Clone()
    pt_singlemuon_trigger_efficiency.Divide(pt_singlemuon_mettrigger)

    # Draw:

    shared_utils.histoStyler(pt_singleelectron_mettrigger)
    shared_utils.histoStyler(pt_singleelectron_eltrigger)
    shared_utils.histoStyler(pt_singlemuon_mettrigger)
    shared_utils.histoStyler(pt_singlemuon_mutrigger)

    fout = TFile("disapptrks_trigger_efficiency.root", "recreate")

    c1 = shared_utils.mkcanvas("c1")
    leg = shared_utils.mklegend(x1=.7, y1=.6, x2=.92, y2=.8, color=kWhite)

    for lepton in ["electron", "muon"]:
        c1.Clear()
        if lepton == "electron":
            pt_electron_trigger_efficiency.Draw()
        elif lepton == "muon":
            pt_singlemuon_trigger_efficiency.Draw()
        #pt_singleelectron_mettrigger.Scale(pt_singleelectron_mettrigger.GetIntegral())
    
    fout.Close()

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles", default = "../skims/current/")
    parser.add_option("--output", dest = "outputfile", default = "output.root")
    parser.add_option("--folder", dest = "folder", default="output")
    parser.add_option("--pattern", dest = "pattern", default="Run2016*MET.root")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--jobs_per_file", dest = "jobs_per_file", default = 50)
    parser.add_option("--event_start", dest = "event_start", default = 0)
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--start", dest="start", action="store_true")
    parser.add_option("--plot", dest="plot", action="store_true")
    parser.add_option("--submit", dest="submit", action="store_true")
    (options, args) = parser.parse_args()
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    print "Get single lepton trigger efficiency from skim"

    if options.hadd:
        os.system("hadd -f output.root %s/*.root" % (options.folder))
        quit()

    if options.plot:
        get_and_plot_ratio(options.outputfile)
        quit()

    # otherwise run locally:
    else:
        options.inputfiles = options.inputfiles.split(",")

        main(options.inputfiles,
             options.outputfile,
            )
