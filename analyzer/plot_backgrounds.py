#!/bin/env python
from __future__ import division
from ROOT import *
import collections
import glob
import os
import shared_utils
from optparse import OptionParser
import time

def plot_validation(plottype, variable, root_file, datalabel, category, lumi, region, dedx, pdffile, use_iso = False):
    
    dataid = variable + "_" + region + "_" + datalabel
    
    # get all histograms from ddbg.root:
    histos = collections.OrderedDict()
    fin = TFile(root_file, "read")
    
    for obj in fin.GetListOfKeys():
        label = obj.ReadObj().GetName()
        histos[label] = obj.ReadObj()

    for label in histos.keys():
        histos[label].SetDirectory(0)
        histos[label].SetLineWidth(2)

        if "Run201" not in label:
            histos[label].Scale(lumi)
        shared_utils.histoStyler(histos[label])

        # combine short and long tracks:
        if category == "" and "_short" in label and label.replace("_short", "_long") in histos:
            histos[label.replace("_short", "")] = histos[label].Clone()
            histos[label.replace("_short", "")].SetDirectory(0)
            histos[label.replace("_short", "")].Add(histos[label.replace("_short", "_long")])

    fin.Close()

    for label in histos:
        easyname = label.replace(dataid, "Data")
        easyname = easyname.replace("_", " ")
        easyname = easyname.replace("sr", "SR")
        histos[label].SetTitle(easyname)
    
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    legend.SetHeader(region + " " + dedx)
    colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]

    color_fakebg = 207
    color_promptbg = 216

    #################################
    # prompt background             #
    #################################
    
    # ABCD method to get prompt contribution in SR:
    # ________ _________ __________ 
    #         |         |          |
    #  1 DT   |    A    |    C     |
    # ________|_________|__________|
    #         |         |          |      ABCD method: C = D     * A / B
    #  1 el   |    B    |    D     |                       shape * scale
    # ________|_________|__________|
    #         |         |          |      shape from CR, scale from sideband
    #         | lowDeDx | highDeDx |
    #         |         |          |

    # first, subtract fake background from low-dE/dx sideband DT region (A):
    histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category] = histos[dataid + "_sr_SidebandDeDx" + category].Clone()
    if not use_iso:
        histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Add(histos[dataid + "_fakeprediction_SidebandDeDx" + category], -1)
    else:
        histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Add(histos[dataid + "_fakepredictionIsoMVA_SidebandDeDx" + category], -1)

    # do C = D * A / B
    histos[dataid + "_promptprediction" + dedx + category] = histos[dataid + "_promptEl" + dedx].Clone()
    histos[dataid + "_promptprediction" + dedx + category].Multiply(histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category])
    prompt_scale = histos[dataid + "_promptprediction" + dedx + category].Clone()
    histos[dataid + "_promptprediction" + dedx + category].Divide(histos[dataid + "_promptEl_SidebandDeDx" + category])
    
    histos[dataid + "_promptprediction" + dedx + category].SetFillColor(color_promptbg)
    histos[dataid + "_promptprediction" + dedx + category].SetTitle("Prompt prediction")

    #################################
    # Fake background               #
    #################################
    if not use_iso:
        histos[dataid + "_fakeprediction" + dedx + category].SetTitle("Fake prediction")
    else:
        histos[dataid + "_fakepredictionIsoMVA" + dedx + category].SetTitle("Fake prediction")


    ######################
    # Plot               #
    ######################

    lumi = float("%.2f" % (lumi/1e3))

    if "ValidationMT" in region and variable == "leadinglepton_mt":
        ymin = 1e2; ymax = 1e6
    elif "ValidationMT" in region and variable == "tracks_invmass":
        ymin = 1e-1; ymax = 5e3
    elif "ValidationZLL" in region and variable == "leadinglepton_mt":
        ymin = 1e-4; ymax = 1e4
    elif "ValidationZLL" in region and variable == "tracks_invmass":
        ymin = 5e-2; ymax = 5e3
    elif "SElBaseline" in region and variable == "HT":
        ymin = 1e-5; ymax = 1e3
    elif "SElBaseline" in region and variable == "MHT":
        ymin = 1e-5; ymax = 1e5
    elif "SMuBaseline" in region and variable == "HT":
        ymin = 1e-5; ymax = 1e3
    elif "SMuBaseline" in region and variable == "MHT":
        ymin = 1e-5; ymax = 1e5
    elif "Baseline" in region and variable == "HT":
        ymin = 1e0; ymax = 1e9
    elif "Baseline" in region and variable == "MHT":
        ymin = 1e-5; ymax = 1e8
    elif "Baseline" in region:
        ymin = 5e-8; ymax = 5e5
    else:
        ymin = 5e1; ymax = 2e4

    if plottype == "validation":
        
        ##################################
        # Do validation plot             #
        ##################################

        if not use_iso:
            histos[dataid + "_fakeprediction" + dedx + category].SetFillColor(color_fakebg)
            stacked_histograms = [
                                   histos[dataid + "_promptprediction" + dedx + category],
                                   histos[dataid + "_fakeprediction" + dedx + category],
                                 ]
        else:
            histos[dataid + "_fakepredictionIsoMVA" + dedx + category].SetFillColor(color_fakebg)
            stacked_histograms = [
                                   histos[dataid + "_promptprediction" + dedx + category],
                                   histos[dataid + "_fakepredictionIsoMVA" + dedx + category],
                                 ]

        # signal region is blinded
        if "Validation" in region:
            datahist = histos[dataid + "_sr" + dedx + category]
        else:
            datahist = stacked_histograms[-1]

        for i_label, label in enumerate(histos):
            histos[label].GetYaxis().SetRangeUser(ymin, ymax)
        
        for stacked_histogram in stacked_histograms:
            stacked_histogram.GetYaxis().SetRangeUser(ymin, ymax)
            stacked_histogram.GetYaxis().SetLimits(ymin, ymax)
        
        #print stacked_histograms[0].GetBinContent(1), stacked_histograms[1].GetBinContent(1), stacked_histograms[1].GetBinContent(2)        
        
        hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, datahist, stacked_histograms, lumi = lumi, datamc = 'Data')
        #stacked_histograms[-1].SetTitle("")
        
        #print stacked_histograms[0].GetBinContent(1), stacked_histograms[1].GetBinContent(1), stacked_histograms[1].GetBinContent(2)    
        
        hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
        hratio.GetYaxis().SetTitle('Data/prediction')

        xlabel = variable
        xlabel = xlabel.replace("leptons_mt", "m_{T}^{lepton} (GeV)")
        xlabel = xlabel.replace("leadinglepton_mt", "m_{T}^{lepton} (GeV)")
        hratio.GetXaxis().SetTitle(xlabel)

        # add fake CR:
        if not use_iso:
            histos[dataid + "_fakecr" + dedx + category].SetLineColor(kTeal)
            histos[dataid + "_fakecr" + dedx + category].Draw("same")
            legend.AddEntry(histos[dataid + "_fakecr" + dedx + category], "Fake CR")
        else:
            histos[dataid + "_fakecrIsoMVA" + dedx + category].SetLineColor(kTeal)
            histos[dataid + "_fakecrIsoMVA" + dedx + category].Draw("same")
            legend.AddEntry(histos[dataid + "_fakecrIsoMVA" + dedx + category], "Fake CR")

        ## add prompt CR:
        #prompt_scale.SetLineColor(kTeal+2)
        #prompt_scale.Draw("same")
        #legend.AddEntry(prompt_scale, "Prompt bg. scale")

        #if not datalabel:
        #    # add MC Truth info:
        #    histos[dataid + "_srgenfake" + dedx + category].SetLineColor(kRed)
        #    histos[dataid + "_srgenfake" + dedx + category].Draw("same")
        #    legend.AddEntry(histos[dataid + "_srgenfake" + dedx + category], "Genfakes")
        #    
        #    histos[dataid + "_srgenprompt" + dedx + category].SetLineColor(kOrange)
        #    histos[dataid + "_srgenprompt" + dedx + category].Draw("same")
        #    legend.AddEntry(histos[dataid + "_srgenprompt" + dedx + category], "Genprompt")
        
        for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
            if hratio.GetBinContent(ibin)==0:
                hratio.SetBinContent(ibin,-999)
        hratio.SetMarkerColor(kBlack)

        if use_iso:
            canvas.SaveAs("validation/validation_" + pdffile + "_isoMVA.pdf")
        else:
            canvas.SaveAs("validation/validation_" + pdffile + ".pdf")

    if plottype == "fakeclosure" or plottype == "promptclosure":

        ##########################
        # Do closure plot        #
        ##########################

        if variable == "MHT":
            xmin = 0
            xmax = 400
        else:
            xmin = False
            xmax = False

        histos[dataid + "_srgenprompt" + dedx + category].SetFillColor(color_promptbg)
        histos[dataid + "_srgenprompt" + dedx + category].SetTitle("Prompt background SR (MC Truth)")
        histos[dataid + "_srgenfake" + dedx + category].SetFillColor(color_fakebg)
        histos[dataid + "_srgenfake" + dedx + category].SetTitle("Fake background SR (MC Truth)")

        stacked_histograms = [
                               histos[dataid + "_srgenfake" + dedx + category],
                               histos[dataid + "_srgenprompt" + dedx + category],
                             ]

        #histos["combined_truth"] = histos[dataid + "_srgenprompt" + dedx + category].Clone()
        #histos["combined_truth"].Add(histos[dataid + "_srgenfake" + dedx + category])
        #histos["combined_truth"].SetTitle("MC Truth everything")

        #hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histos["combined_truth"], stacked_histograms, lumi = lumi, datamc = 'Data')
        if plottype == "fakeclosure":
            hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histos[dataid + "_srgenfake" + dedx + category], stacked_histograms, lumi = lumi, datamc = 'Data')
        elif plottype == "promptclosure":
            hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histos[dataid + "_srgenprompt" + dedx + category], stacked_histograms, lumi = lumi, datamc = 'Data')

        for i_label, label in enumerate(histos):
            histos[label].GetYaxis().SetRangeUser(ymin, ymax)
            if xmin and xmax:
                histos[label].GetXaxis().SetRangeUser(xmin, xmax)
        hratio.GetXaxis().SetTitle(variable)

        if plottype == "fakeclosure":
            new_ratio = histos[dataid + "_srgenfake" + dedx + category].Clone()
            new_ratio.Divide(histos[dataid + "_fakeprediction" + dedx + category])
            hratio.GetYaxis().SetTitle('Truth/Pred.')
        elif plottype == "promptclosure":
            new_ratio = histos[dataid + "_srgenprompt" + dedx + category].Clone()
            new_ratio.Divide(histos[dataid + "_promptprediction" + dedx + category])
            hratio.GetYaxis().SetTitle('Truth/Pred.')

        if plottype == "fakeclosure":
            histos[dataid + "_fakeprediction" + dedx + category].SetLineColor(91)
            histos[dataid + "_fakeprediction" + dedx + category].Draw("same")
            legend.AddEntry(histos[dataid + "_fakeprediction" + dedx + category], "Fake prediction")
            
            histos[dataid + "_fakecrIso" + dedx + category].SetLineColor(kTeal)
            histos[dataid + "_fakecrIso" + dedx + category].SetFillColor(0)
            histos[dataid + "_fakecrIso" + dedx + category].Draw("same")
            legend.AddEntry(histos[dataid + "_fakecrIso" + dedx + category], "Fake CR")

        elif plottype == "promptclosure":
            histos[dataid + "_promptprediction" + dedx + category].SetLineColor(8)
            histos[dataid + "_promptprediction" + dedx + category].Draw("same")
            legend.AddEntry(histos[dataid + "_promptprediction" + dedx + category], "Prompt prediction")
            
            prompt_scale.SetLineColor(kTeal)
            prompt_scale.Draw("same")
            legend.AddEntry(prompt_scale, "Prompt bg. scale")

        legend.Draw()

        for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
            #if hratio.GetBinContent(ibin)==0:
            #    hratio.SetBinContent(ibin,-999)
            hratio.SetBinContent(ibin, new_ratio.GetBinContent(ibin))
                
        hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
        if xmin and xmax:
            hratio.GetXaxis().SetRangeUser(xmin, xmax)
        hratio.GetYaxis().SetLimits(-0.1,2.6)    
        
        hratio.SetMarkerColor(kBlack)
        canvas.SaveAs("closure/" + plottype + "_" + pdffile + ".pdf")


def run(index):

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/tools/skim_05"
    inputfile = "ddbg34.root"

    with open(folder + "/luminosity.py") as fin:
        lumis = eval(fin.read())
    
    #variables = ["leadinglepton_mt", "tracks_invmass", "HT", "MHT", "tracks_deDxHarmonic2pixel", "n_btags", "MinDeltaPhiMhtJets", "n_goodjets"]
    #variables = ["leadinglepton_mt", "tracks_invmass"]

    #regions = ["BaselineNoLeptonsO150", "SElBaseline", "SMuBaseline"]
    #regions = ["Baseline", "HadBaseline"]

    #regions = ["BaselineNoLeptonsO150", "SElBaseline", "SMuBaseline"]
    #variables = ["leadinglepton_mt", "tracks_invmass", "HT", "MHT", "tracks_deDxHarmonic2pixel", "n_btags", "MinDeltaPhiMhtJets", "n_goodjets"]
    #dedexids = [""]
  
    #regions = ["BaselineJetsNoLeptons", "SElBaseline", "SMuBaseline", "HadBaseline", "BaselineElectrons", "BaselineMuons"]
    #variables = ["HT", "MHT"] #, "tracks_deDxHarmonic2pixel", "n_btags", "MinDeltaPhiMhtJets", "n_goodjets"]
    #dedexids = ["_MidDeDx", "_HighDeDx"]

    #regions = ["SElBaseline", "SMuBaseline"]
    #variables = ["HT", "MHT"] #, "tracks_deDxHarmonic2pixel", "n_btags", "MinDeltaPhiMhtJets", "n_goodjets"]
    #dedexids = [""] #, "_MidDeDx", "_HighDeDx"]

    #regions = ["SMuValidationZLL", "SMuValidationMT", "SElValidationZLL", "SElValidationMT"]
    #variables = ["leadinglepton_mt", "tracks_invmass", "HT", "MHT", "tracks_deDxHarmonic2pixel", "n_btags", "MinDeltaPhiMhtJets", "n_goodjets"]
    #dedexids = ["", "_MidDeDx", "_HighDeDx"]

    regions = ["SMuValidationMT", "SElValidationMT"]
    variables = ["tracks_invmass"]
    dedexids = ["", "_MidDeDx", "_HighDeDx"]

    counter = 0
    for region in regions:
        for variable in variables:
            for category in [""]:
                for dedx in dedexids:

                    counter += 1
                    if counter != index:
                        continue
                    
                    lumi = 31000
                    
                    if "Validation" in region:
                        if "SEl" in region:
                            datalabel = "Run2016SingleElectron"
                            lumi = lumis["Run2016_SingleElectron"] * 1e3
                        elif "SMu" in region:
                            datalabel = "Run2016SingleMuon"
                            lumi = lumis["Run2016_SingleMuon"] * 1e3
                        plot_validation("validation", variable, inputfile, datalabel, category, lumi, region, dedx, variable + dedx + category + "_" + region)

                    if "Baseline" in region:
                        plot_validation("fakeclosure", variable, inputfile, "Summer16", category, lumi, region, dedx, variable + dedx + category + "_" + region)

                    if "SMu" not in region and "SEl" not in region:
                        plot_validation("fakeclosure", variable, inputfile, "Summer16QCDZJets", category, lumi, region, dedx, variable + dedx + category + "_" + region + "_QCDZJets")
                    #    #plot_validation("promptclosure", variable, inputfile, "Summer16", category, 36000, region, dedx, variable + dedx + category + "_" + region)
                    #    #plot_validation("promptclosure", variable, inputfile, "Summer16DY", category, 36000, region, dedx, variable + dedx + category + "_" + region + "_DY")
    
    if index == -1:
        return counter + 1


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index")
    (options, args) = parser.parse_args()

    if options.index:
        run(int(options.index))
    else:
        for i in range(0, run(-1)):
            os.system("./plot_backgrounds.py --index %s" % i)
            
