#!/bin/env python
from __future__ import division
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


def get_histograms(variable, root_file, datalabel, category, region, dedx, lumi, use_iso = True):

    # get all histograms from ddbg.root:
    histos = collections.OrderedDict()
    fin = TFile(root_file, "read")
    
    for obj in fin.GetListOfKeys():
        label = obj.ReadObj().GetName()
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
            
        # if no dedx selected, combine mid and high dedx:
        if dedx == "" and "_MidDeDx" in label and label.replace("_MidDeDx", "_HighDeDx") in histos:
            if label.replace("_MidDeDx", "") not in histos:
                histos[label.replace("_MidDeDx", "")] = histos[label].Clone()
                histos[label.replace("_MidDeDx", "")].SetDirectory(0)
                histos[label.replace("_MidDeDx", "")].Add(histos[label.replace("_MidDeDx", "_HighDeDx")])

    fin.Close()

    dataid = variable + "_" + region + "_" + datalabel

    #for label in histos:
    #    easyname = label.replace(dataid, "Data")
    #    easyname = easyname.replace("_", " ")
    #    easyname = easyname.replace("sr", "SR")
    #    histos[label].SetTitle(easyname)
    
    #################################
    # prompt background             #
    #################################
    
    # ABCD method to get prompt contribution in SR:
    # ________ _________ __________ 
    #         |         |          |
    # highDeDx|    A    |    C     |
    # ________|_________|__________|
    #         |         |          |      ABCD method: C = D     * A / B
    # lowDeDx |    B    |    D     |                       shape * scale
    # ________|_________|__________|
    #         |         |          |      shape from CR, scale from sideband
    #         |  1 el   |   1 DT   |     
    #         |         |          |      

    # first, subtract fake background from low-dE/dx sideband DT region (A):
    if "region" in variable:
        histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category] = histos[dataid.replace("Corrected", "Corrected_sideband") + "_sr_SidebandDeDx" + category].Clone()
        if not use_iso:
            histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Add(histos[dataid.replace("Corrected", "Corrected_sideband") + "_fakeprediction_SidebandDeDx" + category], -1)
        else:
            histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Add(histos[dataid.replace("Corrected", "Corrected_sideband") + "_fakepredictionIso_SidebandDeDx" + category], -1)
    else:
        histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category] = histos[dataid + "_sr_SidebandDeDx" + category].Clone()
        if not use_iso:
            histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Add(histos[dataid + "_fakeprediction_SidebandDeDx" + category], -1)
        else:
            histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Add(histos[dataid + "_fakepredictionIso_SidebandDeDx" + category], -1)

    # do C = D * A / B
    #histos[dataid + "_promptprediction" + dedx + category] = histos[dataid + "_promptEl" + dedx].Clone()
    #histos[dataid + "_promptprediction" + dedx + category].Multiply(histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category])
    #prompt_scale = histos[dataid + "_promptprediction" + dedx + category].Clone()
    #histos[dataid + "_promptprediction" + dedx + category].Divide(histos[dataid + "_promptEl_SidebandDeDx" + category])
    
    #dataid_prompt = variable + "_PromptEl_" + datalabel
    #histos[dataid + "_promptprediction" + dedx + category] = histos[dataid_prompt + "_prompt" + dedx].Clone()
    #histos[dataid + "_promptprediction" + dedx + category].Multiply(histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category])
    #prompt_scale = histos[dataid + "_promptprediction" + dedx + category].Clone()
    #histos[dataid + "_promptprediction" + dedx + category].Divide(histos[dataid_prompt + "_prompt_SidebandDeDx" + category])
 
    #region_D = histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Clone()
    #region_A = histos["HT_PromptEl_" + datalabel + "_prompt" + dedx].Clone()
    #region_B = histos["HT_PromptEl_" + datalabel + "_prompt_SidebandDeDx" + category].Clone()
    #histos[dataid + "_promptprediction" + dedx + category] = region_D.Clone()
    #histos[dataid + "_promptprediction" + dedx + category].Scale(region_A.Integral()/region_B.Integral())
    #print "region_D.Integral()", region_A.Integral()
    #print "region_B.Integral()", region_B.Integral()
    
    # CR from Sam:
    infile = TFile('/nfs/dust/cms/user/beinsam/LongLiveTheChi/Analyzer/CMSSW_10_1_0/src/analysis/background-estimation/prompt/output/promptDataDrivenSingleElData2016.root')
    hcontrollow = infile.Get('hElSElValidationMTZone0p0to2p1_InvMassControl')
    hcontrollow.SetDirectory(0)
    hcontrolmed = infile.Get('hElSElValidationMTZone2p1to4p0_InvMassControl')
    hcontrolmed.SetDirectory(0)
    hcontrolhigh = infile.Get('hElSElValidationMTZone4p0to99_InvMassControl')
    hcontrolhigh.SetDirectory(0)
    infile.Close()
    
    mxax = hcontrollow.GetXaxis()
    highlowZeeA = hcontrolmed.Integral (mxax.FindBin(80),mxax.FindBin(100)) / hcontrollow.Integral(mxax.FindBin(80),mxax.FindBin(100))
    highlowZeeB = hcontrolhigh.Integral(mxax.FindBin(80),mxax.FindBin(100)) / hcontrollow.Integral(mxax.FindBin(80),mxax.FindBin(100))
    
    if dedx == "_MidDeDx":
        histos[dataid + "_promptprediction" + dedx + category] = histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Clone()
        histos[dataid + "_promptprediction" + dedx + category].Scale(highlowZeeA)
    elif dedx == "_HighDeDx":
        histos[dataid + "_promptprediction" + dedx + category] = histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Clone()
        histos[dataid + "_promptprediction" + dedx + category].Scale(highlowZeeB)
    elif dedx == "":
        h_low = histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Clone()    
        h_low.Scale(highlowZeeA)
        if "region" in variable:
            for ibin in range(1, h_low.GetXaxis().GetNbins() + 1):
                if h_low.GetBinLowEdge(ibin) % 2 != 0:
                    h_low.SetBinContent(ibin, 0)
        
        h_high = histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Clone()
        h_high.Scale(highlowZeeB)
        if "region" in variable:
            for ibin in range(1, h_high.GetXaxis().GetNbins() + 1):
                if h_high.GetBinLowEdge(ibin) % 2 == 0:
                    h_high.SetBinContent(ibin, 0)
        
        histos[dataid + "_promptprediction" + dedx + category] = h_low.Clone()
        histos[dataid + "_promptprediction" + dedx + category].Add(h_high)

    histos[dataid + "_promptprediction" + dedx + category].SetFillColor(color_promptbg)
    histos[dataid + "_promptprediction" + dedx + category].SetTitle("Prompt prediction")
    histos[dataid + "_promptprediction" + dedx + category].SetName(dataid + "_promptprediction" + dedx + category)

    #fout = TFile("prompt.root", "update")
    #histos[dataid + "_promptprediction" + dedx + category] = rebin_histo(histos[dataid + "_promptprediction" + dedx + category], 54, 1, 55)
    #histos[dataid + "_promptprediction" + dedx + category].Write()
    #fout.Close()
    #quit()
    
    #################################
    # Fake background               #
    #################################
    
    if not use_iso:
        histos[dataid + "_fakeprediction" + dedx + category].SetTitle("Fake prediction")
    else:
        histos[dataid + "_fakepredictionIso" + dedx + category].SetTitle("Fake prediction")        

    return histos


def plot_validation(plottype, variable, root_file, datalabel, category, lumi, region, dedx, pdffile, use_iso = False):
    
    histos = get_histograms(variable, root_file, datalabel, category, region, dedx, lumi, use_iso = use_iso)
    #for label in histos:
    #    if "Run201" not in label:
    #        histos[label].Scale(lumi)
        
    dataid = variable + "_" + region + "_" + datalabel
        
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    legend.SetHeader(region + " " + dedx)

    lumi = float("%.2f" % (lumi/1e3))

    if "ValidationMT" in region and variable == "leadinglepton_mt":
        ymin = 1e2; ymax = 1e6
    elif "ValidationMT" in region and variable == "tracks_invmass":
        ymin = 1e-1; ymax = 5e3
    elif "ValidationZLL" in region and variable == "leadinglepton_mt":
        ymin = 1e-4; ymax = 1e4
    elif "ValidationZLL" in region and variable == "tracks_invmass":
        ymin = 5e-2; ymax = 5e3
    else:
        ymin = 5e1; ymax = 2e4

    if not use_iso:
        histos[dataid + "_fakeprediction" + dedx + category].SetFillColor(color_fakebg)
        stacked_histograms = [
                               histos[dataid + "_promptprediction" + dedx + category],
                               histos[dataid + "_fakeprediction" + dedx + category],
                             ]
    else:
        histos[dataid + "_fakepredictionIso" + dedx + category].SetFillColor(color_fakebg)
        stacked_histograms = [
                               histos[dataid + "_promptprediction" + dedx + category],
                               histos[dataid + "_fakepredictionIso" + dedx + category],
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

    hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, datahist, stacked_histograms, lumi = lumi, datamc = 'Data')
    stacked_histograms[-1].SetTitle("")
    
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
        histos[dataid + "_fakecrIso" + dedx + category].SetLineColor(kTeal)
        histos[dataid + "_fakecrIso" + dedx + category].Draw("same")
        legend.AddEntry(histos[dataid + "_fakecrIso" + dedx + category], "Fake CR")

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
        canvas.SaveAs("validation/validation_" + pdffile + "_iso.pdf")
    else:
        canvas.SaveAs("validation/validation_" + pdffile + ".pdf")


def plot_fakeclosure(plottype, variable, root_file, datalabel, category, lumi, region, dedx, pdffile, use_iso = True):
    
    histos = get_histograms(variable, root_file, datalabel, category, region, dedx, lumi, use_iso = use_iso)

    #for label in histos:
    #    if "Run201" not in label:
    #        histos[label].Scale(lumi)

    dataid = variable + "_" + region + "_" + datalabel

    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    legend.SetHeader(region + " " + dedx)

    lumi = float("%.2f" % (lumi/1e3))

    if "SElBaseline" in region and variable == "HT":
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

    if variable == "MHT":
        xmin = 0
        xmax = 400
    else:
        xmin = False
        xmax = False

    #histos[dataid + "_srgenprompt" + dedx + category].SetFillColor(color_promptbg)
    #histos[dataid + "_srgenprompt" + dedx + category].SetTitle("Prompt background SR (MC Truth)")
    histos[dataid + "_srgenfake" + dedx + category].SetFillColor(color_fakebg)
    histos[dataid + "_srgenfake" + dedx + category].SetTitle("Fake background SR (MC Truth)")

    stacked_histograms = [
                           histos[dataid + "_srgenfake" + dedx + category],
                           #histos[dataid + "_srgenprompt" + dedx + category],
                         ]

    hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histos[dataid + "_srgenfake" + dedx + category], stacked_histograms, lumi = lumi, datamc = 'Data')

    for i_label, label in enumerate(histos):
        histos[label].GetYaxis().SetRangeUser(ymin, ymax)
        if xmin and xmax:
            histos[label].GetXaxis().SetRangeUser(xmin, xmax)
    hratio.GetXaxis().SetTitle(variable)

    new_ratio = histos[dataid + "_srgenfake" + dedx + category].Clone()
    new_ratio.Divide(histos[dataid + "_fakeprediction" + dedx + category])
    hratio.GetYaxis().SetTitle('Truth/Pred.')

    histos[dataid + "_fakeprediction" + dedx + category].SetLineColor(91)
    histos[dataid + "_fakeprediction" + dedx + category].Draw("same")
    legend.AddEntry(histos[dataid + "_fakeprediction" + dedx + category], "Fake prediction")
    
    histos[dataid + "_fakecrIso" + dedx + category].SetLineColor(kTeal)
    histos[dataid + "_fakecrIso" + dedx + category].SetFillColor(0)
    histos[dataid + "_fakecrIso" + dedx + category].Draw("same")
    legend.AddEntry(histos[dataid + "_fakecrIso" + dedx + category], "Fake CR")

    legend.Draw()

    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        hratio.SetBinContent(ibin, new_ratio.GetBinContent(ibin))
            
    hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
    if xmin and xmax:
        hratio.GetXaxis().SetRangeUser(xmin, xmax)
    hratio.GetYaxis().SetLimits(-0.1,2.6)    
    
    hratio.SetMarkerColor(kBlack)
    canvas.SaveAs("closure/" + plottype + "_" + pdffile + ".pdf")


def run(index):

    folder = "/afs/desy.de/user/k/kutznerv/dust/shorttrack/analysis/eventselection/tools/skim_06_onlytagged"
    with open(folder + "/luminosity.py") as fin:
        lumis = eval(fin.read())
    
    #regions = ["SMuValidationMT", "SElValidationMT"]
    #variables = ["leadinglepton_mt", "tracks_invmass"]
    #dedexids = ["_MidDeDx", "_HighDeDx"]

    regions = ["Baseline"] #, "BaselineJetsNoLeptons", "SElBaseline", "SMuBaseline"]
    variables = ["regionCorrected"] #, "HT", "MHT", "tracks_deDxHarmonic2pixel", "n_btags", "MinDeltaPhiMhtJets", "n_goodjets"]
    dedexids = [""]

    counter = 0
    for region in regions:
        for variable in variables:
            for category in [""]:
                for dedx in dedexids:
                    
                    counter += 1
                    if counter != index:
                        continue
                
                    if "Validation" in region:
                        if "SEl" in region:
                            lumi = lumis["Run2016_SingleElectron"] * 1e3
                            inputfile = "prediction_Run2016SingleElectron.root"
                        
                        elif "SMu" in region:
                            lumi = lumis["Run2016_SingleMuon"] * 1e3
                            inputfile = "prediction_Run2016SingleMuon.root"
                                                    
                        plot_validation("validation", variable, inputfile, "Run2016", category, lumi, region, dedx, region + dedx + "_" + variable + category)
                        
                    if "Baseline" in region:
                        
                        lumi = 137000
                    
                        if "region" not in variable:
                            plot_fakeclosure("fakeclosure", variable, "prediction_Summer16.root", "Summer16", category, lumi, region, dedx, region + dedx + "_" + variable + category)
                        else:
                            #plot_fakeclosure("fakeclosure", variable, "predictionRegion_Summer16.root", "Summer16", category, lumi, region, dedx, region + dedx + "_" + variable + category)
                             plot_fakeclosure("fakeclosure", variable, "predictionRegion_Run2016.root", "Run2016", category, lumi, region, dedx, region + dedx + "_" + variable + category)                           

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index")
    (options, args) = parser.parse_args()

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    if options.index:
        run(int(options.index))
    else:
        for i in range(0, 1000):
            os.system("./plot_backgrounds3.py --index %s" % i)
            