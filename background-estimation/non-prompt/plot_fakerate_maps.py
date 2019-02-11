#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *

def get_fakerate(path = "output/", variable = "HT_cleaned:n_allvertices", nBinsX=10, xmin=0, xmax=50, nBinsY=10, ymin=0, ymax=1000, rootfile = False, foldername = "dilepton/bg/short", selected_sample = "Summer16", base_cuts = "PFCaloMETRatio<5", numerator_cuts = "", denominator_cuts = "", extra_text = "combined MC background"):

    if ":" in variable:
        plot2D = True
    else:
        plot2D = False
        
    if plot2D:
        fakes_numerator = get_histogram(variable, base_cuts + numerator_cuts + " && n_DT>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample = selected_sample)
        fakes_denominator = get_histogram(variable, base_cuts + denominator_cuts + " && n_DT==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample = selected_sample)
    else:
        fakes_numerator = get_histogram(variable, base_cuts + numerator_cuts + " && n_DT>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample = selected_sample)
        fakes_denominator = get_histogram(variable, base_cuts + denominator_cuts + " && n_DT==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample = selected_sample)

    try:
        print fakes_numerator.GetEntries()
        print fakes_denominator.GetEntries()
    except:
        print "Error while getting histogram!"
        return
        
    fout = TFile(rootfile, "update")
    fout.cd()
    gDirectory.mkdir(foldername)
    fout.cd(foldername)
    
    fake_rate = fakes_numerator.Clone()
    fake_rate.Divide(fakes_denominator)
    fake_rate.SetName("fakerate_%s" % (variable.replace(":", "_")))
    
    if plot2D:
        fake_rate.SetTitle(";%s; %s; fake rate"  % (variable.split(":")[0], variable.split(":")[1]))
    else:
        fake_rate.SetTitle(";%s; fake rate"  % variable)
    
    fake_rate.SetName("fakerate_%s" % (variable.replace(":", "_")))
    fake_rate.SetDirectory(gDirectory)
    fake_rate.Write()

    if plot2D:  
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
        canvas.Write("canvas_%s" % (variable.replace(":", "_")))
        if not os.path.exists("plots"): os.mkdir("plots")
        canvas.SaveAs("plots/fakerate_%s_%s.pdf" % (foldername.replace("/", "_"), variable.replace(":", "_")))

    fout.Close()


if __name__ == "__main__":
    
    path = "output_fakerate_2016v2/"
    base_cuts = "PFCaloMETRatio<5"
    rootfile = "fakerate_new.root"

    selected_mc = "Summer16"
    #data_periods = ["2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H", "2016"]
    data_periods = ["2016"]

    cut_is_short_track = " && ((n_DT==1 && DT1_is_pixel_track == 1) || (n_DT==2 && DT1_is_pixel_track == 1 && DT2_is_pixel_track == 1)) "
    cut_is_long_track  = " && ((n_DT==1 && DT1_is_pixel_track == 0) || (n_DT==2 && DT1_is_pixel_track == 0 && DT2_is_pixel_track == 0)) "

    # get fake rate from dilepton region:
    for variable in ["n_allvertices", "HT_cleaned:n_allvertices"]:

        get_fakerate(path = path, rootfile = rootfile, foldername = "dilepton/Summer16/short", variable = variable, base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_short_track, selected_sample = selected_mc, extra_text = "combined MC background, pixel-only tracks")    
        get_fakerate(path = path, rootfile = rootfile, foldername = "dilepton/Summer16/long", variable = variable, base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_long_track, selected_sample = selected_mc, extra_text = "combined MC background, pixel+strips tracks")
        
        for period in data_periods:
            get_fakerate(path = path, rootfile = rootfile, foldername = "dilepton/%s/short" % period, variable = variable, base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_short_track, selected_sample = "%s*SingleElectron" % period, extra_text = "Run%s SingleElectron, pixel-only tracks" % period)
            get_fakerate(path = path, rootfile = rootfile, foldername = "dilepton/%s/long" % period, variable = variable, base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_long_track, selected_sample = "%s*SingleElectron" % period, extra_text = "Run%s SingleElectron, pixel+strips tracks" % period)

    # get fake rate from QCD-only events:
    for variable in ["n_allvertices", "HT:n_allvertices"]:
        
        get_fakerate(path = path, rootfile = rootfile, foldername = "qcd/Summer16/short", variable = variable, base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_short_track, selected_sample = selected_mc + "*QCD", extra_text = "combined MC background, pixel-only tracks")
        get_fakerate(path = path, rootfile = rootfile, foldername = "qcd/Summer16/long", variable = variable, base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_long_track, selected_sample = selected_mc + "*QCD", extra_text = "combined MC background, pixel+strips tracks")
        
        for period in data_periods:
            get_fakerate(path = path, rootfile = rootfile, foldername = "qcd/%s/short" % period, variable = variable, base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_short_track, selected_sample = "%s*JetHT" % period, extra_text = "Run%s JetHT, pixel-only tracks" % period)
            get_fakerate(path = path, rootfile = rootfile, foldername = "qcd/%s/long" % period, variable = variable, base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_long_track, selected_sample = "%s*JetHT" % period, extra_text = "Run%s JetHT, pixel+strips tracks" % period)
        

