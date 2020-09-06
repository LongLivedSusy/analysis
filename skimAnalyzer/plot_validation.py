#!/bin/env python
from __future__ import division
import __main__ as main
from ROOT import *
import collections
import os
import shared_utils
from optparse import OptionParser

color_fakebg = 207
color_promptbg = 216

#flags:
use_prompt_fakesubtraction = True
use_prompt_DeltaPhi = False
use_fakes_DeltaPhi = False

def plot_prediction(variable, root_file, datalabel, category, lumi, region, dedx, pdffile, outputfolder, frregion):

    os.system("mkdir -p " + outputfolder)

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
        else:
            histos[label].Scale(2.5693430654)                               # scale to full Run-2 lumi
            histos[label].SetTitle("Data (2016)")
               
    fin.Close()

    if category == "":
        categories = ["_short", "_long"]
    else:
        categories = [category]
    
    h_fakeprediction = 0
    h_promptprediction = 0
    
    for i_category in categories:

        #################################
        # Fake background               #
        #################################
        
        h_ifakeprediction = histos[dataid + "_fakeprediction-" + frregion + dedx + i_category].Clone()
        h_ifakeprediction.SetTitle("Fake prediction")
                
        #################################
        # prompt background             #
        #################################
        
        # method: EDep sideband
        
        if use_prompt_DeltaPhi:
            h_caloSB = histos[dataid + "_srECSBenhanced" + dedx + i_category]
        else:
            h_caloSB = histos[dataid + "_srECSB" + dedx + i_category]
            
        if "Run201" in datalabel:
            # if running on data: high-low-factor from SingleElectron dataset:
            fin = TFile(root_file.replace("MET", "SingleElectron").replace("SingleMuon", "SingleElectron").replace("JetHT", "SingleElectron"), "read")
            h_DY_low = fin.Get(datalabel + "_" + "tracks_invmass" + "_PromptDY_srEC" + i_category)
            h_DY_high = fin.Get(datalabel + "_" + "tracks_invmass" + "_PromptDY_srECSB" + i_category)
            h_DY_low.SetDirectory(0)
            h_DY_high.SetDirectory(0)
            fin.Close()
        else:
            h_DY_low = histos[datalabel + "_tracks_invmass_PromptDY_srEC" + i_category]
            h_DY_high = histos[datalabel + "_tracks_invmass_PromptDY_srECSB" + i_category]
                
        try:
            ULowHigh = h_DY_low.Integral(h_DY_low.GetXaxis().FindBin(70), h_DY_low.GetXaxis().FindBin(110)) / h_DY_high.Integral(h_DY_high.GetXaxis().FindBin(70), h_DY_high.GetXaxis().FindBin(110))
        except:
            ULowHigh = 0
        
        h_ipromptprediction = h_caloSB.Clone()

        if "regionCorrected" in dataid:
            h_ipromptprediction_multi = histos[dataid + "_srECSB" + dedx + i_category + "_multi"].Clone()
            h_ipromptprediction.Add(h_ipromptprediction_multi)    

        if use_prompt_fakesubtraction:
            # subtract fake background:
            h_ipromptprediction.Add(h_ifakeprediction, -1)            
            
            # check for negative entries:
            for ibin in range(1, h_ipromptprediction.GetXaxis().GetNbins()+1):
                if h_ipromptprediction.GetBinContent(ibin)<0:
                    h_ipromptprediction.SetBinContent(ibin, 0)
        
        h_ipromptprediction.SetDirectory(0)
        h_ipromptprediction.Scale(ULowHigh)
        h_ipromptprediction.SetTitle("Prompt prediction")
    
        # add short and long together:
        if h_fakeprediction == 0:
            h_fakeprediction = h_ifakeprediction
        else:
            h_fakeprediction.Add(h_ifakeprediction)
            
        if h_promptprediction == 0:
            h_promptprediction = h_ipromptprediction
        else:
            h_promptprediction.Add(h_ipromptprediction)
    
    
    ####################
    # plot everything: #
    ####################
    
    if "Run201" in datalabel:
        if "Validation" in region or "LowMHT" in region:
            plots = ["prediction-with-data"]
        else:
            plots = ["prediction-without-data"]
    else:
        #plots = ["prediction-without-data", "prediction-prompt", "prediction-fake", "contamination-truefakes", "contamination-trueprompt"]
        plots = ["prediction-without-data", "prediction-prompt", "prediction-fake"]
        
        
    h_promptprediction.SetLineColor(color_promptbg)
    h_fakeprediction.SetLineColor(color_fakebg)
    h_promptprediction.SetFillColor(color_promptbg)
    h_fakeprediction.SetFillColor(color_fakebg)

    for plot in plots:
    
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
        ymin = 1e-1; ymax = 1e2
        
        if plot == "prediction-with-data":
                    
            stacked_histograms = [
                                   h_fakeprediction.Clone(),
                                   h_promptprediction.Clone(),
                                 ]

            if category == "":
                datahist = histos[dataid + "_sr" + dedx + "_short"]                
                datahist.Add(histos[dataid + "_sr" + dedx + "_long"])                
            else:    
                datahist = histos[dataid + "_sr" + dedx + category]
            datahist.SetLineColor(kBlack)
            datahist.SetTitle("Data")        


        if plot == "mc-with-data":
            
            mcdataid = "Summer16_" + variable + "_" + region
            
            if category == "":
                datahist = histos[dataid + "_sr" + dedx + "_short"]                
                datahist.Add(histos[dataid + "_sr" + dedx + "_long"])                
                stacked_histograms = [
                                       histos[mcdataid + "_srgenfake" + dedx + "_short"].Clone(),
                                       histos[mcdataid + "_srgenfake" + dedx + "_long"].Clone(),
                                       histos[mcdataid + "_srgenprompt" + dedx + "_short"].Clone(),
                                       histos[mcdataid + "_srgenprompt" + dedx + "_long"].Clone(),
                                     ]
            else:    
                datahist = histos[dataid + "_sr" + dedx + category]
                stacked_histograms = [
                                       histos[mcdataid + "_srgenfake" + dedx + category].Clone(),
                                       histos[mcdataid + "_srgenprompt" + dedx + category].Clone(),
                                     ]

            datahist.SetLineColor(kBlack)
            datahist.SetTitle("Data")        
            
            
        elif plot == "prediction-without-data":
            
            stacked_histograms = [
                                   h_fakeprediction.Clone(),
                                   h_promptprediction.Clone(),
                                 ]
        
            datahist = stacked_histograms[0].Clone()
            for stacked_histogram in stacked_histograms[1:]:
                datahist.Add(stacked_histogram.Clone())
            datahist.SetLineColor(kBlack)
            datahist.SetTitle("Added predictions")
            
        
        elif plot == "prediction-with-mctruth":
            
            stacked_histograms = [
                                   h_fakeprediction.Clone(),
                                   h_promptprediction.Clone(),
                                 ]
                                
            if category == "":
                datahist = histos[dataid + "_srgenfake" + dedx + "_short"].Clone()
                datahist.Add(histos[dataid + "_srgenprompt" + dedx + "_short"].Clone())
                datahist.Add(histos[dataid + "_srgenfake" + dedx + "_long"].Clone())
                datahist.Add(histos[dataid + "_srgenprompt" + dedx + "_long"].Clone())
            else:    
                datahist = histos[dataid + "_srgenfake" + dedx + category].Clone()
                datahist.Add(histos[dataid + "_srgenprompt" + dedx + category].Clone())
                datahist.SetLineColor(kBlack)
                datahist.SetTitle("Obs. from MC")
        
        elif plot == "prediction-prompt":
                    
            stacked_histograms = [
                                   #h_fakeprediction.Clone(),
                                   h_promptprediction.Clone(),
                                 ]
        
            if category == "":
                datahist = histos[dataid + "_srgenprompt" + dedx + "_short"].Clone()
                datahist.Add(histos[dataid + "_srgenprompt" + dedx + "_long"].Clone())
            else:
                datahist = histos[dataid + "_srgenprompt" + dedx + category].Clone()

            #datahist.Add(histos[dataid + "_srgenprompt" + dedx + category].Clone())
            datahist.SetLineColor(kBlack)
            datahist.SetTitle("Prompt obs. from MC")
        
        elif plot == "prediction-fake":
                    
            stacked_histograms = [
                                   h_fakeprediction.Clone(),
                                   #h_promptprediction.Clone(),
                                 ]
                            
            if category == "":
                datahist = histos[dataid + "_srgenfake" + dedx + "_short"].Clone()
                datahist.Add(histos[dataid + "_srgenfake" + dedx + "_long"].Clone())
            else:
                datahist = histos[dataid + "_srgenfake" + dedx + category].Clone()
            #datahist.Add(histos[dataid + "_srgenprompt" + dedx + category].Clone())
            datahist.SetLineColor(kBlack)
            datahist.SetTitle("Fake obs. from MC")
            
        elif plot == "contamination-truefakes":
                    
            stacked_histograms = [
                                   histos[dataid + "_srgenfake" + dedx + category].Clone(),
                                   histos[dataid + "_srgenprompt" + dedx + category].Clone(),
                                 ]
                                 
            histos[dataid + "_srgenfake" + dedx + category].SetLineColor(color_fakebg)
            histos[dataid + "_srgenfake" + dedx + category].SetFillColor(color_fakebg)
            histos[dataid + "_srgenprompt" + dedx + category].SetLineColor(color_promptbg)
            histos[dataid + "_srgenprompt" + dedx + category].SetFillColor(color_promptbg)
            
            datahist = histos[dataid + "_srgenfake" + dedx + category].Clone()
            datahist.SetLineColor(kBlack)
            datahist.SetTitle("Fakes (MC Truth)")

        elif plot == "contamination-trueprompt":
                    
            stacked_histograms = [
                                   histos[dataid + "_srgenfake" + dedx + category].Clone(),
                                   histos[dataid + "_srgenprompt" + dedx + category].Clone(),
                                 ]
                                 
            histos[dataid + "_srgenfake" + dedx + category].SetLineColor(color_fakebg)
            histos[dataid + "_srgenfake" + dedx + category].SetFillColor(color_fakebg)
            histos[dataid + "_srgenprompt" + dedx + category].SetLineColor(color_promptbg)
            histos[dataid + "_srgenprompt" + dedx + category].SetFillColor(color_promptbg)
        
            datahist = histos[dataid + "_srgenprompt" + dedx + category].Clone()
            datahist.SetLineColor(kBlack)
            datahist.SetTitle("Prompt (MC Truth)")
        
        
        for i_label, label in enumerate(histos):
            histos[label].GetYaxis().SetRangeUser(ymin, ymax)
        h_promptprediction.GetYaxis().SetRangeUser(ymin, ymax)
        h_fakeprediction.GetYaxis().SetRangeUser(ymin, ymax)    
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
        
        for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
            if hratio.GetBinContent(ibin)==0:
                hratio.SetBinContent(ibin,-999)
        hratio.SetMarkerColor(kBlack)
               
        foldername = outputfolder + "/%s%s" % (category.replace("_short", "Short").replace("_long", "Long"), region)
        if not use_prompt_fakesubtraction:
            foldername += "WithoutSubtraction"
        if use_prompt_DeltaPhi or use_fakes_DeltaPhi:
            foldername += "DeltaPhiEnhanced"

        os.system("mkdir -p " + foldername)

        #canvas.SaveAs(foldername + "/" + pdffile + "_" + plot + ".pdf")
        canvas.SaveAs(foldername + "/" + pdffile + "_" + plot + ".png")

        # write out ROOT file:
        #fout = TFile(foldername + "/" + pdffile + "_" + plot + ".root", "recreate")
        #h_promptprediction.Write()
        #h_fakeprediction.Write()
        #fout.Close()
        
        


def run(index, histograms_folder = ""):
    
    regions = [
                #"Baseline",
                #"QCDLowMHT50",
                "HadBaseline",
                "SMuBaseline",
                "SElBaseline",
                "SMuValidationMT",
                "SElValidationMT",
                "SElValidationZLL",
                "SMuValidationZLL",
                "PromptDY",
                "PromptDYenhanced",
                "QCDLowMHTFakerateDet",
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
                  "tracks_MinDeltaPhiTrackLepton",
                  "tracks_MinDeltaPhiTrackJets",
                  "tracks_ptRatioTrackMht",
                  "tracks_ptRatioTrackLepton",
                  "tracks_ptRatioTrackJets",
                  "MinDeltaPhiMhtJets",
                  "MinDeltaPhiLeptonMht",
                  "MinDeltaPhiLeptonJets",
                  "ptRatioMhtJets",
                  "ptRatioLeptonMht",
                  "ptRatioLeptonJets",
                  "region",
                ]

    dedexids = [
                 #"",
                 "_MidHighDeDx",
                 #"_MidDeDx",
                 #"_HighDeDx",
               ]
                  
    fakerateregions = [
                    "QCDLowMHT2D",
                    #"QCDLowMHT",
                      ]

    categories = [
                  "",
                  "_short",
                  "_long",
                 ]

    data_periods = [
                     "Summer16",
                     "Run2016",
                     #"Run2017",
                     #"Run2018",
                    ]

    outputfolder = histograms_folder + "_plots"

    counter = 0
    for region in regions:
        for variable in variables:
            for category in categories:
                               
                if (variable == "tracks_is_pixel_track" or "region" in variable):
                    if category != "":
                        continue

                if category == "" and not (variable == "tracks_is_pixel_track" or "region" in variable):
                    continue

                if category == "" and region != "Baseline":
                    continue

                for dedx in dedexids:
                    for frregion in fakerateregions:
                        for data_period in data_periods:
                            
                            counter += 1
                            if counter != index: continue
                                
                            #lumi = 35200
                            lumi = 137000
                                                                                       
                            if "Run201" in data_period:
                                if "SEl" in region:
                                    merged_histograms_file = histograms_folder + "/merged_%sSingleElectron.root" % data_period
                                elif "SMu" in region:
                                    merged_histograms_file = histograms_folder + "/merged_%sSingleMuon.root" % data_period
                                elif "QCD" in region:
                                    merged_histograms_file = histograms_folder + "/merged_%sJetHT.root" % data_period
                                else:
                                    merged_histograms_file = histograms_folder + "/merged_%sMET.root" % data_period

                                if "region" in variable and region == "Baseline":
                                    merged_histograms_file = histograms_folder + "/merged_%sAll.root" % data_period

                            else:
                                merged_histograms_file = histograms_folder + "/merged_Summer16.root"

                            plot_prediction(variable, merged_histograms_file, data_period, category, lumi, region, dedx, data_period + "_" + region + dedx + "_" + variable + category + frregion, outputfolder, frregion)     

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
        for i in range(0, run(-1) + 1):
            os.system("./%s --index %s --histograms %s" % (this_scripts_name, i, options.histograms_folder))
            
