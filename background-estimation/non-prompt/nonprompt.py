#!/bin/env python
from __future__ import division
from ROOT import *
from optparse import OptionParser
import math, os, glob
from GridEngineTools import runParallel
import collections
import shared_utils
import re
    
def correct_dedx_intercalibration(dedx, filename):
    
    correction_values = shared_utils.datacalibdict
    correction_value = 1.0
    for label in correction_values:
        if label in filename:
            correction_value = correction_values[label]    
    return correction_value * dedx


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
           ( (not sideband and DeDxAverage >= binkey[8][0] and DeDxAverage <= binkey[8][1]) or sideband) and \
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


def fill_histogram(histos, histogram_name, variable, value, weight):
    
    histogram_names = [histogram_name, histogram_name.replace("_short_", "_combined_").replace("_long_", "_combined_").replace("_multi_", "_combined_")]

    for histogram_name in histogram_names:
        histogram = histos[histogram_name]

        # and value>0 and value%2!=0

        if "region" in histogram_name and "ZoneDeDx" in histogram_name and value>0:
            histogram.Fill(value, weight)
            histogram.Fill(value + 1, weight)
        else:
            histogram.Fill(value, weight)


def event_loop(input_filenames, output_file, nevents=-1, treename="Events", event_start=0, fakerate_file="fakerate.root"):

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

    nev = 0
    ignore_files = []

    if "_skim.root" in input_filenames[0]:

        # use identifier to get n_ev, useful when input hasn't been merged yet:
        file_name = input_filenames[0].split("/")[-1]
        identifier = "_".join(file_name.split("_")[:-2]).replace("_ext1", "*").replace("_ext2", "*").replace("_ext3", "*").replace("ext4", "*")
        if "/" in input_filenames[0]:
            folder = "/".join(input_filenames[0].split("/")[:-1])
        else:
            folder = "."
        print "globstring:", folder + "/*%s*" % identifier
        loop_over_files = glob.glob(folder + "/*%s*" % identifier)
        loop_over_files += glob.glob(folder + "/*%s*" % identifier.replace("AOD_", "ext1AOD_"))
        loop_over_files += glob.glob(folder + "/*%s*" % identifier.replace("AOD_", "ext2AOD_"))
        loop_over_files += glob.glob(folder + "/*%s*" % identifier.replace("AOD_", "ext3AOD_"))
        loop_over_files = list(set(loop_over_files))

    else:

        # only use input filenames for n_ev calculation
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

    event_selections = {
                "Baseline":          "(n_goodleptons==0 || tracks_invmass>110)",
                "HadBaseline":       "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || tracks_invmass>110)",
                "SMuBaseline":       "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leptons_mt>90",
                "SMuValidationZLL":  "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElBaseline":       "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leptons_mt>90",
                "SElValidationZLL":  "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElValidationMT":   "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leptons_mt<70",
                "SMuValidationMT":   "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leptons_mt<70",
                      }

    # add zones:
    for event_selection in event_selections.keys():
        for zone in ["ZoneDeDx0p0to2p1", "ZoneDeDx4p0toInf"]:
            lower_cut = zone.split("DeDx")[-1].split("to")[0].replace("p", ".")
            higher_cut = zone.split("to")[-1].replace("p", ".")
            if higher_cut == "Inf":
                higher_cut = 9999
            event_selections[event_selection + zone] = event_selections[event_selection] + " && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (lower_cut, higher_cut)
                      
    # load fakerate maps...
    h_fakerates = {}   
    fakerate_variable = "HT:n_allvertices"
    fakerate_maptag = "qcd_lowMHT_loose8"
    tfile_fakerate = TFile(fakerate_file, "open")
    h_fakerates["short"] = tfile_fakerate.Get("%s_short/%s/fakerate_%s" % (fakerate_maptag, data_period, fakerate_variable.replace(":", "_")))
    h_fakerates["long"] = tfile_fakerate.Get("%s_long/%s/fakerate_%s" % (fakerate_maptag, data_period, fakerate_variable.replace(":", "_")))

    # output histograms
    histos = {
        "leptonMT": TH1F("leptonMT", "leptonMT", 16, 0, 160),
        "InvMass": TH1F("InvMass", "InvMass", 50, 0, 200),
        "HT": TH1F("HT", "HT", 35 , 0, 700),
        "MET": TH1F("MET", "MET", 35 , 0, 700),
        "MHT": TH1F("MHT", "MHT", 35 , 0, 700),
        "DeDx": TH1F("DeDx", "DeDx", 60, 0, 6),
        "DeDxCorrected": TH1F("DeDxCorrected", "DeDxCorrected", 60, 0, 6),
        "region": TH1F("region", "region", 88, 1, 89),
        #"n_tags": TH1F("n_tags", "n_tags", 3, 0, 3),
        #"n_goodjets": TH1F("n_goodjets", "n_goodjets", 10, 0, 10),
        #"n_goodelectrons": TH1F("n_goodelectrons", "n_goodelectrons", 5, 0, 5),
        #"n_goodmuons": TH1F("n_goodmuons", "n_goodmuons", 5, 0, 5),
        #"MinDeltaPhiMhtJets": TH1F("MinDeltaPhiMhtJets", "MinDeltaPhiMhtJets", 16, 0, 3.2),
        #"n_btags": TH1F("n_btags", "n_btags", 4, 0, 4),
        #"Track1MassFromDedx": TH1F("Track1MassFromDedx", "Track1MassFromDedx", 25, 0, 1000),
        #"Log10DedxMass": TH1F("Log10DedxMass", "Log10DedxMass", 10, 0, 5),
             }

    output_variables = histos.keys()

    # add histograms for the regions
    for variable in histos.keys():
        for category in ["combined", "short", "long", "multi"]:
            for event_selection in event_selections:
                    for itype in ["signalfake", "signalprompt", "control", "controlfake", "controlprompt", "signal", "prediction"]:
                        h_name = "%s_%s_%s_%s" % (variable, itype, category, event_selection)
                        histos[h_name] = histos[variable].Clone()
                        histos[h_name].SetName(h_name)

    nev_tree = tree.GetEntries()
    print "Looping over %s events" % nev_tree
    
    for iEv, event in enumerate(tree):

        if iEv < event_start: continue
        if nevents > 0 and iEv > nevents + event_start: break
        
        if (iEv+1) % 100 == 0:
            print "Processing event %s / %s" % (iEv + 1, nev_tree)

        if is_data:
            weight = 1.0
        else:
            weight = 1.0 * event.CrossSection * event.puWeight / nev

        # loop over all event selections:
        for event_selection in event_selections:

            # check event level:
            if event_selections[event_selection] != "" and not tree.Query("", event_selections[event_selection], "", 1, iEv).GetRowCount(): continue

            # check for  leptons_mt>90 cut:
            if "Baseline" in event_selection and event.n_goodleptons>0:
                pass_event = True
                for i in range(len(event.leptons_mt)):
                    if event.leptons_mt < 90:
                        pass_event = False
                if not pass_event: continue

            tagged_tracks = {}
            tagged_tracks["SR_short"] = []
            tagged_tracks["CR_short"] = []
            tagged_tracks["SR_long"] = []
            tagged_tracks["CR_long"] = []

            regions = {}
            regions["region_signal"] = 0
            regions["region_control"] = 0

            # loop over all tracks and tag all disappearing tracks:
            for i, track in enumerate(event.tracks_pt):

                # need to recheck track level cuts here:
                if "n_goodleptons==0" in event_selections[event_selection] and event.n_goodleptons==0:
                    pass
                else:
                    if "tracks_invmass<" in event_selections[event_selection]:
                        cutval = event_selections[event_selection].split("tracks_invmass<")[-1].split()[0].replace("(", "").replace(")", "")
                        if not eval("event.tracks_invmass<%s" % cutval):
                            continue
                    if "tracks_invmass>" in event_selections[event_selection]:
                        cutval = event_selections[event_selection].split("tracks_invmass>")[-1].split()[0].replace("(", "").replace(")", "")
                        if not eval("event.tracks_invmass>%s" % cutval):
                            continue

                SR_short = event.tracks_SR_short[i]==1
                SR_long = event.tracks_SR_long[i]==1
                CR_short = event.tracks_CR_short[i]==1
                CR_long = event.tracks_CR_long[i]==1

                if SR_short or CR_short or SR_long or CR_long:

                    is_prompt_track = event.tracks_prompt_electron[i]==1 or event.tracks_prompt_muon[i]==1 or event.tracks_prompt_tau[i]==1 or event.tracks_prompt_tau_leadtrk[i]==1
                    is_fake_track = event.tracks_fake[i]==1
                    dedx = event.tracks_deDxHarmonic2pixel[i]
                    dedx_corrected = correct_dedx_intercalibration(dedx, input_filenames[0])
                    log10dedxmass = TMath.Log10(TMath.Sqrt((dedx-3.01) * pow(event.tracks_pt[i] * TMath.CosH(event.tracks_eta[i]),2)/1.74))
                    log10dedxmass_corrected = TMath.Log10(TMath.Sqrt((dedx_corrected-3.01) * pow(event.tracks_pt[i] * TMath.CosH(event.tracks_eta[i]),2)/1.74))
                    InvMass = event.tracks_invmass[i]

                    track_info = {
                                   "is_pixel_track": event.tracks_is_pixel_track[i],
                                   "is_prompt_track": is_prompt_track,
                                   "is_fake_track": is_fake_track,
                                   "dedx": dedx,
                                   "dedx_corrected": dedx_corrected,
                                   "log10dedxmass": log10dedxmass,
                                   "log10dedxmass_corrected": log10dedxmass_corrected,
                                   "InvMass": InvMass,
                                 }
                    
                    if SR_short:
                        tagged_tracks["SR_short"].append(track_info)
                    if CR_short:
                        tagged_tracks["CR_short"].append(track_info)
                    if SR_long:
                        tagged_tracks["SR_long"].append(track_info)
                    if CR_long:
                        tagged_tracks["CR_long"].append(track_info)

            n_DT = {}
            n_DT["signal"] = len(tagged_tracks["SR_short"]) + len(tagged_tracks["SR_long"])
            n_DT["control"] = len(tagged_tracks["CR_short"]) + len(tagged_tracks["CR_long"])
            
            if n_DT["signal"] + n_DT["control"] == 0:
                continue 
            
            # get signal region bin:
            if n_DT["signal"]>0:
                is_pixel_track = list(tagged_tracks["SR_short"] + tagged_tracks["SR_long"])[0]["is_pixel_track"]
                dedx = list(tagged_tracks["SR_short"] + tagged_tracks["SR_long"])[0]["dedx"]

                if "ZoneDeDx" in event_selection:
                    regions["region_signal"] = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT["signal"], is_pixel_track, dedx, event.n_goodelectrons, event.n_goodmuons, input_filenames[0], sideband = True)
                else:
                    regions["region_signal"] = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT["signal"], is_pixel_track, dedx, event.n_goodelectrons, event.n_goodmuons, input_filenames[0])

            if n_DT["control"]>0:
                is_pixel_track = list(tagged_tracks["CR_short"] + tagged_tracks["CR_long"])[0]["is_pixel_track"]
                dedx = list(tagged_tracks["CR_short"] + tagged_tracks["CR_long"])[0]["dedx"]

                if "ZoneDeDx" in event_selection:
                    regions["region_control"] = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT["control"], is_pixel_track, dedx, event.n_goodelectrons, event.n_goodmuons, input_filenames[0], sideband = True)
                else:
                    regions["region_control"] = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT["control"], is_pixel_track, dedx, event.n_goodelectrons, event.n_goodmuons, input_filenames[0])
                        
            # get fake rate for event:
            fakerate_short = -1
            fakerate_long = -1
            if ":" in fakerate_variable:
                xvalue = eval("event.%s" % fakerate_variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[1])
                yvalue = eval("event.%s" % fakerate_variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[0])                
                fakerate_short = getBinContent_with_overflow(h_fakerates["short"], xvalue, yval = yvalue)
                fakerate_long = getBinContent_with_overflow(h_fakerates["long"], xvalue, yval = yvalue)
            else:                
                xvalue = eval("event.%s" % fakerate_variable)
                fakerate_short = getBinContent_with_overflow(h_fakerates["short"], xvalue)
                fakerate_long = getBinContent_with_overflow(h_fakerates["long"], xvalue)
                        
            # fill histograms:    
            for variable in output_variables:

                if variable == "leptonMT" and len(event.leptons_mt) == 0:
                    continue

                for current_region in ["signal", "control"]:
                    
                    current_region_short = current_region.replace("signal", "SR").replace("control", "CR")
                
                    if n_DT[current_region] == 1:
                        for category in ["short", "long"]:
                            if len(tagged_tracks[current_region_short + "_" + category]) == 1:                                
                                if variable == "region":
                                    value = regions["region_%s" % current_region]
                                elif variable == "DeDx":
                                    value = tagged_tracks[current_region_short + "_" + category][0]["dedx"]
                                elif variable == "DeDxCorrected":
                                    value = tagged_tracks[current_region_short + "_" + category][0]["dedx_corrected"]
                                elif variable == "leptonMT":
                                    value = event.leptons_mt[0]
                                elif variable == "InvMass":
                                    value = tagged_tracks[current_region_short + "_" + category][0]["InvMass"]
                                else:
                                    value = eval("event.%s" % variable)
                                                                
                                fill_histogram(histos, variable + "_" + current_region + "_" + category + "_" + event_selection, variable, value, weight)
                                if tagged_tracks[current_region_short + "_" + category][0]["is_fake_track"] == 1:
                                    fill_histogram(histos, variable + "_" + current_region + "fake_" + category + "_" + event_selection, variable, value, weight)
                                if tagged_tracks[current_region_short + "_" + category][0]["is_prompt_track"] == 1:
                                    fill_histogram(histos, variable + "_" + current_region + "prompt_" + category + "_" + event_selection, variable, value, weight)
                                    
                                if current_region == "control" and category == "short":
                                    fill_histogram(histos, variable + "_prediction_" + category + "_" + event_selection, variable, value, weight * fakerate_short)
                                elif current_region == "control" and category == "long":
                                    fill_histogram(histos, variable + "_prediction_" + category + "_" + event_selection, variable, value, weight * fakerate_long)

                    elif n_DT[current_region] >= 2:
                        
                        if variable == "region":
                            value = regions["region_%s" % current_region]
                        elif variable == "DeDx":
                            value = list(tagged_tracks[current_region_short + "_short"] + tagged_tracks[current_region_short + "_long"])[0]["dedx"]
                        elif variable == "DeDxCorrected":
                            value = list(tagged_tracks[current_region_short + "_short"] + tagged_tracks[current_region_short + "_long"])[0]["dedx_corrected"]
                        elif variable == "leptonMT":
                            value = event.leptons_mt[0]
                        elif variable == "InvMass":
                            value = list(tagged_tracks[current_region_short + "_short"] + tagged_tracks[current_region_short + "_long"])[0]["InvMass"]
                        else:
                            value = eval("event.%s" % variable)

                        fill_histogram(histos, variable + "_" + current_region + "_multi_" + event_selection, variable, value, weight)
                        
                        # check if all tagged tracks are fake or prompt tracks:
                        all_tracks_are_fake = True
                        all_tracks_are_prompt = True
                        all_tracks_are_short = True
                        all_tracks_are_long = True
                        
                        for track in list(tagged_tracks[current_region_short + "_short"] + tagged_tracks[current_region_short + "_long"]):
                            if track["is_prompt_track"] != 1:
                                all_tracks_are_prompt = False
                            if track["is_fake_track"] != 1:
                                all_tracks_are_fake = False
                            if track["is_pixel_track"] != 1:
                                all_tracks_are_short = False
                            if track["is_pixel_track"] != 0:
                                all_tracks_are_long = False
                                
                        if all_tracks_are_prompt:
                            fill_histogram(histos, variable + "_" + current_region + "prompt_multi_" + event_selection, variable, value, weight)
                        if all_tracks_are_fake:
                            fill_histogram(histos, variable + "_" + current_region + "fake_multi_" + event_selection, variable, value, weight)
                            
                        if current_region == "control" and all_tracks_are_short:
                            fill_histogram(histos, variable + "_prediction_multi_" + event_selection, variable, value, weight * fakerate_short * fakerate_short)
                        elif current_region == "control" and all_tracks_are_long:
                            fill_histogram(histos, variable + "_prediction_multi_" + event_selection, variable, value, weight * fakerate_long * fakerate_long)
                        elif current_region == "control":
                            fill_histogram(histos, variable + "_prediction_multi_" + event_selection, variable, value, weight * fakerate_short * fakerate_long)
                        

                            
                         
    if event_start>0:
        output_file = output_file.replace(".root", "_%s.root" % event_start)

    fout = TFile(output_file, "recreate")
    for var in histos:
        histos[var].Write()

    fout.Close()


def hadd_everything(options):

    #os.system("hadd -f %s/prediction_Summer16_all.root %s/Summer16*.root &" % (options.prediction_folder, options.prediction_folder))
    #os.system("hadd -f %s/prediction_Summer16_QCDZJets.root %s/Summer16.QCD*.root %s/Summer16.ZJets*.root &" % (options.prediction_folder, options.prediction_folder, options.prediction_folder))
    #os.system("hadd -f %s/prediction_Run2016_all.root %s/Run2016*MET*.root %s/Run2016*SingleMuon*.root %s/Run2016*SingleElectron*.root &" % (options.prediction_folder, options.prediction_folder, options.prediction_folder, options.prediction_folder))
    #os.system("hadd -f %s/prediction_Run2016_MET.root %s/Run2016*MET*.root &" % (options.prediction_folder, options.prediction_folder))
    os.system("hadd -f %s/prediction_Run2016_SingleElectron.root %s/Run2016*SingleElectron*.root &" % (options.prediction_folder, options.prediction_folder))
    os.system("hadd -f %s/prediction_Run2016_SingleMuon.root %s/Run2016*SingleMuon*.root &" % (options.prediction_folder, options.prediction_folder))
    #for period in ["", "B", "C", "D", "E", "F", "G", "H"]:
    #    os.system("hadd -f %s/prediction_Run2016%s.root %s/Run2016%s*MET*.root %s/Run2016%s*SingleMuon*.root %s/Run2016%s*SingleElectron*.root" % (options.prediction_folder, period, options.prediction_folder, period, options.prediction_folder, period, options.prediction_folder, period))
    #    os.system("hadd -f %s/prediction_Run2016%s_MET.root %s/Run2016%s*MET*.root" % (options.prediction_folder, period, options.prediction_folder, period))   
                 

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles")
    parser.add_option("--output", dest = "outputfiles")
    parser.add_option("--folder", dest = "prediction_folder", default="prediction")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--unweighted", dest="unweighted", action="store_true")
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--jobs_per_file", dest = "jobs_per_file", default = 3)
    parser.add_option("--njobs", dest = "njobs", default = 2000)
    parser.add_option("--event_start", dest = "event_start", default = 0)
    parser.add_option("--fakerate_file", dest = "fakerate_file", default = "fakerate.root")
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--start", dest="start", action="store_true")
    (options, args) = parser.parse_args()
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    if options.hadd:
        hadd_everything(options)
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
        input_files += glob.glob(options.inputfiles + "/Summer16.TT_Tune*.root")
        input_files += glob.glob(options.inputfiles + "/Run2016*MET*.root")
        input_files += glob.glob(options.inputfiles + "/Run2016*SingleElectron*.root")
        input_files += glob.glob(options.inputfiles + "/Run2016*SingleMuon*.root")

        os.system("mkdir -p %s" % options.prediction_folder)
        commands = []
 
        if True:

            if options.njobs > len(input_files):
                options.njobs = len(input_files)

            file_segments = [input_files[x:x+int(len(input_files)/options.njobs)] for x in range(0, len(input_files), int(len(input_files)/options.njobs))]
            for file_segment in file_segments:
                command = ""
                for input_file in file_segment:
                    command += "./nonprompt.py --input %s --output %s/%s --fakerate_file %s; " % (input_file, options.prediction_folder, file_segment[0].split("/")[-1], options.fakerate_file)
                commands.append(command)

        if False:

            for input_file in input_files:

                # get nev:
                tree = TChain("Events")
                tree.Add(input_file)
                nev = tree.GetEntries()
                nev_per_interval = int(nev/int(options.jobs_per_file))
                 
                for i in range(int(options.jobs_per_file)):
                    event_start = i * nev_per_interval
                    commands.append("./nonprompt.py --input %s --output %s/%s --nev %s --fakerate_file %s --event_start %s" % (input_file, options.prediction_folder, input_file.split("/")[-1], nev_per_interval, options.fakerate_file, event_start))
           
        runParallel(commands, options.runmode, condorDir = "nonprompt.condor", use_more_mem=False, use_more_time=False, confirm=not options.start)

        hadd_everything(options)

    # otherwise run locally:
    else:

        if not options.inputfiles and args:
            inputfiles_list = args
        else:
            inputfiles_list = options.inputfiles.split(",")

        event_loop(inputfiles_list,
             options.outputfiles,
             nevents = int(options.nev),
             fakerate_file = options.fakerate_file,
             event_start = int(options.event_start),
            )

