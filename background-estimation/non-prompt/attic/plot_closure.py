#!/bin/env python
import os
from ROOT import *
from plotting import *
import collections
import multiprocessing 

def closure_plot(variable, folder, file_label, regions, selected_mc, selected_data, base_cuts, fakerate_map, extra_text, nBinsX, xmin, xmax, category, rootfile="control.root", lumi=135.0, xlabel=False, ymin=False, ymax=False, autoscaling=True, numevents=-1):
   
    histos = collections.OrderedDict()

    category_cuts = ""
    if category == "short":
        category_cuts = " && tracks_is_pixel_track==1"
    elif category == "long":
        category_cuts = " && tracks_is_pixel_track==0"

    histos["mc_prompt"] = get_histogram(variable, base_cuts + category_cuts + " && n_DT_bdt>0 && n_DT_actualfake_bdt==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=selected_mc, numevents=numevents)
    histos["mc_nonprompt"] = get_histogram(variable, base_cuts + category_cuts + " && n_DT_bdt==n_DT_actualfake_bdt && n_DT_actualfake_bdt>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=selected_mc, numevents=numevents)

    for data_type in ["mc", "data"]:

        if data_type == "data" and selected_data == "":
            continue

        if data_type == "mc":
            selected_sample = selected_mc
        else:
            selected_sample = selected_data

        histos["%s_CR" % data_type] = get_histogram(variable, base_cuts, nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=selected_sample, numevents=numevents)
        for region in regions:

            if len(category)>0: region = region + "_" + category

            histos["%s_prediction_%s" % (data_type, region)] = get_histogram(variable, base_cuts, scaling="*fakerate_%s_%s" % (region, fakerate_map), nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=selected_sample, numevents=numevents)
         
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
            ymin = global_ymin * 1e-1
            ymax = global_ymax

    histos["mc_CR"].Draw("hist e")
    histos["mc_CR"].SetFillColor(0)
    histos["mc_CR"].SetLineColor(16)

    if xmax:
        histos["mc_CR"].GetXaxis().SetRangeUser(xmin, xmax)
    if ymax:
        histos["mc_CR"].GetYaxis().SetRangeUser(ymin, ymax)
    histos["mc_CR"].GetXaxis().SetLabelSize(0)   
    histos["mc_CR"].SetTitle(";;events")

    histos["mc_prompt"].Draw("same hist e")
    histos["mc_prompt"].SetFillStyle(3003)
    histos["mc_nonprompt"].Draw("same hist e")
    histos["mc_nonprompt"].SetFillStyle(3003)

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

    canvas.Write()
    if not os.path.exists("%s/plots" % folder): os.mkdir("%s/plots" % folder)
    canvas.SaveAs("%s/plots/%s.pdf" % (folder, file_label))

    print "\n ### plot saved in %s/plots/%s.pdf \n" % (folder, file_label)

    fout.Close()


def closure_plot_wrapper(args):
    return closure_plot(*args)


if __name__ == "__main__":

    folder = "output_skim_24_merged/"

    os.system("rm " + folder + "/plots/control.root")

    variables = {
                 #"region": [32, 1, 33],
                 "HT": [10, 0, 1000],
                 #"HT_cleaned": [10, 0, 1000],
                 #"MET": [20, 0, 1000],
                 #"MHT": [10, 0, 1000],
                 #"n_jets": [50, 0, 50],
                 #"n_btags": [15, 0, 15],
                 #"n_allvertices": [20, 0, 100],
                 #"n_NVtx": [10, 0, 50],
                 #"MinDeltaPhiMhtJets": [15, 0, 4],
                 #"DT1_is_pixel_track": [2, 0, 2],
                 #"n_DT_bdt": [2, 0, 2],
                }

    cuts = {
            #"dilepton": ["PFCaloMETRatio<5 && dilepton_CR==1", "Summer16", ""],
            #"QCD_ZJets_MHT": ["PFCaloMETRatio<5 && MHT<200 && n_leptons==0", "Summer16.QCD|Summer16.ZJetsToNuNu", ""],
            #"QCD_ZJets_MHT_nogen": ["PFCaloMETRatio<5 && MHT<200 && n_leptons==0 && n_genLeptons==0", "Summer16.QCD", ""],
            #"QCD_sideband_ZJets_MHT_nogen": ["PFCaloMETRatio<5 && n_leptons==0 && n_genLeptons==0 && qcd_sideband_CR==1", "Summer16.QCD", ""],
            #"QCD_ZJets_MHT_nogen_test": ["PFCaloMETRatio<5 && n_leptons==0 && n_genLeptons==0", "Summer16.QCD|Summer16.ZJetsToNuNu", ""],
            #"QCD_ZJets_MHT_nogen": ["PFCaloMETRatio<5", "Summer16", ""],
            #"QCD_single_lepton": ["PFCaloMETRatio<5 && n_leptons==0 ", "Summer16.QCD_HT200to300", ""],
            #"QCD_single_lepton_filters": ["PFCaloMETRatio<5 && passesUniversalSelection==1 && HT>100 && n_leptons==0 ", "Summer16.QCD", ""],
            #"QCD_single_lepton_nogen": ["PFCaloMETRatio<5 && n_leptons==0 && n_genLeptons==0", "Summer16.QCD", ""],
            #"new_QCD_MHT_nogen": ["PFCaloMETRatio<5 && MHT<200 && n_leptons==0 && n_genLeptons==0", "Summer16.QCD", ""],
            "new_QCD_nogen": ["PFCaloMETRatio<5 && n_leptons==0 && n_genLeptons==0", "Summer16.QCD|Summer16.ZJetsToNuNu", ""],
           }

    regions = [
               "qcd",
               "qcd_sideband",
               #"dilepton",
              ]

    fakerate_maps = [
                     #"HT",
                     #"n_allvertices",
                     "HT_n_allvertices", 
                     #"n_DT_bdt"
                     #"HT_cleaned",
                     #"HT_cleaned_n_allvertices", 
                    ]

    categories = [
                    #"",
                    "short",
                    #"long",
                 ]

    overwrite = True

    args = []

    for variable in variables:
        for fakerate_map in fakerate_maps:
            for cut in cuts:
                for category in categories:

                    nBinsX = variables[variable][0]
                    xmin = variables[variable][1]
                    xmax = variables[variable][2]
                    extra_text = cut
                    plotname = "closure_" + cut + "_" + fakerate_map + "_" + variable + category
                    base_cuts = cuts[cut][0]
                    selected_mc = cuts[cut][1]
                    selected_data = cuts[cut][2]
             
                    if not overwrite and os.path.exists(folder + "/plots/%s.pdf" % plotname):
                        print "already done!"
                        continue

                    #args.append([variable, folder, plotname, regions, selected_mc, selected_data, base_cuts, fakerate_map, extra_text, nBinsX, xmin, xmax, category])
                
                    closure_plot(variable, folder, plotname, regions, selected_mc, selected_data, base_cuts, fakerate_map, extra_text, nBinsX, xmin, xmax, category)

#pool = multiprocessing.Pool(int(multiprocessing.cpu_count() * 0.5))
#pool.map(closure_plot_wrapper, args) 
