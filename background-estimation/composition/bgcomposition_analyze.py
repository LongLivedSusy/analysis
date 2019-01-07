#!/bin/env python
from __future__ import division
import glob
import os
from ROOT import *
import CfgUtils
import numpy as np
import treeplotter
import uuid

def get_histogram(variable, cutstring, nBins=False, xmin=False, xmax=False, path="./output_tautrack", config="../cfg/samples_cmssw8_all.cfg", unweighted = False):

    unique = str(uuid.uuid1())
    
    samples = CfgUtils.update_samples_with_filenames(path, config)

    histograms = {}

    h_bg_combined = 0
    h_data_combined = 0

    for sample in samples.keys():

        if sample == "global" or sample == "total": continue
        if len(samples[sample]["filenames"]) == 0: continue            

        try:
            contents = treeplotter.get_histogram_from_file(samples[sample]["filenames"], "Events", variable, nBins=nBins, xmin=xmin, xmax=xmax, cutstring=cutstring)
        except:
            continue
        histogram = contents[0].Clone()
        histogram.SetDirectory(0)
        histogram.SetName(unique)
        
        count = histogram.GetEntries()
        nev = contents[1]
        xsec = samples[sample]["xsec"]
        lumi = samples["global"]["lumi"]
        
        if nev > 0:
            scale = lumi * xsec / nev
        else:
            scale = 0
        
        if not unweighted: histogram.Scale(scale)
        
        if samples[sample]["type"] == "b":
            
            if h_bg_combined == 0:
                h_bg_combined = histogram
            else:
                print "adding to combined bg:", sample
                h_bg_combined.Add(histogram)

    return h_bg_combined


def stack_gendisapptrks(variable, binWidth, xmin, xmax, xlabel = "", ymin = False, ymax = False, path = "", config = "../cfg/samples_cmssw8_all.cfg", base_cuts = "", suffix = "", unweighted = False, output_folder="", extra_text="", extra_text_inline = "", require_mask = False):

    if xlabel == "": xlabel = variable

    canvas = TCanvas("genparticleStack", "genparticleStack", 800, 800)  
    canvas.SetRightMargin(0.05)
    canvas.SetLogy(True)

    nBins = int(xmax/binWidth)

    if require_mask:
        base_cuts += " && (taggedtrack1_mask>0 || taggedtrack2_mask>0) "

    select_electrons = " && (taggedtrack1_bgtype==11 || taggedtrack2_bgtype==11) "
    select_muons = " && (taggedtrack1_bgtype==13 || taggedtrack2_bgtype==13) "
    select_taus = " && (taggedtrack1_bgtype==15 || taggedtrack2_bgtype==15) "
    select_nonprompt = " && (taggedtrack1_bgtype==0 || taggedtrack2_bgtype==0) "
    require_photon = " && ((taggedtrack1_gamma_DR<0.1 && taggedtrack1_gamma_ptfraction>1) || (taggedtrack2_gamma_DR<0.1 && taggedtrack2_gamma_ptfraction>1)) "
    reject_photon = " && !((taggedtrack1_gamma_DR<0.1 && taggedtrack1_gamma_ptfraction>1) || (taggedtrack2_gamma_DR<0.1 && taggedtrack2_gamma_ptfraction>1)) "

    h_electrons = get_histogram(variable, base_cuts + select_electrons + reject_photon, nBins=nBins, xmin=xmin, xmax=xmax, path=path, config=config, unweighted=unweighted)
    h_muons = get_histogram(variable, base_cuts + select_muons + reject_photon, nBins=nBins, xmin=xmin, xmax=xmax, path=path, config=config, unweighted=unweighted)
    h_taus = get_histogram(variable, base_cuts + select_taus + reject_photon, nBins=nBins, xmin=xmin, xmax=xmax, path=path, config=config, unweighted=unweighted)
    h_nonprompt = get_histogram(variable, base_cuts + select_nonprompt, nBins=nBins, xmin=xmin, xmax=xmax, path=path, config=config, unweighted=unweighted)
    h_gammaconv_electrons = get_histogram(variable, base_cuts + select_electrons + require_photon, nBins=nBins, xmin=xmin, xmax=xmax, path=path, config=config, unweighted=unweighted)
    h_gammaconv_muons = get_histogram(variable, base_cuts + select_muons + require_photon, nBins=nBins, xmin=xmin, xmax=xmax, path=path, config=config, unweighted=unweighted)
    h_gammaconv_taus = get_histogram(variable, base_cuts + select_taus + require_photon, nBins=nBins, xmin=xmin, xmax=xmax, path=path, config=config, unweighted=unweighted)
    h_gammaconv_nonprompt = get_histogram(variable, base_cuts + select_nonprompt + require_photon, nBins=nBins, xmin=xmin, xmax=xmax, path=path, config=config, unweighted=unweighted)

    mcstack = THStack("genBGstacked", "")
    legend = TLegend(0.6, 0.65, 0.89, 0.89)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    # get correct stacking order:
    integrals = {}
    integrals["h_electrons"] = h_electrons.Integral()
    integrals["h_muons"] = h_muons.Integral()
    integrals["h_taus"] = h_taus.Integral()
    integrals["h_nonprompt"] = h_nonprompt.Integral()
    integrals["h_gammaconv_electrons"] = h_gammaconv_electrons.Integral()
    integrals["h_gammaconv_muons"] = h_gammaconv_muons.Integral()
    integrals["h_gammaconv_taus"] = h_gammaconv_taus.Integral()
    integrals["h_gammaconv_nonprompt"] = h_gammaconv_nonprompt.Integral()
    print integrals    
    for key, value in sorted(integrals.iteritems(), key=lambda (k,v): (v,k)):
        print "%s: %s" % (key, value)
        eval("mcstack.Add(%s)" % key)

    h_electrons.SetFillColor(kBlue)
    h_electrons.SetLineColor(kBlack)

    h_muons.SetFillColor(kRed)
    h_muons.SetLineColor(kBlack)

    h_taus.SetFillColor(kGreen)
    h_taus.SetLineColor(kBlack)

    h_nonprompt.SetFillColor(kCyan)
    h_nonprompt.SetLineColor(kBlack)

    h_gammaconv_electrons.SetFillColor(kBlue)
    h_gammaconv_electrons.SetFillStyle(3002)
    h_gammaconv_electrons.SetLineColor(kBlack)

    h_gammaconv_muons.SetFillColor(kRed)
    h_gammaconv_muons.SetFillStyle(3002)
    h_gammaconv_muons.SetLineColor(kBlack)

    h_gammaconv_taus.SetFillColor(kGreen)
    h_gammaconv_taus.SetFillStyle(3002)
    h_gammaconv_taus.SetLineColor(kBlack)

    h_gammaconv_nonprompt.SetFillColor(kCyan)
    h_gammaconv_nonprompt.SetFillStyle(3002)
    h_gammaconv_nonprompt.SetLineColor(kBlack)

    legend.AddEntry(h_nonprompt, "non-prompt", "F")
    legend.AddEntry(h_electrons, "prompt (e^{#pm})", "F")
    legend.AddEntry(h_muons, "prompt (#mu^{#pm})", "F")
    legend.AddEntry(h_taus, "prompt (#tau^{#pm})", "F")
    legend.AddEntry(h_gammaconv_nonprompt, "#gamma conversion (non-prompt)", "F")
    legend.AddEntry(h_gammaconv_electrons, "#gamma conversion (e^{#pm})", "F")
    legend.AddEntry(h_gammaconv_muons, "#gamma conversion (#mu^{#pm})", "F")
    legend.AddEntry(h_gammaconv_taus, "#gamma conversion (#tau^{#pm})", "F")

    mcstack.Draw("hist")
    htitle = ""
    mcstack.SetTitle("%s;%s;events" % (htitle, xlabel))
    legend.Draw()

    if ymin:
        mcstack.SetMinimum(ymin)
    if ymax:
        mcstack.SetMaximum(1.5 * ymax)

    mcstack.GetYaxis().SetTitleOffset(1.3)

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)

    #latex.DrawLatex(0.95, 0.91, "%s, 150 fb^{-1} (13 TeV)" % extra_text)

    if "pixelonly" in suffix:
        extra_text_inline = "pixel-only tracks"
    elif "pixelstrips" in suffix:
        extra_text_inline = "pixel+strips tracks"

    latex.SetTextAlign(13)
    latex.SetTextFont(52)
    latex.DrawLatex(0.13, 0.87, "%s" % extra_text_inline)

    # stamp plot
    showlumi = True
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
    tl.SetTextSize(0.9*tl.GetTextSize())
    tl.DrawLatex(0.135,0.915, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(0.9*tl.GetTextSize())
    xlab = 0.213
    tl.DrawLatex(xlab,0.915, '  simulation preliminary')
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.75*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
    xthing = 0.6202
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.915,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())
    # end of stamping

    if not os.path.exists(os.getcwd() + "/" + output_folder):
        os.mkdir(os.getcwd() + "/" + output_folder)

    canvas.SaveAs(output_folder + "genBGstacked_%s%s.pdf" % (variable, suffix))
    canvas.SaveAs(output_folder + "genBGstacked_%s%s.root" % (variable, suffix))

   
if __name__ == "__main__":

    config = "../cfg/samples_cmssw8_all.cfg"
    path = "output_bgcomposition/"

    #output_folder = "plots_bgcomposition/"
    #require_mask = False

    output_folder = "plots_bgcomposition_masked/"
    require_mask = True
    
    base_cuts = "n_DT>0 && PFCaloMETRatio<5 && MHT>250"

    # do stacked background plots (stacked by background type):
   
    stack_gendisapptrks("taggedtrack1_tagid", 1, 1, 4, ymin=1e-2, xlabel="track category", path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts, suffix = "", config = config)    
    stack_gendisapptrks("taggedtrack1_pt", 50, 30, 430, ymin=1e0, xlabel="track p_{T} (GeV)", path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts, suffix = "", config = config)
    stack_gendisapptrks("taggedtrack1_pt", 50, 30, 430, ymin=1e0, xlabel="track p_{T} (GeV)", path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts + " && taggedtrack1_tagid==1", suffix = "_pixelonly", config = config)
    stack_gendisapptrks("taggedtrack1_pt", 50, 30, 430, ymin=1e0, xlabel="track p_{T} (GeV)", path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts + " && taggedtrack1_tagid==2", suffix = "_pixelstrips", config = config)

    stack_gendisapptrks("HT", 100, 0, 1000, xlabel="H_{T} (GeV)", ymin=1e0, path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts, suffix = "", config = config)
    stack_gendisapptrks("HT", 100, 0, 1000, xlabel="H_{T} (GeV)", ymin=1e0, path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts + " && taggedtrack1_tagid==1", suffix = "_pixelonly", config = config)
    stack_gendisapptrks("HT", 100, 0, 1000, xlabel="H_{T} (GeV)", ymin=1e0, path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts + " && taggedtrack1_tagid==2", suffix = "_pixelstrips", config = config)

    stack_gendisapptrks("MHT", 100, 0, 1000, xlabel="missing H_{T} (GeV)", ymin=1e0, path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts, suffix = "", config = config)
    stack_gendisapptrks("MHT", 100, 0, 1000, xlabel="missing H_{T} (GeV)", ymin=1e0, path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts + " && taggedtrack1_tagid==1", suffix = "_pixelonly", config = config)
    stack_gendisapptrks("MHT", 100, 0, 1000, xlabel="missing H_{T} (GeV)", ymin=1e0, path=path, output_folder=output_folder, require_mask = require_mask, base_cuts = base_cuts + " && taggedtrack1_tagid==2", suffix = "_pixelstrips", config = config)

    # standard stacked background plots (stacked by MC sample):

    stack_gendisapptrks("n_DT", 1, 0, 3, xlabel="n_{DT}", path=path, output_folder=output_folder, base_cuts = "PFCaloMETRatio<5 && MHT>250", suffix = "", config = config)

    plot_config = {
        "n_DT":          {"binw": 1, "xmin": 0, "xmax": 5, "xlabel": "number of DT", "ylabel": "events", "logx": False, "logy": True},
        "n_DT_realfake": {"binw": 1, "xmin": 0, "xmax": 5, "xlabel": "number of fake DT", "ylabel": "events", "logx": False, "logy": True},
                  }
    treeplotter.loop_over_files(path, config, plot_config, tree_folder_name="Events", cutstring = "PFCaloMETRatio<5 && MHT>250", ignore_samples="Run201", folder = output_folder)
