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

def plot_signalregions_cutflow(ntuple, lheader, pdfname, do_sr, ctau, numevents = -1, absolute=False, uselog = True, debug = False):

    if "SMS" not in ntuple:
        return 0

    # plot event selection cutflow and bins
    
    legendlabels = [
        "all events",                       # cut_allevents     # cutstage1 
        "+ N_{DTk} #geq 1",                 # cut_dtk1          # cutstage2 
        "+ #geq1 N_{jet}",                  # cut_njet1         # cutstage3 
        "+ MET>30 GeV",                     # cut_mht30         # cutstage4 
        "+ m_{T} (DTk,MET)>20 GeV",         # cut_mtDtkMHT      # cutstage5 
        "+ cut on N_{e}",                   # cut_nel           # cutstage6 
        "+ cut on N_{#mu}",                 # cut_nmu           # cutstage7 
        "+ cut m_{inv} (DTk,lep)>120 GeV",  # cut_minv          # cutstage8 
        "+ cut m_{T} (lep,MET)>110 GeV",    # cut_mt            # cutstage9 
        "+ cut on MET",                     # cut_mht           # cutstage10
        "+ cut on N_{b-jet}",               # cut_bjet          # cutstage11
        "+ cut on N_{jet}",                 # cut_njet          # cutstage12
        "+ cut on N_{DTk}",                 # cut_dtk           # cutstage13
        "+ cut on dE/dx",                   # cut_dedx          # cutstage14
    ]
    histocolors = [
         kBlack,
         kGray,
         kRed,
         kRed-7,
         kRed-9,
         kRed-10,
         kOrange,
         kOrange-3,
         kOrange-7,
         kBlue,
         kCyan,
         kViolet,
         kViolet-7,
         kViolet-10,
    ]
    
    # get counts
    srcounts = collections.OrderedDict()
    srcounts[ntuple] = collections.OrderedDict()
        
    if do_sr:
        srbins = range(49+1)[1:]
    else:
        srbins = [49, 50, 51, 52]

    # number of events surviving for stage 1 = n_cutstageSR==1  (all tracks)
    # number of events surviving for stage 2 = n_cutstageSR>=2  ("+ N_{DTk} #geq 1")
    # number of events surviving for stage 3 = n_cutstageSR>=3  ...
    
    for sr in srbins:

        srcounts[ntuple][sr] = collections.OrderedDict()            
        
        for i_cutstage, cutstage in enumerate(range(len(legendlabels))):
            
            if "SMS" in ntuple:
                finalcuts = "n_cutstageCtau%sSR%s>=%s" % (ctau, sr, i_cutstage+1)
            else:
                finalcuts = "n_cutstageSR%s>=%s" % (sr, i_cutstage+1)

            if not debug:                
                h_tmp = plotting.get_all_histos([ntuple], "Events", "n_goodjets", cutstring=finalcuts, nBinsX=1, xmin=0, xmax=100, unweighted=absolute, numevents=numevents)
                if h_tmp:
                    count = h_tmp.Integral()
                else:
                    count = 0
            else:
                count = 1
            
            srcounts[ntuple][sr][cutstage] = count            
                            
    #print srcounts
    
    # Do plotting:
    
    if do_sr:
        plottypes = ["sr_eff", "sr_abs"]
    else:
        plottypes = ["baseline_eff", "baseline_abs"]
    
    for plottype in plottypes:
    
        if "eff" in plottype:
            legendlabels[1] = "events with N_{DTk} #geq 1"
    
        if "SMS" in ntuple:
            legendlabels[1] = legendlabels[1].replace("N_{DTk}", "#chi_{1}^{0}-matched N_{DTk}")
    
        if absolute and "abs" not in plottype:
            continue
        if not absolute and "eff" not in plottype:
            continue
            
        print plottype
                    
        canvas = TCanvas("c1", "c1", 1000, 630)
        canvas.SetBottomMargin(.16)
        canvas.SetLeftMargin(.14)
        canvas.SetGrid()
        
        legend = shared_utils.mklegend(x1=0.17, y1=0.17, x2=0.5, y2=0.6)
        legend.SetTextSize(0.03)
        
        histos = collections.OrderedDict()
        for ntuple in srcounts:
            for sr in srcounts[ntuple]:
                for cutstage in srcounts[ntuple][sr]:
                    hname = ntuple + "_%s" % cutstage
                    if hname not in histos:
                        if "sr" in plottype: 
                            histos[hname] = TH1D(hname, hname, 50, 0, 50)
                        if "baseline" in plottype:
                            histos[hname] = TH1D(hname, hname, 4, 49, 53)  
                    count = srcounts[ntuple][sr][cutstage]
                    if "sr" in plottype: 
                        histos[hname].SetBinContent(sr + 1, count)
                    if "baseline" in plottype:
                        histos[hname].SetBinContent(sr - 49 + 1, count)
                        
                    #print "Filled", hname, sr, count
                        
        # normalize to all events:
        if "eff" in plottype:
            for ntuple in srcounts:
                for cutstage in srcounts[ntuple][sr]:
                    if cutstage == 0:
                        continue
                    hname = ntuple + "_%s" % cutstage
                    histos[hname].Divide(histos[ntuple + "_0"])
        
        for i_histo, identifier in enumerate(histos):
                
                if "eff" in plottype and "_0" in identifier:
                    continue
                
                if i_histo == 0:
                    drawoptions = "hist E0"
                else:
                    drawoptions = "hist E0 same"
            
                shared_utils.histoStyler(histos[identifier])
                
                #print identifier
                i = int(identifier.split("_")[-1])
                histos[identifier].SetLineColor(histocolors[i])
                
                if "_0" in identifier:
                    histos[identifier].SetLineStyle(2)
                
                histos[identifier].GetXaxis().SetLabelSize(0.5 * histos[identifier].GetXaxis().GetLabelSize())
                histos[identifier].GetYaxis().SetLabelSize(histos[identifier].GetXaxis().GetLabelSize())
                histos[identifier].GetZaxis().SetLabelSize(0.6 * histos[identifier].GetYaxis().GetLabelSize())
                histos[identifier].GetYaxis().SetTitleSize(0.7 * histos[identifier].GetYaxis().GetTitleSize())
                histos[identifier].GetYaxis().SetMaxDigits(4)
                
                if "eff" in plottype:
                    if uselog:
                        histos[identifier].GetYaxis().SetRangeUser(1e-8,7)
                    else:
                        histos[identifier].GetYaxis().SetRangeUser(0,1.2)
                if "abs" in plottype:
                    if uselog:
                        histos[identifier].GetYaxis().SetRangeUser(0.5,1e8)
                        if "SMS" in ntuple:
                            histos[identifier].GetYaxis().SetRangeUser(0.5,1e5)
                    else:
                        histos[identifier].GetYaxis().SetRangeUser(0,1e7)
                histos[identifier].SetTitleSize(0.6 * histos[identifier].GetTitleSize())            
        
                histos[identifier].Draw(drawoptions)

                if "eff" in plottype: 
                    ylabel = "percentage of ntuple events"
                if "abs" in plottype: 
                    ylabel = "unweighted ntuple events"
                histos[identifier].SetTitle(";signal region;%s" % ylabel)

                if "baseline" in plottype: 
                    histos[identifier].SetTitle(";;%s" % ylabel)            
                    histos[identifier].GetXaxis().SetBinLabel(1, "had. ch.")
                    histos[identifier].GetXaxis().SetBinLabel(2, "#mu ch.")
                    histos[identifier].GetXaxis().SetBinLabel(3, "el. ch.")
                    histos[identifier].GetXaxis().SetBinLabel(4, "n_{DTk}#geq2")
                else:
                    histos[identifier].GetXaxis().SetRangeUser(1,50)
                    
        legend.SetHeader(lheader)
        for i in range(len(legendlabels)):
            if "eff" in plottype and i==0:
                continue
            legend.AddEntry(histos[ntuple + "_%s" % (i)], legendlabels[i])
        
        legend.Draw()
                
        #shared_utils.stamp()
        if uselog:
            canvas.SetLogy(True)
        
        os.system("mkdir -p plots-cutflow")
        thispdfname = "plots-cutflow/%s_ctau%s_%s.pdf" % (pdfname.replace(".pdf", ""), ctau, plottype)     
        #thispdfname = thispdfname.replace(".pdf", "_%s.pdf" % plottype)

        canvas.SaveAs(thispdfname)  
        
        fout = TFile(thispdfname.replace(".pdf", ".root"), "recreate")
        for i_label, label in enumerate(histos):
            hname = label.split("/")[-1]
            hname = hname.replace("*root", "")
            histos[label].SetName(hname)
            histos[label].Write()
        canvas.Write()  
        fout.Close()
        
    

if __name__ == "__main__":
    
    parser = OptionParser()
    parser.add_option("--index", dest="index", default=-1)
    parser.add_option("--numevents", dest="numevents", default=-1)
    parser.add_option("--debug", dest="debug", action="store_true")
    (options, args) = parser.parse_args()
    options.index = int(options.index)
    
    ctau = 200
        
    if options.index == 1:
       plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17MiniAODv2.WJetsToLNu*root", "WJetsToLNu bg.", "cutflow_bg.pdf", False, ctau, numevents = int(options.numevents), debug = options.debug)
    if options.index == 2:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17MiniAODv2.WJetsToLNu*root", "WJetsToLNu bg.", "cutflow_bg.pdf", False, ctau, numevents = int(options.numevents), debug = options.debug, absolute = True)
    if options.index == 3:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowApr24_merged/RunIIFall17FSv3.SMS-T1btbt*root", "T1btbt (m(#tilde{g})=1.5 TeV, m(#tilde{#chi}_{1}^{0})=1.1 TeV, c#tau=%s cm)" % (ctau), "cutflow_t1btbt.pdf", False, ctau, numevents = int(options.numevents), debug = options.debug)
    if options.index == 4:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowApr24_merged/RunIIFall17FSv3.SMS-T1btbt*root", "T1btbt (m(#tilde{g})=1.5 TeV, m(#tilde{#chi}_{1}^{0})=1.1 TeV, c#tau=%s cm)" % (ctau), "cutflow_t1btbt.pdf", False, ctau, numevents = int(options.numevents), debug = options.debug, absolute = True)
    if options.index == 5:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowApr24_merged/RunIIFall17FSv3.SMS-T2tb*root", "T2tb (m(#tilde{b})=1 TeV, m(#tilde{#chi}_{1}^{0})=900 GeV, c#tau=%s cm)" % (ctau), "cutflow_t2tb.pdf", False, ctau, numevents = int(options.numevents), debug = options.debug)
    if options.index == 6:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowApr24_merged/RunIIFall17FSv3.SMS-T2tb*root", "T2tb (m(#tilde{b})=1 TeV, m(#tilde{#chi}_{1}^{0})=900 GeV, c#tau=%s cm)" % (ctau), "cutflow_t2tb.pdf", False, ctau, numevents = int(options.numevents), debug = options.debug, absolute = True)
    if options.index == 7:
       plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17MiniAODv2.WJetsToLNu*root", "WJetsToLNu bg.", "cutflow_bg.pdf", True, ctau, numevents = int(options.numevents), debug = options.debug)
    if options.index == 8:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowDec21b_merged/RunIIFall17MiniAODv2.WJetsToLNu*root", "WJetsToLNu bg.", "cutflow_bg.pdf", True, ctau, numevents = int(options.numevents), debug = options.debug, absolute = True)
    if options.index == 9:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowApr24_merged/RunIIFall17FSv3.SMS-T1btbt*root", "T1btbt (m(#tilde{g})=1.5 TeV, m(#tilde{#chi}_{1}^{0})=1.1 TeV, c#tau=%s cm)" % (ctau), "cutflow_t1btbt.pdf", True, ctau, numevents = int(options.numevents), debug = options.debug)
    if options.index == 10:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowApr24_merged/RunIIFall17FSv3.SMS-T1btbt*root", "T1btbt (m(#tilde{g})=1.5 TeV, m(#tilde{#chi}_{1}^{0})=1.1 TeV, c#tau=%s cm)" % (ctau), "cutflow_t1btbt.pdf", True, ctau, numevents = int(options.numevents), debug = options.debug, absolute = True)
    if options.index == 11:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowApr24_merged/RunIIFall17FSv3.SMS-T2tb*root", "T2tb (m(#tilde{b})=1 TeV, m(#tilde{#chi}_{1}^{0})=900 GeV, c#tau=%s cm)" % (ctau), "cutflow_t2tb.pdf", True, ctau, numevents = int(options.numevents), debug = options.debug)
    if options.index == 12:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowApr24_merged/RunIIFall17FSv3.SMS-T2tb*root", "T2tb (m(#tilde{b})=1 TeV, m(#tilde{#chi}_{1}^{0})=900 GeV, c#tau=%s cm)" % (ctau), "cutflow_t2tb.pdf", True, ctau, numevents = int(options.numevents), debug = options.debug, absolute = True)
    if options.index == -1:
        for i in range(12+1)[1:]:
            os.system("./cutflowCutstageSRCtau10.py --index %s &" % i)
            os.system("./cutflowCutstageSRCtau200.py --index %s &" % i)
