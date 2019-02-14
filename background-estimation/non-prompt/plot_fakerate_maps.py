#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *

def get_fakerate(path, variable, rootfile, foldername, base_cuts, numerator_cuts, selected_sample, extra_text, nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, xlabel = False, ylabel = False, denominator_cuts = ""):

    print "## Doing", variable, selected_sample, extra_text

    if ":" in variable:
        plot2D = True
    else:
        plot2D = False

    # set default binning:
    if not nBinsX and plot2D and "short" in foldername:
        nBinsX=5; xmin=0; xmax=50; nBinsY=5; ymin=0; ymax=1000
    elif not nBinsX and plot2D and "long" in foldername:
        nBinsX=10; xmin=0; xmax=50; nBinsY=10; ymin=0; ymax=1000
    elif not nBinsX and (variable == "HT" or variable == "HT_cleaned" or variable == "MHT" or variable == "MHT_cleaned"):
        nBinsX=20; xmin=0; xmax=1000
    elif not nBinsX:
        nBinsX=10; xmin=0; xmax=50; nBinsY=10; ymin=0; ymax=1000

    if plot2D:
        fakes_numerator = get_histogram(variable, base_cuts + numerator_cuts + " && n_DT>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample=selected_sample)
        fakes_denominator = get_histogram(variable, base_cuts + denominator_cuts + " && n_DT==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample=selected_sample)
    else:
        fakes_numerator = get_histogram(variable, base_cuts + numerator_cuts + " && n_DT>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample)
        fakes_denominator = get_histogram(variable, base_cuts + denominator_cuts + " && n_DT==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample)

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

    labels = {"HT": "H_{T} (GeV)", "MHT": "missing H_{T} (GeV)", "HT_cleaned": "cleaned H_{T} (GeV)", "MHT_cleaned": "cleaned missing H_{T} (GeV)", "n_allvertices": "number of vertices"}
    if not xlabel:
        xlabel = variable.split(":")[0]
        if xlabel in labels:
            xlabel = labels[xlabel]
    if not ylabel and plot2D:
        ylabel = variable.split(":")[1]
        if ylabel in labels:
            ylabel = labels[ylabel]

    if plot2D:
        fake_rate.SetTitle(";%s; %s; fake rate"  % (ylabel, xlabel))
    else:
        fake_rate.SetTitle(";%s; fake rate" % xlabel)
    
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
        if not os.path.exists("%s/plots" % path): os.mkdir("%s/plots" % path)
        canvas.SaveAs("%s/plots/fakeratemap_%s_%s.pdf" % (path, foldername.replace("/", "_"), variable.replace(":", "_")))

    fout.Close()


if __name__ == "__main__":

    base_cuts = "PFCaloMETRatio<5"    
    rootfile = "fakerate_newrelease.root"

    for configuration in ["2017/2018", "2016"]:

        if configuration == "2016":
            path = "output_fakerate_sideband/"
            selected_mc = "Summer16"
            data_periods = ["2016"]
        
        if configuration == "2017/2018":
            path = "output_fakerate_sideband/"
            selected_mc = "Fall17"
            data_periods = ["2017", "2018"]
        
        cut_is_short_track = " && ((n_DT==1 && DT1_is_pixel_track == 1) || (n_DT==2 && DT1_is_pixel_track == 1 && DT2_is_pixel_track == 1)) "
        cut_is_long_track  = " && ((n_DT==1 && DT1_is_pixel_track == 0) || (n_DT==2 && DT1_is_pixel_track == 0 && DT2_is_pixel_track == 0)) "
        
        #for variable in ["HT:n_allvertices", "n_allvertices"]:
        #for variable in ["MHT", "HT"]:
        for variable in ["MHT:n_allvertices", "HT:n_NVtx", "n_NVtx"]:
        
            # get fake rate from dilepton region:
            get_fakerate(path, variable.replace("HT", "HT_cleaned"), rootfile, "dilepton/%s/short" % selected_mc, base_cuts + " && dilepton_CR==1", cut_is_short_track, selected_mc, "combined MC background, pixel-only tracks")    
            get_fakerate(path, variable.replace("HT", "HT_cleaned"), rootfile, "dilepton/%s/long" % selected_mc, base_cuts + " && dilepton_CR==1", cut_is_long_track, selected_mc, "combined MC background, pixel+strips tracks")
            
            for period in data_periods:
                get_fakerate(path, variable.replace("HT", "HT_cleaned"), rootfile, "dilepton/%s/short" % period, base_cuts + " && dilepton_CR==1", cut_is_short_track, "%s*SingleElectron" % period, "Run%s SingleElectron, pixel-only tracks" % period)
                get_fakerate(path, variable.replace("HT", "HT_cleaned"), rootfile, "dilepton/%s/long" % period, base_cuts + " && dilepton_CR==1", cut_is_long_track, "%s*SingleElectron" % period, "Run%s SingleElectron, pixel+strips tracks" % period)
        
            # get fake rate from QCD-only events:
            get_fakerate(path, variable, rootfile, "qcd/%s/short" % selected_mc, base_cuts + " && qcd_CR==1", cut_is_short_track, selected_mc + "*QCD", "combined MC background, pixel-only tracks")
            get_fakerate(path, variable, rootfile, "qcd/%s/long" % selected_mc, base_cuts + " && qcd_CR==1", cut_is_long_track, selected_mc + "*QCD", "combined MC background, pixel+strips tracks")
            
            for period in data_periods:
                get_fakerate(path, variable, rootfile, "qcd/%s/short" % period, base_cuts + " && qcd_CR==1", cut_is_short_track, "%s*JetHT" % period, "Run%s JetHT, pixel-only tracks" % period)
                get_fakerate(path, variable, rootfile, "qcd/%s/long" % period, base_cuts + " && qcd_CR==1", cut_is_long_track, "%s*JetHT" % period, "Run%s JetHT, pixel+strips tracks" % period)
                
            # get fake rate from QCD sideband region:          
            get_fakerate(path, variable, rootfile, "qcd_sideband/%s/short" % selected_mc, base_cuts + " && qcd_sideband_CR==1", cut_is_short_track, selected_mc + "*QCD", "combined MC background, pixel-only tracks")
            get_fakerate(path, variable, rootfile, "qcd_sideband/%s/long" % selected_mc, base_cuts + " && qcd_sideband_CR==1", cut_is_long_track, selected_mc + "*QCD", "combined MC background, pixel+strips tracks")
            
            for period in data_periods:
                get_fakerate(path, variable, rootfile, "qcd_sideband/%s/short" % period, base_cuts + " && qcd_sideband_CR==1", cut_is_short_track, "%s*JetHT" % period, "Run%s JetHT, pixel-only tracks" % period)
                get_fakerate(path, variable, rootfile, "qcd_sideband/%s/long" % period, base_cuts + " && qcd_sideband_CR==1", cut_is_long_track, "%s*JetHT" % period, "Run%s JetHT, pixel+strips tracks" % period)
        
