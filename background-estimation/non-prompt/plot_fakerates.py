#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *
import collections

def do_1D_plot(root_file, category, variable, tag, regions = [], data_periods = [], outfile = False, autoscaling = True, extra_text = ""):

    fin = TFile(root_file, "read")

    hist_names = []  
    histos = collections.OrderedDict()

    if category == "combined":
        categories = ["short", "long"]
    else:
        categories = [category]

    for region in regions:
        for i_category in categories:
            colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]
            for data_type in data_periods:
                color = colors.pop(0)
                hist_name = region + "_" + tag + "_" + i_category + "/" + data_type + "/fakerate_" + variable 
                hist_names.append(hist_name)
                label = hist_name.replace("/", "_")
                histos[label] = fin.Get(hist_name)
                histos[label].SetLineColor(color)
                histos[label].SetLineWidth(2)
                if "short" in i_category:
                    histos[label].SetLineStyle(1)
                elif "long" in i_category:
                    histos[label].SetLineStyle(2)
                if "Run201" in hist_name:
                    if "short" in i_category:
                        histos[label].SetMarkerStyle(20)
                    elif "long" in i_category:
                        histos[label].SetMarkerStyle(22)
                    histos[label].SetMarkerSize(1)
                    histos[label].SetMarkerColor(color)

    canvas = TCanvas("fakerate", "fakerate", 800, 800)  
    canvas.SetLeftMargin(0.14)
    canvas.SetLogy(True)
    
    legend = TLegend(0.55, 0.6, 0.85, 0.85)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)

    for i, label in enumerate(histos):

        if i == 0:
            if "Run201" in hist_name:
                histos[label].Draw("p")
            else:
                histos[label].Draw("hist e")
            histos[label].GetYaxis().SetRangeUser(1e-6,1e-2)
        else:
            if "Run201" in hist_name:
                histos[label].Draw("p same")
            else:    
                histos[label].Draw("hist e same")

        # make nice labels
        desc = ""
        period = ""
        if "Run2016" in label and "short" in label:
            desc = "short tracks, 2016 data"
            period = 2016
        elif "Run2016" in label and "long" in label:
            desc = "long tracks, 2016 data"
            period = 2016
        elif "Run2017" in label and "short" in label:
            desc = "short tracks, 2017 data"
            period = 2017
        elif "Run2017" in label and "long" in label:
            desc = "long tracks, 2017 data"
            period = 2017
        elif "short" in label:
            desc = "short tracks, MC"
        elif "long" in label:
            desc = "long tracks, MC"

        desc = label
        desc = desc.replace("qcd_lowMHT_loose6_", "")
        desc = desc.replace("_", "")
        desc = desc.replace("short", "short tracks, ")
        desc = desc.replace("long", "long tracks, ")
        desc = desc.replace("fakerateHT", "")
        desc = desc.replace("fakeratenallvertices", "")
        desc = desc.replace("fakeratetrackspt", "")
        legend.AddEntry(histos[label], desc)

    if autoscaling:
        global_ymin = 1e10
        global_ymax = 1e-10
        for histo in histos:
            current_ymin = 1e10
            for ibin in range(histos[histo].GetNbinsX()):
               value = histos[histo].GetBinContent(ibin)
               if value < current_ymin and value != 0:
                    current_ymin = value
            if current_ymin < global_ymin:
                global_ymin = current_ymin
            if histos[histo].GetMaximum() > global_ymax:
                global_ymax = histos[histo].GetMaximum()
    
        ymin = global_ymin * 1e-1
        ymax = global_ymax * 1e1

        for label in histos:
            histos[label].GetYaxis().SetRangeUser(ymin, ymax)


    for label in histos:
        if "vertices" in variable:
            histos[label].GetXaxis().SetRangeUser(0, 50)

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)
    latex.SetTextAlign(13)
    latex.SetTextFont(52)
    latex.DrawLatex(0.18, 0.87, extra_text)
           
    legend.Draw()

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)

    if period == 2016:
        lumi = 13.62
    elif period == 2017:
        lumi = 5.36
    latex.DrawLatex(0.90, 0.91, "%.1f fb^{-1} (13 TeV)" % lumi)


    stamp_plot()
    canvas.SetTitle("fakerate-%s-%s-%s-%s" % (variable, category, tag, period) )    
    canvas.SaveAs("plots/fakerate-%s-%s-%s-%s.pdf" % (variable, category, tag, period) )

    if outfile:
        fout = TFile(outfile, "update")
        canvas.Write()
        fout.Close()

    fin.Close()


def do_2D_plot(root_file, hist_name, extra_text, outfile = False, ratio = False):

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

    if ratio:
        if "Run2016G" in hist_name:
            fake_rate_mc = fin.Get(hist_name.replace("Run2016G", "Summer16"))
            fake_rate.Divide(fake_rate_mc)
        elif "Run2017" in hist_name:
            print "Getting", hist_name.replace("Run2017", "Fall17")
            fake_rate_mc = fin.Get(hist_name.replace("Run2017", "Fall17"))
            fake_rate.Divide(fake_rate_mc)

        fake_rate.SetTitle(";number of vertices;H_{T} (GeV);Data/MC")
        fake_rate.GetZaxis().SetRangeUser(0,2)
        hist_name += "_ratio"
        canvas.SetLogz(False)
    else:
        canvas.SetLogz(True)
        fake_rate.GetZaxis().SetRangeUser(1e-4,1e0)

    if "tracks_phi" in hist_name:
        #fake_rate.Rebin2D(2, 2)
        gStyle.SetPalette(1)
        fake_rate.GetZaxis().SetRangeUser(1e-3,1e0)
 
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
    #fake_rate.GetZaxis().SetRangeUser(1e-6, 1e-1)
    fake_rate.Draw("COLZ")
    
    #latex.DrawLatex(0.18, 0.87, extra_text)

    stamp_plot()
    canvas.SetTitle("fakeratemap_" + hist_name.replace("/", "_").replace("fakerate_", "") + "_" + tag)
    canvas.SaveAs("plots/fakeratemap_" + hist_name.replace("/", "_").replace("fakerate_", "") + "_" + tag + ".pdf")

    if outfile:
        fout = TFile(outfile, "update")
        canvas.Write()
        fout.Close()

    fin.Close()


if __name__ == "__main__":

    root_file = "fakerate.root"
    out_file = False

    # 1D plots
    for data_type in ["Summer16", "Fall17"]:
        # do 1D fakerate comparison plots:
        #for category in ["combined", "short", "long"]:
        for category in ["combined"]:
            for variable in ["n_allvertices", "HT", "MHT", "n_btags", "n_goodjets", "tracks_pt"]:
                for tag in ["loose6"]:

                    if "Summer16" in data_type:
                        data_periods = [data_type, "Run2016C", "Run2016E", "Run2016F", "Run2016G", "Run2016H"]
                    elif "Fall17" in data_type:
                        data_periods = [data_type, "Run2017"]

                    print data_type, category, variable, tag
                    do_1D_plot(root_file, category, variable, tag, regions = ["qcd_lowMHT"], data_periods = data_periods, outfile = out_file)

    # 2D plots
    # redo the 2D plots in a slightly nicer way:
    for variable in ["HT_n_allvertices", "tracks_eta_tracks_phi"]:
        for region in ["qcd_lowMHT"]:
            for data_type in ["Summer16", "Run2016", "Run2016G", "Fall17", "Run2017", "Run2018"]:
                for category in ["short", "long"]:
                    for tag in ["loose6"]:
                        if "interpolated" in variable and region == "dilepton":
                            variable = variable.replace("HT", "HT_cleaned")
                        else:
                            variable = variable.replace("_cleaned", "")
                        
                        hist_name = region + "_" + tag + "_" + category + "/" + data_type + "/fakerate_" + variable

                        if "201" in data_type:
                            extra_text = "Run%s (%s region, %s tracks)" % (data_type, region, category)
                        else:
                            extra_text = "%s MC (%s region, %s tracks)" % (data_type, region, category)

                        do_2D_plot(root_file, hist_name, extra_text, outfile = out_file)
                        if "2016G" in data_type or "2017" in data_type:
                            do_2D_plot(root_file, hist_name, extra_text, outfile = out_file, ratio = True)

