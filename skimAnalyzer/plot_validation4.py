#!/bin/env python
from __future__ import division
import __main__ as main
from ROOT import *
import collections
import glob
import os
import shared_utils
from optparse import OptionParser
import time

color_fakebg = 207
color_promptbg = 216

def rebin_histo(histogram, nbins, xmin, xmax):
    h_name = histogram.GetName()
    h_rebinned = TH1F(h_name + "_rebin", h_name + "_rebin", nbins, xmin, xmax)
    for ibin in range(1, histogram.GetXaxis().GetNbins()+1):
        xvalue = histogram.GetBinLowEdge(ibin)
        value = histogram.GetBinContent(ibin)
        valueErr = histogram.GetBinError(ibin)
        h_rebinned.SetBinContent(h_rebinned.GetXaxis().FindBin(xvalue), value)
        h_rebinned.SetBinError(h_rebinned.GetXaxis().FindBin(xvalue), valueErr)
    shared_utils.histoStyler(h_rebinned)
    return h_rebinned


def plot_validation(variable, root_file, datalabel, category, lumi, region, dedx, pdffile, outputfolder, frregion = "QCDLowMHT"):

    os.system("mkdir -p " + outputfolder)
    #if os.path.exists(outputfolder + "/" + pdffile + ".pdf"):
    #    print "ok"
    #    return

    dataid = datalabel + "_" + variable + "_" + region

    # get all histograms from ddbg.root:
    histos = collections.OrderedDict()
    fin = TFile(root_file, "read")
    
    for obj in fin.GetListOfKeys():
        label = obj.ReadObj().GetName()
        if dataid in label or "srEC" in label:
            histos[label] = obj.ReadObj()

    for label in histos.keys():
        histos[label].SetDirectory(0)
        histos[label].SetLineWidth(2)
        shared_utils.histoStyler(histos[label])
        if "Run201" not in label:
            histos[label].Scale(lumi)
    
        # combine short and long tracks:
        if category == "" and "_short" in label and label.replace("_short", "_long") in histos:
            histos[label.replace("_short", "")] = histos[label].Clone()
            histos[label.replace("_short", "")].SetDirectory(0)
            histos[label.replace("_short", "")].Add(histos[label.replace("_short", "_long")])
            
    fin.Close()

    for label in histos:
        if "Run2016" in label:
            easyname = "Data"
            histos[label].SetTitle(easyname)
    
    #################################
    # prompt background             #
    #################################
    
    # method: EDep sideband
    
    h_caloSB = histos[dataid + "_srECSB" + dedx + category]
        
    if "Run201" in datalabel:
        # if running on data: high-low-factor from SingleElectron dataset:
        print "open", root_file.replace("MET", "SingleElectron").replace("SingleMuon", "SingleElectron").replace("JetHT", "SingleElectron")
        fin = TFile(root_file.replace("MET", "SingleElectron").replace("SingleMuon", "SingleElectron").replace("JetHT", "SingleElectron"), "read")
        #h_DY_low = fin.Get(datalabel + "_tracks_invmass_PromptDY_srECSB" + category)
        #h_DY_high = fin.Get(datalabel + "_tracks_invmass_PromptDY_srECSB" + category)
        h_DY_low = fin.Get(datalabel + "_" + "tracks_invmass" + "_PromptDY_srEC" + category)
        h_DY_high = fin.Get(datalabel + "_" + "tracks_invmass" + "_PromptDY_srECSB" + category)
        h_DY_low.SetDirectory(0)
        h_DY_high.SetDirectory(0)
        fin.Close()
    else:
        print "no"
        h_DY_low = histos[datalabel + "_tracks_invmass_PromptDY_srEC" + category]
        h_DY_high = histos[datalabel + "_tracks_invmass_PromptDY_srECSB" + category]
    
    print "h_DY_low.Integral() / h_DY_high.Integral()", h_DY_low.Integral(), "/", h_DY_high.Integral()
    try:
        ULowHigh = h_DY_low.Integral() / h_DY_high.Integral()
    except:
        ULowHigh = 0
    
    h_promptprediction = h_caloSB.Clone()
    h_promptprediction.SetDirectory(0)
    h_promptprediction.Scale(ULowHigh)
    h_promptprediction.SetTitle("Prompt prediction")
    
    
    #################################
    # Fake background               #
    #################################
    
    h_fakeprediction = histos[dataid + "_fakeprediction-" + frregion + dedx + category].Clone()
    h_fakeprediction.SetTitle("Fake prediction")

    #h_fakepredictionLeft = histos[dataid + "_fakeprediction-" + frregion + dedx + category + "Left"].Clone()
    #h_fakepredictionRight = histos[dataid + "_fakeprediction-" + frregion + dedx + category + "Right"].Clone()

    ####################
    # plot everything: #
    ####################
    
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    #legend.SetHeader(region.replace("SMu", "Muon ").replace("SEl", "Electron ").replace("MT", "").replace("Validation", "validation") + " region, " + dedx.replace("_", "").replace("MidHighDeDx", "dE/dx>2.0 MeV/cm").replace("MidDeDx", "2.0>dE/dx>4.0 MeV/cm").replace("HighDeDx", "dE/dx>4.0 MeV/cm"))

    lumi = float("%.2f" % (lumi/1e3))

    ymin = 1e-3; ymax = 1e5
    
    if "Run201" in dataid:
        
        h_promptprediction.SetLineColor(color_promptbg)
        h_fakeprediction.SetLineColor(color_fakebg)
        
        stacked_histograms = [
                               h_fakeprediction.Clone(),
                               #h_promptprediction.Clone(),
                             ]

        if "Validation" in region:
            datahist = histos[dataid + "_sr" + dedx + category]
        else:
            datahist = stacked_histograms[-1]
    else:
        # MC:

        histos[dataid + "_srgenprompt" + dedx + category].SetTitle("MC Truth prompt")
        histos[dataid + "_srgenprompt" + dedx + category].SetFillColor(color_promptbg)
        
        histos[dataid + "_srgenfake" + dedx + category].SetTitle("MC Truth fake")
        histos[dataid + "_srgenfake" + dedx + category].SetFillColor(color_fakebg)
        
        stacked_histograms = [
                               histos[dataid + "_srgenfake" + dedx + category].Clone(),
                               histos[dataid + "_srgenprompt" + dedx + category].Clone(),
                             ]
        
        datahist = h_fakeprediction
    

    for i_label, label in enumerate(histos):
        histos[label].GetYaxis().SetRangeUser(ymin, ymax)
    
    for ihisto in stacked_histograms:
        ihisto.GetYaxis().SetRangeUser(ymin, ymax)
    datahist.GetYaxis().SetRangeUser(ymin, ymax)
    
    for stacked_histogram in stacked_histograms:
        stacked_histogram.GetYaxis().SetRangeUser(ymin, ymax)
        stacked_histogram.GetYaxis().SetLimits(ymin, ymax)

    #hratio, pads = shared_utils.FabDraw(canvas, legend, datahist, stacked_histograms, ymin, ymax, lumi = lumi, datamc = 'Data')
    hratio, pads = shared_utils.FabDraw(canvas, legend, datahist, stacked_histograms, datamc = 'Data')
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

    ## add fake CR:
    #histos[dataid + "_fakecr" + dedx + category].SetLineColor(kTeal)
    #histos[dataid + "_fakecr" + dedx + category].Draw("same")
    #legend.AddEntry(histos[dataid + "_fakecr" + dedx + category], "Fake CR")
    
    ## add systematics:
    #h_fakepredictionLeft.SetLineColor(kTeal)
    #h_fakepredictionLeft.Draw("same")
    #h_fakepredictionRight.SetLineColor(kTeal)
    #h_fakepredictionRight.Draw("same")
    
    # recalculate ratio: FR pred / FR Truth
    if not "Run201" in dataid:
        
        # MC:
        hratio.GetYaxis().SetTitle('Fake pred./genFake')
        new_ratio = h_fakeprediction.Clone()
        new_ratio.Divide(histos[dataid + "_srgenfake" + dedx + category])
        for ibin in range(1, hratio.GetXaxis().GetNbins()+1):
            hratio.SetBinContent(ibin, new_ratio.GetBinContent(ibin))
            hratio.SetBinError(ibin, new_ratio.GetBinError(ibin))

    else:
        
        # Data:
        pads[1].cd()
                
        #fullpredictionLeft = h_fakepredictionLeft.Clone()
        #fullpredictionLeft.Add(h_promptprediction)        
        #new_ratioLeft = histos[dataid + "_sr" + dedx + category].Clone()
        #new_ratioLeft.Divide(fullpredictionLeft)
        #new_ratioLeft.SetLineColor(kTeal)
        #new_ratioLeft.SetMarkerSize(0)
        #new_ratioLeft.Draw("same")
        #
        #fullpredictionRight = h_fakepredictionRight.Clone()
        #fullpredictionRight.Add(h_promptprediction)        
        #new_ratioRight = histos[dataid + "_sr" + dedx + category].Clone()
        #new_ratioRight.Divide(fullpredictionRight)
        #new_ratioRight.SetLineColor(kTeal)
        #new_ratioRight.SetMarkerSize(0)
        #new_ratioRight.Draw("same")
        
        
    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)

    canvas.SaveAs(outputfolder + "/" + pdffile + ".pdf")


def run(index, histograms_folder = ""):
    
    #regions = ["SElValidationMT", "SMuValidationMT" ]#, "HadBaseline", "SMuBaseline", "SElBaseline"]
    #regions = ["HadBaseline", "SMuBaseline", "SElBaseline", "SMuValidationMT", "SElValidationMT"]#, "SElValidationMT" "Baseline", "HadBaseline", "SMuBaseline", "SElBaseline"]
    regions = [
                "SMuValidationMT",
                "SElValidationMT",
              ]
    
    variables = [
                 ##"regionCorrected",
                 #"HT",
                 #"MHT",
                 #"n_goodjets",
                 ##"n_btags",
                 #"leadinglepton_mt",
                 "tracks_invmass",
                 ##"tracks_is_pixel_track",
                 ##"tracks_pt",
                 ##"tracks_eta",
                 ##"tracks_deDxHarmonic2pixelCorrected",
                 ##"tracks_matchedCaloEnergy",
                 ##"tracks_trkRelIso",
                ]
    dedexids = [""] # _MidHighDeDx "_MidDeDx", "_HighDeDx"
    fakerateregions = ["QCDLowHT"] #,"QCDLowMHTSimple", "QCDLowMHTHT"] 
    #fakerateregions = ["QCDLowMHT"]
    categories = ["_short", "_long"]

    data_periods = [
                     "Run2016",
                     #"Run2017",
                     #"Run2018",
                    ]

    outputfolder = histograms_folder + "_plots"

    counter = 0
    for region in regions:

        if "Validation" in region:
            use_data_list = [True]
        else:
            use_data_list = [False]

        for use_data in use_data_list:
            for variable in variables:
                for category in categories:
                    for dedx in dedexids:
                        for frregion in fakerateregions:
                            for data_period in data_periods:
                                if category == "" and variable != "tracks_is_pixel_track":
                                    continue
                                if category != "" and variable == "tracks_is_pixel_track":
                                    continue
                                if "region" in variable and region != "Baseline":
                                    continue
                                
                                counter += 1
                                if counter != index: continue
                                
                                #if not use_data:
                                #    plot_validation(variable, histograms_folder + "/FILE", "Summer16", category, 36000, region, dedx, "Summer16_" + region + dedx + "_" + variable + category + frregion, outputfolder, frregion = frregion)
                                #    #if "SMu" not in region and "SEl" not in region:
                                #    #    plot_validation(variable, histograms_file, "Summer16QCDZJets", category, 36000, region, dedx, "Summer16QCDZJets_" + region + dedx + "_" + variable + category + frregion, outputfolder, frregion = frregion)
                                #
                                #if "region" in variable:
                                #    plot_validation(variable, histograms_folder + "/FILE", "Run2016", category, 35000, region, dedx, "Run2016_" + region + dedx + "_" + variable + category + frregion, outputfolder, frregion = frregion)
                                #
                                #if "SElValidation" in region and use_data:
                                #    #lumi = lumis["Run2016_SingleElectron"] * 1e3
                                #    lumi = 34330
                                #    plot_validation(variable, histograms_folder + "/FILE", "Run2016SingleElectron", category, lumi, region, dedx, "Run2016SingleElectron_" + region + dedx + "_" + variable + category + frregion, outputfolder, frregion = frregion)
                                                            
                                if "SMuValidation" in region and use_data:
                                    #lumi = lumis["Run2016_SingleMuon"] * 1e3
                                    lumi = 35200
                                    plot_validation(variable, histograms_folder + "/merged_%sSingleMuon.root" % data_period, data_period, category, lumi, region, dedx, data_period + "_" + region + dedx + "_" + variable + category + frregion, outputfolder, frregion = frregion)     

                                elif "SElValidation" in region and use_data:
                                    #lumi = lumis["Run2016_SingleMuon"] * 1e3
                                    lumi = 35200
                                    plot_validation(variable, histograms_folder + "/merged_%sSingleElectron.root" % data_period, data_period, category, lumi, region, dedx, data_period + "_" + region + dedx + "_" + variable + category + frregion, outputfolder, frregion = frregion)     

    return counter
    
                        
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index")
    parser.add_option("--histograms", dest = "histograms_folder")
    (options, args) = parser.parse_args()

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    this_scripts_name = main.__file__

    if options.index:
        run(int(options.index), histograms_folder = options.histograms_folder)
    else:
        for i in range(0, run(-1)+1):
            os.system("./%s --index %s --histograms %s" % (this_scripts_name, i, options.histograms_folder))
            