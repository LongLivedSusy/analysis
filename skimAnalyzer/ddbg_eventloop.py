#!/bin/env python
from __future__ import division
import __main__ as main
from ROOT import *
from optparse import OptionParser
import math, os, glob
import GridEngineTools
import re
import math
import shared_utils
import collections

def calculate_fakerate(rootfile, samples, variables, event_selections, path):
    
    os.system("rm " + rootfile)
    
    h_fakerates = {}
    for variable in variables:
        for run_period in samples:
            for event_selection in event_selections:
                for category in ["short", "long"]:
                    
                    tfile_merged = TFile(path + "/merged_%s.root" % run_period, "update")
                        
                    fakes_numerator = tfile_merged.Get(run_period + "_" + variable + "_" + event_selection + "_sr_" + category)
                    fakes_numerator.SetDirectory(0)
                    fakes_denominator = tfile_merged.Get(run_period + "_" + variable + "_" + event_selection + "_fakecr_" + category)
                    fakes_denominator.SetDirectory(0)
                    fakes_numeratorECSB = tfile_merged.Get(run_period + "_" + variable + "_" + event_selection + "_srECSB_" + category)
                    fakes_numeratorECSB.SetDirectory(0)
                    
                    tfile_merged.Close()

                    tfile_fakerate = TFile(rootfile, "update")
                    fakes_numerator.Write()
                    fakes_denominator.Write()
                    fakes_numeratorECSB.Write()

                    fakerate = fakes_numerator.Clone()
                    fakerate.SetName(fakerate.GetName().replace("_sr_", "_fakerate_"))
                    fakerate.Divide(fakes_denominator)
                    fakerate.Write()
                                        
                    fakerateECSB = fakes_numeratorECSB.Clone()
                    fakerateECSB.SetName(fakerateECSB.GetName().replace("_srECSB_", "_fakerateECSB_"))
                    fakerateECSB.Divide(fakes_denominator)
                    fakerateECSB.Write()

                    # close file
                    tfile_fakerate.Close()


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
        elif "SingleElectron" in filename and (n_goodmuons>0 or n_goodelectrons==0):
            return 0
        else:
            return region
    else:
        return region

 
def get_value(event, variable, i_track):
                        
    if ":" not in variable:
        if "tracks_" in variable:
            value = eval("event.%s[%s]" % (variable, i_track))
        else:
            value = eval("event.%s" % variable)
        return value
    
    else:
        if "tracks_" in variable.split(":")[0]:
            xvalue = eval("event.%s[%s]" % (variable.split(":")[0], i_track))
        else:
            xvalue = eval("event.%s" % variable.split(":")[0])
        if "tracks_" in variable.split(":")[1]:
            yvalue = eval("event.%s[%s]" % (variable.split(":")[1], i_track))
        else:
            yvalue = eval("event.%s" % variable.split(":")[1])
        return (xvalue, yvalue)


def fill_histogram(variable, value, histograms, event_selection, data_period, zone, weight, scaling):
    h_name = data_period + "_" + variable + "_" + event_selection + "_" + zone
    if ":" not in variable:
        histograms[h_name].Fill(value, weight*scaling)    
    else:
        histograms[h_name].Fill(value[0], yvalue[1], weight*scaling)
    

def event_loop(input_filenames, output_file, tags, variables, binnings, event_selections, zones, fakerate_filename, mode, nevents=-1, treename="Events", event_start=0, check_overwrite=False):

    # check if output file exists:
    if check_overwrite and os.path.exists(output_file):
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
    for tree_file in input_filenames:
        fin = TFile(tree_file)
        fin.Get("nev")
        fin.Get(treename)
        h_nev = fin.Get("nev")
        nev += int(h_nev.GetBinContent(1))
        fin.Close()

    tree = TChain(treename)       
    for i, tree_file in enumerate(input_filenames):
        tree.Add(tree_file)
        
    # construct all histograms:
    histograms = {}
    for variable in variables:
        for event_selection in event_selections:
            for zone in zones:
                if "srgen" in zone and is_data: continue
                h_name = data_period + "_" + variable + "_" + event_selection + "_" + zone
                
                if ":" not in variable:
                    histograms[h_name] = TH1F(h_name, h_name, binnings[mode][variable][0], binnings[mode][variable][1], binnings[mode][variable][2])
                else:
                    histograms[h_name] = TH2F(h_name, h_name, binnings[mode][variable][0], binnings[mode][variable][1], binnings[mode][variable][2], binnings[mode][variable][3], binnings[mode][variable][4], binnings[mode][variable][5])
                    
    
    # convert ROOT cutstrings to python statements:
    event_selections_converted = {}
    for event_selection in event_selections:
        event_selections_converted[event_selection] = parse_root_cutstring(event_selections[event_selection], tracks_increment_variable = "i_track")

    event_selections_converted_notracks = {}
    for event_selection in event_selections_converted:
        
        if event_selection == "Baseline":
            
            event_selections_converted_notracks[event_selection] = "(event.n_goodleptons==0 or event.leadinglepton_mt>90)"
        
        else:
        
            cutstring = event_selections_converted[event_selection]
            
            # remove tracks variables:
            cutstring_parts = cutstring.split()
            new_cutstring = ""
            for cutstring_part in cutstring_parts:
                if "tracks_" not in cutstring_part:
                    new_cutstring += cutstring_part + " "
            for i in range(10):
                new_cutstring = new_cutstring.replace("and and", "and")
            
            if new_cutstring.split()[-1] == "and":
                new_cutstring = " ".join(new_cutstring.split()[:-1])
            
            event_selections_converted_notracks[event_selection] = new_cutstring

    zones_converted = {}
    for zone in zones:
        zones_converted[zone] = parse_root_cutstring(zones[zone][0], tracks_increment_variable = "i_track")

    # Get fakerate maps:
    if fakerate_filename:
        h_fakerate = {}
        tfile_fakerate = TFile(fakerate_filename, "open")
        for zone in zones:
            h_label = zones[zone][1]
            if h_label != "":
                h_fakerate[h_label] = tfile_fakerate.Get(data_period + "_" + h_label)
                h_fakerate[h_label].SetDirectory(0)
        tfile_fakerate.Close()

    # main event loop:
    nev_tree = tree.GetEntries()
    for iEv, event in enumerate(tree):

        if iEv < int(event_start): continue
        if int(nevents) > 0 and iEv > int(nevents) + int(event_start): break
        
        if (iEv+1) % 10000 == 0:
            print "%s: %s/%s" % (input_filenames[0].split("/")[-1], iEv + 1, nev_tree)

        # check triggers:
        if is_data:
            if "MET" in first_filename:
                if event.triggered_met!=1: continue
            elif "SingleElectron" in first_filename:
                if event.triggered_singleelectron!=1: continue
            elif "SingleMuon" in first_filename:
                if event.triggered_singlemuon!=1: continue
            elif "JetHT" in first_filename:
                if event.triggered_ht!=1: continue
            else:
                print "no trigger defined!"
                quit()

        weight = 1.0
        if not is_data:
            weight = 1.0 * event.CrossSection * event.puWeight / nev

        # get fakerates for event:
        fakerates = {}
        if fakerate_filename:
            for label in h_fakerate:
                fakerate_variable = label.split("_")[0]
                if ":" in fakerate_variable:
                    if "HT:n_allvertices" in label:
                        xvalue = eval("event.HT")
                        yvalue = eval("event.n_allvertices")
                    else:
                        xvalue = eval("event.%s" % fakerate_variable.split(":")[0])
                        yvalue = eval("event.%s" % fakerate_variable.split(":")[1])
                    fakerates[label] = getBinContent_with_overflow(h_fakerate[label], xvalue, yval = yvalue)
                else:
                    xvalue = eval("event.%s" % fakerate_variable)
                    fakerates[label] = getBinContent_with_overflow(h_fakerate[label], xvalue)        
        
        # loop over all event selections:
        for event_selection in event_selections:
            for zone in zones:
                
                if "gen" in zone and is_data:
                    continue

                # this is to speed things up       
                if not eval(event_selections_converted_notracks[event_selection]):
                    continue
                                        
                scaling_by_hlabel = zones[zone][1]
                if scaling_by_hlabel == "":
                    scaling = 1.0
                else:                        
                    scaling = fakerates[scaling_by_hlabel]

                if len(zones[zone])>=3:
                    selected_nDT = zones[zone][2]
                else:
                    selected_nDT = "any"

                cuts_converted = []
                if "+++" not in zones_converted[zone]:
                    cut_converted = event_selections_converted[event_selection] + " and " + zones_converted[zone]
                    cuts_converted.append(cut_converted) 
                else:
                    cut_converted = event_selections_converted[event_selection] + " and " + zones_converted[zone].split("+++")[0]
                    cuts_converted.append(cut_converted) 
                    cut_converted = event_selections_converted[event_selection] + " and " + zones_converted[zone].split("+++")[1]
                    cuts_converted.append(cut_converted) 

                for variable in variables:
                        
                    if "region" in variable and event_selection != "Baseline":
                        continue
                        
                    values = []
                    track_index = -1
                    
                    for cut_converted in cuts_converted:
                        
                        if "tracks_" in cut_converted:
                            # cutstring with tracks in it
                            if "tracks_" in variable:
                                for i_track in xrange(len(event.tracks_ptError)):
                                    if eval(cut_converted):
                                        values.append(get_value(event, variable, i_track))
                                        track_index = i_track
                            else:
                                for i_track in xrange(len(event.tracks_ptError)):
                                    if eval(cut_converted):
                                        if variable == "regionCorrected":
                                            params = [event.HT, event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, 1, event.tracks_is_pixel_track[i_track], event.tracks_deDxHarmonic2pixelCorrected[i_track], event.n_goodelectrons, event.n_goodmuons, first_filename]
                                            values.append(params)
                                        else:
                                            values.append(get_value(event, variable, i_track))
                                        track_index = i_track
                                        break
                        
                        elif eval(cut_converted):
                            # cutstring without tracks in it                       
                            if "tracks_" in variable:
                                for i_track in xrange(len(event.tracks_ptError)):
                                    values.append(get_value(event, variable, i_track))
                                    track_index = i_track
                                    
                            else:
                                values.append(get_value(event, variable, -1))
                    
                    # count number of tagged tracks
                    n_tag = len(values)
                        
                    # fill histograms:
                    if variable == "regionCorrected" and len(values)>0:
                                                
                        if "sr" in zone:
                            
                            # get region number for signal region - depending on n(DT):
                            if n_tag==1:  
                                value = get_signal_region(*regionCorrected_list[0])
                            elif n_tag>1:
                                regionCorrected_list[0][5] = n_tag
                                value = get_signal_region(*regionCorrected_list[0])
                            fill_histogram(variable, value, histograms, event_selection, data_period, zone, weight, scaling)
                    
                        elif "cr" in zone:
                            
                            # fill CR region bins for n(DT)=1 and n(DT)>1:
                            regionCorrected_list[0][5] = 1
                            value = get_signal_region(*regionCorrected_list[0])
                            fill_histogram(variable, value, histograms, event_selection, data_period, zone, weight, scaling)
                            
                            regionCorrected_list[0][5] = 2
                            value = get_signal_region(*regionCorrected_list[0])
                            fill_histogram(variable, value, histograms, event_selection, data_period, zone, weight, scaling)
                            
                        elif "prediction" in zone:
                    
                            regionCorrected_list[0][5] = 1
                            value = get_signal_region(*regionCorrected_list[0])
                            fill_histogram(variable, value, histograms, event_selection, data_period, zone, weight, scaling)
                            
                            # apply fake rate twice to account for n(DT)>1:
                            regionCorrected_list[0][5] = 2
                            value = get_signal_region(*regionCorrected_list[0])
                            fill_histogram(variable, value, histograms, event_selection, data_period, zone, weight, scaling*scaling)
                            
                    else:
                        
                        if selected_nDT == "any":
                            for value in values:
                                fill_histogram(variable, value, histograms, event_selection, data_period, zone, weight, scaling)                    
                        elif selected_nDT == "single" and len(values) == 1:
                            fill_histogram(variable, values[0], histograms, event_selection, data_period, zone, weight, scaling)                    
                        elif selected_nDT == "multi" and len(values) > 1:
                            for value in values:
                                fill_histogram(variable, value, histograms, event_selection, data_period, zone, weight, scaling)                    
                            
                    
                            
    if event_start>0:
        output_file = output_file.replace(".root", "_%s.root" % event_start)
    
    fout = TFile(output_file, "recreate")
    for h_name in histograms:
        histograms[h_name].Write()
    fout.Close()
                 

def hadd_everything(samples, outputfolder):
    
    try:
        for data_period in samples:
            if "Run201" in data_period:
                os.system("hadd -f %s/merged_%s.root %s/%s" % (outputfolder, data_period, outputfolder, samples[data_period][0]))
            elif data_period == "Summer16":
                os.system("hadd -f %s/merged_Summer16.root %s/Summer16.*root" % (outputfolder, outputfolder))
    except Exception as e:
        print "hadd", str(e)
        quit()
    

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--inputfile", dest = "inputfile")
    parser.add_option("--outputfile", dest = "outputfile")
    parser.add_option("--mode", dest="mode")
    parser.add_option("--outputfolder", dest="outputfolder", default = "evlp96")
    parser.add_option("--fakeratefile", dest="fakeratefile", default = "fakerate.root")
    parser.add_option("--skimfolder", dest="skimfolder", default = "../ntupleanalyzer/skim_26_baseline")
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--tag", dest = "tag", default = 1)
    parser.add_option("--jobs_per_file", dest = "jobs_per_file", default = 1)
    parser.add_option("--event_start", dest = "event_start", default = 0)
    parser.add_option("--runmode", dest="runmode", default="multi")
    (options, args) = parser.parse_args()
    
    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
        
    baseline_selection = [
        #"abs(tracks_eta)<2.4",   
        "tracks_eta>-2.4",
        "tracks_eta<2.4",
        #"!(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566)",                              
        "tracks_highpurity==1",
        "tracks_ptErrOverPt2<10",
        "tracks_dzVtx<0.1",
        "tracks_trkRelIso<0.2",  
        "tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2",           
        "tracks_nMissingInnerHits==0",                                                     
        "tracks_nValidPixelHits>=3",    
        #"tracks_nMissingMiddleHits==0",
        #"tracks_chi2perNdof<2.88",
        #"tracks_pixelLayersWithMeasurement>=2",
        "tracks_passmask==1",
        "tracks_pass_reco_lepton==1",
        "tracks_passPFCandVeto==1",                                   
        #"tracks_passpionveto==1",
        #"tracks_passjetveto==1",
             ]
    
    baseline_long = "tracks_is_pixel_track==1 && " + " && ".join(baseline_selection)
    baseline_short = "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && " + " && ".join(baseline_selection)

    tags = collections.OrderedDict()

    if int(options.tag) == 1:
        print "using tag #1"
        tags["SR_short"] =  "tracks_is_pixel_track==1 && tracks_mva_loose>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
        tags["SR_long"] = "tracks_is_pixel_track==0 && tracks_mva_loose>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"
        tags["SREC_short"] = tags["SR_short"].replace("_chi2", "_chi2_sideband")
        tags["SREC_long"] = tags["SR_long"].replace("_chi2", "_chi2_sideband")
        tags["CR_short"] = "tracks_is_pixel_track==1 && tracks_dxyVtx>0.02"
        tags["CR_long"] = "tracks_is_pixel_track==0 && tracks_dxyVtx>0.02"
        EDepMax = 10
        EDepSideBandMin = 13
        EDepSideBandMax = 27

    elif int(options.tag) == 2:
        print "using tag #2"
        tags["SR_short"] =  "tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>-0.05 && tracks_dxyVtx<0.02 && tracks_trkRelIso<0.01"
        tags["SR_long"] = "tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>-0.15 && tracks_dxyVtx<0.02 && tracks_trkRelIso<0.01"
        tags["SREC_short"] = tags["SR_short"].replace("_chi2", "_chi2_sideband")
        tags["SREC_long"] = tags["SR_long"].replace("_chi2", "_chi2_sideband")
        tags["CR_short"] = "tracks_is_pixel_track==1 && tracks_dxyVtx>0.02"
        tags["CR_long"] = "tracks_is_pixel_track==0 && tracks_dxyVtx>0.02"
        EDepMax = 15
        EDepSideBandMin = 17
        EDepSideBandMax = 35

    elif int(options.tag) == 3:
        print "using tag #3"
        tags["SR_short"] =  "tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
        tags["SR_long"] = "tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"
        tags["SREC_short"] = tags["SR_short"].replace("_chi2", "_chi2_sideband")
        tags["SREC_long"] = tags["SR_long"].replace("_chi2", "_chi2_sideband")
        tags["CR_short"] = "tracks_is_pixel_track==1 && tracks_dxyVtx>0.02"
        tags["CR_long"] = "tracks_is_pixel_track==0 && tracks_dxyVtx>0.02"
        EDepMax = 15
        EDepSideBandMin = 17
        EDepSideBandMax = 35

    elif int(options.tag) == 4:
        print "using tag #4"
        tags["SR_short"] =  "tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
        tags["SR_long"] = "tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"
        tags["SREC_short"] = tags["SR_short"].replace("_chi2", "_chi2_sideband")
        tags["SREC_long"] = tags["SR_long"].replace("_chi2", "_chi2_sideband")
        tags["CR_short"] = "tracks_is_pixel_track==1 && tracks_dxyVtx>0.02"
        tags["CR_long"] = "tracks_is_pixel_track==0 && tracks_dxyVtx>0.02"
        EDepMax = 10
        EDepSideBandMin = 13
        EDepSideBandMax = 27
    
    elif int(options.tag) == 5:
        print "using tag #5"
        tags["SR_short"] =  "tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
        tags["SR_long"] = "tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>(tracks_dxyVtx*(0.7/0.01) - 0.2) && tracks_trkRelIso<0.01"
        tags["SREC_short"] = tags["SR_short"].replace("_chi2", "_chi2_sideband")
        tags["SREC_long"] = tags["SR_long"].replace("_chi2", "_chi2_sideband")
        tags["CR_short"] = "tracks_is_pixel_track==1 && tracks_dxyVtx>0.02"
        tags["CR_long"] = "tracks_is_pixel_track==0 && tracks_dxyVtx>0.02"
        EDepMax = 15
        EDepSideBandMin = 17
        EDepSideBandMax = 35
    
    
    variables = {}
    variables["analysis"] = [
                              #"HT",
                              #"MHT",
                              #"n_goodjets",
                              #"n_btags",
                              "leadinglepton_mt",
                              "tracks_invmass",
                              "tracks_region",
                              #"tracks_is_pixel_track",
                              #"tracks_pt",
                              #"tracks_eta",
                              #"tracks_deDxHarmonic2pixelCorrected",
                              #"tracks_matchedCaloEnergy",
                              #"tracks_trkRelIso",
                              "regionCorrected",
                              #"regionCorrected_sideband",
                            ]
    variables["fakerate"] = [
                              #"tracks_pt",
                              #"tracks_is_pixel_track",
                              #"HT",
                              #"MHT",
                              #"n_goodjets",
                              #"n_allvertices",
                              #"n_btags",
                              "HT:n_allvertices",
                            ]
                
    binnings = {}
    binnings["analysis"] = {}
    binnings["analysis"]["LepMT"] = [8, 0, 160]
    binnings["analysis"]["leptons_mt"] = binnings["analysis"]["LepMT"]
    binnings["analysis"]["leadinglepton_mt"] = binnings["analysis"]["LepMT"]
    binnings["analysis"]["InvMass"] = [10, 0, 200]
    binnings["analysis"]["tracks_invmass"] = binnings["analysis"]["InvMass"]
    binnings["analysis"]["Ht"] = [5, 0, 1000]
    binnings["analysis"]["HT"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["Met"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["MET"] = binnings["analysis"]["Met"]
    binnings["analysis"]["Mht"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["MHT"] = binnings["analysis"]["Mht"]
    binnings["analysis"]["tracks_pt"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["leadinglepton_pt"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["leadinglepton_eta"] = [15, 0, 3]
    binnings["analysis"]["tracks_eta"] = [15, 0, 3]
    binnings["analysis"]["tracks_dxyVtx"] = [20, 0, 0.1]
    binnings["analysis"]["DeDxAverage"] = [7, 0, 7]
    binnings["analysis"]["tracks_massfromdeDxPixel"] = binnings["analysis"]["DeDxAverage"]
    binnings["analysis"]["DeDxAverageCorrected"] = binnings["analysis"]["DeDxAverage"]
    binnings["analysis"]["tracks_deDxHarmonic2pixel"] = binnings["analysis"]["DeDxAverage"]
    binnings["analysis"]["tracks_deDxHarmonic2pixelCorrected"] = binnings["analysis"]["DeDxAverage"]
    binnings["analysis"]["BinNumber"] = [ 88, 1, 89]
    binnings["analysis"]["region"] = binnings["analysis"]["BinNumber"]
    binnings["analysis"]["n_tags"] = [ 3, 0, 3]
    binnings["analysis"]["n_goodjets"] = [ 10, 0, 10]
    binnings["analysis"]["n_btags"] = binnings["analysis"]["n_goodjets"]
    binnings["analysis"]["n_goodelectrons"] = [ 5, 0, 5]
    binnings["analysis"]["n_goodmuons"] = [ 5, 0, 5]
    binnings["analysis"]["MinDeltaPhiMhtJets"] = [ 16, 0, 3.2]
    binnings["analysis"]["BTags"] = [ 4, 0, 4]
    binnings["analysis"]["tracks_is_pixel_track"] = [ 2, 0, 2]
    binnings["analysis"]["Track1MassFromDedx"] = [ 25, 0, 1000]
    binnings["analysis"]["Log10DedxMass"] = [10, 0, 5]
    binnings["analysis"]["regionCorrected"] = [54,1,55]
    binnings["analysis"]["regionCorrected_sideband"] = binnings["analysis"]["regionCorrected"]
    binnings["analysis"]["region"] = binnings["analysis"]["regionCorrected"]
    binnings["analysis"]["tracks_matchedCaloEnergy"] = [25, 0, 50]
    binnings["analysis"]["tracks_trkRelIso"] = [20, 0, 0.2]
    binnings["analysis"]["tracks_region"] = [54, 1, 55]

    binnings["fakerate"] = {}
    binnings["fakerate"]["tracks_pt"] = [20, 0, 1000]
    binnings["fakerate"]["tracks_is_pixel_track"] = [2, 0, 2]
    binnings["fakerate"]["HT"] = [5, 0, 2000]
    binnings["fakerate"]["MHT"] = [10, 0, 2000]
    binnings["fakerate"]["n_allvertices"] = [25, 0, 50]
    binnings["fakerate"]["n_goodjets"] = [20, 0, 20]
    binnings["fakerate"]["n_btags"] = [10, 0, 10]
    binnings["fakerate"]["MinDeltaPhiMhtJets"] = [100, 0, 5]
    binnings["fakerate"]["tracks_eta"] = [12, -3, 3]
    binnings["fakerate"]["tracks_phi"] = [16, -4, 4]
    binnings["fakerate"]["HT:n_allvertices"] = [3, 0, 2000, 3, 0, 50]
    
    dEdxSidebandLow = 1.6
    dEdxLow = 2.0
    dEdxMid = 4.0

    # construct all histograms:
    zones = collections.OrderedDict()
    for dedx in ["", "_MidHighDeDx"]:                    
        if dedx == "_SidebandDeDx":
            lower = dEdxSidebandLow; upper = dEdxLow
        elif dedx == "_MidDeDx":
            lower = dEdxLow; upper = dEdxMid
        elif dedx == "_MidHighDeDx":
            lower = dEdxLow; upper = 9999
        elif dedx == "_HighDeDx":
            lower = dEdxMid; upper = 9999
        elif dedx == "_MidHighDeDx":
            lower = dEdxLow; upper = 9999
        elif dedx == "":
            lower = 0; upper = 9999
                        
        for is_pixel_track, category in enumerate(["long", "short"]):

            # for prompt bg:
            if dedx != "":
                morecuts = " && tracks_is_pixel_track==%s && tracks_matchedCaloEnergy<%s && tracks_deDxHarmonic2pixelCorrected>%s && tracks_deDxHarmonic2pixelCorrected<%s" % (is_pixel_track, EDepMax, lower, upper)
                morecutsEC = " && tracks_is_pixel_track==%s && tracks_deDxHarmonic2pixelCorrected>%s && tracks_deDxHarmonic2pixelCorrected<%s" % (is_pixel_track, lower, upper)
            else:
                morecuts = " && tracks_is_pixel_track==%s && tracks_matchedCaloEnergy<%s" % (is_pixel_track, EDepMax)
                morecutsEC = " && tracks_is_pixel_track==%s" % (is_pixel_track)
            
            # zones[label] = [cut, weight, nDT]
            zones["srEC%s_%s_single" % (dedx, category)] = [" && %s %s && tracks_matchedCaloEnergy<%s" % (tags["SREC_" + category], morecutsEC, EDepMax), "", "single"]
            zones["srECSB%s_%s_single" % (dedx, category)] = [" && %s %s && tracks_matchedCaloEnergy>%s && tracks_matchedCaloEnergy<%s" % (tags["SREC_" + category], morecutsEC, EDepSideBandMin, EDepSideBandMax), "", "single"]
            zones["srEC%s_%s_multi" % (dedx, category)] = [" && %s %s && tracks_matchedCaloEnergy<%s" % (tags["SREC_" + category], morecutsEC, EDepMax), "", "multi"]
            zones["srECSB%s_%s_multi" % (dedx, category)] = [" && %s %s && tracks_matchedCaloEnergy>%s && tracks_matchedCaloEnergy<%s" % (tags["SREC_" + category], morecutsEC, EDepSideBandMin, EDepSideBandMax) + " +++ " + " && %s %s" % (tags["SR_" + category], morecuts), "", "multi"]
                
            for syst in [""]:
                zones["sr%s_%s%s_single" % (dedx, category, syst)] = [" && %s %s" % (tags["SR%s_" % syst + category], morecuts), "", "single"]
                zones["sr%s_%s%s_multi" % (dedx, category, syst)] = [" && %s %s" % (tags["SR%s_" % syst + category], morecuts), "", "multi"]
                zones["srgenfake%s_%s%s_single" % (dedx, category, syst)] = [" && %s && tracks_fake==1 %s" % (tags["SR%s_" % syst + category], morecuts), "", "single"]
                zones["srgenfake%s_%s%s_multi" % (dedx, category, syst)] = [" && %s && tracks_fake==1 %s" % (tags["SR%s_" % syst + category], morecuts), "", "multi"]
                zones["srgenprompt%s_%s%s_single" % (dedx, category, syst)] = [" && %s && tracks_fake==0 %s" % (tags["SR%s_" % syst + category], morecuts), "single"]
                zones["srgenprompt%s_%s%s_multi" % (dedx, category, syst)] = [" && %s && tracks_fake==0 %s" % (tags["SR%s_" % syst + category], morecuts), "multi"]
                zones["fakecr%s_%s%s" % (dedx, category, syst)] = [" && %s %s" % (tags["CR%s_" % syst + category], morecuts), ""]
                if options.mode == "analysis":
                    #zones["fakeprediction-QCDLowMHT%s_%s%s" % (dedx, category, syst)] =       [" && %s %s" % (tags["CR%s_" % syst + category], morecuts), "HT_QCDLowMHT_fakerate_%s%s" % (category, syst)]
                    zones["fakeprediction-QCDLowMHT2D%s_%s%s" % (dedx, category, syst)] =     [" && %s %s" % (tags["CR%s_" % syst + category], morecuts), "HT:n_allvertices_QCDLowMHT_fakerate_%s%s" % (category, syst)]
                    #zones["fakepredictionECSB-QCDLowMHT%s_%s%s" % (dedx, category, syst)] =   [" && %s %s" % (tags["CR%s_" % syst + category], morecuts), "HT_QCDLowMHT_fakerateECSB_%s%s" % (category, syst)]
                    #zones["fakepredictionECSB-QCDLowMHT2D%s_%s%s" % (dedx, category, syst)] = [" && %s %s" % (tags["CR%s_" % syst + category], morecuts), "HT:n_allvertices_QCDLowMHT_fakerateECSB_%s%s" % (category, syst)]
   
    #n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<90 && leadinglepton_id==13 && tracks_mva_loose>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01 && tracks_is_pixel_track==1 && tracks_matchedCaloEnergy<10 && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_deDxHarmonic2pixelCorrected<9999
   
    event_selections = {}
    event_selections["analysis"] = collections.OrderedDict()
    event_selections["analysis"]["Baseline"] =           "(n_goodleptons==0 || (leadinglepton_mt>90 && tracks_invmass>110))"
    #event_selections["analysis"]["HadBaseline"] =        "HT>150 && MHT>150 && n_goodjets>=1 && n_goodleptons==0"
    #event_selections["analysis"]["SMuBaseline"] =        "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leadinglepton_mt>90"
    #event_selections["analysis"]["SMuValidationZLL"] =   "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90"
    event_selections["analysis"]["SMuValidationMT"] =     "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<90"
    #event_selections["analysis"]["QCDLowMHT"] =          "n_goodleptons==0 && MHT<100"
    #event_selections["analysis"]["SElBaseline"] =        "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90"
    #event_selections["analysis"]["SElValidationZLL"] =   "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90"
    event_selections["analysis"]["SElValidationMT"] =     "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leadinglepton_mt<90"
    #event_selections["analysis"]["PromptDY"] =           "n_goodelectrons>0 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110"
    event_selections["analysis"]["PromptDY"] =            "leadinglepton_id==11 && tracks_invmass>=70 && tracks_invmass<=110"
    #event_selections["analysis"]["PromptDY"] =            "leadinglepton_id==11"

    event_selections["fakerate"] = collections.OrderedDict()
    #event_selections["fakerate"]["QCDLowMHT"] =          "n_goodleptons==0 && MHT<150"
    event_selections["fakerate"]["QCDLowMHT"] =           "n_goodleptons==0 && MHT<100"
    #event_selections["fakerate"]["QCDLowMHT"] =          "n_goodleptons==0 && MHT<50"
    #event_selections["fakerate"]["Dilepton"] =           "dilepton_invmass>60 && dilepton_invmass<120"
    #event_selections["fakerate"]["DileptonLowMHT"] =     "dilepton_invmass>70 && dilepton_invmass<110 && MHT<150"
    #event_selections["fakerate"]["DileptonEl"] =         "dilepton_leptontype==11 && dilepton_invmass>70 && dilepton_invmass<110"
    #event_selections["fakerate"]["DileptonMu"] =         "dilepton_leptontype==13 && dilepton_invmass>70 && dilepton_invmass<110"
              
    fakeratesamples = {
                #"Summer16": ["Summer16.DYJetsToLL*root", "Summer16.QCD*root", "Summer16.WJetsToLNu*root", "Summer16.ZJetsToNuNu_HT*root", "Summer16.WW_TuneCUETP8M1*root", "Summer16.WZ_TuneCUETP8M1*root", "Summer16.ZZ_TuneCUETP8M1*root", "Summer16.TTJets_DiLept*root", "Summer16.TTJets_SingleLeptFromT*root"],
                "Run2016": ["Run2016*JetHT*root"],
                #"Run2017": ["Run2017*JetHT*root"],
                #"Run2018": ["Run2018*JetHT*root"],
              }
              
    samples = {
                #"Summer16": ["Summer16.DYJetsToLL*root", "Summer16.QCD*root", "Summer16.WJetsToLNu*root", "Summer16.ZJetsToNuNu_HT*root", "Summer16.WW_TuneCUETP8M1*root", "Summer16.WZ_TuneCUETP8M1*root", "Summer16.ZZ_TuneCUETP8M1*root", "Summer16.TTJets_DiLept*root", "Summer16.TTJets_SingleLeptFromT*root"],
                "Run2016SingleElectron": ["Run2016*SingleElectron*root"],
                "Run2016SingleMuon": ["Run2016*SingleMuon*root"],
                "Run2016MET": ["Run2016*MET*root"],
                #"Run2017SingleElectron": ["Run2017*SingleElectron*root"],
                #"Run2017SingleMuon": ["Run2017*SingleMuon*root"],
                #"Run2017MET": ["Run2017*MET*root"],
                #"Run2018SingleElectron": ["Run2018*SingleElectron*root"],
                #"Run2018SingleMuon": ["Run2018*SingleMuon*root"],
                #"Run2018MET": ["Run2018*MET*root"],
              }
                                                  
    if options.inputfile:
        if options.mode == "fakerate":
            fakeratefile = False
        else:
            fakeratefile = options.fakeratefile
        
        if fakeratefile and fakeratefile != "False":
            fakeratefile = options.outputfolder + "/" + fakeratefile
        else:
            fakeratefile = False
        
        event_loop([options.inputfile], options.outputfile, tags, variables[options.mode], binnings, event_selections[options.mode], zones, fakeratefile, options.mode, nevents=options.nev, treename="Events", event_start=options.event_start)
                    
    else:
        
        os.system("mkdir -p %s" % options.outputfolder)
        os.system("mkdir -p %s_fakerate" % options.outputfolder)
        outputfolder_fakerate = options.outputfolder + "_fakerate"
        
        # 1) calculate fake rate num and denom:
        print "\n@@@@@@@@\nstep 1\n@@@@@@@@\n"
        inputfiles = []
        for data_period in fakeratesamples:
            for sample in fakeratesamples[data_period]:
                #FIXME
                #inputfiles += glob.glob(options.skimfolder + "/" + sample)[0:20]
                inputfiles += glob.glob(options.skimfolder + "/" + sample)[:]
        commands = []
        for i, inputfile in enumerate(inputfiles):            
            if options.jobs_per_file>1:
                fin = TFile(inputfile)
                tree = fin.Get("Events")
                nev = tree.GetEntries()
                fin.Close()
                for iStart in range(0, nev, int(nev/options.jobs_per_file)):
                    cmd = "./ddbg_eventloop.py --outputfolder %s --inputfile %s --outputfile %s --mode fakerate --event_start %s --nev %s --tag %s; " % (outputfolder_fakerate, inputfile, outputfolder_fakerate + "/" + inputfile.split("/")[-1], iStart, int(nev/options.jobs_per_file), options.tag)
                    commands.append(cmd)
            else:
                cmd = "./ddbg_eventloop.py --outputfolder %s --inputfile %s --outputfile %s --mode fakerate  --tag %s; " % (outputfolder_fakerate, inputfile, outputfolder_fakerate + "/" + inputfile.split("/")[-1], options.tag)
                commands.append(cmd)
                
        print "Running %s jobs" % len(commands)        
        print "@@@@@@@@@"
        print commands
        print "@@@@@@@@@"        
        GridEngineTools.runParallel(commands, options.runmode, "%s.condor" % outputfolder_fakerate + "_fakerate", confirm=False)
                
        # 2) hadd everything:
        print "\n@@@@@@@@\nstep 2\n@@@@@@@@\n"
        hadd_everything(fakeratesamples, outputfolder_fakerate)
        
        # 3) calculate fake rate:
        print "\n@@@@@@@@\nstep 3\n@@@@@@@@\n"
        try:
            calculate_fakerate(options.outputfolder + "/" + options.fakeratefile, fakeratesamples, variables["fakerate"], event_selections["fakerate"], outputfolder_fakerate)
        except Exception as e:
            print str(e)
                        
        # 4) run parallel to get histograms / predictions in event loop
        print "\n@@@@@@@@\nstep 4\n@@@@@@@@\n"
        inputfiles = []
        for data_period in samples:
            for sample in samples[data_period]:
                #FIXME
                #inputfiles += glob.glob(options.skimfolder + "/" + sample)[0:10]
                inputfiles += glob.glob(options.skimfolder + "/" + sample)[:]
        commands = []      
        for i, inputfile in enumerate(inputfiles):
            if options.jobs_per_file>1:         
                fin = TFile(inputfile)
                tree = fin.Get("Events")
                nev = tree.GetEntries()
                fin.Close()
                for iStart in range(0, nev, int(nev/options.jobs_per_file)):
                    print "iStart, ev in intervall, nev", iStart, int(nev/options.jobs_per_file), nev
                    cmd = "./ddbg_eventloop.py --outputfolder %s --inputfile %s --outputfile %s --mode analysis --event_start %s --nev %s  --tag %s; " % (options.outputfolder, inputfile, options.outputfolder + "/" + inputfile.split("/")[-1], iStart, int(nev/options.jobs_per_file), options.tag)
                    commands.append(cmd)
            else:
                cmd = "./ddbg_eventloop.py --outputfolder %s --inputfile %s --outputfile %s --mode analysis --tag %s; " % (options.outputfolder, inputfile, options.outputfolder + "/" + inputfile.split("/")[-1], options.tag)
                commands.append(cmd)
            
        print "Running %s jobs" % len(commands)        
        GridEngineTools.runParallel(commands, options.runmode, "%s.condor" % options.outputfolder, confirm=False)
        
        # 5) hadd
        print "\n@@@@@@@@\nstep 5\n@@@@@@@@\n"
        hadd_everything(samples, options.outputfolder)
        
        
        
    
    
