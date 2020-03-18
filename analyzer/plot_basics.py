#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import os
import collections
import shared_utils
import glob

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

binnings = {}
binnings["MHT"] = [20, 0, 1000]
binnings["tracks_invmass"] = [50, 40, 140]
binnings["dilepton_invmass"] = [50, 40, 140]
binnings["leptons_mt"] = [16, 0, 160]
binnings["leadinglepton_mt"] = [16, 0, 160]
binnings["tracks_mva_tight:tracks_dxyVtx"] = [40, 0, 0.04, 20, 0.1, 1.0]
binnings["tracks_mva_loose:tracks_dxyVtx"] = [50, 0, 0.05, 40, -1.0, 1.0]

def plot2D(variable, cutstring, histos, lumi, pdffile, ymin=1e-1, ymax=1e5, showdata = False, drawoption = "colz"):

    # BDT sideband region plot
    
    for label in histos:
        histos[label].SetLineWidth(2)
        shared_utils.histoStyler(histos[label])

        size = 0.059
        font = 132
        histos[label].GetZaxis().SetLabelFont(font)
        histos[label].GetZaxis().SetTitleFont(font)
        histos[label].GetZaxis().SetTitleSize(size)
        histos[label].GetZaxis().SetLabelSize(size)   
        histos[label].GetZaxis().SetTitleOffset(1.2)

        histos[label].GetXaxis().SetNdivisions(5)

        histos[label].SetMarkerStyle(20)
        histos[label].SetMarkerSize(0.2)
        histos[label].SetMarkerColorAlpha(histos[label].GetFillColor(), 0.5)

        variable = variable.replace("tracks_mva_loose", "MVA score")
        variable = variable.replace("tracks_dxyVtx", "d_{xy} (cm)")
        histos[label].SetTitle(";%s;%s;Events" % (variable.split(":")[1], variable.split(":")[0]))

    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)

    canvas = shared_utils.mkcanvas()
    canvas.SetLogz(True)
    canvas.SetRightMargin(0.2)

    # combine backgrounds:
    histos["CombinedBg"] = 0
    for label in histos:
        if "Signal" not in label and "CombinedBg" not in label:
            if histos["CombinedBg"] == 0:
                histos["CombinedBg"] = histos[label].Clone()
            else:
                histos["CombinedBg"].Add(histos[label])
    if histos["CombinedBg"] == 0:
        del histos["CombinedBg"]

    for label in histos:
        histos[label].Draw(drawoption)
    
    if "/" in pdffile:
        os.system("mkdir -p %s" % "/".join(pdffile.split("/")[:-1]))

    shared_utils.stamp()
    canvas.SaveAs(pdffile + "_" + label + ".pdf")

    # draw some funky lines
    text = TLatex()
    text.SetTextFont(132)
    text.SetTextSize(0.059)

    if "short" in pdffile:
        upper_line = TLine(0, -0.25, (1 + 0.25)/(0.65/0.01), 1)
        upper_line.SetLineWidth(2)
        upper_line.Draw("same")

        #lower_line = TLine(0, -0.5, (1 + 0.5)/(0.65/0.01), 1)
        #lower_line.SetLineWidth(2)
        #lower_line.Draw("same")
        lower_line2 = TLine(0.02, -1, 0.02, 1)
        lower_line2.SetLineWidth(2)
        lower_line2.Draw("same")

        text.DrawLatex(0.005, 0.75, "SR")
        text.DrawLatex(0.03, 0.75, "CR")
    
    if "long" in pdffile:
        upper_line = TLine(0, 0.05, (1 - 0.05)/(0.7/0.01), 1)
        upper_line.SetLineWidth(2)
        upper_line.Draw("same")

        #lower_line = TLine(0, -0.5, (1 + 0.5)/(0.7/0.01), 1)
        #lower_line.SetLineWidth(2)
        #lower_line.Draw("same")
        lower_line2 = TLine(0.02, -1, 0.02, 1)
        lower_line2.SetLineWidth(2)
        lower_line2.Draw("same")

        text.DrawLatex(0.003, 0.75, "SR")
        text.DrawLatex(0.03, 0.75, "CR")

    canvas.SaveAs(pdffile + "_" + label + "_lines.pdf")


def plot1D(variable, cutstring, histos, lumi, pdffile, ymin=1e-1, ymax=1e5, showdata = False):

    contains_data = False
    for label in histos.keys():
        if not "Data" in label:
            histos[label].Scale(lumi)
        else:
            contains_data = True
    
    for label in histos:
        histos[label].SetLineWidth(2)
        shared_utils.histoStyler(histos[label])

    histolist = [histos[histos.keys()[0]]]
    for label in histos:
        if not "Data" in label and not "Signal" in label:
            histolist.append(histos[label])

    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)

    canvas = shared_utils.mkcanvas()
    canvas.SetFillStyle(4000)    
      
    lumi = float("%.2f" % (lumi/1e3))

    if contains_data and showdata:
        hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histolist[0], histolist[1:], lumi = lumi, datamc = 'Data')
    else:
        print "No data"
        hratio, pad1, pad2 = shared_utils.FabDraw(canvas, legend, histolist[-1], histolist, lumi = lumi, datamc = 'Data')
        histolist[-1].SetTitle("")

    for i_label, label in enumerate(histos):
        histos[label].GetYaxis().SetRangeUser(ymin, ymax)

    for label in histos:
        if "Signal" in label:
            histos[label].Draw("same")
            legend.AddEntry(histos[label], histos[label].GetTitle())
       
    hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
    hratio.GetYaxis().SetTitle('Data/MC')

    xlabel = variable
    xlabel = xlabel.replace("leptons_mt", "m_{T}^{lepton} (GeV)")
    xlabel = xlabel.replace("leadinglepton_mt", "m_{T}^{lepton} (GeV)")
    xlabel = xlabel.replace("dilepton_invmass", "m_{ll} (GeV)")
    hratio.GetXaxis().SetTitle(xlabel)

    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)

    if "/" in pdffile:
        os.system("mkdir -p %s" % "/".join(pdffile.split("/")[:-1]))
    canvas.SaveAs(pdffile + ".pdf")
    

def do_plots(variables, cutstring, thisbatchname, folder, labels, ymin = 1e-5, ymax = 1e10, showdata = False):

    with open(folder + "/luminosity.py") as fin:
        lumis = eval(fin.read())

    lumi = 0

    for variable in variables:
        histos = collections.OrderedDict()
        for label in labels:

            globstrings = labels[label][0]
            color = labels[label][1]

            if not showdata and "Data" in label:
                continue

            histos[label] = 0

            for globstring in globstrings:
                input_files = glob.glob(folder + "/" + globstring + "*.root")
                if len(input_files) == 0: continue
                print label, ":\n", ",".join(input_files), "\n"
                if not ":" in variable:
                    currenthisto = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cutstring, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2])
                else:
                    currenthisto = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cutstring, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2], nBinsY=binnings[variable][3], ymin=binnings[variable][4], ymax=binnings[variable][5])

                if "Data" in label:
                    lumi += lumis[globstring.replace("*", "_")] * 1e3

                if histos[label] == 0:
                    histos[label] = currenthisto.Clone()
                    histos[label].SetDirectory(0)
                else:
                    histos[label].Add(currenthisto.Clone())

            histos[label].SetTitle(label)
            if "Data" in label:
                histos[label].SetLineColor(color)
            else:
                histos[label].SetFillColor(color)
                histos[label].SetLineColor(color)
                histos[label].SetMarkerColor(color)

        if lumi == 0:
            lumi = 37000

        if not ":" in variable:
            plot1D(variable, cutstring, histos, lumi, "%s_%s" % (thisbatchname, variable), ymin, ymax, showdata = showdata)
        else:
            plot2D(variable, cutstring, histos, lumi, "%s_%s" % (thisbatchname, variable), ymin, ymax, showdata = showdata)



if __name__ == "__main__":

    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/tools/skim_05"
    
    labels = collections.OrderedDict()

    labels["Data"] = [[
            "Run2016*MET"
                ], kBlack]
    labels["WJetsToLNu"] = [[
            "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1",
            "Summer16.WJetsToLNu_TuneCUETP8M1",
                ], 85]
    labels["DYJetsToLL"] = [[
            "Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1",
                ], 67]
    labels["QCD"] = [[
            "Summer16.QCD_HT200to300_TuneCUETP8M1",
            "Summer16.QCD_HT300to500_TuneCUETP8M1",
            "Summer16.QCD_HT500to700_TuneCUETP8M1",
            "Summer16.QCD_HT700to1000_TuneCUETP8M1",
            "Summer16.QCD_HT1000to1500_TuneCUETP8M1",
            "Summer16.QCD_HT1500to2000_TuneCUETP8M1",
            "Summer16.QCD_HT2000toInf_TuneCUETP8M1",
                ], 97]
    labels["TTJets"] = [[
            "Summer16.TT_TuneCUETP8M2T4",
                ], 8]
    labels["Diboson"] = [[
                "Summer16.ZZ_TuneCUETP8M1",
                "Summer16.WW_TuneCUETP8M1",
                "Summer16.WZ_TuneCUETP8M1",
                ], 62]
    labels["ZJets"] = [[
                "Summer16.ZJetsToNuNu_HT-100To200_13TeV",
                "Summer16.ZJetsToNuNu_HT-200To400_13TeV",
                "Summer16.ZJetsToNuNu_HT-400To600_13TeV",
                "Summer16.ZJetsToNuNu_HT-600To800_13TeV",
                "Summer16.ZJetsToNuNu_HT-800To1200_13TeV",
                "Summer16.ZJetsToNuNu_HT-1200To2500_13TeV",
                "Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV",
                ], 8]
    labels["Signal"] = [[
                "Summer16.g1800_chi1400_27_200970_step4_10AODSIM",
                "Summer16.g1800_chi1400_27_200970_step4_30AODSIM",
                "Summer16.g1800_chi1400_27_200970_step4_50AODSIM",
                "Summer16.g1800_chi1400_27_200970_step4_100AODSIM",
                ], kBlue]

    event_selections = {
                "Baseline":               "(n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0",
                "BaselineNoLeptons":      "n_goodleptons==0",
                "BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110 && leadinglepton_mt>90",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leadinglepton_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<70",
                      }

    dEdxSidebandLow = 1.6
    dEdxLow = 2.1
    dEdxMid = 4.0

    has_DT = "(n_tracks_SR_short+n_tracks_SR_long)>0 && "
    has_DT_MidDeDx = has_DT + "tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s && " % (dEdxLow, dEdxMid)
    has_DT_HighDeDx = has_DT + "tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s && " % (dEdxMid, 9999)

    if True:

        ## cand tracks:
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==1", "bdtsideband/cand_bdtsideband_short", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==0", "bdtsideband/cand_bdtsideband_long", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==1", "bdtsideband/cand_bdtsideband_short_genfake", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==0 && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==1", "bdtsideband/cand_bdtsideband_long_genfake", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==0", "bdtsideband/cand_bdtsideband_short_genprompt", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==0 && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==0", "bdtsideband/cand_bdtsideband_long_genprompt", folder, labels)
        #
        ## with added dxy-BDT cut to define cut function:
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_tight>0.1 && tracks_is_pixel_track==1", "bdtsideband/dxybdt_bdtsideband_short", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_bdt>0.25 && tracks_is_pixel_track==0", "bdtsideband/dxybdt_bdtsideband_long", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_tight>0.1 && tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==1", "bdtsideband/dxybdt_bdtsideband_short_genfake", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_bdt>0.25 && tracks_is_pixel_track==0 && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==1", "bdtsideband/dxybdt_bdtsideband_long_genfake", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_tight>0.1 && tracks_is_pixel_track==1 && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==0", "bdtsideband/dxybdt_bdtsideband_short_genprompt", folder, labels)
        #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_bdt>0.25 && tracks_is_pixel_track==0 && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==0", "bdtsideband/dxybdt_bdtsideband_long_genprompt", folder, labels)

        # SR and CR tracks:
        labels = {"Signal": labels["Signal"]}
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && (tracks_SR_short>0 || tracks_CR_short>0)", "bdtsideband/bdtsideband_short", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && (tracks_SR_long>0 || tracks_CR_long>0)", "bdtsideband/bdtsideband_long", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==1 && (tracks_SR_short>0 || tracks_CR_short>0)", "bdtsideband/bdtsideband_short_genfake", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==1 && (tracks_SR_long>0 || tracks_CR_long>0)", "bdtsideband/bdtsideband_long_genfake", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==0 && (tracks_SR_short>0 || tracks_CR_short>0)", "bdtsideband/bdtsideband_short_genprompt", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_chiCandGenMatchingDR>0.01 && tracks_fake==0 && (tracks_SR_long>0 || tracks_CR_long>0)", "bdtsideband/bdtsideband_long_genprompt", folder, labels)

        
    if False:
        # leading lepton mT
        binnings["tracks_pt"] = [25, 0, 1000]
        binnings["tracks_nMissingOuterHits"] = [10, 0, 10]
        do_plots(["tracks_nMissingOuterHits"], has_DT + event_selections["Baseline"], "mcstudy/mcBaselineDT", folder, labels)
        do_plots(["tracks_nMissingOuterHits"], event_selections["Baseline"], "mcstudy/Baseline", folder, labels)

    if False:
        # leading lepton mT
        binnings["leadinglepton_mt"] = [25, 0, 1000]
        do_plots(["leadinglepton_mt"], has_DT + event_selections["HT>0"], "mcstudy", folder, labels)

    if False:
        # MC validation region
        labels["Data"] = [["Run2016G*SingleElectron", "Run2016H*SingleElectron"], kBlack]
        do_plots(["leadinglepton_mt"], has_DT + event_selections["SElValidationMT"], "SElValidationMT", folder, labels, showdata = True)
        do_plots(["tracks_invmass"], has_DT + event_selections["SElValidationZLL"], "SElValidationZLL", folder, labels, showdata = True)

        labels["Data"] = [["Run2016G*SingleMuon", "Run2016H*SingleMuon"], kBlack]
        do_plots(["leptons_mt"], has_DT + event_selections["SMuValidationMT"], "SMuValidationMT", folder, labels)
        do_plots(["tracks_invmass"], has_DT + event_selections["SMuValidationZLL"], "SMuValidationZLL", folder, labels)

    if False:
        # z peak:
        labels["Data"] = [["Run2016G*SingleElectron", "Run2016H*SingleElectron"], kBlack]
        do_plots(["dilepton_invmass"], "dilepton_invmass>0", "zpeak_electron", folder, labels, ymin = 1e-2, ymax = 1e8, showdata = True)

        labels["Data"] = [["Run2016G*SingleMuon", "Run2016H*SingleMuon"], kBlack]
        do_plots(["dilepton_invmass"], "dilepton_invmass>0", "zpeak_muon", folder, labels, ymin = 1e-1, ymax = 1e8, showdata = True)

