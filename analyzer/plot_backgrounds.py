#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import collections
import glob
import os
import shared_utils

def plot_validation(variable, root_file, mclabel, datalabel, category, lumi, region, pdffile):
    
    dataid = variable + "_" + region + "_" + datalabel
    mcid = variable + "_" + region + "_" + mclabel
    
    dedx = "_MidDeDx"
    
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
        easyname = easyname.replace(mcid, "MC")
        easyname = easyname.replace("_", " ")
        easyname = easyname.replace("sr", "SR")
        histos[label].SetTitle(easyname)
    
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    legend.SetHeader(region + " region")
    colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]
       
    #################################
    # prompt background             #
    #################################
    
    # ABCD method to get prompt contribution in SR:
    # _______ _________ __________
    #        |         |         |
    #  1 DT  |    A    |    C    |
    # _______|_________|_________|
    #        |         |         |      ABCD method: C = D     * A / B
    #  1 el  |    B    |    D    |                       shape * scale
    # _______|_________|_________| 
    #        | lowDeDx | highDeDx|      shape from CR, scale from sideband

    # first, subtract fake background from low-dE/dx sideband DT region (A):
    histos[dataid + "_sr_SidebandDeDx_fakesubtraced" + category] = histos[dataid + "_sr_SidebandDeDx" + category].Clone()
    histos[dataid + "_sr_SidebandDeDx_fakesubtraced" + category].Add(histos[dataid + "_fakeprediction_SidebandDeDx" + category], -1)

    # do C = D * A / B
    histos[dataid + "_promptprediction" + dedx + category] = histos[dataid + "_promptEl" + dedx].Clone()
    histos[dataid + "_promptprediction" + dedx + category].Multiply(histos[dataid + "_sr_SidebandDeDx_fakesubtraced" + category])
    prompt_scale = histos[dataid + "_promptprediction" + dedx + category].Clone()
    histos[dataid + "_promptprediction" + dedx + category].Divide(histos[dataid + "_promptEl_SidebandDeDx" + category])

    histos[dataid + "_promptprediction" + category].SetFillColor(207)
    histos[dataid + "_promptprediction" + category].SetTitle("Prompt prediction")

    #################################
    # Fake background               #
    #################################
    
    histos[dataid + "_fakeprediction" + dedx + category].SetFillColor(216)
    histos[dataid + "_fakeprediction" + dedx + category].SetTitle("Fake prediction")
    
    #################################
    # Stack backgrounds             #
    #################################

    stacked_histograms = [
                           histos[dataid + "_fakeprediction" + dedx + category],
                           histos[dataid + "_promptprediction" + dedx + category],
                         ]

    lumi = float("%.2f" % (lumi/1e3))

    # signal region is blinded
    if "Validation" in region:
        datahist = histos[dataid + "_sr" + dedx + category]
    else:
        datahist = stacked_histograms[-1]
    
    hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, datahist, stacked_histograms, lumi = lumi, datamc = 'Data')
    stacked_histograms[-1].SetTitle("")

    if "ValidationMT" in region and variable == "leadinglepton_mt":
        ymin = 5e1; ymax = 2e4
    if "ValidationMT" in region and variable == "tracks_invmass":
        ymin = 1e-1; ymax = 5e3
    elif "ValidationZLL" in region and variable == "tracks_invmass":
        ymin = 5e-2; ymax = 5e3
    elif "ValidationZLL" in region and variable == "leadinglepton_mt":
        ymin = 1e-1; ymax = 1e4
    else:
        ymin = 5e1; ymax = 2e4

    for i_label, label in enumerate(histos):
        histos[label].GetYaxis().SetRangeUser(ymin, ymax)
           
    hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
    hratio.GetYaxis().SetTitle('Data/prediction')

    xlabel = variable
    xlabel = xlabel.replace("leptons_mt", "m_{T}^{lepton} (GeV)")
    xlabel = xlabel.replace("leadinglepton_mt", "m_{T}^{lepton} (GeV)")
    hratio.GetXaxis().SetTitle(xlabel)

    # add fake CR:
    histos[dataid + "_fakecr" + dedx + category].SetLineColor(kTeal)
    histos[dataid + "_fakecr" + dedx + category].Draw("same")
    legend.AddEntry(histos[dataid + "_fakecr" + dedx + category], "Fake CR")

    # add prompt CR:
    prompt_scale.SetLineColor(kTeal+2)
    prompt_scale.Draw("same")
    legend.AddEntry(prompt_scale, "Prompt bg. scale")

    # add MC Truth info:
    histos[dataid + "_srgenfake" + dedx + category].SetLineColor(kRed)
    histos[dataid + "_srgenfake" + dedx + category].Draw("same")
    legend.AddEntry(histos[dataid + "_srgenfake" + dedx + category], "Genfakes")
    
    histos[dataid + "_srgenprompt" + dedx + category].SetLineColor(kOrange)
    histos[dataid + "_srgenprompt" + dedx + category].Draw("same")
    legend.AddEntry(histos[dataid + "_srgenprompt" + dedx + category], "Genprompt")
    
    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)
    canvas.SaveAs(pdffile + ".pdf")


if __name__ == "__main__":

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
   
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/tools/skim_69_merged"
    inputfile = "ddbg20.root"

    with open(folder + "/luminosity.py") as fin:
        lumis = eval(fin.read())

    regions = collections.OrderedDict()
    regions["SElValidationMT"] = ["leadinglepton_mt", "tracks_invmass"]
    #regions["SElValidationZLL"] = ["leadinglepton_mt", "tracks_invmass"]
    #regions["SMuValidationMT"] = ["leadinglepton_mt", "tracks_invmass"]
    #regions["SMuValidationZLL"] = ["leadinglepton_mt", "tracks_invmass"]
    
    for region in regions:
        for variable in regions[region]:
            
            if "SEl" in region:
                datalabel = "SingleElectron"
            elif "SMu" in region:
                datalabel = "SingleMuon"
            else:
                continue
            
            plot_validation(variable, inputfile, "Summer16", "Run2016%s" % datalabel, "", lumis["Run2016_%s" % datalabel] * 1e3, region, "combined_" + variable + "_" + region)

