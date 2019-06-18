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

    # add prediction
    for var in histos.keys():
        histos[var + "_control_short"] = histos[var].Clone()
        histos[var + "_control_short"].SetName(var + "_control_short")
        histos[var + "_control_long"] = histos[var].Clone()
        histos[var + "_control_long"].SetName(var + "_control_long")
        histos[var + "_prediction_short"] = histos[var].Clone()
        histos[var + "_prediction_short"].SetName(var + "_prediction_short")
        histos[var + "_prediction_long"] = histos[var].Clone()
        histos[var + "_prediction_long"].SetName(var + "_prediction_long")
        histos[var + "_fakebg_short"] = histos[var].Clone()
        histos[var + "_fakebg_short"].SetName(var + "_fakebg_short")
        histos[var + "_fakebg_long"] = histos[var].Clone()
        histos[var + "_fakebg_long"].SetName(var + "_fakebg_long")
        histos[var + "_promptbg_short"] = histos[var].Clone()
        histos[var + "_promptbg_short"].SetName(var + "_promptbg_short")
        histos[var + "_promptbg_long"] = histos[var].Clone()
        histos[var + "_promptbg_long"].SetName(var + "_promptbg_long")

    # load fake rate histograms:
    fakerate_regions = []
    #for i_region in ["dilepton", "qcd", "qcd_sideband"]:
    for i_region in ["dilepton"]:
        for i_cond in ["tight", "loose1", "loose2", "loose3", "combined"]:
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
    
    nev = tree.GetEntries()
    print "Looping over %s events" % nev

    for iEv, event in enumerate(tree):

        if nevents > 0 and iEv > nevents: break
        if (iEv+1) % 1000 == 0:
            PercentProcessed = int( 20 * iEv / nev )
            line = "[" + PercentProcessed*"#" + (20-PercentProcessed)*" " + "]\t" + "Processing event %s / %s" % (iEv + 1, nev)
            print line
        
        if event.passesUniversalSelection==1 and event.MHT>250 and event.MinDeltaPhiMhtJets>0.3 and event.n_jets>0 and event.n_leptons==0:
            is_control_region = True
        else:
            is_control_region = False
    
        for var in histos:
            if "_" not in var:
                histos[var].Fill(eval("event.%s" % var))
        
        # if in control region, get fake rate:
        if is_control_region:
                
            for variable in fakerate_variables:
                
                if ":" in variable:
                    xvalue = eval("event.%s" % variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[1])
                    yvalue = eval("event.%s" % variable.replace("_interpolated", "").replace("_cleaned", "").split(":")[0])
                else:                
                    xvalue = eval("event.%s" % variable)
                
                for fr_region in fakerate_regions:
                    hist_name = fr_region + "/" + data_period + "/fakerate_" + variable.replace(":", "_")
                    if ":" in variable:
                        fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue, yval = yvalue)
                    else:                
                        fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue)
                
                    if "short" in hist_name:
                        histos[variable + "_control_short"].Fill(xvalue)
                        histos[variable + "_prediction_short"].Fill(xvalue, fakerate)
                    elif "long" in hist_name:
                        histos[variable + "_control_long"].Fill(xvalue)
                        histos[variable + "_prediction_long"].Fill(xvalue, fakerate)
        
                # check for DT:
                if event.tracks_is_pixel_track==1 and event.tracks_mva_bdt>0.1:
                    print "Found short DT"
                    if event.tracks_fake==1:
                        histos[variable + "_fakebg_short"].Fill(xvalue)
                    if event.tracks_prompt_electron==1 and event.tracks_prompt_muon==1:
                        histos[variable + "_promptbg_short"].Fill(xvalue)
                if event.tracks_is_pixel_track==0 and event.tracks_mva_bdt>0.25:
                    print "Found long DT"
                    if event.tracks_fake==1:
                        histos[variable + "_fakebg_long"].Fill(xvalue)
                    if event.tracks_prompt_electron==1 and event.tracks_prompt_muon==1:
                        histos[variable + "_promptbg_long"].Fill(xvalue)

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
