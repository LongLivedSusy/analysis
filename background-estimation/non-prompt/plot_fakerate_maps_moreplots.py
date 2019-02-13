#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *

def do_2D_plot(root_file, hist_name, path, extra_text):

    print hist_name

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


def do_1D_plot(root_file, hist_name, path, extra_text):

    print hist_name

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


if __name__ == "__main__":

    root_file = "fakerate_newrelease.root"
    path = "output_fakerate_2016v2_sideband"

    # redo the 2D plots in a slightly nicer way:
    for region in ["dilepton", "qcd", "qcd_sideband"]:
        for data_type in ["Summer16", "Fall17", "2016", "2017", "2018"]:
            for category in ["short", "long"]:
                for variable in ["HT_n_allvertices"]:
                    if region == "dilepton":
                        variable = variable.replace("HT", "HT_cleaned")
                    hist_name = region + "/" + data_type + "/" + category + "/fakerate_" + variable

                    if "201" in data_type:
                        extra_text = "Run%s (%s region, %s tracks)" % (data_type, region, category)
                    else:
                        extra_text = "%s MC (%s region, %s tracks)" % (data_type, region, category)

                    do_2D_plot(root_file, hist_name, path, extra_text)

    # do 1D fakerate comparison plots:



