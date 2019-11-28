#!/bin/env python
from __future__ import division
import glob
from ROOT import *
import plotting
import uuid
import os

def get_histograms_from_folder(folder, samples, variable, cutstring, nBinsX, xmin, xmax, threads=-1, numevents=-1):

    histos = {}

    for label in samples:
        histo = plotting.get_histogram(variable, cutstring, tree_folder_name="Events", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=samples[label]["select"], threads=threads, numevents=numevents)
        if histo:
            histos[label] = histo

    return histos


def stack_histograms(histos, samples, variable, xlabel, ylabel, folder, signal_scaling_factor=1.0, suffix="", logx=False, logy=True, miniylabel="Data/MC", lumi=False, ymin=False, ymax=False, xmin=False, xmax=False, yaxis_label="Events", output_folder = ".", include_data = True, width=900):
 
    canvas = TCanvas("canvas", "canvas", width, 800)

    pad1 = TPad("pad1", "pad1", 0, 0.16, 1, 1.0)
    pad1.SetRightMargin(0.05)
    pad1.SetLogy(logy)
    pad2 = TPad("pad2", "pad2", 0.0, 0.025, 1.0, 0.235)
    pad2.SetBottomMargin(0.25)
    pad2.SetRightMargin(0.05)
    pad1.SetTopMargin(0.07)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()

    l = canvas.GetLeftMargin()
    t = canvas.GetTopMargin()
    r = canvas.GetRightMargin()
    b = canvas.GetBottomMargin()

    #canvas.SetTopMargin(0.05)
    #canvas.SetBottomMargin(1.2*b)
    #canvas.SetLeftMargin(1.2*l)
    #canvas.SetRightMargin(0.7*r)
    
    canvas.SetLogx(logx)
    canvas.SetLogy(logy)
   
    legend = TLegend(0.60, 0.65, 0.95, 0.93)
    legend.SetTextSize(0.03)
    minimum_y_value = 1e6

    global_minimum = 1e10
    global_maximum = 1e-10
   
    mcstack = THStack("mcstack-%s" % str(uuid.uuid1()), "")

    samples_for_sorting = []

    # get total lumi value:
    plot_has_data = False
    total_lumi = 0
    for label in sorted(histos):
        if samples[label]["type"] == "data" and include_data:
            plot_has_data = True
            total_lumi += samples[label]["lumi"]
    
    if not lumi and plot_has_data:
        lumi = total_lumi

    # plot backgrounds:
    for label in sorted(histos):

        if samples[label]["type"] == "bg" or samples[label]["type"] == "sg":
            histos[label].Scale(lumi * 1000.0)

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
    mcstack.SetTitle(";;%s" % yaxis_label)
    mcstack.GetYaxis().SetTitleOffset(1.3)
    mcstack.GetXaxis().SetTitleOffset(1.3)

    # plot signal:
    for label in sorted(histos):
        if samples[label]["type"] == "sg":
            histos[label].SetLineColor(samples[label]["color"])
            histos[label].SetMarkerColor(samples[label]["color"])
            histos[label].SetLineWidth(3)
            histos[label].Scale(signal_scaling_factor)
            histos[label].Draw("same hist")
            legend.AddEntry(histos[label], label)

    # plot data:
    if plot_has_data:

        combined_data = 0
        for label in sorted(histos):
            if samples[label]["type"] == "data":
                if combined_data == 0:
                    combined_data = histos[label].Clone()
                else:
                     combined_data.Add(histos[label])        

        combined_data.SetLineColor(kBlack)
        combined_data.SetMarkerColor(kBlack)
        combined_data.SetMarkerColor(kBlack)
        combined_data.SetMarkerStyle(20)
        combined_data.SetMarkerSize(1)
        combined_data.SetLineWidth(3)
        combined_data.Draw("same E & X0")
        legend.AddEntry(combined_data, "Data")

    # set minimum/maximum ranges   
    if global_minimum != 0:
        mcstack.SetMinimum(1e-2 * global_minimum)
    else:
        mcstack.SetMinimum(1e-2)

    if ymin:
        mcstack.SetMinimum(ymin)
   
    if logy:
        global_maximum_scale = 10
    else:
        global_maximum_scale = 1
   
    if not ymax:
        mcstack.SetMaximum(global_maximum_scale * global_maximum)
    else:
        mcstack.SetMaximum(ymax)

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

    latex.DrawLatex(0.95, 0.95, "%.1f fb^{-1} (13 TeV)" % lumi)
    
    #latex.SetTextSize(0.35*t)
    #latex.SetTextFont(52)
    #latex.DrawLatex(0.4, 1-0.5*t+0.15*0.5*t, "CMS Work in Progress")
    
    # plot ratio
    pad2.cd()
    
    combined_mc_background = 0
    for label in sorted(histos):
        if samples[label]["type"] == "bg":
            if combined_mc_background == 0:
                combined_mc_background = histos[label].Clone()
            else:
                 combined_mc_background.Add(histos[label])        

    if plot_has_data:
        ratio = combined_data.Clone()
    else:
        ratio = combined_mc_background.Clone()
        
    ratio.Divide(combined_mc_background)
    if xmax:
        ratio.GetXaxis().SetRangeUser(xmin, xmax)
    ratio.Draw("same e0")
    ratio.SetTitle(";%s;%s" % (xlabel, miniylabel))
    pad2.SetGridx(True)
    pad2.SetGridy(True)
    ratio.GetXaxis().SetTitleSize(0.13)
    ratio.GetYaxis().SetTitleSize(0.13)
    ratio.GetYaxis().SetTitleOffset(0.38)
    ratio.GetYaxis().SetRangeUser(0,2)
    ratio.GetYaxis().SetNdivisions(4)
    ratio.GetXaxis().SetLabelSize(0.15)
    ratio.GetYaxis().SetLabelSize(0.15)
    
    if len(output_folder)>0:
        os.system("mkdir -p %s" % output_folder)
    canvas.SaveAs("%s/%s%s.pdf" % (output_folder, variable, suffix))
    canvas.SaveAs("%s/%s%s.root" % (output_folder, variable, suffix))
    print "\n****************\n"
    
