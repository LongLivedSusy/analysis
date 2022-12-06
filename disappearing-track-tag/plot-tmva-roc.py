#!/usr/bin/env python
from ROOT import *
from math import sqrt
from array import array
import shared_utils
from collections import OrderedDict
import plotting
import numpy

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def graphStyler(h, color=kBlack):
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    size = 0.059 #.059
    font = 132
    h.GetXaxis().SetLabelFont(font)
    h.GetYaxis().SetLabelFont(font)
    h.GetXaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleSize(size)
    h.GetXaxis().SetTitleSize(size)
    h.GetXaxis().SetLabelSize(size)
    h.GetYaxis().SetLabelSize(size)
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetTitleOffset(1.05)
    h.SetFillColor(kWhite)


tmva_folders = OrderedDict({
                #"sep21v1-baseline",
                #"sep21v1-useLayers",
                #"sep21v1-baseline": "BDT training with PU",
                "sep21v1-baseline-noPU": "BDT training without PU",
                #"sep21v1-baseline-withPU": "BDT training with PU",
                })

extralabel = "_PU"

categories = [
              "short",
              "long"
             ]

plot_roc = 1
plot_after_bdt = 0
use_prebaked_histo = 0

if plot_roc:
    
    # ROC comparison plot
    
    histos = {}
    
    for category in categories:
            
        canvas = shared_utils.mkcanvas("c1")
        legend = shared_utils.mklegend(x1=.17, y1=.17, x2=.6, y2=.6)
        legend.SetTextSize(0.035)
        emptyhisto = TH2F("empty", "empty", 1, 0, 1, 1, 0, 1)
        shared_utils.histoStyler(emptyhisto)
        emptyhisto.Draw()
        emptyhisto.GetYaxis().SetTitle('Background rejection')
        emptyhisto.GetXaxis().SetTitle('Signal efficiency')
        
        drawhists = []
    
        for i_phase, phase in enumerate(["2016", "2017"]):
    
            #colors = range(209,270)
            #colors = [kBlack, kBlue, kBlue-3, kBlue-9, kCyan, kCyan-3, kGreen, kGreen-3, kOrange, kRed, kPink, kMagenta, kMagenta-3]
            colors = [kAzure, kOrange,  kCyan, kGreen-3, kRed, kMagenta, kRed-9, kAzure+2]
            
            color = 0
            dicke = len(tmva_folders)+1
            
            for i_tmva_folder, current_tmva_folder in enumerate(sorted(tmva_folders)):
                
                tmva_folder = "%s-%s-tracks-%s" % (phase, category, current_tmva_folder)
                print tmva_folder
                
                #if phase in tmva_folder and category in tmva_folder:
                    
                print tmva_folder
                fin = TFile("%s/output.root" % tmva_folder)
                
                # get histogram
                if use_prebaked_histo:
                    histos[tmva_folder] = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_rejBvsS")
                    histos[tmva_folder].SetDirectory(0)
                    shared_utils.histoStyler(histos[tmva_folder])
                else:
                
                    bdt_cut = []
                    efficiencies_signal = []
                    efficiencies_background = []
                
                    #treefin = TFile("%s/output.root" % tmva_folder)
                    tmvatree = fin.Get("dataset/TestTree")
                    
                    #(%s)*CrossSection*puWeight
                    
                    for i_classID, classID in enumerate(["Signal", "Background"]):
                        histo_denom = plotting.get_histogram_from_tree(tmvatree, "BDT", cutstring="(classID==%s)*weight" % i_classID, nBinsX=50, xmin=-1, xmax=1, add_overflow=False)        
                        denom = histo_denom.Integral(histo_denom.GetXaxis().FindBin(-1), histo_denom.GetXaxis().FindBin(1))
                        for i_score in numpy.arange(-1.0, 1.0, 0.2):
                            
                            print classID, i_score
                            
                            histo_num = plotting.get_histogram_from_tree(tmvatree, "BDT", cutstring="(classID==%s && BDT>%s)*weight" % (i_classID, i_score), nBinsX=50, xmin=-1, xmax=1, add_overflow=False)        
                            num = histo_num.Integral(histo_num.GetXaxis().FindBin(i_score), histo_num.GetXaxis().FindBin(1))
                            
                            #print i_score, num, denom
                            
                            if i_classID == 0:
                                # fill bdt thresholds only once
                                bdt_cut.append(i_score)
                                if denom>0:
                                    efficiencies_signal.append(1.0*num/denom)
                                else:
                                    efficiencies_signal.append(0)
                            else:
                                if denom>0:
                                    efficiencies_background.append(1.0 - 1.0*num/denom)
                                else:
                                    efficiencies_background.append(0)
                    
                    #histos[tmva_folder] = TH1F(tmva_folder, tmva_folder, 100, 0, 1)
                    #histos[tmva_folder].SetDirectory(0)
                    histos[tmva_folder] = TGraph()
                    
                    for i_bin, eff_sg in enumerate(efficiencies_signal):
                        #print bdt_cut[i_bin], efficiencies_signal[i_bin], efficiencies_background[i_bin]
                        #histos[tmva_folder].Fill(histos[tmva_folder].GetXaxis().FindBin(efficiencies_signal[i_bin]), efficiencies_background[i_bin])
                        #histos[tmva_folder].Fill(efficiencies_signal[i_bin], efficiencies_background[i_bin])
                        histos[tmva_folder].SetPoint(i_bin, efficiencies_signal[i_bin], efficiencies_background[i_bin])
                    
                    #histos[tmva_folder] = roughgraph
                    
                    #for i in range(100):
                    #    histos[tmva_folder].Fill(i, roughgraph.Eval(i*1.0/100))

                    graphStyler(histos[tmva_folder])

                histos[tmva_folder].SetName(tmva_folder)
                #histos[tmva_folder].SetTitle('')
                #histos[tmva_folder].GetXaxis().SetRangeUser(0.5, 1)
                #histos[tmva_folder].GetYaxis().SetRangeUser(0.5, 1)
                
                color = colors.pop(0)
                histos[tmva_folder].SetLineColor(color)
                
                fin.Close()
                
                label = tmva_folder.replace("-", " ")
    
                histos[tmva_folder].SetLineStyle(i_phase + 1)
                histos[tmva_folder].SetLineWidth(dicke - i_tmva_folder)
    
                legendtext = "%s %s tracks, %s" % (phase, category, tmva_folders[current_tmva_folder])

                legend.AddEntry(histos[tmva_folder], legendtext)
                legend.SetHeader("%s tracks" % category)
    
                drawhists.append(tmva_folder)
            
            for i, label in enumerate(drawhists):
                if use_prebaked_histo:
                    histos[label].Draw("hist same")
                else:
                    histos[label].Draw("c same")
            
        legend.Draw()
        shared_utils.stamp(showlumi=False)
        #canvas.SaveAs("ROC_%s_%s%s.pdf" % (phase, category, extralabel))
        canvas.SaveAs("ROC_%s%s.pdf" % (category, extralabel))
    

if plot_after_bdt:

    # BDT output plot

    bg_efficiencies = {}

    for phase in [
                  #"2016",
                  "2017",
                 ]:
        for category in categories:

            if category == "short":
                if phase == "2016":
                    bdtcut = 0.1
                elif phase == "2017":
                    bdtcut = 0.12
            elif category == "long":
                if phase == "2016":
                    bdtcut = 0.1
                elif phase == "2017":
                    bdtcut = 0.15


            for tmva_folder in sorted(tmva_folders):
                tmva_folder = "%s-%s-tracks-%s" % (phase, category, tmva_folder)

                for plot_efficiencies in [False, True]:
                    
                    canvas = shared_utils.mkcanvas("c1")
                    legend = shared_utils.mklegend(x1=0.55, y1=0.65, x2=0.9, y2=0.9)
                    legend.SetTextSize(0.035)
                    legend.SetHeader("%s tracks (%s)" % (category, phase))
                    
                    label = tmva_folder.split("tracks-")[1]
                    
                    fin = TFile("%s/output.root" % tmva_folder)
                    
                    try:
                        temp = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_effS")
                        temp.SetTitle('')
                    except:
                        print "ignoring", tmva_folder
                        continue
                    
                    if plot_efficiencies:
                        h_S = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_effS")
                        h_B = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_effB")
                        h_Train_S = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_trainingEffS")
                        h_Train_B = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_trainingEffB")
                        
                        #bgeff = h_B.GetBinContent(h_B.GetXaxis().FindBin(bdtcut))
                        bgeff = 0.0725901899158 #2017-short-tracks-aug21v4-baseline
                        #print "bgeff", bgeff
                        
                        for iBin in range(h_B.GetNbinsX()):
                            yval = h_B.GetBinContent(iBin)
                            xval = h_B.GetXaxis().GetBinCenter(iBin)
                            if xval > -0.1 and yval <= bgeff:
                                print tmva_folder, xval
                                bg_efficiencies[tmva_folder] = xval
                                break
                        
                    else:
                        h_S = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_S")
                        h_B = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_B")
                        h_Train_S = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_Train_S")
                        h_Train_B = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_Train_B")
                                            
                    h_S.SetTitle('')
                    h_B.SetTitle('')
                    h_Train_S.SetTitle('')
                    h_Train_B.SetTitle('')
                    h_S.GetYaxis().SetTitle('(1/N) dN / dx')
                    h_S.GetXaxis().SetTitle('BDT output')
                    shared_utils.histoStyler(h_S)
                    shared_utils.histoStyler(h_B)
                    shared_utils.histoStyler(h_Train_S)
                    shared_utils.histoStyler(h_Train_B)
                    
                    h_S.SetLineColor(kBlue)
                    h_S.SetFillColorAlpha(kBlue, 0.6)
                    h_B.SetLineColor(kRed)
                    h_B.SetFillColorAlpha(kRed, 0.6)
                    h_Train_S.SetMarkerStyle(20)
                    h_Train_B.SetMarkerStyle(20)
                    h_Train_S.SetMarkerColor(kBlue)
                    h_Train_B.SetMarkerColor(kRed)
                    h_Train_S.SetLineColor(kBlue)
                    h_Train_B.SetLineColor(kRed)

                    legend.AddEntry(h_S, "Signal (testing)")
                    legend.AddEntry(h_B, "Background (testing)")
                    legend.AddEntry(h_Train_S, "Signal (training)")
                    legend.AddEntry(h_Train_B, "Background (training)")
                    
                    h_S.Draw("hist")
                    h_S.GetXaxis().SetRangeUser(-1, 1)
                    if plot_efficiencies:
                        h_S.GetYaxis().SetRangeUser(0, 1)
                    else:
                        h_S.GetYaxis().SetRangeUser(0, 10)
                    h_B.Draw("hist same")
                    h_Train_S.Draw("p same")
                    h_Train_B.Draw("p same")
                    
                    legend.Draw()
                    shared_utils.stamp(showlumi=False)
                    if plot_efficiencies:
                        extralabel2 = "_eff"
                    else:
                        extralabel2 = ""
                    canvas.SaveAs("plots/output_%s_%s_%s%s%s.pdf" % (label, category, phase, extralabel, extralabel2))
                    fin.Close()

    print bg_efficiencies
