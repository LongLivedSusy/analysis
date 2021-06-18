#!/usr/bin/env python
from ROOT import *
from math import sqrt
from array import array
import shared_utils
import glob

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

tmva_folders = glob.glob("optimize-*/output.root")
rocarea = {}
ks_signal = {}
ks_background = {}

for phase in ["2016", "2017"]:
    for category in ["short", "long"]:

        histos = {}
        colors = range(209,270)

        canvas = shared_utils.mkcanvas("c1")
        legend = shared_utils.mklegend(x1=.17, y1=.17, x2=.75, y2=.6)
        legend.SetTextSize(0.035)
        
        rocarea["%s, %s tracks" % (phase, category)] = TH1F("rocarea", ";depth, number of trees;area under ROC", 55, 0, 55)
        ks_signal["%s, %s tracks" % (phase, category)] = TH1F("ks_signal", ";depth, number of trees;KS test (signal)", 55, 0, 55)
        ks_background["%s, %s tracks" % (phase, category)] = TH1F("ks_background", ";depth, number of trees;KS test (background)", 55, 0, 55)
        shared_utils.histoStyler(rocarea["%s, %s tracks" % (phase, category)])
        shared_utils.histoStyler(ks_signal["%s, %s tracks" % (phase, category)])
        shared_utils.histoStyler(ks_background["%s, %s tracks" % (phase, category)])
        
        binLabels = {}
        iBin = 1
        for tmva_folder in sorted(tmva_folders):
            if phase in tmva_folder and category in tmva_folder:
                iBin += 1                
                fin = TFile(tmva_folder)
                histos[tmva_folder] = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_rejBvsS")
                histos[tmva_folder].SetDirectory(0)
                histos[tmva_folder].SetName(tmva_folder)
                histos[tmva_folder].SetTitle('')
                histos[tmva_folder].GetYaxis().SetTitle('Background rejection')
                histos[tmva_folder].GetXaxis().SetTitle('Signal efficiency')
                shared_utils.histoStyler(histos[tmva_folder])
                color = colors.pop(0)
                histos[tmva_folder].SetLineColor(color)
                
                # get KS score:
                # TMVA uses X parameter to calculate KS score (the pseudo experiment option)
                # https://root-forum.cern.ch/t/kolmogorov-test-on-two-histograms-with-the-x-option/16984/2
                h_test_S = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_S")
                h_train_S = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_Train_S")
                ks_score_signal = h_test_S.KolmogorovTest(h_train_S, "X")
                ks_signal["%s, %s tracks" % (phase, category)].SetBinContent(iBin, ks_score_signal)
                
                # get KS score:
                # TMVA uses X parameter to calculate KS score (the pseudo experiment option)
                # https://root-forum.cern.ch/t/kolmogorov-test-on-two-histograms-with-the-x-option/16984/2
                h_test_B = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_B")
                h_train_B = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_Train_B")
                ks_score_background = h_test_B.KolmogorovTest(h_train_B, "X")
                ks_background["%s, %s tracks" % (phase, category)].SetBinContent(iBin, ks_score_background)
                    
                fin.Close()
                ntrees = tmva_folder.split("ntrees")[1].split("/")[0]
                ndepth = tmva_folder.split("ndepth")[1].split("-")[0]                
                legend.AddEntry(histos[tmva_folder], "depth=%s, %s trees" % (ndepth, ntrees))
                area_under_curve = histos[tmva_folder].Integral() / 100.0
                rocarea["%s, %s tracks" % (phase, category)].SetBinContent(iBin, area_under_curve)
                binLabels[iBin] = "%s, %s" % (ndepth, ntrees)
                
                
        
        for i, label in enumerate(histos):
            if i == 0:
                histos[label].Draw("hist")
            else:
                histos[label].Draw("hist same")
        
        legend.Draw()
        shared_utils.stamp(showlumi=False)
        canvas.SaveAs("optimize_%s_%s.pdf" % (phase, category))


# ROC plot:
canvas = shared_utils.mkcanvas("c1")
colors = [kBlue, kRed, kOrange, kMagenta]
legend = shared_utils.mklegend(x1=.2, y1=.2, x2=.5, y2=.4)
legend.SetTextSize(0.035)

for i, label in enumerate(rocarea):
    if i == 0:
        rocarea[label].Draw("hist")
    else:
        rocarea[label].Draw("hist same")

    rocarea[label].GetYaxis().SetRangeUser(0.85, 1)
    rocarea[label].GetXaxis().SetLabelSize(0.03)
    rocarea[label].SetLineColor(colors.pop(0))
    legend.AddEntry(rocarea[label], label)
    for i in binLabels:
        rocarea[label].GetXaxis().SetBinLabel(i, binLabels[i])
    
legend.Draw()
shared_utils.stamp(showlumi=False)
canvas.SaveAs("rocarea.pdf")


# KS signal plot:
for i_histo, ks_histo in enumerate([ks_signal, ks_background]):

    canvas = shared_utils.mkcanvas("c1")
    colors = [kBlue, kRed, kOrange, kMagenta]
    legend = shared_utils.mklegend(x1=.2, y1=.2, x2=.5, y2=.4)
    legend.SetTextSize(0.035)
    
    for i, label in enumerate(ks_histo):
        if i == 0:
            ks_histo[label].Draw("hist")
        else:
            ks_histo[label].Draw("hist same")
    
        ks_histo[label].GetYaxis().SetRangeUser(0, 1)
        ks_histo[label].GetXaxis().SetLabelSize(0.03)
        ks_histo[label].SetLineColor(colors.pop(0))
        legend.AddEntry(ks_histo[label], label)
        for i in binLabels:
            ks_histo[label].GetXaxis().SetBinLabel(i, binLabels[i])
        
    legend.Draw()
    shared_utils.stamp(showlumi=False)
    canvas.SaveAs("ks_test_%s.pdf" % i_histo)
