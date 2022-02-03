#!/bin/env python
from __future__ import division
from ROOT import *
import GridEngineTools
import plotting
import os
import collections
import shared_utils
import glob
from array import array
from optparse import OptionParser
 
binnings = {
            #"n_goodjets":                            [ 10, 0, 10, "number of jets"],
            "MHT":                                    [ [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 700], 0, 700, "missing H_{T} (GeV)"],
            #"HT":                                    [ [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 700], 0, 700, "H_{T} (GeV)"],
            "leadinglepton_pt":                       [ [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 176, 200, 250, 500], 0, 500, "leading p_{T}^{lep} (GeV)"],
            "leadingelectron_pt":                     [ [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 176, 200, 250, 500], 0, 500, "p_{T}^{el} (GeV)"],
            "leadingmuon_pt":                         [ [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 176, 200, 250, 500], 0, 500, "p_{T}^{#mu} (GeV)"],
            "leadinglepton_pt:MHT":                   [ [0, 50, 100, 150, 200, 300, 700], 0, 700, [0, 30, 60, 90, 200, 500], 0, 500, "missing H_{T} (GeV); p_{T}^{lep} (GeV)"],  
            "leadingelectron_pt:MHT":                 [ [0, 50, 100, 150, 200, 300, 700], 0, 700, [0, 30, 60, 90, 200, 500], 0, 500, "missing H_{T} (GeV); p_{T}^{lep} (GeV)"],  
            "leadingmuon_pt:MHT":                     [ [0, 50, 100, 150, 200, 300, 700], 0, 700, [0, 30, 60, 90, 200, 500], 0, 500, "missing H_{T} (GeV); p_{T}^{lep} (GeV)"],  
            #"leadinglepton_eta:leadinglepton_phi":   [ 20, -3.2, 3.2, "phi; eta" ],
           }

def savetoroot(obj, label, outputfolder, folderlabel):
    
    obj.SetName(label)
    if "h_" in label:
        obj.SetDirectory(0)
    fout = TFile(outputfolder + "/" + label + ".root", "recreate")
    fout.mkdir(folderlabel)
    fout.cd(folderlabel)
    obj.Write()
    fout.Write()
    fout.Close()


def stamp_cuts(cuts_channel, channel, variable, use_or_trigger, denom_label, extra_label):
    
    cuts_channel = cuts_channel.replace("n_goodelectrons", "n_{el}")
    cuts_channel = cuts_channel.replace("n_goodmuons", "n_{#mu}")
    
    if ":" in variable:
        yoffset = 0.35
    else:
        yoffset = 0

    tl2 = TLatex()
    tl2.SetNDC()
    #tl2.SetTextFont(50)
    tl2.SetTextSize(0.027)
    if channel == "MHT":
        tl2.DrawLatex(0.15, 0.27 + yoffset, "#epsilon = #frac{n_{ev}(MHT trigger & %s)}{n_{ev}(%s)} " % (denom_label, denom_label))
    elif channel == "SEl":
        if use_or_trigger:
            tl2.DrawLatex(0.15, 0.27 + yoffset, "#epsilon = #frac{n_{ev}((el. || MHT trigger) & %s)}{n_{ev}(%s)} " % (denom_label, denom_label)) 
        else:
            tl2.DrawLatex(0.15, 0.27 + yoffset, "#epsilon = #frac{n_{ev}(el. trigger & %s)}{n_{ev}%s)} " % (denom_label, denom_label)) 
    elif channel == "SMu":
        if use_or_trigger:
            tl2.DrawLatex(0.15, 0.27 + yoffset, "#epsilon = #frac{n_{ev}((#mu || MHT trigger) trigger & %s)}{n_{ev}(%s)} " % (denom_label, denom_label))
        else:
            tl2.DrawLatex(0.15, 0.27 + yoffset, "#epsilon = #frac{n_{ev}(#mu trigger & %s)}{n_{ev}(%s)} " % (denom_label, denom_label))
    
    if ":" not in variable:
        cuts_channel_minus1 = plotting.get_nMinus1_cuts(cuts_channel, variable)
    else:
        cuts_channel_minus1 = plotting.get_nMinus1_cuts(cuts_channel, variable.split(":")[0])
        cuts_channel_minus1 = plotting.get_nMinus1_cuts(cuts_channel_minus1, variable.split(":")[1])
        
    cuts_channel_minus1 = cuts_channel_minus1.replace(" && ", ", ")
    cuts_channel_minus1 = cuts_channel_minus1.replace(" &&", "")
    cuts_channel_minus1 = cuts_channel_minus1.replace(" || ", " or ")
    cuts_channel_minus1 = cuts_channel_minus1.replace(" ||", "")
    cuts_channel_minus1 = cuts_channel_minus1.replace("n_goodjets", "nJet")
    cuts_channel_minus1 = cuts_channel_minus1.replace(">=", "#geq")
    cuts_channel_minus1 = cuts_channel_minus1.replace("<=", "#leq")
    cuts_channel_minus1 = cuts_channel_minus1.replace("==", "=")
    
    if cuts_channel_minus1[-1] == ",":
        cuts_channel_minus1 = cuts_channel_minus1[:-1]
    elif cuts_channel_minus1[-2] == ",":
        cuts_channel_minus1 = cuts_channel_minus1[:-2]
        
    tl2.DrawLatex(0.15, 0.40 + yoffset, extra_label)
    tl2.DrawLatex(0.15, 0.35 + yoffset, cuts_channel_minus1)


def combinedplots(channel, variable, outputfolder, folderlabel, cuts_channel, skim_folder, use_or_trigger = True):
   
    if channel == "SEl" and "leadingmuon" in variable:
        return
    if channel == "SMu" and "leadingelectron" in variable:
        return
    
    numevents = -1
    
    pdffile = "%s/triggereff_%s_%s.pdf" % (outputfolder, folderlabel, variable.replace(":", "-"))
    
    histos = {}      
      
    # select/unselect specific run period:
    period = ""

    for year in [
                2016,
                2017,
                2018,
                ]:

        if channel == "MHT":
            glob_mht_num =   "Run%s%s*SingleElectron*.root" % (year, period)
            glob_mht_denom = "Run%s%s*SingleElectron*.root" % (year, period)
            denom = "triggered_singleelectron==1"
            denom_label = "el trigger"
            extra_label = "num.: JetHT, denom.: SingleMu"

        # switches
        if "useswitchdenom" in folderlabel:
            glob_sel_num =   "Run%s%s*SingleMuon*.root" % (year, period)
            glob_sel_denom = "Run%s%s*SingleMuon*.root" % (year, period)
            glob_smu_num =   "Run%s%s*SingleElectron*.root" % (year, period)
            glob_smu_denom = "Run%s%s*SingleElectron*.root" % (year, period)
            if channel == "SEl":
                denom = "triggered_singlemuon==1"
                denom_label = "mu trigger"
                extra_label = "SingleMuon dataset"
            elif channel == "SMu":
                denom = "triggered_singleelectron==1"
                denom_label = "el trigger"
                extra_label = "SingleElectron dataset"

        elif "usejethtother" in folderlabel:
            glob_sel_num =   "Run%s%s*JetHT*.root" % (year, period)
            glob_sel_denom = "Run%s%s*SingleMuon*.root" % (year, period)
            glob_smu_num =   "Run%s%s*JetHT*.root" % (year, period)
            glob_smu_denom = "Run%s%s*SingleElectron*.root" % (year, period)
            if channel == "SEl":
                denom = "triggered_singlemuon==1"
                denom_label = "mu trigger"
                extra_label = "num.: JetHT, denom.: SingleMu"
            elif channel == "SMu":
                denom = "triggered_singleelectron==1"
                denom_label = "el trigger"
                extra_label = "num.: JetHT, denom.: SingleEl"

        elif "usejetht" in folderlabel:
            glob_sel_num =   "Run%s%s*JetHT*.root" % (year, period)
            glob_sel_denom = "Run%s%s*JetHT*.root" % (year, period)
            glob_smu_num =   "Run%s%s*JetHT*.root" % (year, period)
            glob_smu_denom = "Run%s%s*JetHT*.root" % (year, period)
            denom = "triggered_ht==1"
            denom_label = "HT trigger"
            extra_label = "JetHT dataset"

        else:
            glob_sel_num =   "Run%s%s*MET*.root" % (year, period)
            glob_sel_denom = "Run%s%s*MET*.root" % (year, period)
            glob_smu_num =   "Run%s%s*MET*.root" % (year, period)
            glob_smu_denom = "Run%s%s*MET*.root" % (year, period)
            denom = "triggered_met==1"
            denom_label = "MHT trigger"
            extra_label = "MET dataset"
            use_or_trigger = False
                    
        if ":" in variable:
            nMinus1 = False
        else:
            nMinus1 = True
    
        nBinsX = binnings[variable][0]
        xmin = binnings[variable][1]
        xmax = binnings[variable][2]
        
        if ":" in variable:
            nBinsY = binnings[variable][3]
            ymin = binnings[variable][4]
            ymax = binnings[variable][5]
        else:
            nBinsY = False
            ymin = False
            ymax = False
        
        def get_treff_histogram(globstring, variable, cutA, cutB):
            if year == 2018 and "SingleElectron" in globstring:
                globstring = globstring.replace("SingleElectron", "EGamma")
            histo = plotting.get_all_histos([skim_folder + "/" + globstring], "Events", variable, numevents=numevents, nMinus1=nMinus1, cutstring=cuts_channel + cutA + cutB , nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)        
            histo.SetDirectory(0)
            return histo
        
        # denominator:
        if channel == "MHT":
            histos["num_%s_%s_%s" % (variable, channel, year)] = get_treff_histogram(glob_mht_num, variable, denom, " && triggered_met==1")
            histos["denom_%s_%s_%s" % (variable, channel, year)] = get_treff_histogram(glob_mht_denom, variable, denom, "")
        elif channel == "SEl":
            if use_or_trigger:
                histos["num_%s_%s_%s" % (variable, channel, year)] = get_treff_histogram(glob_sel_num, variable, denom, " && (triggered_met==1 || triggered_singleelectron==1)")
            else:
                histos["num_%s_%s_%s" % (variable, channel, year)] = get_treff_histogram(glob_sel_num, variable, denom, " && triggered_singleelectron==1")
            histos["denom_%s_%s_%s" % (variable, channel, year)] = get_treff_histogram(glob_sel_denom, variable, denom, "")
        elif channel == "SMu":
            if use_or_trigger:
                histos["num_%s_%s_%s" % (variable, channel, year)] = get_treff_histogram(glob_smu_num, variable, denom, " && (triggered_met==1 || triggered_singlemuon==1)")
            else:
                histos["num_%s_%s_%s" % (variable, channel, year)] = get_treff_histogram(glob_smu_num, variable, denom, " && triggered_singlemuon==1")
            histos["denom_%s_%s_%s" % (variable, channel, year)] = get_treff_histogram(glob_smu_denom, variable, denom, "")            
                 
    c1 = shared_utils.mkcanvas("c1")
    
    #legend = TLegend(0.5, 0.2, 0.88, 0.4)
    legend = TLegend(0.55, 0.2, 0.88, 0.5)
    legend.SetTextSize(0.03)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    
    if ":" not in variable:
        if isinstance(binnings[variable][0], list):
            histo = TH1F("histo", "", len(binnings[variable][0])-1, array('d', binnings[variable][0]))
        else:
            histo = TH1F("histo", "", binnings[variable][0], binnings[variable][1], binnings[variable][2])
    else:
        if isinstance(binnings[variable][0], list):
            histo = TH2F("histo", "", len(binnings[variable][0])-1, array('d', binnings[variable][0]), len(binnings[variable][3])-1, array('d', binnings[variable][3]))
        else:
            histo = TH2F("histo", "", binnings[variable][0], binnings[variable][1], binnings[variable][2], binnings[variable][3], binnings[variable][4], binnings[variable][5])
    
    if ":" not in variable:
        histo.SetTitle(";%s; trigger efficiency #epsilon" % binnings[variable][3])
    else:
        histo.SetTitle(";%s; trigger efficiency #epsilon" % binnings[variable][6])
    
    shared_utils.histoStyler(histo)
    
    gStyle.SetPaintTextFormat("4.2f")

    if ":" not in variable:
        histo.Draw("hist")
        histo.GetYaxis().SetRangeUser(0,1.1)
        c1.SetLogy(False)
        c1.SetLogz(False)
    else:
        histo.Draw("colz text e")
        histo.GetZaxis().SetRangeUser(0, 1)
        histo.GetZaxis().SetTitle("trigger efficiency #epsilon")
        c1.SetRightMargin(.13)
        size = 0.15
        font = 132
        histo.GetZaxis().SetLabelFont(font)
        histo.GetZaxis().SetTitleFont(font)
        histo.GetZaxis().SetTitleSize(size)
        histo.GetZaxis().SetLabelSize(size)
        histo.GetZaxis().SetTitleOffset(1)
        c1.SetLogy(False)
        c1.SetLogz(False)
    
    h_effs = {}
    for i_year, year in enumerate([2016, 2017, 2018]):
        
        denom = histos["denom_%s_%s_%s" % (variable, channel, year)].Clone()
        num = histos["num_%s_%s_%s" % (variable, channel, year)].Clone()
            
        if "normalizeDenom" in folderlabel:
            # calc. eff with normalizing to denominator
            numNormEff = num.Clone()
            denomNormEff = denom.Clone()
            if denom.Integral()>0:
                numNormEff.Scale(1.0/denom.Integral())
            if denom.Integral()>0:
                denomNormEff.Scale(1.0/denom.Integral())
            h_effs["eff_%s" % year] = numNormEff.Clone()
            h_effs["eff_%s" % year].Divide(denomNormEff)
            if "altern." not in extra_label:
                extra_label += "; altern."
        else:
            # default TEfficiency
            h_effs["eff_%s" % year] = TEfficiency(num.Clone(), denom.Clone())
        
        if ":" not in variable:
            # 1D histograms:
            h_effs["eff_%s" % year].Draw("same")
            h_effs["eff_%s" % year].SetLineWidth(2)

            if year == 2016:
                print "extra"
                numNorm = num.Clone()
                denomNorm = denom.Clone()
                if num.Integral()>0:
                    numNorm.Scale(1.0/num.Integral())
                if denom.Integral():
                    denomNorm.Scale(1.0/denom.Integral())
                denomNorm.SetLineColor(kBlue)
                denomNorm.SetFillColor(kBlue)
                denomNorm.SetFillStyle(3354)
                denomNorm.Draw("hist f same")
                numNorm.SetLineColor(kTeal)
                numNorm.SetFillColor(kTeal)
                numNorm.SetFillStyle(3345)
                numNorm.Draw("hist f same")

                legend.AddEntry(numNorm, "2016 norm. numerator", "f")
                legend.AddEntry(denomNorm, "2016 norm. denominator", "f")
                #legend.AddEntry(numNorm, "2016 numerator", "f")
                #legend.AddEntry(denomNorm, "2016 denominator", "f")
                            
        else:
            # 2D histograms:
            h_effs["eff_%s" % year].Draw("colz text e same")

            stamp_cuts(cuts_channel, channel, variable, use_or_trigger, denom_label, extra_label)
            #shared_utils.stamp()
            c1.SaveAs(pdffile.replace(".pdf", "_%s.pdf" % year))
            #savetoroot(c1, "c_triggereff_%s_%s_%s" % (channel, variable.replace(":", "-"), year), outputfolder, folderlabel)
            #savetoroot(h_effs["eff_%s" % year], "h_triggereff_%s_%s_%s" % (channel, variable.replace(":", "-"), year), outputfolder, folderlabel)
           
            return 0

    h_effs["eff_2016"].SetFillColorAlpha(0, 0)    
    h_effs["eff_2017"].SetFillColorAlpha(0, 0)    
    h_effs["eff_2018"].SetFillColorAlpha(0, 0)    
    
    h_effs["eff_2016"].SetLineColor(kBlue)    
    if channel == "MHT":
        legend.AddEntry(h_effs["eff_2016"], "2016")
    else:
        legend.AddEntry(h_effs["eff_2016"], "2016, %s" % channel)
    h_effs["eff_2017"].SetLineColor(kRed)    
    if channel == "MHT":
        legend.AddEntry(h_effs["eff_2017"], "2017")
    else:
        legend.AddEntry(h_effs["eff_2017"], "2017, %s" % channel)
    h_effs["eff_2018"].SetLineColor(kGreen+2)
    if channel == "MHT":
        legend.AddEntry(h_effs["eff_2018"], "2018")
    else:
        legend.AddEntry(h_effs["eff_2018"], "2018, %s" % channel)
    
    stamp_cuts(cuts_channel, channel, variable, use_or_trigger, denom_label, extra_label)
    shared_utils.stamp()
  
    legend.Draw()
    
    c1.SetGrid(True)
    
    c1.SaveAs(pdffile)
    savetoroot(h_effs["eff_2016"], "h_triggereff_%s_%s_2016" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)
    savetoroot(h_effs["eff_2017"], "h_triggereff_%s_%s_2017" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)
    savetoroot(h_effs["eff_2018"], "h_triggereff_%s_%s_2018" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)
    savetoroot(c1, "c_triggereff_%s_%s" % (folderlabel, variable.replace(":", "-")), outputfolder, folderlabel)


if __name__ == "__main__":
       
    parser = OptionParser()
    parser.add_option("--channel", dest = "channel", default = False)
    parser.add_option("--variable", dest = "variable", default = False)
    parser.add_option("--outputfolder", dest = "outputfolder", default = "plots")
    parser.add_option("--label", dest = "label", default = "trigger")
    parser.add_option("--cuts", dest = "cuts", default = "0")
    parser.add_option("--runmode", dest = "runmode", default = "multi")
    parser.add_option("--skim", dest = "skim_folder", default = "../ntupleanalyzer/skim_126_leadingtrigger_merged2/")
    (options, args) = parser.parse_args()

    if not options.channel:

        cmds = []
                    
        cuts_mht = {
                #"mht-baseline":                          "HT>150 && MHT>150 && n_goodjets>=1 && ",
                #"mht-baseline-fullcuts":                 "n_goodelectrons==0 && n_goodmuons==0 && HT>150 && MHT>150 && n_goodjets>=1 && ",
                #"mht-baseline-fullcuts300":              "n_goodelectrons==0 && n_goodmuons==0 && HT>300 && MHT>150 && n_goodjets>=1 && ",
                   }

        cuts_sel = {
                #"usejetht-sel-mht30":                    "HT>30 && MHT>30 && n_goodjets>=1 && leadinglepton_type==11 && ",
                #"useswitchdenom-sel-mht30":              "HT>30 && MHT>30 && n_goodjets>=1 && leadinglepton_type==11 && n_goodelectrons>=1 && n_goodmuons>=1 && ",
                #"useswitchdenom-sel-mht30":              "HT>30 && MHT>30 && n_goodjets>=1 && leadinglepton_type==11 && ",
                #"useswitchdenom-sel-mht30":              "HT>30 && MHT>30 && n_goodjets>=1 && ",
                #"useswitchdenom-sel-mincuts":            "leadinglepton_type==11 && n_goodelectrons>=1 && n_goodmuons>=1 && ",
                "useswitchdenom-sel":                     "HT>30 && MHT>30 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons>=1 && ",
                #"usejetht-sel-mht300":                   "HT>30 && MHT>300 && n_goodjets>=1 && ",
                #"usejethtother-sel-mht300":              "HT>30 && MHT>300 && n_goodjets>=1 && ",
                #"useswitchdenom-sel-mht300":             "HT>30 && MHT>300 && n_goodjets>=1 && ",
                #"usemet-sel-baseline":                   "HT>30 && MHT>30 && n_goodjets>=1 && ",
                #"sel-mht50":                             "HT>30 && MHT>30 && MHT<50 && n_goodjets>=1 && ",
                #"sel-baseline-fullcuts":                 "n_goodelectrons==1 && n_goodmuons==0 && HT>30 && MHT>30 && n_goodjets>=1 && ",
                #"sel-baseline-fullcuts300":              "n_goodelectrons==1 && n_goodmuons==0 && HT>300 && MHT>30 && n_goodjets>=1 && ",
                   }
        
        cuts_smu = {
                #"usejetht-smu-mht30":                    "HT>30 && MHT>30 && n_goodjets>=1 && leadinglepton_type==13 && ",
                #"useswitchdenom-smu-mht30":              "HT>30 && MHT>30 && n_goodjets>=1 && leadinglepton_type==13 && n_goodelectrons>=1 && n_goodmuons>=1 && ",
                #"useswitchdenom-smu-mht30":              "HT>30 && MHT>30 && n_goodjets>=1 && leadinglepton_type==13 && ",
                #"useswitchdenom-smu-mht30":              "HT>30 && MHT>30 && n_goodjets>=1 && ",
                #"useswitchdenom-smu-mincuts":            "leadinglepton_type==13 && n_goodelectrons>=1 && n_goodmuons>=1 && ",
                "useswitchdenom-smu":                     "HT>30 && MHT>30 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons>=1 && ",
                #"usejetht-smu-mht300":                   "HT>30 && MHT>300 && n_goodjets>=1 && ",
                #"usejethtother-smu-mht300":              "HT>30 && MHT>300 && n_goodjets>=1 && ",
                #"useswitchdenom-smu-mht300":             "HT>30 && MHT>300 && n_goodjets>=1 && ",
                #"usemet-smu-baseline":                   "HT>30 && MHT>30 && n_goodjets>=1 && ",
                #"smu-mht50":                             "HT>30 && MHT>30 && MHT<50 && n_goodjets>=1 && ",
                #"smu-baseline-fullcuts":                 "n_goodmuons==1 && n_goodelectrons==0 && HT>30 && MHT>30 && n_goodjets>=1 && ",
                #"smu-baseline-fullcuts300":              "n_goodmuons==1 && n_goodelectrons==0 && HT>300 && MHT>30 && n_goodjets>=1 && ",
                   }
        

        for label in cuts_sel:
            channel = "SEl"
            for j_variable in binnings.keys():
                cmds.append("./plot-trigger-efficiency-from-skim.py --channel %s --variable %s --outputfolder %s --label %s --cuts '%s' --skim %s " % (channel, j_variable, options.outputfolder, label, cuts_sel[label], options.skim_folder))
        
        for label in cuts_smu:
            channel = "SMu"
            for j_variable in binnings.keys():
                cmds.append("./plot-trigger-efficiency-from-skim.py --channel %s --variable %s --outputfolder %s --label %s --cuts '%s' --skim %s " % (channel, j_variable, options.outputfolder, label, cuts_smu[label], options.skim_folder))

        for label in cuts_mht:
            channel = "MHT"
            for j_variable in binnings.keys():
                cmds.append("./plot-trigger-efficiency-from-skim.py --channel %s --variable %s --outputfolder %s --label %s --cuts '%s' --skim %s " % (channel, j_variable, options.outputfolder, label, cuts_mht[label], options.skim_folder))

        GridEngineTools.runParallel(cmds, options.runmode, ncores_percentage=0.9, condorDir=options.outputfolder + ".condor")

    else:
        os.system("mkdir -p %s" % options.outputfolder)
        combinedplots(options.channel, options.variable, options.outputfolder, options.label, options.cuts, options.skim_folder)

