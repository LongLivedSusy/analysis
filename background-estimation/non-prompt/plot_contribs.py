#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *
import collections
from shared_utils import *

def plot(variable, xlabel, signalfile="/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Signal/T1qqqqLL/Glu2000_Chi1ne1500.root", promptfile = "/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Background/prompt-bg-results.root", fakefile = "/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Background/fake-bg-results.root", suffix = ""):

    os.system("hadd -f bg-predictions.root %s %s %s" % (promptfile, fakefile, signalfile) )
    fin = TFile("bg-predictions.root", "read")

    hist_names = []  
    histos = collections.OrderedDict()

    histos["hFkBaseline"] = fin.Get("hFkBaseline_%s" % variable)    
    histos["hElBaseline"] = fin.Get("hElBaseline_%s" % variable)
    histos["hMuBaseline"] = fin.Get("hMuBaseline_%s" % variable)
    histos["hPiBaseline"] = fin.Get("hPiBaseline_%s" % variable)
    
    if signalfile:
        histos["hBaselineTruth"] = fin.Get("hBaseline_%s" % variable.replace("Method", "Truth"))
        signallabel = signalfile.split("/")[-1].replace(".root", "")
    else:
        signallabel = ""

    colors = [kBlack, kRed, kBlue, kGreen, kOrange, kAzure, kMagenta, kYellow, kTeal]
    for label in histos:
        color = colors.pop(0)
        histos[label].SetLineColor(color)
        histos[label].SetFillColor(0)
        histos[label].SetLineWidth(2)
        histos[label].SetTitle(";%s;Events" % xlabel)
        #histos[label].SetMarkerSize(0)
        histos[label].SetMarkerColor(color)
        histos[label].GetXaxis().SetRangeUser(1,89)
        
    canvas = TCanvas("prediction", "prediction", 1500, 800)  
    canvas.SetLeftMargin(0.08)
    canvas.SetRightMargin(0.05)
    canvas.SetLogy(True)
    
    legend = TLegend(0.15, 0.75, 0.5, 0.88)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)

    for i, label in enumerate(histos):

        if i == 0:
            histos[label].Draw("hist e")
            histos[label].GetYaxis().SetRangeUser(1e-4,1e4)
        else:
            histos[label].Draw("hist e same")

        desc = label
        desc = desc.replace("hFkBaseline", "fake tracks")
        desc = desc.replace("hElBaseline", "prompt electrons")
        desc = desc.replace("hMuBaseline", "prompt muons")
        desc = desc.replace("hPiBaseline", "prompt pions")
        desc = desc.replace("hBaselineTruth", "signal (m_gluino=%s GeV, m_LSP=%s GeV)" % (signallabel.split("_")[0].replace("Glu", ""), signallabel.split("Chi1ne")[1])  )
        legend.AddEntry(histos[label], desc)

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)
    latex.SetTextAlign(13)
    latex.SetTextFont(52)
           
    legend.Draw()

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)

    latex.DrawLatex(0.95, 0.91, "%.1f fb^{-1} (13 TeV)" % 36.0)

    latex.SetTextSize(0.03)
    latex.SetTextFont(52)
    latex.DrawLatex(0.24, 0.91, "CMS Work in Progress")

    lines = {}
    def drawlines(xbins, lines):

        xmin = 1
        xmax = 89
        ndc_xmin = 0.15
        ndc_xmax = 0.90

        for xbin in xbins:

            xbin_loweredge = int(xbin.split("-")[0])
            xbin_upperedge = int(xbin.split("-")[1])

            # draw some lines:
            lines[xbin_upperedge] = TLine(xbin_upperedge, 1e-4, xbin_upperedge, 1e4)
            lines[xbin_upperedge].SetLineWidth(2)
            lines[xbin_upperedge].Draw("same")
            
            # draw region labels:
            ndc_pos = xbin_loweredge + (xbin_upperedge - xbin_loweredge) / 2.0
            print ndc_pos
            ndc_pos = ndc_pos/(xmax - xmin)
            print ndc_pos
            ndc_pos = ndc_xmin + (ndc_xmax - ndc_xmin) * ndc_pos
            print ndc_pos
            
            latex.SetTextFont(22)
            #latex.DrawLatex(ndc_pos, 0.7, xbins[xbin])    
            
    xbins = {
              "0-20":  "MHT<300 GeV",
              "20-33": "MHT>300 GeV",
              "33-41": "HT<1000 GeV",
              "41-49": "HT>1000 GeV",
              "49-57": "DT+mu",
              "57-65": "DT+mu, btags>0",
              "65-72": "DT+el",
              "73-80": "DT+el, btags>0",
              "81-89": "multiple DT",
            }
        
    drawlines(xbins, lines)
    
    #stamp_plot()
    #canvas.SetTitle("fakerate-%s-%s-%s-%s" % (variable, category, tag, period) )    
    canvas.SaveAs("contribs_piano_%s%s_%s.pdf" % (variable, suffix, signallabel))

    fin.Close()


def do_ratio():

    fin = TFile("closure_Run2016.root", "open")  
    h_with_zmass_matching = fin.Get("hFkBaseline_BinNumberMethod")
    h_with_zmass_matching.SetTitle("h_with_zmass_matching")
    h_with_zmass_matching.SetDirectory(0)
    fin.Close()

    fin = TFile("/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/v2/Background/fake-bg-results.root", "open")
    h_without_zmass_matching = fin.Get("hFkBaseline_BinNumberMethod")
    h_without_zmass_matching.SetTitle("h_without_zmass_matching")
    h_without_zmass_matching.SetDirectory(0)
    h_without_zmass_matching.SetLineColor(kRed)
    fin.Close()

    histoStyler(h_with_zmass_matching)
    histoStyler(h_without_zmass_matching)

    h_with_zmass_matching.SetLineColor(kRed)
    h_without_zmass_matching.SetLineColor(kBlue)

    c1 = mkcanvas("c1")
    leg = mklegend(x1=.7, y1=.6, x2=.92, y2=.8, color=kWhite)

    #hData = h_with_zmass_matching
    hData = TH1D("data", "data", 88, 0, 88)
    hmcs = [h_with_zmass_matching, h_without_zmass_matching]

    hratio = FabDraw(c1,leg,hData,hmcs,datamc='MC',lumi=34.6, title = '', LinearScale=False, fractionthing='truth / method')

    #hratio.GetYaxis().SetRangeUser(-0.1,2.6)
    #hratio.GetYaxis().SetTitle('Events/bin')
    #hratio.GetXaxis().SetTitle("Search bin")
    #hratio.SetLineColor(kBlack)

    #for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
    #    if hratio.GetBinContent(ibin)==0:
    #        hratio.SetBinContent(ibin,-999)
    #hratio.SetMarkerColor(kBlack)
    #hratio.SetDirectory(0)

    c1.cd(2)
    c1.SetLogy()
    c1.Update()
    c1.cd(1)
    #hMC.SetTitle('')
    #hMC.Draw('same p')

    c1.Update()
    #fnew.cd()
    #c1.Write()
    c1.SaveAs("ratio.pdf")

    #c1.Divide(1,2,0,0)
    #c1.cd(1)
    #c1.SetLogy(True)
    #h_with_zmass_matching.Draw("hist")
    #h_without_zmass_matching.Draw("same hist")

    #c1.cd(2)

    #ratio = h_with_zmass_matching.Clone()
    #ratio.Divide(h_without_zmass_matching)
    #ratio.Draw()
    
    #c1.SaveAs("ratio.root")


#do_ratio()

for variable in ["BinNumber"]: #["DeDxAverage", "Ht", "Log10DedxMass", "Mht", "NJets"]
    plot(variable + "Method", "search bin")

