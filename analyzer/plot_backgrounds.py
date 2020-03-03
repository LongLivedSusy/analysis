#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import collections
import glob
import os
import shared_utils

def plot_validation(variable, root_file, mclabel, datalabel, category, lumi, region, pdffile):
    
    # get all histograms from ddbg.root:
    histos = collections.OrderedDict()
    fin = TFile(root_file, "read")

    import get_backgrounds
    zones = get_backgrounds.histos.keys()
    #zones = ['_sr_short', '_sr_long', '_srSideband_short', '_srSideband_long', '_srMid_short', '_srMid_long', '_srMidHighDeDx_short', '_srMidHighDeDx_long', '_srHighDeDx_short', '_srHighDeDx_long', '_fakecr_short', '_fakecr_long', '_fakecrSideband_short', '_fakecrSideband_long', '_fakecrMid_short', '_fakecrMid_long', '_fakecrMidHighDeDx_short', '_fakecrMidHighDeDx_long', '_fakecrHighDeDx_short', '_fakecrHighDeDx_long', '_fakeprediction_short', '_fakeprediction_long', '_fakepredictionSideband_short', '_fakepredictionSideband_long', '_fakepredictionMid_short', '_fakepredictionMid_long', '_fakepredictionMidHighDeDx_short', '_fakepredictionMidHighDeDx_long', '_fakepredictionHighDeDx_short', '_fakepredictionHighDeDx_long', '_lowDeDxPromptElectron', '_lowDeDxDTnoLep', '_lowDeDxDT', '_midHighDeDxPromptElectron', '_midHighDeDxDTnoLep', '_midHighDeDxDT', '_midDeDxPromptElectron', '_midDeDxDTnoLep', '_midDeDxDT', '_highDeDxPromptElectron', '_highDeDxDTnoLep', '_highDeDxDT', '_srgenfakes_short', '_srgenfakes_long', '_srgenprompt_short', '_srgenprompt_long']

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

    fin.Close()

    for label in histos.keys():
        easyname = label.replace(datalabel, "Data")
        easyname = easyname.replace(mclabel, "MC")
        easyname = easyname.replace("_", " ")
        easyname = easyname.replace("sr", "SR")
        histos[label].SetTitle(easyname)
    
    # ABCD method to get prompt contribution in SR:

    # first, subtract fake background from low-dE/dx sideband DT region:
    #histos[datalabel + "_lowDeDxDT_fakesubtraced"] = histos[datalabel + "_lowDeDxDT"].Clone()
    #histos[datalabel + "_lowDeDxDT_fakesubtraced"].Add(histos[datalabel + "_fakepredictionSideband"], -1)
    
    # ABCD method: C = D  * A / B
    histos[datalabel + "_promptprediction"] = histos[datalabel + "_midDeDxPromptElectron"].Clone()
    histos[datalabel + "_promptprediction"].Multiply(histos[datalabel + "_midDeDxDT"])
    #histos[datalabel + "_promptprediction"].Multiply(histos[datalabel + "_lowDeDxDT_fakesubtraced"])
    histos[datalabel + "_promptprediction"].Divide(histos[datalabel + "_midDeDxPromptElectron"])

    # plot:
    canvas = shared_utils.mkcanvas()
    canvas.SetFillStyle(4000)    
    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
    legend.SetHeader(region + " region")
    colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]
    
    # Fake prediction using FR map
    histos[datalabel + "_fakeprediction" + category].SetFillColor(216)
    histos[datalabel + "_fakeprediction" + category].SetTitle("Fake prediction")
    
    # Fake pred. using constant factor:
    #data_fakerate_short = fin.Get("HT_FakeRateDetQCDJetHT_Run2016JetHT_sr_short")
    #data_fakerate_short_denom = fin.Get("HT_FakeRateDetQCDJetHT_Run2016JetHT_fakecr_short")
    #data_fakerate_short.SetDirectory(0)
    #data_fakerate_short_denom.SetDirectory(0)
    #fr_short = data_fakerate_short.Integral()/data_fakerate_short_denom.Integral()
    #data_fakerate_short.Divide(data_fakerate_short_denom)
    #data_fakerate_short.Draw()
    #canvas.Print("fakerate_data_short.pdf")
    #
    #data_fakerate_long = fin.Get("HT_FakeRateDetQCDJetHT_Run2016JetHT_sr_long")
    #data_fakerate_long_denom = fin.Get("HT_FakeRateDetQCDJetHT_Run2016JetHT_fakecr_long")
    #data_fakerate_long.SetDirectory(0)
    #data_fakerate_long_denom.SetDirectory(0)
    #fr_long = data_fakerate_long.Integral()/data_fakerate_long_denom.Integral()
    #data_fakerate_long.Divide(data_fakerate_long_denom)
    #data_fakerate_long.Draw()
    #canvas.Print("fakerate_data_long.pdf")    
    
    histos[datalabel + "_promptprediction"].SetFillColor(207)
    histos[datalabel + "_promptprediction"].SetTitle("Prompt prediction")

    stacked_histograms = [
                           histos[datalabel + "_fakeprediction" + category],
                           histos[datalabel + "_promptprediction"],
                         ]

    lumi = float("%.2f" % (lumi/1e3))

    if "Validation" in region:
        datahist = histos[datalabel + "_sr" + category]
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
    hratio.GetXaxis().SetTitle(xlabel)

    # add fake CR:
    histos[datalabel + "_fakecr" + category].SetLineColor(kTeal)
    histos[datalabel + "_fakecr" + category].Draw("same")
    legend.AddEntry(histos[datalabel + "_fakecr" + category], "Fake CR")

    # add prompt CR:
    histos[datalabel + "_highDeDxPromptElectron"].SetLineColor(kTeal+2)
    histos[datalabel + "_highDeDxPromptElectron"].Draw("same")
    legend.AddEntry(histos[datalabel + "_highDeDxPromptElectron"], "Prompt el. (dE/dx>2.1)")

    ## add MC Truth info:
    #histos[mclabel + "_srgenfakes" + category].SetLineColor(kRed)
    #histos[mclabel + "_srgenfakes" + category].Draw("same")
    #legend.AddEntry(histos[mclabel + "_srgenfakes" + category], "Genfakes")
    #
    #histos[mclabel + "_srgenprompt" + category].SetLineColor(kOrange)
    #histos[mclabel + "_srgenprompt" + category].Draw("same")
    #legend.AddEntry(histos[mclabel + "_srgenprompt" + category], "Genprompt")
    
    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)
    canvas.SaveAs(pdffile + ".pdf")


if __name__ == "__main__":

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
   
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/tools/skim_69_merged"
    inputfile = "ddbg5.root"

    with open(folder + "/luminosity.py") as fin:
        lumis = eval(fin.read())

    regions = collections.OrderedDict()
    regions["SElValidationMT"] = ["leadinglepton_mt", "tracks_invmass"]
    #regions["SMuValidationMT"] = ["leadinglepton_mt", "tracks_invmass"]
    regions["SElValidationZLL"] = ["leadinglepton_mt", "tracks_invmass"]
    #regions["SMuValidationZLL"] = ["leadinglepton_mt", "tracks_invmass"]
    
    for region in regions:
        for variable in regions[region]:
            
            if "SEl" in region:
                datalabel = "SingleElectron"
            elif "SMu" in region:
                datalabel = "SingleMuon"
            else:
                continue
            
            #plot_validation(variable, inputfile, "Summer16", "Run2016%s" % datalabel, "_short", lumis["Run2016_%s" % datalabel] * 1e3, region, "short_" + variable + "_" + region)
            #plot_validation(variable, inputfile, "Summer16", "Run2016%s" % datalabel, "_long", lumis["Run2016_%s" % datalabel] * 1e3, region, "long_" + variable + "_" + region)
            plot_validation(variable, inputfile, "Summer16", "Run2016%s" % datalabel, "", lumis["Run2016_%s" % datalabel] * 1e3, region, "combined_" + variable + "_" + region)

