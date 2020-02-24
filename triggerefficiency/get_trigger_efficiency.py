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


def main(input_filenames, output_file, eta_low = 0, eta_high = 2.4, nevents = -1, event_start = 0, treename = "TreeMaker2/PreSelection"):

    tree = TChain(treename)
    for tree_file in input_filenames:
        tree.Add(tree_file)
   
    ###################################################################################################
    # output histograms

    pt_binning = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 250, 300]

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
        passed_UniversalSelection = passesUniversalSelection(event) and event.MET>280
        if not passed_UniversalSelection: continue

        # check trigger:
        triggered_met = shared_utils.PassTrig(event, 'MhtMet6pack')
        triggered_singleelectron = shared_utils.PassTrig(event, 'SingleElectron')
        triggered_singlemuon = shared_utils.PassTrig(event, 'SingleMuon')

        goodleptons = {"electrons": [], "muons": []}

        for i, electron in enumerate(event.Electrons):
            if abs(electron.Eta()) >= eta_low and abs(electron.Eta()) < eta_high and bool(event.Electrons_tightID[i]) and bool(event.Electrons_passIso[i]):
                goodleptons["electrons"].append(electron)
        for i, muon in enumerate(event.Muons):
            if abs(muon.Eta()) >= eta_low and abs(muon.Eta()) < eta_high and bool(event.Muons_tightID[i]) and bool(event.Muons_passIso[i]):
                goodleptons["muons"].append(muon)

        if len(goodleptons["electrons"]) == 1:
            pt_lepton = goodleptons["electrons"][0].Pt()
            if triggered_met == 1:
                histos["pt_singleelectron_mettrigger"].Fill(pt_lepton, weight)
            if triggered_singleelectron == 1 and triggered_met == 1:
                histos["pt_singleelectron_eltrigger"].Fill(pt_lepton, weight)

        if len(goodleptons["muons"]) == 1:
            pt_lepton = goodleptons["muons"][0].Pt()
            if triggered_met == 1:
                histos["pt_singlemuon_mettrigger"].Fill(pt_lepton, weight)
            if triggered_singlemuon == 1 and triggered_met == 1:
                histos["pt_singlemuon_mutrigger"].Fill(pt_lepton, weight)

        ###################################################################################################

    if event_start>0:
        output_file = output_file.replace(".root", "_%s.root" % event_start)

    fout = TFile(output_file, "recreate")
    for var in histos:
        histos[var].Write()

    fout.Close()


def get_and_plot_ratio(hadded_file, header, pdffile):

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

    legend = TLegend(0.6, 0.2, 0.88, 0.4)
    legend.SetHeader(header)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)    

    # Draw:
    shared_utils.histoStyler(pt_electron_trigger_efficiency)
    shared_utils.histoStyler(pt_singlemuon_trigger_efficiency)
    pt_electron_trigger_efficiency.SetTitle(";lepton p_{T} (GeV); trigger efficiency #epsilon")
    legend.AddEntry(pt_electron_trigger_efficiency, "SingleElectron (2016)")    
    pt_singlemuon_trigger_efficiency.SetTitle(";lepton p_{T} (GeV); trigger efficiency #epsilon")
    legend.AddEntry(pt_singlemuon_trigger_efficiency, "SingleMuon (2016)")
    pt_electron_trigger_efficiency.SetLineWidth(2)
    pt_electron_trigger_efficiency.SetLineColor(kBlack)
    pt_electron_trigger_efficiency.GetYaxis().SetRangeUser(0,1.1)
    pt_singlemuon_trigger_efficiency.SetLineWidth(2)
    pt_singlemuon_trigger_efficiency.SetLineColor(kRed)
    pt_singlemuon_trigger_efficiency.GetYaxis().SetRangeUser(0,1.1)
    
    fout = TFile("disapptrks_trigger_efficiency.root", "recreate")

    c1 = shared_utils.mkcanvas("c1")
    pt_electron_trigger_efficiency.Draw()
    pt_singlemuon_trigger_efficiency.Draw("same")
    legend.Draw()
    
    shared_utils.stamp()
    c1.SetGrid(True)
    
    c1.SaveAs(pdffile)
    
    fout.Close()

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles", default = "../skims/current/")
    parser.add_option("--output", dest = "outputfile", default = "output.root")
    parser.add_option("--folder", dest = "folder", default="output")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--plot", dest="plot", action="store_true")
    (options, args) = parser.parse_args()
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
    gROOT.SetBatch(True) 

    print "Get single lepton trigger efficiency from skim"

    if options.hadd:
        os.system("hadd -f output_barrel.root %s/*_barrel.root" % (options.folder))
        os.system("hadd -f output_endcap.root %s/*_endcap.root" % (options.folder))

        for period in ["2016", "2016A", "2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H"]:
            for region in ["barrel", "endcap"]:
                os.system("hadd -f output_%s_%s.root %s/*%s*_%s.root" % (period, region, options.folder, period, region))

        options.plot = True
        quit()

    if options.plot:
        for period in ["2016", "2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H"]:
            for region in ["barrel", "endcap"]:
                get_and_plot_ratio("output_%s_%s.root" % (period, region), "%s region, %s Data" % (region, period), "%s_singlelepton_trigger_%s.pdf" % (region, period))
                get_and_plot_ratio("output_%s_%s.root" % (period, region), "%s region, %s Data" % (region, period), "%s_singlelepton_trigger_%s.png" % (region, period))
        quit()

    # otherwise run locally:
    else:
        options.inputfiles = options.inputfiles.split(",")
        main(options.inputfiles, options.outputfile.replace(".root", "_barrel.root"), eta_low = 0, eta_high = 1.5)
        main(options.inputfiles, options.outputfile.replace(".root", "_endcap.root"), eta_low = 1.5, eta_high = 2.4)
