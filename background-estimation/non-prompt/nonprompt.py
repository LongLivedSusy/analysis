#!/bin/env python
from __future__ import division
from ROOT import *
from optparse import OptionParser
import math, os, glob
from GridEngineTools import runParallel
import collections
from array import array
import tags
import shared_utils
import array

# loose8 tag
base_cuts = "tracks_is_reco_lepton==0 && tracks_passPFCandVeto==1 && tracks_nValidPixelHits>=3"
SR_short = tags.convert_cut_string(base_cuts + " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.65/0.01) - 0.25) && tracks_trkRelIso<0.01")
CR_short = tags.convert_cut_string(base_cuts + " && tracks_is_pixel_track==1 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_dxyVtx>0.02")
SR_long = tags.convert_cut_string(base_cuts + " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose>(tracks_dxyVtx*(0.7/0.01) + 0.05) && tracks_trkRelIso<0.01")
CR_long = tags.convert_cut_string(base_cuts + " && tracks_is_pixel_track==0 && tracks_mva_bdt_loose<(tracks_dxyVtx*(0.7/0.01) - 0.5) && tracks_dxyVtx>0.02")

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
    binnumbers = collections.OrderedDict()

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


def fill_histogram(histogram, variable, value, weight):
    
    if variable == "sidebandregion" and value>0 and value%2!=0:
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

    # load tree
    tree = TChain(treename)

    nev = 0
    ignore_files = []
    for tree_file in input_filenames:
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


    tree = TChain(treename)       
    for i, tree_file in enumerate(input_filenames):
        if not tree_file in ignore_files:
            tree.Add(tree_file)

    event_selections = {
                "baseline":                 "True",
                "baseline_simplecuts":      "event.MHT>150 and event.n_goodjets>=1",
                "baseline_region_MHT50":    "event.MHT>50",
                "SElValidationZLL":         "event.n_goodjets>=1 and event.n_goodelectrons>=1 and event.n_goodmuons==0 and event.dilepton_invmass>=65 and event.dilepton_invmass<=110",
                "SMuValidationZLL":         "event.n_goodjets>=1 and event.n_goodmuons>=1 and event.n_goodelectrons==0 and event.dilepton_invmass>=65 and event.dilepton_invmass<=110",
                "SElValidationMT":          "event.n_goodjets==1 and event.n_goodelectrons==1 and event.n_goodmuons==0 and event.leptons_mtw<70",
                "SMuValidationMT":          "event.n_goodjets==1 and event.n_goodmuons==1 and event.n_goodelectrons==0 and event.leptons_mtw<70",
                      }

    # load fakerate maps...
    h_fakerates = {}   
    fakerate_variable = "HT:n_allvertices"
    fakerate_maptag = "qcd_lowMHT_loose8"
    tfile_fakerate = TFile(fakerate_file, "open")
    h_fakerates["short"] = tfile_fakerate.Get("%s_short/%s/fakerate_%s" % (fakerate_maptag, data_period, fakerate_variable.replace(":", "_")))
    h_fakerates["long"] = tfile_fakerate.Get("%s_long/%s/fakerate_%s" % (fakerate_maptag, data_period, fakerate_variable.replace(":", "_")))

    # output histograms
    histos = {
        "leptonMT": TH1F("leptonMT", "leptonMT", 8, 0, 80),
        "HT": TH1F("HT", "HT", 10, 0, 2000),
        "MET": TH1F("MET", "MET", 15, 0, 1200),
        "MHT": TH1F("MHT", "MHT", 20, 0, 1000),
        "n_goodjets": TH1F("n_goodjets", "n_goodjets", 10, 0, 10),
        "n_goodelectrons": TH1F("n_goodelectrons", "n_goodelectrons", 5, 0, 5),
        "n_goodmuons": TH1F("n_goodmuons", "n_goodmuons", 5, 0, 5),
        "MinDeltaPhiMhtJets": TH1F("MinDeltaPhiMhtJets", "MinDeltaPhiMhtJets", 16, 0, 3.2),
        "n_btags": TH1F("n_btags", "n_btags", 4, 0, 4),
        #"Track1MassFromDedx": TH1F("Track1MassFromDedx", "Track1MassFromDedx", 25, 0, 1000),
        #"Log10DedxMass": TH1F("Log10DedxMass", "Log10DedxMass", 10, 0, 5),
        "DeDx": TH1F("DeDx", "DeDx", 100, 0, 10),
        "DeDxCorrected": TH1F("DeDxCorrected", "DeDxCorrected", 100, 0, 10),
        #"n_tags": TH1F("n_tags", "n_tags", 3, 0, 3),
        "region": TH1F("region", "region", 88, 1, 89),
        "sidebandregion": TH1F("sidebandregion", "sidebandregion", 88, 1, 89),
             }

    output_variables = histos.keys()

    # add histograms for the regions
    for variable in histos.keys():
        for category in ["short", "long", "multi"]:
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
        
        if (iEv+1) % 10000 == 0:
            print "Processing event %s / %s" % (iEv + 1, nev_tree)

        if is_data:
            weight = 1.0
        else:
            weight = 1.0 * event.CrossSection * event.puWeight / nev

        # loop over all event selections:
        for event_selection in event_selections:

            if not eval(event_selections[event_selection]): continue

            tagged_tracks = {}
            tagged_tracks["SR_short"] = []
            tagged_tracks["CR_short"] = []
            tagged_tracks["SR_long"] = []
            tagged_tracks["CR_long"] = []

            regions = {}
            regions["region_signal"] = 0
            regions["region_control"] = 0
            regions["sidebandregion_signal"] = 0
            regions["sidebandregion_control"] = 0

            # loop over all tracks and tag all disappearing tracks:
            for i, track in enumerate(event.tracks_pt):

                if eval(CR_short) or eval(CR_short) or eval(SR_long) or eval(CR_long):

                    is_prompt_track = event.tracks_prompt_electron[i]==1 or event.tracks_prompt_muon[i]==1 or event.tracks_prompt_tau[i]==1 or event.tracks_prompt_tau_leadtrk[i]==1
                    is_fake_track = event.tracks_fake[i]==1
                    dedx = event.tracks_deDxHarmonic2pixel[i]
                    dedx_corrected = correct_dedx_intercalibration(dedx, input_filenames[0])
                    log10dedxmass = TMath.Log10(TMath.Sqrt((dedx-3.01) * pow(event.tracks_pt[i] * TMath.CosH(event.tracks_eta[i]),2)/1.74))
                    log10dedxmass_corrected = TMath.Log10(TMath.Sqrt((dedx_corrected-3.01) * pow(event.tracks_pt[i] * TMath.CosH(event.tracks_eta[i]),2)/1.74))
                    
                    track_info = {
                                   "is_pixel_track": event.tracks_is_pixel_track[i],
                                   "is_prompt_track": is_prompt_track,
                                   "is_fake_track": is_fake_track,
                                   "dedx": dedx,
                                   "dedx_corrected": dedx_corrected,
                                   "log10dedxmass": log10dedxmass,
                                   "log10dedxmass_corrected": log10dedxmass_corrected,
                                 }
                    
                    if eval(SR_short):
                        tagged_tracks["SR_short"].append(track_info)
                    if eval(CR_short):
                        tagged_tracks["CR_short"].append(track_info)
                    if eval(SR_long):
                        tagged_tracks["SR_long"].append(track_info)
                    if eval(CR_long):
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
                regions["region_signal"] = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT["signal"], is_pixel_track, dedx, event.n_goodelectrons, event.n_goodmuons, input_filenames[0])
                regions["sidebandregion_signal"] = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT["signal"], is_pixel_track, dedx, event.n_goodelectrons, event.n_goodmuons, input_filenames[0], sideband = True)
            if n_DT["control"]>0:
                is_pixel_track = list(tagged_tracks["CR_short"] + tagged_tracks["CR_long"])[0]["is_pixel_track"]
                dedx = list(tagged_tracks["CR_short"] + tagged_tracks["CR_long"])[0]["dedx"]
                regions["region_control"] = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT["control"], is_pixel_track, dedx, event.n_goodelectrons, event.n_goodmuons, input_filenames[0])
                regions["sidebandregion_control"] = get_signal_region(event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, n_DT["control"], is_pixel_track, dedx, event.n_goodelectrons, event.n_goodmuons, input_filenames[0], sideband = True)
                        
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

                # any other region than sideband should fall in a region bin
                #if variable != "sidebandregion":
                #    if regions["region_signal"] + regions["region_control"] == 0:
                #        continue

                if variable == "leptonMT" and "MT" not in event_selection:
                    continue

                for current_region in ["signal", "control"]:
                    
                    current_region_short = current_region.replace("signal", "SR").replace("control", "CR")
                
                    if n_DT[current_region] == 1:
                        for category in ["short", "long"]:
                            if len(tagged_tracks[current_region_short + "_" + category]) == 1:                                
                                if variable == "region":
                                    value = regions["region_%s" % current_region]
                                elif variable == "sidebandregion":
                                    value = regions["sidebandregion_%s" % current_region]
                                elif variable == "DeDx":
                                    value = tagged_tracks[current_region_short + "_" + category][0]["dedx"]
                                elif variable == "DeDxCorrected":
                                    value = tagged_tracks[current_region_short + "_" + category][0]["dedx_corrected"]
                                elif variable == "leptonMT":
                                    value = event.leptons_mtw[0]
                                else:
                                    value = eval("event.%s" % variable)
                                                                
                                fill_histogram(histos[variable + "_" + current_region + "_" + category + "_" + event_selection], variable, value, weight)
                                if tagged_tracks[current_region_short + "_" + category][0]["is_fake_track"] == 1:
                                    fill_histogram(histos[variable + "_" + current_region + "fake_" + category + "_" + event_selection], variable, value, weight)
                                if tagged_tracks[current_region_short + "_" + category][0]["is_prompt_track"] == 1:
                                    fill_histogram(histos[variable + "_" + current_region + "prompt_" + category + "_" + event_selection], variable, value, weight)

                    elif n_DT[current_region] >= 2:
                        
                        if variable == "region":
                            value = regions["region_%s" % current_region]
                        elif variable == "sidebandregion":
                            value = regions["sidebandregion_%s" % current_region]
                        elif variable == "DeDx":
                            value = list(tagged_tracks[current_region_short + "_short"] + tagged_tracks[current_region_short + "_long"])[0]["dedx"]
                        elif variable == "DeDxCorrected":
                            value = list(tagged_tracks[current_region_short + "_short"] + tagged_tracks[current_region_short + "_long"])[0]["dedx_corrected"]
                        elif variable == "leptonMT":
                            value = event.leptons_mtw[0]
                        else:
                            value = eval("event.%s" % variable)

                        fill_histogram(histos[variable + "_" + current_region + "_multi_" + event_selection], variable, value, weight)
                        
                        # check if all tagged tracks are fake or prompt tracks:
                        all_tracks_are_fake = True
                        all_tracks_are_prompt = True
                        
                        for track in list(tagged_tracks[current_region_short + "_short"] + tagged_tracks[current_region_short + "_long"]):
                            if track["is_prompt_track"] != 1:
                                all_tracks_are_prompt = False
                            if track["is_fake_track"] != 1:
                                all_tracks_are_fake = False
                                
                        if all_tracks_are_prompt:
                            fill_histogram(histos[variable + "_" + current_region + "prompt_multi_" + event_selection], variable, value, weight)
                        if all_tracks_are_fake:
                            fill_histogram(histos[variable + "_" + current_region + "fake_multi_" + event_selection], variable, value, weight)
                            
                         
    if event_start>0:
        output_file = output_file.replace(".root", "_%s.root" % event_start)

    fout = TFile(output_file, "recreate")
    for var in histos:
        #if histos[var].GetEntries()>0:
        #    print var, histos[var].GetEntries()
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
        os.system("hadd -f %s/prediction_Summer16.root %s/Summer16*.root" % (options.prediction_folder, options.prediction_folder))
        os.system("hadd -f %s/prediction_Run2016.root %s/Run2016*MET*.root %s/Run2016*SingleMuon*.root %s/Run2016*SingleElectron*.root" % (options.prediction_folder, options.prediction_folder, options.prediction_folder, options.prediction_folder))
        
        for period in ["B", "C", "D", "E", "F", "G", "H"]:
            os.system("hadd -f %s/prediction_Run2016%s.root %s/Run2016%s*MET*.root %s/Run2016%s*SingleMuon*.root %s/Run2016%s*SingleElectron*.root" % (options.prediction_folder, period, options.prediction_folder, period, options.prediction_folder, period, options.prediction_folder, period))
            os.system("hadd -f %s/prediction_Run2016%s_MET.root %s/Run2016%s*MET*.root" % (options.prediction_folder, period, options.prediction_folder, period))                    
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
            if "Summer16.TT_Tune" in input_file: use_file = True
            if "Run2016" in input_file and "MET" in input_file: use_file = True
            if "Run2016" in input_file and "SingleMuon" in input_file: use_file = True
            if "Run2016" in input_file and "SingleElectron" in input_file: use_file = True
            if not use_file: continue
            
            # get nev:
            tree = TChain("Events")
            tree.Add(input_file)
            nev = tree.GetEntries()
            
            nev_per_interval = int(nev/int(options.jobs_per_file))
            
            for i in range(int(options.jobs_per_file)):
                
                event_start = i * nev_per_interval
                
                commands.append("./nonprompt.py --input %s --output %s/%s --nev %s --fakerate_file %s --event_start %s --unweighted %s" % (input_file, options.prediction_folder, input_file.split("/")[-1], nev_per_interval, options.fakerate_file, event_start, options.unweighted))
        
        runParallel(commands, options.runmode, condorDir = "nonprompt.condor", use_more_mem=False, use_more_time=False, confirm=not options.start)

    # otherwise run locally:
    else:
        options.inputfiles = options.inputfiles.split(",")

        event_loop(options.inputfiles,
             options.outputfiles,
             nevents = int(options.nev),
             fakerate_file = options.fakerate_file,
             event_start = int(options.event_start),
            )
