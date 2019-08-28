#!/bin/env python
import os
from ROOT import *
from plotting import *
import collections
from optparse import OptionParser
import array

def closure_plot(root_file, variable, tag, category, cr, canvas_label, extra_text = "", xlabel = False, lumi = 135000, autoscaling = True, xmax = False, ymax = False, ymin = False, fr_regions = [], fr_maps = [], output_root_file = False, pdf_output = True, outpath = "plots"):
   
    if variable == "n_jets":
        xmin = 0; xmax = 30
       
    histos = collections.OrderedDict()

    tfile = TFile(root_file, "open")

    # get histograms -- special handling for regions histogram

    if variable == "regions":

        # create empty region hists
        histos["mc_CR"] = TH1F("mc_CR", "mc_CR", 33, 0, 33)
        histos["mc_nonprompt"] = TH1F("mc_nonprompt", "mc_nonprompt", 33, 0, 33)
        histos["mc_prompt"] = TH1F("mc_prompt", "mc_prompt", 33, 0, 33)
        for fr_region in fr_regions:
            for fr_map in fr_maps:
                histos["mc_prediction_%s_%s" % (fr_region, fr_map)] = TH1F("mc_prediction_%s_%s" % (fr_region, fr_map), "mc_prediction_%s_%s" % (fr_region, fr_map), 33, 0, 33)
    
        # get histograms:
        for ivariable in ["region_short", "region_long", "region_multi"]:
            
            if ivariable == "region_short": icategory = "short"
            elif ivariable == "region_long": icategory = "long"
            elif ivariable == "region_multi": icategory = category

            htmp = {}           
            htmp["mc_nonprompt"] = tfile.Get("%s_%s_fakebg_%s_%s" % (ivariable, tag, icategory, cr) )
            htmp["mc_prompt"] = tfile.Get("%s_%s_promptbg_%s_%s" % (ivariable, tag, icategory, cr) )
            htmp["mc_CR"] = tfile.Get("%s_%s_control_%s_%s" % (ivariable, tag, icategory, cr) )               
            for fr_region in fr_regions:
                for fr_map in fr_maps:
                    htmp["mc_prediction_%s_%s" % (fr_region, fr_map)] = tfile.Get("%s_%s_%s_%s_%s_prediction_%s" % (ivariable, fr_region, tag, icategory, fr_map, cr) )

            for label in htmp:
                for ibin in range(htmp[label].GetXaxis().GetNbins()):
                    yval = htmp[label].GetBinContent(ibin+1) + histos[label].GetBinContent(ibin+1)
                    xval = htmp[label].GetXaxis().GetBinCenter(ibin+1)
                    histos[label].SetBinContent(histos[label].GetXaxis().FindBin(xval), yval)

    else:

        histos["mc_CR"] = tfile.Get("%s_%s_control_%s_%s" % (variable, tag, category, cr) )
        histos["mc_nonprompt"] = tfile.Get("%s_%s_fakebg_%s_%s" % (variable, tag, category, cr) )
        histos["mc_prompt"] = tfile.Get("%s_%s_promptbg_%s_%s" % (variable, tag, category, cr) )
        for fr_region in fr_regions:
            for fr_map in fr_maps:
                histos["mc_prediction_%s_%s" % (fr_region, fr_map)] = tfile.Get("%s_%s_%s_%s_%s_prediction_%s" % (variable, fr_region, tag, category, fr_map, cr) )
                if "BDT" in fr_map and "short" in category:
                    histos["mc_prediction_%s_%s" % (fr_region, fr_map)].Scale(10e-3)
                if "BDT" in fr_map and "long" in category:
                    histos["mc_prediction_%s_%s" % (fr_region, fr_map)].Scale(10e-4)

    # rebin histograms:
    for label in histos:
      if "HT" in variable:
          redoBinning = [0, 100, 200, 300, 400, 500, 1000]
      elif variable == "MinDeltaPhiMhtJets":
          redoBinning = [0.3,0.5,0.7,0.9]
      elif variable == "n_btags":
          redoBinning = [0,1,2,5]
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

        if not "data" in label:
            histos[label].Scale(lumi)

        if "prediction" in label or "data" in label:
            histos[label].SetMarkerStyle(22)
            histos[label].SetMarkerColor(color)
            histos[label].SetMarkerSize(1.5)

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
   
    histos["mc_prompt"].Draw("same hist e")
    histos["mc_nonprompt"].Draw("same hist e")

    legend = TLegend(0.3, 0.7, 0.89, 0.89)
    legend.SetHeader(extra_text)
    legend.SetTextSize(0.025)
    legend.AddEntry(histos["mc_CR"], "Control region (CR)")
    legend.AddEntry(histos["mc_nonprompt"], "Non-prompt background in SR (MC Truth)")
    legend.AddEntry(histos["mc_prompt"], "Prompt contamination in SR (MC Truth)")
    legend.SetBorderSize(0)

    for label in histos:
        if "prediction" in label:

            legend_label = label
            legend_label = legend_label.replace("mc_prediction_", "Non-prompt prediction (")
            legend_label = legend_label.replace("qcd_sideband_", "QCD-only, 100<MHT<200 GeV, ")
            legend_label = legend_label.replace("qcd_lowMHT_", "QCD-only, MHT<200 GeV, ")
            legend_label = legend_label.replace("HT_n_allvertices", "2D map)")
            legend.AddEntry(histos[label], legend_label)
    
            if "mc" in label:
                #gStyle.SetErrorX(0)    
                histos[label].Draw("same p")   
    
            if "data" in label:
                histos[label].SetMarkerStyle(20)
                histos[label].SetMarkerColor(kOrange)
                histos[label].SetLineColorAlpha(0, 0)
                
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
            #ratios[label] = histos[label].Clone()
            #ratios[label].Divide(histos["mc_nonprompt"])
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
        canvas.Write()
        fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--hadd", dest="hadd", action="store_true")
    parser.add_option("--path", dest="path", default="prediction")
    parser.add_option("--pdf", dest="pdf", action="store_true")
    parser.add_option("--outroot", dest="outroot", default="closure.root")
    (options, args) = parser.parse_args()

    if options.hadd:
        for data_period in ["Summer16", "Fall17"]:
            os.system("hadd -f %s %s/*%s*root" % ("prediction_%s.root" % data_period, options.path, data_period))

    #for data_period in ["Summer16", "Fall17"]:
    for data_period in ["Summer16"]:

        os.system("rm closure_%s.root" % data_period)

        root_file = "prediction_%s.root" % data_period

        for variable in ["HT", "MHT", "n_btags", "n_goodjets", "regions"]:
            for tag in ["loose5", "loose6dz1"]:
                for category in ["short", "long"]:
                    for cr in ["cr1"]:           
                        if "short" in variable and category != "short": continue
                        if "long" in variable and category != "long": continue
                        canvas_label = "prediction_%s_%s_%s_%s_%s_%s" % (data_period, variable, tag, category, "comparison", cr)


                        extra_text = "%s, %s tracks" % (data_period.replace("Summer16", "2016 MC").replace("Fall17", "2017 MC"), category)

                        #closure_plot(root_file, variable, tag, category, cr, canvas_label, fr_regions = ["qcd_lowMHT"], fr_maps = ["HT_n_allvertices", "BDT1", "BDT2", "BDT3", "BDT4", "BDT5", "BDT6", "BDT7", "BDT8", "BDT9"], output_root_file = "closure_%s.root" % data_period, pdf_output = options.pdf, outpath = "plots_%s" % data_period)
                        closure_plot(root_file, variable, tag, category, cr, canvas_label, fr_regions = ["qcd_lowMHT"], fr_maps = ["HT_n_allvertices"], output_root_file = "closure_%s.root" % data_period, pdf_output = options.pdf, extra_text = extra_text, outpath = "closure")
            

