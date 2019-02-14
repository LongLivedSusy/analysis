#!/bin/env python
import os
from ROOT import *
from plotting import *
import collections

def control_plot(folder, label, rootfile = "control.root", lumi = 135.0, selected_region = "", data = "Summer16", mc = "Run2016_MET", variable = "", xlabel = "", extra_text = "", nBinsX = False, xmin = False, xmax = False, ymin = False, ymax = False, fakerate_map = "HT_n_allvertices", base_cuts = "PFCaloMETRatio<5"):
    
    if selected_region == "zeroleptons":
        base_cuts += " && n_leptons==0 "
    elif selected_region == "meta":
        base_cuts += " && meta_CR==1 "

    # get all histograms:
    histos = collections.OrderedDict()
    histos["mc"] = get_histogram(variable, base_cuts + " && n_DT>0 ", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=mc)
    histos["mc_prompt"] = get_histogram(variable, base_cuts + " && ((n_DT==1 && DT1_actualfake==0) || (n_DT==2 && DT1_actualfake==0 && DT2_actualfake==0))", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=mc)
    histos["mc_actualfakes"] = get_histogram(variable, base_cuts + " && ((n_DT==1 && DT1_actualfake==1) || (n_DT==2 && DT1_actualfake==1 && DT2_actualfake==1))", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=mc)
    histos["mc_noDT"] = get_histogram(variable, base_cuts + " && n_DT==0 ", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=mc)
    histos["mc_noDT_xFR_dilepton"] = get_histogram(variable, base_cuts + " && n_DT==0", scaling="*fakerate_dilepton_%s" % fakerate_map.replace("HT", "HT_cleaned"), nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=mc)
    histos["mc_noDT_xFR_qcd"] = get_histogram(variable, base_cuts + " && n_DT==0", scaling="*fakerate_qcd_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=mc)
    histos["mc_noDT_xFR_qcd_sideband"] = get_histogram(variable, base_cuts + " && n_DT==0", scaling="*fakerate_qcd_sideband_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=mc)

    if data:
        histos["data_noDT"] = get_histogram(variable, base_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=data)
        histos["data_noDT_xFR_dilepton"] = get_histogram(variable, base_cuts + " && n_DT==0", scaling="*fakerate_dilepton_%s" % fakerate_map.replace("HT", "HT_cleaned"), nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=data)
        histos["data_noDT_xFR_qcd"] = get_histogram(variable, base_cuts + " && n_DT==0", scaling="*fakerate_qcd_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=data)
        histos["data_noDT_xFR_qcd_sideband"] = get_histogram(variable, base_cuts + " && n_DT==0", scaling="*fakerate_qcd_sideband_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=data)

    colors = [kBlack, kBlue, kRed, kBlack, kRed, kGreen, kGreen+2, kBlue+2, kAzure, kRed, kRed, kGreen, kGreen+2, kBlack, kBlue, kRed, kGreen, kBlue+2, kAzure, kRed, kRed]

    for label in histos:
        histos[label].SetLineWidth(2)
        color = colors.pop(0)
        histos[label].SetLineColor(color)

        if not "data" in label:
            histos[label].Scale(lumi)

        if "xFR" in label or "data" in label:
            histos[label].SetMarkerStyle(22)
            histos[label].SetMarkerColor(color)
            histos[label].SetMarkerSize(1)
        else:
            histos[label].SetFillColor(color)

    # plotting:
    fout = TFile("%s/plots/%s" % (folder, rootfile), "update")

    if selected_region != "":
        label = selected_region + "_" + variable

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
    if False:
        global_ymin = 1e10
        global_ymax = 1e-10
        for histo in histos:
            current_ymin = 1e10
            for ibin in range(histos[histo].GetnBinsX()):
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

    histos["mc_noDT"].Draw("hist e")
    histos["mc_noDT"].SetFillColor(0)
    if not data:
        histos["mc_noDT"].SetLineColor(16)
    else:
        histos["mc_noDT"].SetLineColor(1)
    histos["mc_noDT"].Scale(1.0/1e2)
    if xmax:
        histos["mc_noDT"].GetXaxis().SetRangeUser(xmin, xmax)
    if ymax:
        histos["mc_noDT"].GetYaxis().SetRangeUser(ymin, ymax)
    histos["mc_noDT"].GetXaxis().SetLabelSize(0)   
    histos["mc_noDT"].SetTitle(";;events")

    if not data:
        histos["mc"].Draw("same hist e")
        histos["mc"].SetFillStyle(3003)
        histos["mc_prompt"].Draw("same hist e")
        histos["mc_prompt"].SetFillStyle(3003)

    histos["mc_actualfakes"].Draw("same hist e")
    histos["mc_actualfakes"].SetFillStyle(3003)

    histos["mc_noDT_xFR_dilepton"].Draw("same p")
    histos["mc_noDT_xFR_qcd"].Draw("same p")
    histos["mc_noDT_xFR_qcd_sideband"].Draw("same p")

    # draw data:
    if data:
        histos["data_noDT_xFR_dilepton"].Draw("same p")
        histos["data_noDT_xFR_dilepton"].SetMarkerStyle(20)
        histos["data_noDT_xFR_dilepton"].SetMarkerColor(kRed)
        histos["data_noDT_xFR_dilepton"].SetLineColorAlpha(0, 0)

        histos["data_noDT_xFR_qcd"].Draw("same p")
        histos["data_noDT_xFR_qcd"].SetMarkerStyle(20)
        histos["data_noDT_xFR_qcd"].SetMarkerColor(kOrange)
        histos["data_noDT_xFR_qcd"].SetLineColorAlpha(0, 0)

        histos["data_noDT"].Draw("same p")
        histos["data_noDT"].SetMarkerStyle(20)
        histos["data_noDT"].SetMarkerColor(kBlack)
        histos["data_noDT"].SetLineColorAlpha(0, 0)

    legend = TLegend(0.4, 0.7, 0.89, 0.89)
    legend.SetTextSize(0.025)
    if not data:
        legend.AddEntry(histos["mc"], "signal region (SR) / 100")
        legend.AddEntry(histos["mc_prompt"], "prompt background in SR (MC Truth)")
    legend.AddEntry(histos["mc_actualfakes"], "non-prompt background in SR (MC Truth)")
    legend.AddEntry(histos["mc_noDT"], "control region (MC)")
    legend.AddEntry(histos["mc_noDT_xFR_dilepton"], "prediction from MC (dilepton region)")
    legend.AddEntry(histos["mc_noDT_xFR_qcd"], "prediction from MC (QCD-only)")
    legend.AddEntry(histos["mc_noDT_xFR_qcd_sideband"], "prediction from MC (QCD sideband)")
    if data:
        legend.AddEntry(histos["data_noDT"], "control region (Data)")
        legend.AddEntry(histos["data_noDT_xFR_dilepton"], "prediction from Data (dilepton region)")
        legend.AddEntry(histos["data_noDT_xFR_qcd"], "prediction from Data (QCD region)")
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
    ratio_dilepton = histos["mc_noDT_xFR_dilepton"].Clone()
    ratio_dilepton.Divide(histos["mc_actualfakes"])
    if xmax:
        ratio_dilepton.GetXaxis().SetRangeUser(xmin, xmax)
    ratio_dilepton.Draw("e0")

    ratio_qcd = histos["mc_noDT_xFR_qcd"].Clone()
    ratio_qcd.Divide(histos["mc_actualfakes"])
    if xmax:
        ratio_qcd.GetXaxis().SetRangeUser(xmin, xmax)
    ratio_qcd.Draw("same e0")

    ratio_qcd_sideband = histos["mc_noDT_xFR_qcd_sideband"].Clone()
    ratio_qcd_sideband.Divide(histos["mc_actualfakes"])
    if xmax:
        ratio_qcd_sideband.GetXaxis().SetRangeUser(xmin, xmax)
    ratio_qcd_sideband.Draw("same e0")

    if xlabel == "":
        xlabel = variable
    if data:
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


for folder in ["output_skim_sideband2"]:

    merge_skim = True

    os.system("rm " + folder + "/plots/control.root")

    variables = {"region": [40, 0, 40],
                 "HT": [20, 0, 1000],
                 "MET": [20, 0, 1000],
                 "MHT": [20, 0, 1000],
                 "n_jets": [20, 0, 20],
                 "n_btags": [15, 0, 15],
                 "n_allvertices": [10, 0, 50],
                 "n_NVtx": [10, 0, 50],
                 "MinDeltaPhiMhtJets": [15, 0, 4],
                 }

    for region in ["zeroleptons", "inclusive", "meta"]:

        for variable in variables:

            nBinsX = variables[variable][0]
            xmin = variables[variable][1]
            xmax = variables[variable][2]
        
            if region == "inclusive":
                mc = "Summer16"
                data = "Run2016_SingleElectron"
                extra_text = "n_{leptons} #geq 0"
            elif region == "meta":
                mc = "Summer16"
                data = "Run2016_SingleElectron"
                extra_text = "meta control region"
            elif region == "zeroleptons":
                mc = "Summer16"
                data_type = "Run2016_MET"
                extra_text = "n_{leptons} = 0"

            extra_text += ", skim: %s" % folder.replace("output_skim_", "")

            control_plot(folder, variable, variable = variable, data = False, mc = mc, selected_region = region, extra_text = extra_text, nBinsX=nBinsX, xmin=xmin, xmax=xmax)

