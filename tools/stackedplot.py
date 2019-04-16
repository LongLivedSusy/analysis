#!/bin/env python
from __future__ import division
import glob
from ROOT import *
import plotting
import uuid
import os

def get_histograms_from_folder(folder, samples, variable, cutstring, nBinsX, xmin, xmax):

    histos = {}

    for label in samples:
        histos[label] = plotting.get_histogram(variable, cutstring, tree_folder_name="Events", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=samples[label]["select"])

    return histos


def stack_histograms(histos, samples, variable, xlabel, ylabel, folder, signal_scaling_factor=1.0, suffix="", logx=False, logy=True):
 
    canvas = TCanvas("canvas", "canvas", 900, 800)

    pad1 = TPad("pad1", "pad1", 0, 0.16, 1, 1.0)
    pad1.SetRightMargin(0.05)
    pad1.SetLogy(True)
    pad2 = TPad("pad2", "pad2", 0.0, 0.025, 1.0, 0.235)
    pad2.SetBottomMargin(0.25)
    pad2.SetRightMargin(0.05)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()

    l = canvas.GetLeftMargin()
    t = canvas.GetTopMargin()
    r = canvas.GetRightMargin()
    b = canvas.GetBottomMargin()

    canvas.SetTopMargin(0.5*t)
    canvas.SetBottomMargin(1.2*b)
    canvas.SetLeftMargin(1.2*l)
    canvas.SetRightMargin(0.7*r)
    
    canvas.SetLogx(logx)
    canvas.SetLogy(logy)
   
    legend = TLegend(0.50, 0.70, 0.94, 0.94)
    legend.SetTextSize(0.03)
    minimum_y_value = 1e6

    global_minimum = 1e10
    global_maximum = 1e-10
   
    mcstack = THStack("mcstack-%s" % str(uuid.uuid1()), "")

    samples_for_sorting = []

    # get lumi value:
    lumi = -1
    for label in sorted(histos):
        if samples[label]["type"] == "data":
            lumi = samples[label]["lumi"]

    # plot backgrounds:
    for label in sorted(histos):

        if samples[label]["type"] == "bg" or samples[label]["type"] == "sg":
            histos[label].Scale(lumi)

        if histos[label].GetMinimum(0) < global_minimum:
            global_minimum = histos[label].GetMinimum(0) 
        if histos[label].GetMaximum() > global_maximum:
            global_maximum = histos[label].GetMaximum()

        if samples[label]["type"] == "bg":
            histos[label].SetFillColor(samples[label]["color"])
            histos[label].SetLineColor(samples[label]["color"])
            histos[label].SetMarkerColor(samples[label]["color"])
            histos[label].SetLineWidth(0)
            samples_for_sorting.append([label, histos[label].Integral()])
            
    # stack histograms with the largest integral to appear on the top of the stack:
    def Sort(sub_li, i_index): 
        return(sorted(sub_li, key = lambda x: x[i_index]))     

    print "Stacking"   
    for label in Sort(samples_for_sorting, 1):
        mcstack.Add(histos[label[0]])
        legend.AddEntry(histos[label[0]], label[0])
                                
    mcstack.Draw("hist")
    mcstack.GetXaxis().SetLabelSize(0)   
    mcstack.SetTitle(";;events")
    mcstack.GetYaxis().SetTitleOffset(1.3)
    mcstack.GetXaxis().SetTitleOffset(1.3)

    # plot signal:
    for label in sorted(histos):
        if samples[label]["type"] == "sg":
            histos[label].SetLineColor(samples[label]["color"])
            histos[label].SetMarkerColor(samples[label]["color"])
            histos[label].SetLineWidth(3)
            histos[label].Draw("same hist")
            legend.AddEntry(histos[label], label)

    # plot data:
    for label in sorted(histos):
        if samples[label]["type"] == "data":
            histos[label].SetLineColor(samples[label]["color"])
            histos[label].SetMarkerColor(samples[label]["color"])
            histos[label].SetMarkerColor(samples[label]["color"])
            histos[label].SetMarkerStyle(20)
            histos[label].SetMarkerSize(1)
            histos[label].SetLineWidth(0)
            histos[label].Draw("same p")
            legend.AddEntry(histos[label], label)

    # set minimum/maximum ranges   
    if global_minimum != 0:
        mcstack.SetMinimum(0.1 * global_minimum)
    else:
        mcstack.SetMinimum(1e-5)
   
    if logy:
        global_maximum_scale = 1e3
    else:
        global_maximum_scale = 1
   
    mcstack.SetMaximum(global_maximum_scale * global_maximum)

    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.Draw()

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.35 * t)

    lumi = lumi/1000
    latex.DrawLatex(1-0.7*r, 1-0.5*t+0.15*0.5*t, "%.1f fb^{-1} (13 TeV)" % lumi)
    
    latex.SetTextSize(0.35*t)
    latex.SetTextFont(52)
    latex.DrawLatex(0.4, 1-0.5*t+0.15*0.5*t, "CMS Work in Progress")
    
    # plot ratio
    pad2.cd()
    
    combined_mc_background = 0
    for label in sorted(histos):
        if samples[label]["type"] == "bg":
            if combined_mc_background == 0:
                combined_mc_background = histos[label].Clone()
            else:
                 combined_mc_background.Add(histos[label])        
    
    data = 0
    for label in sorted(histos):
        if samples[label]["type"] == "data":
            data = histos[label].Clone()
    
    ratio = data.Clone()
    ratio.Divide(combined_mc_background)
    #ratio.GetXaxis().SetRangeUser(xmin, xmax)
    ratio.Draw("same e0")

    ratio.SetTitle(";%s;Pred./Truth" % xlabel)
    pad2.SetGridx(True)
    pad2.SetGridy(True)
    ratio.GetXaxis().SetTitleSize(0.13)
    ratio.GetYaxis().SetTitleSize(0.13)
    ratio.GetYaxis().SetTitleOffset(0.38)
    ratio.GetYaxis().SetRangeUser(0,2)
    ratio.GetYaxis().SetNdivisions(4)
    ratio.GetXaxis().SetLabelSize(0.15)
    ratio.GetYaxis().SetLabelSize(0.15)
    
    os.system("mkdir -p %s/plots" % folder)
    canvas.SaveAs("%s/plots/%s%s.pdf" % (folder, variable, suffix))

