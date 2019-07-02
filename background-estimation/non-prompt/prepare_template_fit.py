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
    data = "Run2016*MET"

    histos = collections.OrderedDict()

    cuts = {
             "base":        "passesUniversalSelection==1 && MHT>250 && MinDeltaPhiMhtJets>0.3 && n_jets>0",
             "noleptons":   "passesUniversalSelection==1 && MHT>250 && MinDeltaPhiMhtJets>0.3 && n_jets>0 && n_leptons==0",
           }

    variables = {
                  "HT_short":  [" && tracks_is_pixel_track==1 ", 40, 0, 1000],
                  "HT_long":  [" && tracks_is_pixel_track==0 ", 40, 0, 1000],
                  "MHT_short":  [" && tracks_is_pixel_track==1 ", 40, 0, 1000],
                  "MHT_long":  [" && tracks_is_pixel_track==0 ", 40, 0, 1000],
                  "n_jets_short":  [" && tracks_is_pixel_track==1 ", 30, 0, 30],
                  "n_jets_long":  [" && tracks_is_pixel_track==0 ", 30, 0, 30],
                  "n_btags_short":  [" && tracks_is_pixel_track==1 ", 15, 0, 15],
                  "n_btags_long":  [" && tracks_is_pixel_track==0 ", 15, 0, 15],
                  "MinDeltaPhiMhtJets_short":  [" && tracks_is_pixel_track==1 ", 20, 0, 1],
                  "MinDeltaPhiMhtJets_long":  [" && tracks_is_pixel_track==0 ", 20, 0, 1],
                  "tracks_massfromdeDxPixel":  [" && tracks_is_pixel_track==1 ", 80, 0, 4000],
                  "tracks_massfromdeDxStrips": [" && tracks_is_pixel_track==0 ", 80, 0, 4000],
                  "log10(tracks_massfromdeDxPixel)":  [" && tracks_is_pixel_track==1 ", 50, 0, 5],
                  "log10(tracks_massfromdeDxStrips)": [" && tracks_is_pixel_track==0 ", 50, 0, 5],
                }

    tags = {
             "loose1a":      {"short": " && tracks_mva_bdt_loose>0 ", "long": " && tracks_mva_bdt_loose>0 ", "track_SR": " && tracks_dxyVtx<=0.01 ", "track_CR": " && tracks_dxyVtx>0.01 "},
             #"loose1b":      {"short": " && tracks_mva_bdt_loose>0.1 ", "long": " && tracks_mva_bdt_loose>0.1 ", "track_SR": " && tracks_dxyVtx<=0.01 ", "track_CR": " && tracks_dxyVtx>0.01 "},
             #"loose2a":      {"short": " && tracks_mva_bdt_loose>0 ", "long": " && tracks_mva_bdt_loose>0 ", "track_SR": " && tracks_dxyVtx<=0.02 ", "track_CR": " && tracks_dxyVtx>0.05 "},
             #"loose2b":      {"short": " && tracks_mva_bdt_loose>0.1 ", "long": " && tracks_mva_bdt_loose>0.1 ", "track_SR": " && tracks_dxyVtx<=0.02 ", "track_CR": " && tracks_dxyVtx>0.05 "},
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

                fakelike          = control_region + track_selection + tags[tag]["track_CR"] + " && tracks_is_reco_lepton==0 "         # fake-like: select high-dxy region
                promptlike        = control_region + track_selection + tags[tag]["track_SR"] + " && tracks_is_reco_lepton==1 "         # prompt-like: select leptons
                background_tracks = control_region + track_selection + tags[tag]["track_SR"] + " && tracks_is_reco_lepton==0 "
                signal_tracks     = control_region + track_selection + tags[tag]["track_SR"] + " && tracks_is_reco_lepton==0 "

                treevariable = variable.replace("_short", "").replace("_long", "")

                configurations["%s_%s_bg_%s" % (variable, tag, label)] =                  [treevariable, background_tracks, nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_fake_%s" % (variable, tag, label)] =             [treevariable, background_tracks + " && tracks_fake==1 ", nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_prompt_%s" % (variable, tag, label)] =           [treevariable, background_tracks + " && tracks_fake==0 ", nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_promptlike_%s" % (variable, tag, label)] =       [treevariable, promptlike, nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_fakelike_%s" % (variable, tag, label)] =         [treevariable, fakelike, nBinsX, xmin, xmax, path, mc_background]
                if not "n_leptons==0" in control_region:                                   
                    configurations["%s_%s_data_promptlike_%s" % (variable, tag, label)] = [treevariable, promptlike, nBinsX, xmin, xmax, path, data]
                configurations["%s_%s_data_fakelike_%s" % (variable, tag, label)] =       [treevariable, fakelike, nBinsX, xmin, xmax, path, data]
                configurations["%s_%s_signal_ctau10_%s" % (variable, tag, label)] =       [treevariable, signal_tracks, nBinsX, xmin, xmax, path, "Summer16.g1800_chi1400_27_200970_step4_10AODSIM"]
                configurations["%s_%s_signal_ctau30_%s" % (variable, tag, label)] =       [treevariable, signal_tracks, nBinsX, xmin, xmax, path, "Summer16.g1800_chi1400_27_200970_step4_30AODSIM"]
                configurations["%s_%s_signal_ctau50_%s" % (variable, tag, label)] =       [treevariable, signal_tracks, nBinsX, xmin, xmax, path, "Summer16.g1800_chi1400_27_200970_step4_50AODSIM"]
                configurations["%s_%s_signal_ctau100_%s" % (variable, tag, label)] =      [treevariable, signal_tracks, nBinsX, xmin, xmax, path, "Summer16.g1800_chi1400_27_200970_step4_100AODSIM"]

    return configurations


def get_single_histogram(config):
    return get_histogram(config[0], config[1], nBinsX=config[2], xmin=config[3], xmax=config[4], path=config[5], selected_sample=config[6])


def plot(histo_file, variable = "tracks_massfromdeDxStrips", tag = "loose1a", category = "long", path = ".", lumi = 26216, canvas_label=False, autoscaling=True, ymin=False, ymax=False, xmin=0, xmax=2500, extra_text = ""):

    histos = {}
    fin = TFile(histo_file, "open")
    #histos["control_region"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg", "noleptons"))
    histos["mc_prompt"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_prompt", "noleptons"))
    histos["mc_fake"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_fake", "noleptons"))
    histos["mc_promptlike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_promptlike", "base"))
    histos["mc_fakelike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_fakelike", "noleptons"))
    histos["data_promptlike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "data_promptlike", "base"))
    histos["data_fakelike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "data_fakelike", "noleptons"))
    histos["signal_ctau10"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "signal_ctau10", "noleptons"))
    histos["signal_ctau30"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "signal_ctau30", "noleptons"))
    histos["signal_ctau50"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "signal_ctau50", "noleptons"))
    histos["signal_ctau100"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "signal_ctau100", "noleptons"))
    
    for histo in histos:
        try:
            nev = histos[histo].GetEntries()
            if not "data" in histo:
                histos[histo].Scale(lumi)
        except:
            print "Empty:", histo

    if not canvas_label:
        canvas_label = variable + "_" + tag
    xlabel = variable
    
    #colors = [kBlack, kBlue, kRed, kBlack, kTeal, kGreen, kGreen+2, kBlue+2, kAzure, kRed, kRed, kGreen, kGreen+2, kBlack, kBlue, kRed, kGreen, kBlue+2, kAzure, kRed, kRed]
    colors = [kRed, kOrange, kBlue, kGreen]
    
    for label in histos:
        histos[label].SetLineWidth(2)
        if "signal" in label:
            color = colors.pop(0)
            histos[label].SetLineColor(color)
            
        if "prediction" in label or "data" in label:
            histos[label].SetMarkerStyle(20)
            if "signal" in label: histos[label].SetMarkerColor(color)
            histos[label].SetMarkerSize(1)

    for bg in ["prompt", "fake"]:
             
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
                ymin = global_ymin * 1e1
                ymax = global_ymax * 1e1
        
        if bg == "prompt":
            histos["mc_prompt"].Draw("hist e")
            histos["mc_prompt"].SetLineColor(16)
            if xmax:
                histos["mc_prompt"].GetXaxis().SetRangeUser(xmin, xmax)
            if ymax:
                histos["mc_prompt"].GetYaxis().SetRangeUser(ymin, ymax)
            histos["mc_prompt"].GetXaxis().SetLabelSize(0)   
            histos["mc_prompt"].SetTitle(";;Events")
        else:        
            histos["mc_fake"].Draw("hist e")
            histos["mc_fake"].SetLineColor(16)
            if xmax:
                histos["mc_fake"].GetXaxis().SetRangeUser(xmin, xmax)
            if ymax:
                histos["mc_fake"].GetYaxis().SetRangeUser(ymin, ymax)
            histos["mc_fake"].GetXaxis().SetLabelSize(0)   
            histos["mc_fake"].SetTitle(";;events")
                
        if bg == "prompt":
            histos["mc_promptlike"].Draw("same hist e")
            histos["mc_promptlike"].SetMarkerColor(1)
            histos["mc_promptlike"].SetLineColor(1)
            histos["data_promptlike"].SetMarkerColor(1)
            histos["data_promptlike"].SetLineColor(1)
            histos["data_promptlike"].Draw("same p")
        else:
            histos["mc_fakelike"].Draw("same hist e")
            histos["mc_fakelike"].SetMarkerColor(1)
            histos["mc_fakelike"].SetLineColor(1)
            histos["data_fakelike"].SetMarkerColor(1)
            histos["data_fakelike"].SetLineColor(1)
            histos["data_fakelike"].Draw("same p")
        
        histos["signal_ctau10"].Draw("same hist")
        histos["signal_ctau30"].Draw("same hist")
        histos["signal_ctau50"].Draw("same hist")
        histos["signal_ctau100"].Draw("same hist")
        
        legend = TLegend(0.55, 0.55, 0.89, 0.89)
        legend.SetTextSize(0.03)
        if bg == "prompt":
            legend.AddEntry(histos["mc_prompt"], "true prompt tracks in MC SR")
            legend.AddEntry(histos["mc_promptlike"], "prompt-like tracks in MC SR")
            legend.AddEntry(histos["data_promptlike"], "prompt-like tracks in data SR")
        else:
            legend.AddEntry(histos["mc_fake"], "true fake tracks in MC SR")
            legend.AddEntry(histos["mc_fakelike"], "fake-like tracks in MC CR")
            legend.AddEntry(histos["data_fakelike"], "fake-like tracks in data CR")
        legend.AddEntry(histos["signal_ctau10"], "signal c#tau=10 cm")
        legend.AddEntry(histos["signal_ctau30"], "signal c#tau=30 cm")
        legend.AddEntry(histos["signal_ctau50"], "signal c#tau=50 cm")
        legend.AddEntry(histos["signal_ctau100"], "signal c#tau=100 cm")
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
        latex.DrawLatex(0.93, 0.91, "%.1f fb^{-1} (13 TeV)" % (lumi/1000.0))
        
        # plot ratios
        pad2.cd()
        
        if not xlabel:
            xlabel = variable
        
        ratios = collections.OrderedDict()
        for i, label in enumerate(histos):
            if "data" in label:
                ratios[label] = histos[label].Clone()
                
                if bg == "fake" and "fakelike" in label:
                    ratios[label].Divide(histos["mc_fakelike"])
                elif bg == "prompt" and "promptlike" in label:
                    ratios[label].Divide(histos["mc_promptlike"])
                else:
                    continue
                if xmax:
                    ratios[label].GetXaxis().SetRangeUser(xmin, xmax)
        
                if i==0:
                    ratios[label].Draw("e0")
                else:
                    ratios[label].Draw("same e0")
        
                ratios[label].SetTitle(";%s;Data/MC" % xlabel)
                ratios[label].GetXaxis().SetTitleSize(0.13)
                ratios[label].GetYaxis().SetTitleSize(0.13)
                ratios[label].GetYaxis().SetTitleOffset(0.38)
                ratios[label].GetYaxis().SetRangeUser(0,10)
                ratios[label].GetYaxis().SetNdivisions(4)
                ratios[label].GetXaxis().SetLabelSize(0.15)
                ratios[label].GetYaxis().SetLabelSize(0.15)
        
        pad2.SetGridx(True)
        pad2.SetGridy(True)
        
        if not os.path.exists(path + "/plots"):
             os.mkdir(path + "/plots")
        canvas.SaveAs(path + "/plots/" + canvas_label + "_" + bg + ".pdf")


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest="index", default=False)
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--plot", dest="plot", action="store_true")
    (options, args) = parser.parse_args()

    configurations = get_configurations()
    path = configurations[configurations.keys()[0]][5]

    if options.index:

        label = configurations.keys()[int(options.index)]
               
        histogram = get_single_histogram(configurations[configurations.keys()[int(options.index)]])
        fout = TFile("template_pt%s.root" % options.index, "recreate")
        histogram.SetName(label)
        histogram.Write()
        fout.Close()

    elif options.hadd:

        os.system("hadd -f %s/template.root template_pt*root && rm template_pt*root" % path)

    elif options.plot:

        template_file = path + "/template2.root"

        for tag in ["loose1a"]:

            plot(template_file, variable = "log10(tracks_massfromdeDxStrips)", tag = tag, category = "long", lumi = 26216, xmin=1, xmax=5, extra_text = "", path = path)
            plot(template_file, variable = "log10(tracks_massfromdeDxPixel)", tag = tag, category = "short", lumi = 26216, xmin=1, xmax=5, extra_text = "", path = path)
            
            for category in ["short", "long"]:
                plot(template_file, variable = "MHT_%s" % category, tag = tag, category = category, lumi = 26216, xmin=250, xmax=1000, path = path)
                plot(template_file, variable = "HT_%s" % category, tag = tag, category = category, lumi = 26216, xmin=0, xmax=1000, path = path)
                plot(template_file, variable = "n_jets_%s" % category, tag = tag, category = category, lumi = 26216, path = path)
                plot(template_file, variable = "n_btags_%s" % category, tag = tag, category = category, xmin=0, xmax=8, lumi = 26216, path = path)
                plot(template_file, variable = "MinDeltaPhiMhtJets_%s" % category, tag = tag, category = category, xmin=0.3, xmax=1, lumi = 26216, path = path)

    else:

        commands = []
        for i in range(len(configurations)):
            commands.append("./prepare_template_fit.py --index %s" % i)
        raw_input("running %s jobs!" % len(commands) )
        runParallel(commands, options.runmode, condorDir = "prepare_template_fit_condor", dontCheckOnJobs=False)

    
