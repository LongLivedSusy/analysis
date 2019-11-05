#!/bin/env python
from __future__ import division
import glob
from ROOT import *
import plotting
import uuid
import os
#from fitter import *

gStyle.SetOptStat(0);
gROOT.SetBatch(True)

def stack_histograms(histos, outputdir, samples, variable, xlabel, ylabel, signal_scaling_factor=0.00276133, suffix="", outformat="pdf", logx=False, logy=True, save_shape=False):

    canvas = TCanvas("canvas", "canvas", 900, 800)

    pad1 = TPad("pad1", "pad1", 0, 0.16, 1, 1.0)
    pad1.SetRightMargin(0.05)
    pad1.SetLogx(logx)
    pad1.SetLogy(logy)
    pad2 = TPad("pad2", "pad2", 0.0, 0.025, 1.0, 0.235)
    pad2.SetBottomMargin(0.25)
    pad2.SetRightMargin(0.05)
    pad2.SetLogx(logx)
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
   
    legend_bkg = TLegend(0.30, 0.70, 0.55, 0.90)
    legend_bkg.SetNColumns(2)
    legend_bkg.SetTextSize(0.03)
    legend_sig = TLegend(0.60, 0.70, 0.94, 0.90)
    legend_sig.SetNColumns(2)
    legend_sig.SetTextSize(0.03)
    minimum_y_value = 1e6

    global_minimum = 1e10
    global_maximum = 1e-10
   
    mcstack = THStack("mcstack-%s" % str(uuid.uuid1()), "")

    samples_for_sorting = []

    # get lumi value:
    lumi = 135900
    unblind = False
    for label in sorted(histos):
	# check data in sample list
        if samples[label]["type"] == "data":
            lumi = samples[label]["lumi"]
	    unblind = True

    # plot backgrounds:
    for label in sorted(histos):

        if samples[label]["type"] == "bg":
	    histos[label].Scale(lumi)
	## signal scaling factor : cross-section in pb
        if samples[label]["type"] == "sg":
	    histos[label].Scale(lumi*signal_scaling_factor)

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
        legend_bkg.AddEntry(histos[label[0]], label[0])
        legend_bkg.AddEntry(histos[label[0]], '(%0.2f)'%(histos[label[0]].Integral()),"")
                                
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
            legend_sig.AddEntry(histos[label], label)
            legend_sig.AddEntry(histos[label], '(%0.2f)'%(histos[label].Integral()),"")

    print "Combining"
    combined_mc_background = 0
    for label in sorted(histos):
        if samples[label]["type"] == "bg":
            if combined_mc_background == 0:
                combined_mc_background = histos[label].Clone()
            else:
                combined_mc_background.Add(histos[label])       
    
    combined_mc_background.SetFillStyle(3004)
    combined_mc_background.SetFillColorAlpha(1,0.95)
    combined_mc_background.SetLineWidth(1)
    combined_mc_background.Draw("same e2")
    legend_bkg.AddEntry(combined_mc_background, "Total backgrounds stat.err")
    legend_bkg.AddEntry(combined_mc_background, " " ,"")
    
    combined_mc_signal = 0
    for label in sorted(histos):
        if samples[label]["type"] == "sg":
            if combined_mc_signal == 0:
                combined_mc_signal = histos[label].Clone()
            else:
                combined_mc_signal.Add(histos[label])       

    #combined_mc_signal.SetLineColor(kYellow)
    #combined_mc_signal.Draw("same hist")
    #legend_sig.AddEntry(combined_mc_signal, "Total signal")
    #legend_sig.AddEntry(combined_mc_signal, '(%0.2f)'%(combined_mc_signal.Integral()),"")

    # plot data:
    for label in sorted(histos):
        if samples[label]["type"] == "data":
            histos[label].SetLineColor(samples[label]["color"])
            histos[label].SetMarkerColor(samples[label]["color"])
            histos[label].SetMarkerColor(samples[label]["color"])
            histos[label].SetMarkerStyle(20)
            histos[label].SetMarkerSize(1)
            #histos[label].SetLineWidth(0)
	    histos[label].Draw("same e1")
	    legend_sig.AddEntry(histos[label], label)
	    legend_sig.AddEntry(histos[label], '(%0.2f)'%(histos[label].Integral()),"")
    
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

    legend_bkg.SetBorderSize(0)
    legend_bkg.SetFillStyle(0)
    legend_bkg.Draw()
    legend_sig.SetBorderSize(0)
    legend_sig.SetFillStyle(0)
    legend_sig.Draw()

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
    
    data = 0
    for label in sorted(histos):
        if samples[label]["type"] == "data":
            data = histos[label].Clone()
  
    if unblind : 
	ratio = data.Clone()
	ratio_mc = combined_mc_background.Clone()
	ratio.Divide(combined_mc_background)
    	ratio_mc.Divide(combined_mc_background)
	ratio.Draw("same e0")
    	ratio_mc.Draw("same e2")
    else : 
	ratio = combined_mc_background.Clone()
	ratio.Divide(combined_mc_background)
	ratio.Draw("same e2")
    #ratio.GetXaxis().SetRangeUser(xmin, xmax)


    ratio.SetTitle(";%s;Data/MC" % xlabel)
    pad2.SetGridx(True)
    pad2.SetGridy(True)
    pad2.SetTickx()
    ratio.GetXaxis().SetTitleSize(0.13)
    ratio.GetYaxis().SetTitleSize(0.13)
    ratio.GetYaxis().SetTitleOffset(0.38)
    ratio.GetYaxis().SetRangeUser(-1,5)
    ratio.GetYaxis().SetNdivisions(6)
    ratio.GetXaxis().SetLabelSize(0.15)
    ratio.GetYaxis().SetLabelSize(0.15)
    
    os.system("mkdir -p %s" % (outputdir))
    canvas.SaveAs("%s/%s%s.%s" % (outputdir, variable, suffix, outformat))

    # Save combined MC histogram for fitting
    if save_shape == True : 
	os.system("mkdir -p ./shapes")
	fout = TFile("./shapes/shape_%s.root"%variable,"recreate")
    	combined_mc_background.SetName("combined_mc_background")
    	combined_mc_background.Write()
    	for label in sorted(histos):
    	    if samples[label]["type"] == "sg":
    	        histos[label].SetName(label)
    	        histos[label].Write()
    	    #if samples[label]["type"] == "bg":
    	    #    histos[label].SetName(label)
    	    #    histos[label].Write()
    	    if samples[label]["type"] == "data":
    	        histos[label].SetName(label)
    	        histos[label].Write()
