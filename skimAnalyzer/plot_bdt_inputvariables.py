#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import os
import collections
import shared_utils
import glob
import multiprocessing
import copy

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()
tl = TLatex()
tl.SetNDC()
cmsTextFont = 61
extraTextFont = 50
lumiTextSize = 0.6
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffset = 0.1
regularfont = 42
originalfont = tl.GetTextFont()
epsi = "#scale[1.3]{#font[122]{e}}"
epsilon = 0.0001

datamc = 'Data'
def stamp(lumi='35.9', showlumi = False, WorkInProgress = True):
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(0.98*tl.GetTextSize())
    tl.DrawLatex(0.15,0.845, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(1.0/0.98*tl.GetTextSize())
    xlab = 0.235
    if WorkInProgress: tl.DrawLatex(xlab,0.845, ' Work in Progress')
    else: tl.DrawLatex(xlab,0.845, ('MC' in datamc)*' simulation '+'preliminary')
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
    xthing = 0.57
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing-0.02,0.845,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())


def stamp2(lumi,datamc='MC'):
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(1.6*tl.GetTextSize())
	tl.DrawLatex(0.152,0.82, 'CMS')
	tl.SetTextFont(extraTextFont)
	tl.DrawLatex(0.14,0.74, ('MC' in datamc)*' simulation'+' internal')
	tl.SetTextFont(regularfont)
	if lumi=='': tl.DrawLatex(0.62,0.82,'#sqrt{s} = 13 TeV')
	else: tl.DrawLatex(0.47,0.82,'#sqrt{s} = 13 TeV, L = '+str(lumi)+' fb^{-1}')
	#tl.DrawLatex(0.64,0.82,'#sqrt{s} = 13 TeV')#, L = '+str(lumi)+' fb^{-1}')	
	tl.SetTextSize(tl.GetTextSize()/1.6)


def FabDraw(cGold,leg,hTruth,hComponents,datamc='MC',lumi=35.9, title = '', ytitle = False, LinearScale=False, fractionthing='(bkg-obs)/obs'):
    print 'datamc in FabDraw'
    cGold.cd()
    pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
    pad1.SetBottomMargin(0.0)
    pad1.SetLeftMargin(0.12)
    if not LinearScale:
        pad1.SetLogy()

    pad1.SetGridx()
    #pad1.SetGridy()
    pad1.Draw()
    pad1.cd()
    for ih in range(1,len(hComponents[1:])+1):
        hComponents[ih].Add(hComponents[ih-1])
    hComponents.reverse()        
    if ytitle:
        hComponents[0].GetYaxis().SetTitle(ytitle)
    elif abs(hComponents[0].Integral(-1,999)-1)<0.001:
        hComponents[0].GetYaxis().SetTitle('Normalized')
    else: hComponents[0].GetYaxis().SetTitle('Events/bin')
    cGold.Update()
    hTruth.GetYaxis().SetTitle('Normalized')
    hTruth.GetYaxis().SetTitleOffset(1.15)
    hTruth.SetMarkerStyle(20)
    histheight = 1.5*max(hComponents[0].GetMaximum(),hTruth.GetMaximum())
    if LinearScale: low, high = 0, histheight
    else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hTruth.GetMinimum())), 1000*histheight

    title0 = hTruth.GetTitle()
    if datamc=='MC':
        for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
        leg.AddEntry(hTruth,hTruth.GetTitle(),'lpf')        
    else:
        for ihComp, hComp in enumerate(hComponents):
            leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
        leg.AddEntry(hTruth,title0,'lp')    
    hTruth.SetTitle('')
    hComponents[0].SetTitle('')
    if LinearScale: hComponents[0].GetYaxis().SetRangeUser(0, 1.5*hTruth.GetMaximum())
    else: hComponents[0].GetYaxis().SetRangeUser(0.001, 100*hTruth.GetMaximum())
    hComponents[0].Draw('hist')

    for h in hComponents[1:]: 
        h.Draw('hist same')
        cGold.Update()
        print 'updating stack', h
    hComponents[0].Draw('same') 
    hTruth.Draw('p same')
    hTruth.Draw('e same')    
    cGold.Update()
    hComponents[0].Draw('axis same')           
    leg.Draw()        
    cGold.Update()
    stamp2(lumi,datamc)
    cGold.Update()
    cGold.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.3)
    pad2.SetLeftMargin(0.12)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    hTruthCopy = hTruth.Clone('hTruthClone'+hComponents[0].GetName())
    hRatio = hTruthCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
    hRatio.SetMarkerStyle(20)
    #hFracDiff = hComponents[0].Clone('hFracDiff')
    #hFracDiff.SetMarkerStyle(20)
    hTruthCopy.SetMarkerStyle(20)
    hTruthCopy.SetMarkerColor(1) 
    #histoStyler(hFracDiff, 1)
    shared_utils.histoStyler(hTruthCopy, 1)
    #hFracDiff.Add(hTruthCopy,-1)
    #hFracDiff.Divide(hTruthCopy)
    #hRatio.Divide(hTruthCopy)
    hRatio.Divide(hComponents[0])
    hRatio.GetYaxis().SetRangeUser(0.0,.1)###
    hRatio.SetTitle('')
    if 'prediction' in title0: hRatio.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
    else: hRatio.GetYaxis().SetTitle(fractionthing)
    hRatio.GetXaxis().SetTitleSize(0.12)
    hRatio.GetXaxis().SetLabelSize(0.11)
    hRatio.GetYaxis().SetTitleSize(0.12)
    hRatio.GetYaxis().SetLabelSize(0.12)
    hRatio.GetYaxis().SetNdivisions(5)
    hRatio.GetXaxis().SetNdivisions(10)
    hRatio.GetYaxis().SetTitleOffset(0.5)
    hRatio.GetXaxis().SetTitleOffset(1.0)
    hRatio.GetXaxis().SetTitle(hTruth.GetXaxis().GetTitle())
    hRatio.Draw()
    hRatio.Draw('e0')    
    pad1.cd()
    hComponents.reverse()
    hTruth.SetTitle(title0)
    return hRatio, [pad1, pad2]


def FabDrawNoRatio(cGold,leg,hTruth,hComponents,datamc='MC',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
    cGold.cd()
    cGold.SetLogy(True)
    cGold.SetGridx()
    for ih in range(1,len(hComponents[1:])+1):
        hComponents[ih].Add(hComponents[ih-1])
    hComponents.reverse()        
    if abs(hComponents[0].Integral(-1,999)-1)<0.001:
        hComponents[0].GetYaxis().SetTitle('Normalized')
    else: hComponents[0].GetYaxis().SetTitle('Events/bin')
    cGold.Update()
    hTruth.GetYaxis().SetTitle('Normalized')
    hTruth.GetYaxis().SetTitleOffset(1.15)
    hTruth.SetMarkerStyle(20)
    histheight = 1.5*max(hComponents[0].GetMaximum(),hTruth.GetMaximum())
    if LinearScale: low, high = 0, histheight
    else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hTruth.GetMinimum())), 1000*histheight
    
    title0 = hTruth.GetTitle()
    hTruth.SetTitle('')
    if datamc=='MC':
        for hcomp in hComponents:
            leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
        #leg.AddEntry(hTruth,hTruth.GetTitle(),'lpf')        
    else:
        for ihComp, hComp in enumerate(hComponents):
            leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
        #leg.AddEntry(hTruth,title0,'lp')    
    hComponents[0].GetYaxis().SetRangeUser(10, 10*hTruth.GetMaximum())
    hComponents[0].Draw('hist')

    for h in hComponents[1:]: 
        h.Draw('hist same')
        cGold.Update()
        print 'updating stack', h
    hComponents[0].Draw('same') 
    hTruth.Draw('p same')
    hTruth.Draw('e same')    
    cGold.Update()
    hComponents[0].Draw('axis same')           
    leg.Draw()        
    cGold.Update()
    stamp(lumi,datamc)
    cGold.Update()
    cGold.cd()
    hComponents[0].SetTitle(";%s;Events/bin" % title)
    #hComponents[0].GetXaxis().SetTitleSize(0.12)
    #hComponents[0].GetXaxis().SetLabelSize(0.11)
    hComponents[0].GetXaxis().SetNdivisions(10)
    #hComponents[0].GetXaxis().SetTitleOffset(1.0)


def do_plots(variable, cutstring, thisbatchname, folder, labels, binnings, signalscaling, normalize, LinearScale, includeData, lumi, ymin, ymax, ignore = [], unweighted = False):

    # get histograms:
    histos = collections.OrderedDict()
    for label in labels:

        if label in ignore: continue

        if isinstance(cutstring, list):
            if ("Signal" in label or "SMS" in label):
                thiscutstring = cutstring[1] + " && " + labels[label][2]
            elif "Background" in label and "WP" in label:
                thiscutstring = cutstring[0] + " && " + labels[label][2]
            elif "Data" in label and len(labels[label])>2:
                thiscutstring = cutstring[0] + " && " + labels[label][2]
            else:
                thiscutstring = cutstring[0]
        else:
            if "Signal" in label or "SMS" in label:
                thiscutstring = cutstring + " && " + labels[label][2]
            elif "Background" in label and len(labels[label])>2:
                thiscutstring = cutstring + " && " + labels[label][2]
            elif "Data" in label and len(labels[label])>2:
                thiscutstring = cutstring + " && " + labels[label][2]
            else:
                thiscutstring = cutstring

        globstrings = labels[label][0]
        color = labels[label][1]
        histos[label] = 0

        for globstring in globstrings:
            input_files = glob.glob(folder + "/" + globstring + "*root")
            if len(input_files) == 0: continue
            currenthisto = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=thiscutstring, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2], unweighted=unweighted)
            shared_utils.histoStyler(currenthisto)
            if histos[label] == 0:
                histos[label] = currenthisto.Clone()
                histos[label].SetDirectory(0)
            else:
                histos[label].Add(currenthisto.Clone())

        histos[label].SetTitle(label)
        if "Data" in label or "Signal" in label or "WP" in label:
            histos[label].SetLineColor(color)
            histos[label].SetFillColorAlpha(0, 0)
        else:
            histos[label].SetFillColor(color)
            
    # prepare:
    contains_data = False
    for label in histos.keys():
        if "Data" in label:
            contains_data = True
        else:
            histos[label].Scale(lumi)

        if "Signal" in label:
            histos[label].SetLineWidth(2)
            histos[label].Scale(signalscaling)
        elif "WP" in label:
            histos[label].SetLineWidth(2)
        else:
            histos[label].SetLineWidth(0)
    
    if contains_data and includeData:
        histolist = [histos[histos.keys()[0]]]
    else:
        histolist = []
    
    h_bgadded = 0
    histolistbg = []
    for label in sorted(histos):
        if not "Data" in label and not "Signal" in label and not "WP" in label:
            histolistbg.append(histos[label])
            if not h_bgadded:
                h_bgadded = histos[label].Clone()
            else:
                h_bgadded.Add(histos[label])
    histolistbg = sorted(histolistbg, key=lambda item: item.Integral())
    histolist += histolistbg
    
    # draw canvas:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1 = 0.55, y1 = 0.5, x2 = 0.88, y2 = 0.8)
    #legend.SetTextSize(0.04)
    canvas.SetFillColorAlpha(0,0)    
          
    lumi = float("%.2f" % (lumi/1e3))

    if contains_data and includeData:
        if normalize:
            htruth = histos[histos.keys()[0]].Clone()
            haux = h_bgadded.Clone()
            haux.SetTitle("Added MC backgrounds")
            haux.SetFillColor(62)
            htruth.Scale(1.0/htruth.Integral())
            haux.Scale(1.0/haux.Integral())
            htruth.SetLineColor(kBlack)
            htruth.SetLineWidth(1)
            htruth.SetLineStyle(1)
            hratio, pads = FabDraw(canvas, legend, htruth, [haux], lumi = lumi, datamc = 'Data', LinearScale=LinearScale, fractionthing = "Data/MC")
            htruth.SetLineColor(kBlack)
            htruth.SetLineWidth(1)
            htruth.SetLineStyle(1)
            hratio.GetYaxis().SetRangeUser(0, 2.5)
            htruth.GetYaxis().SetRangeUser(ymin, ymax)
            haux.GetYaxis().SetRangeUser(ymin, ymax)
        else:                       
            hratio, pads = shared_utils.FabDraw(canvas, legend, histolist[0], histolist[1:], lumi = lumi, LinearScale=LinearScale, datamc = 'Data')
    else:
        example = histos[histos.keys()[0]].Clone()
        empty_histo = TH1D("Data", "Data", example.GetXaxis().GetNbins(), example.GetXaxis().GetBinLowEdge(1), example.GetXaxis().GetBinLowEdge(example.GetXaxis().GetNbins()+1))
        shared_utils.histoStyler(empty_histo)
                
        FabDrawNoRatio(canvas, legend, empty_histo, histolist, title = binnings[3], lumi = lumi, datamc = 'MC', LinearScale=LinearScale)
        histolist[-1].SetTitle("")
        hratio = False

    for i_label, label in enumerate(histos):
        
        color = labels[label][1]
        
        histos[label].GetYaxis().SetRangeUser(ymin, ymax)
        if "Signal" in label:
            
            if variable == "tracks_invmass": continue
            
            if normalize and histos[label].Integral()>0:
                histos[label].Scale(1.0/histos[label].Integral())
            if "WP" in label or "BDT" in label:
                histos[label].SetLineStyle(2)
            
            legend.AddEntry(histos[label], histos[label].GetTitle())            
            histos[label].Draw("hist same")
        
        elif label == "Backgrounds (WP)":
            if normalize and histos[label].Integral()>0:
                histos[label].Scale(1.0/histos[label].Integral())
            legend.AddEntry(histos[label], "Added MC bg. (after BDT)")            
            histos[label].Draw("hist same")
            
            
        elif "Data" in label:
            histos[label].SetMarkerColor(color)
            histos[label].SetMarkerSize(1)
            histos[label].SetMarkerStyle(20)            
            histos[label].SetLineColor(color)
            histos[label].SetLineWidth(1)
            if normalize and histos[label].Integral()>0:
                histos[label].Scale(1.0/histos[label].Integral())
            if i_label > 0:
                histos[label].Draw("p same")
                histos[label].Draw("e same")
                if label == "Data (WP)":
                    legend.AddEntry(histos[label], "Data (after BDT)")
                else:
                    legend.AddEntry(histos[label], histos[label].GetTitle())
        
        #else:
        #    legend.AddEntry(histos[label], histos[label].GetTitle())
        
      
    if hratio:

        hratio.GetYaxis().SetRangeUser(0, 2)    
        hratio.GetYaxis().SetTitle('Data/MC')

        if len(binnings) == 4:
            hratio.GetXaxis().SetTitle(binnings[3])
        else:
            hratio.GetXaxis().SetTitle(str(variable))

        data_mc_after_bdt_available = 0
        for label in enumerate(histos):
            if "Data (WP)" in label:
                data_mc_after_bdt_available += 1
            if "Backgrounds (WP)" in label:
                data_mc_after_bdt_available += 1
        if data_mc_after_bdt_available == 2:
            pads[1].cd()
            h_ratio_after = histos["Data (WP)"].Clone()
            h_ratio_after.SetName("h_ratio_after")
            h_ratio_after.Divide(histos["Backgrounds (WP)"])
            h_ratio_after.SetLineColor(kMagenta)
            h_ratio_after.SetMarkerStyle(20)
            h_ratio_after.Draw("p same")
            

    #for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
    #    if hratio.GetBinContent(ibin)==0:
    #        hratio.SetBinContent(ibin,-999)
    #hratio.SetMarkerColor(kBlack)

    os.system("mkdir -p %s" % thisbatchname)
    pdfname = thisbatchname + "/" + variable.replace("/", "_") + ".pdf"
    
    if unweighted:
        pdfname = pdfname.replace(".pdf", "_unweighted.pdf")
    
    canvas.SaveAs(pdfname)
    

def do_eff_plots(variable, cutstring, thisbatchname, folder, labels, binnings, signalscaling, normalize, LinearScale, includeData, lumi, ymin, ymax, ignore = [], unweighted = False):

    # get histograms:
    histos = collections.OrderedDict()
    for label in labels:

        if label in ignore: continue

        if isinstance(cutstring, list):
            if ("Signal" in label or "SMS" in label):
                thiscutstring = cutstring[1] + " && " + labels[label][2]
            elif "Background" in label and "WP" in label:
                thiscutstring = cutstring[0] + " && " + labels[label][2]
            elif "Data" in label and len(labels[label])>2:
                thiscutstring = cutstring[0] + " && " + labels[label][2]
            else:
                thiscutstring = cutstring[0]
        else:
            if "Signal" in label or "SMS" in label:
                thiscutstring = cutstring + " && " + labels[label][2]
            elif "Background" in label and len(labels[label])>2:
                thiscutstring = cutstring + " && " + labels[label][2]
            elif "Data" in label and len(labels[label])>2:
                thiscutstring = cutstring + " && " + labels[label][2]
            else:
                thiscutstring = cutstring

        globstrings = labels[label][0]
        color = labels[label][1]
        histos[label] = 0

        for globstring in globstrings:
            input_files = glob.glob(folder + "/" + globstring + "*root")
            if len(input_files) == 0: continue
            currenthisto = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=thiscutstring, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2], unweighted=unweighted)
            shared_utils.histoStyler(currenthisto)
            if histos[label] == 0:
                histos[label] = currenthisto.Clone()
                histos[label].SetDirectory(0)
            else:
                histos[label].Add(currenthisto.Clone())

        histos[label].SetTitle(label)
        if "Data" in label or "Signal" in label or "WP" in label:
            histos[label].SetLineColor(color)
            histos[label].SetFillColorAlpha(0, 0)
        else:
            histos[label].SetFillColor(color)
            
    # prepare:
    contains_data = False
    for label in histos.keys():
        if "Data" in label:
            contains_data = True
        else:
            histos[label].Scale(lumi)

        if "Signal" in label:
            histos[label].SetLineWidth(2)
            histos[label].Scale(signalscaling)
        elif "WP" in label or "BDT" in label:
            histos[label].SetLineWidth(2)
        else:
            histos[label].SetLineWidth(0)
    
    if contains_data and includeData:
        histolist = [histos[histos.keys()[0]]]
    else:
        histolist = []
    
    h_bgadded = 0
    histolistbg = []
    for label in sorted(histos):
        if not "Data" in label and not "Signal" in label and not "WP" in label:
            histolistbg.append(histos[label])
            if not h_bgadded:
                h_bgadded = histos[label].Clone()
            else:
                h_bgadded.Add(histos[label])
    histolistbg = sorted(histolistbg, key=lambda item: item.Integral())
    histolist += histolistbg
    
    # draw canvas:
    canvas = shared_utils.mkcanvas()
    legend = shared_utils.mklegend(x1 = 0.45, y1 = 0.5, x2 = 0.88, y2 = 0.8)
    legend.SetTextSize(0.06)
    canvas.SetFillColorAlpha(0,0)    
          
    lumi = float("%.2f" % (lumi/1e3))

    h_eff_mc = histos["Backgrounds (WP)"].Clone()
    h_eff_mc.Divide(h_bgadded)
    h_eff_mc.SetTitle("#epsilon_{BDT}(Background)")
    h_eff_mc.SetLineColor(kBlue)

    h_eff_data = histos["Data (WP)"].Clone()
    h_eff_data.Divide(histos["Data"])
    h_eff_data.SetTitle("#epsilon_{BDT}(Data)")

    h_eff_data.SetLineColor(kBlack)
    h_eff_data.SetLineWidth(1)
    h_eff_data.SetLineStyle(1)
    hratio, pads = FabDraw(canvas, legend, h_eff_data, [h_eff_mc], lumi = 1.0, datamc = 'Data', ytitle = "BDT efficiency", LinearScale=LinearScale, fractionthing = "Data/MC")
    h_eff_data.SetLineColor(kBlack)
    h_eff_data.SetLineWidth(1)
    h_eff_data.SetLineStyle(1)
    hratio.GetYaxis().SetRangeUser(0, 2.5)
    h_eff_data.GetYaxis().SetRangeUser(ymin, ymax)
    h_eff_mc.GetYaxis().SetRangeUser(ymin, ymax)
    
    pads[0].cd()
    h_eff_sg = histos["Signal (pooled T1qqqq, x10^{3}, after BDT)"].Clone()
    h_eff_sg.Divide(histos["Signal (pooled T1qqqq, x10^{3})"])
    h_eff_sg.SetTitle("#epsilon_{BDT}(Signal, T1qqqq)")
    h_eff_sg.SetFillColorAlpha(0, 0)
    h_eff_sg.SetLineColor(kMagenta)
    h_eff_sg.SetLineWidth(2)
    h_eff_sg.Draw("hist same")
    legend.AddEntry(h_eff_sg,h_eff_sg.GetTitle(),'lf')
    
    if "phase0" in thisbatchname:
        h_eff_sgt1 = histos["Signal (pooled T2bt, x10^{3}, after BDT)"].Clone()
        h_eff_sgt1.Divide(histos["Signal (pooled T2bt, x10^{3})"])
        h_eff_sgt1.SetTitle("#epsilon_{BDT}(Signal, T2bt)")
        h_eff_sgt1.SetFillColorAlpha(0, 0)
        h_eff_sgt1.SetLineColor(kMagenta)
        h_eff_sgt1.SetLineStyle(2)
        h_eff_sgt1.SetLineWidth(2)
        h_eff_sgt1.Draw("hist same")
        legend.AddEntry(h_eff_sgt1,h_eff_sgt1.GetTitle(),'lf')
    
        print "***"
        print "long:", h_eff_data.GetBinContent(1), h_eff_mc.GetBinContent(1), h_eff_sg.GetBinContent(1), h_eff_sgt1.GetBinContent(1)
        print "short:", h_eff_data.GetBinContent(2), h_eff_mc.GetBinContent(2), h_eff_sg.GetBinContent(2), h_eff_sgt1.GetBinContent(2)
        print "***"
    
    if hratio:

        hratio.GetYaxis().SetRangeUser(0, 2)    
        hratio.GetYaxis().SetTitle('Data/MC')
        if len(binnings) == 4:
            hratio.GetXaxis().SetTitle(binnings[3])
        else:
            hratio.GetXaxis().SetTitle(str(variable))
    
    os.system("mkdir -p %s_eff" % thisbatchname)
    pdfname = thisbatchname + "_eff/" + variable.replace("/", "_") + ".pdf"
        
    canvas.SaveAs(pdfname)


def do_eff_plots_wrapper(parameters):
    
    return do_eff_plots(*parameters)


def do_plots_wrapper(parameters):
    
    return do_plots(*parameters)


if __name__ == "__main__":
        
    use_allMC = 0
    before_preselection = 0
    plot_input_variables = 1
    plot_output_variables = 0
    dy_control_region = 1
    lowmht_control_region = 0
    bdt_efficiency = 0
    use_vetoes = 0
    use_tighter_shortcuts = 0
    
    plotfolder = "bdtnewplots2"
    #folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_90_bdts_merged"
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_96_fullEta_merged"
    
    if use_allMC:
        plotfolder += "_allMC" 
    if use_vetoes:
        plotfolder += "_vetoes"
    if use_tighter_shortcuts:
        plotfolder += "_tightershortcuts"
        
        
    datasets_phase0 = collections.OrderedDict()
    datasets_phase1 = collections.OrderedDict()
    
    datasets_phase0["Data"] = [[
                "Run2016*SingleElectron"
                ], kBlack]
    datasets_phase0["WJetsToLNu"] = [[
                "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1",
                "Summer16.WJetsToLNu_TuneCUETP8M1",
                ], 85]
    datasets_phase0["DYJetsToLL"] = [[
                "Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1",
                ], 67]
    datasets_phase0["TTJets"] = [[
                #"Summer16.TT_TuneCUETP8M2T4_13TeV-powheg-pythia8",
                "Summer16.TTJets_DiLept",
                "Summer16.TTJets_SingleLeptFromT",
                "Summer16.TTJets_SingleLeptFromTbar",
                ], 8]
    datasets_phase0["Diboson"] = [[
                "Summer16.ZZ_TuneCUETP8M1",
                "Summer16.WW_TuneCUETP8M1",
                "Summer16.WZ_TuneCUETP8M1",
                ], 62]
    if use_allMC:
        datasets_phase0["QCD"] = [[
                    "Summer16.QCD_HT200to300_TuneCUETP8M1",
                    "Summer16.QCD_HT300to500_TuneCUETP8M1",
                    "Summer16.QCD_HT500to700_TuneCUETP8M1",
                    "Summer16.QCD_HT700to1000_TuneCUETP8M1",
                    "Summer16.QCD_HT1000to1500_TuneCUETP8M1",
                    "Summer16.QCD_HT1500to2000_TuneCUETP8M1",
                    "Summer16.QCD_HT2000toInf_TuneCUETP8M1",
                    ], 97]
        datasets_phase0["ZJets"] = [[
                    "Summer16.ZJetsToNuNu_HT-100To200_13TeV",
                    "Summer16.ZJetsToNuNu_HT-200To400_13TeV",
                    "Summer16.ZJetsToNuNu_HT-400To600_13TeV",
                    "Summer16.ZJetsToNuNu_HT-600To800_13TeV",
                    "Summer16.ZJetsToNuNu_HT-800To1200_13TeV",
                    "Summer16.ZJetsToNuNu_HT-1200To2500_13TeV",
                    "Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV",
                    ], kOrange]
    #datasets_phase0["Signal, m_{Glu}=2.0 TeV, m_{#chi}=1.975 TeV"] = [[
    #            "RunIISummer16MiniAODv3.SMS-T1qqqq",
    #            ], kRed, "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2000 && signal_lsp_mass==1975"]
    #datasets_phase0["Signal, m_{Glu}=2.5 TeV, m_{#chi}=2.475 TeV"] = [[
    #            "RunIISummer16MiniAODv3.SMS-T1qqqq",
    #            ], kMagenta, "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2500 && signal_lsp_mass==2475"]
    #datasets_phase0["Signal, m_{Glu}=2.8 TeV, m_{#chi}=2.775 TeV"] = [[
    #            "RunIISummer16MiniAODv3.SMS-T1qqqq",
    #            ], kOrange, "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2800 && signal_lsp_mass==2775"]
    #datasets_phase0["Signal (T2bt), m_{#chi}=1 TeV"] = [[
    #            "RunIISummer16MiniAODv3.SMS-T2bt-LLChipm_ctau-200_mLSP-1000_",
    #            ], kYellow, "tracks_chiCandGenMatchingDR<0.01"]
    datasets_phase0["Signal (pooled T1qqqq, x10^{3})"] = [[
                "RunIISummer16MiniAODv3.SMS-T1qqqq",
                ], kRed, "tracks_chiCandGenMatchingDR<0.01"]
    datasets_phase0["Signal (pooled T2bt, x10^{3})"] = [[
                "RunIISummer16MiniAODv3.SMS-T2bt",
                ], kOrange, "tracks_chiCandGenMatchingDR<0.01"]
                
    datasets_phase1["Data"] = [[
                "Run2017*SingleElectron",
                "Run2018*EGamma",
                ], kBlack]
    datasets_phase1["WJetsToLNu"] = [[
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",
                ], 85]
    datasets_phase1["DYJetsToLL"] = [[
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
                ], 67]
    if use_allMC:
        datasets_phase1["QCD"] = [[
                    "RunIIFall17MiniAODv2.QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",
                    "RunIIFall17MiniAODv2.QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",
                    "RunIIFall17MiniAODv2.QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",
                    "RunIIFall17MiniAODv2.QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8",
                    "RunIIFall17MiniAODv2.QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",
                    "RunIIFall17MiniAODv2.QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",
                    "RunIIFall17MiniAODv2.QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",
                    ], 97]
        datasets_phase1["ZJets"] = [[
                    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
                    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",   
                    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400_13TeV-madgraph",
                    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
                    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
                    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800_13TeV-madgraph",
                    "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
                    ], kOrange]
    datasets_phase1["TTJets"] = [[
                "RunIIFall17MiniAODv2.TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8",
                ], 8]
    datasets_phase1["Diboson"] = [[
                "RunIIFall17MiniAODv2.WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
                "RunIIFall17MiniAODv2.WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
                "RunIIFall17MiniAODv2.WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_v2",
                ], 62]
    datasets_phase1["Signal (pooled T1qqqq, x10^{3})"] = [[
                "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq",
                ], kRed, "tracks_chiCandGenMatchingDR<0.01"]
    #datasets_phase1["Signal, m_{Glu}=2.0 TeV, m_{#chi}=1.975 TeV"] = [[
    #            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq",
    #            ], kRed, "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2000 && signal_lsp_mass==1975"]
    #datasets_phase1["Signal, m_{Glu}=2.5 TeV, m_{#chi}=2.475 TeV"] = [[
    #            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq",
    #            ], kOrange, "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2500 && signal_lsp_mass==2475"]
    #datasets_phase1["Signal, m_{Glu}=2.8 TeV, m_{#chi}=2.775 TeV"] = [[
    #            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq",
    #            ], kYellow, "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2800 && signal_lsp_mass==2775"]
    #datasets_phase1["Signal, T1qqqq (c#tau=10cm)"] = [[
    #            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-10_TuneCP2_13TeV",
    #            ], kRed, "tracks_chiCandGenMatchingDR<0.01"]
    #datasets_phase1["Signal, T1qqqq (c#tau=50cm)"] = [[
    #            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-50_TuneCP2_13TeV",
    #            ], kOrange, "tracks_chiCandGenMatchingDR<0.01"]
    #datasets_phase1["Signal, T1qqqq (c#tau=200cm)"] = [[
    #            "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq-LLChipm_ctau-200_TuneCP2_13TeV",
    #            ], kYellow, "tracks_chiCandGenMatchingDR<0.01"]
        
    event_selections = {
                  "Baseline":               "((n_goodelectrons==0 && n_goodmuons==0) || (tracks_invmass>110 && leadinglepton_mt>90))",
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
                      
    wp_full = {
                  "short_phase0": "tracks_is_pixel_track==1 && tracks_mva_nov20_noEdep>0.1 && tracks_matchedCaloEnergy<15 ",
                  "short_phase1": "tracks_is_pixel_track==1 && tracks_mva_nov20_noEdep>0.12 && tracks_matchedCaloEnergy<15 ",
                  "long_phase0": "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_mva_nov20_noEdep>0.1 && tracks_matchedCaloEnergy/tracks_p<0.15 ",
                  "long_phase1":"tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_mva_nov20_noEdep>0.15 && tracks_matchedCaloEnergy/tracks_p<0.15 ",
         }

    wp = {
                  "short_phase0": "tracks_is_pixel_track==1 && tracks_mva_nov20_noEdep>0.1 ",
                  "short_phase1": "tracks_is_pixel_track==1 && tracks_mva_nov20_noEdep>0.12 ",
                  "long_phase0": "tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_mva_nov20_noEdep>0.1 ",
                  "long_phase1":"tracks_is_pixel_track==0 && tracks_nMissingOuterHits>=2 && tracks_mva_nov20_noEdep>0.15 ",
         }
         
    if use_tighter_shortcuts:
        wp["short_phase0"] += " && tracks_dxyVtx<0.005 && tracks_dzVtx<0.01" 
        wp["long_phase0"] += " && tracks_dxyVtx<0.005 && tracks_dzVtx<0.01" 
            
    variables = {
                  #"tracks_is_pixel_track": [2, 0, 2, "pixel-only track"],
                  #"tracks_trkRelIso": [[0, 0.005, 0.01, 0.015, 0.02, 0.2], 0, 0.2, "relative track isolation"],
                  "tracks_dxyVtx": [[0, 0.005, 0.01, 0.015, 0.02, 0.1], 0, 0.1, "d_{xy} (cm)"],
                  #"tracks_dzVtx": [[0, 0.005, 0.01, 0.015, 0.02, 0.1], 0, 0.1, "d_{z} (cm)"],
                  #"tracks_nMissingOuterHits": [20, 0, 20, "missing outer hits"],
                  #"tracks_nValidPixelHits": [10, 0, 10, "pixel hits"],
                  #"tracks_nValidTrackerHits": [20, 0, 20, "tracker hits"],
                  #"tracks_chi2perNdof": [20, 0, 5.0, "track #chi^{2}/ndof"],
                  #"tracks_ptErrOverPt2": [[0, 0.005, 0.01, 0.015, 0.02, 0.1], 0, 0.1, "#Delta p_{T} / p_{T}^{2} (GeV^{-1})"],                  
                  #"tracks_deDxHarmonic2pixel": [20, 0, 10, "pixel dE/dx (MeV/cm)"],
                  #"tracks_matchedCaloEnergy": [20, 0, 50, "E_{dep} (GeV)"],
                  "tracks_invmass": [15, 60, 120, "m_{lepton, track}^{inv} (GeV)"],
                  #"tracks_matchedCaloEnergy/tracks_p": [40, 0, 2.0, "E_{dep}/p_{track}"],
                  #"abs(tracks_eta)": [50, 0, 2.5, "#eta"],
                  #"tracks_trackQualityHighPurity": [2, 0, 2, "high quality, high purity track"],
                  #"tracks_ptErrOverPt2": [20, 0, 5, "#Delta p_{T} / p_{T}^{2} (1/GeV)"],                  
                  #"tracks_dzVtx": [25, 0, 1.0, "d_{z} (cm)"],
                  #"tracks_trkRelIso": [40, 0, 0.2, "relative track isolation"],
                  ####"tracks_chargedPtSum": [40, 0, 2.0, "charged p_{T} sum (GeV)"],      
                  #"tracks_mva_tight_may20_chi2_pt15": [20, -1.0, 1.0, "BDT response"],
                  #"tracks_mva_tight_may21": [20, -1.0, 1.0, "BDT response"],
                  #"tracks_mva_tight_may21EquSgXsec": [20, -1.0, 1.0, "BDT response"],
                  #"tracks_mva_nov20_noEdep": [20, -1.0, 1.0, "BDT response"],
                  #"HT": [20, 0, 700, "H_{T} (GeV)"],
                  #"MHT": [20, 0, 700, "missing H_{T} (GeV)"],
                  #"n_goodjets": [20, 0, 20, "n_{jet}"],
                  #"n_btags": [10, 0, 10, "n_{btags}"],
                  #"tracks_fake"] = [2, 0, 2, "isfake"]
                  #"tracks_deDxHarmonic2pixel": [20, 0, 10, "track dE/dx (MeV/cm)"],
                  #"tracks_invmass": [10, 0, 200, "m_{DT, track} (GeV)"],
                  #"regionCorrected"] = [54, 1, 55, "search bin"]
                  #"dilepton_invmass"] = [50, 40, 140, "m_{l, l} (GeV)"]
                  #"leadinglepton_mt": [16, 0, 160, "lepton m_{T} (GeV)"],
                  #"tracks_mva_loose"] = [20, -1, 1, "BDT score"]
                  #"leadinglepton_mt"] = [16, 0, 160, "m_{T} (GeV)"]
                  #"tracks_mva_tight:tracks_dxyVtx"] = [40, 0, 0.04, 20, 0.1, 1.0]
                  #"tracks_mva_loose:tracks_dxyVtx"] = [50, 0, 0.05, 40, -1.0, 1.0]
                  #"tracks_trkMiniRelIso"] = [50, 0, 0.2, "track miniIsolation"]
                  #"tracks_nMissingInnerHits"] = [20, 0, 20, "missing inner hits"]
                  #"tracks_nMissingMiddleHits"] = [20, 0, 20, "missing middle hits"]
                 }    

    parameters = []

    for phase in [
                   0,
                   #1,
                 ]:
                 
        if phase == 0:
            lumi = 35000
            labels = datasets_phase0
            signalscaling = 1e3
        else:
            lumi = 102000
            labels = datasets_phase1
            signalscaling = 1e3

        if before_preselection:

            folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_82_merged"

            ymin = 1e-4
            ymax = 1e8

            presel_variables = {
                          "abs(tracks_eta)": [50, 0, 2.5, "#eta"],
                          "tracks_trackQualityHighPurity": [2, 0, 2, "high quality, high purity track"],
                          "tracks_ptErrOverPt2": [20, 0, 40, "#Delta p_{T} / p_{T}^{2} (1/GeV)"],                  
                          "tracks_dzVtx": [25, 0, 1.0, "d_{z} (cm)"],
                          "tracks_trkRelIso": [40, 0, 0.2, "relative track isolation"],
                         }    
            for variable in presel_variables:
                parameters.append((variable, "tracks_is_pixel_track==1 && tracks_pt>15", "%s/beforepreselection_short_p%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(presel_variables[variable]), signalscaling, False, False, False, lumi, ymin, ymax))        
                parameters.append((variable, "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2", "%s/beforepreselection_long_p%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(presel_variables[variable]), signalscaling, False, False, False, lumi, ymin, ymax))        

        if plot_input_variables:

            ymin = 1e0
            ymax = 1e8
            
            #datasets_phase0["Data (WP)"] = [[
            #            "Run2016*SingleElectron"
            #            ], kMagenta, wp["short_phase%s" % phase]]
            #datasets_phase0["Backgrounds (WP)"] = [datasets_phase0["WJetsToLNu"][0] + datasets_phase0["DYJetsToLL"][0] + datasets_phase0["TTJets"][0] + datasets_phase0["Diboson"][0], kMagenta, wp["short_phase%s" % phase]]
            #datasets_phase0["Signal (pooled T1qqqq, x10^{3}, after BDT)"] = [[
            #            "RunIISummer16MiniAODv3.SMS-T1qqqq",
            #            ], kRed, "tracks_chiCandGenMatchingDR<0.01 && " + wp["short_phase%s" % phase]]
            #datasets_phase0["Signal (pooled T2bt, x10^{3}, after BDT)"] = [[
            #            "RunIISummer16MiniAODv3.SMS-T2bt",
            #            ], kOrange, "tracks_chiCandGenMatchingDR<0.01 && " + wp["short_phase%s" % phase]]
            
            for variable in variables:
                parameters.append((variable, "tracks_is_pixel_track==1 && tracks_pt>25" , "%s/input_short_p%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, False, False, lumi, ymin, ymax))        
                parameters.append((variable, "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2" , "%s/input_long_p%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, False, False, lumi, ymin, ymax))        
        
        if plot_output_variables:
            
            ymin = 1e-4
            ymax = 1e8
            
            for variable in variables:
                parameters.append((variable, "tracks_is_pixel_track==1 && tracks_pt>15 && " + wp_full["short_phase%s" % phase] , "%s/output_short_p%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, False, False, lumi, ymin, ymax))        
                parameters.append((variable, "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2 && " + wp_full["long_phase%s" % phase] , "%s/output_long_p%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, False, False, lumi, ymin, ymax))        
                        
        if dy_control_region:

            if bdt_efficiency:
                ymin = 1e-4
                ymax = 1e1
                ymin_lin = 0
                ymax_lin = 1.0    
            else:
                ymin = 1e0
                ymax = 1e6
                ymin_lin = 0
                ymax_lin = 1.2

            basecuts = "tracks_trackQualityHighPurity==1 && tracks_passPFCandVeto==1 && abs(tracks_eta)<2.0 && tracks_ptErrOverPt2<10.0 && abs(tracks_dzVtx)<0.1 && tracks_trkRelIso<0.2 && tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2 && tracks_nMissingInnerHits==0 && tracks_nValidPixelHits>=2 "
            DYregion = "n_goodelectrons>=1 && tracks_invmass>65 && tracks_invmass<110"
            vetoes = "&& tracks_passpionveto==1 && tracks_passjetveto==1 && tracks_passleptonveto==1"
            #vetoes = " && tracks_passpionveto==1 "
            if use_vetoes:
                DYregion += vetoes
            
            for variable in variables:
                
                datasets_phase0["Data (WP)"] = [[
                            "Run2016*SingleElectron"
                            ], kMagenta, wp["short_phase%s" % phase]]
                datasets_phase0["Backgrounds (WP)"] = [datasets_phase0["WJetsToLNu"][0] + datasets_phase0["DYJetsToLL"][0] + datasets_phase0["TTJets"][0] + datasets_phase0["Diboson"][0], kMagenta, wp["short_phase%s" % phase]]

                datasets_phase1["Data (WP)"] = [[
                            "Run2017*SingleElectron",
                            "Run2018*EGamma",
                            ], kMagenta, wp["short_phase%s" % phase]]
                datasets_phase1["Backgrounds (WP)"] = [datasets_phase1["WJetsToLNu"][0] + datasets_phase1["DYJetsToLL"][0] + datasets_phase1["TTJets"][0] + datasets_phase1["Diboson"][0], kMagenta, wp["short_phase%s" % phase]]

                if use_allMC:
                    datasets_phase0["Backgrounds (WP)"] = [datasets_phase0["WJetsToLNu"][0] + datasets_phase0["DYJetsToLL"][0] + datasets_phase0["TTJets"][0] + datasets_phase0["Diboson"][0] + datasets_phase0["QCD"][0] + datasets_phase0["ZJets"][0], kMagenta, wp["short_phase%s" % phase]]

                if bdt_efficiency:
                    datasets_phase0["Signal (pooled T1qqqq, x10^{3}, after BDT)"] = [[
                                "RunIISummer16MiniAODv3.SMS-T1qqqq",
                                ], kRed, "tracks_chiCandGenMatchingDR<0.01 && " + wp["short_phase%s" % phase]]
                    datasets_phase0["Signal (pooled T2bt, x10^{3}, after BDT)"] = [[
                                "RunIISummer16MiniAODv3.SMS-T2bt",
                                ], kOrange, "tracks_chiCandGenMatchingDR<0.01 && " + wp["short_phase%s" % phase]]
                    datasets_phase1["Signal (pooled T1qqqq, x10^{3}, after BDT)"] = [[
                                "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq",
                                ], kRed, "tracks_chiCandGenMatchingDR<0.01 && " + wp["short_phase%s" % phase]]

                ##parameters.append((variable, [DYregion + " && tracks_is_pixel_track==1 && tracks_pt>25", "tracks_is_pixel_track==1 && tracks_pt>25"], "%s/dycr-short-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, False, True, lumi, ymin, ymax))
                #parameters.append((variable, [DYregion + " && tracks_is_pixel_track==1 && tracks_pt>25", "tracks_is_pixel_track==1 && tracks_pt>25"], "%s/dycrLin-short-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, True, True, lumi, ymin_lin, 10000))
                parameters.append((variable, [DYregion + " && tracks_is_pixel_track==1 && tracks_pt>25", "tracks_is_pixel_track==1 && tracks_pt>25"], "%s/dycrLinNorm-short-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, True, True, True, lumi, ymin_lin, ymax_lin))
                                    
                datasets_phase0["Data (WP)"] = [[
                            "Run2016*SingleElectron"
                            ], kMagenta, wp["long_phase%s" % phase]]
                datasets_phase1["Data (WP)"] = [[
                            "Run2017*SingleElectron",
                            "Run2018*EGamma",
                            ], kMagenta, wp["long_phase%s" % phase]]
                if bdt_efficiency:
                    datasets_phase0["Signal (pooled T1qqqq, x10^{3}, after BDT)"] = [[
                                "RunIISummer16MiniAODv3.SMS-T1qqqq",
                                ], kRed, "tracks_chiCandGenMatchingDR<0.01 && " + wp["long_phase%s" % phase]]
                    datasets_phase0["Signal (pooled T2bt, x10^{3}, after BDT)"] = [[
                                "RunIISummer16MiniAODv3.SMS-T2bt",
                                ], kOrange, "tracks_chiCandGenMatchingDR<0.01 && " + wp["long_phase%s" % phase]]
                    datasets_phase1["Signal (pooled T1qqqq, x10^{3}, after BDT)"] = [[
                                "RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq",
                                ], kOrange, "tracks_chiCandGenMatchingDR<0.01 && " + wp["long_phase%s" % phase]]
                datasets_phase0["Backgrounds (WP)"] = [datasets_phase0["WJetsToLNu"][0] + datasets_phase0["DYJetsToLL"][0] + datasets_phase0["TTJets"][0] + datasets_phase0["Diboson"][0], kMagenta, wp["long_phase%s" % phase]]
                datasets_phase1["Backgrounds (WP)"] = [datasets_phase1["WJetsToLNu"][0] + datasets_phase1["DYJetsToLL"][0] + datasets_phase1["TTJets"][0] + datasets_phase1["Diboson"][0], kMagenta, wp["long_phase%s" % phase]]
                if use_allMC:
                    datasets_phase0["Backgrounds (WP)"] = [datasets_phase0["WJetsToLNu"][0] + datasets_phase0["DYJetsToLL"][0] + datasets_phase0["TTJets"][0] + datasets_phase0["Diboson"][0] + datasets_phase0["QCD"][0] + datasets_phase0["ZJets"][0], kMagenta, wp["long_phase%s" % phase]]
                
                #parameters.append((variable, [DYregion + " && tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2", "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2"], "%s/dycr-long-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, False, True, lumi, ymin, ymax))
                #parameters.append((variable, [DYregion + " && tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2", "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2"], "%s/dycrLin-long-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, True, True, lumi, ymin_lin, 10000))
                parameters.append((variable, [DYregion + " && tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2", "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2"], "%s/dycrLinNorm-long-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, True, True, True, lumi, ymin_lin, ymax_lin))
        
        if lowmht_control_region:

            if bdt_efficiency:
                ymin = 1e-4
                ymax = 1e1
                ymin_lin = 0
                ymax_lin = 1.0    
            else:
                ymin = 1e0
                ymax = 1e6
                ymin_lin = 0
                ymax_lin = 1.2

            
            basecuts = "tracks_trackQualityHighPurity==1 && tracks_passPFCandVeto==1 && abs(tracks_eta)<2.0 && tracks_ptErrOverPt2<10.0 && abs(tracks_dzVtx)<0.1 && tracks_trkRelIso<0.2 && tracks_trackerLayersWithMeasurement>=2 && tracks_nValidTrackerHits>=2 && tracks_nMissingInnerHits==0 && tracks_nValidPixelHits>=2 "
            LowMHTregion = "HT>30 && n_goodelectrons==0 && n_goodmuons==0 && MHT<60"
            vetoes = " && tracks_passjetveto==1 && tracks_passleptonveto==1 && tracks_passpionveto==1"
            #vetoes = " && tracks_passpionveto==1 "
            if use_vetoes:
                LowMHTregion += vetoes
            
            for variable in variables:
                
                datasets_phase0["Data (WP)"] = [[
                            "Run2016*JetHT"
                            ], kMagenta, wp["short_phase%s" % phase]]
                datasets_phase0["Backgrounds (WP)"] = [datasets_phase0["WJetsToLNu"][0] + datasets_phase0["DYJetsToLL"][0] + datasets_phase0["TTJets"][0] + datasets_phase0["Diboson"][0], kMagenta, wp["short_phase%s" % phase]]
                if use_allMC:
                    datasets_phase0["Backgrounds (WP)"] = [datasets_phase0["WJetsToLNu"][0] + datasets_phase0["DYJetsToLL"][0] + datasets_phase0["TTJets"][0] + datasets_phase0["Diboson"][0] + datasets_phase0["QCD"][0] + datasets_phase0["ZJets"][0], kMagenta, wp["short_phase%s" % phase]]
                datasets_phase0["Signal (pooled T1qqqq, x10^{3}, after BDT)"] = [[
                            "RunIISummer16MiniAODv3.SMS-T1qqqq",
                            ], kRed, "tracks_chiCandGenMatchingDR<0.01 && " + wp["short_phase%s" % phase]]
                datasets_phase0["Signal (pooled T2bt, x10^{3}, after BDT)"] = [[
                            "RunIISummer16MiniAODv3.SMS-T2bt",
                            ], kOrange, "tracks_chiCandGenMatchingDR<0.01 && " + wp["short_phase%s" % phase]]
                parameters.append((variable, [LowMHTregion + " && tracks_is_pixel_track==1 && tracks_pt>25", "tracks_is_pixel_track==1 && tracks_pt>25"], "%s/lowmht-short-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, False, True, lumi, ymin, ymax))
                #parameters.append((variable, [LowMHTregion + " && tracks_is_pixel_track==1 && tracks_pt>25", "tracks_is_pixel_track==1 && tracks_pt>25"], "%s/lowmhtLin-short-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, True, True, lumi, ymin_lin, 10000))
                parameters.append((variable, [LowMHTregion + " && tracks_is_pixel_track==1 && tracks_pt>25", "tracks_is_pixel_track==1 && tracks_pt>25"], "%s/lowmhtLinNorm-short-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, True, True, True, lumi, ymin_lin, ymax_lin))
                                       
                datasets_phase0["Data (WP)"] = [[
                            "Run2016*JetHT"
                            ], kMagenta, wp["long_phase%s" % phase]]
                datasets_phase0["Signal (pooled T1qqqq, x10^{3}, after BDT)"] = [[
                            "RunIISummer16MiniAODv3.SMS-T1qqqq",
                            ], kRed, "tracks_chiCandGenMatchingDR<0.01 && " + wp["long_phase%s" % phase]]
                datasets_phase0["Signal (pooled T2bt, x10^{3}, after BDT)"] = [[
                            "RunIISummer16MiniAODv3.SMS-T2bt",
                            ], kOrange, "tracks_chiCandGenMatchingDR<0.01 && " + wp["long_phase%s" % phase]]
                datasets_phase0["Backgrounds (WP)"] = [datasets_phase0["WJetsToLNu"][0] + datasets_phase0["DYJetsToLL"][0] + datasets_phase0["TTJets"][0] + datasets_phase0["Diboson"][0] + datasets_phase0["QCD"][0] + datasets_phase0["ZJets"][0], kMagenta, wp["long_phase%s" % phase]]
                if use_allMC:
                    datasets_phase0["Backgrounds (WP)"] = [datasets_phase0["WJetsToLNu"][0] + datasets_phase0["DYJetsToLL"][0] + datasets_phase0["TTJets"][0] + datasets_phase0["Diboson"][0], kMagenta, wp["long_phase%s" % phase]]
                parameters.append((variable, [LowMHTregion + " && tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2", "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2"], "%s/lowmht-long-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, False, True, lumi, ymin, ymax))
                #parameters.append((variable, [LowMHTregion + " && tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2", "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2"], "%s/lowmhtLin-long-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, False, True, True, lumi, ymin_lin, 10000))
                parameters.append((variable, [LowMHTregion + " && tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2", "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2"], "%s/lowmhtLinNorm-long-phase%s" % (plotfolder, phase), folder, copy.deepcopy(labels), copy.deepcopy(variables[variable]), signalscaling, True, True, True, lumi, ymin_lin, ymax_lin))
                  
                                    
    #parameters = [parameters[0]]
                                    
    print "Plotting %s plots..." % len(parameters)
    pool = multiprocessing.Pool(int(multiprocessing.cpu_count()))
    if bdt_efficiency:
        pool.map(do_eff_plots_wrapper, parameters)
    else:
        pool.map(do_plots_wrapper, parameters)

