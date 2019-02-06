#!/bin/env python
from __future__ import division
from ROOT import *
import treeplotter
from plotting import *

def fakerate_plot(variable, binWidth, xmin, xmax, xlabel = "", path = "./output", cutstring = "PFCaloMETRatio<5", foldername = "dilepton", rootfile = "fakerate.root"):
    
    if xlabel == "": xlabel = variable
    
    canvas = TCanvas("fakerate", "fakerate", 800, 800)  

    #if len(cutstring) > 0:
    #    base_cuts = cutstring + " && EvtNumEven==0"
    #else:
    #    base_cuts = "EvtNumEven==0"
    base_cuts = cutstring
   
    nBinsX = int(xmax/binWidth)

    fakes_numerator_bg = get_histogram(variable, base_cuts + " && n_DT>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample = "Summer16")
    fakes_denominator_bg = get_histogram(variable, base_cuts + " && n_DT==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample = "Summer16")
    fakes_numerator_data = get_histogram(variable, base_cuts + " && n_DT>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample = "Run2016C*Single")
    fakes_denominator_data = get_histogram(variable, base_cuts + " && n_DT==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample = "Run2016C*Single")

    fake_rate_bg = fakes_numerator_bg.Clone()
    fake_rate_bg.Divide(fakes_denominator_bg)
    fake_rate_bg.SetName("fake_rate_bg")

    fake_rate_data = fakes_numerator_data.Clone()
    fake_rate_data.Divide(fakes_denominator_data)
    fake_rate_data.SetName("fake_rate_data")
      
    #check tracks if they are close to a genParticle with status 1:  
    #if len(cutstring) > 0:
    #    base_cuts = cutstring + " && EvtNumEven==1"
    #else:
    #    base_cuts = "EvtNumEven==1"

    fakes_gen_nominator = get_histogram(variable, base_cuts + " && n_DT_actualfake>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample = "Summer16")
    fakes_gen_denominator = get_histogram(variable, base_cuts + " && n_DT_actualfake==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=path, selected_sample = "Summer16")

    fake_rate_gen = fakes_gen_nominator.Clone()
    fake_rate_gen.Divide(fakes_gen_denominator)
    fake_rate_gen.SetName("fake_rate_gen")

    fout = TFile(rootfile, "update")
    fout.mkdir(foldername)
    fout.cd(foldername)

    canvas.SetLogy(True)

    # plot absolute values of numerator and denominator:
    fakes_denominator_bg.Draw("hist")
    fakes_denominator_bg.SetLineWidth(2)
    fakes_denominator_bg.SetLineStyle(2)
    fakes_denominator_bg.SetLineColor(kBlue)

    fakes_numerator_bg.Draw("same hist")
    fakes_numerator_bg.SetLineWidth(2)
    fakes_numerator_bg.SetLineColor(kBlue)

    fakes_denominator_data.Draw("same hist")
    fakes_denominator_data.SetLineWidth(2)
    fakes_denominator_data.SetLineStyle(2)
    fakes_denominator_data.SetLineColor(kBlack)

    fakes_numerator_data.Draw("same hist")
    fakes_numerator_data.SetLineWidth(2)
    fakes_numerator_data.SetLineColor(kBlack)

    fakes_gen_denominator.Draw("same hist")
    fakes_gen_denominator.SetLineWidth(2)
    fakes_gen_denominator.SetLineStyle(2)
    fakes_gen_denominator.SetLineColor(kRed)
    
    fakes_gen_nominator.Draw("same hist")
    fakes_gen_nominator.SetLineWidth(2)
    fakes_gen_nominator.SetLineColor(kRed)
    
    fakes_denominator_bg.GetYaxis().SetRangeUser(1e1,1e8)
    fakes_denominator_bg.SetTitle(";%s;events" % xlabel)

    legend = TLegend(0.4, 0.7, 0.96, 0.96)
    legend.SetTextSize(0.025)
    legend.AddEntry(fakes_denominator_data, "denominator (data)")
    legend.AddEntry(fakes_numerator_data, "nominator (data)")
    legend.AddEntry(fakes_denominator_bg, "denominator (MC)")
    legend.AddEntry(fakes_numerator_bg, "nominator (MC)")
    legend.AddEntry(fakes_gen_denominator, "denominator (MC + GenMatching)")
    legend.AddEntry(fakes_gen_nominator, "nominator (MC + GenMatching)")
    legend.Draw()

    stamp_plot()
    canvas.SetName("%s/%s_%s_absolutes" % (foldername, foldername, variable))
    canvas.Write()

    # plot fake rates:
    canvas.Clear()
    pad1 = TPad("pad1", "pad1", 0, 0.2, 1, 1.0)
    pad1.SetRightMargin(0.05)
    pad1.SetLogy(True)
    pad2 = TPad("pad2", "pad2", 0.0, 0.025, 1.0, 0.27)
    pad2.SetBottomMargin(0.4)
    pad2.SetRightMargin(0.05)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()

    fake_rate_bg.Draw("p")
    fake_rate_bg.GetXaxis().SetLabelSize(0)
    fake_rate_bg.SetMarkerStyle(20)
    fake_rate_bg.SetMarkerColor(kBlue)
    fake_rate_bg.SetLineWidth(2)
    fake_rate_bg.SetLineColor(kBlue)

    fake_rate_data.Draw("same p")
    fake_rate_data.SetMarkerStyle(20)
    fake_rate_data.SetMarkerColor(kBlack)
    fake_rate_data.SetLineWidth(2)
    fake_rate_data.SetLineColor(kBlack)

    fake_rate_gen.Draw("same p")
    fake_rate_gen.SetMarkerStyle(5)
    fake_rate_gen.SetMarkerColor(kRed)
    fake_rate_gen.SetLineWidth(2)
    fake_rate_gen.SetLineColor(kRed)

    ymin = 1e6
    for ibin in range(fake_rate_bg.GetNbinsX()):
        value = fake_rate_bg.GetBinContent(ibin)
        if value < ymin and value > 0:
            ymin = value
    for ibin in range(fake_rate_gen.GetNbinsX()):
        value = fake_rate_gen.GetBinContent(ibin)
        if value < ymin and value > 0:
            ymin = value
    ymax = max(fake_rate_bg.GetMaximum(), fake_rate_data.GetMaximum())

    fake_rate_bg.GetYaxis().SetRangeUser(0.5*ymin, 1.5*ymax)

    fake_rate_bg.SetTitle(";;fake rate")

    legend = TLegend(0.43, 0.75, 0.94, 0.89)
    legend.SetTextSize(0.03)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.AddEntry(fake_rate_data, "Fake rate from data")

    legend.AddEntry(fake_rate_bg, "Fake rate from MC")
    legend.AddEntry(fake_rate_gen, "Fake rate from MC + truth")
    legend.Draw()

    stamp_plot()

    # ratio plot
    pad2.cd()
    ratio = fake_rate_bg.Clone()
    ratio.Divide(fake_rate_gen)
    ratio.Draw()
    ratio.SetTitle(";%s;MC/Truth" % xlabel)
    pad2.SetGridx(True)
    pad2.SetGridy(True)
    ratio.GetXaxis().SetTitleSize(0.12)
    ratio.GetYaxis().SetTitleSize(0.12)
    ratio.GetYaxis().SetTitleOffset(0.35)
    ratio.GetYaxis().SetRangeUser(0.75,1.25)
    ratio.GetYaxis().SetNdivisions(4)
    ratio.GetXaxis().SetLabelSize(0.12)
    ratio.GetYaxis().SetLabelSize(0.12)

    canvas.SetName("%s/%s_%s_fakerate" % (foldername, foldername, variable))
    canvas.Write()
    canvas.SaveAs("plots/fakerate_%s_%s.pdf" % (foldername, variable))

    fout.Close()


if __name__ == "__main__":
    
    path = "output_fakerate/"
    base_cuts = "PFCaloMETRatio<5"
    rootfile = "plots.root"

    # dilepton region
    fakerate_plot("n_allvertices", 5, 0, 50, xlabel = "n_{vertex}", rootfile = rootfile, path = path, cutstring = base_cuts + " && dilepton_CR==1", foldername = "dilepton")

    quit()

    fakerate_plot("HT_cleaned", 40, 0, 1000, xlabel = "H_{T}", rootfile = rootfile, path = path, cutstring = base_cuts + " && dilepton_CR==1", foldername = "dilepton")
    fakerate_plot("MHT_cleaned", 40, 0, 1000, xlabel = "missing H_{T}", rootfile = rootfile, path = path, cutstring = base_cuts + " && dilepton_CR==1", foldername = "dilepton")

    # QCD-only events
    fakerate_plot("n_allvertices", 5, 0, 50, xlabel = "n_{vertex}", rootfile = rootfile, path = path, cutstring = base_cuts + " && qcd_CR==1", foldername = "qcd")
    fakerate_plot("HT", 40, 0, 1000, xlabel = "H_{T}", rootfile = rootfile, path = path, cutstring = base_cuts + " && qcd_CR==1", foldername = "qcd")
    fakerate_plot("MHT", 40, 0, 1000, xlabel = "missing H_{T}", rootfile = rootfile, path = path, cutstring = base_cuts + " && qcd_CR==1", foldername = "qcd")

    # create stacked plots (using treeplotter):
    config = "../../cfg/samples_cmssw8_all.cfg"

    # z mass plot:
    plot_config = {"dilepton_invmass": {"binw": 2, "xmin": 75, "xmax": 120, "ymin": 1e5, "xlabel": "m_{ll} (GeV)", "ylabel": "events", "logx": False, "logy": True} }
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = base_cuts + " && dilepton_CR==1 && lepton_type==11", suffix="_ee", ignore_samples="Run201", folder = "plots")
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = base_cuts + " && dilepton_CR==1 && lepton_type==13", suffix="_mumu", ignore_samples="Run201", folder = "plots")

    # number of DT:
    plot_config = {"n_DT": {"binw": 1, "xmin": 0, "xmax": 3, "xlabel": "number of DT", "ylabel": "events", "logx": False, "logy": True} }
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = base_cuts + " && dilepton_CR==1", suffix="", ignore_samples="Run201", folder = "plots")




