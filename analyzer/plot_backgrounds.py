#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import collections
import glob
import os
import shared_utils
import get_backgrounds

def plot_validation(variable, root_file, mclabel, datalabel, category, lumi, region, pdffile):
    
    # get all histograms from ddbg.root:
    histos = collections.OrderedDict()
    fin = TFile(root_file, "read")

    zones = get_backgrounds.histos.keys()
    for zone in zones:
        histos[mclabel + zone] = fin.Get(variable + "_" + region + "_" + mclabel + zone)
        histos[datalabel + zone] = fin.Get(variable + "_" + region + "_" + datalabel + zone)

    for label in histos.keys():

        try:
            histos[label].SetDirectory(0)
            histos[label].SetLineWidth(2)
        except:
            del histos[label]
            continue

        if "Run201" not in label:
            histos[label].Scale(lumi)
        shared_utils.histoStyler(histos[label])

        # combine short and long tracks:
        if category == "" and "_short" in label:
            try:
                histos[label.replace("_short", "")] = histos[label].Clone()
                histos[label.replace("_short", "")].SetDirectory(0)
                histos[label.replace("_short", "")].Add(histos[label.replace("_short", "_long")])
            except:
                del histos[label.replace("_short", "")]
                continue

    for label in histos.keys():
        easyname = label.replace(datalabel, "Data")
        easyname = easyname.replace(mclabel, "MC")
        easyname = easyname.replace("_", " ")
        easyname = easyname.replace("sr", "SR")
        histos[label].SetTitle(easyname)

    fin.Close()
    
    # ABCD method to get prompt contribution in SR:

    # first, subtract fake background from low-dE/dx sideband DT region:
    histos[datalabel + "_lowDeDxDT_fakesubtraced"] = histos[datalabel + "_lowDeDxDT"].Clone()
    histos[datalabel + "_lowDeDxDT_fakesubtraced"].Add(histos[datalabel + "_fakepredictionSideband"], -1)
    
    histos[datalabel + "_promptprediction"] = histos[datalabel + "_highDeDxPromptElectron"].Clone()
    #histos[datalabel + "_promptprediction"].Multiply(histos[datalabel + "_lowDeDxDT"])
    histos[datalabel + "_promptprediction"].Multiply(histos[datalabel + "_lowDeDxDT_fakesubtraced"])
    histos[datalabel + "_promptprediction"].Divide(histos[datalabel + "_lowDeDxPromptElectron"])

    # plot:
    canvas = shared_utils.mkcanvas()
    canvas.SetFillStyle(4000)    
    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    legend.SetHeader(region + " region")
    colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]
    
    histos[datalabel + "_fakeprediction" + category].SetFillColor(216)
    histos[datalabel + "_fakeprediction" + category].SetTitle("Fake prediction")
    histos[datalabel + "_promptprediction"].SetFillColor(207)
    histos[datalabel + "_promptprediction"].SetTitle("Prompt prediction")

    stacked_histograms = [
                           histos[datalabel + "_fakeprediction" + category],
                           histos[datalabel + "_promptprediction"],
                         ]

    lumi = float("%.2f" % (lumi/1e3))

    hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histos[datalabel + "_srMidHighDeDx" + category], stacked_histograms, lumi = lumi, datamc = 'Data')

    if "ValidationMT" in region and variable == "leptons_mt":
        ymin = 5e1; ymax = 2e4
    if "ValidationMT" in region and variable == "tracks_invmass":
        ymin = 1e-1; ymax = 5e3
    elif "ValidationZLL" in region and variable == "tracks_invmass":
        ymin = 5e-2; ymax = 5e3
    elif "ValidationZLL" in region and variable == "leptons_mt":
        ymin = 1e-1; ymax = 1e4
    else:
        ymin = 5e1; ymax = 2e4

    for i_label, label in enumerate(histos):
        histos[label].GetYaxis().SetRangeUser(ymin, ymax)
           
    hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
    hratio.GetYaxis().SetTitle('Data/prediction')

    xlabel = variable
    xlabel = xlabel.replace("leptons_mt", "m_{T}^{lepton} (GeV)")
    hratio.GetXaxis().SetTitle(xlabel)

    histos[datalabel + "_fakecr" + category].SetLineColor(kTeal)
    histos[datalabel + "_fakecr" + category].Draw("same")
    legend.AddEntry(histos[datalabel + "_fakecr" + category], "Fake CR")

    histos[datalabel + "_highDeDxPromptElectron"].SetLineColor(kTeal+2)
    histos[datalabel + "_highDeDxPromptElectron"].Draw("same")
    legend.AddEntry(histos[datalabel + "_highDeDxPromptElectron"], "Prompt el. (dE/dx>2.1)")


    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)
    canvas.SaveAs(pdffile + ".pdf")


if __name__ == "__main__":

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
   
    folder = "../skims/current"
    with open(folder + "/luminosity.py") as fin:
        lumis = eval(fin.read())

    inputfile = "ddbg2.root"

    regions = collections.OrderedDict()
    regions["SElValidationMT"] = ["leptons_mt", "tracks_invmass"]
    regions["SMuValidationMT"] = ["leptons_mt", "tracks_invmass"]
    regions["SElValidationZLL"] = ["leptons_mt", "tracks_invmass"]
    regions["SMuValidationZLL"] = ["leptons_mt", "tracks_invmass"]
    
    for region in regions:
        for variable in regions[region]:
            
            if "SEl" in region:
                datalabel = "SingleElectron"
            elif "SMu" in region:
                datalabel = "SingleMuon"
            else:
                continue
            
            plot_validation(variable, inputfile, "Summer16", "Run2016%s" % datalabel, "", lumis["Run2016_%s" % datalabel] * 1e3, region, variable + "_" + region)

    

