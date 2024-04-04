#!/bin/env python
from __future__ import division
from optparse import OptionParser
from ROOT import *
import plotting
import os
import collections
import shared_utils
import glob
import numpy
import collections

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

cuts = collections.OrderedDict()

cuts["BDT_short"] = [
            "tracks_is_pixel_track==1",
            "tracks_pt>25",
            "tracks_passmask==1",
            "tracks_trackQualityHighPurity==1",
            "abs(tracks_eta)<2.0",
            "tracks_ptErrOverPt2<10",
            "tracks_dxyVtx<0.1",
            "tracks_dzVtx<0.1",
            "tracks_trkRelIso<0.2",
            "tracks_trackerLayersWithMeasurement>=2",
            "tracks_nValidTrackerHits>=2",
            "tracks_nMissingInnerHits==0",
            "tracks_nValidPixelHits>=2",
            "tracks_passPFCandVeto==1",
            "tracks_passleptonveto==1",
            "tracks_passpionveto==1",
            "tracks_passjetveto==1",
            "tracks_nMissingOuterHits>=0",
            "tracks_mva_sep21v1_baseline>$BDTCUT",
            "tracks_matchedCaloEnergy<15",
]

cuts["BDT_long"] = [
            "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2",
            "tracks_pt>40",
            "tracks_passmask==1",
            "tracks_trackQualityHighPurity==1",
            "abs(tracks_eta)<2.0",
            "tracks_ptErrOverPt2<10",
            "tracks_dxyVtx<0.1",
            "tracks_dzVtx<0.1",
            "tracks_trkRelIso<0.2",
            "tracks_trackerLayersWithMeasurement>=2",
            "tracks_nValidTrackerHits>=2",
            "tracks_nMissingInnerHits==0",
            "tracks_nValidPixelHits>=2",
            "tracks_passPFCandVeto==1",
            "tracks_passleptonveto==1",
            "tracks_passpionveto==1",
            "tracks_passjetveto==1",
            "tracks_nMissingOuterHits>=2",
            "tracks_mva_sep21v1_baseline>$BDTCUT",
            "tracks_matchedCaloEnergy/tracks_p<0.2",
]

def write_table():

    latex = r"""
\begin{tabular}{|c|clll|clll|}
\hline
                          & \multicolumn{4}{c|}{$n_{\text{tracks}}$(Phase 0)}                                                                                     & \multicolumn{4}{c|}{$n_{\text{tracks}}$(Phase 1)}                                                                                     \\ \hline
                          & \multicolumn{2}{c|}{short}                                & \multicolumn{2}{c|}{long}                            & \multicolumn{2}{c|}{short}                                & \multicolumn{2}{c|}{long}                            \\ \hline
\multicolumn{1}{|c|}{cut} & \multicolumn{1}{l|}{signal} & \multicolumn{1}{l|}{backg.} & \multicolumn{1}{l|}{signal} & backg.                 & \multicolumn{1}{l|}{signal} & \multicolumn{1}{l|}{backg.} & \multicolumn{1}{l|}{signal} & backg.                 \\ \hline
$LINE
\end{tabular}
"""

    latexline = r"\multicolumn{1}{|c|}{$CUT}      & \multicolumn{1}{c|}{$p0shortsg}      & \multicolumn{1}{c|}{$p0shortbg}      & \multicolumn{1}{c|}{$p0longsg}      & \multicolumn{1}{c|}{$p0longbg} & \multicolumn{1}{c|}{$p1shortsg}      & \multicolumn{1}{c|}{$p1shortbg}      & \multicolumn{1}{c|}{$p1longsg}      & \multicolumn{1}{c|}{$p1longbg} \\ \hline"

    tablelines = {}
    tablelines["Had"] = []
    tablelines["El"] = []
    tablelines["Mu"] = []

    fin = {}
    canvases = {}
    histos = {}
    
    fin["Had0"] = TFile("plots/cutflow_skim_32_cutflow_hadronic_phase0_BDT.root")
    fin["Had1"] = TFile("plots/cutflow_skim_32_cutflow_hadronic_phase1_BDT.root")
    fin["El0"] = TFile("plots/cutflow_skim_32_cutflow_electron_phase0_BDT.root")
    fin["El1"] = TFile("plots/cutflow_skim_32_cutflow_electron_phase1_BDT.root")
    fin["Mu0"] = TFile("plots/cutflow_skim_32_cutflow_muon_phase0_BDT.root")
    fin["Mu1"] = TFile("plots/cutflow_skim_32_cutflow_muon_phase1_BDT.root")

    for label in fin:
        canvases[label] = fin[label].Get("c1")
        canvases[label].SetName("c1_" + label)
        #canvases[label].SetDirectory(0)

        histos[label + "_sg_BDT_long"] = canvases[label].GetPrimitive("sg_BDT_long")
        histos[label + "_sg_BDT_long"].SetName(label + "_sg_BDT_long")
        histos[label + "_sg_BDT_long"].SetDirectory(0)
        histos[label + "_sg_BDT_short"] = canvases[label].GetPrimitive("sg_BDT_short")
        histos[label + "_sg_BDT_short"].SetName(label + "_sg_BDT_short")
        histos[label + "_sg_BDT_short"].SetDirectory(0)
        histos[label + "_bg_BDT_long"] = canvases[label].GetPrimitive("bg_BDT_long")
        histos[label + "_bg_BDT_long"].SetName(label + "_bg_BDT_long")
        histos[label + "_bg_BDT_long"].SetDirectory(0)
        histos[label + "_bg_BDT_short"] = canvases[label].GetPrimitive("bg_BDT_short")
        histos[label + "_bg_BDT_short"].SetName(label + "_bg_BDT_short")
        histos[label + "_bg_BDT_short"].SetDirectory(0)

    for channel in ["Had", "El", "Mu"]:
        for i_cutlabel, binlabel in enumerate(cuts["BDT_short"]):      
            thisline = latexline

            if "tracks_is_pixel_track" in binlabel: binlabel = "track category"
            elif "tracks_ptErrOverPt2" in binlabel: binlabel = "$\Delta p_{T}$"
            elif "tracks_neutralPtSum/tracks_pt" in binlabel: binlabel = "nt. $\Sigma p_{T}/pT$"
            elif "tracks_neutralPtSum" in binlabel: binlabel = "nt. pTSum"
            elif "tracks_chargedPtSum/tracks_pt" in binlabel: binlabel = "ch. $\Sigma p_{T}/pT$"
            elif "tracks_chargedPtSum" in binlabel: binlabel = "ch. $\Sigma p_{T}$"
            elif "tracks_pt" in binlabel: binlabel = "$p_{T}$"
            elif "tracks_passmask" in binlabel: binlabel = "mask"
            elif "tracks_trackQualityHighPurity" in binlabel: binlabel = "purity"
            elif "tracks_eta" in binlabel: binlabel = "$\eta$"
            elif "tracks_dzVtx" in binlabel: binlabel = "$d_{z}$"
            elif "tracks_dxyVtx" in binlabel: binlabel = "$d_{xy}$"
            elif "tracks_trkRelIso" in binlabel: binlabel = "relIso"
            elif "tracks_trackerLayersWithMeasurement" in binlabel: binlabel = "layers"
            elif "tracks_nValidTrackerHits" in binlabel: binlabel = "tracker hits"
            elif "tracks_nMissingInnerHits" in binlabel: binlabel = "miss. inner hits"
            elif "tracks_nValidPixelHits" in binlabel: binlabel = "pixel hits"
            elif "tracks_passPFCandVeto" in binlabel: binlabel = "PFCand"
            elif "tracks_passleptonveto" in binlabel: binlabel = "lepton veto"
            elif "tracks_passpionveto" in binlabel: binlabel = "pion veto"
            elif "tracks_passjetveto" in binlabel: binlabel = "jet veto"
            elif "tracks_deDxHarmonic2pixel" in binlabel: binlabel = "dE/dx"
            elif "tracks_mva_tight_may20_chi2" in binlabel: binlabel = "BDT"
            elif "tracks_mva_" in binlabel: binlabel = "BDT"
            elif "tracks_matchedCaloEnergy/tracks_p" in binlabel: binlabel = "EDep/track p"     
            elif "tracks_nMissingOuterHits" in binlabel: binlabel = "miss. outer hits"
            elif "tracks_nMissingMiddleHits" in binlabel: binlabel = "miss. middle hits"
            elif "tracks_exo_leptoniso" in binlabel: binlabel = "lepton iso"
            elif "tracks_exo_trackiso" in binlabel: binlabel = "track iso"
            elif "tracks_exo_jetiso" in binlabel: binlabel = "jet iso"
            elif "tracks_matchedCaloEnergy" in binlabel: binlabel = "EDep"     
            elif "tracks_mt2_leptoniso" in binlabel: binlabel = "lepton iso"
            elif "tracks_mt2_trackiso" in binlabel: binlabel = "track iso"
            elif "tracks_pixelLayersWithMeasurement" in binlabel: binlabel = "pixel layers"

            thisline = thisline.replace("$CUT", binlabel)
            thisline = thisline.replace("$p0shortsg", "%.3f" % histos[channel + "0_sg_BDT_short"].GetBinContent(i_cutlabel + 1))
            thisline = thisline.replace("$p1shortsg", "%.3f" % histos[channel + "1_sg_BDT_short"].GetBinContent(i_cutlabel + 1))
            thisline = thisline.replace("$p0shortbg", "%.3f" % histos[channel + "0_bg_BDT_short"].GetBinContent(i_cutlabel + 1))
            thisline = thisline.replace("$p1shortbg", "%.3f" % histos[channel + "1_bg_BDT_short"].GetBinContent(i_cutlabel + 1))
            thisline = thisline.replace("$p0longsg", "%.3f" % histos[channel + "0_sg_BDT_long"].GetBinContent(i_cutlabel + 1))
            thisline = thisline.replace("$p1longsg", "%.3f" % histos[channel + "1_sg_BDT_long"].GetBinContent(i_cutlabel + 1))
            thisline = thisline.replace("$p0longbg", "%.3f" % histos[channel + "0_bg_BDT_long"].GetBinContent(i_cutlabel + 1))
            thisline = thisline.replace("$p1longbg", "%.3f" % histos[channel + "1_bg_BDT_long"].GetBinContent(i_cutlabel + 1))
            tablelines[channel].append(thisline)


    for channel in tablelines:

        thistable = latex
        thistable = thistable.replace("$LINE", "\n".join(tablelines[channel]))

        with open('table_%s.tex' % channel, 'w') as f:
          f.write(thistable)


def plot_cutflow(sg_files, bg_files, header, prefix, basecuts = "", numevents = -1, debug = False):
                
    histos = {}
    for bgsg in ["sg", "bg"]:
        for label in cuts:
            histos[bgsg + "_" + label] = TH1D(bgsg + "_" + label, bgsg + "_" + label, 20, 0, 20)
    
    # get consecutive cuts:
    cuts_consecutive = collections.OrderedDict()
    for label in cuts:
        cuts_consecutive[label] = []
        for i, cut in enumerate(cuts[label]):
            cuts_consecutive[label].append(" && ".join(cuts[label][:i+1]))

    # get nev:
    counts = {} 
    for bgsg in ["sg", "bg"]:
                
        for label in cuts_consecutive:
            counts[bgsg + "_" + label] = []
            for i, cut in enumerate(cuts_consecutive[label]):
                                                
                finalcuts = cut
                if "phase 0" in header:
                    if "short" in label:
                        finalcuts = finalcuts.replace("$BDTCUT", "0.1")
                    elif "long" in label:
                        finalcuts = finalcuts.replace("$BDTCUT", "0.12")
                elif "phase 1" in header:
                    if "short" in label:
                        finalcuts = finalcuts.replace("$BDTCUT", "0.15")
                    elif "long" in label:
                        finalcuts = finalcuts.replace("$BDTCUT", "0.08")                
                                
                if debug:
                    count = 1
                else:
                    if bgsg == "sg":
                        h_tmp = plotting.get_all_histos(sg_files, "Events", "tracks_is_pixel_track", cutstring = finalcuts + " && tracks_chiCandGenMatchingDR<0.01 " + basecuts, nBinsX=2, xmin=0, xmax=2, numevents=numevents)
                    else:
                        h_tmp = plotting.get_all_histos(bg_files, "Events", "tracks_is_pixel_track", cutstring = finalcuts, nBinsX=2, xmin=0, xmax=2, numevents=numevents)
                        
                    if h_tmp:
                        count = h_tmp.Integral()
                    else:
                        count = 0
                        
                counts[bgsg + "_" + label].append(count)
                histos[bgsg + "_" + label].Fill(i, count)
    
    # normalize histos:
    for label in histos:
        normalization = histos[label].GetBinContent(1)
        if normalization > 0:
            histos[label].Scale(1.0/normalization)
        
    # set alphanumeric x-axis labels:
    for label in histos:
        for i in range(1, histos[label].GetNbinsX() + 1):
            if i<=len(cuts[label.replace("sg_", "").replace("bg_", "")]):           
                
                binlabel = cuts[label.replace("sg_", "").replace("bg_", "")][i-1]
                if "tracks_is_pixel_track" in binlabel: binlabel = "category"
                elif "tracks_ptErrOverPt2" in binlabel: binlabel = "#Delta p_{T}"
                elif "tracks_neutralPtSum/tracks_pt" in binlabel: binlabel = "nt. #Sigma p_{T}/pT"
                elif "tracks_neutralPtSum" in binlabel: binlabel = "nt. pTSum"
                elif "tracks_chargedPtSum/tracks_pt" in binlabel: binlabel = "ch. #Sigma p_{T}/pT"
                elif "tracks_chargedPtSum" in binlabel: binlabel = "ch. #Sigma p_{T}"
                elif "tracks_pt" in binlabel: binlabel = "p_{T}"
                elif "tracks_passmask" in binlabel: binlabel = "mask"
                elif "tracks_trackQualityHighPurity" in binlabel: binlabel = "purity"
                elif "tracks_eta" in binlabel: binlabel = "|#eta|<2.0"
                elif "tracks_dzVtx" in binlabel: binlabel = "d_{z}<0.1"
                elif "tracks_dxyVtx" in binlabel: binlabel = "d_{xy}<0.1"
                elif "tracks_trkRelIso" in binlabel: binlabel = "relIso<0.2"
                elif "tracks_trackerLayersWithMeasurement" in binlabel: binlabel = "tr. layers >=2"
                elif "tracks_nValidTrackerHits" in binlabel: binlabel = "tracker hits >=2"
                elif "tracks_nMissingInnerHits" in binlabel: binlabel = "miss. inner hits = 0"
                elif "tracks_nValidPixelHits" in binlabel: binlabel = "pixel hits >=2"
                elif "tracks_passPFCandVeto" in binlabel: binlabel = "PFCand"
                elif "tracks_passleptonveto" in binlabel: binlabel = "lepton veto"
                elif "tracks_passpionveto" in binlabel: binlabel = "pion veto"
                elif "tracks_passjetveto" in binlabel: binlabel = "jet veto"
                elif "tracks_deDxHarmonic2pixel" in binlabel: binlabel = "dE/dx"
                elif "tracks_mva_tight_may20_chi2" in binlabel: binlabel = "BDT"
                elif "tracks_mva_" in binlabel: binlabel = "BDT"
                elif "tracks_matchedCaloEnergy/tracks_p" in binlabel: binlabel = "EDep/track p"     
                elif "tracks_nMissingOuterHits" in binlabel: binlabel = "miss. outer hits"
                elif "tracks_nMissingMiddleHits" in binlabel: binlabel = "miss. middle hits"
                elif "tracks_exo_leptoniso" in binlabel: binlabel = "lepton iso"
                elif "tracks_exo_trackiso" in binlabel: binlabel = "track iso"
                elif "tracks_exo_jetiso" in binlabel: binlabel = "jet iso"
                elif "tracks_matchedCaloEnergy" in binlabel: binlabel = "E_{dep}"     
                elif "tracks_mt2_leptoniso" in binlabel: binlabel = "lepton iso"
                elif "tracks_mt2_trackiso" in binlabel: binlabel = "track iso"
                elif "tracks_pixelLayersWithMeasurement" in binlabel: binlabel = "pixel layers"

                #binlabel = binlabel.replace("$BDTCUT", "BDT")

                print binlabel

                histos[label].GetXaxis().SetBinLabel(i, binlabel);
    
	canvas = TCanvas("c1","c1",1000,630)
	canvas.SetBottomMargin(.16)
	canvas.SetLeftMargin(.14)
	canvas.SetGrid()
        
    legend = shared_utils.mklegend(x1=0.17, y1=0.17, x2=0.4, y2=0.4)
    legend.SetTextSize(0.03)
        
    for i_label, label in enumerate(cuts.keys()):
        for bgsg in ["sg", "bg"]:
        
            if i_label == 0 and bgsg == "sg":
                drawoptions = "hist"
            else:
                drawoptions = "hist same"
        
            identifier = bgsg + "_" + label
            shared_utils.histoStyler(histos[identifier])
            
            if "short" in label:
                category = "short"
                histos[identifier].SetLineColor(kRed)
            elif "long" in label:
                category = "long"
                histos[identifier].SetLineColor(kBlue)
            
            #histos[identifier].GetXaxis().SetLabelSize(0.4 * histos[identifier].GetXaxis().GetLabelSize())
            #histos[identifier].GetYaxis().SetLabelSize(histos[identifier].GetXaxis().GetLabelSize())
            #histos[identifier].GetZaxis().SetLabelSize(0.6 * histos[identifier].GetYaxis().GetLabelSize())
            #histos[identifier].GetYaxis().SetTitleSize(0.7 * histos[identifier].GetYaxis().GetTitleSize())
            
            histos[identifier].Draw(drawoptions)
            
            if bgsg == "bg":
                histos[identifier].SetLineStyle(2)
            else:
                histos[identifier].SetLineStyle(1)
            
            histos[identifier].SetTitle(";;percentage of tracks remaining")
            legend.AddEntry(histos[identifier], "%s tracks (%s)" % (category, bgsg))
            histos[identifier].GetYaxis().SetRangeUser(0,1.1)
                        
    #legend.SetTextSize(0.045)
    legend.SetHeader(header)
    legend.Draw()
            
    #shared_utils.stamp()
            
    batchname = sg_files[0].split("/")[2]
    canvas.Print("plots-dtkcutflow/cutflow_" + batchname + "_" + prefix + "_" + label.replace("_short", "").replace("_long", "") + ".pdf")  
     
    fout = TFile("plots-dtkcutflow/cutflow_" + batchname + "_" + prefix + "_" + label.replace("_short", "").replace("_long", "") + ".root", "recreate")
    for i_label, label in enumerate(histos):
        histos[label].SetName(label)
        histos[label].Write()
    canvas.Write()  
    #canvas.SaveAs("plots-dtkcutflow/cutflow_" + batchname + "_" + prefix + "_" + label.replace("_short", "").replace("_long", "") + ".root")  
    fout.Close()
       

if __name__ == "__main__":
    
    parser = OptionParser()
    parser.add_option("--index", dest="index", default=-1)
    parser.add_option("--table", dest="table", action="store_true")
    (options, args) = parser.parse_args()
    options.index = int(options.index)

    if options.table:
        write_table()
        quit()


    if options.index == -1:
        for i in range(1, 8):
            os.system("./cutflowDtk.py --index %s &" % i)
   
    channels = {
                  "T1btbt (m(#tilde{g})=1.5 TeV, m(#tilde{#chi}_{1}^{0})=1.1 TeV)":           "",
                  "T2tb (m(#tilde{b})=1 TeV, m(#tilde{#chi}_{1}^{0})=900 GeV)":           "",
                  #"leptonic channe":           "",
                  #"hadronic channel":   "HT>150 && MHT>150 && n_goodjets>=1 && n_goodelectrons==0 && n_goodmuons==0 && ",
                  #"electron channel":   "MHT>30 && n_goodjets>=1 && n_goodelectrons>=1 && tracks_invmass>120 && leadinglepton_mt>110 && ",
                  #"muon channel":       "MHT>30 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>120 && leadinglepton_mt>110 && ",
               }
    
    counter = 0
    for channel in sorted(channels.keys()):
        if "T1btbt" in channel or "hadronic" in channel:
            sgfiles = ["../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17FSv3.SMS-T1btbt-LLChipm-ctau10to200-mGluino-1000to2800-mLSP0to2800.root"]
            bgfiles = ["../ntupleanalyzer/skim_cutflowDec21b_merged/Summer16.QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"]    
        elif "T2tb" in channel or "muon" in channel:
            sgfiles = ["../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17FSv3.SMS-T2tb-LLChipm-ctau10to200-mStop-400to1750-mLSP0to1650.root"]
            bgfiles = ["../ntupleanalyzer/skim_cutflowDec21b_merged/Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"]
               
        counter += 1
        if options.index == counter:
            #plot_cutflow(sgfiles, bgfiles, "%s (phase 0)" % channel, channel.split()[0] + "_phase0", basecuts = channels[channel])
            plot_cutflow(sgfiles, bgfiles, "%s (phase 0)" % channel, channel.split()[0] + "_phase0_ctau10", basecuts = " && SusyCTau==10")
            plot_cutflow(sgfiles, bgfiles, "%s (phase 0)" % channel, channel.split()[0] + "_phase0_ctau200", basecuts = " && SusyCTau==200")

    for channel in sorted(channels.keys()):
        if "T1btbt" in channel or "hadronic" in channel:
            sgfiles = ["../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17FSv3.SMS-T1btbt-LLChipm-ctau10to200-mGluino-1000to2800-mLSP0to2800.root"]
            bgfiles = ["../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17MiniAODv2.QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8.root"]    
        elif "T2tb" in channel or "muon" in channel:
            sgfiles = ["../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17FSv3.SMS-T2tb-LLChipm-ctau10to200-mStop-400to1750-mLSP0to1650.root"]
            bgfiles = ["../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8.root"]

        counter += 1
        if options.index == counter:
            #plot_cutflow(sgfiles, bgfiles, "%s (phase 1)" % channel, channel.split()[0] + "_phase1", basecuts = channels[channel])
            plot_cutflow(sgfiles, bgfiles, "%s (phase 1)" % channel, channel.split()[0] + "_phase1_ctau10", basecuts = " && SusyCTau==10")
            plot_cutflow(sgfiles, bgfiles, "%s (phase 1)" % channel, channel.split()[0] + "_phase1_ctau200", basecuts = " && SusyCTau==200")

