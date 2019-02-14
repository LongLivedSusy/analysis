#!/bin/env python
import os
from ROOT import *
from plotting import *

def control_plot(folder, label, rootfile = "control.root", lumi = 135.0, selected_region = "", data_types = ["Summer16", "Run2016_MET"], variable = "", xlabel = "", extra_text = "", draw_data = False, xmin = False, xmax = False, ymin = False, ymax = False):
    
    histos = {}

    for data_type in data_types:

        if "2016" in data_type or "2017" in data_type or "2018" in data_type:
            is_data = True
        else:
            is_data = False

        try:
            fin = TFile(folder + "/merged_%s.root" % data_type, "READ")
        except:
            print "cannot open", folder + "/merged_%s.root" % data_type
            return
        colors = [kBlack, kBlue, kRed, kGreen, kBlue+2, kAzure, kRed, kRed, kGreen, kGreen+2]
        
        #for ilabel in ["h_region", "h_region_prompt", "h_region_actualfakes", "h_region_xFR_dilepton", "h_region_xFR_qcd", "h_region_noDT", "h_region_noDT_xFR_dilepton", "h_region_noDT_xFR_qcd"]:
        for ilabel in ["h_region", "h_region_prompt", "h_region_actualfakes", "h_region_xFR_dilepton", "h_region_xFR_qcd", "h_region_xFR_qcd_sideband", "h_region_noDT", "h_region_noDT_xFR_dilepton", "h_region_noDT_xFR_qcd", "h_region_noDT_xFR_qcd_sideband"]:

            if selected_region != "":
                file_label = ilabel.replace("h_region", "h_%s_region" % selected_region)
            else:
                file_label = ilabel

            if is_data:
                data_type = "data"
            else:
                data_type = "bg"

            if variable != "":
                file_label = file_label.replace("region", variable)

            ilabel = ilabel + "_%s" % data_type

            #file_label = file_label.replace("qcd", "qcd_sideband")
            histos[ilabel] = fin.Get("hists/" + file_label).Clone()
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


    fout = TFile("%s/plots/%s" % (folder, rootfile), "update")

    if selected_region != "":
        label = selected_region + "_" + label

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

    # y axis autoscaler
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
        ymin = global_ymin * 1e2
        ymax = global_ymax * 1e1

    histos["h_region_noDT_bg"].Draw("hist e")
    histos["h_region_noDT_bg"].SetFillColor(0)
    if not draw_data:
        histos["h_region_noDT_bg"].SetLineColor(16)
    else:
        histos["h_region_noDT_bg"].SetLineColor(1)
    histos["h_region_noDT_bg"].Scale(1.0/1e2)
    if xmax:
        histos["h_region_noDT_bg"].GetXaxis().SetRangeUser(xmin, xmax)
    if ymax:
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
    histos["h_region_noDT_xFR_qcd_sideband_bg"].Draw("same p")

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
    legend.AddEntry(histos["h_region_noDT_xFR_dilepton_bg"], "prediction from MC (dilepton region)")
    legend.AddEntry(histos["h_region_noDT_xFR_qcd_bg"], "prediction from MC (QCD-only)")
    legend.AddEntry(histos["h_region_noDT_xFR_qcd_sideband_bg"], "prediction from MC (QCD sideband)")
    if draw_data:
        legend.AddEntry(histos["h_region_noDT_data"], "control region (Data)")
        legend.AddEntry(histos["h_region_noDT_xFR_dilepton_data"], "prediction from Data (dilepton region)")
        legend.AddEntry(histos["h_region_noDT_xFR_qcd_data"], "prediction from Data (QCD region)")
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
    if xmax:
        ratio_dilepton.GetXaxis().SetRangeUser(xmin, xmax)
    ratio_dilepton.Draw("e0")

    ratio_qcd = histos["h_region_noDT_xFR_qcd_bg"].Clone()
    ratio_qcd.Divide(histos["h_region_actualfakes_bg"])
    if xmax:
        ratio_qcd.GetXaxis().SetRangeUser(xmin, xmax)
    ratio_qcd.Draw("same e0")

    ratio_qcd_sideband = histos["h_region_noDT_xFR_qcd_sideband_bg"].Clone()
    ratio_qcd_sideband.Divide(histos["h_region_actualfakes_bg"])
    if xmax:
        ratio_qcd_sideband.GetXaxis().SetRangeUser(xmin, xmax)
    ratio_qcd_sideband.Draw("same e0")

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
    if not os.path.exists("%s/plots" % folder): os.mkdir("%s/plots" % folder)
    canvas.SaveAs("%s/plots/control_%s.pdf" % (folder, label))

    fout.Close()


#for folder in ["output_skim_2016v2_maps", "output_skim_2016v2_nomaps"]:
for folder in ["output_skim_sideband"]:

    merge_skim = True

    os.system("rm " + folder + "/plots/control.root")

    if merge_skim:
        os.system("hadd -f %s/merged_Run2016_SingleMuon.root %s/Run2016*SingleMuon*root" % (folder, folder))
        os.system("hadd -f %s/merged_Run2016_SingleElectron.root %s/Run2016*SingleElectron*root" % (folder, folder))
        os.system("hadd -f %s/merged_Run2016_MET.root %s/Run2016*MET*root" % (folder, folder))
        os.system("hadd -f %s/merged_Summer16.root %s/Summer16*root" % (folder, folder))

    variables = {"region": [40, 0, 40],
                 "HT": [20, 0, 1000],
                 "MET": [20, 0, 1000],
                 "MHT": [20, 0, 1000],
                 "njets": [20, 0, 20],
                 "n_btags": [15, 0, 15],
                 "n_allvertices": [10, 0, 50],
                 "MinDeltaPhiMhtJets": [15, 0, 4],
                 }

    for region in ["inclusive", "meta", "zeroleptons"]:
        for variable in variables:

            xmin = variables[variable][1]
            xmax = variables[variable][2]
        
            if region == "inclusive":
                data_type = ["Summer16", "Run2016_SingleElectron"]
                extra_text = "n_{leptons} #geq 0"
            elif region == "meta":
                data_type = ["Summer16", "Run2016_SingleElectron"]
                extra_text = "meta control region"
            elif region == "zeroleptons":
                data_type = ["Summer16", "Run2016_MET"]
                extra_text = "n_{leptons} = 0"

            extra_text += ", skim: %s" % folder.replace("output_skim_", "")

            control_plot(folder, variable, variable = variable, data_types = data_type, selected_region = region, extra_text = extra_text, xmin=xmin, xmax=xmax)

