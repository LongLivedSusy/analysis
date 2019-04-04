#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *

def get_fakerate(path, variable, rootfile, foldername, base_cuts, numerator_cuts, selected_sample, extra_text, nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, xlabel=False, ylabel=False, denominator_cuts=""):

    print "## Doing", variable, selected_sample, extra_text

    if ":" in variable:
        plot2D = True
    else:
        plot2D = False
        
    binning = {
                "n_DT": [1, 0, 10],
                "HT": [10, 0, 1000],
                "HT_cleaned": [10, 0, 1000],
                "MHT": [10, 0, 1000],
                "MHT_cleaned": [10, 0, 1000],
                "n_allvertices": [20, 0, 100],
                "NumInteractions": [20, 0, 100],
                "n_jets": [50, 0, 50],
                "n_jets_cleaned": [50, 0, 50],
                "n_btags": [50, 0, 50],
                "n_btags_cleaned": [50, 0, 50],
                "MinDeltaPhiMhtJets": [100, 0, 5],                    
                "MinDeltaPhiMhtJets_cleaned": [100, 0, 5],
    }
    
    if not plot2D:
        nBinsX = binning[variable][0]
        xmin = binning[variable][1]
        xmax = binning[variable][2]
    else:
        variable1 = variable.split(":")[1]
        variable2 = variable.split(":")[0]
        nBinsX = binning[variable1][0]
        xmin = binning[variable1][1]
        xmax = binning[variable1][2]
        nBinsY = binning[variable2][0]
        ymin = binning[variable2][1]
        ymax = binning[variable2][2]
        
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
    rootfile = "fakerate_newrelease_v3.root"

    for configuration in ["2016MC"]:

        if configuration == "2016MC":
            path = "output_fakerate_v3_merged/"
            selected_mc = "Summer16"
            data_periods = []

        if configuration == "2016":
            path = "output_fakerate_v3_merged/"
            selected_mc = "Summer16"
            data_periods = ["2016"]
        
        if configuration == "2017/2018":
            path = "output_fakerate_v3_merged/"
            selected_mc = "Fall17"
            data_periods = ["2017", "2018"]
        
        cut_is_short_track = " && ((n_DT==1 && DT1_passpionveto == 1 && DT1_is_pixel_track == 1) || (n_DT==2 && DT1_passpionveto == 1 && DT2_passpionveto == 1 && DT1_is_pixel_track == 1 && DT2_is_pixel_track == 1)) "
        cut_is_long_track  = " && ((n_DT==1 && DT1_passpionveto == 1 && DT1_is_pixel_track == 0) || (n_DT==2 && DT1_passpionveto == 1 && DT2_passpionveto == 1 && DT1_is_pixel_track == 0 && DT2_is_pixel_track == 0)) "
                
        for variable in ["n_DT", "HT:n_allvertices", "MHT:n_allvertices", "n_allvertices", "MHT", "HT", "NumInteractions", "n_jets", "n_btags", "MinDeltaPhiMhtJets"]:
                
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
            
            # get fake rate from dilepton region:
            variable_cleaned = variable.replace("HT", "HT_cleaned").replace("n_jets", "n_jets_cleaned").replace("n_btags", "n_btags_cleaned").replace("MinDeltaPhiMhtJets", "MinDeltaPhiMhtJets_cleaned") 
            
            get_fakerate(path, variable_cleaned, rootfile, "dilepton/%s/short" % selected_mc, base_cuts + " && dilepton_CR==1", cut_is_short_track, selected_mc, "combined MC background, pixel-only tracks")    
            get_fakerate(path, variable_cleaned, rootfile, "dilepton/%s/long" % selected_mc, base_cuts + " && dilepton_CR==1", cut_is_long_track, selected_mc, "combined MC background, pixel+strips tracks")
            
            for period in data_periods:
                get_fakerate(path, variable_cleaned, rootfile, "dilepton/%s/short" % period, base_cuts + " && dilepton_CR==1", cut_is_short_track, "%s*SingleElectron" % period, "Run%s SingleElectron, pixel-only tracks" % period)
                get_fakerate(path, variable_cleaned, rootfile, "dilepton/%s/long" % period, base_cuts + " && dilepton_CR==1", cut_is_long_track, "%s*SingleElectron" % period, "Run%s SingleElectron, pixel+strips tracks" % period)
            
