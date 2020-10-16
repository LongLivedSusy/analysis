#!/bin/env python
from __future__ import division
import __main__ as main
from ROOT import *
import collections
import os
import shared_utils
from optparse import OptionParser

color_fakebg = kSpring - 1
color_promptbg = kAzure + 1

use_prompt_fakesubtraction = True

def get_histo(root_file, label, lumi = False, title = False, color = False):
    
    print label
    
    #if "gen" in label:
    #    label = label.replace("_short", "short").replace("_long", "long").replace("_gen", "gen")
    
    #print "getting %s from %s" % (label, root_file)
    
    fin = TFile(root_file, "read")
    histo = fin.Get(label)
    histo.SetDirectory(0)
    fin.Close()
    histo.SetLineWidth(2)
    shared_utils.histoStyler(histo)
    if not "Run201" in label and lumi:
        # this is MC, scale with lumi:
        histo.Scale(lumi)
    #else:
    #    # this is data, scale up to Run-2 lumi....:
    #    histo.Scale(3.8)
    #    histo.SetTitle("Data (2016)")
    #    histo.SetTitle("Data")

    if title:
        histo.SetTitle(title)
    if color:
        histo.SetLineColor(color)
        histo.SetFillColor(color)

    return histo


def plot_prediction(variable, root_file, datalabel, category, lumi, region, pdffile, outputfolder):

    os.system("mkdir -p " + outputfolder)
    dataid = datalabel + "_" + variable + "_" + region
    
    histos = collections.OrderedDict()
   
    h_fakeprediction = 0
    h_promptprediction = 0
    
    ###############################
    # get predictions and geninfo #
    ###############################
    
    histos["fakeprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakeprediction_" + category, lumi, "Fake prediction", color_fakebg)
    if use_prompt_fakesubtraction:
        #histos["promptprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptpredictionsubtracted_" + category, lumi, "Prompt prediction", color_promptbg)
        histos["promptprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptprediction_" + category, lumi, "Prompt prediction", color_promptbg)
        h_fake_ccontribution = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptRegionCkappa3_" + category, lumi, "Prompt prediction", color_promptbg)
        histos["promptprediction"].Add(h_fake_ccontribution, -1)

    else:
        histos["promptprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptprediction_" + category, lumi, "Prompt prediction", color_promptbg)
    
    if "Run201" not in datalabel:
        histos["srgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_srgenfake_" + category, lumi, "MC fakes", color_fakebg)
        histos["srgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_srgenprompt_" + category, lumi, "MC prompt", color_promptbg)
        histos["fakecrgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakecrgenfake_" + category, lumi, "MC fakes", color_fakebg)
        histos["fakecrgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakecrgenprompt_" + category, lumi, "MC prompt", color_promptbg)
        histos["promptECaloLowgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloLowgenfake_" + category, lumi, "MC fakes", color_fakebg)
        histos["promptECaloLowgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloLowgenprompt_" + category, lumi, "MC prompt", color_promptbg)
        histos["promptECaloSidebandgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloSidebandgenfake_" + category, lumi, "MC fakes", color_fakebg)
        histos["promptECaloSidebandgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloSidebandgenprompt_" + category, lumi, "MC prompt", color_promptbg)    
    
    c1 = shared_utils.mkcanvas()
    htmp = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptRegionCkappa1_" + category, lumi, "htmp", color_promptbg)
    htmp.Draw()
    c1.Print("kappa1%s.pdf" % category)

    htmp = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptRegionCkappa2_" + category, lumi, "htmp", color_promptbg)
    htmp.Draw()
    c1.Print("kappa2%s.pdf" % category)
    
    htmp = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptRegionCkappa3_" + category, lumi, "htmp", color_promptbg)
    htmp.Draw()
    c1.Print("kappa3%s.pdf" % category)
    
    htmp = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptRegionCkappa4_" + category, lumi, "htmp", color_promptbg)
    htmp.Draw()
    c1.Print("kappa4%s.pdf" % category)
    
    

    
    def makeplot(stacked_histograms, datahist, plotlabel):

        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    
        ymin = 1e-1; ymax = 1e2
        datahist.GetYaxis().SetRangeUser(ymin, ymax)
        for stacked_histogram in stacked_histograms:
            stacked_histogram.GetYaxis().SetRangeUser(ymin, ymax)
            stacked_histogram.GetYaxis().SetLimits(ymin, ymax)
    
        hratio, pads = shared_utils.FabDraw(canvas, legend, datahist, stacked_histograms, datamc = 'Data', lumi = lumi/1e3)
        stacked_histograms[-1].SetTitle("")
    
        hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
        if "Run201" in dataid:
            hratio.GetYaxis().SetTitle('Data/prediction')
        else:
            hratio.GetYaxis().SetTitle('Fake pred./truth')
        
        xlabel = variable
        xlabel = xlabel.replace("leptons_mt", "m_{T}^{lepton} (GeV)")
        xlabel = xlabel.replace("leadinglepton_mt", "m_{T}^{lepton} (GeV)")
        hratio.GetXaxis().SetTitle(xlabel)
        
        # add prompt and fake MC truth ratios:
        if plotlabel == "mctruthsr":
            h_fakepred_ratio = histos["fakeprediction"].Clone()
            h_fakepred_ratio.Divide(histos["srgenfake"].Clone())
            h_promptpred_ratio = histos["promptprediction"].Clone()
            h_promptpred_ratio.Divide(histos["srgenprompt"].Clone())
            pads[1].cd()
            h_promptpred_ratio.Draw("hist same")
            h_promptpred_ratio.SetFillColor(0)
            h_fakepred_ratio.Draw("hist same")
            h_fakepred_ratio.SetFillColor(0)
        
        elif plotlabel == "mctruthfakecr":
            h_fakecrgenfake = histos["fakecrgenfake"].Clone()
            h_fakecrgenprompt = histos["fakecrgenprompt"].Clone()
            pads[0].cd()
            h_fakecrgenfake.Draw("hist same")
            h_fakecrgenfake.SetFillColor(0)
            h_fakecrgenprompt.Draw("hist same")
            h_fakecrgenprompt.SetFillColor(0)
    
        for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
            if hratio.GetBinContent(ibin)==0:
                hratio.SetBinContent(ibin,-999)
        hratio.SetMarkerColor(kBlack)
        
           
        foldername = outputfolder + "/%s%s" % (category.replace("_short", "Short").replace("_long", "Long"), region)
        if use_prompt_fakesubtraction:
            foldername += "Subtraction"

        os.system("mkdir -p " + foldername)

        #canvas.SaveAs(foldername + "/" + pdffile + "_" + plotlabel + ".pdf")
        canvas.SaveAs(foldername + "/" + pdffile + "_" + plotlabel + "_" + data_period + ".png")
                
    # predictions vs. data:
    stacked_histograms = [
                           histos["promptprediction"].Clone(),
                           histos["fakeprediction"].Clone(),
                         ]
    datahist = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_" + category)
    datahist.SetTitle("Signal region")
    makeplot(stacked_histograms, datahist, "predictdata")
        
    
        
    # predictions vs. data:
    #tacked_histograms = [
    #                      #get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloSideband_" + category),
    #                      histos["promptprediction"].Clone(),
    #                      #histos["fakeprediction"].Clone(),
    #                    ]
    #atahist = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloLow_" + category)
    #atahist.SetTitle("Signal region")
    #akeplot(stacked_histograms, datahist, "promptECaloLow")
    
        
    if "Run201" not in datalabel:
        # genfake vs fakepred, genprompt vs promptpred, all gen vs. all pred:
        stacked_histograms = [
                               histos["srgenprompt"].Clone(),
                               histos["srgenfake"].Clone(),
                             ]
        datahist = histos["srgenprompt"]
        datahist.Add(histos["srgenfake"])
        datahist.SetTitle("Added predictions")
        makeplot(stacked_histograms, datahist, "mctruthsr")
        
        # fake cr MC Truth:
        stacked_histograms = [
                               histos["fakecrgenprompt"].Clone(),
                               histos["fakecrgenfake"].Clone(),
                             ]
        datahist = histos["fakecrgenprompt"]
        datahist.Add(histos["fakecrgenfake"])
        datahist.SetTitle("Combined MC Truth")
        makeplot(stacked_histograms, datahist, "mctruthfakecr")

        # fake cr MC Truth:
        stacked_histograms = [
                               histos["promptECaloSidebandgenprompt"].Clone(),
                               histos["promptECaloSidebandgenfake"].Clone(),
                             ]
        datahist = histos["promptECaloSidebandgenprompt"]
        datahist.Add(histos["promptECaloSidebandgenfake"])
        datahist.SetTitle("Combined MC Truth")
        makeplot(stacked_histograms, datahist, "mctruthpromptcr")


        # prompt closure:
        stacked_histograms = [
                               histos["promptprediction"].Clone(),
                             ]
        datahist = histos["srgenprompt"]
        datahist.SetTitle("Prompt MC Truth")
        makeplot(stacked_histograms, datahist, "promptclosure")
        
        # fake closure:
        stacked_histograms = [
                               histos["fakeprediction"].Clone(),
                             ]
        datahist = histos["srgenfake"]
        datahist.SetTitle("Non-prompt MC Truth")
        makeplot(stacked_histograms, datahist, "fakeclosure")

        
        #stacked_histograms = [
        #                       histos["fakecrgenprompt"].Clone(),
        #                       histos["fakecrgenfake"].Clone(),
        #                     ]
        #datahist = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_" + category, lumi)
        #datahist.SetTitle("Signal region")
        #makeplot(stacked_histograms, datahist, "fakecrcontamination")
        #
        #stacked_histograms = [
        #                       histos["promptECaloSidebandgenprompt"].Clone(),
        #                       histos["promptECaloSidebandgenfake"].Clone(),
        #                     ]
        #datahist = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_" + category, lumi)
        #datahist.SetTitle("Signal region")
        #makeplot(stacked_histograms, datahist, "promptECaloSidebandcontamination")
        #
        #    
        #stacked_histograms = [
        #                       histos["promptECaloLowgenprompt"].Clone(),
        #                       histos["promptECaloLowgenfake"].Clone(),
        #                     ]
        #datahist = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_" + category, lumi)
        #datahist.SetTitle("Signal region")
        #makeplot(stacked_histograms, datahist, "promptECaloLowcontamination")
    

if __name__ == "__main__":

    print "OK"

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    histograms_folder = "reboot34"
    
    regions = [
                #"QCDLowMHT",
                #"PromptDY",
                #"Baseline",
                "QCDLowMHT50",
                #"QCDLowMHT",
                #"QCDLowMHTJets",
                #"HadBaseline",
                #"SMuBaseline",
                #"SElBaseline",
                #"SMuValidationMT",
                #"SElValidationMT",
                #"SElValidationZLL",
                #"SMuValidationZLL",
                #"PromptDY",
                #"PromptDYenhanced",
                #"QCDLowMHT",
                #"QCDLowMHTJets",
              ]
    
    variables = [
                  "HT",
                  #"MHT",
                  #"n_tags",
                  #"n_goodjets",
                  #"n_btags",
                  #"leadinglepton_mt",
                  #"tracks_invmass",
                  #"tracks_is_pixel_track",
                  #"tracks_pt",
                  #"n_tags",
                  #"tracks_eta",
                  #"tracks_etaHarmonic2pixel",
                  #"tracks_matchedCaloEnergy",
                  #"tracks_trkRelIso",
                  #"tracks_MinDeltaPhiTrackMht",
                  #"tracks_MinDeltaPhiTrackLepton",
                  #"tracks_MinDeltaPhiTrackJets",
                  #"tracks_ptRatioTrackMht",
                  #"tracks_ptRatioTrackLepton",
                  #"tracks_ptRatioTrackJets",
                  #"MinDeltaPhiMhtJets",
                  #"MinDeltaPhiLeptonMht",
                  #"MinDeltaPhiLeptonJets",
                  #"ptRatioMhtJets",
                  #"ptRatioLeptonMht",
                  #"ptRatioLeptonJets",
                  #"tracks_ECaloPt",
                  #"region",
                ]
                  
    categories = [
                  #"",
                  "short",
                  "long",
                 ]

    data_periods = [
                     "Summer16",
                     #"Fall17",
                     "Run2016",
                     #"Run2017",
                     #"Run2018",
                    ]

    outputfolder = histograms_folder + "_plots"

    for region in regions:
        for variable in variables:
            for category in categories:

                print region, variable, category

                if (variable == "tracks_is_pixel_track" or "region" in variable):
                    if category != "":
                        continue

                if category == "" and not (variable == "tracks_is_pixel_track" or "region" in variable):
                    continue

                if category == "" and region != "Baseline":
                    continue

                for data_period in data_periods:

                    lumi = 137000.0
                    #lumi = 35900

                    if "Run201" in data_period:
                        if "SEl" in region or "PromptDY" in region:
                            merged_histograms_file = histograms_folder + "/merged_%sSingleElectron.root" % data_period
                        elif "SMu" in region:
                            merged_histograms_file = histograms_folder + "/merged_%sSingleMuon.root" % data_period
                        elif "QCD" in region:
                            merged_histograms_file = histograms_folder + "/merged_%sJetHT.root" % data_period
                        else:
                            merged_histograms_file = histograms_folder + "/merged_%sMET.root" % data_period
                        if "region" in variable and region == "Baseline":
                            merged_histograms_file = histograms_folder + "/merged_%sAll.root" % data_period
                    elif "Summer16" in data_period:
                        merged_histograms_file = histograms_folder + "/merged_Summer16.root"
                    elif "Fall17" in data_period:
                        merged_histograms_file = histograms_folder + "/merged_Fall17.root"

                    plot_prediction(variable, merged_histograms_file, data_period, category, lumi, region, region + "_" + variable + category, outputfolder)     


    
                        

