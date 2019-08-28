#!/bin/env python
from __future__ import division
from ROOT import *
from optparse import OptionParser
import math, os, glob
from GridEngineTools import runParallel
import collections
from array import array

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
    binnumbers[((0,float("inf")),(250,400),(1,1),  (0,float("inf")),(1,1),  (0,0),  (1,1),      (0.5,float("inf")))] = 1
    binnumbers[((0,float("inf")),(250,400),(1,1),  (0,float("inf")),(1,1),  (1,1),  (0,0),      (0.5,float("inf")))] = 2
    binnumbers[((0,float("inf")),(250,400),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.5,float("inf")))] = 3
    binnumbers[((0,float("inf")),(250,400),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,float("inf")))] = 4
    binnumbers[((0,float("inf")),(250,400),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.5,float("inf")))] = 5
    binnumbers[((0,float("inf")),(250,400),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.5,float("inf")))] = 6
    binnumbers[((0,float("inf")),(250,400),(6,float("inf")),(0,0),  (1,1),  (0,0),  (1,1),      (0.5,float("inf")))] = 7
    binnumbers[((0,float("inf")),(250,400),(6,float("inf")),(0,0),  (1,1),  (1,1),  (0,0),      (0.5,float("inf")))] = 8
    binnumbers[((0,float("inf")),(250,400),(6,float("inf")),(1,float("inf")),(1,1),  (0,0),  (1,1),      (0.5,float("inf")))] = 9
    binnumbers[((0,float("inf")),(250,400),(6,float("inf")),(1,float("inf")),(1,1),  (1,1),  (0,0),      (0.5,float("inf")))] = 10
    binnumbers[((0,float("inf")),(400,700),(1,1),  (0,float("inf")),(1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 11
    binnumbers[((0,float("inf")),(400,700),(1,1),  (0,float("inf")),(1,1),  (1,1),  (0,0),      (0.3,float("inf")))] = 12
    binnumbers[((0,float("inf")),(400,700),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 13
    binnumbers[((0,float("inf")),(400,700),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.5,float("inf")))] = 14
    binnumbers[((0,float("inf")),(400,700),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 15
    binnumbers[((0,float("inf")),(400,700),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,float("inf")))] = 16
    binnumbers[((0,float("inf")),(400,700),(6,float("inf")),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 17
    binnumbers[((0,float("inf")),(400,700),(6,float("inf")),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,float("inf")))] = 18
    binnumbers[((0,float("inf")),(400,700),(6,float("inf")),(1,float("inf")),(1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 19
    binnumbers[((0,float("inf")),(400,700),(6,float("inf")),(1,float("inf")),(1,1),  (1,1),  (0,0),      (0.3,float("inf")))] = 20
    binnumbers[((0,float("inf")),(700,float("inf")),(1,1),  (0,float("inf")),(1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 21
    binnumbers[((0,float("inf")),(700,float("inf")),(1,1),  (0,float("inf")),(1,1),  (1,1),  (0,0),      (0.5,float("inf")))] = 22
    binnumbers[((0,float("inf")),(700,float("inf")),(2,5),  (0,0),  (1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 23
    binnumbers[((0,float("inf")),(700,float("inf")),(2,5),  (0,0),  (1,1),  (1,1),  (0,0),      (0.3,float("inf")))] = 24
    binnumbers[((0,float("inf")),(700,float("inf")),(2,5),  (1,5),  (1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 25
    binnumbers[((0,float("inf")),(700,float("inf")),(2,5),  (1,5),  (1,1),  (1,1),  (0,0),      (0.3,float("inf")))] = 26
    binnumbers[((0,float("inf")),(700,float("inf")),(6,float("inf")),(0,0),  (1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 27
    binnumbers[((0,float("inf")),(700,float("inf")),(6,float("inf")),(0,0),  (1,1),  (1,1),  (0,0),      (0.3,float("inf")))] = 28
    binnumbers[((0,float("inf")),(700,float("inf")),(6,float("inf")),(1,float("inf")),(1,1),  (0,0),  (1,1),      (0.3,float("inf")))] = 29
    binnumbers[((0,float("inf")),(700,float("inf")),(6,float("inf")),(1,float("inf")),(1,1),  (1,1),  (0,0),      (0.3,float("inf")))] = 30
    binnumbers[((0,float("inf")),(0,400),  (0,float("inf")),(0,float("inf")),(2,float("inf")),(0,float("inf")),(0,float("inf")),    (0.0,float("inf")))]= 31
    binnumbers[((0,float("inf")),(400,float("inf")),(0,float("inf")),(0,float("inf")),(2,float("inf")),(0,float("inf")),(0,float("inf")),    (0.0,float("inf")))]= 32

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
        

def main(input_filenames, output_file, fakerate_file = "fakerate.root", bdt_folder = False, nevents = -1, treename = "Events", event_start = 0):

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
    histos["n_goodjets"] = TH1F("n_jets", "n_jets", 11, 0, 11)
    histos["MinDeltaPhiMhtJets"] = TH1F("MinDeltaPhiMhtJets", "MinDeltaPhiMhtJets", 20, 0, 1)
    histos["n_btags"] = TH1F("n_btags", "n_btags", 21, 0, 20)
    histos["region_long"] = TH1F("region_long", "region_long", 33, 0, 33)
    histos["region_short"] = TH1F("region_short", "region_short", 33, 0, 33)
    histos["region_multi"] = TH1F("region_multi", "region_multi", 33, 0, 33)

    control_regions = {
                        #"cr0": "event.passesUniversalSelection==1                   and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0",
                        "cr1": "event.passesUniversalSelection==1 and event.MHT>50  and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0",
                        #"cr2": "event.passesUniversalSelection==1 and event.MHT>100 and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0",
                        #"cr3": "event.passesUniversalSelection==1 and event.MHT>150 and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0",
                        #"cr4": "event.passesUniversalSelection==1 and event.MHT>200 and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0",
                        #"cr5": "event.passesUniversalSelection==1 and event.MHT>250 and event.MinDeltaPhiMhtJets>0.3 and event.n_goodjets>0 and event.n_goodelectrons==0",
                      }

    output_variables = histos.keys()

    #tag_names = ["tight", "loose1", "loose2", "loose3", "loose4"]
    tag_names = ["loose6", "looseloose6dz1", "looseloose6dz3"]

    # load fake rate histograms:
    fakerate_regions = []
    for i_region in ["qcd_lowMHT"]:
        for i_cond in tag_names:
            for i_cat in ["_short", "_long"]:
                fakerate_regions.append(i_region + "_" + i_cond + i_cat)

    #fakerate_variables = ["HT", "n_allvertices", "HT:n_allvertices", "BDT1", "BDT2", "BDT3", "BDT4", "BDT5", "BDT6", "BDT7", "BDT8", "BDT9"]
    #fakerate_variables = ["HT:n_allvertices", "BDT1", "BDT2", "BDT3", "BDT4", "BDT5", "BDT6", "BDT7", "BDT8", "BDT9"]
    fakerate_variables = ["HT:n_allvertices"]

    if fakerate_file:
        
        # load fakerate maps:
        tfile_fakerate = TFile(fakerate_file, "open")

        # get all fakerate histograms:
        h_fakerates = {}
        for region in fakerate_regions:
            for variable in fakerate_variables:    

                if "BDT" in variable: continue
               
                hist_name = region + "/" + data_period + "/fakerate_" + variable.replace(":", "_")
                
                hist_name = hist_name.replace("//", "/")
                try:
                    h_fakerates[hist_name] = tfile_fakerate.Get(hist_name)
                except:
                    print "Can't read, using FR=1", hist_name
                    h_fakerates[hist_name] = TH1F(hist_name, hist_name, 1, -10000, 10000)
                    h_fakerates[hist_name].Fill(1)

    # add more histograms
    more_hists = []
    for variable in output_variables:               
        for fakerate_variable in fakerate_variables:
            for category in ["short", "long"]:
                for cr in control_regions:
                    for label in ["tagged", "prediction"]:
                        for fr_region in fakerate_regions:
                                h_suffix = "_%s_%s_%s_%s" % (fr_region, fakerate_variable.replace(":", "_"), label, cr)
                                histos[variable + h_suffix] = histos[variable].Clone()
                                histos[variable + h_suffix].SetName(variable + h_suffix)
                    
                    for tag in tag_names:
                        for itype in ["fakebg", "promptbg", "control", "tagged"]:
                            h_suffix =  "_%s_%s_%s_%s" % (tag, itype, category, cr)
                            histos[variable + h_suffix] = histos[variable].Clone()
                            histos[variable + h_suffix].SetName(variable + h_suffix)
                            more_hists.append(h_suffix[1:])

    if nevents > 0:
        nev = nevents
    else:
        nev = tree.GetEntries()

    # Predict the regression target
    if bdt_folder:
        bdt_tags = [
                     "fakerate_Summer16_qcd_lowMHT_tight_short",
                     "fakerate_Summer16_qcd_lowMHT_tight_long",
                     "fakerate_Summer16_qcd_lowMHT_loose3_short",
                     "fakerate_Summer16_qcd_lowMHT_loose3_long",
                     "fakerate_Summer16_qcd_lowMHT_loose4_short",
                     "fakerate_Summer16_qcd_lowMHT_loose4_long",
                   ]

        readers = {}
        tmva_variables = {}
        tmva_variables["HT"] = array('f',[0])
        tmva_variables["n_allvertices"] = array('f',[0])
        for bdt_tag in bdt_tags:
            readers[bdt_tag] = TMVA.Reader()
            readers[bdt_tag].AddVariable("HT", tmva_variables["HT"])
            readers[bdt_tag].AddVariable("n_allvertices", tmva_variables["n_allvertices"])
            for i_BDT in ["BDT1", "BDT2", "BDT3", "BDT4", "BDT5", "BDT6", "BDT7", "BDT8", "BDT9"]:
                readers[bdt_tag].BookMVA(i_BDT, "%s/weights_%s/TMVARegression_%s.weights.xml" % (bdt_folder, bdt_tag, i_BDT))

    print "Looping over %s events" % nev

    for iEv, event in enumerate(tree):

        if iEv < event_start: continue
        if nevents > 0 and iEv > nevents + event_start: break
        
        if (iEv+1) % 10000 == 0:
            print "Processing event %s / %s" % (iEv + 1, nev)

        weight = 1.0 * event.CrossSection * event.puWeight / tree.GetEntries()

        # check if event passes control region
        pass_cr = {}    
        for cr in control_regions:
            pass_cr[cr] = eval(control_regions[cr])
        
        passes_cr = False
        for cr in pass_cr:
            if pass_cr[cr]:
                passes_cr = True
                break
        
        if not passes_cr: continue
        
        event.region_short = get_signal_region(event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, 1, True)
        event.region_long = get_signal_region(event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, 1, False)
        event.region_multi = get_signal_region(event.MHT, event.n_goodjets, event.n_btags, event.MinDeltaPhiMhtJets, 2, True)

        #############################
        # we're in a control region #
        #############################              

        for cr in pass_cr:
            
            # check if event passes this control region:
            if not pass_cr[cr]: continue
            
            for variable in output_variables:
            
                value = eval("event.%s" % variable)
            
                ###################################################
                # for each tag, check if in signal/control region #
                ###################################################
            
                flags = {}
                for label in more_hists:
                    for control_region in control_regions:
                        label = label.replace("_%s" % control_region, "")
                    flags[label] = 0

                def set_flag(label, flags, event, itrack):
                    if event.tracks_is_pixel_track[itrack]==1:
                        flags[label + "_short"] += 1
                    elif event.tracks_is_pixel_track[itrack]==0:
                        flags[label + "_long"] += 1
                    return flags

                # loop over tracks:
                #for i in range(len(event.tracks)):
                for i in range(len(event.tracks_pt)):
            
                    is_prompt_track = event.tracks_prompt_electron[i]==1 or event.tracks_prompt_muon[i]==1 or event.tracks_prompt_tau[i]==1 or event.tracks_prompt_tau_leadtrk[i]==1
                    is_fake_track = not is_prompt_track
                    good_track = event.tracks_is_reco_lepton[i]==0 and event.tracks_passPFCandVeto[i]==1 and event.tracks_passpionveto[i]==1 and event.tracks_passmask[i]!=0

                    if "tight" in tag_names:
                        # tight tag
                        if event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt[i]>0.1 and good_track:
                            flags = set_flag("tight_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("tight_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("tight_promptbg", flags, event, i)
                        flags["tight_control_short"] += 1
                        if event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt[i]>0.25 and good_track:
                            flags = set_flag("tight_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("tight_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("tight_promptbg", flags, event, i)
                        flags["tight_control_long"] += 1

                    if "loose1" in tag_names:
                        # loose1 tag: default tag to go
                        if event.tracks_mva_bdt_loose[i]>0 and event.tracks_dxyVtx[i]<=0.01 and good_track:
                            flags = set_flag("loose1_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("loose1_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("loose1_promptbg", flags, event, i)
                        if event.tracks_mva_bdt_loose[i]>0 and event.tracks_dxyVtx[i]>0.01 and good_track:
                            flags = set_flag("loose1_control", flags, event, i)

                    if "loose2" in tag_names:                    
                        # loose2 tag: Akshansh's recipe
                        if event.tracks_mva_bdt_loose[i]>0 and event.tracks_dxyVtx[i]<=0.01 and good_track:
                            flags = set_flag("loose2_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("loose2_fakebg", flags, event, i)
                            if is_prompt_track:
                                flags = set_flag("loose2_promptbg", flags, event, i)
                        if event.tracks_mva_bdt_loose[i]>0 and event.tracks_dxyVtx[i]>0.02 and event.tracks_dxyVtx[i]<0.1 and good_track:
                            flags = set_flag("loose2_control", flags, event, i)


                    if "loose3" in tag_names:            
                        # loose3 tag: fancy cut function
                        if event.tracks_mva_bdt_loose[i]>event.tracks_dxyVtx[i]*0.5/0.01 and good_track:
                            flags = set_flag("loose3_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("loose3_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("loose3_promptbg", flags, event, i)
                        if event.tracks_mva_bdt_loose[i]<event.tracks_dxyVtx[i]*0.5/0.01 and good_track:
                            flags = set_flag("loose3_control", flags, event, i)                        

                    if "loose4" in tag_names:                    
                        # loose4 tag: fancy cut function, Sams changes
                        if event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt_loose[i]>(event.tracks_dxyVtx[i]*0.7/0.01 - 0.1) and good_track:
                            flags = set_flag("loose4_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("loose4_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("loose4_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt_loose[i]<(event.tracks_dxyVtx[i]*0.7/0.01 - 0.1) and good_track:
                            flags["loose4_control_short"] += 1
                        if event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt_loose[i]>(event.tracks_dxyVtx[i]*0.7/0.01 + 0.15) and good_track:
                            flags = set_flag("loose4_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("loose4_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("loose4_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt_loose[i]<(event.tracks_dxyVtx[i]*0.7/0.01 + 0.15) and good_track:
                            flags["loose4_control_long"] += 1

                    if "loose5" in tag_names:                    
                        # loose5 tag: fancy cut function, Sams changes
                        if event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt_loose[i]>(event.tracks_dxyVtx[i]*0.5/0.01 - 0.3) and good_track:
                            flags = set_flag("loose5_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("loose5_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("loose5_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt_loose[i]<(event.tracks_dxyVtx[i]*0.5/0.01 - 0.3) and good_track:
                            flags["loose5_control_short"] += 1
                        if event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt_loose[i]>(event.tracks_dxyVtx[i]*0.6/0.01 + 0.05) and good_track:
                            flags = set_flag("loose5_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("loose5_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("loose5_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt_loose[i]<(event.tracks_dxyVtx[i]*0.6/0.01 + 0.05) and good_track:
                            flags["loose5_control_long"] += 1

                    if "loose6" in tag_names:                    
                        if event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt_loose[i]>(event.tracks_dxyVtx[i]*(0.65/0.01) - 0.25) and good_track:
                            flags = set_flag("loose6_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("loose6_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("loose6_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==1 and event.tracks_mva_bdt_loose[i]<(event.tracks_dxyVtx[i]*(0.65/0.01) - 0.25) and good_track:
                            flags["loose6_control_short"] += 1
                        if event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt_loose[i]>(event.tracks_dxyVtx[i]*(0.7/0.01) + 0.05) and good_track:
                            flags = set_flag("loose6_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("loose6_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("loose6_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==0 and event.tracks_mva_bdt_loose[i]<(event.tracks_dxyVtx[i]*(0.7/0.01) + 0.05) and good_track:
                            flags["loose6_control_long"] += 1

                    if "looseloose6dz1" in tag_names:                    
                        if event.tracks_is_pixel_track[i]==1 and event.tracks_dzVtx[i]<0.1 and event.tracks_mva_bdt_looseloose[i]>(event.tracks_dxyVtx[i]*(0.65/0.01) - 0.25) and good_track:
                            flags = set_flag("looseloose6dz1_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("looseloose6dz1_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("looseloose6dz1_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==1 and event.tracks_dzVtx[i]<0.1 and event.tracks_mva_bdt_looseloose[i]<(event.tracks_dxyVtx[i]*(0.65/0.01) - 0.25) and good_track:
                            flags["looseloose6dz1_control_short"] += 1
                        if event.tracks_is_pixel_track[i]==0 and event.tracks_dzVtx[i]<0.1 and event.tracks_mva_bdt_looseloose[i]>(event.tracks_dxyVtx[i]*(0.7/0.01) + 0.05) and good_track:
                            flags = set_flag("looseloose6dz1_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("looseloose6dz1_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("looseloose6dz1_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==0 and event.tracks_dzVtx[i]<0.1 and event.tracks_mva_bdt_looseloose[i]<(event.tracks_dxyVtx[i]*(0.7/0.01) + 0.05) and good_track:
                            flags["looseloose6dz1_control_long"] += 1

                    if "looseloose6dz3" in tag_names:                    
                        if event.tracks_is_pixel_track[i]==1 and event.tracks_dzVtx[i]<0.3 and event.tracks_mva_bdt_looseloose[i]>(event.tracks_dxyVtx[i]*(0.65/0.01) - 0.25) and good_track:
                            flags = set_flag("looseloose6dz3_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("looseloose6dz3_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("looseloose6dz3_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==1 and event.tracks_dzVtx[i]<0.3 and event.tracks_mva_bdt_looseloose[i]<(event.tracks_dxyVtx[i]*(0.65/0.01) - 0.25) and good_track:
                            flags["looseloose6dz3_control_short"] += 1
                        if event.tracks_is_pixel_track[i]==0 and event.tracks_dzVtx[i]<0.3 and event.tracks_mva_bdt_looseloose[i]>(event.tracks_dxyVtx[i]*(0.7/0.01) + 0.05) and good_track:
                            flags = set_flag("looseloose6dz3_tagged", flags, event, i)
                            if is_fake_track:
                                flags = set_flag("looseloose6dz3_fakebg", flags, event, i)
                            elif is_prompt_track:
                                flags = set_flag("looseloose6dz3_promptbg", flags, event, i)
                        elif event.tracks_is_pixel_track[i]==0 and event.tracks_dzVtx[i]<0.3 and event.tracks_mva_bdt_looseloose[i]<(event.tracks_dxyVtx[i]*(0.7/0.01) + 0.05) and good_track:
                            flags["looseloose6dz3_control_long"] += 1

                # check if event has at least one interesting track:
                event_ignore = True
                for flag in flags:
                    if flags[flag] > 0:
                        event_ignore = False
                        break
                if event_ignore: continue
                
                for label in flags:
                    if flags[label]:
                        if variable + "_" + label + "_" + cr in histos:

                            # for multiple DR search bins, count n_DT for this label:
                            if variable == "region_multi":
                                if flags[label]<2:
                                    continue

                            histos[variable + "_" + label + "_" + cr].Fill(value, weight)
           
                ###################################################
                # get fake rate from histogram/map for each event #
                ###################################################
            
                if fakerate_file:

                    for fakerate_variable in fakerate_variables:
                
                        if "BDT" in fakerate_variable: continue

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
                
                            try:
                                if ":" in fakerate_variable:
                                    fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue, yval = yvalue)
                                else:                
                                    fakerate = getBinContent_with_overflow(h_fakerates[hist_name], xvalue)
                            except:
                                print "ERROR getting fake rate for", hist_name
                                quit()
                            
                            if "short" in hist_name:
                                if ("tight" in tag_names and "tight" in hist_name and flags["tight_control_short"]) or \
                                   ("loose6" in tag_names and "loose6" in hist_name and flags["loose6_control_short"]) or \
                                   ("loose6dz1" in tag_names and "loose6dz1" in hist_name and flags["loose6dz1_control_short"]) or \
                                   ("loose6dz3" in tag_names and "loose6dz3" in hist_name and flags["loose6dz3_control_short"]) or \
                                   ("loose6dzX" in tag_names and "loose6dzX" in hist_name and flags["loose6dzX_control_short"]) or \
                                   ("loose1" in tag_names and "loose1" in hist_name and flags["loose1_control_short"]) or \
                                   ("loose2" in tag_names and "loose2" in hist_name and flags["loose2_control_short"]) or \
                                   ("loose3" in tag_names and "loose3" in hist_name and flags["loose3_control_short"]) or \
                                   ("loose4" in tag_names and "loose4" in hist_name and flags["loose4_control_short"]) or \
                                   ("loose5" in tag_names and "loose5" in hist_name and flags["loose5_control_short"]):

                                   if variable == "region_multi":
                                       fakerate = fakerate*fakerate
                                    
                                   histos[variable + "_" + fr_region + "_" + fakerate_variable.replace(":", "_") + "_prediction_" + cr].Fill(value, weight * fakerate)
                
                            elif "long" in hist_name:
                                if ("tight" in tag_names and "tight" in hist_name and flags["tight_control_long"]) or \
                                   ("loose6" in tag_names and "loose6" in hist_name and flags["loose6_control_long"]) or \
                                   ("loose6dz1" in tag_names and "loose6dz1" in hist_name and flags["loose6dz1_control_long"]) or \
                                   ("loose6dz3" in tag_names and "loose6dz3" in hist_name and flags["loose6dz3_control_long"]) or \
                                   ("loose6dzX" in tag_names and "loose6dzX" in hist_name and flags["loose6dzX_control_long"]) or \
                                   ("loose1" in tag_names and "loose1" in hist_name and flags["loose1_control_long"]) or \
                                   ("loose2" in tag_names and "loose2" in hist_name and flags["loose2_control_long"]) or \
                                   ("loose3" in tag_names and "loose3" in hist_name and flags["loose3_control_long"]) or \
                                   ("loose4" in tag_names and "loose4" in hist_name and flags["loose4_control_long"]) or \
                                   ("loose5" in tag_names and "loose5" in hist_name and flags["loose5_control_long"]):

                                   if variable == "region_multi":
                                       fakerate = fakerate*fakerate

                                   histos[variable + "_" + fr_region + "_" + fakerate_variable.replace(":", "_") + "_prediction_" + cr].Fill(value, weight * fakerate)

                if bdt_folder:
                    tmva_variables["HT"][0] = event.HT
                    tmva_variables["n_allvertices"][0] = event.n_allvertices
                    for fr_region in fakerate_regions:
                        bdt_tag = "fakerate_%s_%s" % (data_period, fr_region)
                        if bdt_tag in readers:
                            for i_BDT in fakerate_variables:
                                if not "BDT" in i_BDT: continue
                                fakerate = readers[bdt_tag].EvaluateRegression(i_BDT)[0]
                                print "fakerate =", fakerate
                                histos[variable + "_" + fr_region + "_" + i_BDT + "_prediction_" + cr].Fill(value, weight * fakerate)

    if event_start>0:
        output_file = output_file.replace(".root", "_%s.root" % event_start)

    fout = TFile(output_file, "recreate")
    for var in histos:
        histos[var].Write()

    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest = "inputfiles")
    parser.add_option("--output", dest = "outputfiles")
    parser.add_option("--prediction_folder", dest = "prediction_folder", default="prediction")
    parser.add_option("--nev", dest = "nev", default = -1)
    parser.add_option("--jobs_per_file", dest = "jobs_per_file", default = 50)
    parser.add_option("--event_start", dest = "event_start", default = 0)
    parser.add_option("--fakerate_file", dest = "fakerate_file", default = "fakerate.root")
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--start", dest="start", action="store_true")
    (options, args) = parser.parse_args()
       
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
    
    # run parallel if input is a folder:
    if options.inputfiles[-1] == "/":
        print "Got input folder, running in batch mode (%s)" % options.runmode
       
        input_files = glob.glob(options.inputfiles + "/*.root")
        os.system("mkdir -p %s" % options.prediction_folder)
        commands = []

        for input_file in input_files:
            if "QCD_HT" not in input_file and "ZJetsToNuNu_HT" not in input_file: continue
                
            # get nev:
            tree = TChain("Events")
            tree.Add(input_file)
            nev = tree.GetEntries()
            
            nev_per_interval = int(nev/int(options.jobs_per_file))
            
            for i in range(int(options.jobs_per_file)):
                
                event_start = i * nev_per_interval
                
                commands.append("./get_prediction.py --input %s --output %s/%s --nev %s --fakerate_file %s --event_start %s" % (input_file, options.prediction_folder, input_file.split("/")[-1], nev_per_interval, options.fakerate_file, event_start))
           
        runParallel(commands, options.runmode, condorDir = "get_prediction.condor", use_more_mem=False, use_more_time=False, confirm=not options.start)

    # otherwise run locally:
    else:
        options.inputfiles = options.inputfiles.split(",")

        main(options.inputfiles,
             options.outputfiles,
             nevents = int(options.nev),
             fakerate_file = options.fakerate_file,
             event_start = int(options.event_start),
            )
