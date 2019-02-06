#!/bin/env python
import sys, os, glob
import os
from ROOT import *
from plotting import *

def control_plot(folder, label, rootfile, lumi = 2.572 + 4.242, lepton_region = ""):
    
    histos = {}

    # read MC background:
    for data_type in ["bg", "2016_SingleElectron"]:

        if "2016" in data_type or "2017" in data_type or "2018" in data_type:
            is_data = True
        else:
            is_data = False

        fin = TFile(folder + "/merged_%s.root" % data_type, "READ")
        colors = [kBlack, kBlue, kRed, kGreen, kBlue+2, kAzure, kRed, kOrange]
        
        for ilabel in ["h_region", "h_region_prompt", "h_region_actualfakes", "h_region_xFR_dilepton", "h_region_xFR_qcd", "h_region_noDT", "h_region_noDT_xFR_dilepton", "h_region_noDT_xFR_qcd"]:

            if "zeroleptons" in lepton_region:
                file_label = ilabel.replace("h_region", "h_zeroleptons_region")
            elif "onelepton" in lepton_region:
                file_label = ilabel.replace("h_region", "h_onelepton_region")
            else:
                file_label = ilabel

            print "file_label", file_label

            if is_data: data_type = "data"

            ilabel = ilabel + "_%s" % data_type

            histos[ilabel] = fin.Get(file_label).Clone()
            histos[ilabel].SetDirectory(0)
            histos[ilabel].SetLineWidth(2)
            color = colors.pop(0)
            histos[ilabel].SetLineColor(color)
            # scale all MC histos to given lumi:
            if not is_data:
                histos[ilabel].Scale(lumi)

            if "xFR" in ilabel or is_data:
                histos[ilabel].SetMarkerStyle(22)
                histos[ilabel].SetMarkerColor(color)
                histos[ilabel].SetMarkerSize(1)
            else:
                histos[ilabel].SetFillColor(color)

        fin.Close()


    fout = TFile(rootfile, "update")

    if lepton_region != "":
        label = label + "_" + lepton_region

    canvas = TCanvas("%s_closure" % label, "%s_closure" % label, 800, 800)
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

    histos["h_region_bg"].Draw("hist e")
    histos["h_region_bg"].SetFillStyle(3003)
    histos["h_region_bg"].GetXaxis().SetRangeUser(1,33)
    histos["h_region_bg"].GetXaxis().SetLabelSize(0)
    histos["h_region_bg"].GetYaxis().SetRangeUser(1e-5,2e6)
    histos["h_region_bg"].SetTitle(";;events")

    histos["h_region_noDT_bg"].Draw("same hist e")
    histos["h_region_noDT_bg"].SetFillColor(0)
    histos["h_region_noDT_bg"].SetLineColor(1)

    histos["h_region_prompt_bg"].Draw("same hist e")
    histos["h_region_prompt_bg"].SetFillStyle(3003)
    histos["h_region_actualfakes_bg"].Draw("same hist e")
    histos["h_region_actualfakes_bg"].SetFillStyle(3003)

    histos["h_region_noDT_xFR_dilepton_bg"].Draw("same p")
    histos["h_region_noDT_xFR_qcd_bg"].Draw("same p")

    # draw data:
    histos["h_region_noDT_xFR_dilepton_data"].Draw("same p")
    histos["h_region_noDT_xFR_dilepton_data"].SetMarkerStyle(20)
    histos["h_region_noDT_xFR_dilepton_data"].SetMarkerColor(kRed)
    histos["h_region_noDT_xFR_dilepton_data"].SetLineColorAlpha(0, 0)

    histos["h_region_noDT_xFR_qcd_data"].Draw("same p")
    histos["h_region_noDT_xFR_qcd_data"].SetMarkerStyle(20)
    histos["h_region_noDT_xFR_qcd_data"].SetMarkerColor(kOrange)
    histos["h_region_noDT_xFR_qcd_data"].SetLineColorAlpha(0, 0)

    histos["h_region_noDT_data"].Draw("same p")
    histos["h_region_noDT_data"].SetMarkerStyle(20)
    histos["h_region_noDT_data"].SetMarkerColor(kBlack)
    histos["h_region_noDT_data"].SetLineColorAlpha(0, 0)

    legend = TLegend(0.4, 0.7, 0.89, 0.89)
    legend.SetTextSize(0.025)
    #legend.AddEntry(histos["h_region_bg"], "signal region (SR)")
    legend.AddEntry(histos["h_region_prompt_bg"], "prompt background in SR (MC Truth)")
    legend.AddEntry(histos["h_region_actualfakes_bg"], "non-prompt background in SR (MC Truth)")
    legend.AddEntry(histos["h_region_noDT_bg"], "control region (MC)")
    legend.AddEntry(histos["h_region_noDT_data"], "control region (Data)")
    legend.AddEntry(histos["h_region_noDT_xFR_dilepton_bg"], "prediction from MC (Dilepton method)")
    legend.AddEntry(histos["h_region_noDT_xFR_qcd_bg"], "prediction from MC (QCD method)")
    legend.AddEntry(histos["h_region_noDT_xFR_dilepton_data"], "prediction from Data (Dilepton method)")
    legend.AddEntry(histos["h_region_noDT_xFR_qcd_data"], "prediction from Data (QCD method)")
    legend.SetBorderSize(0)

    if "zeroleptons" in lepton_region:
        legend.SetHeader("n_{lepton} = 0")
    elif "onelepton" in lepton_region:
        legend.SetHeader("n_{lepton} = 1")
    else:
        legend.SetHeader("n_{lepton} #geq 0")

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
    ratio_dilepton = histos["h_region_noDT_xFR_dilepton_bg"].Clone()
    ratio_dilepton.Divide(histos["h_region_actualfakes_bg"])
    ratio_dilepton.GetXaxis().SetRangeUser(1,33)
    ratio_dilepton.Draw("e0")

    ratio_qcd = histos["h_region_noDT_xFR_qcd_bg"].Clone()
    ratio_qcd.Divide(histos["h_region_actualfakes_bg"])
    ratio_qcd.GetXaxis().SetRangeUser(1,33)
    ratio_qcd.Draw("same e0")

    # data ratio:
    #ratio_dilepton_data = histos["h_region_noDT_xFR_dilepton_data"].Clone()
    #ratio_dilepton_data.Divide(histos["h_region_actualfakes_bg"])
    #ratio_dilepton_data.GetXaxis().SetRangeUser(1,33)
    #ratio_dilepton_data.Draw("same e0")

    ratio_dilepton.SetTitle(";signal / control region bin;Pred./Truth")
    pad2.SetGridx(True)
    pad2.SetGridy(True)
    ratio_dilepton.GetXaxis().SetTitleSize(0.13)
    ratio_dilepton.GetYaxis().SetTitleSize(0.13)
    ratio_dilepton.GetYaxis().SetTitleOffset(0.38)
    ratio_dilepton.GetYaxis().SetRangeUser(0,2)
    ratio_dilepton.GetYaxis().SetNdivisions(4)
    ratio_dilepton.GetXaxis().SetLabelSize(0.15)
    ratio_dilepton.GetYaxis().SetLabelSize(0.15)

    canvas.Write()
    if not os.path.exists("plots"): os.mkdir("plots")
    canvas.SaveAs("plots/nonprompt_control_%s.pdf" % label)

    fout.Close()


# folder containing skim output:
folder = "output_skim"
merge_skim = False

# set to True to do an hadd:
if merge_skim or not os.path.exists("%s/merged_bg.root" % folder):
    os.system("hadd -f %s/merged_bg.root %s/Summer16*root" % (folder, folder))
    for dataset in ["SingleElectron", "SingleMuon"]:
        for period in ["2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H"]:
            os.system("hadd -f %s/merged_%s_%s.root %s/Run%s*%s*root" % (folder, period, dataset, folder, period, dataset))
        os.system("hadd -f %s/merged_2016_%s.root %s/Run2016*%s*root" % (folder, dataset, folder, dataset))

control_plot(folder, "bg", "plots.root")
control_plot(folder, "bg", "plots.root", lepton_region = "zeroleptons")
control_plot(folder, "bg", "plots.root", lepton_region = "onelepton")

