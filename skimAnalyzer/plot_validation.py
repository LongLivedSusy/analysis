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

def plot_validation(variable, root_file, datalabel, category, lumi, region, dedx, pdffile, region_fakeid = ""):

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

    dataid = datalabel + "_" + variable + "_" + region

    for label in histos:
        if "Run2016" in label:
            easyname = "Data"
            histos[label].SetTitle(easyname)
        #easyname = label.replace(dataid, "Data")
        #easyname = easyname.replace("_", " ")
        #easyname = easyname.replace("sr", "SR")
        #histos[label].SetTitle(easyname)
    
    #################################
    # prompt background             #
    #################################
    
    # ABCD method to get prompt contribution in SR:
    # ________ _________ __________ 
    #         |         |          |
    # highDeDx|    A2   |    C2    |
    # ________ _________ __________ 
    #         |         |          |
    # lowDeDx |    A1   |    C1    |
    # ________|_________|__________|
    # ________|_________|__________|
    #         |         |          |      ABCD method: C = D     * A / B
    # sideDeDx|    B    |    D     |                       shape * scale
    # ________|_________|__________|
    #         |         |          |      shape from CR, scale from sideband
    #         |  1 el   |   1 DT   |     
    #         |         |          |      

    # first, subtract fake background from low-dE/dx sideband DT region (A):
    if "region" in variable:
        histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category] = histos[dataid.replace("Corrected", "Corrected_sideband") + "_sr_SidebandDeDx" + category].Clone()
        histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Add(histos[dataid.replace("Corrected", "Corrected_sideband") + "_fakeprediction%s_SidebandDeDx" % region_fakeid + category], -1)
    else:
        histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category] = histos[dataid + "_sr_SidebandDeDx" + category].Clone()
        histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Add(histos[dataid + "_fakeprediction%s_SidebandDeDx" % region_fakeid + category], -1)

    # do C = D * A / B
    #histos[dataid + "_promptprediction" + dedx + category] = histos[dataid + "_promptEl" + dedx].Clone()
    #histos[dataid + "_promptprediction" + dedx + category].Multiply(histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category])
    #prompt_scale = histos[dataid + "_promptprediction" + dedx + category].Clone()
    #histos[dataid + "_promptprediction" + dedx + category].Divide(histos[dataid + "_promptEl_SidebandDeDx" + category])
    #dataid_prompt = variable + "_PromptEl_" + datalabel
    #histos[dataid + "_promptprediction" + dedx + category] = histos[dataid_prompt + "_PromptEl" + dedx].Clone()
    #histos[dataid + "_promptprediction" + dedx + category].Multiply(histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category])
    #prompt_scale = histos[dataid + "_promptprediction" + dedx + category].Clone()
    #histos[dataid + "_promptprediction" + dedx + category].Divide(histos[dataid_prompt + "_PromptEl_SidebandDeDx" + category])
    
    if False:
           
        region_A = histos["HT_PromptEl_" + datalabel + "_PromptEl" + dedx + category].Clone()
        region_B = histos["HT_PromptEl_" + datalabel + "_PromptEl_SidebandDeDx" + category].Clone()
        histos[dataid + "_promptprediction" + dedx + category] = histos[dataid + "_sr_SidebandDeDx_fakesubtracted" + category].Clone()
        
        #mxax = region_B.GetXaxis()
        #highlowZee = region_A.Integral (mxax.FindBin(80),mxax.FindBin(100)) / region_B.Integral(mxax.FindBin(80),mxax.FindBin(100))
        
        histos[dataid + "_promptprediction" + dedx + category].Scale(region_A.Integral()/region_B.Integral())
        #histos[dataid + "_promptprediction" + dedx + category].Scale(highlowZee)
    
    ### CR from Sam:
    if True:
        
        #infile = TFile('/nfs/dust/cms/user/beinsam/LongLiveTheChi/Analyzer/CMSSW_10_1_0/src/analysis/background-estimation/prompt/output/promptDataDrivenSingleElData2016.root')
        infile = TFile('promptDataDrivenSingleElData2016.root')
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
    
    histos[dataid + "_fakeprediction" + region_fakeid + dedx + category].SetTitle("Fake prediction")

    ####################
    # plot everything: #
    ####################
    
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
    
    if "Run201" in dataid:
        
        histos[dataid + "_fakeprediction" + region_fakeid + dedx + category].SetFillColor(color_fakebg)
        
        stacked_histograms = [
                               histos[dataid + "_promptprediction" + dedx + category],
                               histos[dataid + "_fakeprediction" + region_fakeid + dedx + category],
                             ]

        if "Validation" in region:
            datahist = histos[dataid + "_sr" + dedx + category]
        else:
            datahist = stacked_histograms[-1]
    else:
        # MC:

        histos[dataid + "_srgenprompt" + dedx + category].SetTitle("MC Truth prompt")
        histos[dataid + "_srgenprompt" + dedx + category].SetFillColor(color_promptbg)
        
        histos[dataid + "_srgenfake" + region_fakeid + dedx + category].SetTitle("MC Truth fake")
        histos[dataid + "_srgenfake" + region_fakeid + dedx + category].SetFillColor(color_fakebg)
        
        stacked_histograms = [
                               histos[dataid + "_srgenfake" + region_fakeid + dedx + category],
                               histos[dataid + "_srgenprompt" + dedx + category],
                             ]
        
        datahist = histos[dataid + "_fakeprediction" + dedx + category]
    

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
    histos[dataid + "_fakecr" + region_fakeid + dedx + category].SetLineColor(kTeal)
    histos[dataid + "_fakecr" + region_fakeid + dedx + category].Draw("same")
    legend.AddEntry(histos[dataid + "_fakecr" + region_fakeid + dedx + category], "Fake CR")

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

    if region_fakeid == "":
        canvas.SaveAs("validation/" + pdffile + ".pdf")
    else:
        canvas.SaveAs("validation/" + pdffile + "_" + region_fakeid + ".pdf")


def run(index, histograms_file = "", region_fakeid = ""):

    #folder = "/afs/desy.de/user/k/kutznerv/dust/shorttrack/analysis/eventselection/tools/skim_06_onlytagged"
    #with open(folder + "/luminosity.py") as fin:
    #    lumis = eval(fin.read())
    
    regions = ["SMuValidationMT", "SElValidationMT"]
    variables = ["leadinglepton_mt", "tracks_invmass"]      #"n_goodjets", "n_btags", "HT", "MHT", 
    dedexids = ["_MidDeDx", "_HighDeDx"]

    counter = 0
    for region in regions:
        for variable in variables:
            for category in [""]:
                for dedx in dedexids:
                    
                    counter += 1
                    if counter != index: continue
                
                    if "SEl" in region:
                        #lumi = lumis["Run2016_SingleElectron"] * 1e3
                        lumi = 34330
                        plot_validation(variable, histograms_file, "Run2016SingleElectron", category, lumi, region, dedx, "val_" + region + dedx + "_" + variable + category, region_fakeid = region_fakeid)
                        plot_validation(variable, histograms_file, "Summer16", category, lumi, region, dedx, "clo_" + region + dedx + "_" + variable + category, region_fakeid = region_fakeid)
                    
                    elif "SMu" in region:
                        #lumi = lumis["Run2016_SingleMuon"] * 1e3
                        lumi = 35200
                        plot_validation(variable, histograms_file, "Run2016SingleMuon", category, lumi, region, dedx, "val_" + region + dedx + "_" + variable + category, region_fakeid = region_fakeid)
                        plot_validation(variable, histograms_file, "Summer16", category, lumi, region, dedx, "clo_" + region + dedx + "_" + variable + category, region_fakeid = region_fakeid)
                        
    return counter
    
                        
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index")
    parser.add_option("--histograms", dest = "histograms_file")
    parser.add_option("--regionfakeid", dest = "region_fakeid", default = "")
    (options, args) = parser.parse_args()

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    this_scripts_name = main.__file__

    if options.index:
        run(int(options.index), histograms_file = options.histograms_file, region_fakeid = options.region_fakeid)
    else:
        for i in range(0, run(-1)+1):
            os.system("./%s --index %s --histograms %s --regionfakeid '%s'" % (this_scripts_name, i, options.histograms_file, options.region_fakeid))
            