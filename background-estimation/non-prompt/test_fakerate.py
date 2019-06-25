#!/bin/env python
from __future__ import division
from ROOT import *
from optparse import OptionParser
import math, os, glob
from GridEngineTools import runParallel
import time
import collections

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


def get_signal_region(MHT, NJets, n_btags, MinDeltaPhiMhtJets, n_DT, is_pixel_track):
  
    is_tracker_track = not is_pixel_track

    binnumbers = collections.OrderedDict()
    #           'Ht',             'Mht',                'NJets',            'BTags',            'NTags',            'NPix',             'NPixStrips',       'MinDPhiMhtJets'
    binnumbers[((0,float("inf")), (250,400),            (1,1),              (0,float("inf")),   (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 1
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (0,0),              (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 2
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (1,5),              (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 3
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (0,0),              (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 4
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (1,float("inf")),   (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 5
    binnumbers[((0,float("inf")), (400,700),            (1,1),              (0,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 6
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 7
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (1,5),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 8
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 9
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (1,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 10
    binnumbers[((0,float("inf")), (700,float("inf")),   (1,1),              (0,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 11
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 12
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (1,5),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 13
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 14
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (1,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 15
    binnumbers[((0,float("inf")), (250,400),            (1,1),              (0,float("inf")),   (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 16
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (0,0),              (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 17
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (1,5),              (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 18
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (0,0),              (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 19
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (1,float("inf")),   (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 20
    binnumbers[((0,float("inf")), (400,700),            (1,1),              (0,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 21
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 22
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (1,5),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 23
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 24
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (1,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 25
    binnumbers[((0,float("inf")), (700,float("inf")),   (1,1),              (0,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 26
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 27
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (1,5),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 28
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 29
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (1,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 30
    binnumbers[((0,float("inf")), (250,400),            (1,float("inf")),   (0,float("inf")),   (2,float("inf")),   (0,float("inf")),   (0,float("inf")),   (0.0,float("inf")))] = 31
    binnumbers[((0,float("inf")), (400,float("inf")),   (1,float("inf")),   (0,float("inf")),   (2,float("inf")),   (0,float("inf")),   (0,float("inf")),   (0.0,float("inf")))] = 32

    region = 0
    for binkey in binnumbers:
        if MHT >= binkey[1][0] and MHT <= binkey[1][1] and \
           NJets >= binkey[2][0] and NJets <= binkey[2][1] and \
           n_btags >= binkey[3][0] and n_btags <= binkey[3][1] and \
           n_DT >= binkey[4][0] and n_DT <= binkey[4][1] and \
           is_pixel_track >= binkey[5][0] and is_pixel_track <= binkey[5][1] and \
           is_tracker_track >= binkey[6][0] and is_tracker_track <= binkey[6][1] and \
           MinDeltaPhiMhtJets >= binkey[7][0] and MinDeltaPhiMhtJets <= binkey[7][1]:
            region = binnumbers[binkey]
            break

    return region
        

def main(input_filenames, output_file, fakerate_file = "fakerate.root", nevents = -1, treename = "Events"):

    # load tree
    tree = TChain(treename)
    for iFile in input_filenames:
        tree.Add(iFile)
   
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
    
    # output histograms
    histos = {}
    histos["HT"] = TH1F("HT", "HT", 10, 0, 1000)
    histos["MHT"] = TH1F("MHT", "MHT", 10, 0, 1000)
    histos["n_jets"] = TH1F("n_jets", "n_jets", 101, 0, 100)
    histos["MinDeltaPhiMhtJets"] = TH1F("MinDeltaPhiMhtJets", "MinDeltaPhiMhtJets", 20, 0, 1)
    histos["n_btags"] = TH1F("n_btags", "n_btags", 21, 0, 20)
    histos["region_long"] = TH1F("region_long", "region_long", 15, 1, 16)
    histos["region_short"] = TH1F("region_short", "region_short", 15, 16, 31)
    histos["region_multi"] = TH1F("region_multi", "region_multi", 2, 31, 33)

    output_variables = histos.keys()

    # load fake rate histograms:
    fakerate_regions = []
    for i_region in ["dilepton", "qcd", "qcd_sideband", "qcd_highMHT"]:
    #for i_region in ["dilepton"]:
        for i_cond in ["tight", "loose1", "loose2", "crosscheck"]:
            for i_cat in ["_short", "_long"]:
                fakerate_regions.append(i_region + "_" + i_cond + i_cat)

    #fakerate_variables = ["n_allvertices"]
    fakerate_variables = ["HT", "n_allvertices", "HT:n_allvertices"]
    
    # load fakerate maps:
    tfile_fakerate = TFile(fakerate_file, "open")

    # get all fakerate histograms:
    h_fakerates = {}
    for region in fakerate_regions:
        for variable in fakerate_variables:                   
            hist_name = region + "/" + data_period + "/fakerate_" + variable.replace(":", "_")
            
            hist_name = hist_name.replace("//", "/")
            h_fakerates[hist_name] = tfile_fakerate.Get(hist_name)

    # add more histograms
    more_hists = []

    for variable in output_variables:               
        for fakerate_variable in fakerate_variables:

            # add histogram if not there yet
            for category in ["short", "long"]:

                for label in ["tagged", "prediction"]:
                    for fr_region in fakerate_regions:  
                        h_suffix = "_%s_%s_%s" % (fr_region, fakerate_variable.replace(":", "_"), label)
                        histos[variable + h_suffix] = histos[variable].Clone()
                        histos[variable + h_suffix].SetName(variable + h_suffix)

                for tag in ["tight", "loose1", "loose2", "crosscheck"]:
                    for itype in ["fakebg", "promptbg", "control", "tagged"]:
                        h_suffix =  "_%s_%s_%s" % (tag, itype, category)
                        histos[variable + h_suffix] = histos[variable].Clone()
                        histos[variable + h_suffix].SetName(variable + h_suffix)
                        more_hists.append(h_suffix[1:])

    if nevents > 0:
        nev = nevents
    else:
        nev = tree.GetEntries()

    print "Looping over %s events" % nev
    start_time = time.time()

    for iEv, event in enumerate(tree):

        if nevents > 0 and iEv > nevents: break
        interval = 10000
        if (iEv+1) % interval == 0:
            PercentProcessed = int( 40 * iEv / nev )
            line = "[" + PercentProcessed * "*" + (40-PercentProcessed) * " " + "]\t" + "Processing event %s / %s" % (iEv + 1, nev)
            elapsed_time = int(time.time() - start_time)
            line += ", est. %s minutes left" % int(elapsed_time / (iEv/interval) * (nev/interval) / 60.0)
            print line

        weight = 1.0 * event.CrossSection * event.puWeight / nev

        #is_control_region = event.passesUniversalSelection==1 and event.MHT>250 and event.MinDeltaPhiMhtJets>0.3 and event.n_jets>0 and event.n_leptons==0 and event.n_genLeptons==0
        is_control_region = event.passesUniversalSelection==1 and event.MHT>250 and event.MinDeltaPhiMhtJets>0.3 and event.n_jets>0 and event.n_leptons==0
        
        if is_control_region:

            event.region_short = get_signal_region(event.MHT, event.n_jets, event.n_btags, event.MinDeltaPhiMhtJets, 1, True)
            event.region_long = get_signal_region(event.MHT, event.n_jets, event.n_btags, event.MinDeltaPhiMhtJets, 1, False)
            event.region_multi = get_signal_region(event.MHT, event.n_jets, event.n_btags, event.MinDeltaPhiMhtJets, 2, True)

            ###############################
            # we're in the control region #
            ###############################              

            for variable in output_variables:

                value = eval("event.%s" % variable)

                ###################################################
                # for each tag, check if in signal/control region #
                ###################################################

                flags = {}
                for label in more_hists:
                    flags[label] = False

                def set_flag(label, flags, event, itrack):
                    if event.tracks_is_pixel_track[itrack]==1:
                        flags[label + "_short"] = True
                    elif event.tracks_is_pixel_track[itrack]==0:
                        flags[label + "_long"] = True
                    return flags

                # loop over tracks:
                for i in range(len(event.tracks)):

                    #is_prompt_track = event.tracks_prompt_electron[i]==1 or event.tracks_prompt_muon[i]==1 or event.tracks_prompt_tau[i]==1 or event.tracks_prompt_tau_leadtrk[i]==1
                    is_prompt_track = event.tracks_prompt_electron[i]==1 or event.tracks_prompt_muon[i]==1
                    is_fake_track = not is_prompt_track

                    # tight tag
                    if event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt[i]>0.1:
                        flags = set_flag("tight_tagged", flags, event, i)
                        if is_fake_track:
                            flags = set_flag("tight_fakebg", flags, event, i)
                        if is_prompt_track:
                            flags = set_flag("tight_promptbg", flags, event, i)
                    flags["tight_control_short"] = is_control_region
                    if event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt[i]>0.25:
                        flags = set_flag("tight_tagged", flags, event, i)
                        if is_fake_track:
                            flags = set_flag("tight_fakebg", flags, event, i)
                        if is_prompt_track:
                            flags = set_flag("tight_promptbg", flags, event, i)
                    flags["tight_control_long"] = is_control_region

                    # crosscheck tight tag
                    if event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt[i]>0.1 and is_fake_track:
                        flags = set_flag("crosscheck_tagged", flags, event, i)
                        if is_fake_track:
                            flags = set_flag("crosscheck_fakebg", flags, event, i)
                        if is_prompt_track:
                            flags = set_flag("crosscheck_promptbg", flags, event, i)
                    flags["crosscheck_control_short"] = is_control_region
                    if event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt[i]>0.25 and is_fake_track:
                        flags = set_flag("crosscheck_tagged", flags, event, i)
                        if is_fake_track:
                            flags = set_flag("crosscheck_fakebg", flags, event, i)
                        if is_prompt_track:
                            flags = set_flag("crosscheck_promptbg", flags, event, i)
                    flags["crosscheck_control_long"] = is_control_region

                    # loose1 tag
                    if event.tracks_mva_bdt_loose[i]>0.1 and event.tracks_dxyVtx[i]<=0.01:
                        flags = set_flag("loose1_tagged", flags, event, i)
                        if is_fake_track:
                            flags = set_flag("loose1_fakebg", flags, event, i)
                        if is_prompt_track:
                            flags = set_flag("loose1_promptbg", flags, event, i)
                    if event.tracks_mva_bdt_loose[i]>0.1 and event.tracks_dxyVtx[i]>0.01:
                            flags = set_flag("loose1_control", flags, event, i)

                    # loose2 tag
                    if event.tracks_mva_bdt_loose[i]>0.1 and event.tracks_dxyVtx[i]<=0.02:
                        flags = set_flag("loose2_tagged", flags, event, i)
                        if is_fake_track:
                            flags = set_flag("loose2_fakebg", flags, event, i)
                        if is_prompt_track:
                            flags = set_flag("loose2_promptbg", flags, event, i)
                    if event.tracks_mva_bdt_loose[i]>0.1 and event.tracks_dxyVtx[i]>0.05:
                            flags = set_flag("loose2_control", flags, event, i)

                for label in flags:
                    if flags[label]:
                        if variable+"_"+label in histos:
                            histos[variable + "_" + label].Fill(value, weight)

                ###################################################
                # get fake rate from histogram/map for each event #
                ###################################################

                for fakerate_variable in fakerate_variables:

                    if ":" in fakerate_variable:
                        xvalue = eval("event.%s" % fakerate_variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[1])
                        yvalue = eval("event.%s" % fakerate_variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[0])
                    else:                
                        xvalue = eval("event.%s" % fakerate_variable)
                    
                    for fr_region in fakerate_regions:              

                        hist_name = fr_region + "/" + data_period + "/fakerate_" + fakerate_variable.replace(":", "_")

                        #FIXME
                        if "dilepton" in hist_name and "interpolated" in hist_name:
                            continue
                            hist_name = hist_name.replace("HT", "HT_cleaned")

                        if ":" in fakerate_variable:
                            fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue, yval = yvalue)
                        else:                
                            fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue)
                        
                        if "short" in hist_name:
                            if ("tight" in hist_name and flags["tight_control_short"]) or ("loose1" in hist_name and flags["loose1_control_short"]) or ("loose2" in hist_name and flags["loose2_control_short"]) or ("crosscheck" in hist_name and flags["crosscheck_control_short"]):
                                histos[variable + "_" + fr_region + "_" + fakerate_variable.replace(":", "_") + "_prediction"].Fill(value, weight * fakerate)

                        elif "long" in hist_name:
                            if ("tight" in hist_name and flags["tight_control_long"]) or ("loose1" in hist_name and flags["loose1_control_long"]) or ("loose2" in hist_name and flags["loose2_control_long"]) or ("crosscheck" in hist_name and flags["crosscheck_control_short"]):
                                histos[variable + "_" + fr_region + "_" + fakerate_variable.replace(":", "_") + "_prediction"].Fill(value, weight * fakerate)

        else:
            for variable in output_variables:

                if "region" in variable: continue

                value = eval("event.%s" % variable)
                histos[variable].Fill(eval("event.%s" % variable), weight)


    fout = TFile(output_file, "recreate")
    for var in histos:
        histos[var].Write()

    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles")
    parser.add_option("--output", dest = "outputfiles")
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--fakerate_file", dest = "fakerate_file", default = "fakerate.root")
    parser.add_option("--runmode", dest="runmode", default="grid")
    (options, args) = parser.parse_args()
       
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
    
    # run parallel if input is a folder:
    if options.inputfiles[-1] == "/":
        print "Got input folder, running in batch mode (%s)!" % options.runmode

        #output_folder = options.inputfiles[:-1] + "_prediction"
        output_folder = options.inputfiles[:-1] + "_prediction_crosscheck_6"
        
        input_files = glob.glob(options.inputfiles + "/*.root")
        os.system("mkdir -p %s" % output_folder)
        commands = []

        for input_file in input_files:
            if "QCD_HT" in input_file or "ZJetsToNuNu_HT" in input_file:
                commands.append("./test_fakerate.py --input %s --output %s/%s --nev %s --fakerate_file %s" % (input_file, output_folder, input_file.split("/")[-1], options.nev, options.fakerate_file))
    
        raw_input("start %s jobs?" % len(commands))
        runParallel(commands, options.runmode, condorDir = "test_fakerate_condor", dontCheckOnJobs=False, use_more_mem=True, use_more_time=True)

    # otherwise run locally:
    else:
        options.inputfiles = options.inputfiles.split(",")

        main(options.inputfiles,
             options.outputfiles,
             nevents = int(options.nev),
             fakerate_file = options.fakerate_file,
            )
