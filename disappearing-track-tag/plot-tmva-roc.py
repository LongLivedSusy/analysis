#!/usr/bin/env python
from ROOT import *
from math import sqrt
from array import array
import shared_utils

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

tmva_folders = [
        #"2017-short-tracks-may21",
        #"2017-long-tracks-may21",
        #"2016-short-tracks-may21",
        #"2016-long-tracks-may21",
        #"2016-long-tracks-may21-equSgXsec",
        #"2016-short-tracks-may21-equSgXsec",
        #"2017-long-tracks-may21-equSgXsec",
        #"2017-short-tracks-may21-equSgXsec",
        #"2016-long-tracks-may21-equSgXsec2",
        #"2016-short-tracks-may21-equSgXsec2",
        #"2017-long-tracks-may21-equSgXsec2",
        #"2017-short-tracks-may21-equSgXsec2",
        #"2016-long-tracks-nov20-noEdep",
        #"2016-short-tracks-nov20-noEdep",
        #"2017-long-tracks-nov20-noEdep",
        #"2017-short-tracks-nov20-noEdep",
        #"2016-long-tracks-may21-equSgXsec3",
        #"2016-short-tracks-may21-equSgXsec3",
        #"2017-long-tracks-may21-equSgXsec3",
        #"2017-short-tracks-may21-equSgXsec3",
        #"2017-short-tracks-may21v2",
        #"2016-short-tracks-may21v2",
        #"2017-short-tracks-may21v2",
        #"2016-short-tracks-may21v2",
        #"2017-long-tracks-may21-equSgXsec3",
        #"2017-short-tracks-may21-equSgXsec3",
        #"2016-long-tracks-may21-noveto",
        #"2016-short-tracks-may21-noveto",
        #"2017-long-tracks-may21-noveto",
        #"2017-short-tracks-may21-noveto",
        "2016-long-tracks-sgtest-boosted",
        "2016-long-tracks-sgtest-compressed",
        "2016-long-tracks-sgtest-corner",
        "2016-long-tracks-sgtest-inverted",
        "2016-short-tracks-sgtest-boosted",
        "2016-short-tracks-sgtest-compressed",
        "2016-short-tracks-sgtest-corner",
        "2016-short-tracks-sgtest-inverted",
        "2017-long-tracks-sgtest-boosted",
        "2017-long-tracks-sgtest-compressed",
        "2017-long-tracks-sgtest-corner",
        "2017-long-tracks-sgtest-inverted",
        "2017-short-tracks-sgtest-boosted",
        "2017-short-tracks-sgtest-compressed",
        "2017-short-tracks-sgtest-corner",
        "2017-short-tracks-sgtest-inverted",
]


# ROC plot:

histos = {}

#colors = [kBlack, kBlue, kBlue-3, kBlue-9, kCyan, kCyan-3, kGreen, kGreen-3, kOrange, kRed, kPink, kMagenta, kMagenta-3]
#colors = [kAzure, kCyan, kGreen-3, kOrange, kRed, kMagenta, kRed-9, kAzure+2]
colors = range(209,270)

canvas = shared_utils.mkcanvas("c1")
legend = shared_utils.mklegend(x1=.17, y1=.17, x2=.6, y2=.6)
legend.SetTextSize(0.035)

color = 0

for tmva_folder in sorted(tmva_folders):
    print tmva_folder
    fin = TFile("%s/output.root" % tmva_folder)
    histos[tmva_folder] = fin.Get("dataset/Method_BDT/BDT/MVA_BDT_rejBvsS")
    histos[tmva_folder].SetDirectory(0)
    histos[tmva_folder].SetName(tmva_folder)
    histos[tmva_folder].SetTitle('')
    histos[tmva_folder].GetYaxis().SetTitle('Background rejection')
    histos[tmva_folder].GetXaxis().SetTitle('Signal efficiency')
    shared_utils.histoStyler(histos[tmva_folder])
    
    if "noEdep" in tmva_folder:
        histos[tmva_folder].SetLineWidth(3)
        #histos[tmva_folder].SetLineColor(color)
    elif "equSgXsec" in tmva_folder:
        histos[tmva_folder].SetLineStyle(3)
    elif "noveto" in tmva_folder:
        histos[tmva_folder].SetLineStyle(2)
    elif "may21v2" in tmva_folder:
        color = colors.pop(0)
    else:
        color = colors.pop(0)
    histos[tmva_folder].SetLineColor(color)
    
    fin.Close()
    
    label = tmva_folder.replace("-", " ")
    label = label.replace("may21 equSgXsec3", ", with equal sg. xsections")
    label = label.replace("may21v2", ", without no. of pixel hits")
    label = label.replace("may21", ", xsection-weighted signal")
    legend.AddEntry(histos[tmva_folder], label)

for i, label in enumerate(histos):
    if i == 0:
        histos[label].Draw("hist")
    else:
        histos[label].Draw("hist same")

legend.Draw()
shared_utils.stamp(showlumi=False)
canvas.SaveAs("ROC.pdf")

quit()

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
                canvas.SaveAs("output_%s_%s_%s.pdf" % (label, category, phase))
                fin.Close()
