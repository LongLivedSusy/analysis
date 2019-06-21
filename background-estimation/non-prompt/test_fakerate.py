#!/bin/env python
from __future__ import division
from ROOT import *
from optparse import OptionParser
import math

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
        

def main(input_filenames, output_file, fakerate_file = "fakerate.root", nevents = -1, treename = "Events", lumi = 135):

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
    #histos["MHT"] = TH1F("MHT", "MHT", 10, 0, 1000)
    output_variables = histos.keys()

    # load fake rate histograms:
    fakerate_regions = []
    #for i_region in ["dilepton", "qcd", "qcd_sideband"]:
    for i_region in ["dilepton"]:
        #for i_cond in ["tight", "loose1", "loose2", "crosscheck"]:
        for i_cond in ["loose1"]:
            for i_cat in ["_short", "_long"]:
                fakerate_regions.append(i_region + "_" + i_cond + i_cat)

    #fakerate_variables = ["HT", "n_allvertices", "HT:n_allvertices", "HT:n_allvertices_interpolated"]
    fakerate_variables = ["HT"]
        
    # load fakerate maps:
    tfile_fakerate = TFile(fakerate_file, "open")

    # get all fakerate histograms:
    h_fakerates = {}
    for region in fakerate_regions:
        for variable in fakerate_variables:                   
            hist_name = region + "/" + data_period + "/fakerate_" + variable.replace(":", "_")
            
            hist_name = hist_name.replace("//", "/")
            try:
                h_fakerates[hist_name] = tfile_fakerate.Get(hist_name)
            except:
                print "Couldn't load", hist_name

    # add more histograms
    more_hists = []

    for variable in output_variables:               
        for fakerate_variable in fakerate_variables:

            # add histogram if not there yet
            for category in ["short", "long"]:

                for label in ["prediction"]:
                    for fr_region in fakerate_regions:  
                        h_suffix = "_%s_%s_%s" % (fr_region, fakerate_variable.replace(":", "_"), label)
                        histos[variable + h_suffix] = histos[variable].Clone()
                        histos[variable + h_suffix].SetName(variable + h_suffix)

                #for tag in ["tight", "loose1", "loose2", "crosscheck"]:
                for tag in ["loose1"]:
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

    for iEv, event in enumerate(tree):

        if nevents > 0 and iEv > nevents: break
        if (iEv+1) % 100000 == 0:
            PercentProcessed = int( 40 * iEv / nev )
            line = "[" + PercentProcessed * "*" + (40-PercentProcessed) * " " + "]\t" + "Processing event %s / %s" % (iEv + 1, nev)
            print line

        weight = event.CrossSection * event.puWeight * lumi
        
        is_control_region = event.passesUniversalSelection==1 and event.MHT>250 and event.MinDeltaPhiMhtJets>0.3 and event.n_jets>0 and event.n_leptons==0

        if is_control_region:

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

                flags["tight_control_short"] = is_control_region
                flags["tight_control_long"] = is_control_region

                # loop over tracks:
                for i in range(len(event.tracks)):

                    is_fake_track = event.tracks_fake[i]==1
                    #is_prompt_track = event.tracks_prompt_electron[i]==1 or event.tracks_prompt_muon[i]==1 or event.tracks_prompt_tau[i]==1
                    is_prompt_track = not is_fake_track

                    if event.tracks_is_pixel_track[i]==1:
                        if event.tracks_mva_bdt[i]>0.1:
                            flags["tight_tagged_short"] = True
                            if is_fake_track:
                                flags["tight_fakebg_short"] = True
                            if is_prompt_track:
                                flags["tight_promptbg_short"] = True
                        if event.tracks_mva_bdt_loose[i]>0 and event.tracks_dxyVtx[i]<=0.01:
                            flags["loose1_tagged_short"] = True
                            if is_fake_track:
                                flags["loose1_fakebg_short"] = True
                            if is_prompt_track:
                                flags["loose1_promptbg_short"] = True
                        if event.tracks_mva_bdt_loose[i]>0 and event.tracks_dxyVtx[i]>0.01:
                                flags["loose1_control_short"] = True
                    if event.tracks_is_pixel_track[i]==0:
                        if event.tracks_mva_bdt[i]>0.25:
                            flags["tight_tagged_long"] = True
                            if is_fake_track:
                                flags["tight_fakebg_long"] = True
                            if is_prompt_track:
                                flags["tight_promptbg_long"] = True
                        if event.tracks_mva_bdt_loose[i]>0:
                            flags["loose1_tagged_long"] = True
                            if is_fake_track:
                                flags["loose1_fakebg_long"] = True
                            if is_prompt_track:
                                flags["loose1_promptbg_long"] = True
                        if event.tracks_mva_bdt_loose[i]>0 and event.tracks_dxyVtx[i]>0.01:
                                flags["loose1_control_long"] = True

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
                        if "interpolated" in hist_name:
                            hist_name = hist_name.replace("HT", "HT_cleaned")

                        if ":" in fakerate_variable:
                            fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue, yval = yvalue)
                        else:                
                            fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue)
                        
                        if "short" in hist_name:

                            if ("tight" in hist_name and flags["tight_control_short"]) or ("loose1" in hist_name and flags["loose1_control_short"]) or ("loose2" in hist_name and flags["loose2_control_short"]):
                                histos[variable + "_" + fr_region + "_" + fakerate_variable.replace(":", "_") + "_prediction"].Fill(value, weight * fakerate)

                        elif "long" in hist_name:

                            if ("tight" in hist_name and flags["tight_control_long"]) or ("loose1" in hist_name and flags["loose1_control_long"]) or ("loose2" in hist_name and flags["loose2_control_long"]):
                                histos[variable + "_" + fr_region + "_" + fakerate_variable.replace(":", "_") + "_prediction"].Fill(value, weight * fakerate)

        else:
            for variable in output_variables:
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
    (options, args) = parser.parse_args()
    
    options.inputfiles = options.inputfiles.split(",")
    
    #gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    main(options.inputfiles,
         options.outputfiles,
         nevents = int(options.nev),
        )
