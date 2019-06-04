#!/bin/env python
from __future__ import division
from optparse import OptionParser
import os
from ROOT import *
from plotting import *
import uuid

def save_2d_plots(fake_rate, fake_rate_interpolated):

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
    
    for i, histogram in enumerate([fake_rate, fake_rate_interpolated]):
        histogram.GetZaxis().SetTitleOffset(1.5)
        histogram.GetZaxis().SetRangeUser(1e-6, 1e-1)
        histogram.Draw("COLZ")
        latex.DrawLatex(0.18, 0.87, extra_text)
        stamp_plot()
        if i == 0:
            canvas.Write("canvas_%s" % (variable.replace(":", "_")))
            if not os.path.exists("%s/plots" % path): os.mkdir("%s/plots" % path)
            canvas.SaveAs("%s/plots/fakeratemap_%s_%s.pdf" % (path, foldername.replace("/", "_"), variable.replace(":", "_")))
        else:
            canvas.Write("canvas_%s_interpolated" % (variable.replace(":", "_")))
            if not os.path.exists("%s/plots" % path): os.mkdir("%s/plots" % path)
            canvas.SaveAs("%s/plots/fakeratemap_%s_%s_interpolated.pdf" % (path, foldername.replace("/", "_"), variable.replace(":", "_")))


def get_interpolated_histogram(histo):

    graph = TGraph2D()

    nBinsX = histo.GetXaxis().GetNbins()
    nBinsY = histo.GetYaxis().GetNbins()

    xmin = histo.GetXaxis().GetXmin()
    xmax = histo.GetXaxis().GetXmax()
    ymin = histo.GetYaxis().GetXmin()
    ymax = histo.GetYaxis().GetXmax()

    for xbin in range(1, nBinsX + 2):
        for ybin in range(1, nBinsY + 2):            
            xval = histo.GetXaxis().GetBinLowEdge(xbin)
            yval = histo.GetYaxis().GetBinLowEdge(ybin)
            zval = histo.GetBinContent(xbin, ybin)
            if zval > 0:
                graph.SetPoint(graph.GetN(), xval, yval, zval)

    hName = str(uuid.uuid1()).replace("-", "")
    interpolated_histo = TH2F(hName, hName, nBinsX, xmin, xmax, nBinsY, ymin, ymax)
    
    graph.SetHistogram(interpolated_histo)
    graph.Draw("surf4")
    interpolated_histo = graph.GetHistogram()
    interpolated_histo.SetDirectory(0)
         
    return interpolated_histo


def get_fakerate(path, variable, rootfile, foldername, base_cuts, numerator_cuts, denominator_cuts, selected_sample, extra_text, binning, nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, xlabel=False, ylabel=False):

    print "## Doing", variable, selected_sample, extra_text

    plot2D = False
    if ":" in variable:
        plot2D = True
                 
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
        fakes_numerator = get_histogram(variable, base_cuts + numerator_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample=selected_sample)
        fakes_denominator = get_histogram(variable, base_cuts + denominator_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample=selected_sample)
    else:
        fakes_numerator = get_histogram(variable, base_cuts + numerator_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample)
        fakes_denominator = get_histogram(variable, base_cuts + denominator_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample)

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
    
    # also save interpolated histogram:
    if plot2D:
        fake_rate_interpolated = get_interpolated_histogram(fake_rate)
        fake_rate_interpolated.SetName("fakerate_%s_interpolated" % (variable.replace(":", "_")))
        fake_rate_interpolated.SetDirectory(gDirectory)
        fake_rate_interpolated.Write()

    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest="inputfiles")
    (options, args) = parser.parse_args()

    ### start of configuration ###

    path = "output_skim_31_fakerate_merged/"
    rootfile = path + "/fakerate.root"
    
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

    regioncuts = {
                    "tight": {
                                "base_cuts" = "passesUniversalSelection==1",
                                "cut_is_short_track": " && tracks_is_pixel_track==1 ",
                                "cut_is_long_track": " && tracks_is_pixel_track==0 ",
                                "numerator_cuts": " && tracks_tagged_bdt>=1 ",
                                "denominator_cuts": " && tracks_tagged_bdt==0",
                              },
                    "loose1": {
                                "base_cuts" = "passesUniversalSelection==1",
                                "cut_is_short_track": " && tracks_is_pixel_track==1 ",
                                "cut_is_long_track": " && tracks_is_pixel_track==0 ",
                                "numerator_cuts": " && tracks_tagged_bdt_loose>=1 && tracks_dxyVtx<=0.01",
                                "denominator_cuts": " && tracks_tagged_bdt_loose>=1 && tracks_dxyVtx>0.01 && tracks_dxyVtx<0.25",
                              },
                    "loose2": {
                                "base_cuts" = "passesUniversalSelection==1",
                                "cut_is_short_track": " && tracks_is_pixel_track==1 ",
                                "cut_is_long_track": " && tracks_is_pixel_track==0 ",
                                "numerator_cuts": " && tracks_tagged_bdt_loose>=1 && tracks_dxyVtx<=0.02",
                                "denominator_cuts": " && tracks_tagged_bdt_loose>=1 && tracks_dxyVtx>0.02 && tracks_dxyVtx<0.25",
                              },
                 }

    selected_datasets = ["Summer16", "Fall17", "Run2016", "Run2017", "Run2018"]
    variables = ["HT", "n_allvertices", "HT:n_allvertices"]
    regions = {
               "dilepton": " && dilepton_invmass>0",
               "qcd": " && qcd_CR==1",
               "qcd_sideband": " && qcd_sideband_CR==1",
              }


    ### end of configuration ###
    
    counter = 0
    total_number_of_combinations = len(selected_datasets) * len(variables) * len(regions) * len(regioncuts)

    for label in regioncuts:

        cut_is_short_track = regioncuts[label]["cut_is_short_track"]
        cut_is_long_track = regioncuts[label]["cut_is_long_track"]
        numerator_cuts = regioncuts[label]["numerator_cuts"]
        denominator_cuts = regioncuts[label]["denominator_cuts"]
        base_cuts = regioncuts[label]["base_cuts"]

        for selected_dataset in selected_datasets:
            for variable in variables:          
                for region in regions:
                
                    cuts = base_cuts + regions[region]

                    current_selected_dataset = selected_dataset
                    if "Run201" in selected_dataset:
                        # running on data
                        if "qcd" in region:
                            current_selected_dataset += "*JetHT"
                        elif "dilepton" in region:
                            current_selected_dataset += "*Single"
                    else:
                        # running on MC
                        if "qcd" in region:
                            current_selected_dataset += "*QCD"

                    current_variable = variable
                    if "dilepton" in region:
                        current_variable = variable.replace("HT", "HT_cleaned").replace("n_jets", "n_jets_cleaned").replace("n_btags", "n_btags_cleaned").replace("MinDeltaPhiMhtJets", "MinDeltaPhiMhtJets_cleaned")                    

                    counter += 1; print "\n Getting fake rate %s / %s \n" % (counter, total_number_of_combinations)
                    get_fakerate(path, current_variable, rootfile, "%s_%s/%s" % (region, label, selected_dataset), cuts, numerator_cuts, denominator_cuts, current_selected_dataset, "MC", binning)

                    counter += 1; print "\n Getting fake rate %s / %s \n" % (counter, total_number_of_combinations)
                    get_fakerate(path, current_variable, rootfile, "%s_%s_short/%s" % (region, label, selected_dataset), cuts + cut_is_short_track, numerator_cuts, denominator_cuts, current_selected_dataset, "MC, pixel-only tracks", binning)

                    counter += 1; print "\n Getting fake rate %s / %s \n" % (counter, total_number_of_combinations)
                    get_fakerate(path, current_variable, rootfile, "%s_%s_long/%s" % (region, label, selected_dataset), cuts + cut_is_long_track, numerator_cuts, denominator_cuts, current_selected_dataset, "MC, pixel+strips tracks", binning)
                    
