#!/bin/env python
from __future__ import division
import __main__ as main
from ROOT import *
import collections
import os
import shared_utils
from optparse import OptionParser
import glob

color_fakebg = kSpring - 1
color_promptbg = kAzure + 1

def get_histo(root_file, label, lumi = False, title = False, color = False):
    
    if "_combined" in label:
        h_combined = get_histo(root_file, label.replace("_combined", "_short"), lumi = lumi, title = title, color = color)
        h_long = get_histo(root_file, label.replace("_combined", "_long"), lumi = lumi, title = title, color = color)
        h_combined.Add(h_long)
        return h_combined
        
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


def plot_prediction(variable, root_file, datalabel, category, lumi, region, pdffile, outputfolder, fakeratevariable, use_prompt_fakesubtraction):

    os.system("mkdir -p " + outputfolder)
    dataid = datalabel + "_" + variable + "_" + region
    
    histos = collections.OrderedDict()
   
    h_fakeprediction = 0
    h_promptprediction = 0
    
    ###############################
    # get predictions and geninfo #
    ###############################
    
    histos["fakeprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakeprediction_" + fakeratevariable + "_" + category, lumi, "Fake prediction", color_fakebg)
    histos["promptprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptprediction_tracks_pt_" + category, lumi, "Prompt prediction", color_promptbg)
    h_fake_contribution = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptRegionCkappa_" + fakeratevariable + "_" + category, lumi, "Prompt prediction", color_promptbg)
    h_fake_contribution_srgenprompt = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptRegionCkappa_" + fakeratevariable + "_genprompt_" + category, lumi, "Prompt prediction", color_promptbg)
    h_fake_contribution_srgenfake = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptRegionCkappa_" + fakeratevariable + "_genfake_" + category, lumi, "Prompt prediction", color_promptbg)
    
    if use_prompt_fakesubtraction:
        histos["promptprediction"].Add(h_fake_contribution, -1)
    
    if "Run201" not in datalabel:
        histos["srgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_genfake_" + category, lumi, "non-prompt MC Truth", color_fakebg)
        histos["srgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_genprompt_" + category, lumi, "prompt MC Truth", color_promptbg)
        histos["fakecrgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakecr_genfake_" + category, lumi, "non-prompt MC Truth", color_fakebg)
        histos["fakecrgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakecr_genprompt_" + category, lumi, "prompt MC Truth", color_promptbg)
        histos["promptcrgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloSideband_genfake_" + category, lumi, "non-prompt MC Truth", color_fakebg)
        histos["promptcrgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloSideband_genprompt_" + category, lumi, "prompt MC Truth", color_promptbg)    
        
        if use_prompt_fakesubtraction:
            histos["promptcrgenfake"].Add(h_fake_contribution_srgenfake, -1)
            histos["promptcrgenprompt"].Add(h_fake_contribution_srgenprompt, -1)
        

    def makeplot(stacked_histograms, datahist, plotlabel, ratiovalues = False, ratiolabel = False, ratio_limits = False, header = False):

        foldername = outputfolder + "/%s/%s%s%s_%sFR" % (data_period, category.replace("short", "Short").replace("long", "Long"), region, plotlabel, fakeratevariable.replace("_", "").replace(":", "-"))

        if use_prompt_fakesubtraction:
            foldername += "_FakeSubtraction"
        
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
        
        if header:
            legend.SetHeader(header)
        else:
            legend.SetHeader("%s, %s tracks" % (region, category))
    
        ymin = 1e0; ymax = 1e2
        datahist.GetYaxis().SetRangeUser(ymin, ymax)
        for stacked_histogram in stacked_histograms:
            stacked_histogram.GetYaxis().SetRangeUser(ymin, ymax)
            stacked_histogram.GetYaxis().SetLimits(ymin, ymax)
    
        hratio, pads = shared_utils.FabDraw(canvas, legend, datahist, stacked_histograms, datamc = 'Data', lumi = lumi/1e3)
        stacked_histograms[-1].SetTitle("")
        
        if ratio_limits:
            hratio.GetYaxis().SetRangeUser(ratio_limits[0], ratio_limits[1])
        else:
            hratio.GetYaxis().SetRangeUser(-0.1,2.6)
        
        if "Run201" in dataid:
            hratio.GetYaxis().SetTitle('Data/prediction')
        else:
            hratio.GetYaxis().SetTitle('Fake pred./truth')
            
        if ratiolabel:
            hratio.GetYaxis().SetTitle(ratiolabel)
        
        xlabel = variable
        xlabel = xlabel.replace("leptons_mt", "m_{T}^{lepton} (GeV)")
        xlabel = xlabel.replace("leadinglepton_mt", "m_{T}^{lepton} (GeV)")
        hratio.GetXaxis().SetTitle(xlabel)
    
        for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
            if ratiovalues:
                hratio.SetBinContent(ibin, ratiovalues.GetBinContent(ibin))
            else:
                if hratio.GetBinContent(ibin)==0:
                    hratio.SetBinContent(ibin,-999)
        hratio.SetMarkerColor(kBlack)
        
        os.system("mkdir -p " + foldername)
        canvas.SaveAs(foldername + "/" + pdffile + ".png")
        #canvas.SaveAs(foldername + "/" + pdffile + ".pdf")
                
    # predictions vs. data:
    
    if histos["promptprediction"].Integral() > histos["fakeprediction"].Integral():
        stacked_histograms = [
                           histos["fakeprediction"].Clone(),
                           histos["promptprediction"].Clone(),
                             ]
    else:
        stacked_histograms = [
                           histos["promptprediction"].Clone(),
                           histos["fakeprediction"].Clone(),
                             ]
                         
    if "Validation" in region or "QCD" in region:
        datahist = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_" + category)
        datahist.SetTitle("Signal region")
        makeplot(stacked_histograms, datahist, "")
    else:
        datahist = histos["promptprediction"]
        datahist.Add(histos["fakeprediction"])
        datahist.SetTitle("Added predictions")
        makeplot(stacked_histograms, datahist, "")
            
        
    if "Run201" not in datalabel:
        # genfake vs fakepred, genprompt vs promptpred, all gen vs. all pred:
        if histos["promptprediction"].Integral() > histos["fakeprediction"].Integral():
            stacked_histograms = [
                                   histos["srgenfake"].Clone(),
                                   histos["srgenprompt"].Clone(),
                                 ]
        else:
            stacked_histograms = [
                                   histos["srgenprompt"].Clone(),
                                   histos["srgenfake"].Clone(),
                                 ]
        datahist = histos["srgenprompt"]
        datahist.Add(histos["srgenfake"])
        datahist.SetTitle("Added predictions")
        makeplot(stacked_histograms, datahist, "MCSignal")
        
        # fake cr MC Truth:
        stacked_histograms = [
                               histos["fakecrgenprompt"].Clone(),
                               histos["fakecrgenfake"].Clone(),
                             ]
        datahist = histos["fakecrgenprompt"].Clone()
        datahist.Add(histos["fakecrgenfake"].Clone())
        datahist.SetTitle("Prompt+Fake MC Truth")
        h_sum = histos["fakecrgenprompt"].Clone()
        h_sum.Add(histos["fakecrgenfake"].Clone())
        h_ratio = histos["fakecrgenprompt"].Clone()
        h_ratio.Divide(h_sum)
        makeplot(stacked_histograms, datahist, "MCFakeCR", ratiovalues = h_ratio, ratiolabel = "Prompt cont. (%)", ratio_limits = (-0.01, 1.01), header = "Fake control region")
        
        # prompt cr MC Truth:
        stacked_histograms = [
                               histos["promptcrgenfake"].Clone(),
                               histos["promptcrgenprompt"].Clone(),
                             ]
        datahist = histos["promptcrgenprompt"].Clone()
        datahist.Add(histos["promptcrgenfake"].Clone())
        datahist.SetTitle("Prompt+Fake MC Truth")
        h_sum = histos["promptcrgenprompt"].Clone()
        h_sum.Add(histos["promptcrgenfake"].Clone())
        h_ratio = histos["promptcrgenfake"].Clone()
        h_ratio.Divide(h_sum)
        makeplot(stacked_histograms, datahist, "MCpromptcr", ratiovalues = h_ratio, ratiolabel = "Fake cont. (%)", ratio_limits = (-0.01, 1.01), header = "Prompt control region")

        # closure:
        stacked_histograms = [
                               histos["promptprediction"].Clone(),
                               histos["fakeprediction"].Clone(),
                             ]
        datahist = histos["srgenprompt"]
        datahist.Add(histos["srgenfake"])
        datahist.SetTitle("Prompt+Fake MC Truth")
        makeplot(stacked_histograms, datahist, "Closure")

        # prompt closure:
        stacked_histograms = [
                               histos["promptprediction"].Clone(),
                             ]
        datahist = histos["srgenprompt"]
        datahist.SetTitle("Prompt MC Truth")
        makeplot(stacked_histograms, datahist, "PromptClosure")
        
        # fake closure:
        stacked_histograms = [
                               histos["fakeprediction"].Clone(),
                             ]
        datahist = histos["srgenfake"]
        datahist.SetTitle("Non-prompt MC Truth")
        makeplot(stacked_histograms, datahist, "FakeClosure")
    

if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    if len(args)>0:
        histograms_folder = args[0]
    else:
        print "Usage: ./plot_validation.py <folder>"
        quit()
        
    regions = [
                #"QCDLowMHT",
                #"PromptDY",
                "Baseline",
                #"QCDLowMHT",
                #"QCDLowMHT",
                #"QCDLowMHTJets",
                #"QCDLowMHT50",
                "HadBaseline",
                "SMuBaseline",
                "SElBaseline",
                #"QCDLowMHT",
                #"QCDLowMHTJet",
                #"QCDLowMHTValidation",
                "QCDLowMHTVal",
                "SMuValidationLowMT",
                "SElValidationLowMT",
                "SElValidationHighMT",
                "SMuValidationHighMT",                
                #"SElValidationZLL",
                #"SMuValidationZLL",
                #"PromptDY",
                #"PromptDYenhanced",
                #"QCDLowMHT",
                #"QCDLowMHTJets",
              ]
    
    variables = [
                "HT",
                "MHT",
                "n_goodjets",
                "n_btags",
                "leadinglepton_mt",
                "tracks_invmass",
                "tracks_is_pixel_track",
                "tracks_pt",
                "tracks_eta",
                "tracks_deDxHarmonic2pixel",
                "tracks_matchedCaloEnergy",
                "tracks_trkRelIso",
                "tracks_MinDeltaPhiTrackMht",
                "tracks_ptRatioTrackMht",
                "n_tags",
                "region",
                ]
                  
    categories = [
                "combined",
                "short",
                "long",
                 ]
                 
    fakeratevariables = [
                              "HT",
                              #"HT:n_allvertices",
                            ]

    # check data period:
    data_periods = []
    merged_files = glob.glob(histograms_folder + "/merged_*.root")
    for merged_file in merged_files:
        if "All" in merged_file: continue
        for period in [
                        #"Summer16",
                        "Fall17",
                        "Run2016",
                        "Run2017",
                        "Run2018"
                       ]:
            if period in merged_file and period not in data_periods:
                    data_periods.append(period)
                    print "Looking at %s" % period

    outputfolder = histograms_folder + "_plots"

    for fakeratevariable in fakeratevariables:
        for use_prompt_fakesubtraction in [
                                            False,
                                            True,
                                           ]:
            for region in regions:
                for variable in variables:
                    for category in categories:

                        if variable == "region":
                            if category is not "combined": continue
                            
                        print region, variable, category
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
            
                            plot_prediction(variable, merged_histograms_file, data_period, category, lumi, region, region + "_" + variable + "_" + category, outputfolder, fakeratevariable, use_prompt_fakesubtraction)     


    
                        

