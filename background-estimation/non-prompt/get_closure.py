#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *
import collections
from optparse import OptionParser
import array

def closure_plot(root_file, variable, category, cr, canvas_label, root_file_data = False, extra_text = "", xlabel = False, lumi = 36000, autoscaling = True, xmax = False, ymax = False, ymin = False, fr_regions = [], fr_maps = [], output_root_file = False, pdf_output = True, outpath = "plots"):

    if "Run201" in output_root_file:
        is_data = True
    else:
        is_data = False
       
    histos = collections.OrderedDict()

    print "opening", root_file
    tfile = TFile(root_file, "open")

    if False:
                
        histos["mc_CR"] = tfile.Get("%s_nonpromptcontrol_%s_%s" % (variable, "short", cr) )
        histos["mc_nonprompt"] = tfile.Get("%s_signalfake_%s_%s" % (variable, "short", cr) )
        histos["mc_prompt"] = tfile.Get("%s_signalprompt_%s_%s" % (variable, "short", cr) )
        histos["mc_prediction"] = tfile.Get("%s_nonpromptprediction_%s_%s" % (variable, "short", cr) )

        histos["mc_CR"].Add(tfile.Get("%s_nonpromptcontrol_%s_%s" % (variable, "long", cr) ))
        histos["mc_nonprompt"].Add(tfile.Get("%s_signalfake_%s_%s" % (variable, "long", cr) ))
        histos["mc_prompt"].Add(tfile.Get("%s_signalprompt_%s_%s" % (variable, "long", cr) ))
        histos["mc_prediction"].Add(tfile.Get("%s_nonpromptprediction_%s_%s" % (variable, "long", cr) ))

        histos["mc_CR"].Add(tfile.Get("%s_nonpromptcontrol_%s_%s" % (variable, "multi", cr) ))
        histos["mc_nonprompt"].Add(tfile.Get("%s_signalfake_%s_%s" % (variable, "multi", cr) ))
        histos["mc_prompt"].Add(tfile.Get("%s_signalprompt_%s_%s" % (variable, "multi", cr) ))
        histos["mc_prediction"].Add(tfile.Get("%s_nonpromptprediction_%s_%s" % (variable, "multi", cr) ))

        canvas_label = canvas_label.replace("_short", "").replace("_long", "")

    else:
        
        histos["mc_CR"] = tfile.Get("%s_nonpromptcontrol_%s_%s" % (variable, category, cr) )
        histos["mc_nonprompt"] = tfile.Get("%s_signalfake_%s_%s" % (variable, category, cr) )
        histos["mc_prompt"] = tfile.Get("%s_signalprompt_%s_%s" % (variable, category, cr) )
        histos["mc_prediction"] = tfile.Get("%s_nonpromptprediction_%s_%s" % (variable, category, cr) )
    
    # rebin histograms:
    for label in histos:
        if "HT" in variable:
            redoBinning = [0, 100, 200, 300, 400, 500, 1000]
        elif variable == "MinDeltaPhiMhtJets":
            redoBinning = [0.3, 0.5, 0.7, 0.9]
        elif variable == "n_btags":
            redoBinning = [0, 1, 2, 5]
        else:
            redoBinning = False
            
        if redoBinning:
            nbins = len(redoBinning)-1
            newxs = array.array('d', redoBinning)
            histos[label] = histos[label].Rebin(nbins, label, newxs)
  
    colors = [kTeal, kBlue, kRed, kBlue, kRed, kOrange, kMagenta, kAzure, kTeal+2, kBlue+2, kRed+2, kBlue+2, kRed+2, kOrange+2, kMagenta+2, kAzure+2]

    for label in histos:                
        histos[label].SetLineWidth(2)
        color = colors.pop(0)
        histos[label].SetLineColor(color)

        if not is_data:
            histos[label].Scale(lumi)

        if "prediction" in label or "data" in label:
            histos[label].SetMarkerStyle(22)
            histos[label].SetMarkerColor(color)
            histos[label].SetMarkerSize(1.5)

    # rename labels:
    canvas_label = canvas_label.replace("_MET", "_Met")
    canvas_label = canvas_label.replace("_MHT", "_Mht")
    canvas_label = canvas_label.replace("_n_jets", "_NJets")
    canvas_label = canvas_label.replace("_n_btags", "_BTags")
    canvas_label = canvas_label.replace("_n_goodjets", "_NJets")
    canvas_label = canvas_label.replace("_n_goodelectrons", "_NElectrons")
    canvas_label = canvas_label.replace("_n_goodmuons", "_NMuons")
    canvas_label = canvas_label.replace("_n_tags", "_NTags")
    canvas_label = canvas_label.replace("_HT", "_Ht")
    canvas_label = canvas_label.replace("_MinDeltaPhiMhtJets", "_MinDPhiMhtJets")
    canvas_label = canvas_label.replace("_region", "_BinNumber")

    canvas = TCanvas(canvas_label, canvas_label, 800, 800)
    canvas.SetRightMargin(0.06)
    canvas.SetLeftMargin(0.12)
    canvas.SetLogy(True)

    pad1 = TPad("pad1", "pad1", 0, 0.16, 1, 1.0)
    pad1.SetRightMargin(0.05)
    pad1.SetLogy(True)
    pad2 = TPad("pad2", "pad2", 0.0, 0.025, 1.0, 0.235)
    pad2.SetBottomMargin(0.25)
    pad2.SetRightMargin(0.05)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()

    if autoscaling:
        global_ymin = 1e10
        global_ymax = 1e-10
        for histo in histos:
            current_ymin = 1e10
            for ibin in range(histos[histo].GetNbinsX()):
               value = histos[histo].GetBinContent(ibin)
               if value < current_ymin and value != 0:
                    current_ymin = value
            if current_ymin < global_ymin:
                global_ymin = current_ymin
            if histos[histo].GetMaximum() > global_ymax:
                global_ymax = histos[histo].GetMaximum()
    
        if not ymax:
            ymin = global_ymin * 1e-1
            ymax = global_ymax * 5e2

    histos["mc_CR"].Draw("hist e")

    if xmax:
        histos["mc_CR"].GetXaxis().SetRangeUser(xmin, xmax)
    if ymax:
        histos["mc_CR"].GetYaxis().SetRangeUser(ymin, ymax)
    histos["mc_CR"].GetXaxis().SetLabelSize(0)   
    histos["mc_CR"].SetTitle(";;events")
   
    if not is_data:
        histos["mc_prompt"].Draw("same hist e")
        histos["mc_nonprompt"].Draw("same hist e")

    histos["mc_prediction"].Draw("same hist p")

    legend = TLegend(0.3, 0.7, 0.89, 0.89)
    legend.SetHeader(extra_text)
    legend.SetTextSize(0.025)
    legend.AddEntry(histos["mc_CR"], "Control region (CR)")
    legend.AddEntry(histos["mc_nonprompt"], "Non-prompt background in SR (MC Truth)")
    legend.AddEntry(histos["mc_prompt"], "Prompt contamination in SR (MC Truth)")
    legend.AddEntry(histos["mc_prediction"], "Prediction")
    legend.SetBorderSize(0)
               
    legend.Draw()
    stamp_plot()

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)
    latex.DrawLatex(0.93, 0.91, "%.1f fb^{-1} (13 TeV)" % (lumi/1000))

    # plot ratios
    pad2.cd()
    
    if not xlabel:
        xlabel = variable
    
    ratios = collections.OrderedDict()
    for i, label in enumerate(histos):
        if "prediction" in label:
            if is_data:
                ratios[label] = histos["mc_prediction"].Clone()
            else:
                ratios[label] = histos["mc_nonprompt"].Clone()
            ratios[label].SetLineColor(histos[label].GetLineColor())
            ratios[label].SetMarkerStyle(histos[label].GetMarkerStyle())
            ratios[label].SetMarkerSize(histos[label].GetMarkerSize())
            ratios[label].SetMarkerColor(histos[label].GetMarkerColor())
            ratios[label].Divide(histos[label])
            if xmax:
                ratios[label].GetXaxis().SetRangeUser(xmin, xmax)
    
            if i==0:
                ratios[label].Draw("e0")
            else:
                ratios[label].Draw("same e0")
    
            if "HT" in xlabel or "MET" in xlabel or "pt" in xlabel:
                xlabel += " (GeV)"

            ratios[label].SetTitle(";%s;Truth/Pred." % xlabel)
            ratios[label].GetXaxis().SetTitleSize(0.13)
            ratios[label].GetYaxis().SetTitleSize(0.13)
            ratios[label].GetYaxis().SetTitleOffset(0.38)
            ratios[label].GetYaxis().SetRangeUser(0,2)
            ratios[label].GetYaxis().SetNdivisions(4)
            ratios[label].GetXaxis().SetLabelSize(0.15)
            ratios[label].GetYaxis().SetLabelSize(0.15)
    
    pad2.SetGridx(True)
    pad2.SetGridy(True)

    if pdf_output:
        os.system("mkdir -p %s" % outpath)
        canvas.SaveAs(outpath + "/" + canvas_label + ".pdf")

    if output_root_file:
        fout = TFile(output_root_file, "update")
        if is_data:
            histos["mc_prediction"].SetName("%sMethod" % (canvas_label))
        else:
            histos["mc_prediction"].SetName("%sTruth" % (canvas_label))
        histos["mc_prediction"].SetTitle(";%s;Events" % xlabel)
        histos["mc_prediction"].GetXaxis().SetLabelSize(0.03)   
        histos["mc_prediction"].Scale(3.859)
        histos["mc_prediction"].Write()

        if is_data:
            histos["mc_CR"].SetName("%sMethod_CR" % (canvas_label))
        else:
            histos["mc_CR"].SetName("%sTruth_CR" % (canvas_label))
        histos["mc_CR"].SetTitle(";%s;Events" % xlabel)
        histos["mc_CR"].GetXaxis().SetLabelSize(0.03)   
        histos["mc_CR"].Scale(3.859)
        histos["mc_CR"].Write()

        fout.Close()
        

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--folder", dest = "prediction_folder", default = "prediction")
    parser.add_option("--selection", dest = "selection", default = "Baseline")
    parser.add_option("--category", dest = "category", default = "combined")
    (options, args) = parser.parse_args()
   
    variables = ['BTags', 'Met', 'Mht', 'BinNumber', 'InvMass', 'DeDxAverageCorrected', 'LepMT', 'Ht', 'DeDxAverage']
    data_periods = ["Summer16_all", "Run2016_all", "Run2016_SingleElectron", "Run2016_SingleMuon", "Run2016_MET"]

    options.selection = "SElValidationZLL,Baseline,SMuValidationZLLZoneDeDx4p0toInf,SMuValidationMTZoneDeDx4p0toInf,SElValidationMTZoneDeDx0p0to2p1,SMuValidationMTZoneDeDx0p0to2p1,SMuValidationZLLZoneDeDx2p1to4p0,BaselineZoneDeDx2p1to4p0,SMuBaseline,SMuBaselineZoneDeDx2p1to4p0,SMuValidationMTZoneDeDx1p6to2p1,SElValidationZLLZoneDeDx2p1to4p0,HadBaseline,SMuValidationMT,SElValidationZLLZoneDeDx1p6to2p1,SMuBaselineZoneDeDx1p6to2p1,SElBaseline,BaselineZoneDeDx1p6to2p1,SMuValidationZLLZoneDeDx1p6to2p1,SElValidationMTZoneDeDx1p6to2p1,SElValidationZLLZoneDeDx4p0toInf,HadBaselineZoneDeDx0p0to2p1,SElBaselineZoneDeDx4p0toInf,SMuBaselineZoneDeDx0p0to2p1,SElValidationZLLZoneDeDx0p0to2p1,SElValidationMT,BaselineZoneDeDx0p0to2p1,HadBaselineZoneDeDx2p1to4p0,HadBaselineZoneDeDx4p0toInf,SMuBaselineZoneDeDx4p0toInf,SElValidationMTZoneDeDx2p1to4p0,SMuValidationZLLZoneDeDx0p0to2p1,BaselineZoneDeDx4p0toInf,SMuValidationZLL,SElBaselineZoneDeDx0p0to2p1,SElValidationMTZoneDeDx4p0toInf,SMuValidationMTZoneDeDx2p1to4p0,SElBaselineZoneDeDx1p6to2p1,HadBaselineZoneDeDx1p6to2p1,SElBaselineZoneDeDx2p1to4p0"

    for data_period in data_periods:

        os.system("rm %s/closure_%s.root" % (options.prediction_folder, data_period))
    
        root_file = "%s/prediction_%s.root" % (options.prediction_folder, data_period)
            
        for variable in variables:
            
            for event_selection in options.selection.split(","):
                                    
                if event_selection == "baseline":
                    canvas_label = "hFkBaseline_%s" % variable
                elif event_selection == "SElValidationMT":
                    canvas_label = "hFkSElValidationMT_%s" % variable
                elif event_selection == "SMuValidationMT":
                    canvas_label = "hFkSMuValidationMT_%s" % variable
                else:
                    canvas_label = "%s_%s" % (event_selection, variable)
                
                print root_file, variable, options.category, event_selection
                
                extra_text = "%s, %s tracks" % (data_period.replace("Summer16", "2016 MC").replace("Fall17", "2017 MC"), options.category)
                closure_plot(root_file, variable, options.category, event_selection, canvas_label, fr_regions = ["qcd_lowMHT"], fr_maps = ["HT_n_allvertices"], output_root_file = options.prediction_folder + "/closure_%s.root" % (data_period), extra_text = extra_text, outpath = "%s/plots_%s_%s" % (options.prediction_folder, data_period, event_selection))

