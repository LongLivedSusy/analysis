#!/bin/env python
from __future__ import division
from optparse import OptionParser
import os
from ROOT import *
import plotting
from GridEngineTools import runParallel
import collections

def get_histos(config, index):

    histos = collections.OrderedDict()
    for label in config:
        histos[label] = plotting.get_histogram(config[label])

        
def get_configurations():

    configurations = collections.OrderedDict()

    path = "output_skim_13_merged"
    mc_background = "Summer16.DYJetsToLL|Summer16.QCD|Summer16.WJetsToLNu|Summer16.ZJetsToNuNu_HT|Summer16.WW_TuneCUETP8M1|Summer16.WZ_TuneCUETP8M1|Summer16.ZZ_TuneCUETP8M1|Summer16.TTJets_TuneCUETP8M1_13TeV"
    mc_signal = "output_skim_13_merged/Summer16.g1800_chi1400_27_200970_step4"
    data = "Run2016*MET"

    histos = collections.OrderedDict()

    base = "passesUniversalSelection==1 && MinDeltaPhiMhtJets>0.3 && n_goodjets>0"

    cuts = {
             "base":                  base + " && MHT>250",
             "MHT0_base":             base + " && MHT<200",
             "MHT1_base":             base + " && MHT<250",
             "MHT2_base":             base + " && MHT>250 && MHT<350",
             "MHT3_base":             base + " && MHT>250 && MHT<400",
             "MHT4_base":             base + " && MHT>400",
             "MHT5_base":             base + " && MHT>450",
             "njets1_base":           base + " && MHT>250 && n_goodjets<=4",
             "njets2_base":           base + " && MHT>250 && n_goodjets>=5",
           }

    variables = {
                  "log10(tracks_massfromdeDxPixel)":  [" && tracks_is_pixel_track==1 ", 50, 0, 5],
                  "log10(tracks_massfromdeDxStrips)": [" && tracks_is_pixel_track==0 ", 50, 0, 5],
                }

    good_track = " && tracks_passpionveto==1 "

    tags = {
             "loose1":      {"short": " && tracks_mva_bdt_loose>0 ",
                             "long": " && tracks_mva_bdt_loose>0 ",
                             "track_SR": " && tracks_dxyVtx<=0.01 ",
                             "track_CR": " && tracks_dxyVtx>0.01 "},
             "loose2":      {"short": " && tracks_mva_bdt_loose>0 ",
                             "long": " && tracks_mva_bdt_loose>0 ",
                             "track_SR": " && tracks_dxyVtx<=0.01 ",
                             "track_CR": " && tracks_dxyVtx>0.02 && tracks_dxyVtx<0.1 "},
             "loose3":      {"short": " ",
                             "long": " ",
                             "track_SR": " && tracks_mva_bdt_loose>tracks_dxyVtx*0.5/0.01 ",
                             "track_CR": " && tracks_mva_bdt_loose<tracks_dxyVtx*0.5/0.01 "},
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

                fakelike          = control_region + good_track + track_selection + tags[tag]["track_CR"] + " && tracks_is_reco_lepton==0 && tracks_passPFCandVeto==1 && n_goodleptonsid==0"       # fake-like: select high-dxy region
                promptlike        = control_region + good_track + track_selection + tags[tag]["track_SR"] + " && tracks_is_reco_lepton==1 "                                                        # prompt-like: select leptons
                sr_tracks         = control_region + good_track + track_selection + tags[tag]["track_SR"] + " && tracks_is_reco_lepton==0 && tracks_passPFCandVeto==1 && n_goodleptonsid==0 "      # tagged tracks in the SR

                treevariable = variable.replace("_short", "").replace("_long", "")

                configurations["%s_%s_bg_%s" % (variable, tag, label)] =                  [treevariable, sr_tracks, nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_genfake_%s" % (variable, tag, label)] =          [treevariable, sr_tracks + " && tracks_fake==1 ", nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_genprompt_%s" % (variable, tag, label)] =        [treevariable, sr_tracks + " && tracks_fake==0 ", nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_genfakelike_%s" % (variable, tag, label)] =      [treevariable, fakelike + " && tracks_fake==1 ", nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_genpromptlike_%s" % (variable, tag, label)] =    [treevariable, promptlike + " && tracks_fake==0 ", nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_promptlike_%s" % (variable, tag, label)] =       [treevariable, promptlike, nBinsX, xmin, xmax, path, mc_background]
                configurations["%s_%s_bg_fakelike_%s" % (variable, tag, label)] =         [treevariable, fakelike, nBinsX, xmin, xmax, path, mc_background]

                configurations["%s_%s_sg_%s" % (variable, tag, label)] =                  [treevariable, sr_tracks, nBinsX, xmin, xmax, path, mc_signal]
                configurations["%s_%s_sg_genfake_%s" % (variable, tag, label)] =          [treevariable, sr_tracks + " && tracks_fake==1 ", nBinsX, xmin, xmax, path, mc_signal]
                configurations["%s_%s_sg_genprompt_%s" % (variable, tag, label)] =        [treevariable, sr_tracks + " && tracks_fake==0 ", nBinsX, xmin, xmax, path, mc_signal]
                configurations["%s_%s_sg_genfakelike_%s" % (variable, tag, label)] =      [treevariable, fakelike + " && tracks_fake==1 ", nBinsX, xmin, xmax, path, mc_signal]
                configurations["%s_%s_sg_genpromptlike_%s" % (variable, tag, label)] =    [treevariable, promptlike + " && tracks_fake==0 ", nBinsX, xmin, xmax, path, mc_signal]
                configurations["%s_%s_sg_promptlike_%s" % (variable, tag, label)] =       [treevariable, promptlike, nBinsX, xmin, xmax, path, mc_signal]
                configurations["%s_%s_sg_fakelike_%s" % (variable, tag, label)] =         [treevariable, fakelike, nBinsX, xmin, xmax, path, mc_signal]

                configurations["%s_%s_data_%s" % (variable, tag, label)] =                [treevariable, sr_tracks, nBinsX, xmin, xmax, path, data]
                configurations["%s_%s_data_promptlike_%s" % (variable, tag, label)] =     [treevariable, promptlike, nBinsX, xmin, xmax, path, data]
                configurations["%s_%s_data_fakelike_%s" % (variable, tag, label)] =       [treevariable, fakelike, nBinsX, xmin, xmax, path, data]

    return configurations


def get_single_histogram(config):
    return plotting.get_histogram(config[0], config[1], nBinsX=config[2], xmin=config[3], xmax=config[4], path=config[5], selected_sample=config[6])


def plot(histo_file, variable = "tracks_massfromdeDxStrips", tag = "loose1a", category = "long", path = ".", lumi = 26216, canvas_label=False, autoscaling=True, ymin=False, ymax=False, xmin=0, xmax=2500, extra_text = "", prefix = ""):

    histos = {}
    fin = TFile(histo_file, "open")
    histos["bg_prompt"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_genprompt", prefix + "noleptons"))
    histos["bg_fake"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_genfake", prefix + "noleptons"))
    histos["bg_promptlike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_promptlike", prefix + "base"))
    histos["bg_fakelike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_fakelike", prefix + "noleptons"))
    histos["data_promptlike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "data_promptlike", prefix + "base"))
    histos["data_fakelike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "data_fakelike", prefix + "noleptons"))
    histos["sg_promptlike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "sg_promptlike", prefix + "base"))
    histos["sg_fakelike"] = fin.Get("%s_%s_%s_%s" % (variable, tag, "sg_fakelike", prefix + "noleptons"))
       
    for histo in histos:
        try:
            nev = histos[histo].GetEntries()
            if not "data" in histo:
                histos[histo].Scale(lumi)
        except:
            print "Empty:", histo

    if not canvas_label:
        canvas_label = variable + "_" + tag
    
    #colors = [kBlack, kBlue, kRed, kBlack, kTeal, kGreen, kGreen+2, kBlue+2, kAzure, kRed, kRed, kGreen, kGreen+2, kBlack, kBlue, kRed, kGreen, kBlue+2, kAzure, kRed, kRed]
    colors = [kRed, kOrange, kBlue, kGreen]
    
    for label in histos:
        histos[label].SetLineWidth(2)
        if "sg" in label:
            color = colors.pop(0)
            histos[label].SetLineColor(color)
            
        if "data" in label:
            histos[label].SetMarkerStyle(20)
            if "sg" in label: histos[label].SetMarkerColor(color)
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
            histos["mc_prompt"].GetYaxis().SetLabelSize(0.25)   
            histos["mc_prompt"].SetTitle(";;Events")
        else:        
            histos["mc_fake"].Draw("hist e")
            histos["mc_fake"].SetLineColor(16)
            if xmax:
                histos["mc_fake"].GetXaxis().SetRangeUser(xmin, xmax)
            if ymax:
                histos["mc_fake"].GetYaxis().SetRangeUser(ymin, ymax)
            histos["mc_fake"].GetXaxis().SetLabelSize(0)   
            histos["mc_fake"].GetYaxis().SetLabelSize(0.25)   
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
        
        plotting.stamp_plot()
        
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
        
                ratios[label].SetTitle(";%s;Data/MC" % variable)
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
        canvas.SaveAs(path + "/plots/" + prefix + canvas_label + "_" + bg + ".pdf")


def waterfall_plot(histo_file, variable = "tracks_massfromdeDxStrips", tag = "loose1a", category = "long", path = ".", lumi = 26216, canvas_label=False, autoscaling=True, ymin=False, ymax=False, xmin=False, xmax=4, extra_text = "", prefixes = ["lowMHT", "lowlowMHT", "lowlowlowMHT"], bg = "prompt", suffix = "", normalize_histograms = True, include_sg = False, include_bg = True):

    histos = collections.OrderedDict()
    fin = TFile(histo_file, "open")

    for prefix in prefixes:
        if bg == "prompt":
            histos["data_promptlike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "data_promptlike", prefix + "base"))
        else:
            histos["data_fakelike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "data_fakelike", prefix + "base"))


    if include_bg:        
        for prefix in prefixes:
            if bg == "prompt":
                histos["bg_promptlike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_promptlike", prefix + "base"))
            else:
                histos["bg_fakelike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_fakelike", prefix + "base"))

        for prefix in prefixes:
            if bg == "prompt":
                histos["bg_genpromptlike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_genpromptlike", prefix + "base"))
            else:
                histos["bg_genfakelike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_genfakelike", prefix + "base"))

        for prefix in prefixes:
            if bg == "prompt":
                histos["bg_genprompt_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_genprompt", prefix + "base"))
            else:
                histos["bg_genfake_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "bg_genfake", prefix + "base"))

    if include_sg:
        for prefix in prefixes:
            if bg == "prompt":
                histos["sg_promptlike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "sg_promptlike", prefix + "base"))
            else:
                histos["sg_fakelike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "sg_fakelike", prefix + "base"))

        for prefix in prefixes:
            if bg == "prompt":
                histos["sg_genpromptlike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "sg_genpromptlike", prefix + "base"))
            else:
                histos["sg_genfakelike_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "sg_genfakelike", prefix + "base"))

        for prefix in prefixes:
            if bg == "prompt":
                histos["sg_genprompt_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "sg_genprompt", prefix + "base"))
            else:
                histos["sg_genfake_%s" % prefix] = fin.Get("%s_%s_%s_%s" % (variable, tag, "sg_genfake", prefix + "base"))

    
    bg_colors = [kRed, kOrange, kMagenta, kMagenta, kRed+2, kOrange+2, kMagenta+2, kMagenta+2]
    bg_truth_colors = [kRed, kOrange, kMagenta, kMagenta, kRed+2, kOrange+2, kMagenta+2, kMagenta+2]
    bg_truthlike_colors = [kRed, kOrange, kMagenta, kMagenta, kRed+2, kOrange+2, kMagenta+2, kMagenta+2]
    sg_colors = [kBlue, kTeal, kGreen, kAzure, kBlack, kBlue+2, kTeal+2, kGreen+2, kAzure+2]
    sg_truth_colors = [kBlue, kTeal, kGreen, kAzure, kBlack, kBlue+2, kTeal+2, kGreen+2, kAzure+2]
    data_colors = [kRed, kOrange, kMagenta, kMagenta, kRed+2, kOrange+2, kMagenta+2, kMagenta+2]

    for histo in histos.keys():
        try:
            nev = histos[histo].GetEntries()
        except:
            print "Empty:", histo
            del histos[histo]
            continue

        if not "data" in histo:
            histos[histo].Scale(lumi)

        if "sg_" in histo and ("_fakelike_" in histo or "_promptlike_" in histo):
            color = sg_colors.pop(0)
        elif "sg_" in histo and ("_genfake_" in histo or "_genprompt_" in histo):
            color = sg_truth_colors.pop(0)
        elif "bg_" in histo and ("_fakelike_" in histo or "_promptlike_" in histo):
            color = bg_colors.pop(0)
        elif "bg_" in histo and ("_genfake_" in histo or "_genprompt_" in histo):
            color = bg_truthlike_colors.pop(0)
        elif "bg_" in histo and ("_genfakelike_" in histo or "_genpromptlike_" in histo):
            color = bg_truth_colors.pop(0)
        elif "data_" in histo and ("_fakelike_" in histo or "_promptlike_" in histo):
            color = data_colors.pop(0)

        histos[histo].SetLineColor(color)

        histos[histo].SetLineWidth(2)
        if "_genfake_" in histo or "_genprompt_" in histo:
            histos[histo].SetLineColorAlpha(1, 0)
            histos[histo].SetLineStyle(3)
            histos[histo].SetMarkerStyle(22)
            histos[histo].SetMarkerColor(color)
        if "_genfakelike_" in histo or "_genpromptlike_" in histo:
            histos[histo].SetLineStyle(7)
        if "data" in histo:
            histos[histo].SetLineColorAlpha(1, 0)
            histos[histo].SetMarkerStyle(20)
            histos[histo].SetMarkerColor(color)


        if normalize_histograms and histos[histo].Integral() != 0:
            histos[histo].Scale(1.0/histos[histo].Integral())
        histos[histo].Rebin(10)

        if xmax:
            histos[histo].GetXaxis().SetRangeUser(xmin, xmax)
       
    canvas = TCanvas("waterfall", "waterfall", 800, 800)
    canvas.SetRightMargin(0.06)
    canvas.SetLeftMargin(0.12)
    canvas.SetLogy(True)
    
    #pad1 = TPad("pad1", "pad1", 0, 0.155, 1, 1.0)
    pad1 = TPad("pad1", "pad1", 0, 0.32, 1, 1.0)
    pad1.SetRightMargin(0.05)
    pad1.SetLogy(True)
    pad1.SetBottomMargin(0.05)

    pad2 = TPad("pad2", "pad2", 0.0, 0.025, 1.0, 0.235)
    pad2.SetBottomMargin(0.25)
    pad2.SetRightMargin(0.05)

    pad3 = TPad("pad3", "pad3", 0.0, 0.218, 1.0, 0.35)
    pad3.SetBottomMargin(0)
    pad3.SetTopMargin(0)
    pad3.SetRightMargin(0.05)


    pad1.Draw()
    pad2.Draw()
    pad3.Draw()
    pad1.cd()

    legend = TLegend(0.55, 0.65, 0.89, 0.89)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)

    header = ""
    if tag == "loose1":
        header = "tag: loose (SR: d_{xy}<0.01, CR: d_{xy}>0.01)"
    elif tag == "loose2":
        header = "tag: loose (SR: d_{xy}<0.01, CR: 0.02<d_{xy}<0.1)"
    elif tag == "loose3":
        header = "tag: loose (SR/CR from cut function)"
    legend.SetHeader(header)
    
    for i, label in enumerate(histos):
            
        if "data" in label or "_genfake_" in label or "_genprompt_" in label:
            draw_option = "p"
        else:
            draw_option = "hist"

        if i == 0:
            histos[label].Draw(draw_option)
            if normalize_histograms:
                histos[label].SetTitle(";;tracks normalized to unity")
            else:
                histos[label].SetTitle(";;tracks")
        else:
            histos[label].Draw(draw_option + " same")
        
        histos[label].GetYaxis().SetTitleSize(0.04)
        histos[label].GetYaxis().SetLabelSize(0.04)
        histos[label].GetYaxis().SetTitleOffset(1.1)

        legendlabel = label
        legendlabel = legendlabel.replace("data", "Data ")
        legendlabel = legendlabel.replace("sg", "SG ")
        legendlabel = legendlabel.replace("bg", "BG ")
        legendlabel = legendlabel.replace("_promptlike", "prompt-like tracks")
        legendlabel = legendlabel.replace("_genpromptlike", "prompt-like tracks, MC Truth")
        legendlabel = legendlabel.replace("_genprompt", "prompt tracks, MC Truth")
        legendlabel = legendlabel.replace("_genfakelike", "fake-like tracks")
        legendlabel = legendlabel.replace("_fakelike", "fake-like tracks")
        legendlabel = legendlabel.replace("_genfake", "fake tracks, MC Truth")
        legendlabel = legendlabel.replace("_fake", "fake-like tracks, MC Truth")
        legendlabel = legendlabel.replace("_MHT0_", " (MHT<200)")
        legendlabel = legendlabel.replace("_MHT1_", " (MHT<250)")
        legendlabel = legendlabel.replace("_MHT2_", " (250<MHT<350)")
        legendlabel = legendlabel.replace("_MHT3_", " (250<MHT<400)")
        legendlabel = legendlabel.replace("_MHT4_", " (MHT>400)")
        legendlabel = legendlabel.replace("_MHT5_", " (MHT>450)")
        legendlabel = legendlabel.replace("_njets1_", " (n_goodjets#leq4)")
        legendlabel = legendlabel.replace("_njets2_", " (n_goodjets#geq5)")
        
        legend.AddEntry(histos[label], legendlabel)
    
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
                
    for label in histos:
        histos[label].SetMaximum(global_ymax*1e2)
        histos[label].SetMinimum(global_ymin)
        
    legend.Draw()
    plotting.stamp_plot()
    
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
    ratios = collections.OrderedDict()
    for i, label in enumerate(histos):
        if "data" not in label and ("_promptlike" in label or "_fakelike" in label or "_genpromptlike" in label or "_genfakelike" in label):
            ratios[label] = histos[label].Clone()
            if "_promptlike" in label:
                ratios[label].Divide(histos[label.replace("_promptlike", "_genprompt")])
            elif "_fakelike" in label:
                ratios[label].Divide(histos[label.replace("_fakelike", "_genfake")])
            elif "_genpromptlike" in label:
                ratios[label].Divide(histos[label.replace("_genpromptlike", "_genprompt")])
            elif "_genfakelike" in label:
                ratios[label].Divide(histos[label.replace("_genfakelike", "_genfake")])
            else:
                continue
            if xmax:
                ratios[label].GetXaxis().SetRangeUser(xmin, xmax)
    
            if i==0:
                ratios[label].Draw("e0")
            else:
                ratios[label].Draw("same e0")
    
            if bg == "prompt":
                ratios[label].SetTitle(";%s;p.like/prompt" % variable)
            else:
                ratios[label].SetTitle(";%s;f.like/fake" % variable)
            ratios[label].GetXaxis().SetTitleSize(0.13)
            ratios[label].GetYaxis().SetTitleSize(0.13)
            ratios[label].GetYaxis().SetTitleOffset(0.38)
            ratios[label].GetYaxis().SetRangeUser(1.5e-1,0.5e1)
            ratios[label].GetYaxis().SetNdivisions(4)
            ratios[label].GetXaxis().SetLabelSize(0.15)
            ratios[label].GetYaxis().SetLabelSize(0.15)

        pad2.SetLogy(True)
        pad2.SetGridx(True)
        pad2.SetGridy(True)

    pad3.cd()     
    lowhigh_ratios = collections.OrderedDict()
    for i, label in enumerate(histos):
        if "_promptlike" in label or "_fakelike" in label:
            lowhigh_ratios[label] = histos[label].Clone()
            if "bg_promptlike" in label and ("MHT1_" in label or "njets1_" in label):
                lowhigh_ratios[label].Divide(histos[label.replace("MHT1_", "MHT4_").replace("njets1_", "njets2_")])
            elif "bg_fakelike" in label and ("MHT1_" in label or "njets1_" in label):
                lowhigh_ratios[label].Divide(histos[label.replace("MHT1_", "MHT4_").replace("njets1_", "njets2_")])
            elif "bg_genpromptlike" in label and ("MHT1_" in label or "njets1_" in label):
                lowhigh_ratios[label].Divide(histos[label.replace("MHT1_", "MHT4_").replace("njets1_", "njets2_")])
            elif "bg_genfakelike" in label and ("MHT1_" in label or "njets1_" in label):
                lowhigh_ratios[label].Divide(histos[label.replace("MHT1_", "MHT4_").replace("njets1_", "njets2_")])
            elif "data_promptlike" in label and ("MHT1_" in label or "njets1_" in label):
                lowhigh_ratios[label].Divide(histos[label.replace("MHT1_", "MHT4_").replace("njets1_", "njets2_")])
            elif "data_fakelike" in label and ("MHT1_" in label or "njets1_" in label):
                lowhigh_ratios[label].Divide(histos[label.replace("MHT1_", "MHT4_").replace("njets1_", "njets2_")])
            else:
                continue
            if xmax:
                lowhigh_ratios[label].GetXaxis().SetRangeUser(xmin, xmax)
    
            if i==0:
                lowhigh_ratios[label].Draw("e0")
            else:
                lowhigh_ratios[label].Draw("same e0")
    
            lowhigh_ratios[label].SetTitle(";;low/high")
            lowhigh_ratios[label].GetXaxis().SetTitleSize(0)
            lowhigh_ratios[label].GetYaxis().SetTitleSize(0.2)
            lowhigh_ratios[label].GetYaxis().SetTitleOffset(0.24)
            lowhigh_ratios[label].GetYaxis().SetRangeUser(1.5e-1,0.5e1)
            lowhigh_ratios[label].GetYaxis().SetNdivisions(4)
            lowhigh_ratios[label].GetXaxis().SetLabelSize(0)
            lowhigh_ratios[label].GetYaxis().SetLabelSize(0.2)
            lowhigh_ratios[label].SetLineColor(kBlack)
            if "data" in label:
                lowhigh_ratios[label].SetMarkerColor(kBlack)
                lowhigh_ratios[label].SetLineColorAlpha(1, 0)

        pad3.SetLogy(True)
        pad3.SetGridx(True)
        pad3.SetGridy(True)
    
    canvas.SaveAs(path + "/plots/waterfall_" + bg + "_" + tag + "_" + suffix + ".pdf")        
    

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest="index", default=False)
    parser.add_option("--runmode", dest="runmode", default="grid")
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--plot", dest="plot", action="store_true")
    parser.add_option("--waterfall", dest="waterfall", action="store_true") 
    parser.add_option("--template", dest="template", default=False)       
    parser.add_option("--submit", dest="submit", action="store_true") 
    (options, args) = parser.parse_args()

    configurations = get_configurations()
    path = configurations[configurations.keys()[0]][5]

    if not options.template:        
        options.template = path + "/template.root"

    if options.index:

        label = configurations.keys()[int(options.index)]
               
        histogram = get_single_histogram(configurations[configurations.keys()[int(options.index)]])
        os.system("mkdir -p %s/template_histos" % path)
        fout = TFile(path + "/template_histos/template_pt%s.root" % options.index, "recreate")
        histogram.SetName(label)
        histogram.Write()
        fout.Close()

    elif options.hadd:

        os.system("hadd -f %s %s/template_histos/template_pt*.root" % (options.template, path))

    elif options.plot:

        for tag in ["loose1", "loose2", "loose3"]:
            for prefix in [""]:

                try:
                    plot(options.template, variable = "log10(tracks_massfromdeDxStrips)", tag = tag, category = "long", lumi = 26216, xmin=1, xmax=5, extra_text = "", path = path, prefix = prefix)
                    plot(options.template, variable = "log10(tracks_massfromdeDxPixel)", tag = tag, category = "short", lumi = 26216, xmin=1, xmax=5, extra_text = "", path = path, prefix = prefix)
                except:
                    print "Missing histos for", tag, prefix, "?"
                
    elif options.waterfall:
        
        for bg in ["prompt", "fake"]:
            for tag in ["loose1", "loose2", "loose3"]:
                prefixes = ["MHT1_", "MHT4_"]
                waterfall_plot(options.template, variable = "log10(tracks_massfromdeDxStrips)", tag = tag, category = "long", bg = bg, path = path, prefixes = prefixes, suffix = "highlowMHT")
                waterfall_plot(options.template, variable = "log10(tracks_massfromdeDxStrips)", tag = tag, category = "long", bg = bg, path = path, prefixes = prefixes, include_sg = True, include_bg = False, suffix = "highlowMHT_signal")

                prefixes = ["njets1_", "njets2_"]
                waterfall_plot(options.template, variable = "log10(tracks_massfromdeDxStrips)", tag = tag, category = "long", bg = bg, path = path, prefixes = prefixes, suffix = "highlowJets")
                waterfall_plot(options.template, variable = "log10(tracks_massfromdeDxStrips)", tag = tag, category = "long", bg = bg, path = path, prefixes = prefixes, include_sg = True, include_bg = False, suffix = "highlowJets_signal")

    elif options.submit:

        commands = []
        for i in range(len(configurations)):
            commands.append("./template_fit.py --index %s" % i)
        raw_input("running %s jobs!" % len(commands) )
        runParallel(commands, options.runmode, condorDir = "template_fit_condor", dontCheckOnJobs=False)

    
