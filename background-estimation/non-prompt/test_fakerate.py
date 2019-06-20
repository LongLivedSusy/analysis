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
    output_variables = ["HT"]
    histos["HT"] = TH1F("HT", "HT", 10, 0, 1000)

    # load fake rate histograms:
    fakerate_regions = []
    #for i_region in ["dilepton", "qcd", "qcd_sideband"]:
    for i_region in ["dilepton"]:
        for i_cond in ["tight", "loose1", "loose2", "loose3", "combined"]:
            for i_cat in ["_short", "_long"]:
                fakerate_regions.append(i_region + "_" + i_cond + i_cat)

    #fakerate_variables = ["HT", "n_allvertices", "HT:n_allvertices", "HT:n_allvertices_interpolated"]
    fakerate_variables = ["HT:n_allvertices"]
        
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
    for variable in output_variables:               
        for fakerate_variable in fakerate_variables:

            # add histogram if not there yet
            for category in ["short", "long"]:
                for label in ["control", "prediction", "fakebg", "promptbg"]:
                    h_suffix = "_%s_%s_%s" % (fakerate_variable, label, category)
                    if variable + h_suffix not in histos:
                        histos[variable + h_suffix] = histos[variable].Clone()
                        histos[variable + h_suffix].SetName(variable + h_suffix)
    
    nev = tree.GetEntries()
    print "Looping over %s events" % nev

    for iEv, event in enumerate(tree):

        if nevents > 0 and iEv > nevents: break
        if (iEv+1) % 10000 == 0:
            PercentProcessed = int( 20 * iEv / nev )
            line = "[" + PercentProcessed*"#" + (20-PercentProcessed)*" " + "]\t" + "Processing event %s / %s" % (iEv + 1, nev)
            print line
        
        if event.passesUniversalSelection==1 and event.MHT>250 and event.MinDeltaPhiMhtJets>0.3 and event.n_jets>0 and event.n_leptons==0:

                ###############################
                # we're in the control region #
                ###############################

                weight = event.CrossSection * event.puWeight * lumi

                for variable in output_variables:
                    for fakerate_variable in fakerate_variables:

                        value = eval("event.%s" % variable)

                        if ":" in fakerate_variable:
                            xvalue = eval("event.%s" % fakerate_variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[1])
                            yvalue = eval("event.%s" % fakerate_variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[0])
                        else:                
                            xvalue = eval("event.%s" % fakerate_variable)
                        
                        for fr_region in fakerate_regions:              

                            hist_name = fr_region + "/" + data_period + "/fakerate_" + fakerate_variable.replace(":", "_")
                            if ":" in fakerate_variable:
                                fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue, yval = yvalue)
                            else:                
                                fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue)
                            
                            if "short" in hist_name:
                                histos[variable + "_" + fakerate_variable + "_control_short"].Fill(value, weight)
                                histos[variable + "_" + fakerate_variable + "_prediction_short"].Fill(value, weight * fakerate)
                            elif "long" in hist_name:
                                histos[variable + "_" + fakerate_variable + "_control_long"].Fill(value, weight)
                                histos[variable + "_" + fakerate_variable + "_prediction_long"].Fill(value, weight * fakerate)
                
                            fill_fakebg_short = False
                            fill_promptbg_short = False
                            fill_fakebg_long = False
                            fill_promptbg_long = False

                            # check for DT:
                            for i in range(len(event.tracks)):
                                if event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt[i]>0.1:
                                #if event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt_loose[i]>0:
                                    print "Found short DT"
                                    print "fakerate", fakerate
                                    if event.tracks_fake[i]==1:
                                        fill_fakebg_short = True
                                    if event.tracks_prompt_electron[i]==1 or event.tracks_prompt_muon[i]==1 or event.tracks_prompt_tau[i]==1:
                                        fill_promptbg_short = True
                                if event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt[i]>0.25:
                                #if event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt_loose[i]>0:
                                    print "Found long DT"
                                    print "fakerate", fakerate
                                    if event.tracks_fake[i]==1:
                                        fill_fakebg_long = True
                                    if event.tracks_prompt_electron[i]==1 or event.tracks_prompt_muon[i]==1 or event.tracks_prompt_tau[i]==1:
                                        fill_promptbg_long = True
                                        
                            if fill_fakebg_short: histos[variable + "_" + fakerate_variable + "_fakebg_short"].Fill(value, weight)
                            if fill_promptbg_short: histos[variable + "_" + fakerate_variable + "_promptbg_short"].Fill(value, weight)
                            if fill_fakebg_long: histos[variable + "_" + fakerate_variable + "_fakebg_long"].Fill(value, weight)
                            if fill_promptbg_long: histos[variable + "_" + fakerate_variable + "_promptbg_long"].Fill(value, weight)

        else:

            #####################
            # no cuts for event #
            #####################

            for variable in output_variables:
                histos[variable].Fill(eval("event.%s" % variable))


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
    
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    main(options.inputfiles,
         options.outputfiles,
         nevents = int(options.nev),
        )
