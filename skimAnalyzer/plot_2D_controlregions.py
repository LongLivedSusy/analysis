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

        variable = variable.replace("tracks_mva_loose_may20_chi2", "MVA score")
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
        
        if "CombinedBg" in label or "Signal" in label:
            
            histos[label].Draw(drawoption)
            shared_utils.stamp()
            
            text = TLatex()
            text.SetTextFont(132)
            text.SetTextSize(0.059)
            
            if "short" in pdffile:
                upper_line = TLine(0, -0.5, (0.8 + 0.5)/(0.65/0.01), 0.8)
                upper_line.SetLineWidth(2)
                upper_line.Draw("same")
                lower_line = TLine(0.02, -1, 0.02, 1)
                lower_line.SetLineWidth(2)
                lower_line.Draw("same")
            
                text.DrawLatex(0.005, 0.75, "SR")
                text.DrawLatex(0.03, 0.75, "CR")
            
            if "long" in pdffile:
                upper_line = TLine(0, -0.05, (1 + 0.05)/(0.7/0.01), 1)
                upper_line.SetLineWidth(2)
                upper_line.Draw("same")
                lower_line = TLine(0.02, -1, 0.02, 1)
                lower_line.SetLineWidth(2)
                lower_line.Draw("same")
            
                text.DrawLatex(0.003, 0.75, "SR")
                text.DrawLatex(0.03, 0.75, "CR")
            
            canvas.SaveAs(pdffile + "_" + label.replace(":", "_").replace(" ", "_") + ".pdf")


def plot1D(variable, cutstring, histos, lumi, pdffile, xlabel = False, ymin=1e-1, ymax=1e5, showdata = True):

    contains_data = False
    for label in histos.keys():
        if not "Data" in label:
            histos[label].Scale(lumi)
            print "scaling with", lumi
        else:
            contains_data = True
        if "Signal" in label:
            histos[label].SetLineWidth(2)

    
    if contains_data:
        histolist = [histos[histos.keys()[0]]]
    else:
        histolist = []
        
    histolistbg = []
    for label in histos:
        if not "Data" in label and not "Signal" in label:
            histolistbg.append(histos[label])
    histolistbg = sorted(histolistbg, key=lambda item: item.Integral())
    histolist += histolistbg
    
    legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)

    canvas = shared_utils.mkcanvas()
    canvas.SetFillStyle(4000)    
      
    lumi = float("%.2f" % (lumi/1e3))

    if contains_data and showdata:
        hratio, pads = shared_utils.FabDraw(canvas, legend, histolist[0], histolist[1:], lumi = lumi, datamc = 'Data')
    else:
        print "No data"
        
        example = histos[histos.keys()[0]].Clone()
        print "example.GetXaxis().GetNbins()", example.GetXaxis().GetNbins()
        print "example.GetXaxis().GetBinLowEdge(0)", example.GetXaxis().GetBinLowEdge(1)
        print "example.GetXaxis().GetBinLowEdge(example.GetXaxis().GetNbins()+1)", example.GetXaxis().GetBinLowEdge(example.GetXaxis().GetNbins()+1)
        
        empty_histo = TH1D("Data", "Data", example.GetXaxis().GetNbins(), example.GetXaxis().GetBinLowEdge(1), example.GetXaxis().GetBinLowEdge(example.GetXaxis().GetNbins()+1))
        shared_utils.histoStyler(empty_histo)
        
        print canvas, legend, empty_histo, histolist, lumi
        
        hratio, pads = shared_utils.FabDraw(canvas, legend, empty_histo, histolist, lumi = lumi, datamc = 'MC')
        histolist[-1].SetTitle("")

    for i_label, label in enumerate(histos):
        histos[label].GetYaxis().SetRangeUser(ymin, ymax)

    for label in histos:
        if "Signal" in label:
            histos[label].Draw("same")
            legend.AddEntry(histos[label], histos[label].GetTitle())
       
    hratio.GetYaxis().SetRangeUser(-0.1,2.6)    
    hratio.GetYaxis().SetTitle('Data/MC')

    if xlabel == False:
        xlabel = variable
    hratio.GetXaxis().SetTitle(str(xlabel))

    for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
        if hratio.GetBinContent(ibin)==0:
            hratio.SetBinContent(ibin,-999)
    hratio.SetMarkerColor(kBlack)

    if "/" in pdffile:
        os.system("mkdir -p %s" % "/".join(pdffile.split("/")[:-1]))
    canvas.SaveAs(pdffile + ".pdf")
    

def do_plots(variable, cutstring, thisbatchname, folder, labels, binnings, returnhistos = False, signalcut = False, ymin = 1e2, ymax = 1e12, showdata = True):

    #with open(folder + "/luminosity.py") as fin:
    #    lumis = eval(fin.read())

    lumi = 0

    histos = collections.OrderedDict()
    for label in labels:
                    
        if "Signal" in label:
            scaling = 1000
            if signalcut:
                cutstring += " && " + signalcut
        else:
            scaling = 1

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
                currenthisto = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cutstring, scaling=scaling, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2])
            else:
                currenthisto = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cutstring, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2], nBinsY=binnings[variable][3], ymin=binnings[variable][4], ymax=binnings[variable][5])

                overflow_top = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cutstring, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2], nBinsY=1, ymin=binnings[variable][5], ymax=9999)
                overflow_right = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cutstring, nBinsX=1, xmin=binnings[variable][2], xmax=9999, nBinsY=binnings[variable][3], ymin=binnings[variable][4], ymax=binnings[variable][5])

                # upper Y overflow:
                for ibinx in range(1, currenthisto.GetXaxis().GetNbins()):
                    value = currenthisto.GetBinContent(ibinx, currenthisto.GetYaxis().GetNbins())
                    overflow = overflow_top.GetBinContent(ibinx, 1)
                    currenthisto.SetBinContent(ibinx, currenthisto.GetYaxis().GetNbins(), value + overflow)

                # right X overflow:
                for ibiny in range(1, currenthisto.GetYaxis().GetNbins()):
                    value = currenthisto.GetBinContent(currenthisto.GetXaxis().GetNbins(), ibiny)
                    overflow = overflow_right.GetBinContent(1, ibiny)
                    currenthisto.SetBinContent(currenthisto.GetXaxis().GetNbins(), ibiny, value + overflow)

            currenthisto.SetLineWidth(2)
            shared_utils.histoStyler(currenthisto)

            #if "Data" in label:
            #    lumi += lumis[globstring.replace("*", "_")] * 1e3

            if histos[label] == 0:
                histos[label] = currenthisto.Clone()
                histos[label].SetDirectory(0)
            else:
                histos[label].Add(currenthisto.Clone())

        histos[label].SetTitle(label)
        if "Data" in label or "Signal" in label:
            print "setting color", label, color
            histos[label].SetLineColor(color)
        else:
            histos[label].SetFillColor(color)
            histos[label].SetLineColor(color)
            #histos[label].SetMarkerColor(color)

    if returnhistos:
        return histos

    if lumi == 0:
        lumi = 36000

    if not ":" in variable:
        print "binnings[variable][3]", binnings[variable][3]
        plot1D(variable, cutstring, histos, lumi, "%s_%s" % (thisbatchname, variable), xlabel = binnings[variable][3], ymin = ymin, ymax = ymax, showdata = showdata)
    else:
        plot2D(variable, cutstring, histos, lumi, "%s_%s" % (thisbatchname, variable), ymin = ymin, ymax = ymax, showdata = showdata)


if __name__ == "__main__":
    
    labels_sg = collections.OrderedDict()
    labels_bg = collections.OrderedDict()
    labels_data = collections.OrderedDict()

    binnings = {}
    binnings["MHT"] = [20, 0, 1000, "missing H_T (GeV)"]
    binnings["tracks_invmass"] = [10, 0, 200, "m_{DT, track} (GeV)"]
    binnings["regionCorrected"] = [54, 1, 55, "search bin"]
    binnings["dilepton_invmass"] = [50, 40, 140, "m_{l, l} (GeV)"]
    binnings["leptons_mt"] = [16, 0, 160, "m_{T} (GeV)"]
    binnings["tracks_mva_loose"] = [20, -1, 1, "BDT score"]
    binnings["tracks_mva_loose_may20_chi2"] = binnings["tracks_mva_loose"]
    binnings["tracks_mva_tight_may20_chi2"] = binnings["tracks_mva_loose"]
    binnings["tracks_dxyVtx"] = [10, 0, 0.1, "d_{xy} (cm)"]
    binnings["tracks_matchedCaloEnergy"] = [20, 0, 50, "E_{dep} (GeV)"]
    binnings["leadinglepton_mt"] = [16, 0, 160, "m_{T} (GeV)"]
    binnings["tracks_mva_tight:tracks_dxyVtx"] = [40, 0, 0.04, 20, 0.1, 1.0]
    binnings["tracks_mva_loose:tracks_dxyVtx"] = [50, 0, 0.05, 40, -1.0, 1.0]
    binnings["tracks_mva_tight_may20_chi2:tracks_dxyVtx"] = [40, 0, 0.04, 20, 0.1, 1.0]
    binnings["tracks_mva_loose_may20_chi2:tracks_dxyVtx"] = [50, 0, 0.05, 40, -1.0, 1.0]
    binnings["tracks_deDxHarmonic2pixelCorrected"] = [20, 0, 10]
    binnings["tracks_dzVtx"] = [50, 0, 0.05, "d_{z} (cm)"]
    binnings["tracks_trkRelIso"] = [20, 0, 0.02, "relative track isolation"]
    binnings["tracks_ptErrOverPt2"] = [20, 0, 0.1, "#Delta p_{T} / p_{T}^{2} (1/GeV)"]
    binnings["tracks_trkMiniRelIso"] = [50, 0, 0.2, "track miniIsolation"]
    binnings["tracks_nMissingInnerHits"] = [20, 0, 20, "missing inner hits"]
    binnings["tracks_nMissingMiddleHits"] = [20, 0, 20, "missing middle hits"]
    binnings["tracks_nMissingOuterHits"] = [20, 0, 20, "missing outer hits"]
    binnings["tracks_nValidPixelHits"] = [10, 0, 10, "pixel hits"]
    binnings["tracks_nValidTrackerHits"] = [20, 0, 20, "tracker hits"]
    binnings["tracks_mva_tight"] = [20, -1.0, 1.0, "d_{xy}-informed BDT score"]
    binnings["tracks_mva_loose"] = [20, -1.0, 1.0, "BDT score"]
    binnings["tracks_chi2perNdof"] = [20, 0, 5.0, "track #chi^{2}/ndof"]
    binnings["tracks_fake"] = [2, 0, 2, "isfake"]
    
    labels_data["Data"] = [[
            "Run2016*MET"
                ], kBlack]
    labels_data["Data"] = [[
            "Run2016*SingleMuon"
                ], kBlack]
    labels_bg["WJetsToLNu"] = [[
            "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1",
            "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1",
            "Summer16.WJetsToLNu_TuneCUETP8M1",
                ], 85]
    labels_bg["DYJetsToLL"] = [[
            "Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1",
            "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1",
                ], 67]
    labels_bg["QCD"] = [[
            "Summer16.QCD_HT200to300_TuneCUETP8M1",
            "Summer16.QCD_HT300to500_TuneCUETP8M1",
            "Summer16.QCD_HT500to700_TuneCUETP8M1",
            "Summer16.QCD_HT700to1000_TuneCUETP8M1",
            "Summer16.QCD_HT1000to1500_TuneCUETP8M1",
            "Summer16.QCD_HT1500to2000_TuneCUETP8M1",
            "Summer16.QCD_HT2000toInf_TuneCUETP8M1",
                ], 97]
    labels_bg["TTJets"] = [[
            "Summer16.TTJets_DiLept",
            "Summer16.TTJets_SingleLeptFromT",
            "Summer16.TTJets_SingleLeptFromTbar",
                ], 8]
    labels_bg["Diboson"] = [[
                "Summer16.ZZ_TuneCUETP8M1",
                "Summer16.WW_TuneCUETP8M1",
                "Summer16.WZ_TuneCUETP8M1",
                ], 62]
    labels_bg["ZJets"] = [[
                "Summer16.ZJetsToNuNu_HT-100To200_13TeV",
                "Summer16.ZJetsToNuNu_HT-200To400_13TeV",
                "Summer16.ZJetsToNuNu_HT-400To600_13TeV",
                "Summer16.ZJetsToNuNu_HT-600To800_13TeV",
                "Summer16.ZJetsToNuNu_HT-800To1200_13TeV",
                "Summer16.ZJetsToNuNu_HT-1200To2500_13TeV",
                "Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV",
                ], kOrange]
    labels_sg["Signal"] = [[
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
                "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
            ], kBlue]
            
    event_selections = {
                "Baseline":               "(n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0",
                "BaselineNoLeptons":      "n_goodleptons==0",
                "BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110 && leadinglepton_mt>90",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && n_goodleptons==0",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leadinglepton_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<70",
                "PromptDY":               "dilepton_leptontype==11 && dilepton_invmass>65 && dilepton_invmass<110",
                      }

    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_26_baseline"
    
    # with the SR and CR definitions:
    tags = {
            "SR_short": " && tracks_is_pixel_track==1 && tracks_mva_loose_may20_chi2>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01",
            "SR_long":  " && tracks_is_pixel_track==0 && tracks_mva_loose_may20_chi2>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01",
            "CR_short": " && tracks_is_pixel_track==1 && tracks_dxyVtx>0.02",
            "CR_long":  " && tracks_is_pixel_track==0 && tracks_dxyVtx>0.02",
           }
    
    mylabels = dict(labels_bg, **labels_sg)
    for variable in ["tracks_fake", "tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_nMissingOuterHits", "tracks_ptErrOverPt2"]:
        for tag in tags:
            do_plots(variable, event_selections["Baseline"] + " && tracks_deDxHarmonic2pixelCorrected>2.0" + tags[tag], "controlplots/" + tag, folder, mylabels, binnings)
    
    quit()
    
    # BDT score:
    mylabels = dict(labels_bg, **labels_sg)
    for variable in ["tracks_mva_tight_may20_chi2", "tracks_mva_loose_may20_chi2"]:
        do_plots(variable, event_selections["Baseline"] + " && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_is_pixel_track==1", "controlplots/baseline_short", folder, mylabels, binnings)
        do_plots(variable, event_selections["Baseline"] + " && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_is_pixel_track==0", "controlplots/baseline_long", folder, mylabels, binnings)
    
    # 2D plots for fake background:
    do_plots("tracks_mva_loose_may20_chi2:tracks_dxyVtx", event_selections["Baseline"] + " && tracks_fake==1 && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_is_pixel_track==1", "controlplots/bgfake_short_uninformed", folder, labels_bg, binnings)
    do_plots("tracks_mva_loose_may20_chi2:tracks_dxyVtx", event_selections["Baseline"] + " && tracks_fake==1 && tracks_nMissingOuterHits>=2 && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_is_pixel_track==0", "controlplots/bgfake_long_uninformed", folder, labels_bg, binnings)
    do_plots("tracks_mva_loose_may20_chi2:tracks_dxyVtx", event_selections["Baseline"] + " && tracks_fake==1 && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_mva_tight_may20_chi2>0.15 && tracks_is_pixel_track==1", "controlplots/bgfake_short_informed", folder, labels_bg, binnings)
    do_plots("tracks_mva_loose_may20_chi2:tracks_dxyVtx", event_selections["Baseline"] + " && tracks_fake==1 && tracks_nMissingOuterHits>=2 && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_mva_tight_may20_chi2>0.15 && tracks_is_pixel_track==0", "controlplots/bgfake_long_informed", folder, labels_bg, binnings)
        
    # 2D plots for signal    
    do_plots("tracks_mva_loose_may20_chi2:tracks_dxyVtx", event_selections["Baseline"] + " && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_is_pixel_track==1", "controlplots/sg_short_uninformed", folder, labels_sg, binnings)
    do_plots("tracks_mva_loose_may20_chi2:tracks_dxyVtx", event_selections["Baseline"] + " && tracks_nMissingOuterHits>=2 && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_is_pixel_track==0", "controlplots/sg_long_uninformed", folder, labels_sg, binnings)
    do_plots("tracks_mva_loose_may20_chi2:tracks_dxyVtx", event_selections["Baseline"] + " && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_mva_tight_may20_chi2>0.15 && tracks_is_pixel_track==1", "controlplots/sg_short_informed", folder, labels_sg, binnings)
    do_plots("tracks_mva_loose_may20_chi2:tracks_dxyVtx", event_selections["Baseline"] + " && tracks_nMissingOuterHits>=2 && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_mva_tight_may20_chi2>0.15 && tracks_is_pixel_track==0", "controlplots/sg_long_informed", folder, labels_sg, binnings)


          
    

