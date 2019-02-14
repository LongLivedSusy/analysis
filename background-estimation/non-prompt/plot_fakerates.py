#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *
import collections

def do_2D_plot(root_file, hist_name, path, extra_text):

    fin = TFile(root_file, "read")
    
    try:
        fake_rate = fin.Get(hist_name)
        n = fake_rate.GetEntries()
    except:
        print "histogram not available: %s" % hist_name
        return

    canvas = TCanvas("fakerate", "fakerate", 800, 800)  
    canvas.SetRightMargin(0.16)
    canvas.SetLeftMargin(0.14)
    canvas.SetLogz(True)
    
    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)
    latex.SetTextAlign(13)
    latex.SetTextFont(52)
    
    fake_rate.GetZaxis().SetTitleOffset(1.5)
    fake_rate.GetZaxis().SetRangeUser(1e-6, 1e-1)
    fake_rate.Draw("COLZ")
    
    latex.DrawLatex(0.18, 0.87, extra_text)

    stamp_plot()
    if not os.path.exists("%s/plots" % path): os.mkdir("%s/plots" % path)
    canvas.SaveAs("%s/plots/%s.pdf" % (path, "fakeratemap_" + hist_name.replace("/", "_").replace("fakerate_", "")))

    fin.Close()


def do_1D_plot(root_file, path, category, variable, regions = ["dilepton", "qcd", "qcd_sideband"]):

    fin = TFile(root_file, "read")

    hist_names = []  
    histos = collections.OrderedDict()
    #for region in ["dilepton", "qcd", "qcd_sideband"]:
    for region in regions:

        colors = [kBlack, kRed, kBlue, kGreen, kOrange, ]

        for data_type in ["Summer16", "Fall17", "2016", "2017", "2018"]:
            hist_names.append( region + "/" + data_type + "/" + category + "/fakerate_" + variable )

        for hist_name in hist_names:
            label = hist_name.replace("/", "_")
            histos[label] = fin.Get(hist_name)
            color = colors.pop(0)
            histos[label].SetLineColor(color)
            histos[label].SetLineWidth(2)

            if "Summer16" in hist_name or "Fall17" in hist_name:
                histos[label].SetFillColor(color)
                histos[label].SetFillStyle(3003)
                histos[label].SetLineWidth(1)

    canvas = TCanvas("fakerate", "fakerate", 800, 800)  
    canvas.SetLeftMargin(0.14)
    canvas.SetLogy(True)
    
    legend = TLegend(0.55, 0.8, 0.97, 0.97)
    legend.SetTextSize(0.025)

    for i, label in enumerate(histos):

        if i == 0:
            histos[label].Draw("hist e")
            histos[label].GetYaxis().SetRangeUser(1e-6,1e-2)
        else:
            histos[label].Draw("hist e same")

        # make nice labels
        desc = label.replace("_fakerate_n_allvertices", "")
        desc = desc.replace("_short", "").replace("_long", "")
        desc = desc.replace("dilepton", "Dilepton region,")
        desc = desc.replace("qcd_sideband", "QCD sideband,")
        if not "sideband" in desc:
            desc = desc.replace("qcd", "QCD-only events,")
        desc = desc.replace("201", "Run201")
        desc = desc.replace("_", " ")
        legend.AddEntry(histos[label], desc)

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)
    latex.SetTextAlign(13)
    latex.SetTextFont(52)
    latex.DrawLatex(0.18, 0.87, "%s tracks" % category)
           
    legend.Draw()

    stamp_plot()
    if not os.path.exists("%s/plots" % path): os.mkdir("%s/plots" % path)
    canvas.SaveAs("%s/plots/fakerate-1D-%s-%s-%s.pdf" % (path, variable, category, "-".join(regions)) )

    fin.Close()


if __name__ == "__main__":

    root_file = "fakerate.root"
    path = "output_fakerate_sideband"

    # do 1D fakerate comparison plots:
    for category in ["short", "long"]:
        for variable in ["n_allvertices", "HT", "MHT"]:
            for region in ["dilepton", "qcd", "qcd_sideband"]:
                if region == "dilepton":
                    variable = variable.replace("HT", "HT_cleaned")
                else:
                    variable = variable.replace("_cleaned", "")
                do_1D_plot(root_file, path, category, variable, regions = [region])

    # redo the 2D plots in a slightly nicer way:
    for region in ["dilepton", "qcd", "qcd_sideband"]:
        for data_type in ["Summer16", "Fall17", "2016", "2017", "2018"]:
            for category in ["short", "long"]:
                for variable in ["HT_n_allvertices"]:
                    if region == "dilepton":
                        variable = variable.replace("HT", "HT_cleaned")
                    else:
                        variable = variable.replace("_cleaned", "")
                    
                    hist_name = region + "/" + data_type + "/" + category + "/fakerate_" + variable

                    if "201" in data_type:
                        extra_text = "Run%s (%s region, %s tracks)" % (data_type, region, category)
                    else:
                        extra_text = "%s MC (%s region, %s tracks)" % (data_type, region, category)

                    do_2D_plot(root_file, hist_name, path, extra_text)

