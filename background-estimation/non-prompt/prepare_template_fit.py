#!/bin/env python
from __future__ import division
from optparse import OptionParser
import os
from ROOT import *
from plotting import *
import uuid
from GridEngineTools import runParallel
import collections

def get_histos(config, index):

    histos = collections.OrderedDict()
    for label in config:
        histos[label] = get_histogram(config[label])

        
def get_configurations():

    configurations = collections.OrderedDict()

    path = "output_skim_11_merged"
    mc_background = "Summer16.DYJetsToLL|Summer16.QCD|Summer16.WJetsToLNu|Summer16.ZJetsToNuNu_HT|Summer16.WW_TuneCUETP8M1|Summer16.WZ_TuneCUETP8M1|Summer16.ZZ_TuneCUETP8M1|Summer16.TTJets_TuneCUETP8M1_13TeV"

    histos = collections.OrderedDict()

    variables = {
                  "tracks_massfromdeDxPixel":  [" && tracks_is_pixel_track==1 ", 50, 0, 5000],
                  "tracks_massfromdeDxStrips": [" && tracks_is_pixel_track==0 ", 50, 0, 5000],
                }

    cuts = {
             "base":        "passesUniversalSelection==1 && MHT>250 && MinDeltaPhiMhtJets>0.3 && n_jets>0",
             "noleptons":   "passesUniversalSelection==1 && MHT>250 && MinDeltaPhiMhtJets>0.3 && n_jets>0 && n_leptons==0",
           }

    tags = {
             "loose1":      {"short": " && tracks_mva_bdt_loose>0 ", "long": " && tracks_mva_bdt_loose>0 ", "track_SR": " && tracks_dxyVtx<=0.01 ", "track_CR": " && tracks_dxyVtx>0.01 "},
           }

    for variable in variables:

        for label in cuts:

            for tag in tags:

                control_region = cuts[label]
                track_selection = variables[variable][0]
                if "pixel_track==1" in track_selection:
                    track_selection += tags[tag]["short"]
                elif "pixel_track==0" in track_selection:
                    track_selection += tags[tag]["long"]
              
                nBinsX = variables[variable][1]
                xmin = variables[variable][2]
                xmax = variables[variable][3]

                fakelike           = control_region + track_selection + tags[tag]["track_CR"]
                promptlike         = control_region + track_selection + tags[tag]["track_SR"] + " && tracks_is_reco_lepton==1 "
                background_tracks  = control_region + track_selection + tags[tag]["track_SR"]
                signal_tracks      = control_region + track_selection + tags[tag]["track_SR"]

                configurations["%s_%s_bg_%s" % (variable, tag, label)] =             [variable, background_tracks, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample=mc_background]
                configurations["%s_%s_promptlike_%s" % (variable, tag, label)] =     [variable, promptlike, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample=mc_background]
                configurations["%s_%s_fakelike_%s" % (variable, tag, label)] =       [variable, fakelike, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample=mc_background]
                configurations["%s_%s_signal_ctau10_%s" % (variable, tag, label)] =  [variable, signal_tracks, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample="Summer16.g1800_chi1400_27_200970_step4_10AODSIM"]
                configurations["%s_%s_signal_ctau30_%s" % (variable, tag, label)] =  [variable, signal_tracks, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample="Summer16.g1800_chi1400_27_200970_step4_30AODSIM"]
                configurations["%s_%s_signal_ctau50_%s" % (variable, tag, label)] =  [variable, signal_tracks, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample="Summer16.g1800_chi1400_27_200970_step4_50AODSIM"]
                configurations["%s_%s_signal_ctau100_%s" % (variable, tag, label)] = [variable, signal_tracks, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample="Summer16.g1800_chi1400_27_200970_step4_100AODSIM"]

    return configurations


def plot(histos):

    colors = [kBlack, kBlue, kRed, kBlack, kRed, kGreen, kGreen+2, kBlue+2, kAzure, kRed, kRed, kGreen, kGreen+2, kBlack, kBlue, kRed, kGreen, kBlue+2, kAzure, kRed, kRed]

    for label in histos:
        histos[label].SetLineWidth(2)
        color = colors.pop(0)
        histos[label].SetLineColor(color)

        if not "data" in label:
            histos[label].Scale(lumi)

        if "prediction" in label or "data" in label:
            histos[label].SetMarkerStyle(22)
            histos[label].SetMarkerColor(color)
            histos[label].SetMarkerSize(1)

    #fout = TFile(canvas_label + ".root", "recreate")

    canvas = TCanvas(canvas_label, canvas_label, 800, 800)
    canvas.SetRightMargin(0.06)
    canvas.SetLeftMargin(0.12)
    canvas.SetLogy(True)

    pad1 = TPad("pad1", "pad1", 0, 0.16, 1, 1.0)
    pad1.SetRightMargin(0.05)
    pad1.SetLogy(True)
    pad2 = TPad("pad2", "pad2", 0.0, 0.025, 1.0, 0.235)
    pad2.SetBottomMargin(0.25)
    pad2.SetRightMargin(0.05)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()

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
    
        if not ymax:
            ymin = global_ymin * 1e-2
            ymax = global_ymax * 1e2

    histos["control_region"].Draw("hist e")
    histos["control_region"].SetLineColor(16)

    if xmax:
        histos["control_region"].GetXaxis().SetRangeUser(xmin, xmax)
    if ymax:
        histos["control_region"].GetYaxis().SetRangeUser(ymin, ymax)
    histos["control_region"].GetXaxis().SetLabelSize(0)   
    histos["control_region"].SetTitle(";;events")

    histos["promptlike"].Draw("same hist e")
    histos["fakelike"].Draw("same hist e")

    legend = TLegend(0.4, 0.7, 0.89, 0.89)
    legend.SetHeader(extra_text)
    legend.SetTextSize(0.025)
    legend.AddEntry(histos["control_region"], "control region (CR)")
    legend.AddEntry(histos["promptlike"], "prompt background in SR (MC Truth)")
    legend.AddEntry(histos["fakelike"], "non-prompt background in SR (MC Truth)")
    legend.SetBorderSize(0)

    legend.Draw()

    stamp_plot()

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)
    latex.DrawLatex(0.93, 0.91, "%.1f fb^{-1} (13 TeV)" % lumi)

    # plot ratios
    pad2.cd()
    
    if not xlabel:
        xlabel = variable
    
    ratios = collections.OrderedDict()
    for i, label in enumerate(histos):
        if "signal_tracks" in label:
            ratios[label] = histos[label].Clone()
            ratios[label].Divide(histos["control_region"])
            if xmax:
                ratios[label].GetXaxis().SetRangeUser(xmin, xmax)
    
            if i==0:
                ratios[label].Draw("e0")
            else:
                ratios[label].Draw("same e0")
    
            ratios[label].SetTitle(";%s;Pred./Truth" % xlabel)
            ratios[label].GetXaxis().SetTitleSize(0.13)
            ratios[label].GetYaxis().SetTitleSize(0.13)
            ratios[label].GetYaxis().SetTitleOffset(0.38)
            ratios[label].GetYaxis().SetRangeUser(0,2)
            ratios[label].GetYaxis().SetNdivisions(4)
            ratios[label].GetXaxis().SetLabelSize(0.15)
            ratios[label].GetYaxis().SetLabelSize(0.15)
    
    pad2.SetGridx(True)
    pad2.SetGridy(True)

    #canvas.Write()
    canvas.SaveAs(canvas_label + ".pdf")



if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest="index", default=False)
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    (options, args) = parser.parse_args()

    configurations = get_configurations()

    if options.index:
        
        histogram = get_histogram(*configurations[configurations.keys()[int(options.index)]])
        label = configurations.keys()[int(options.index)]

        fout = TFile("template_pt%s.root" % options.index, "recreate")
        histogram.SetName(label)
        histogram.Write()
        fout.Close()

    elif options.hadd:

        os.system("hadd -f template.root template_pt*root && rm template_pt*root")

    else:

        commands = []
        for i in range(len(configurations)):
            commands.append("./prepare_template_fit.py --index %s" % i)
        print "running %s jobs!" % len(commands)
        runParallel(commands, options.runmode, condorDir = "prepare_template_fit_condor", dontCheckOnJobs=False)


