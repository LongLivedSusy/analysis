#!/bin/env python
from __future__ import division
import os
from ROOT import *
from plotting import *

def stack_gendisapptrks(variable, binWidth, xmin, xmax, xlabel = "", ymin = False, ymax = False, path = "", selected_sample="Summer16", base_cuts = "", suffix = "", unweighted = False, output_folder="", extra_text="", extra_text_inline = "", require_mask = False, lumi=135.0):

    if xlabel == "": xlabel = variable

    canvas = TCanvas("genparticleStack", "genparticleStack", 800, 800)  
    canvas.SetRightMargin(0.05)
    canvas.SetLogy(True)

    nBins = int(xmax/binWidth)

    # with pion veto:
    #select_prompt = " && ((n_DT==1 && DT1_passpionveto==1 && DT1_promptbg==1) || (n_DT==2 && (DT1_promptbg==1 || DT2_promptbg==1)))"
    select_promptelectron = " && ((n_DT==1 && DT1_passpionveto==1 && DT1_promptelectron==1) || (n_DT==2 && DT1_passpionveto==1 && DT2_passpionveto==1 && (DT1_promptelectron==1 || DT2_promptelectron==1)))"
    select_promptmuon = " && ((n_DT==1 && DT1_passpionveto==1 && DT1_promptmuon==1) || (n_DT==2 && DT1_passpionveto==1 && DT2_passpionveto==1 && (DT1_promptmuon==1 || DT2_promptmuon==1)))"
    select_prompttau = " && ((n_DT==1 && DT1_passpionveto==1 && (DT1_prompttau==1 || DT1_prompttau_wideDR==1)) || (n_DT==2 && DT1_passpionveto==1 && DT2_passpionveto==1 && ((DT1_prompttau==1 || DT1_prompttau_wideDR==1) || (DT2_prompttau==1 || DT2_prompttau_wideDR==1))))"
    select_nonprompt = " && ((n_DT==1 && DT1_passpionveto==1 && DT1_actualfake==1) || (n_DT==2 && DT1_passpionveto==1 && DT2_passpionveto && (DT1_actualfake==1 || DT2_actualfake==1)))"

    h_promptelectron = get_histogram(variable, base_cuts + select_promptelectron, nBinsX=nBins, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample)
    h_promptmuon = get_histogram(variable, base_cuts + select_promptmuon, nBinsX=nBins, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample)
    h_prompttau = get_histogram(variable, base_cuts + select_prompttau, nBinsX=nBins, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample)
    h_nonprompt = get_histogram(variable, base_cuts + select_nonprompt, nBinsX=nBins, xmin=xmin, xmax=xmax, path=path, selected_sample=selected_sample)

    mcstack = THStack("genBGstacked", "")
    legend = TLegend(0.6, 0.65, 0.89, 0.89)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    if extra_text != "": legend.SetHeader(extra_text)

    # get correct stacking order:
    integrals = {}
    integrals["h_promptelectron"] = h_promptelectron.Integral()
    integrals["h_promptmuon"] = h_promptmuon.Integral()
    integrals["h_prompttau"] = h_prompttau.Integral()
    integrals["h_nonprompt"] = h_nonprompt.Integral()
    print integrals    
    ordered = sorted(integrals.iteritems(), key=lambda (k,v): (v,k))
    for key, value in ordered:
        print "%s: %s" % (key, value)
        eval("mcstack.Add(%s)" % key)

    ordered.reverse()
    for key, value in ordered:
        if "nonprompt" in key: label = "non-prompt"
        elif "promptelectron" in key: label = "prompt e"
        elif "promptmuon" in key: label = "prompt #mu"
        elif "prompttau" in key: label = "prompt #tau"
        eval("legend.AddEntry(%s, '%s', 'F')" % (key, label))    

    h_promptelectron.Scale(lumi)
    h_promptmuon.Scale(lumi)
    h_prompttau.Scale(lumi)
    h_nonprompt.Scale(lumi)

    h_promptelectron.SetFillColor(62)
    h_promptelectron.SetLineColor(kBlack)

    h_promptmuon.SetFillColor(97)
    h_promptmuon.SetLineColor(kBlack)

    h_prompttau.SetFillColor(85)
    h_prompttau.SetLineColor(kBlack)

    h_nonprompt.SetFillColor(67)
    h_nonprompt.SetLineColor(kBlack)

    mcstack.Draw("hist")
    htitle = ""
    mcstack.SetTitle("%s;%s;events" % (htitle, xlabel))
    legend.Draw()

    if ymin:
        mcstack.SetMinimum(ymin)
    if ymax:
        mcstack.SetMaximum(100 * ymax)

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

    #stamp plot:
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
    tl.DrawLatex(xlab,0.915, ' Work in Progress')
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
    xthing = 0.6202
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.915,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())



    latex=TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(kBlack)
    latex.SetTextFont(62)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.03)
    latex.DrawLatex(0.93, 0.91, "%.1f fb^{-1} (13 TeV)" % lumi)

    if not os.path.exists(path + "/plots"):
        os.mkdir(path + "/plots")

    canvas.SaveAs(path + "/plots/bgcomposition_%s%s.pdf" % (variable, suffix))
    canvas.SaveAs(path + "/plots/bgcomposition_%s%s.root" % (variable, suffix))

   
if __name__ == "__main__":

    #path = "output_fakerate5_merged/"  
    path = "output_skim22_merged/"
    base_cuts = "PFCaloMETRatio<5"
    selected_sample = "Summer16"

    base_cuts += " && passesUniversalSelection==1 && PFCaloMETRatio<5 && MHT>250 && n_jets>0 && n_leptons==0"

    extra_text = "signal region"
    suffix = ""
    
    # do stacked background plots (stacked by background type):

    categories = {"short": " && DT1_is_pixel_track==1", "long": " && DT1_is_pixel_track==0"}

    for label in categories:
        stack_gendisapptrks("n_DT", 1, 0, 3, xlabel="n_{DT}", path=path, selected_sample=selected_sample, base_cuts = base_cuts + categories[label], extra_text= "%s, %s tracks" % (extra_text, label), suffix=suffix + "_" + label)       
        stack_gendisapptrks("HT", 50, 0, 1000, xlabel="H_{T} (GeV)", path=path, selected_sample=selected_sample, base_cuts = base_cuts + categories[label], extra_text= "%s, %s tracks" % (extra_text, label), suffix=suffix + "_" + label)
        stack_gendisapptrks("MHT", 50, 0, 1000, xlabel="missing H_{T} (GeV)", path=path, selected_sample=selected_sample, base_cuts = base_cuts + categories[label], extra_text= "%s, %s tracks" % (extra_text, label), suffix=suffix + "_" + label)
        stack_gendisapptrks("DT1_pt", 50, 0, 500, xlabel="p_{T}^{DT} (GeV)", path=path, selected_sample=selected_sample, base_cuts = base_cuts + categories[label], extra_text= "%s, %s tracks" % (extra_text, label), suffix=suffix + "_" + label, ymin=1e-2)


