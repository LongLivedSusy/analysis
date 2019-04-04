#!/bin/env python
import os
from ROOT import *
from plotting import *
import collections

def control_plot(folder, file_label, rootfile = "control.root", lumi = 135.0, selected_region = "", data = "Summer16", mc = "Run2016_MET", variable = "", xlabel = "", extra_text = "", nBinsX = False, xmin = False, xmax = False, ymin = False, ymax = False, fakerate_map = "HT_n_allvertices", base_cuts = "PFCaloMETRatio<5", numevents = -1):
    
    if selected_region == "zeroleptons":
        base_cuts += " && n_leptons==0 "
    elif selected_region == "onelepton":
        base_cuts += " && n_leptons==1 "
    elif selected_region == "meta":
        base_cuts += " && meta_CR==1 "

    # get all histograms:
    histos = collections.OrderedDict()
    for data_type in ["mc", "data"]:

        if data_type == "mc":
            selected_sample = mc
        else:
            selected_sample = data
        if not selected_sample: continue

        if variable != "region":

            histos["%s_noDT" % data_type] = get_histogram(variable, base_cuts + " && n_DT==0 ", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            histos["%s_noDT_xFR_dilepton" % data_type] = get_histogram(variable, base_cuts + " && n_DT==0", scaling="*fakerate_dilepton_%s" % fakerate_map.replace("HT", "HT_cleaned"), nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            histos["%s_noDT_xFR_qcd" % data_type] = get_histogram(variable, base_cuts + " && n_DT==0", scaling="*fakerate_qcd_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            histos["%s_noDT_xFR_qcd_sideband" % data_type] = get_histogram(variable, base_cuts + " && n_DT==0", scaling="*fakerate_qcd_sideband_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)

        else:

            histos["%s_noDT" % data_type] = get_histogram("region_noDT", base_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            h_region_ext = get_histogram("region_noDT_ext", base_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            h_region_ext2 = get_histogram("region_noDT_ext2", base_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            histos["%s_noDT" % data_type].Add(h_region_ext)
            histos["%s_noDT" % data_type].Add(h_region_ext2)

            histos["%s_noDT_xFR_dilepton" % data_type] = get_histogram("region_noDT", base_cuts, scaling="*fakerate_dilepton_%s" % fakerate_map.replace("HT", "HT_cleaned"), nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            h_region_ext = get_histogram("region_noDT_ext", base_cuts, scaling="*fakerate_dilepton_%s" % fakerate_map.replace("HT", "HT_cleaned"), nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            h_region_ext2 = get_histogram("region_noDT_ext2", base_cuts, scaling="*fakerate_dilepton_%s" % fakerate_map.replace("HT", "HT_cleaned"), nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            histos["%s_noDT_xFR_dilepton" % data_type].Add(h_region_ext)
            histos["%s_noDT_xFR_dilepton" % data_type].Add(h_region_ext2)
                    
            histos["%s_noDT_xFR_qcd" % data_type] = get_histogram("region_noDT", base_cuts, scaling="*fakerate_qcd_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            h_region_ext = get_histogram("region_noDT_ext", base_cuts, scaling="*fakerate_qcd_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            h_region_ext2 = get_histogram("region_noDT_ext2", base_cuts, scaling="*fakerate_qcd_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
            histos["%s_noDT_xFR_qcd" % data_type].Add(h_region_ext)
            histos["%s_noDT_xFR_qcd" % data_type].Add(h_region_ext2)
                
        histos["%s_noDT_xFR_qcd_sideband" % data_type] = get_histogram("region_noDT", base_cuts, scaling="*fakerate_qcd_sideband_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
        h_region_ext = get_histogram("region_noDT_ext", base_cuts, scaling="*fakerate_qcd_sideband_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
        h_region_ext2 = get_histogram("region_noDT_ext2", base_cuts, scaling="*fakerate_qcd_sideband_%s" % fakerate_map, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=selected_sample)
        histos["%s_noDT_xFR_qcd_sideband" % data_type].Add(h_region_ext)
        histos["%s_noDT_xFR_qcd_sideband" % data_type].Add(h_region_ext2)

    passpionveto = " && ((n_DT==1 && DT1_passpionveto==1) || (n_DT==2 && DT1_passpionveto==1 && DT2_passpionveto==1)) "

    histos["mc"] = get_histogram(variable, base_cuts + passpionveto + " && n_DT>0 ", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=mc)
    histos["mc_prompt"] = get_histogram(variable, base_cuts + passpionveto + " && ((n_DT==1 && DT1_promptbg==1) || (n_DT==2 && DT1_promptbg==1 && DT2_promptbg==1))", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=mc)
    #histos["mc_tau"] = get_histogram(variable, base_cuts + passpionveto + " && ((n_DT==1 && DT1_prompttau==1) || (n_DT==2 && DT1_prompttau==1 && DT2_prompttau==1))", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=mc)
    #histos["mc_tauwide"] = get_histogram(variable, base_cuts + passpionveto + " && ((n_DT==1 && DT1_prompttau==0 && DT1_prompttau_wideDR==1) || (n_DT==2 && DT1_prompttau==0 && DT1_prompttau_wideDR==1 && DT2_prompttau==0 && DT2_prompttau_wideDR==1))", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=mc)
    histos["mc_actualfakes"] = get_histogram(variable, base_cuts + passpionveto + " && ((n_DT==1 && DT1_actualfake==1) || (n_DT==2 && DT1_actualfake==1 && DT2_actualfake==1))", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, numevents=numevents, selected_sample=mc)

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

    canvas = TCanvas(file_label, file_label, 800, 800)
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
    if True:
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
            ymin = global_ymin * 1e-1
            ymax = global_ymax

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
        #histos["mc_tau"].Draw("same hist e")
        #histos["mc_tau"].SetFillStyle(3003)
        #histos["mc_tauwide"].Draw("same hist e")
        #histos["mc_tauwide"].SetFillStyle(3003)

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
    legend.AddEntry(histos["mc_noDT"], "control region (CR) / 100")
    if not data:
        legend.AddEntry(histos["mc"], "signal region (SR)")
        legend.AddEntry(histos["mc_prompt"], "prompt background in SR (MC Truth)")
        #legend.AddEntry(histos["mc_tau"], "#tau background in SR (MC Truth)")
        #legend.AddEntry(histos["mc_tauwide"], "#tau wide DR background in SR (MC Truth)")
    legend.AddEntry(histos["mc_actualfakes"], "non-prompt background in SR (MC Truth)")
    legend.AddEntry(histos["mc_noDT_xFR_dilepton"], "prediction using CR (dilepton region)")
    legend.AddEntry(histos["mc_noDT_xFR_qcd"], "prediction using CR (QCD-only)")
    legend.AddEntry(histos["mc_noDT_xFR_qcd_sideband"], "prediction using CR (QCD sideband)")
    if data:
        legend.AddEntry(histos["data_noDT"], "control region (Data)")
        legend.AddEntry(histos["data_noDT_xFR_dilepton"], "prediction from data (dilepton region)")
        legend.AddEntry(histos["data_noDT_xFR_qcd"], "prediction from data (QCD region)")
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
    canvas.SaveAs("%s/plots/%s.pdf" % (folder, file_label))

    fout.Close()


for folder in ["output_skim19_v3_merged/"]:

    #os.system("rm " + folder + "/plots/control.root")

    variables = {#"region": [32, 1, 33],
                 "HT": [10, 0, 1000],
                 #"MET": [20, 0, 1000],
                 "MHT": [10, 0, 1000],
                 #"n_jets": [20, 0, 20],
                 #"n_btags": [15, 0, 15],
                 #"n_allvertices": [10, 0, 50],
                 #"n_NVtx": [10, 0, 50],
                 #"MinDeltaPhiMhtJets": [15, 0, 4],
                 #"DT1_is_pixel_track": [2, 0, 2],
                 }

    #for fakerate_map in ["HT_n_allvertices", "n_allvertices", "HT", "MHT", "MHT_n_allvertices"]:
    #for fakerate_map in ["HT_n_allvertices_interpolated"]:
    #for fakerate_map in ["HT_n_allvertices"]:
    #for fakerate_map in ["n_DT"]:
    for fakerate_map in ["n_DT", "HT_n_allvertices_interpolated", "HT:n_allvertices", "MHT:n_allvertices", "n_allvertices", "MHT", "HT", "NumInteractions", "n_jets", "n_btags", "MinDeltaPhiMhtJets"]:

        #for region in ["zeroleptons", "onelepton"]:
        for region in ["zeroleptons"]:
        #for region in ["onelepton"]:

            for variable in variables:

                nBinsX = variables[variable][0]
                xmin = variables[variable][1]
                xmax = variables[variable][2]

                #base_cuts = "PFCaloMETRatio<5 && passesUniversalSelection==1 && HT>100 && n_genLeptons==0"
                #mc = "Summer16*QCD|ZJetsToNuNu"; period = "2016"
                #plotname = "QCD_ZJetsToNuNu_HT100_noGenLeptons_"
                
                base_cuts = "PFCaloMETRatio<5 && passesUniversalSelection==1 && HT>100"
                mc = "Summer16"; period = "2016"
                plotname = "orig_"

                #base_cuts = "MHT<200"
                #mc = "Summer16.QCD"; period = "2016"
                #mc = "Fall17"; period = "2017"
                #mc = "Fall17"; period = "2018"
                #plotname = "QCD_check_"
         
                if region == "onelepton":
                    data = "Run%s_SingleElectron" % period
                    extra_text = "n_{leptons} = 1"
                elif region == "zeroleptons":
                    data = "Run%s_MET" % period
                    extra_text = "n_{leptons} = 0"
                elif region == "meta":
                    data = "Run%s_SingleElectron" % period
                    extra_text = "meta control region"

                extra_text += ", cuts: %s" % base_cuts.replace("passesUniversalSelection", "passFilters")

                plotname += "closure_" + period + "_" + fakerate_map + "_" + region + "_" + variable

                if False and os.path.exists(folder + "/plots/%s.pdf" % plotname):
                    print "already done :-)"
                    continue
            
                control_plot(folder, plotname, variable=variable, data=False, mc=mc, selected_region=region, extra_text=extra_text, nBinsX=nBinsX, xmin=xmin, xmax=xmax, fakerate_map=fakerate_map, base_cuts=base_cuts)
