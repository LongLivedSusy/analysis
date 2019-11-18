#!/bin/env python
from __future__ import division
from optparse import OptionParser
import os
from ROOT import *
import plotting
import uuid
import GridEngineTools
import collections
from tools.tags import tags

def get_interpolated_histogram(histo):

    graph = TGraph2D()

    nBinsX = histo.GetXaxis().GetNbins()
    nBinsY = histo.GetYaxis().GetNbins()

    xmin = histo.GetXaxis().GetXmin()
    xmax = histo.GetXaxis().GetXmax()
    ymin = histo.GetYaxis().GetXmin()
    ymax = histo.GetYaxis().GetXmax()

    for xbin in range(1, nBinsX + 1):
        for ybin in range(1, nBinsY + 1):            
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


def get_fakerate(path, variable, rootfile, foldername, base_cuts, numerator_cuts, denominator_cuts, selected_sample, extra_text, binning, threads, nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, xlabel=False, ylabel=False):

    print "## Getting fake rate for", variable, selected_sample, extra_text

    plot2D = False
    if ":" in variable:
        plot2D = True
                 
    if not plot2D:
        nBinsX = binning[variable.replace("_cleaned", "")][0]
        xmin = binning[variable.replace("_cleaned", "")][1]
        xmax = binning[variable.replace("_cleaned", "")][2]
    else:
        variable1 = variable.split(":")[1]
        variable2 = variable.split(":")[0]
        nBinsX = binning[variable1.replace("_cleaned", "")][0]
        xmin = binning[variable1.replace("_cleaned", "")][1]
        xmax = binning[variable1.replace("_cleaned", "")][2]
        nBinsY = binning[variable2.replace("_cleaned", "")][0]
        ymin = binning[variable2.replace("_cleaned", "")][1]
        ymax = binning[variable2.replace("_cleaned", "")][2]
        
    if plot2D:
        fakes_numerator = plotting.get_histogram(variable, base_cuts + numerator_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample=selected_sample, threads=threads)
        fakes_denominator = plotting.get_histogram(variable, base_cuts + denominator_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample=selected_sample, threads=threads)
    else:
        fakes_numerator = plotting.get_histogram(variable, base_cuts + numerator_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample, threads=threads)
        fakes_denominator = plotting.get_histogram(variable, base_cuts + denominator_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample, threads=threads)

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
    
    fake_rate.SetName("fakerate_%s" % (variable.replace(":", "_").replace("_cleaned", "")))
    fake_rate.SetDirectory(gDirectory)
    fake_rate.Write()
    
    # also save interpolated histogram:
    if plot2D:
        fake_rate_interpolated = get_interpolated_histogram(fake_rate)
        fake_rate_interpolated.SetName("fakerate_%s_interpolated" % (variable.replace(":", "_")))
        fake_rate_interpolated.SetDirectory(gDirectory)
        fake_rate_interpolated.Write()

    fout.Close()


def get_configurations(threads):

    path = "../skims/current/"
    rootfile = "/fakerate.root"

    binning = collections.OrderedDict()    

    binning["tracks_pt"] = [20, 0, 1000]
    binning["HT"] = [10, 0, 1000]
    binning["MHT"] = [10, 0, 1000]
    binning["n_allvertices"] = [20, 0, 100]
    binning["n_goodjets"] = [50, 0, 50]
    binning["n_btags"] = [10, 0, 10]
    binning["MinDeltaPhiMhtJets"] = [100, 0, 5]
    binning["tracks_eta"] = [60, -2.5, 2.5]
    binning["tracks_phi"] = [60, -3.2, 3.2]

    selected_datasets = ["Summer16", "Fall17", "Run2016", "Run2017", "Run2018", "Run2016B", "Run2016C", "Run2016D", "Run2016E", "Run2016F", "Run2016G", "Run2016H", "Run2017B", "Run2017C", "Run2017D", "Run2017E", "Run2017F", "Run2018A", "Run2018B", "Run2018C", "Run2018D"]

    variables = [
                 #"tracks_pt",
                 #"HT",
                 #"MHT",
                 #"n_goodjets",
                 #"n_allvertices",
                 #"n_btags",
                 #"MinDeltaPhiMhtJets",
                 "HT:n_allvertices",
                 #"tracks_eta:tracks_phi",
                ]
    
    regions = collections.OrderedDict()
    regions["qcd_lowMHT"] = " && MHT<200"
    #regions["qcd_sideband"] = " && MHT>100 && MHT<200"
    
    configurations = []

    for label in tags.tags:

        numerator_cuts = tags.tags[label]["SR"]
        denominator_cuts = tags.tags[label]["CR"]
        base_cuts = tags.tags[label]["base_cuts"]

        for selected_dataset in selected_datasets:
            for variable in variables:          
                for region in regions:
                
                    cuts = base_cuts + regions[region]

                    current_selected_dataset = selected_dataset
                    if "Run201" in selected_dataset:
                        # running on data:
                        if "qcd" in region and "JetHT" not in current_selected_dataset:
                            current_selected_dataset += "*JetHT"
                        elif "dilepton" in region and "Single" not in current_selected_dataset:
                            current_selected_dataset += "*Single"
                        else:
                            print "Something wrong"
                            quit()
                    else:
                        # running on MC
                        if "qcd" in region and "QCD" not in current_selected_dataset:
                            current_selected_dataset += "*QCD"
                        elif "dilepton" in region and "DYJetsToLL" not in current_selected_dataset:
                            current_selected_dataset += "*DYJetsToLL"
                        else:
                            print "Something wrong"
                            quit()

                    current_variable = variable
                    if "dilepton" in region:
                        current_variable = variable.replace("HT", "HT_cleaned").replace("n_jets", "n_jets_cleaned").replace("n_btags", "n_btags_cleaned").replace("MinDeltaPhiMhtJets", "MinDeltaPhiMhtJets_cleaned")                    
                    folder = selected_dataset.split(".")[0]
                     
                    configurations.append([path, current_variable, rootfile, "%s_%s/%s" % (region, label, folder), cuts, numerator_cuts, denominator_cuts, current_selected_dataset, "MC, pixel-only tracks", binning, threads])   

    return configurations


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest="index", default=False)
    parser.add_option("--threads", dest="threads", default=3)
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--start", dest="start", action="store_true")
    (options, args) = parser.parse_args()

    configurations = get_configurations(options.threads)

    if options.index:
        if os.path.exists("fakerate_pt%s.root" % options.index):
            print "Already processed :)"
        else:
            configurations[int(options.index)][2] = "fakerate_pt%s.root" % options.index
            get_fakerate(*configurations[int(options.index)])
        
    elif options.hadd:
        os.system("hadd -f fakerate.root fakerate_pt*root && rm fakerate_pt*root")

    else:
        commands = []
        for i in range(len(configurations)):
            commands.append("./get_fakerate.py --index %s" % i)
        GridEngineTools.runParallel(commands, options.runmode, condorDir = "get_fakerate.condor", confirm=not options.start)

        if "multi" in options.runmode:
            print "Finished, writing fake rate histograms to single fakerate.root..."
            os.system("hadd -f fakerate.root fakerate_pt*root && rm fakerate_pt*root")

