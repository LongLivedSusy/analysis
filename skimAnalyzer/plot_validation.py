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

def get_histo(root_file, label, lumi = False, title = False, color = False):
    
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
    if use_prompt_fakesubtraction:
        #histos["promptprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptpredictionsubtracted_" + category, lumi, "Prompt prediction", color_promptbg)
        histos["promptprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptprediction_tracks_pt_" + category, lumi, "Prompt prediction", color_promptbg)
        h_fake_ccontribution = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptRegionCkappa_" + fakeratevariable + "_" + category, lumi, "Prompt prediction", color_promptbg)
        histos["promptprediction"].Add(h_fake_ccontribution, -1)

    else:
        histos["promptprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptprediction_tracks_pt_" + category, lumi, "Prompt prediction", color_promptbg)
    
    if "Run201" not in datalabel:
        histos["srgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_srgenfake_" + category, lumi, "MC fakes", color_fakebg)
        histos["srgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_srgenprompt_" + category, lumi, "MC prompt", color_promptbg)
        histos["fakecrgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakecrgenfake_" + category, lumi, "MC fakes", color_fakebg)
        histos["fakecrgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakecrgenprompt_" + category, lumi, "MC prompt", color_promptbg)
        #histos["promptECaloLowgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloLowgenfake_" + category, lumi, "MC fakes", color_fakebg)
        #histos["promptECaloLowgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloLowgenprompt_" + category, lumi, "MC prompt", color_promptbg)
        histos["promptECaloSidebandgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloSidebandgenfake_" + category, lumi, "MC fakes", color_fakebg)
        histos["promptECaloSidebandgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloSidebandgenprompt_" + category, lumi, "MC prompt", color_promptbg)    
        
    def makeplot(stacked_histograms, datahist, plotlabel):

        foldername = outputfolder + "/%s/%s%s%s_%sFR" % (data_period, category.replace("short", "Short").replace("long", "Long"), region, plotlabel, fakeratevariable.replace("_", "").replace(":", "-"))

        if use_prompt_fakesubtraction:
            foldername += "_FakeSubtraction"
        
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
        
        legend.SetHeader("%s, %s tracks" % (region, category))
    
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
        
        ## add prompt and fake MC truth ratios:
        #if plotlabel == "mctruthsr":
        #    h_fakepred_ratio = histos["fakeprediction"].Clone()
        #    h_fakepred_ratio.Divide(histos["srgenfake"].Clone())
        #    h_promptpred_ratio = histos["promptprediction"].Clone()
        #    h_promptpred_ratio.Divide(histos["srgenprompt"].Clone())
        #    pads[1].cd()
        #    h_promptpred_ratio.Draw("hist same")
        #    h_promptpred_ratio.SetFillColor(0)
        #    h_fakepred_ratio.Draw("hist same")
        #    h_fakepred_ratio.SetFillColor(0)
        #
        #elif plotlabel == "mctruthfakecr":
        #    h_fakecrgenfake = histos["fakecrgenfake"].Clone()
        #    h_fakecrgenprompt = histos["fakecrgenprompt"].Clone()
        #    pads[0].cd()
        #    h_fakecrgenfake.Draw("hist same")
        #    h_fakecrgenfake.SetFillColor(0)
        #    h_fakecrgenprompt.Draw("hist same")
        #    h_fakecrgenprompt.SetFillColor(0)
    
        for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
            if hratio.GetBinContent(ibin)==0:
                hratio.SetBinContent(ibin,-999)
        hratio.SetMarkerColor(kBlack)
           
        os.system("mkdir -p " + foldername)
        canvas.SaveAs(foldername + "/" + pdffile + ".png")
        #canvas.SaveAs(foldername + "/" + pdffile + ".pdf")
                
    # predictions vs. data:
    stacked_histograms = [
                           histos["promptprediction"].Clone(),
                           histos["fakeprediction"].Clone(),
                         ]
                         
    if "Validation" in region or "QCD" in region:
        datahist = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_" + category)
        datahist.SetTitle("Signal region")
    else:
        datahist = histos["promptprediction"]
        datahist.Add(histos["fakeprediction"])
        datahist.SetTitle("Added predictions")
    makeplot(stacked_histograms, datahist, "")
            
        
    if "Run201" not in datalabel:
        ## genfake vs fakepred, genprompt vs promptpred, all gen vs. all pred:
        #stacked_histograms = [
        #                       histos["srgenprompt"].Clone(),
        #                       histos["srgenfake"].Clone(),
        #                     ]
        #datahist = histos["srgenprompt"]
        #datahist.Add(histos["srgenfake"])
        #datahist.SetTitle("Added predictions")
        #makeplot(stacked_histograms, datahist, "MCTruthSR")
        
        ## fake cr MC Truth:
        #stacked_histograms = [
        #                       histos["fakecrgenprompt"].Clone(),
        #                       histos["fakecrgenfake"].Clone(),
        #                     ]
        #datahist = histos["fakecrgenprompt"]
        #datahist.Add(histos["fakecrgenfake"])
        #datahist.SetTitle("Prompt+Fake MC Truth")
        #makeplot(stacked_histograms, datahist, "FakeCR")
        #
        ## fake cr MC Truth:
        #stacked_histograms = [
        #                       histos["promptECaloSidebandgenprompt"].Clone(),
        #                       histos["promptECaloSidebandgenfake"].Clone(),
        #                     ]
        #datahist = histos["promptECaloSidebandgenprompt"]
        #datahist.Add(histos["promptECaloSidebandgenfake"])
        #datahist.SetTitle("Prompt+Fake MC Truth")
        #makeplot(stacked_histograms, datahist, "PromptCR")

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
    
    use_prompt_fakesubtraction = True

    fakeratevariable = "HT"
    #fakeratevariable = "HT:n_allvertices"
    
    regions = [
                #"QCDLowMHT",
                #"PromptDY",
                #"Baseline",
                #"QCDLowMHT",
                #"QCDLowMHTJets",
                #"QCDLowMHT50",
                #"HadBaseline",
                #"SMuBaseline",
                #"SElBaseline",
                "QCDLowMHTValidation",
                "SMuValidationMT",
                "SElValidationMT",
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
                  #"HT",
                  #"MHT",
                  #"n_tags",
                  #"n_goodjets",
                  #"n_btags",
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
                  #"tracks_is_pixel_track",
                  #"tracks_pt",
                  #"n_tags",
                  #"tracks_eta",
                  #"tracks_deDxHarmonic2pixel",
                  #"tracks_matchedCaloEnergy",
                  #"tracks_trkRelIso",
                  #"tracks_MinDeltaPhiTrackMht",
                  #"tracks_ptRatioTrackMht",
                  #"tracks_MinDeltaPhiTrackLepton",
                  #"tracks_MinDeltaPhiTrackJets",
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
                     #"Summer16",
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


    
                        

