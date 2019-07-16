#!/bin/env python
import os
from ROOT import *
from plotting import *
import collections

def closure_plot(root_file, variable, tag, category, canvas_label, extra_text = "", xlabel = False, lumi = 1.0, autoscaling = True, xmax = False, ymax = False, ymin = False, fr_regions = ["dilepton", "dilepton_lowMHT", "qcd_lowlowMHT", "qcd_lowMHT", "qcd_sideband"], fr_maps = ["HT_n_allvertices"], output_root_file = False):
   
    if variable == "n_jets":
        xmin = 0
        xmax = 30
   
    histos = collections.OrderedDict()

    tfile = TFile(root_file, "open")

    histos["mc_nonprompt"] = tfile.Get("%s_%s_fakebg_%s" % (variable, tag, category) )
    histos["mc_prompt"] = tfile.Get("%s_%s_promptbg_%s" % (variable, tag, category) )
    histos["mc_CR"] = tfile.Get("%s_%s_control_%s" % (variable, tag, category) )
        
    for fr_region in fr_regions:
        for fr_map in fr_maps:
            histos["mc_prediction_%s_%s" % (fr_region, fr_map)] = tfile.Get("%s_%s_%s_%s_%s_prediction" % (variable, fr_region, tag, category, fr_map) )
  
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

    histos["mc_CR"].Draw("hist e")
    histos["mc_CR"].SetLineColor(16)

    if xmax:
        histos["mc_CR"].GetXaxis().SetRangeUser(xmin, xmax)
    if ymax:
        histos["mc_CR"].GetYaxis().SetRangeUser(ymin, ymax)
    histos["mc_CR"].GetXaxis().SetLabelSize(0)   
    histos["mc_CR"].SetTitle(";;events")

    histos["mc_prompt"].Draw("same hist e")
    histos["mc_nonprompt"].Draw("same hist e")

    legend = TLegend(0.4, 0.7, 0.89, 0.89)
    legend.SetHeader(extra_text)
    legend.SetTextSize(0.025)
    legend.AddEntry(histos["mc_CR"], "control region (CR)")
    legend.AddEntry(histos["mc_prompt"], "prompt background in SR (MC Truth)")
    legend.AddEntry(histos["mc_nonprompt"], "non-prompt background in SR (MC Truth)")
    legend.SetBorderSize(0)

    for label in histos:
        if "prediction" in label:
    
            legend.AddEntry(histos[label], label)
    
            if "mc" in label:
                histos[label].Draw("same p")   
    
            if "data" in label:
                histos[label].SetMarkerStyle(20)
                histos[label].SetMarkerColor(kOrange)
                histos[label].SetLineColorAlpha(0, 0)
    
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
        if "prediction" in label:
            ratios[label] = histos[label].Clone()
            ratios[label].Divide(histos["mc_nonprompt"])
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

    output_path = "/".join( root_file.split("/")[:-1] )

    canvas.SaveAs(output_path + "/" + canvas_label + ".pdf")

    if output_root_file:
        fout = TFile(output_path + "/" + canvas_label + ".root", "recreate")
        canvas.Write()
        fout.Close()


if __name__ == "__main__":

    root_file = "output_skim_12_merged_prediction/addedbg.root"

    for variable in ["region_short", "region_long", "region_multi", "MHT", "n_jets"]:
        for tag in ["tight", "loose1", "loose2", "loose3"]:
            for category in ["short", "long"]:
                #for fr_map in ["HT", "n_allvertices", "HT_n_allvertices"]:
                for fr_map in ["HT_n_allvertices"]:                   
            
                    if "short" in variable and category != "short": continue
                    if "long" in variable and category != "long": continue
                                
                    canvas_label = "prediction_%s_%s_%s_%s" % (variable, tag, category, fr_map)
            
                    closure_plot(root_file, variable, tag, category, canvas_label, fr_maps = [fr_map])
        

