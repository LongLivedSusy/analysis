#!/bin/env python
from __future__ import division
from ROOT import *
from optparse import OptionParser
import math, os, glob
from GridEngineTools import runParallel
#import collections
import re
import shared_utils
import random
import more_itertools

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
        

def parse_root_cutstring(cut, tracks_increment_variable = "i"):

    # this function converts ROOT cutstrings into python eval statements.

    output = cut
    variables = re.findall(r'\w+', cut)

    for variable in list(set(variables)):
        try:
            float(variable)
        except:
            if "tracks_" in variable:
                output = re.sub(r"\b%s\b" % variable, "event." + variable + "[" + tracks_increment_variable + "]", output)
            else:
                output = re.sub(r"\b%s\b" % variable, "event." + variable, output)

    output = output.replace("&&", "and").replace("||", "or")

    if output.split()[0] == "and":
        output = " ".join(output.split()[1:])

    return output


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
        elif "SingleElectron" in filename and n_goodelectrons==0:
            return 0
        else:
            return region
    else:
        return region


def fill_histogram(event, variable, histograms, event_selection, data_period, zone, variables, weight, scaling, i_track, filename):
                    
    h_name = variable + "_" + event_selection + "_" + data_period + "_" + zone
    sideband = False
    
    if "tracks_" in variable:
        value = eval("event.%s[%s]" % (variable, i_track))
        
    elif "region" in variable:
        
        if "sideband" in variable:
            sideband = True
        
        # recalculate region number, signal region:
        if "sr" in zone and event.n_tracks_SR_short==1 and event.n_tracks_SR_long==0:
            DeDx = -1
            for i in range(len(event.tracks_pt)):
                if event.tracks_SR_short[i] == 1:
                    if "Corrected" in variable:
                        DeDx = event.tracks_deDxHarmonic2pixelCorrected[i]
                    else:
                        DeDx = event.tracks_deDxHarmonic2pixel[i]
                    break
            value = get_signal_region(event.HT, event.MHT, event.n_jets, event.n_btags, event.MinDeltaPhiMhtJets, event.n_tracks_SR_short, True, DeDx, event.n_goodelectrons, event.n_goodmuons, filename, sideband = sideband)
            
        elif "sr" in zone and event.n_tracks_SR_long==1 and event.n_tracks_SR_short==0:
            DeDx = -1
            for i in range(len(event.tracks_pt)):
                if event.tracks_SR_long[i] == 1:
                    if "Corrected" in variable:
                        DeDx = event.tracks_deDxHarmonic2pixelCorrected[i]
                    else:
                        DeDx = event.tracks_deDxHarmonic2pixel[i]
                    break
            value = get_signal_region(event.HT, event.MHT, event.n_jets, event.n_btags, event.MinDeltaPhiMhtJets, event.n_tracks_SR_long, False, DeDx, event.n_goodelectrons, event.n_goodmuons, filename, sideband = sideband)
            
        elif "sr" in zone and event.n_tracks_SR_long>1 or event.n_tracks_SR_short>1:
            # in this case, take highest DeDx of both DTs:
            DeDx = -1
            for i in range(len(event.tracks_pt)):
                if (event.tracks_SR_long[i] + event.tracks_SR_short[i])>0:
                    if "Corrected" in variable:
                        if event.tracks_deDxHarmonic2pixelCorrected[i] > DeDx:
                            DeDx = event.tracks_deDxHarmonic2pixelCorrected[i]
                    else:
                        if event.tracks_deDxHarmonic2pixel[i] > DeDx:
                            DeDx = event.tracks_deDxHarmonic2pixel[i]
            value = get_signal_region(event.HT, event.MHT, event.n_jets, event.n_btags, event.MinDeltaPhiMhtJets, event.n_tracks_SR_short + event.n_tracks_SR_long, False, DeDx, event.n_goodelectrons, event.n_goodmuons, filename, sideband = sideband)            
                        
        # recalculate region number, fake control region:
        elif "fake" in zone and event.n_tracks_CR_short==1 and event.n_tracks_CR_long==0:
            DeDx = -1
            for i in range(len(event.tracks_pt)):
                if event.tracks_CR_short[i] == 1:
                    if "Corrected" in variable:
                        DeDx = event.tracks_deDxHarmonic2pixelCorrected[i]
                    else:
                        DeDx = event.tracks_deDxHarmonic2pixel[i]
                    break
            value = get_signal_region(event.HT, event.MHT, event.n_jets, event.n_btags, event.MinDeltaPhiMhtJets, event.n_tracks_CR_short, True, DeDx, event.n_goodelectrons, event.n_goodmuons, filename, sideband = sideband)
            
        elif "fake" in zone and event.n_tracks_CR_long==1 and event.n_tracks_CR_short==0:
            DeDx = -1
            for i in range(len(event.tracks_pt)):
                if event.tracks_CR_long[i] == 1:
                    if "Corrected" in variable:
                        DeDx = event.tracks_deDxHarmonic2pixelCorrected[i]
                    else:
                        DeDx = event.tracks_deDxHarmonic2pixel[i]
                    break
            value = get_signal_region(event.HT, event.MHT, event.n_jets, event.n_btags, event.MinDeltaPhiMhtJets, event.n_tracks_CR_long, False, DeDx, event.n_goodelectrons, event.n_goodmuons, filename, sideband = sideband)
            
        elif "fake" in zone and event.n_tracks_CR_long>1 or event.n_tracks_CR_short>1:
            # in this case, take highest DeDx of both DTs:
            DeDx = -1
            for i in range(len(event.tracks_pt)):
                if (event.tracks_CR_long[i] + event.tracks_CR_short[i])>0:
                    if "Corrected" in variable:
                        if event.tracks_deDxHarmonic2pixelCorrected[i] > DeDx:
                            DeDx = event.tracks_deDxHarmonic2pixelCorrected[i]
                    else:
                        if event.tracks_deDxHarmonic2pixel[i] > DeDx:
                            DeDx = event.tracks_deDxHarmonic2pixel[i]
            value = get_signal_region(event.HT, event.MHT, event.n_jets, event.n_btags, event.MinDeltaPhiMhtJets, event.n_tracks_CR_short + event.n_tracks_CR_long, False, DeDx, event.n_goodelectrons, event.n_goodmuons, filename, sideband = sideband)            
                        
        else:
            
            value = 0
        
    else:
        value = eval("event.%s" % variable)
    
    histograms[h_name].Fill(value, weight*scaling)

    # if filling the sideband region histogram, fill also the following bin:
    if sideband and "region" in variable and value > 0:
        histograms[h_name].Fill(value+1, weight*scaling)


def get_fakerate(event, fakerate_variables, fakerate_regions, data_period, h_fakerate):
    
    fakerates = {}
    
    for fakerate_variable in fakerate_variables:                
        for fakerate_region in fakerate_regions:
            for fakerate_type in ["fakerate", "fakerateIso"]:
                for category in ["short", "long"]:
                    
                    if data_period == "Run2016":
                        this_data_period = "Run2016GH"
                    else:
                        this_data_period = data_period
                    
                    label = "%s_%s_%s_%s_%s" % (fakerate_variable.replace(":", "_"), fakerate_region, this_data_period, fakerate_type, category)
                                            
                    if ":" in fakerate_variable:
                        xvalue = eval("event.%s" % fakerate_variable.split(":")[1])
                        yvalue = eval("event.%s" % fakerate_variable.split(":")[0])
                        fakerates[fakerate_variable.replace(":", "_") + "_" + fakerate_region + "_" + fakerate_type + "_" + category] = getBinContent_with_overflow(h_fakerate[label], xvalue, yval = yvalue)
                    else:
                        xvalue = eval("event.%s" % fakerate_variable)
                        fakerates[fakerate_variable.replace(":", "_") + "_" + fakerate_region + "_" + fakerate_type + "_" + category] = getBinContent_with_overflow(h_fakerate[label], xvalue)
    
    return fakerates
    

def event_loop(input_filenames, output_file, nevents=-1, treename="Events", event_start=0, fakerate_filename="fakerate.root", input_is_unmerged = True):

    # check if output file exists:
    if os.path.exists(output_file):
        print "Already done, do file check"
        try:
            test = TFile(output_file)
            if not (test.IsZombie() or test.TestBit(TFile.kRecovered)):
                print "Already done, file ok"
                test.Close()
                return
            test.Close()
        except:
            print "Need to redo file"

    # check if data:
    phase = 0
    data_period = ""
    is_data = False
    first_filename = input_filenames[0]
    for label in ["Run2016", "Run2017", "Run2018", "Summer16", "Fall17", "Autumn18"]:
        if label in first_filename:
            data_period = label
            if "Run201" in label:
                is_data = True
            if label == "Run2016" or label == "Summer16":
                phase = 0
            elif label == "Run2017" or label == "Run2018" or label == "Fall17" or label == "Autumn18":
                phase = 1

    nev = 0
    ignore_files = []

    if not is_data:
        if input_is_unmerged:
        
            print "Input is unmerged..."
            file_name = input_filenames[0].split("/")[-1]
            identifier = "_".join(file_name.split("_")[:-2]).replace("_ext1", "*").replace("_ext2", "*").replace("_ext3", "*").replace("ext4", "*")
            if "/" in input_filenames[0]:
                folder = "/".join(input_filenames[0].split("/")[:-1])
            else:
                folder = "."
            print "globstring:", folder + "/*%s*" % identifier
            loop_over_files = glob.glob(folder + "/*%s*.root" % identifier)
            loop_over_files += glob.glob(folder + "/*%s*.root" % identifier.replace("AOD_", "ext1AOD_"))
            loop_over_files += glob.glob(folder + "/*%s*.root" % identifier.replace("AOD_", "ext2AOD_"))
            loop_over_files += glob.glob(folder + "/*%s*.root" % identifier.replace("AOD_", "ext3AOD_"))
            loop_over_files = list(set(loop_over_files))
        
        else:
            loop_over_files = input_filenames
        
        for tree_file in loop_over_files:
            print "Reading %s for n_ev calculation..." % tree_file 
            try:
                fin = TFile(tree_file)
                fin.Get("nev")
                fin.Get(treename)
                h_nev = fin.Get("nev")
                nev += int(h_nev.GetBinContent(1))
                fin.Close()
            except:
                "Ignoring file: %s" % tree_file
                ignore_files.append(ignore_files)
                print "Ignoring", tree_file
                continue
        
        print "n_ev for weighting: %s" % nev

    tree = TChain(treename)       
    for i, tree_file in enumerate(input_filenames):
        if not tree_file in ignore_files:
            tree.Add(tree_file)
    
    dEdxSidebandLow = 1.6
    dEdxLow = 2.1
    dEdxMid = 4.0
    
    event_selections = {
                "Baseline":              "(n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "BaselineJetsNoLeptons": "n_goodjets>=1 && n_goodleptons==0 && MHT>150",
                "BaselineElectrons":     "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "BaselineMuons":         "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110 && leadinglepton_mt>90",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leadinglepton_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<70",
                #"FakeRateDet":            "n_goodleptons==0 && MHT<150",
                "PromptEl":               "n_goodelectrons==1 && n_goodmuons==0",
                      }
    
    event_selections_notracks = {
                "Baseline":               "(n_goodleptons==0 || leadinglepton_mt>90)",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0 && MHT>150",
                "BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && leadinglepton_mt>90",
                "BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && leadinglepton_mt>90",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || (leadinglepton_mt>90))",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && leadinglepton_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && leadinglepton_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && leadinglepton_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && leadinglepton_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leadinglepton_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<70",
                #"FakeRateDet":            "n_goodleptons==0 && MHT<150",
                "PromptEl":               "n_goodelectrons==1 && n_goodmuons==0",
                      }
    
    zones = {}
    for dedx in ["_SidebandDeDx", "_MidDeDx", "_HighDeDx"]:
        if dedx == "_SidebandDeDx":
            lower = dEdxSidebandLow; upper = dEdxLow
        elif dedx == "_MidDeDx":
            lower = dEdxLow; upper = dEdxMid
        elif dedx == "_MidHighDeDx":
            lower = dEdxLow; upper = 9999
        elif dedx == "_HighDeDx":
            lower = dEdxMid; upper = 9999
        elif dedx == "":
            lower = 0; upper = 9999
        
        for category in ["short", "long"]:
            
            if category == "short":
                is_pixel_track = 1
            else:
                is_pixel_track = 0
            
            zones["sr%s_%s" % (dedx, category)] = [" && tracks_is_pixel_track==%s && tracks_SR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (is_pixel_track, category, lower, upper), ""]
            zones["srgenfake%s_%s" % (dedx, category)] = [" && tracks_is_pixel_track==%s && tracks_SR_%s==1 && tracks_fake==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (is_pixel_track, category, lower, upper), ""]
            zones["srgenprompt%s_%s" % (dedx, category)] = [" && tracks_is_pixel_track==%s && tracks_SR_%s==1 && tracks_fake==0 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (is_pixel_track, category, lower, upper), ""]
            
            # previous FR CR region:
            zones["fakecr%s_%s" % (dedx, category)] = [" && tracks_is_pixel_track==%s && tracks_CR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (is_pixel_track, category, lower, upper), ""]
            zones["fakeprediction%s_%s" % (dedx, category)] = [" && tracks_is_pixel_track==%s && tracks_CR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (is_pixel_track, category, lower, upper), "HT_n_allvertices_FakeRateDet_fakerate_%s" % category]
            
            # added iso cut on FR CR and cut on MVA:
            zones["fakecrIsoMVA%s_%s" % (dedx, category)] = [" && tracks_is_pixel_track==%s && tracks_CR_%s==1 && tracks_trkRelIso<0.01 && tracks_mva_loose>-0.2 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (is_pixel_track, category, lower, upper), ""]
            zones["fakepredictionIsoMVA%s_%s" % (dedx, category)] = [" && tracks_is_pixel_track==%s && tracks_CR_%s==1 && tracks_trkRelIso<0.01 && tracks_mva_loose>-0.2 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (is_pixel_track, category, lower, upper), "HT_n_allvertices_FakeRateDet_fakerateIso_%s" % category]

            zones["PromptEl%s" % dedx] = [" && leadinglepton_dedx>%s && leadinglepton_dedx<%s" % (lower, upper), ""]
            #zones["prompt"] = ["(tracks_SR_short+tracks_SR_long)==0", ""]
            #zones["promptMu%s" % dedx] = [" && (tracks_SR_short+tracks_SR_long)==0 && n_goodelectrons==0 && n_goodmuons==1 && leadinglepton_dedx>%s && leadinglepton_dedx<%s" % (lower, upper), ""]

    # streamline zones a bit...:
    for zone_label in zones:
        for delstring in ["&& tracks_deDxHarmonic2pixel<9999", "&& tracks_deDxHarmonic2pixel>0"]:
            if delstring in zones[zone_label][0]:
                zones[zone_label][0] = zones[zone_label][0].replace(delstring, "")

    binnings = {}
    binnings["LepMT"] = [16, 0, 160]
    binnings["leptons_mt"] = binnings["LepMT"]
    binnings["leadinglepton_mt"] = binnings["LepMT"]
    binnings["InvMass"] = [50, 0, 200]
    binnings["tracks_invmass"] = binnings["InvMass"]
    binnings["Ht"] = [35 , 0, 700]
    binnings["HT"] = binnings["Ht"]
    binnings["Met"] = [35 , 0, 700]
    binnings["MET"] = binnings["Met"]
    binnings["Mht"] = [35 , 0, 700]
    binnings["MHT"] = binnings["Mht"]
    binnings["tracks_pt"] = binnings["Ht"]
    binnings["leadinglepton_pt"] = binnings["Ht"]
    binnings["leadinglepton_eta"] = [15, 0, 3]
    binnings["tracks_eta"] = [15, 0, 3]
    binnings["tracks_dxyVtx"] = [20, 0, 0.1]
    binnings["DeDxAverage"] = [60, 0, 6]
    binnings["tracks_massfromdeDxPixel"] = binnings["DeDxAverage"]
    binnings["DeDxAverageCorrected"] = binnings["DeDxAverage"]
    binnings["tracks_deDxHarmonic2pixel"] = binnings["DeDxAverage"]
    binnings["tracks_deDxHarmonic2pixelCorrected"] = binnings["DeDxAverage"]
    binnings["BinNumber"] = [ 88, 1, 89]
    binnings["region"] = binnings["BinNumber"]
    binnings["n_tags"] = [ 3, 0, 3]
    binnings["n_goodjets"] = [ 10, 0, 10]
    binnings["n_btags"] = binnings["n_goodjets"]
    binnings["n_goodelectrons"] = [ 5, 0, 5]
    binnings["n_goodmuons"] = [ 5, 0, 5]
    binnings["MinDeltaPhiMhtJets"] = [ 16, 0, 3.2]
    binnings["BTags"] = [ 4, 0, 4]
    binnings["Track1MassFromDedx"] = [ 25, 0, 1000]
    binnings["Log10DedxMass"] = [10, 0, 5]
    binnings["regionCorrected"] = [54,1,55]
    binnings["regionCorrected_sideband"] = binnings["regionCorrected"]
    binnings["region"] = binnings["regionCorrected"]
    binnings["region_sideband"] = binnings["regionCorrected"]
    
    variables = [
                  "leadinglepton_mt",
                  #"leadinglepton_pt",
                  #"leadinglepton_eta",
                  "tracks_invmass",
                  "tracks_deDxHarmonic2pixelCorrected",
                  #"tracks_pt",
                  #"tracks_eta",
                  #"tracks_dxyVtx",
                  "HT",
                  "MHT",
                  "n_goodjets",
                  "n_btags",
                  #"region",
                  #"region_sideband",
                  "regionCorrected",
                  "regionCorrected_sideband",
                ]
    
    # construct all histograms:
    histograms = {}
    for variable in variables:
        for event_selection in event_selections:
                                     
            for zone in zones:
                if "srgen" in zone and is_data:
                    continue
                if "PromptEl" in zone and "PromptEl" not in event_selection:
                    continue
                    
                h_name = variable + "_" + event_selection + "_" + data_period + "_" + zone
                histograms[h_name] = TH1F(h_name, h_name, binnings[variable][0], binnings[variable][1], binnings[variable][2])
    
    print "# of histograms:", len(histograms)
    
    # convert ROOT cutstrings to python statements:
    event_selections_converted = {}
    for event_selection in event_selections:
        event_selections_converted[event_selection] = parse_root_cutstring(event_selections[event_selection], tracks_increment_variable = "i_track")

    event_selections_converted_notracks = {}
    for event_selection in event_selections_notracks:
        event_selections_converted_notracks[event_selection] = parse_root_cutstring(event_selections_notracks[event_selection], tracks_increment_variable = "i_track")

    zones_converted = {}    
    for zone in zones:
        zones_converted[zone] = parse_root_cutstring(zones[zone][0], tracks_increment_variable = "i_track")

    print "Loading fakerate maps..."
    h_fakerate = {}
    fakerate_variables = [
                 #"HT",
                 #"n_goodjets",
                 #"n_allvertices",
                 #"n_btags",
                 #"MinDeltaPhiMhtJets",
                 "HT:n_allvertices",
                ]
    fakerate_regions = ["FakeRateDet"]
                
    tfile_fakerate = TFile(fakerate_filename, "open")

    for variable in fakerate_variables:
        variable = variable.replace(":", "_")
        for region in fakerate_regions:
            for fakeratetype in ["fakerate", "fakerateIso"]:
                for category in ["short", "long"]:
                    if data_period == "Run2016":
                        this_data_period = "Run2016GH"
                    else:
                        this_data_period = data_period
                    label = "%s_%s_%s_%s_%s" % (variable, region, this_data_period, fakeratetype, category)
                    h_fakerate[label] = tfile_fakerate.Get(label)
                    h_fakerate[label].SetDirectory(0)
            
    tfile_fakerate.Close()

    nev_tree = tree.GetEntries()
    print "Looping over %s events" % nev_tree
    
    for iEv, event in enumerate(tree):

        if iEv < event_start: continue
        if nevents > 0 and iEv > nevents + event_start: break
        
        if (iEv+1) % 1000 == 0:
            print "%s/%s" % (iEv + 1, nev_tree)

        weight = 1.0
        if not is_data:
            weight = 1.0 * event.CrossSection * event.puWeight / nev

        # get fakerate:
        fakerates = {}
        
        # loop over all event selections:
        for event_selection in event_selections:
                        
            for zone in zones:

                if "gen" in zone and is_data:
                    continue
                if "PromptEl" in zone and "PromptEl" not in event_selection:
                    continue

                cut = event_selections[event_selection] + zones[zone][0]

                # check cutstring on event level:                
                #if not tree.Query("", cut, "", 1, iEv).GetRowCount(): continue
                
                if "PromptEl" in zone:
                    if not eval(event_selections_converted[event_selection] + " and " + zones_converted[zone]):
                        continue
                else:
                    if not eval(event_selections_converted_notracks[event_selection]):
                        continue
                                        
                scaling_factor = zones[zone][1]
                if scaling_factor == "":
                    scaling = 1.0
                else:
                    #scaling = eval("event.%s" % scaling_factor)
                    scaling = fakerates[scaling_factor]

                if len(fakerates) == 0:
                    fakerates = get_fakerate(event, fakerate_variables, fakerate_regions, data_period, h_fakerate)
                                                                                
                for variable in variables:
                    
                    if event_selection == "Baseline" and "region" not in variable:
                        continue 
                                             
                    if "tracks_" in cut:
                        
                        cut_converted = event_selections_converted[event_selection] + " and " + zones_converted[zone]
                        
                        if "tracks_" in variable:
                            for i_track in xrange(len(event.tracks_pt)):
                                if eval(cut_converted):
                                    fill_histogram(event, variable, histograms, event_selection, data_period, zone, variables, weight, scaling, i_track, first_filename)
                        else:
                            for i_track in xrange(len(event.tracks_pt)):
                                if eval(cut_converted):
                                    fill_histogram(event, variable, histograms, event_selection, data_period, zone, variables, weight, scaling, -1, first_filename)
                                    break
                            
                    else:
                        # cutstring without tracks in it                       
                        if "tracks_" in variable:
                            for i_track in xrange(len(event.tracks_pt)):
                                fill_histogram(event, variable, histograms, event_selection, data_period, zone, variables, weight, scaling, i_track, first_filename)
                        else:
                            fill_histogram(event, variable, histograms, event_selection, data_period, zone, variables, weight, scaling, -1, first_filename)
            
    if event_start>0:
        output_file = output_file.replace(".root", "_%s.root" % event_start)
    
    fout = TFile(output_file, "recreate")
    for h_name in histograms:
        histograms[h_name].Write()
    fout.Close()
                 

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles")
    parser.add_option("--output", dest = "outputfiles")
    parser.add_option("--folder", dest = "prediction_folder", default="prediction")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--unweighted", dest="unweighted", action="store_true")
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--jobs_per_file", dest = "jobs_per_file", default = 60)
    parser.add_option("--njobs", dest = "njobs")
    parser.add_option("--event_start", dest = "event_start", default = 0)
    parser.add_option("--fakerate_file", dest = "fakerate_file", default = "fakerate.root")
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--start", dest="start", action="store_true")
    parser.add_option("--unmerged", dest="unmerged", action="store_true")
    (options, args) = parser.parse_args()
    
    options.unmerged = True
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    if options.hadd:
        
        for dataset in ["Run2016*MET", "Run2016*SingleElectron", "Run2016*SingleMuon", "Summer16"]:
            os.system("hadd -f %s_%s.root %s/%s*root" % (options.prediction_folder, dataset.replace("*", ""), options.prediction_folder, dataset))
        os.system("hadd -f %s_AllRun2016.root %s_Run2016*.root" % (options.prediction_folder, options.prediction_folder))
        quit()

    # run parallel if input is a folder:
    if options.inputfiles and options.inputfiles[-1] == "/":

        print "Got input folder, running in batch mode (%s)" % options.runmode
       
        input_files = []
        input_files += glob.glob(options.inputfiles + "/Summer16.DYJetsToLL*.root")
        input_files += glob.glob(options.inputfiles + "/Summer16.QCD*.root")
        input_files += glob.glob(options.inputfiles + "/Summer16.WJetsToLNu*.root")
        input_files += glob.glob(options.inputfiles + "/Summer16.ZJetsToNuNu_HT*.root")
        input_files += glob.glob(options.inputfiles + "/Summer16.WW_TuneCUETP8M1*.root")
        input_files += glob.glob(options.inputfiles + "/Summer16.WZ_TuneCUETP8M1*.root")
        input_files += glob.glob(options.inputfiles + "/Summer16.ZZ_TuneCUETP8M1*.root")
        input_files += glob.glob(options.inputfiles + "/Summer16.TTJets*.root")
        input_files += glob.glob(options.inputfiles + "/Run2016*MET*.root")
        input_files += glob.glob(options.inputfiles + "/Run2016*SingleElectron*.root")
        input_files += glob.glob(options.inputfiles + "/Run2016*SingleMuon*.root")

        os.system("mkdir -p %s" % options.prediction_folder)
        commands = []
 
        if options.unmerged:

            print "Running unmerged"

            for input_file in input_files:
                command = "./analyze_skim.py --input %s --output %s/%s --unmerged" % (input_file, options.prediction_folder, input_file.split("/")[-1])
                commands.append(command)

            if options.njobs:
                options.njobs = int(options.njobs)
                random.shuffle(commands)
                file_segments = [list(c) for c in more_itertools.divide(int(options.njobs), commands)]
                
                new_commands = []
                for file_segment in file_segments:
                    command = "; ".join(file_segment)
                    new_commands.append(command)
                    
                commands = new_commands

        else:

            for input_file in input_files:
                tree = TChain("Events")
                tree.Add(input_file)
                nev = tree.GetEntries()
                nev_per_interval = int(nev/int(options.jobs_per_file))
                 
                for i in range(int(options.jobs_per_file)):
                    event_start = i * nev_per_interval
                    commands.append("./analyze_skim.py --input %s --output %s/%s --nev %s --event_start %s" % (input_file, options.prediction_folder, input_file.split("/")[-1], nev_per_interval, event_start))
           
        runParallel(commands, options.runmode, condorDir = "%s.condor" % options.prediction_folder, use_more_mem=False, use_more_time=21600, confirm=not options.start)

    # otherwise run locally:
    else:

        if not options.inputfiles and args:
            inputfiles_list = args
        else:
            inputfiles_list = options.inputfiles.split(",")

        event_loop(inputfiles_list,
             options.outputfiles,
             nevents = int(options.nev),
             fakerate_filename = options.fakerate_file,
             event_start = int(options.event_start),
            )

