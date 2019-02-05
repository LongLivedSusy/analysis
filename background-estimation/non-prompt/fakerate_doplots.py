#!/bin/env python
from __future__ import division
import glob
from ROOT import *
import numpy as np
import uuid
import os
import treeplotter

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

def stamp_plot():

    # from Sam:
    showlumi = False
    lumi = 150
    tl = TLatex()
    tl.SetNDC()
    cmsTextFont = 61
    extraTextFont = 52
    lumiTextSize = 0.6
    lumiTextOffset = 0.2
    cmsTextSize = 0.75
    cmsTextOffset = 0.1
    regularfont = 42
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(0.85*tl.GetTextSize())
    tl.DrawLatex(0.135,0.915, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(1.0/0.85*tl.GetTextSize())
    xlab = 0.213
    tl.DrawLatex(xlab,0.915, ' preliminary')
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
    xthing = 0.6202
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.915,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())


def get_histogram_from_tree(tree, var, cutstring="", drawoptions="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False):

    hName = str(uuid.uuid1()).replace("-", "")

    if not nBinsY:
        histo = TH1F(hName, hName, nBinsX, xmin, xmax)
    else:
        histo = TH2F(hName, hName, nBinsX, xmin, xmax, nBinsY, ymin, ymax)

    tree.Draw("%s>>%s" % (var, hName), cutstring, drawoptions)

    # add overflow bin(s) for 1D and 2D histograms:
    if not nBinsY:
        bin = histo.GetNbinsX()+1
        overflow = histo.GetBinContent(bin)
        histo.AddBinContent((bin-1), overflow)
    else:
        binX = histo.GetNbinsX()+1
        binY = histo.GetNbinsX()+1

        # read and set overflow x values:
        for x in range(0, binX-1):
            overflow_up = histo.GetBinContent(x, binY)
            bin = histo.GetBin(x, binY-1)
            histo.SetBinContent(bin, overflow_up)

        # read and set overflow y values:
        for y in range(0, binY-1):
            overflow_right = histo.GetBinContent(binX, y)
            bin = histo.GetBin(binX-1, y)
            histo.SetBinContent(bin, overflow_right)

        # read and set overflow diagonal values:
        overflow_diag = histo.GetBinContent(binX, binY)
        bin = histo.GetBin(binX-1, binY-1)
        histo.SetBinContent(bin, overflow_diag)
   
    histo.SetDirectory(0)
    return histo


def get_histogram_from_file(tree_files, tree_folder_name, variable, cutstring=False, nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, file_contains_histograms=False, scaling=True):

    is_data = False
    tree = TChain(tree_folder_name)       

    for tree_file in tree_files:
        tree.Add(tree_file)
        if "Run201" in tree_file:
            is_data = True

    if not nBinsY:
        histo = get_histogram_from_tree(tree, variable, cutstring=cutstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax)
    else:
        histo = get_histogram_from_tree(tree, variable, cutstring=cutstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)

    if scaling and not is_data:

        # get number of entries:
        nev = 0
        xsec = 0
        for tree_file in tree_files:
            fin = TFile(tree_file)

            if fin.Get("Nev"):
                hnev = fin.Get("Nev")
                i_nev = hnev.GetBinContent(1)
            elif fin.Get("nev"):
                hnev = fin.Get("nev")
                i_nev = hnev.GetBinContent(1)
            nev += i_nev

            if xsec == 0 and fin.Get("xsec"):
                hxsec = fin.Get("xsec")
                xsec = hxsec.GetBinContent(1)

            fin.Close()

        # scale histogram to 1/fb:
        if nev > 0:
            histo.Scale(xsec/nev)

    return histo


def get_histogram(variable, cutstring, nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, path="./output_tautrack", selected_sample = "Run2016"):

    unique = str(uuid.uuid1())
    
    histograms = {}
    h_combined = 0
    file_names = glob.glob(path + "/*root")
    
    samples = []
    for file_name in file_names:
        identifier = "_".join(file_name.split("_")[:-3])
    
        selectors = selected_sample.split("*")
        count = 0
        for selector in selectors:
            if selector in identifier:
                count += 1
        if count == len(selectors):
            samples.append(identifier)
            
    samples = list(set(samples))

    for sample in samples:

        filenames = glob.glob(sample + "*root")

        if not nBinsY:
            histogram = get_histogram_from_file(filenames, "Events", variable, nBinsX=nBinsX, xmin=xmin, xmax=xmax, cutstring=cutstring).Clone()
        else:
            histogram = get_histogram_from_file(filenames, "Events", variable, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, cutstring=cutstring).Clone()

        histogram.SetDirectory(0)
        histogram.SetName(unique)
               
        if h_combined == 0:
            h_combined = histogram
        else:
            h_combined.Add(histogram)

    return h_combined


def create_2D_plots(path = "output/", variables = "HT_cleaned:n_allvertices", nBinsX=10, xmin=0, xmax=50, nBinsY=10, ymin=0, ymax=1000, rootfile = False, foldername = "dilepton", label = "mc", selected_sample = "Summer16", base_cuts = "PFCaloMETRatio<5", numerator_cuts = "", denominator_cuts = "", extra_text = "combined MC background"):

    fakes_numerator = get_histogram(variables, base_cuts + numerator_cuts + " && n_DT>0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample = selected_sample)
    fakes_denominator = get_histogram(variables, base_cuts + denominator_cuts + " && n_DT==0", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, path=path, selected_sample = selected_sample)

    try:
        print fakes_numerator.GetEntries()
        print fakes_denominator.GetEntries()
    except:
        print "Error while getting histogram!"
        return

    fout = TFile(rootfile, "update")
    fout.mkdir(foldername)
    fout.cd(foldername)

    fakes_numerator.SetName("%s_numerator_%s" % (foldername, label))
    fakes_numerator.Write()
    fakes_denominator.SetName("%s_denominator_%s" % (foldername, label))
    fakes_denominator.Write()

    fake_rate = fakes_numerator.Clone()
    fake_rate.Divide(fakes_denominator)
    fake_rate.SetName("%s_fake_rate_%s" % (foldername, label))
    fake_rate.SetTitle(";number of vertices; H_{T} (GeV); fake rate")
    fake_rate.GetZaxis().SetTitleOffset(1.5)
    fake_rate.GetZaxis().SetRangeUser(1e-6, 1e-1)
    fake_rate.SetName("%s_fake_rate_%s" % (foldername, label))
    fake_rate.Write()
  
    canvas = TCanvas("fakerate", "fakerate", 800, 800)  
    canvas.SetRightMargin(0.16)
    canvas.SetLeftMargin(0.14)
    canvas.SetLogz(True)

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)
    latex.SetTextAlign(13)
    latex.SetTextFont(52)

    fake_rate.Draw("COLZ")
    latex.DrawLatex(0.18, 0.87, extra_text)
    stamp_plot()
    canvas.Write("%s_canvas_%s_%s" % (foldername, label, variables.replace(":", "-")))
    canvas.SaveAs("plots/fakerate_%s_%s_%s.pdf" % (foldername, label, variables.replace(":", "-")))

    fout.Close()


def create_1D_plot(variable, binWidth, xmin, xmax, xlabel = "", path = "./output", cutstring = "PFCaloMETRatio<5", foldername = "dilepton", rootfile = "fakerate.root"):
    
    if xlabel == "": xlabel = variable
    
    canvas = TCanvas("fakerate", "fakerate", 800, 800)  

    if len(cutstring) > 0:
        base_cuts = cutstring + " && EvtNumEven==0"
    else:
        base_cuts = "EvtNumEven==0"
   
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
    if len(cutstring) > 0:
        base_cuts = cutstring + " && EvtNumEven==1"
    else:
        base_cuts = "EvtNumEven==1"

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
    ratio.GetYaxis().SetRangeUser(0,2)
    ratio.GetYaxis().SetNdivisions(4)
    ratio.GetXaxis().SetLabelSize(0.12)
    ratio.GetYaxis().SetLabelSize(0.12)

    canvas.SetName("%s/%s_%s_fakerate" % (foldername, foldername, variable))
    canvas.Write()
    canvas.SaveAs("plots/fakerate_%s_%s" % (foldername, variable))

    fout.Close()


if __name__ == "__main__":
    
    path = "output_fakerate/"
    base_cuts = "PFCaloMETRatio<5"

    create_fakerate_maps_dilepton = 1
    create_fakerate_maps_qcd = 1
    create_1Dplots = 0
    create_stacked_plots = 0

    os.system("rm fakerate-updated.root")
    rootfile = "fakerate-updated.root"

    cut_is_short_track = " && ((n_DT==1 && DT1_is_pixel_track == 1) || (n_DT==2 && DT1_is_pixel_track == 1 && DT2_is_pixel_track == 1)) "
    cut_is_long_track  = " && ((n_DT==1 && DT1_is_pixel_track == 0) || (n_DT==2 && DT1_is_pixel_track == 0 && DT2_is_pixel_track == 0)) "

    if create_fakerate_maps_dilepton:
        create_2D_plots(path = path, rootfile = rootfile, foldername = "dilepton", variables = "HT_cleaned:n_allvertices", base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_short_track, label = "bg_short", selected_sample = "Summer16", extra_text = "combined MC background, pixel-only tracks")
        create_2D_plots(path = path, rootfile = rootfile, foldername = "dilepton", variables = "HT_cleaned:n_allvertices", base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_long_track, label = "bg_long", selected_sample = "Summer16", extra_text = "combined MC background, pixel+strips tracks")
        
        for period in ["2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H"]:
            create_2D_plots(path = path, rootfile = rootfile, foldername = "dilepton", variables = "HT_cleaned:n_allvertices", base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_short_track, label = period + "_short", selected_sample = "%s*Single" % period, extra_text = "Run%s SingleElectron + SingleMuon, pixel-only tracks" % period)
            create_2D_plots(path = path, rootfile = rootfile, foldername = "dilepton", variables = "HT_cleaned:n_allvertices", base_cuts = base_cuts + " && dilepton_CR==1", numerator_cuts = cut_is_long_track, label = period + "_long", selected_sample = "%s*Single" % period, extra_text = "Run%s SingleElectron + SingleMuon, pixel+strips tracks" % period)

    if create_fakerate_maps_qcd:
        create_2D_plots(path = path, rootfile = rootfile, foldername = "qcd", variables = "HT:n_allvertices", base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_short_track, label = "bg_short", selected_sample = "Summer16*QCD", extra_text = "combined MC background, pixel-only tracks")
        create_2D_plots(path = path, rootfile = rootfile, foldername = "qcd", variables = "HT:n_allvertices", base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_long_track, label = "bg_long", selected_sample = "Summer16*QCD", extra_text = "combined MC background, pixel+strips tracks")
        
        for period in ["2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2016H"]:
            create_2D_plots(path = path, rootfile = rootfile, foldername = "qcd", variables = "HT:n_allvertices", base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_short_track, label = period + "_short", selected_sample = "%s*JetHT" % period, extra_text = "Run%s JetHT, pixel-only tracks" % period)
            create_2D_plots(path = path, rootfile = rootfile, foldername = "qcd", variables = "HT:n_allvertices", base_cuts = base_cuts + " && qcd_CR==1", numerator_cuts = cut_is_long_track, label = period + "_long", selected_sample = "%s*JetHT" % period, extra_text = "Run%s JetHT, pixel+strips tracks" % period)
            
    if create_1Dplots:
        create_1D_plot("n_allvertices", 5, 0, 50, xlabel = "n_{vertex}", rootfile = rootfile, path = path, cutstring = base_cuts + " && dilepton_CR==1", foldername = "dilepton")
        create_1D_plot("HT_cleaned", 40, 0, 1000, xlabel = "H_{T}", rootfile = rootfile, path = path, cutstring = base_cuts + " && dilepton_CR==1", foldername = "dilepton")
        create_1D_plot("MHT_cleaned", 40, 0, 1000, xlabel = "missing H_{T}", rootfile = rootfile, path = path, cutstring = base_cuts + " && dilepton_CR==1", foldername = "dilepton")
        create_1D_plot("n_allvertices", 5, 0, 50, xlabel = "n_{vertex}", rootfile = rootfile, path = path, cutstring = base_cuts + " && qcd_CR==1", foldername = "qcd")
        create_1D_plot("HT", 40, 0, 1000, xlabel = "H_{T}", rootfile = rootfile, path = path, cutstring = base_cuts + " && qcd_CR==1", foldername = "qcd")
        create_1D_plot("MHT", 40, 0, 1000, xlabel = "missing H_{T}", rootfile = rootfile, path = path, cutstring = base_cuts + " && qcd_CR==1", foldername = "qcd")

    if create_stacked_plots:

        # use treeplotter to create a stacked plot of the invariant mass and number of DT:
        config = "../../cfg/samples_cmssw8_all.cfg"

        # z mass:
        plot_config = {"dilepton_invmass": {"binw": 2, "xmin": 75, "xmax": 120, "ymin": 1e5, "xlabel": "m_{ll} (GeV)", "ylabel": "events", "logx": False, "logy": True} }
        treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = base_cuts + " && dilepton_CR==1 && lepton_type==11", suffix="_ee", ignore_samples="Run201", folder = "plots")
        treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = base_cuts + " && dilepton_CR==1 && lepton_type==13", suffix="_mumu", ignore_samples="Run201", folder = "plots")

        # number of DT:
        plot_config = {"n_DT": {"binw": 1, "xmin": 0, "xmax": 3, "xlabel": "number of DT", "ylabel": "events", "logx": False, "logy": True} }
        treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = base_cuts + " && dilepton_CR==1", suffix="", ignore_samples="Run201", folder = "plots")




