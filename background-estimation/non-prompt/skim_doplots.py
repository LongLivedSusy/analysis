#!/bin/env python
import sys, os, glob
from ROOT import *

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def stamp_plot():

    # from Sam:
    showlumi = False
    lumi = 150
    tl = TLatex()
    tl.SetNDC()
    cmsTextFont = 61
    extraTextFont = 52
    lumiTextSize = 0.6
    lumiTextOffset = 0.2
    cmsTextSize = 0.75
    cmsTextOffset = 0.1
    regularfont = 42
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(0.85*tl.GetTextSize())
    tl.DrawLatex(0.135,0.915, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(1.0/0.9*tl.GetTextSize())
    xlab = 0.23
    tl.DrawLatex(xlab,0.915, 'simulation preliminary')
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
    xthing = 0.6202
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.915,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())


def control_plot(rootfile = "skimplots.root"):
    
    fin = TFile("output_skim/merged_bg.root", "READ")
    colors = [kBlack, kBlue, kRed, kGreen, kBlue+2, kAzure, kRed, kOrange]

    histos = {}
    for label in ["h_region", "h_region_prompt", "h_region_actualfakes", "h_region_xFR_dilepton", "h_region_xFR_qcd", "h_region_noDT", "h_region_noDT_xFR_dilepton", "h_region_noDT_xFR_qcd"]:
        histos[label] = fin.Get(label)
        histos[label].SetLineWidth(2)
        histos[label].SetLineColor(colors.pop(0))

    fout = TFile(rootfile, "update")

    canvas = TCanvas("regions", "regions", 800, 800)  
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

    histos["h_region"].Draw("hist")
    histos["h_region"].GetXaxis().SetRangeUser(0,33)
    histos["h_region"].SetTitle(";;events")

    histos["h_region_noDT"].Draw("same hist")
    histos["h_region_noDT"].SetFillStyle(3003)
    histos["h_region_noDT"].SetLineWidth(0)
    histos["h_region_noDT"].SetFillColor(1)

    histos["h_region_prompt"].Draw("same")
    histos["h_region_actualfakes"].Draw("same")

    histos["h_region_noDT_xFR_dilepton"].Draw("same p")
    histos["h_region_noDT_xFR_qcd"].Draw("same p")

    legend = TLegend(0.4, 0.75, 0.89, 0.89)
    legend.SetTextSize(0.025)
    legend.AddEntry(histos["h_region"], "signal region (SR)")
    legend.AddEntry(histos["h_region_prompt"], "prompt background in SR (MC Truth)")
    legend.AddEntry(histos["h_region_actualfakes"], "non-prompt background in SR (MC Truth)")
    legend.AddEntry(histos["h_region_noDT"], "control region (CR)")
    legend.AddEntry(histos["h_region_noDT_xFR_dilepton"], "prediction from CR (dilepton method)")
    legend.AddEntry(histos["h_region_noDT_xFR_qcd"], "prediction from CR (QCD method)")
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
    latex.DrawLatex(0.93, 0.91, "1 fb^{-1} (13 TeV)")

    # ratio plot
    pad2.cd()
    ratio = histos["h_region_noDT_xFR_dilepton"].Clone()
    ratio.Divide(histos["h_region_actualfakes"])
    ratio.GetXaxis().SetRangeUser(0,33)
    ratio.Draw()
    ratio.SetTitle(";signal / control region bin;Pred./Truth")
    pad2.SetGridx(True)
    pad2.SetGridy(True)
    ratio.GetXaxis().SetTitleSize(0.12)
    ratio.GetYaxis().SetTitleSize(0.12)
    ratio.GetYaxis().SetTitleOffset(0.4)
    ratio.GetYaxis().SetRangeUser(0,10)
    ratio.GetYaxis().SetNdivisions(4)
    ratio.GetXaxis().SetLabelSize(0.15)
    ratio.GetYaxis().SetLabelSize(0.15)

    canvas.Write()

    fout.Close()
    fin.Close()


# set to True to do an hadd:
if False:
    os.system("hadd -f output_skim/merged_bg.root output_skim/Summer16*root")
    for period in ["2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H"]:
        os.system("hadd -f output_skim/merged_%s.root output_skim/Run%s*root" % (period, period))

control_plot()
