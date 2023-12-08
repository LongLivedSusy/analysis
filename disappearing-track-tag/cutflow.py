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

def plot_signalregions_cutflow(ntuple, lheader, pdfname, numevents = -1, absolute=False, uselog = True, debug = False):

    # plot event selection cutflow and bins
    
    legendlabels = [
        "all events",                       # cut_allevents
        "+ #geq1 N_{jet}",                  # cut_njet1
        "+ MET_{hard}>30 GeV",              # cut_mht30
        "+ m_{T} (DTk,MET)>20 GeV",         # cut_mtDtkMHT
        "+ cut on N_{e}",                   # cut_nel
        "+ cut on N_{#mu}",                 # cut_nmu
        "+ cut m_{inv} (DTk,lep)>120 GeV",  # cut_minv
        "+ cut m_{T} (lep,MHT)>110 GeV",    # cut_mt
        "+ cut on MET_{hard}",              # cut_mht
        "+ cut on N_{jet}",                 # cut_njet
        "+ cut on N_{b}",                   # cut_bjet
        "+ cut on N_{DTk}",                 # cut_dtk
        "+ cut on dE/dx",                   # cut_dedx
    ]
    histocolors = [
         kBlack,
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
    baselineregions = {}
    baselineregions[ntuple] = {}

    srcounts = {}
    srcounts[ntuple] = {}
    for cutstage in range(len(legendlabels)):
        srcounts[ntuple][cutstage] = {}
        for sr in range(49+1)[1:]:

            cut_allevents = "HT>0"

            cut_njet1 = " && n_goodjets>=1"

            cut_mht30 = " && MHT>=30"
            
            cut_mtDtkMHT = " && mtDtMht>=20"
            
            if sr in range(1,24+1):
                cut_nel = " && n_goodelectrons==0"
            if sr in range(25,36+1):
                cut_nel = " && n_goodelectrons==0"
            if sr in range(37,48+1):
                cut_nel = " && n_goodelectrons>=1"
            if sr == 49:
                cut_nel = ""

            if sr in range(1,24+1):
                cut_nmu = " && n_goodmuons==0"
            if sr in range(25,36+1):
                cut_nmu = " && n_goodmuons>=1"
            if sr in range(37,48+1):
                cut_nmu = ""
            if sr == 49:
                cut_nmu = ""

            if sr in range(1,24+1):
                cut_minv = ""
            if sr in range(25,48+1):
                cut_minv = " && invmass>=120"
            if sr == 49:
                cut_minv = ""
            
            if sr in range(1,24+1):
                cut_mt = ""
            if sr in range(25,48+1):
                cut_mt = " && leadinglepton_mt>=110"
            if sr == 49:
                cut_mt = ""
            
            if sr in range(1,16+1):                             cut_mht = " && MHT>150 && MHT<300 "
            if sr in range(17,24+1):                            cut_mht = " && MHT>300 "
            if sr in range(25,32+1) or sr in range(37,44+1):    cut_mht = " && MHT>30 && MHT<100 "
            if sr in range(33,36+1) or sr in range(45,48+1):    cut_mht = " && MHT>100 "
            if sr == 49:                                        cut_mht = " && MHT>30 "
                        
            if sr in range(1,4+1) or sr in range(9,12+1) or sr in range(17,20+1):
                cut_njet = " && n_goodjets>=1 && n_goodjets<=2 "
            if sr in range(5,8+1) or sr in range(13,16+1) or sr in range(21,24+1):
                cut_njet = " && n_goodjets>=3 "
            if sr in range(25,49+1):
                cut_njet = " && n_goodjets>=1 "

            if sr in range(1,8+1):                              cut_bjet = " && n_btags==0 "
            if sr in range(8,16+1):                             cut_bjet = " && n_btags>=1 "
            if sr in range(17,24+1):                            cut_bjet = ""
            if sr in range(25,28+1):                            cut_bjet = " && n_btags==0 "
            if sr in range(29,32+1):                            cut_bjet = " && n_btags>=1 "
            if sr in range(33,36+1):                            cut_bjet = ""
            if sr in range(37,40+1):                            cut_bjet = " && n_btags==0 "
            if sr in range(41,44+1):                            cut_bjet = " && n_btags>=1 "
            if sr in range(45,48+1):                            cut_bjet = ""
            if sr == 49:                                        cut_bjet = ""

            # long/short tracks:
            if sr in [1,2,5,6,9,10,13,14,17,18,21,22,25,26,29,30,33,34,37,38,41,42,45,46]:
                cut_dtk = " && n_DTLong==1 && n_DTShort==0 "
            elif sr in [3,4,7,8,11,12,15,16,19,20,23,24,27,28,31,32,35,36,39,40,43,44,47,48]:
                cut_dtk = " && n_DTLong==0 && n_DTShort==1 "
            elif sr == 49:
                cut_dtk = " && (n_DTShort+n_DTLong)>=2 "

            if sr == 49:
                cut_dedx = ""
            elif sr % 2 == 1:
                cut_dedx = " && tracks_deDxHarmonic2pixel<4 "
            elif sr % 2 == 0:
                cut_dedx = " && tracks_deDxHarmonic2pixel>4 "

            if cutstage == 0:    finalcuts = cut_allevents
            elif cutstage == 1:  finalcuts = " ".join([cut_allevents, cut_njet1])
            elif cutstage == 2:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30])
            elif cutstage == 3:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT])
            elif cutstage == 4:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel])
            elif cutstage == 5:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu])
            elif cutstage == 6:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv])
            elif cutstage == 7:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt])
            elif cutstage == 8:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht])
            elif cutstage == 9:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht, cut_njet])
            elif cutstage == 10: finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht, cut_njet, cut_bjet])
            elif cutstage == 11: finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht, cut_njet, cut_bjet, cut_dtk])
            elif cutstage == 12: finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht, cut_njet, cut_bjet, cut_dtk, cut_dedx])
            
            if "SMS" in ntuple:
                finalcuts += " && tracks_chiCandGenMatchingDR<0.01 "
            
            print finalcuts
            
            if not debug:                
                h_tmp = plotting.get_all_histos([ntuple], "Events", "n_goodjets", cutstring=finalcuts, nBinsX=1, xmin=0, xmax=100, unweighted=absolute, numevents=numevents)
                if h_tmp:
                    count = h_tmp.Integral()
                else:
                    count = 0
            else:
                count = 1
            
            srcounts[ntuple][cutstage][sr] = count            
            
                    
        baselineregions[ntuple][cutstage] = {}
        for sr in range(3+1):

            cut_allevents = "HT>0"

            cut_njet1 = " && n_goodjets>=1"

            cut_mht30 = " && MHT>=30"
            
            cut_mtDtkMHT = " && mtDtMht>=20"
            
            if sr == 0:
                cut_nel = " && n_goodelectrons==0"
            if sr == 1:
                cut_nel = " && n_goodelectrons==0"
            if sr == 2:
                cut_nel = " && n_goodelectrons>=1"
            if sr == 3:
                cut_nel = ""

            if sr == 0:
                cut_nmu = " && n_goodmuons==0"
            if sr == 1:
                cut_nmu = " && n_goodmuons>=1"
            if sr == 2:
                cut_nmu = ""
            if sr == 3:
                cut_nmu = ""

            if sr == 1 or sr == 2:
                cut_minv = " && invmass>=120"
            else:
                cut_minv = ""
            
            if sr == 1 or sr == 2:
                cut_minv = " && leadinglepton_mt>=110"
            else:
                cut_minv = ""
            
            if sr == 0: cut_mht = " && MHT>=150 "
            else:       cut_mht = " && MHT>=30 "
                        
            cut_njet = " && n_goodjets>=1 "
            cut_bjet = " "

            # long/short tracks:
            if sr == 3:
                cut_dtk = " && (n_DTShort+n_DTLong)>=2 "
            else:
                cut_dtk = " && (n_DTShort+n_DTLong)==1 "

            cut_dedx = cut_dtk

            if cutstage == 0:    finalcuts = cut_allevents
            elif cutstage == 1:  finalcuts = " ".join([cut_allevents, cut_njet1])
            elif cutstage == 2:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30])
            elif cutstage == 3:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT])
            elif cutstage == 4:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel])
            elif cutstage == 5:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu])
            elif cutstage == 6:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv])
            elif cutstage == 7:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt])
            elif cutstage == 8:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht])
            elif cutstage == 9:  finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht, cut_njet])
            elif cutstage == 10: finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht, cut_njet, cut_bjet])
            elif cutstage == 11: finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht, cut_njet, cut_bjet, cut_dtk])
            elif cutstage == 12: finalcuts = " ".join([cut_allevents, cut_njet1, cut_mht30, cut_mtDtkMHT, cut_nel, cut_nmu, cut_minv, cut_mt, cut_mht, cut_njet, cut_bjet, cut_dtk, cut_dedx])
            
            if "SMS" in ntuple:
                finalcuts += " && tracks_chiCandGenMatchingDR<0.01 "
            
            print finalcuts
                     
            if not debug:                
                h_tmp = plotting.get_all_histos([ntuple], "Events", "n_goodjets", cutstring=finalcuts, nBinsX=1, xmin=0, xmax=100, unweighted=absolute, numevents=numevents)
                if h_tmp:
                    count = h_tmp.Integral()
                else:
                    count = 0
            else:
                count = 1
            
            baselineregions[ntuple][cutstage][sr] = count            

    
    # Do plotting:
    
    for plottype in [
                     "sr_eff",
                     "sr_abs",
                     "baseline_eff",
                     "baseline_abs"
                     ]:
    
        if absolute and "abs" not in plottype:
            continue
        if not absolute and "eff" not in plottype:
            continue
            
        print plottype
    
        if "sr" in plottype:
            counts = srcounts
        if "baseline" in plottype:
            counts = baselineregions
                
        canvas = TCanvas("c1", "c1", 1000, 630)
        canvas.SetBottomMargin(.16)
        canvas.SetLeftMargin(.14)
        canvas.SetGrid()
        
        legend = shared_utils.mklegend(x1=0.17, y1=0.17, x2=0.5, y2=0.7)
        legend.SetTextSize(0.002)
        
        histos = collections.OrderedDict()
        for ntuple in counts:
            for cutstage in counts[ntuple]:
                hname = ntuple + "_%s" % cutstage
                if "sr" in plottype: 
                    histos[hname] = TH1D(hname, hname, 50, 0, 50)
                if "baseline" in plottype:
                    histos[hname] = TH1D(hname, hname, 4, 0, 4)  
                
                for sr in counts[ntuple][cutstage]:
                    count = counts[ntuple][cutstage][sr]
                    if "sr" in plottype: 
                        histos[hname].SetBinContent(sr, count)
                    if "baseline" in plottype:
                        histos[hname].SetBinContent(sr+1, count)
                        
            
        # normalize to all events:
        if "eff" in plottype:
            for ntuple in counts:
                for cutstage in counts[ntuple]:
                    if cutstage == 0:
                        continue
                    hname = ntuple + "_%s" % cutstage
                    histos[hname].Divide(histos[ntuple + "_0"])
        
        
        for i_histo, identifier in enumerate(sorted(histos)):
                
                if "eff" in plottype and "_0" in identifier:
                    continue
                
                if i_histo == 0:
                    drawoptions = "hist E0"
                else:
                    drawoptions = "hist E0 same"
            
                shared_utils.histoStyler(histos[identifier])
                
                print identifier
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
                        histos[identifier].GetYaxis().SetRangeUser(1e-6,2)
                    else:
                        histos[identifier].GetYaxis().SetRangeUser(0,1.2)
                if "abs" in plottype:
                    if uselog:
                        histos[identifier].GetYaxis().SetRangeUser(1e-6,1e7)
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
                    histos[identifier].GetXaxis().SetBinLabel(1, "had. ch.");
                    histos[identifier].GetXaxis().SetBinLabel(2, "#mu ch.");
                    histos[identifier].GetXaxis().SetBinLabel(3, "el. ch.");
                    histos[identifier].GetXaxis().SetBinLabel(4, "n_{DTk}#geq2");
                    
        legend.SetHeader(lheader)
        for i in range(len(legendlabels)):
            if "eff" in plottype and i==0:
                continue
            legend.AddEntry(histos[ntuple + "_%s" % (i)], legendlabels[i])
        
        legend.SetTextSize(0.045)
        legend.Draw()
                
        shared_utils.stamp()
        if uselog:
            canvas.SetLogy(True)
        
        thispdfname = pdfname    
        thispdfname = thispdfname.replace(".pdf", "_%s.pdf" % plottype)
            
        canvas.Print(thispdfname)  
        canvas.SaveAs(thispdfname.replace(".pdf", ".root"))  
    

if __name__ == "__main__":
    
    parser = OptionParser()
    parser.add_option("--index", dest="index", default=-1)
    parser.add_option("--debug", dest="debug", action="store_true")
    (options, args) = parser.parse_args()
    options.index = int(options.index)
    
    if options.index == 1:
       plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowOct11_merged/RunIIFall17MiniAODv2.WJetsToLNu*root", "WJetsToLNu bg. event(s) with", "cutflow_bg.pdf", debug = options.debug)
    if options.index == 2:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowOct11_merged/RunIIFall17MiniAODv2.WJetsToLNu*root", "WJetsToLNu bg. event(s) with", "cutflow_bg.pdf", debug = options.debug, absolute = True)
    if options.index == 3:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowOct11_merged/RunIIFall17FSv3.SMS-T1btbt*root", "T1btbt sg. event(s) with", "cutflow_t1btbt.pdf", debug = options.debug)
    if options.index == 4:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowOct11_merged/RunIIFall17FSv3.SMS-T1btbt*root", "T1btbt sg. event(s) with", "cutflow_t1btbt.pdf", debug = options.debug, absolute = True)
    if options.index == 5:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowOct11_merged/RunIIFall17FSv3.SMS-T2tb*root", "T2tb sg. event(s) with", "cutflow_t2tb.pdf", debug = options.debug)
    if options.index == 6:
        plot_signalregions_cutflow("../ntupleanalyzer/skim_cutflowOct11_merged/RunIIFall17FSv3.SMS-T2tb*root", "T2tb sg. event(s) with", "cutflow_t2tb.pdf", debug = options.debug, absolute = True)
    if options.index == -1:
        for i in range(6+1)[1:]:
            os.system("./cutflow.py --index %s &" % i)
