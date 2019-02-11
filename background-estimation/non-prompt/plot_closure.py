#!/bin/env python
import os
from ROOT import *
from plotting import *

def control_plot(folder, label, rootfile, lumi = 135.0, lepton_region = "", data_type = ["Summer16", "Run2016_MET"], variable = "", xlabel = "", extra_text = "", draw_data = False, xmin = False, xmax = True, ymin = False, ymax = True):
    
    for draw_data in [False, True]:

        histos = {}

        # read MC background:
        for data_type in ["Summer16", "Run2016_MET"]:

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
                elif "meta" in lepton_region:
                    file_label = ilabel.replace("h_region", "h_meta_region")
                elif "inclusive" in lepton_region:
                    file_label = ilabel.replace("h_region", "h_inclusive_region")
                else:
                    file_label = ilabel

                print "file_label", file_label

                if is_data:
                    data_type = "data"
                else:
                    data_type = "bg"

                if variable != "":
                    file_label = file_label.replace("region", variable)

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


        fout = TFile("plots/control/" + rootfile, "update")

        if lepton_region != "":
            label = lepton_region + "_" + label

        canvas = TCanvas("closure_%s" % label, "closure_%s" % label, 800, 800)
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

        histos["h_region_noDT_bg"].Draw("hist e")
        histos["h_region_noDT_bg"].SetFillColor(0)
        if not draw_data:
            histos["h_region_noDT_bg"].SetLineColor(16)
        else:
            histos["h_region_noDT_bg"].SetLineColor(1)
        histos["h_region_noDT_bg"].Scale(1.0/1e2)
        if xmin and xmax:
            histos["h_region_noDT_bg"].GetXaxis().SetRangeUser(xmin, xmax)
        if ymin and ymax:
            histos["h_region_noDT_bg"].GetYaxis().SetRangeUser(ymin, ymax)
        histos["h_region_noDT_bg"].GetXaxis().SetLabelSize(0)   
        histos["h_region_noDT_bg"].SetTitle(";;events")

        if not draw_data:
            histos["h_region_bg"].Draw("same hist e")
            histos["h_region_bg"].SetFillStyle(3003)
            histos["h_region_prompt_bg"].Draw("same hist e")
            histos["h_region_prompt_bg"].SetFillStyle(3003)

        histos["h_region_actualfakes_bg"].Draw("same hist e")
        histos["h_region_actualfakes_bg"].SetFillStyle(3003)

        histos["h_region_noDT_xFR_dilepton_bg"].Draw("same p")
        histos["h_region_noDT_xFR_qcd_bg"].Draw("same p")

        # draw data:
        if draw_data:
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
        if not draw_data:
            legend.AddEntry(histos["h_region_bg"], "signal region (SR) / 100")
            legend.AddEntry(histos["h_region_prompt_bg"], "prompt background in SR (MC Truth)")
        legend.AddEntry(histos["h_region_actualfakes_bg"], "non-prompt background in SR (MC Truth)")
        legend.AddEntry(histos["h_region_noDT_bg"], "control region (MC)")
        legend.AddEntry(histos["h_region_noDT_xFR_dilepton_bg"], "prediction from MC (Dilepton method)")
        legend.AddEntry(histos["h_region_noDT_xFR_qcd_bg"], "prediction from MC (QCD method)")
        if draw_data:
            legend.AddEntry(histos["h_region_noDT_data"], "control region (Data)")
            legend.AddEntry(histos["h_region_noDT_xFR_dilepton_data"], "prediction from Data (Dilepton method)")
            legend.AddEntry(histos["h_region_noDT_xFR_qcd_data"], "prediction from Data (QCD method)")
        legend.SetBorderSize(0)

        if extra_text != "":
            legend.SetHeader(extra_text)

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
        if xmin and xmax:
            ratio_dilepton.GetXaxis().SetRangeUser(1,33)
        ratio_dilepton.Draw("e0")

        ratio_qcd = histos["h_region_noDT_xFR_qcd_bg"].Clone()
        ratio_qcd.Divide(histos["h_region_actualfakes_bg"])
        if xmin and xmax:
            ratio_qcd.GetXaxis().SetRangeUser(1,33)
        ratio_qcd.Draw("same e0")

        if xlabel == "":
            xlabel = variable
        if draw_data:
            label += "_data"

        ratio_dilepton.SetTitle(";%s;Pred./Truth" % xlabel)
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
        if not os.path.exists("plots/control"): os.mkdir("plots/control")
        canvas.SaveAs("plots/control/control_%s.pdf" % label)

        fout.Close()


root_file = "plots.root"
os.system("rm plots/control/%s" % root_file)

merge_skim = False
for folder in ["output_skim_2016v2_maps_bak", "output_skim_2016v2_nomaps_bak"]:

    map_type = folder.split("_")[-1]

    if merge_skim:
        os.system("hadd -f %s/merged_Run2016_MET.root %s/Run2016*MET*root" % (folder, folder))
        os.system("hadd -f %s/merged_Run2016_SingleLepton.root %s/Run2016*Single*root" % (folder, folder))
        os.system("hadd -f %s/merged_Summer16.root %s/Summer16*root" % (folder, folder))

    control_plot(folder, "region_" + map_type, root_file, data_type = ["Summer16", "Run2016_SingleLepton"], xlabel = "signal / control region bin", extra_text = "n_{lepton} #geq 0")
    control_plot(folder, "MHT_" + map_type, root_file, data_type = ["Summer16", "Run2016_SingleLepton"], variable = "MHT", extra_text = "n_{lepton} #geq 0")
    control_plot(folder, "njets_" + map_type, root_file, data_type = ["Summer16", "Run2016_SingleLepton"], variable = "njets", extra_text = "n_{lepton} #geq 0")

    control_plot(folder, "region_" + map_type, root_file, data_type = ["Summer16", "Run2016_MET"], lepton_region = "zeroleptons", xlabel = "signal / control region bin", extra_text = "n_{lepton} = 0")
    control_plot(folder, "MHT_" + map_type, root_file, data_type = ["Summer16", "Run2016_MET"], lepton_region = "zeroleptons", variable = "MHT", extra_text = "n_{lepton} = 0")
    control_plot(folder, "njets_" + map_type, root_file, data_type = ["Summer16", "Run2016_MET"], lepton_region = "zeroleptons", variable = "njets", extra_text = "n_{lepton} = 0")

    control_plot(folder, "MHT_" + map_type, root_file, data_type = ["Summer16", "Run2016_SingleLepton"], lepton_region = "meta", variable = "MHT", extra_text = "meta CR")
    control_plot(folder, "njets_" + map_type, root_file, data_type = ["Summer16", "Run2016_SingleLepton"], lepton_region = "meta", variable = "njets", extra_text = "meta CR")

