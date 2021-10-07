#!/usr/bin/env python
from ROOT import *
from math import sqrt
from array import array
import shared_utils

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

tmva_folders = [
                #"aug21v3-baseline",
                #"aug21v3-noDeltaPt",
                #"aug21v3-noPixelHits",
                #"aug21v3-noPixelHits-noDeltaPt",
                "jul21-noDeltaPt",
               ]

extralabel = "commited"

# ROC plot:

histos = {}

for category in ["short", "long"]:
        
    canvas = shared_utils.mkcanvas("c1")
    legend = shared_utils.mklegend(x1=.17, y1=.17, x2=.6, y2=.6)
    legend.SetTextSize(0.035)
    
    drawhists = []

    for i_phase, phase in enumerate(["2016", "2017"]):

        #colors = range(209,270)
        #colors = [kBlack, kBlue, kBlue-3, kBlue-9, kCyan, kCyan-3, kGreen, kGreen-3, kOrange, kRed, kPink, kMagenta, kMagenta-3]
        colors = [kAzure, kOrange,  kCyan, kGreen-3, kRed, kMagenta, kRed-9, kAzure+2]
        
        color = 0
        dicke = len(tmva_folders)+1
        
        for i_tmva_folder, tmva_folder in enumerate(sorted(tmva_folders)):
            
            tmva_folder = "%s-%s-tracks-%s" % (phase, category, tmva_folder)
            
            #if phase in tmva_folder and category in tmva_folder:
                
            print tmva_folder
            fin = TFile("%s/output.root" % tmva_folder)
            histos[tmva_folder] = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_rejBvsS")
            histos[tmva_folder].SetDirectory(0)
            histos[tmva_folder].SetName(tmva_folder)
            histos[tmva_folder].SetTitle('')
            histos[tmva_folder].GetYaxis().SetTitle('Background rejection')
            histos[tmva_folder].GetXaxis().SetTitle('Signal efficiency')
            histos[tmva_folder].GetXaxis().SetRangeUser(0.5, 1)
            histos[tmva_folder].GetYaxis().SetRangeUser(0.5, 1)
            
            shared_utils.histoStyler(histos[tmva_folder])
            
            #if "noEdep" in tmva_folder:
            #    histos[tmva_folder].SetLineWidth(3)
            #    #histos[tmva_folder].SetLineColor(color)
            #elif "equSgXsec" in tmva_folder:
            #    histos[tmva_folder].SetLineStyle(3)
            #elif "noveto" in tmva_folder:
            #    histos[tmva_folder].SetLineStyle(2)
            #elif "may21v2" in tmva_folder:
            #    color = colors.pop(0)
            #else:
            color = colors.pop(0)
            histos[tmva_folder].SetLineColor(color)
            
            fin.Close()
            
            label = tmva_folder.replace("-", " ")
            #label = label.replace("may21 equSgXsec3", ", with equal sg. xsections")
            #label = label.replace("may21v2", ", without no. of pixel hits")
            #label = label.replace("may21", ", xsection-weighted signal")
            
            #if "may21v2" in label:
            #    label = "removed pixel hits in training"
            #elif "may21" in label:
            #    label = "pixel hits in training"
            
            #if "noPixelHits-noDeltaPt" in tmva_folder:
            #    histos[tmva_folder].SetLineStyle(2)

            #if "useLayers" in tmva_folder:
            #    histos[tmva_folder].SetLineStyle(2)                

            #if "no" in tmva_folder:
            #    histos[tmva_folder].SetLineStyle(2)                
            #
            #    if "aug21" in tmva_folder:
            #        histos[tmva_folder].SetLineStyle(3)                
            #
            #
            #if "aug21v2" in tmva_folder:
            #    histos[tmva_folder].SetLineStyle(3)                

            #if "noPixel" in tmva_folder:
            #    histos[tmva_folder].SetLineStyle(3)                

            histos[tmva_folder].SetLineStyle(i_phase + 1)
            histos[tmva_folder].SetLineWidth(dicke - i_tmva_folder)
            
            legend.AddEntry(histos[tmva_folder], label.replace("%s tracks " % category, ""))
            legend.SetHeader("%s tracks" % category)

            drawhists.append(tmva_folder)
        
        for i, label in enumerate(drawhists):
            if i == 0:
                histos[label].Draw("hist")
            else:
                histos[label].Draw("hist same")
        
    legend.Draw()
    shared_utils.stamp(showlumi=False)
    #canvas.SaveAs("ROC_%s_%s%s.pdf" % (phase, category, extralabel))
    canvas.SaveAs("ROC_%s%s.pdf" % (category, extralabel))


# BDT output:

for phase in ["2016", "2017"]:
    for category in ["short", "long"]:
        for tmva_folder in sorted(tmva_folders):
            if phase in tmva_folder and category in tmva_folder:

                canvas = shared_utils.mkcanvas("c1")
                legend = shared_utils.mklegend(x1=0.55, y1=0.65, x2=0.9, y2=0.9)
                legend.SetTextSize(0.035)
                legend.SetHeader("%s tracks (%s)" % (category, phase))
                
                label = tmva_folder.split("tracks-")[1]
                
                fin = TFile("%s/output.root" % tmva_folder)

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
                #h_Train_S.SetLineStyle(2)
                #h_Train_B.SetLineStyle(2)
                
                legend.AddEntry(h_S, "Signal (testing)")
                legend.AddEntry(h_B, "Background (testing)")
                legend.AddEntry(h_Train_S, "Signal (training)")
                legend.AddEntry(h_Train_B, "Background (training)")
        
                h_S.Draw("hist")
                h_S.GetXaxis().SetRangeUser(-1, 1)
                h_S.GetYaxis().SetRangeUser(0, 10)
                h_B.Draw("hist same")
                h_Train_S.Draw("p same")
                h_Train_B.Draw("p same")
        
                legend.Draw()
                shared_utils.stamp(showlumi=False)
                canvas.SaveAs("output_%s_%s_%s%s.pdf" % (label, category, phase, extralabel))
                fin.Close()
