#!/bin/env python
from __future__ import division
from ROOT import *
from optparse import OptionParser
import math, os, glob
from GridEngineTools import runParallel
import collections
import array
import shared_utils

binnings =  {
            "Pt": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 250, 300],
            "MHT": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 320, 340, 360, 380, 400, 450, 500, 600, 1000],
            "nJet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            }    

def PassTrig(c, trigname):
    triggerIndeces = {}
    triggerIndeces['MhtMet6pack'] = [124,109,110,111,112,114,115,116]#123
    triggerIndeces['SingleMuon'] = [49,50,65]
    triggerIndeces['SingleElectron'] = [36,37,39,40]
    triggerIndeces['SingleElectronLoose'] = [35,36,37,38,39,40,41,42,43]
    triggerIndeces['HtTrain'] = [67,68,69,70,73,74,75,81,85,89,92,93,94,96,97,100,103,104,105]

    for trigidx in triggerIndeces[trigname]: 
        if c.TriggerPass[trigidx]==1: return True
    return False


def main(input_filenames, output_file, eta_low = 0, eta_high = 2.4, nevents = -1, event_start = 0, treename = "TreeMaker2/PreSelection"):

    tree = TChain(treename)
    for tree_file in input_filenames:
        tree.Add(tree_file)
   
    ###################################################################################################
        
    histos = {}
    for variable in binnings:
        histos[variable + "_MHT_singleelectron_mettrigger"] = TH1F("%s_MHT_singleelectron_mettrigger" % variable, "%s_MHT_singleelectron_mettrigger" % variable, len(binnings[variable])-1, array.array('d', binnings[variable]))
        histos[variable + "_MHT_singleelectron_eltrigger"] = TH1F("%s_MHT_singleelectron_eltrigger" % variable, "%s_MHT_singleelectron_eltrigger" % variable, len(binnings[variable])-1, array.array('d', binnings[variable]))
        histos[variable + "_MHT_singlemuon_mettrigger"] = TH1F("%s_MHT_singlemuon_mettrigger" % variable, "%s_MHT_singlemuon_mettrigger" % variable, len(binnings[variable])-1, array.array('d', binnings[variable]))
        histos[variable + "_MHT_singlemuon_mutrigger"] = TH1F("%s_MHT_singlemuon_mutrigger" % variable, "%s_MHT_singlemuon_mutrigger" % variable, len(binnings[variable])-1, array.array('d', binnings[variable]))

        histos[variable + "_Lep_singleelectron_mettrigger"] = TH1F("%s_Lep_singleelectron_mettrigger" % variable, "%s_Lep_singleelectron_mettrigger" % variable, len(binnings[variable])-1, array.array('d', binnings[variable]))
        histos[variable + "_Lep_singleelectron_eltrigger"] = TH1F("%s_Lep_singleelectron_eltrigger" % variable, "%s_Lep_singleelectron_eltrigger" % variable, len(binnings[variable])-1, array.array('d', binnings[variable]))
        histos[variable + "_Lep_singlemuon_mettrigger"] = TH1F("%s_Lep_singlemuon_mettrigger" % variable, "%s_Lep_singlemuon_mettrigger" % variable, len(binnings[variable])-1, array.array('d', binnings[variable]))
        histos[variable + "_Lep_singlemuon_mutrigger"] = TH1F("%s_Lep_singlemuon_mutrigger" % variable, "%s_Lep_singlemuon_mutrigger" % variable, len(binnings[variable])-1, array.array('d', binnings[variable]))

    ###################################################################################################

    if nevents == -1:
        nevents = tree.GetEntries()

    print "Looping over %s events" % nevents

    for iEv, event in enumerate(tree):
        
        if (iEv+1) % 10000 == 0:
            print "Processing event %s / %s" % (iEv + 1, event_start + nevents)

        weight = 1.0

        ###################################################################################################

        # basic event selection:
        if not shared_utils.passesUniversalDataSelection(event):
            continue
        
        # count good leptons and good jets:
        goodelectrons = []
        goodmuons = []
        n_goodelectrons = 0
        n_goodmuons = 0
        for i, electron in enumerate(event.Electrons):
            if electron.Pt() > 30 and abs(electron.Eta()) < 2.4 and bool(event.Electrons_passIso[i]) and bool(event.Electrons_tightID[i]):

                # check for jets:
                for jet in event.Jets:
                    if jet.DeltaR(electron) < 0.1: continue

                goodelectrons.append(electron)
                n_goodelectrons += 1
                                                                                             
        for i, muon in enumerate(event.Muons):
            if muon.Pt() > 30 and abs(muon.Eta()) < 2.4 and bool(event.Muons_passIso[i]) and bool(event.Muons_tightID[i]):

                # check for jets:
                for jet in event.Jets:
                    if jet.DeltaR(muon) < 0.1: continue

                goodmuons.append(muon)
                n_goodmuons += 1
                
        n_goodleptons = n_goodelectrons + n_goodmuons
        
        n_goodjets = 0
        for jet in event.Jets:
            if jet.Pt() > 30 and abs(jet.Eta()) < 2.4:
                for lepton in list(goodelectrons + goodmuons):
                    if jet.DeltaR(lepton) < 0.5:
                        continue
                n_goodjets += 1

        # check triggers:

        for triggertype in ["MHT", "Lep"]:

            # check trigger:
            triggered_met = PassTrig(event, 'MhtMet6pack')
            
            if triggertype == "MHT":
                # MHT triggers...
                if not (event.HT>150 and n_goodjets>=1):
                    continue
                triggered_singleelectron = event.TriggerPass[36]
                triggered_singlemuon = event.TriggerPass[49]
            else:
                # lepton triggers...
                if not (event.HT>30):
                    continue
                triggered_singleelectron = PassTrig(event, 'SingleElectron')
                triggered_singlemuon = PassTrig(event, 'SingleMuon')
                        
            for variable in binnings:
            
                if n_goodelectrons >= 1:
                    if variable == "Pt":
                        value = goodelectrons[0].Pt()
                    elif variable == "MHT":
                        value = event.MHT
                    elif variable == "nJet":
                        value = n_goodjets
                    
                    if triggered_met == 1:
                        histos[variable + "_" + triggertype + "_singleelectron_mettrigger"].Fill(value, weight)
                    if triggered_singleelectron == 1 and triggered_met == 1:
                        histos[variable + "_" + triggertype + "_singleelectron_eltrigger"].Fill(value, weight)
                
                elif n_goodmuons >= 1 and n_goodelectrons == 0:
                    if variable == "Pt":
                        value = goodmuons[0].Pt()
                    elif variable == "MHT":
                        value = event.MHT
                    elif variable == "nJet":
                        value = n_goodjets                    
                    
                    if triggered_met == 1:
                        histos[variable + "_" + triggertype + "_singlemuon_mettrigger"].Fill(value, weight)
                    if triggered_singlemuon == 1 and triggered_met == 1:
                        histos[variable + "_" + triggertype + "_singlemuon_mutrigger"].Fill(value, weight)

        ###################################################################################################

    if event_start>0:
        output_file = output_file.replace(".root", "_%s.root" % event_start)

    fout = TFile(output_file, "recreate")
    for var in histos:
        histos[var].Write()

    fout.Close()




def combinedplots():

    
    for channel in [ "Lep", "MHT"]:

        histos = {}
        
        for year in [2016, 2017, 2018]:

            if channel == "MHT":
                fin = TFile("Run%s_Lep.root" % year, "open")    
            elif channel == "Lep":
                fin = TFile("Run%s_MET.root" % year, "open")    

            for variable in binnings:
                for label in [
                               variable + "_MHT_singleelectron_mettrigger",
                               variable + "_MHT_singleelectron_eltrigger",
                               variable + "_MHT_singlemuon_mettrigger",
                               variable + "_MHT_singlemuon_mutrigger",
                               variable + "_Lep_singleelectron_mettrigger", 
                               variable + "_Lep_singleelectron_eltrigger", 
                               variable + "_Lep_singlemuon_mettrigger",
                               variable + "_Lep_singlemuon_mutrigger", 
                             ]:
                         
                    histos[label + "_%s" % year] = fin.Get(label)
                    histos[label + "_%s" % year].SetDirectory(0)
                
                    print histos[label + "_%s" % year].GetEntries()
            
            fin.Close()
        
        for variable in binnings:
            
            c1 = shared_utils.mkcanvas("c1")
            
            legend = TLegend(0.5, 0.2, 0.88, 0.4)
            #legend.SetHeader(header)
            legend.SetTextSize(0.035)
            legend.SetBorderSize(0)
            legend.SetFillStyle(0)
            
            histo = TH1F("histo", "", len(binnings[variable])-1, array.array('d', binnings[variable]))
            if variable == "Pt":
                histo.SetTitle(";lepton p_{T} (GeV); trigger efficiency #epsilon")
            elif variable == "MHT":
                histo.SetTitle(";H_{T}^{miss} (GeV); trigger efficiency #epsilon")
            elif variable == "nJet":
                histo.SetTitle(";n_{jet}; trigger efficiency #epsilon")
            
            histo.GetYaxis().SetRangeUser(0,1.1)
            shared_utils.histoStyler(histo)
            histo.Draw("hist")
            
            h_effs = {}
            for i_year, year in enumerate([2016, 2017, 2018]):
                num = histos["%s_%s_singlemuon_mutrigger_%s" % (variable, channel, year)].Clone()
                denom = histos["%s_%s_singlemuon_mettrigger_%s" % (variable, channel, year)].Clone()
                h_effs["mu_%s" % year] = TEfficiency(num.Clone(), denom.Clone())
                print num.GetEntries(), denom.GetEntries()
                
                num = histos["%s_%s_singleelectron_eltrigger_%s" % (variable, channel, year)].Clone()
                denom = histos["%s_%s_singleelectron_mettrigger_%s" % (variable, channel, year)].Clone()
                h_effs["el_%s" % year] = TEfficiency(num.Clone(), denom.Clone())
                print num.GetEntries(), denom.GetEntries()
                
                #shared_utils.histoStyler(h_effs["mu_%s" % year])
                #shared_utils.histoStyler(h_effs["el_%s" % year])
                
                #h_effs["mu_%s" % year].SetTitle(";lepton p_{T} (GeV); trigger efficiency #epsilon")
                #h_effs["el_%s" % year].SetTitle(";lepton p_{T} (GeV); trigger efficiency #epsilon")
                
                #if year == "2016":
                #    h_effs["el_%s" % year].Draw()
                #else:
                h_effs["el_%s" % year].Draw("same")
                #h_effs["el_%s" % year].SetLineColor(kBlue)
                #h_effs["el_%s" % year].SetLineStyle(i_year+1)
                h_effs["el_%s" % year].SetLineWidth(2)
                
                #h_effs["el_%s_legend" % year] = h_effs["el_%s" % year].Clone()
                #h_effs["el_%s_legend" % year].SetLineColor(kBlack)
                
                h_effs["mu_%s" % year].Draw("same")
                #h_effs["mu_%s" % year].SetLineColor(kRed)
                #h_effs["mu_%s" % year].SetLineStyle(i_year+1)
                h_effs["mu_%s" % year].SetLineWidth(2)
                
            
            h_effs["el_2016"].SetLineColor(kBlue)    
            legend.AddEntry(h_effs["el_2016"], "2016, lepton trigger: el.")
            h_effs["el_2017"].SetLineColor(kBlue-9)    
            legend.AddEntry(h_effs["el_2017"], "2017, lepton trigger: el.")
            h_effs["el_2018"].SetLineColor(kAzure+1)    
            legend.AddEntry(h_effs["el_2018"], "2018, lepton trigger: el.")

            h_effs["mu_2016"].SetLineColor(kRed)    
            legend.AddEntry(h_effs["mu_2016"], "2016, lepton trigger: #mu")
            h_effs["mu_2017"].SetLineColor(kOrange+7)    
            legend.AddEntry(h_effs["mu_2017"], "2017, lepton trigger: #mu")
            h_effs["mu_2018"].SetLineColor(kOrange-3)    
            legend.AddEntry(h_effs["mu_2018"], "2018, lepton trigger: #mu")
            
            #legend.AddEntry(h_effs["el_2016"], "denom. trigger: electron")
            #legend.AddEntry(h_effs["mu_2016"], "denom. trigger: muon")
            #legend.AddEntry(h_effs["el_2016_legend"], "2016")
            #legend.AddEntry(h_effs["el_2017_legend"], "2017")
            #legend.AddEntry(h_effs["el_2018_legend"], "2018")
            

            tl2 = TLatex()
            tl2.SetNDC()
            #tl2.SetTextFont(50)
            tl2.SetTextSize(0.027)
            tl2.DrawLatex(0.15,0.27, "#epsilon = #frac{n_{ev}(lepton trigger & MET trigger)}{n_{ev}(MET trigger)} ")
            
            legend.Draw()
    
            shared_utils.stamp()
            c1.SetGrid(True)
    
            c1.SaveAs("eff_%s_%s.pdf" % (channel, variable))
            


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

    pt_electron_trigger_efficiency = TEfficiency(pt_singleelectron_eltrigger.Clone(), pt_singleelectron_mettrigger.Clone())
    pt_singlemuon_trigger_efficiency = TEfficiency(pt_singlemuon_mutrigger.Clone(), pt_singlemuon_mettrigger.Clone())

    #pt_electron_trigger_efficiency = pt_singleelectron_eltrigger.Clone()
    #pt_electron_trigger_efficiency.Divide(pt_singleelectron_mettrigger)
    #pt_singlemuon_trigger_efficiency = pt_singlemuon_mutrigger.Clone()
    #pt_singlemuon_trigger_efficiency.Divide(pt_singlemuon_mettrigger)

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
    parser.add_option("--folder", dest = "folder", default="output5_met")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--plot", dest="plot", action="store_true")
    (options, args) = parser.parse_args()
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
    gROOT.SetBatch(True)

    print "Get single lepton trigger efficiency from skim"

    if options.hadd:
        #os.system("hadd -f Run2016_barrel.root %s/Run2016*_barrel.root" % (options.folder))
        #os.system("hadd -f Run2016_endcap.root %s/Run2016*_endcap.root" % (options.folder))
        #os.system("hadd -f Run2017_barrel.root %s/Run2017*_barrel.root" % (options.folder))
        #os.system("hadd -f Run2017_endcap.root %s/Run2017*_endcap.root" % (options.folder))
        #os.system("hadd -f Run2018_barrel.root %s/Run2018*_barrel.root" % (options.folder))
        #os.system("hadd -f Run2018_endcap.root %s/Run2018*_endcap.root" % (options.folder))

        os.system("hadd -f Run2016_MET.root output5_met/Run2016*.root &")
        os.system("hadd -f Run2017_MET.root output5_met/Run2017*.root &")
        os.system("hadd -f Run2018_MET.root output5_met/Run2018*.root &")

        os.system("hadd -f Run2016_Lep.root output5/Run2016*.root &")
        os.system("hadd -f Run2017_Lep.root output5/Run2017*.root &")
        os.system("hadd -f Run2018_Lep.root output5/Run2018*.root &")

        #options.plot = True
        quit()

    if options.plot:
        combinedplots()
        #for period in ["2017", "2018"]:
        #    for region in ["barrel", "endcap"]:
        #        get_and_plot_ratio("Run%s_%s.root" % (period, region), "%s region, %s Data" % (region, period), "%s_singlelepton_trigger_%s.pdf" % (region, period))
        #        get_and_plot_ratio("Run%s_%s.root" % (period, region), "%s region, %s Data" % (region, period), "%s_singlelepton_trigger_%s.png" % (region, period))

    # otherwise run locally:
    else:
        options.inputfiles = options.inputfiles.split(",")
        #main(options.inputfiles, options.outputfile.replace(".root", "_barrel.root"), eta_low = 0, eta_high = 1.5)
        #main(options.inputfiles, options.outputfile.replace(".root", "_endcap.root"), eta_low = 1.5, eta_high = 2.4)
        main(options.inputfiles, options.outputfile.replace(".root", ".root"))
        
