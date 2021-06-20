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

    #if "/" in pdffile:
    #    os.system("mkdir -p %s" % "/".join(pdffile.split("/")[:-1]))
    #    os.chdir("/".join(pdffile.split("/")[:-1]))

    for label in histos:
        
        if "CombinedBg" in label or "Signal" in label:
            
            histos[label].Draw(drawoption)
            shared_utils.stamp()
            canvas.SaveAs(pdffile + "_" + label.replace(":", "_").replace(" ", "_") + ".pdf")
            
            # draw some funky lcines
            text = TLatex()
            text.SetTextFont(132)
            text.SetTextSize(0.059)
            
            if "short" in pdffile:
                #upper_line = TLine(0, -0.5, (1 + 0.5)/(0.65/0.01), 1)
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
            
            canvas.SaveAs(pdffile + "_" + label.replace(":", "_").replace(" ", "_") + "_lines.pdf")


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
    

def do_plots(variable, cutstring, thisbatchname, folder, labels, binnings, returnhistos = False, scaling = 1.0, signalcut = False, ymin = 1e2, ymax = 1e12, showdata = True):

    #with open(folder + "/luminosity.py") as fin:
    #    lumis = eval(fin.read())

    lumi = 0

    histos = collections.OrderedDict()
    for label in labels:
                    
        #if "Signal" in label:
        #    scaling = 1000.0
        #    if signalcut:
        #        cutstring += " && " + signalcut

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
            #histos[label].SetLineColor(color)
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
    
    labels = collections.OrderedDict()

    binnings = {}
    binnings["MHT"] = [20, 0, 1000, "missing H_T (GeV)"]
    #binnings["tracks_invmass"] = [50, 40, 140, "m_{DT, track} (GeV)"]
    binnings["tracks_invmass"] = [10, 0, 200, "m_{DT, track} (GeV)"]
    binnings["regionCorrected"] = [54, 1, 55, "search bin"]
    binnings["dilepton_invmass"] = [50, 40, 140, "m_{l, l} (GeV)"]
    binnings["leptons_mt"] = [16, 0, 160, "m_{T} (GeV)"]
    binnings["tracks_mva_loose"] = [20, -1, 1, "BDT score"]
    #binnings["tracks_dxyVtx"] = [50, 0, 0.05, "d_{xy} (cm)"]
    binnings["tracks_dxyVtx"] = [10, 0, 0.1, "d_{xy} (cm)"]
    binnings["tracks_matchedCaloEnergy"] = [20, 0, 50, "E_{dep} (GeV)"]
    binnings["leadinglepton_mt"] = [16, 0, 160, "m_{T} (GeV)"]
    binnings["tracks_mva_tight:tracks_dxyVtx"] = [40, 0, 0.04, 20, 0.1, 1.0]
    binnings["tracks_mva_loose:tracks_dxyVtx"] = [50, 0, 0.05, 40, -1.0, 1.0]
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
    
    
    
    ##labels["Data"] = [[
    ##        "Run2016*MET"
    ##            ], kBlack]
    #labels["Data"] = [[
    #        "Run2016*SingleMuon"
    #            ], kBlack]
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
    #        #"Summer16.TT_TuneCUETP8M2T4",
            "Summer16.TTJets_DiLept",
            "Summer16.TTJets_SingleLeptFromT",
            "Summer16.TTJets_SingleLeptFromTbar",
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
                ], kOrange]
    ##labels["Signal x1e3"] = [[
    ##            "Summer16.g1800_chi1400_27_200970_step4_10AODSIM",
    ##            "Summer16.g1800_chi1400_27_200970_step4_30AODSIM",
    ##            "Summer16.g1800_chi1400_27_200970_step4_50AODSIM",
    ##            "Summer16.g1800_chi1400_27_200970_step4_100AODSIM",
    ##            ], kMagenta]
    #labels["Signal (#chi_{1}^{#pm}-matched, x1e3)"] = [[
    #            #"RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
    #            "RunIISummer16MiniAODv3.SMS-T2bt",
    #            "RunIISummer16MiniAODv3.SMS-T1qqqq",
    #            ], kViolet+1]
        
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

    dEdxSidebandLow = 1.6
    dEdxLow = 2.0
    dEdxMid = 4.0

    has_DT = "(tracks_SR_short+tracks_SR_long)>0 && "
    has_DT_MidDeDx = has_DT + "tracks_deDxHarmonic2pixelCorrected>%s && tracks_deDxHarmonic2pixelCorrected<%s && " % (dEdxLow, dEdxMid)
    has_DT_HighDeDx = has_DT + "tracks_deDxHarmonic2pixelCorrected>%s && tracks_deDxHarmonic2pixelCorrected<%s && " % (dEdxMid, 9999)

    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_50_run2_merged"


    if True:
        
        for analysis in ["HadBaseline", "SMuBaseline", "SElBaseline"]:

            bg_ev_sr_fake = 0
            bg_ev_cr_fake = 0
            sg_ev_sr_fake = 0
            sg_ev_cr_fake = 0
            bg_ev_sr_prompt = 0
            bg_ev_cr_prompt = 0
            sg_ev_sr_prompt = 0
            sg_ev_cr_prompt = 0
            
            short_bg_ev_cr_fake=0
            short_bg_ev_cr_prompt=0
            long_bg_ev_cr_fake=0
            long_bg_ev_cr_prompt=0
        
            histos = do_plots("tracks_fake", event_selections[analysis] + " && tracks_is_pixel_track==1 && tracks_dxyVtx>0.02 && tracks_deDxHarmonic2pixelCorrected>2.0", "contam/HadBaseline", folder, labels, binnings, returnhistos = True)
            
            for label in histos:
                histos[label].Scale(36000)
                
                if "Signal" not in label and "Data" not in label:
                    #bg_ev_sr_fake += histos[label].GetBinContent(2)
                    short_bg_ev_cr_fake += histos[label].GetBinContent(2)
                    #bg_ev_sr_prompt += histos[label].Integral(0, histos[label].GetXaxis().FindBin(0.02)) 
                    short_bg_ev_cr_prompt += histos[label].GetBinContent(1)
            
            histos = do_plots("tracks_fake", event_selections[analysis] + " && tracks_is_pixel_track==0 && tracks_dxyVtx>0.04 && tracks_deDxHarmonic2pixelCorrected>2.0", "contam/HadBaseline", folder, labels, binnings, returnhistos = True)
            
            for label in histos:
                histos[label].Scale(36000)
                
                if "Signal" not in label and "Data" not in label:
                    long_bg_ev_cr_fake += histos[label].GetBinContent(2)
                    long_bg_ev_cr_prompt += histos[label].GetBinContent(1)
            
        
            #histos = do_plots("tracks_dxyVtx", event_selections[analysis] + " && tracks_SR_short>=1 && tracks_SR_long==0 && tracks_matchedCaloEnergy<10 && tracks_trkRelIso<0.01 && tracks_fake==1 && tracks_deDxHarmonic2pixelCorrected>2.0", "contam/HadBaseline", folder, labels, binnings, returnhistos = True)
            #
            #for label in histos:
            #    histos[label].Scale(36000)
            #    
            #    if "Signal" not in label and "Data" not in label:
            #        bg_ev_sr_fake += histos[label].Integral(0, histos[label].GetXaxis().FindBin(0.02)) 
            #        bg_ev_cr_fake += histos[label].Integral(histos[label].GetXaxis().FindBin(0.02), 9999) 
            #    elif "Signal" in label:
            #        sg_ev_sr_fake += histos[label].Integral(0, histos[label].GetXaxis().FindBin(0.02)) 
            #        sg_ev_cr_fake += histos[label].Integral(histos[label].GetXaxis().FindBin(0.02), 9999) 
            #
            #histos = do_plots("tracks_dxyVtx", event_selections[analysis] + " && tracks_SR_long>=1 && tracks_SR_short==0 && tracks_matchedCaloEnergy<10 && tracks_trkRelIso<0.01 && tracks_fake==1 && tracks_deDxHarmonic2pixelCorrected>2.0", "contam/HadBaseline", folder, labels, binnings, returnhistos = True)
            #
            #for label in histos:
            #    histos[label].Scale(36000)
            #    
            #    if "Signal" not in label and "Data" not in label:
            #        bg_ev_sr_fake += histos[label].Integral(0, histos[label].GetXaxis().FindBin(0.02)) 
            #        bg_ev_cr_fake += histos[label].Integral(histos[label].GetXaxis().FindBin(0.02), 9999) 
            #    elif "Signal" in label:
            #        sg_ev_sr_fake += histos[label].Integral(0, histos[label].GetXaxis().FindBin(0.02)) 
            #        sg_ev_cr_fake += histos[label].Integral(histos[label].GetXaxis().FindBin(0.02), 9999) 
            #
            #histos = do_plots("tracks_dxyVtx", event_selections[analysis] + " && tracks_SR_short>=1 && tracks_SR_long==0 && tracks_matchedCaloEnergy<10 && tracks_trkRelIso<0.01 && tracks_fake==0 && tracks_deDxHarmonic2pixelCorrected>2.0", "contam/HadBaseline", folder, labels, binnings, returnhistos = True)
            #
            #for label in histos:
            #    histos[label].Scale(36000)
            #    
            #    if "Signal" not in label and "Data" not in label:
            #        bg_ev_sr_prompt += histos[label].Integral(0, histos[label].GetXaxis().FindBin(0.02)) 
            #        bg_ev_cr_prompt += histos[label].Integral(histos[label].GetXaxis().FindBin(0.02), 9999) 
            #    elif "Signal" in label:
            #        sg_ev_sr_prompt += histos[label].Integral(0, histos[label].GetXaxis().FindBin(0.02)) 
            #        sg_ev_cr_prompt += histos[label].Integral(histos[label].GetXaxis().FindBin(0.02), 9999) 
            #
            #histos = do_plots("tracks_dxyVtx", event_selections[analysis] + " && tracks_SR_long>=1 && tracks_SR_short==0 && tracks_matchedCaloEnergy<10 && tracks_trkRelIso<0.01 && tracks_fake==0 && tracks_deDxHarmonic2pixelCorrected>2.0", "contam/HadBaseline", folder, labels, binnings, returnhistos = True)
            #
            #for label in histos:
            #    histos[label].Scale(36000)
            #    
            #    if "Signal" not in label and "Data" not in label:
            #        bg_ev_sr_prompt += histos[label].Integral(0, histos[label].GetXaxis().FindBin(0.02)) 
            #        bg_ev_cr_prompt += histos[label].Integral(histos[label].GetXaxis().FindBin(0.02), 9999) 
            #    elif "Signal" in label:
            #        sg_ev_sr_prompt += histos[label].Integral(0, histos[label].GetXaxis().FindBin(0.02)) 
            #        sg_ev_cr_prompt += histos[label].Integral(histos[label].GetXaxis().FindBin(0.02), 9999) 

            print "\n\n"
            print analysis
            print "short_bg_ev_cr_fake", short_bg_ev_cr_fake
            print "short_bg_ev_cr_prompt", short_bg_ev_cr_prompt
            print "long_bg_ev_cr_fake", long_bg_ev_cr_fake
            print "long_bg_ev_cr_prompt", long_bg_ev_cr_prompt
            raw_input("OK")


        quit()


    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_19_merged"


    if True:
        cats = {"short": " && tracks_is_pixel_track==1",
                "long": " && tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2"}
        
        baseline_selection = [
            "abs(tracks_eta)<2.4",   
            "!(abs(tracks_eta)>1.4442 && abs(tracks_eta)<1.566)",                              
            "tracks_highpurity==1",  
            "tracks_ptErrOverPt2<10",
            "tracks_dzVtx<0.1",      
            "tracks_trkRelIso<0.2",  
            "tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2",           
            "tracks_nMissingInnerHits==0",                                                     
            "tracks_nValidPixelHits>=3",    
            #"tracks_nMissingMiddleHits==0",
            #"tracks_chi2perNdof<2.88",
            #"tracks_pixelLayersWithMeasurement>=2",
            #"tracks_passmask==1",
            "tracks_pass_reco_lepton==1",
            "tracks_passPFCandVeto==1",                                   
            #"tracks_passpionveto==1",
            #"tracks_passjetveto==1",
                 ]
             
        for variable in ["tracks_nMissingInnerHits", "tracks_nMissingMiddleHits", "tracks_nMissingOuterHits", "tracks_dxyVtx", "tracks_dzVtx", "tracks_matchedCaloEnergy", "tracks_trkRelIso", "tracks_nValidPixelHits", "tracks_nValidTrackerHits", "tracks_ptErrOverPt2", "tracks_chi2perNdof"]: 
            for cat in cats: 
                #do_plots(variable, "HT>=0" + cats[cat], "trackvars/all_%s" % cat, folder, labels, binnings, signalcut = "tracks_chiCandGenMatchingDR<0.01")
                do_plots(variable, " && ".join(baseline_selection) + cats[cat], "trackvars2/baseline_%s" % cat, folder, labels, binnings, signalcut = "tracks_chiCandGenMatchingDR<0.01")
        quit()


    if True:
        #do_plots(["tracks_invmass"], "triggered_singlemuon==1 && n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<90 && tracks_SR_long>=1 && tracks_trkRelIso<0.01 && tracks_matchedCaloEnergy<10 && tracks_deDxHarmonic2pixelCorrected>2.0 && tracks_deDxHarmonic2pixelCorrected<9999", "test4", folder, labels, binnings)
        do_plots(["tracks_chi2perNdof"], "HT>0", "before_baseline", folder, labels, binnings)
        do_plots(["tracks_chi2perNdof"], "tracks_basecuts==1", "after_baselineAndVetos", folder, labels, binnings)
        quit()


    if False:
        
        tags = collections.OrderedDict()
        tags["SR_short"] = "tracks_mva_loose>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
        tags["SR_long"] = "tracks_mva_loose>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"
        tags["CR_short"] = "tracks_dxyVtx>0.02 && tracks_trkRelIso<0.01" 
        tags["CR_long"] = "tracks_dxyVtx>0.02 && tracks_trkRelIso<0.01"
        
        tags["SREC_short"] = "tracks_mva_looseNoDep>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
        tags["SREC_long"] = "tracks_mva_looseNoDep>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"
        
        do_plots(["tracks_invmass"], tags["SR_short"] + " && n_goodelectrons>0 && tracks_invmass>65 && tracks_invmass<110 && tracks_matchedCaloEnergy<10", "testshort", folder, labels)
        do_plots(["tracks_invmass"], tags["SR_long"] + " && n_goodelectrons>0 && tracks_invmass>65 && tracks_invmass<110 && tracks_matchedCaloEnergy<10", "testlong", folder, labels)
        do_plots(["tracks_invmass"], tags["SREC_short"] + " && n_goodelectrons>0 && tracks_invmass>65 && tracks_invmass<110 && tracks_matchedCaloEnergy<10", "testlowshort", folder, labels)
        do_plots(["tracks_invmass"], tags["SREC_long"] + " && n_goodelectrons>0 && tracks_invmass>65 && tracks_invmass<110 && tracks_matchedCaloEnergy<10", "testlowlong", folder, labels)
        do_plots(["tracks_invmass"], tags["SREC_short"] + " && n_goodelectrons>0 && tracks_invmass>65 && tracks_invmass<110 && tracks_matchedCaloEnergy>=10 && tracks_matchedCaloEnergy<15", "testhighshort", folder, labels)
        do_plots(["tracks_invmass"], tags["SREC_long"] + " && n_goodelectrons>0 && tracks_invmass>65 && tracks_invmass<110 && tracks_matchedCaloEnergy>=10 && tracks_matchedCaloEnergy<15", "testhighlong", folder, labels)
        quit()

    if True:
        # plot BDT variables:
        del labels["Data"]
        
        tags = collections.OrderedDict()
        #tags["SR_short"] = "tracks_mva_loose>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
        #tags["SR_long"] = "tracks_mva_loose>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"
        #tags["CR_short"] = "tracks_dxyVtx>0.02" 
        #tags["CR_long"] = "tracks_dxyVtx>0.02"
        tags["SR_short"] = "tracks_SR_short==1"
        tags["SR_long"] = "tracks_SR_long==1"
        tags["CR_short"] = "tracks_CR_short==1"
        tags["CR_long"] = "tracks_CR_long==1"
        
        for variable in ["tracks_mva_tight", "tracks_mva_loose", "tracks_trkRelIso", "tracks_ptErrOverPt2", "tracks_matchedCaloEnergy", "tracks_dxyVtx", "tracks_dzVtx", "tracks_nMissingOuterHits", "tracks_nValidPixelHits", "tracks_nValidTrackerHits"]:
            do_plots([variable], "tracks_is_pixel_track==1", "bdtvariables/short_candidates", folder, labels, ymin = 1e-1, ymax = 1e10)
            do_plots([variable], "tracks_is_pixel_track==1 && " + tags["SR_short"], "bdtvariables/short_diagonalcut", folder, labels, ymin = 1e-1, ymax = 1e10)
            do_plots([variable], "tracks_is_pixel_track==0", "bdtvariables/long_candidates", folder, labels, ymin = 1e-1, ymax = 1e10)
            do_plots([variable], "tracks_is_pixel_track==0 && " + tags["SR_long"], "bdtvariables/long_diagonalcut", folder, labels, ymin = 1e-1, ymax = 1e10)
        quit()



    if True:

        #del labels["Data"]

        labels = {"Signal": [[
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
                ], kBlue]}

        # cand tracks:
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_is_pixel_track==1", "bdtsideband_cand_short", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_is_pixel_track==0", "bdtsideband_cand_long", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_is_pixel_track==1 && tracks_fake==1", "bdtsideband_cand_short_genfake", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_is_pixel_track==0 && tracks_fake==1", "bdtsideband_cand_long_genfake", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_is_pixel_track==1 && tracks_fake==0", "bdtsideband_cand_short_genprompt", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_is_pixel_track==0 && tracks_fake==0", "bdtsideband_cand_long_genprompt", folder, labels)

        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_mva_tight>0.1 && tracks_is_pixel_track==1", "bdtsideband_dxybdt_short", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_mva_tight>0.25 && tracks_is_pixel_track==0", "bdtsideband_dxybdt_long", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_mva_tight>0.1 && tracks_is_pixel_track==1  && tracks_fake==1", "bdtsideband_dxybdt_short_genfake", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_mva_tight>0.25 && tracks_is_pixel_track==0  && tracks_fake==1", "bdtsideband_dxybdt_long_genfake", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_mva_tight>0.1 && tracks_is_pixel_track==1  && tracks_fake==0", "bdtsideband_dxybdt_short_genprompt", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_mva_tight>0.25 && tracks_is_pixel_track==0  && tracks_fake==0", "bdtsideband_dxybdt_long_genprompt", folder, labels)

        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && (tracks_SR_short>0 || tracks_CR_short>0)", "bdtsideband_final_short", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && (tracks_SR_long>0 || tracks_CR_long>0)", "bdtsideband_final_long", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + "  && tracks_fake==1 && (tracks_SR_short>0 || tracks_CR_short>0)", "bdtsideband_final_short_genfake", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + "  && tracks_fake==1 && (tracks_SR_long>0 || tracks_CR_long>0)", "bdtsideband_final_long_genfake", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + "  && tracks_fake==0 && (tracks_SR_short>0 || tracks_CR_short>0)", "bdtsideband_final_short_genprompt", folder, labels)
        do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + "  && tracks_fake==0 && (tracks_SR_long>0 || tracks_CR_long>0)", "bdtsideband_final_long_genprompt", folder, labels)
        
        quit()



    # plot regions:
    del labels["Data"]
    #for variable in ["tracks_trkRelIso", "tracks_dzVtx", "tracks_ptErrOverPt2", "tracks_trkMiniRelIso"]: #, "tracks_deDxHarmonic2pixelCorrected"]: #, "tracks_mva_loose", "tracks_matchedCaloEnergy", "tracks_dxyVtx"]:
    for variable in ["tracks_ptErrOverPt2"]:
        do_plots([variable], "(tracks_SR_short+tracks_SR_long)>0 && " + event_selections["Baseline"] + " && tracks_fake==1", "theregion/srbaseline_fake", folder, labels,     ymin = 1e-1, ymax = 1e10)
        do_plots([variable], "(tracks_SR_short+tracks_SR_long)>0 && " + event_selections["Baseline"] + " && tracks_fake==0" , "theregion/srbaseline_prompt", folder, labels,  ymin = 1e-1, ymax = 1e10)
        do_plots([variable], "(tracks_CR_short+tracks_CR_long)>0 && " + event_selections["Baseline"] + " && tracks_fake==1", "theregion/crbaseline_fake", folder, labels,     ymin = 1e-1, ymax = 1e10)
        do_plots([variable], "(tracks_CR_short+tracks_CR_long)>0 && " + event_selections["Baseline"] + " && tracks_fake==0" , "theregion/crbaseline_prompt", folder, labels,  ymin = 1e-1, ymax = 1e10)
    quit()


    # plot regions:
    del labels["Data"]
    do_plots(["regionCorrected"], has_DT + event_selections["Baseline"], "plots_09/baseline", folder, labels, ymin = 1e-4, ymax = 1e4)
    do_plots(["regionCorrected"], has_DT + event_selections["Baseline"] + " && tracks_fake==1" , "plots_09/baseline_fake", folder, labels, ymin = 1e-4, ymax = 1e4)
    do_plots(["regionCorrected"], has_DT + event_selections["Baseline"] + " && tracks_fake==0", "plots_09/baseline_prompt", folder, labels, ymin = 1e-4, ymax = 1e4)
    quit()

    # plot Z peak:
    labels["Data"] = [["Run2016G*SingleElectron", "Run2016H*SingleElectron"], kBlack]
    do_plots(["dilepton_invmass"], "dilepton_invmass>0 && dilepton_leptontype==11", "plots_09/zpeak_electron", folder, labels, ymin = 1e-2, ymax = 1e8, showdata = True)

    # plot some track variables:
    binnings["tracks_pt"] = [25, 0, 1000]
    binnings["tracks_nMissingOuterHits"] = [10, 0, 10]
    for variable in ["tracks_nMissingOuterHits", "tracks_pt"]:
        do_plots([variable], has_DT + event_selections["Baseline"], "plots_09/mcBaselineDT", folder, labels)


    # MC validation region
    labels["Data"] = [["Run2016G*SingleElectron", "Run2016H*SingleElectron"], kBlack]
    for dedx in ["", "_MidDeDx", "_HighDeDx"]: 
        do_plots(["leadinglepton_mt"], has_DT + event_selections["SElValidationMT"], "plots_09/SElValidationMT", folder, labels, showdata = True)
        do_plots(["leadinglepton_mt"], has_DT + event_selections["SElValidationMT"] + " && tracks_fake==1", "plots_09/SElValidationMT_fake", folder, labels)
        do_plots(["leadinglepton_mt"], has_DT + event_selections["SElValidationMT"] + " && tracks_fake==0", "plots_09/SElValidationMT_prompt", folder, labels)
        do_plots(["tracks_invmass"], has_DT + event_selections["SElValidationZLL"], "plots_09/SElValidationZLL", folder, labels, showdata = True)
        do_plots(["tracks_invmass"], has_DT + event_selections["SElValidationZLL"] + " && tracks_fake==1", "plots_09/SElValidationZLL_fake", folder, labels)
        do_plots(["tracks_invmass"], has_DT + event_selections["SElValidationZLL"] + " && tracks_fake==0", "plots_09/SElValidationZLL_prompt", folder, labels)

    labels["Data"] = [["Run2016G*SingleMuon", "Run2016H*SingleMuon"], kBlack]
    do_plots(["leptons_mt"], has_DT + event_selections["SMuValidationMT"], "plots_09/SMuValidationMT", folder, labels, showdata = True)
    do_plots(["tracks_invmass"], has_DT + event_selections["SMuValidationZLL"], "plots_09/SMuValidationZLL", folder, labels, showdata = True)



    #labels = {"Signal": [[
    #        #"Summer16.g1800_chi1400_27_200970_step4_10AODSIM",
    #        #"Summer16.g1800_chi1400_27_200970_step4_30AODSIM",
    #        #"Summer16.g1800_chi1400_27_200970_step4_50AODSIM",
    #        "Summer16.g1800_chi1400_27_200970_step4_100AODSIM",
    #        ], kBlue]}
        #
    ## cand tracks:
    #do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==1", "cand_bdtsideband_short_100", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==0", "cand_bdtsideband_long", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==1  && tracks_fake==1", "cand_bdtsideband_short_genfake", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==0  && tracks_fake==1", "cand_bdtsideband_long_genfake", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==1  && tracks_fake==0", "cand_bdtsideband_short_genprompt", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_is_pixel_track==0  && tracks_fake==0", "cand_bdtsideband_long_genprompt", folder, labels)
    #
    ## with added dxy-BDT cut to define cut function:
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_tight>0.1 && tracks_is_pixel_track==1", "dxybdt_bdtsideband_short", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_tight>0.25 && tracks_is_pixel_track==0", "dxybdt_bdtsideband_long", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_tight>0.1 && tracks_is_pixel_track==1  && tracks_fake==1", "dxybdt_bdtsideband_short_genfake", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_bdt>0.25 && tracks_is_pixel_track==0  && tracks_fake==1", "dxybdt_bdtsideband_long_genfake", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_tight>0.1 && tracks_is_pixel_track==1  && tracks_fake==0", "dxybdt_bdtsideband_short_genprompt", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && tracks_basecuts==1 && tracks_mva_bdt>0.25 && tracks_is_pixel_track==0  && tracks_fake==0", "dxybdt_bdtsideband_long_genprompt", folder, labels)
        #
    ## SR and CR tracks:
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && (tracks_SR_short>0 || tracks_CR_short>0)", "bdtsideband_short", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + " && (tracks_SR_long>0 || tracks_CR_long>0)", "bdtsideband_long", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + "  && tracks_fake==1 && (tracks_SR_short>0 || tracks_CR_short>0)", "bdtsideband_short_genfake", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + "  && tracks_fake==1 && (tracks_SR_long>0 || tracks_CR_long>0)", "bdtsideband_long_genfake", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + "  && tracks_fake==0 && (tracks_SR_short>0 || tracks_CR_short>0)", "bdtsideband_short_genprompt", folder, labels)
    ##do_plots(["tracks_mva_loose:tracks_dxyVtx"], event_selections["Baseline"] + "  && tracks_fake==0 && (tracks_SR_long>0 || tracks_CR_long>0)", "bdtsideband_long_genprompt", folder, labels)

        