#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *

def fakerate_map(path = "output/", variables = "HT_cleaned:n_allvertices", nBinsX=10, xmin=0, xmax=50, nBinsY=10, ymin=0, ymax=1000, rootfile = False, foldername = "dilepton", label = "mc", selected_sample = "Summer16", base_cuts = "PFCaloMETRatio<5", numerator_cuts = "", denominator_cuts = "", extra_text = "combined MC background"):

    fakes_numerator = get_histogram(variables, base_cuts + numerator_cuts + " && n_DT>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample = selected_sample)
    fakes_denominator = get_histogram(variables, base_cuts + denominator_cuts + " && n_DT==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample = selected_sample)

    try:
        print fakes_numerator.GetEntries()
        print fakes_denominator.GetEntries()
    except:
        print "Error while getting histogram!"
        return

    fout = TFile(rootfile, "update")
    fout.mkdir(foldername)
    fout.cd(foldername)

    fakes_numerator.SetName("%s_numerator_%s" % (foldername, label))
    fakes_numerator.Write()
    fakes_denominator.SetName("%s_denominator_%s" % (foldername, label))
    fakes_denominator.Write()

    fake_rate = fakes_numerator.Clone()
    fake_rate.Divide(fakes_denominator)
    fake_rate.SetName("%s_fake_rate_%s" % (foldername, label))
    fake_rate.SetTitle(";number of vertices; H_{T} (GeV); fake rate")
    fake_rate.GetZaxis().SetTitleOffset(1.5)
    fake_rate.GetZaxis().SetRangeUser(1e-6, 1e-1)
    fake_rate.SetName("%s_fake_rate_%s" % (foldername, label))
    fake_rate.Write()
  
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

    fake_rate.Draw("COLZ")
    latex.DrawLatex(0.18, 0.87, extra_text)
    stamp_plot()
    canvas.Write("%s_canvas_%s_%s" % (foldername, label, variables.replace(":", "-")))
    if not os.path.exists("plots"): os.mkdir("plots")
    canvas.SaveAs("plots/fakerate_%s_%s_%s.pdf" % (foldername, label, variables.replace(":", "-")))

    fout.Close()


def combine_fakerate_maps(fout, foldername):

    fout = TFile(rootfile, "update")

    histos = {}

    histos["%s_fake_rate_data_short" % foldername] = 0
    histos["%s_fake_rate_data_long" % foldername] = 0

    for period in ["2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H"]:
        histos["%s_fake_rate_%s_short" % (foldername, period)] = fout.Get("%s/%s_fake_rate_%s_short" % (foldername, foldername, period))
        histos["%s_fake_rate_%s_long" % (foldername, period)] = fout.Get("%s/%s_fake_rate_%s_long" % (foldername, foldername, period))

        if histos["%s_fake_rate_data_short" % foldername] == 0:
            histos["%s_fake_rate_data_short" % foldername] = histos["%s_fake_rate_%s_short" % (foldername, period)].Clone()
        else:
            histos["%s_fake_rate_data_short" % foldername].Add( histos["%s_fake_rate_%s_short" % (foldername, period)] )

        if histos["%s_fake_rate_data_long" % foldername] == 0:
            histos["%s_fake_rate_data_long" % foldername] = histos["%s_fake_rate_%s_long" % (foldername, period)].Clone()
        else:
            histos["%s_fake_rate_data_long" % foldername].Add( histos["%s_fake_rate_%s_long" % (foldername, period)] )

    #FIXME


if __name__ == "__main__":
    
    path = "output_fakerate_2016v2/"
    base_cuts = "PFCaloMETRatio<5"
    rootfile = "fakerate.root"

    selected_mc = "Summer16"
    #periods = ["2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H"]
    data_periods = ["2016"]

    cut_is_short_track = " && ((n_DT==1 && DT1_is_pixel_track == 1) || (n_DT==2 && DT1_is_pixel_track == 1 && DT2_is_pixel_track == 1)) "
    cut_is_long_track  = " && ((n_DT==1 && DT1_is_pixel_track == 0) || (n_DT==2 && DT1_is_pixel_track == 0 && DT2_is_pixel_track == 0)) "

    # get fake rate from dilepton region:
    fakerate_map(path = path, rootfile = rootfile, foldername = "dilepton", variables = "HT_cleaned:n_allvertices", base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_short_track, label = "bg_short", selected_sample = selected_mc, extra_text = "combined MC background, pixel-only tracks")
    fakerate_map(path = path, rootfile = rootfile, foldername = "dilepton", variables = "HT_cleaned:n_allvertices", base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_long_track, label = "bg_long", selected_sample = selected_mc, extra_text = "combined MC background, pixel+strips tracks")
    
    for period in data_periods:
        fakerate_map(path = path, rootfile = rootfile, foldername = "dilepton", variables = "HT_cleaned:n_allvertices", base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_short_track, label = period + "_short", selected_sample = "%s*SingleElectron" % period, extra_text = "Run%s SingleElectron, pixel-only tracks" % period)
        fakerate_map(path = path, rootfile = rootfile, foldername = "dilepton", variables = "HT_cleaned:n_allvertices", base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_long_track, label = period + "_long", selected_sample = "%s*SingleElectron" % period, extra_text = "Run%s SingleElectron, pixel+strips tracks" % period)

    # get fake rate from QCD-only events:
    fakerate_map(path = path, rootfile = rootfile, foldername = "qcd", variables = "HT:n_allvertices", base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_short_track, label = "bg_short", selected_sample = selected_mc + "*QCD", extra_text = "combined MC background, pixel-only tracks")
    fakerate_map(path = path, rootfile = rootfile, foldername = "qcd", variables = "HT:n_allvertices", base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_long_track, label = "bg_long", selected_sample = selected_mc + "*QCD", extra_text = "combined MC background, pixel+strips tracks")
    
    for period in data_periods:
        fakerate_map(path = path, rootfile = rootfile, foldername = "qcd", variables = "HT:n_allvertices", base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_short_track, label = period + "_short", selected_sample = "%s*JetHT" % period, extra_text = "Run%s JetHT, pixel-only tracks" % period)
        fakerate_map(path = path, rootfile = rootfile, foldername = "qcd", variables = "HT:n_allvertices", base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_long_track, label = period + "_long", selected_sample = "%s*JetHT" % period, extra_text = "Run%s JetHT, pixel+strips tracks" % period)
        

