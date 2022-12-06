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
            #"MHT":                                   [ [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 700], 0, 700, "missing H_{T} (GeV)"],
            #"MHT":                                    [ [1, 150, 250, 500], 1, 500, "missing H_{T} (GeV)"],
            #"MHT":                                    [ [150, 500], 150, 500, "missing H_{T} (GeV)"],
            #"MHT":                                    [ [100, 200, 250], 100, 250, "missing H_{T} (GeV)"],
            ##"HT":                                   [ [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 700], 0, 700, "H_{T} (GeV)"],
            ##"leadinglepton_pt":                     [ [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 176, 200, 250, 500], 0, 500, "leading p_{T}^{lep} (GeV)"],
            #"leadingelectron_pt":                    [ [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 176, 200, 250, 500], 0, 500, "p_{T}^{el} (GeV)"],
            #"leadingmuon_pt":                        [ [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 176, 200, 250, 500], 0, 500, "p_{T}^{#mu} (GeV)"],
            ##"leadinglepton_pt:MHT":                 [ [0, 50, 100, 150, 200, 300, 700], 0, 700, [0, 30, 60, 90, 200, 500], 0, 500, "missing H_{T} (GeV); p_{T}^{lep} (GeV)"],  
            "leadingelectron_pt:MHT":                [ [30, 65, 100, 150, 200, 500], 30, 500, [40, 70, 100, 150, 200, 500], 40, 500, "missing H_{T} (GeV); p_{T}^{e} (GeV)"],  
            "leadingmuon_pt:MHT":                    [ [30, 65, 100, 150, 200, 500], 30, 500, [40, 70, 100, 150, 200, 500], 40, 500, "missing H_{T} (GeV); p_{T}^{#mu} (GeV)"],  
            ##"leadinglepton_eta:leadinglepton_phi":  [ 20, -3.2, 3.2, "phi; eta" ],
           }

def savetoroot(obj, label, outputfolder, folderlabel):
    
    obj.SetName(label)
    if "h_" in label:
        obj.SetDirectory(0)
    fout = TFile(outputfolder + "/" + label + "_" + folderlabel + ".root", "recreate")
    fout.mkdir(folderlabel)
    fout.cd(folderlabel)
    obj.Write()
    fout.Write()
    fout.Close()


def stamp_cuts(cuts_channel, channel, variable, use_or_trigger, denom_label, extra_label, replace_cut_label = False):
    
    cuts_channel = cuts_channel.replace("n_goodelectrons", "n_{el}")
    cuts_channel = cuts_channel.replace("n_goodmuons", "n_{#mu}")
    
    if ":" in variable:
        yoffset = 0.22
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
        
    cuts_channel_minus1 = cuts_channel_minus1.replace("((leadingDT_pixeltrack==1 && leadingDT_Edep<20) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.20))", "EDep(DT)<20 GeV / EDep/p(DT)<0.20 ")
    cuts_channel_minus1 = cuts_channel_minus1.replace("((leadingDT_pixeltrack==1 && leadingDT_Edep<15) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.15))", "EDep(DT)<15 GeV / EDep/p(DT)<0.15 ")
    cuts_channel_minus1 = cuts_channel_minus1.replace("((leadingDT_pixeltrack==1 && leadingDT_Edep<30) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.30))", "EDep(DT)<30 GeV / EDep/p(DT)<0.30 ")
    cuts_channel_minus1 = cuts_channel_minus1.replace("((leadingDT_pixeltrack==1 && leadingDT_Edep<50) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.50))", "EDep(DT)<50 GeV / EDep/p(DT)<0.50 ")
    cuts_channel_minus1 = cuts_channel_minus1.replace(" && ", ", ")
    cuts_channel_minus1 = cuts_channel_minus1.replace(" &&", "")
    cuts_channel_minus1 = cuts_channel_minus1.replace(" || ", " or ")
    cuts_channel_minus1 = cuts_channel_minus1.replace(" ||", "")
    cuts_channel_minus1 = cuts_channel_minus1.replace("n_goodjets", "nJet")
    cuts_channel_minus1 = cuts_channel_minus1.replace("(n_DTShort+n_DTLong)", "nDT")
    cuts_channel_minus1 = cuts_channel_minus1.replace("(n_DTEDepSideBandShort+n_DTEDepSideBandLong)", "nDT_{SB}")
    cuts_channel_minus1 = cuts_channel_minus1.replace("(n_DTShort2+n_DTLong2)", "nDT")
    cuts_channel_minus1 = cuts_channel_minus1.replace("(n_DTEDepSideBandShort2+n_DTEDepSideBandLong2)", "nDT_{SB}")
    cuts_channel_minus1 = cuts_channel_minus1.replace("(n_DTShort3+n_DTLong3)", "nDT")
    cuts_channel_minus1 = cuts_channel_minus1.replace("(n_DTEDepSideBandShort3+n_DTEDepSideBandLong3)", "nDT_{SB}")
    cuts_channel_minus1 = cuts_channel_minus1.replace(">=", "#geq")
    cuts_channel_minus1 = cuts_channel_minus1.replace("<=", "#leq")
    cuts_channel_minus1 = cuts_channel_minus1.replace("==", "=")
    
    if cuts_channel_minus1[-1] == ",":
        cuts_channel_minus1 = cuts_channel_minus1[:-1]
    elif cuts_channel_minus1[-2] == ",":
        cuts_channel_minus1 = cuts_channel_minus1[:-2]
        
    tl2.DrawLatex(0.15, 0.40 + yoffset, extra_label)
    
    if not replace_cut_label:
        tl2.DrawLatex(0.15, 0.35 + yoffset, cuts_channel_minus1)
    else:
        tl2.DrawLatex(0.15, 0.35 + yoffset, replace_cut_label)
        

def combinedplots(channel, variable, outputfolder, folderlabel, cuts_channel, skim_folder, use_or_trigger = True):
      
    if channel == "SEl" and "leadingmuon" in variable:
        return
    if channel == "SMu" and "leadingelectron" in variable:
        return
    if channel == "MHT" and "leading" in variable:
        return
            
    numevents = -1
    
    pdffile = "%s/triggereff_%s_%s.pdf" % (outputfolder, folderlabel, variable.replace(":", "_"))
    
    histos = {}      
      
    # select/unselect specific run period:
    period = ""

    for year in [
                2016,
                2017,
                2018,
                ]:

        # switches
        if "switchdenom" in folderlabel:
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

        elif "JetHTother" in folderlabel:
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

        elif "JetHT" in folderlabel:
            glob_sel_num =   "Run%s%s*JetHT*.root" % (year, period)
            glob_sel_denom = "Run%s%s*JetHT*.root" % (year, period)
            glob_smu_num =   "Run%s%s*JetHT*.root" % (year, period)
            glob_smu_denom = "Run%s%s*JetHT*.root" % (year, period)
            denom = "triggered_ht==1"
            denom_label = "HT trigger"
            extra_label = "JetHT dataset"
            
        elif "mht_SingleMu" in folderlabel:
            glob_mht_num =   "Run%s%s*SingleMuon*.root" % (year, period)
            glob_mht_denom = "Run%s%s*SingleMuon*.root" % (year, period)
            denom = "triggered_singlemuon==1"
            denom_label = "muon trigger"
            extra_label = "SingleMuon dataset"   

        elif "mht_SingleEl" in folderlabel:
            glob_mht_num =   "Run%s%s*SingleElectron*.root" % (year, period)
            glob_mht_denom = "Run%s%s*SingleElectron*.root" % (year, period)
            denom = "triggered_singleelectron==1"
            denom_label = "el. trigger"
            extra_label = "SingleElectron dataset"   
            
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
            #extra_label += ", trigger efficiency"
        else:
            if variable == "MHT" and "DtTurnon" in folderlabel:
                print "don't peek into SR"
                nMinus1 = False
            else:
                nMinus1 = True
    
        if "DtTurn" in folderlabel or "DtSide" in folderlabel:
            print "setting nMinus1 = False"
            nMinus1 = False
    
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
                extra_label = "Egamma dataset"
                if ":" in variable:
                    #extra_label = "Egamma dataset, trigger efficiency"
                    extra_label = "Egamma dataset"

            if "combine" in folderlabel and "2016" in globstring:
                histo = plotting.get_all_histos([skim_folder + "/Run201*SingleElectron*", skim_folder + "/Run201*EGamma*"], "Events", variable, numevents=numevents, nMinus1=nMinus1, cutstring=cuts_channel + cutA + cutB , nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)        
            else:
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
        htitle = ";%s; trigger efficiency #epsilon" % binnings[variable][3]
    else:

        if channel == "SEl":
            htitle = ";%s; single-e trigger efficiency #epsilon" % binnings[variable][6]        
            htitle = htitle.replace("{lep}", "{e}")
        elif channel == "SMu":
            htitle = ";%s; single-#mu trigger efficiency #epsilon" % binnings[variable][6]        
            htitle = htitle.replace("{lep}", "{#mu}")
        else:
            htitle = ";%s; trigger efficiency #epsilon" % binnings[variable][6]
    histo.SetTitle(htitle)
    
    shared_utils.histoStyler(histo)
    
    #FIXME
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
        
        print "@@", num.GetEntries()
        print "@@", denom.GetEntries()
            
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
            h_effs["eff_%s_TEff" % year] = TEfficiency(num.Clone(), denom.Clone())

            # convert TEff to normal hist:
            h2dPass = h_effs["eff_%s_TEff" % year].GetPassedHistogram()
            h2dTotal = h_effs["eff_%s_TEff" % year].GetTotalHistogram()
            h_effs["eff_%s" % year] = h2dPass.Clone()
            h_effs["eff_%s" % year].Divide(h2dTotal)
            h_effs["eff_%s" % year].SetDirectory(0)
            shared_utils.histoStyler(h_effs["eff_%s" % year])
            h_effs["eff_%s" % year].SetTitle(htitle)

        if ":" not in variable:
            # 1D histograms:
            h_effs["eff_%s" % year].Draw("same")
            h_effs["eff_%s" % year].SetLineWidth(2)

            if False and year == 2016:
                print "extra"
                numNorm = num.Clone()
                denomNorm = denom.Clone()
                if num.Integral()>0:
                    numNorm.Scale(1.0/denom.Integral())
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
            savetoroot(h_effs["eff_%s" % year], "h_triggereff_%s_%s_%s" % (channel, variable.replace(":", "_"), year), outputfolder, folderlabel)

            #if "eff_%s_TEff" % year in h_effs:
            #    savetoroot(h_effs["eff_%s_TEff" % year], "teff_triggereff_%s_%s_%s" % (channel, variable.replace(":", "_"), year), outputfolder, folderlabel)

            stamp_cuts(cuts_channel, channel, variable, use_or_trigger, denom_label, extra_label)
            shared_utils.stamp()
            c1.SaveAs(pdffile.replace(".pdf", "_%s.pdf" % year))
            savetoroot(c1, "c_triggereff_%s_%s_%s" % (channel, variable.replace(":", "_"), year), outputfolder, folderlabel)
                       
            continue

    if ":" in variable:
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
    
    if folderlabel == "mht_SingleEl_DtTurnon20mva0" or folderlabel == "mht_SingleEl_DtTurnon":
        stamp_cuts(cuts_channel, channel, variable, use_or_trigger, denom_label, extra_label, replace_cut_label = "nJets #geq 1, nDT(E_{dep} SR) #geq 1")        
    elif folderlabel == "mht_SingleEl_DtSideband20mva0" or folderlabel == "mht_SingleEl_DtSideband":
        stamp_cuts(cuts_channel, channel, variable, use_or_trigger, denom_label, extra_label, replace_cut_label = "nJets #geq 1, nDT(E_{dep} sideband) #geq 1")        
    else:
        stamp_cuts(cuts_channel, channel, variable, use_or_trigger, denom_label, extra_label)
    shared_utils.stamp()
  
    legend.Draw()
    
    c1.SetGrid(True)
    
    c1.SaveAs(pdffile)
    savetoroot(h_effs["eff_2016"], "h_triggereff_%s_%s_2016" % (channel, variable.replace(":", "_")), outputfolder, folderlabel)
    savetoroot(h_effs["eff_2017"], "h_triggereff_%s_%s_2017" % (channel, variable.replace(":", "_")), outputfolder, folderlabel)
    savetoroot(h_effs["eff_2018"], "h_triggereff_%s_%s_2018" % (channel, variable.replace(":", "_")), outputfolder, folderlabel)
    
    #if "eff_2016_TEff" in h_effs:
    #    print "@@@@@"
    #    savetoroot(h_effs["eff_2016_TEff"], "teff_triggereff_%s_%s_2016" % (channel, variable.replace(":", "_")), outputfolder, folderlabel)
    #    savetoroot(h_effs["eff_2017_TEff"], "teff_triggereff_%s_%s_2017" % (channel, variable.replace(":", "_")), outputfolder, folderlabel)
    #    savetoroot(h_effs["eff_2018_TEff"], "teff_triggereff_%s_%s_2018" % (channel, variable.replace(":", "_")), outputfolder, folderlabel)
    
    savetoroot(c1, "c_triggereff_%s_%s" % (folderlabel, variable.replace(":", "_")), outputfolder, folderlabel)


if __name__ == "__main__":
       
    parser = OptionParser()
    parser.add_option("--channel", dest = "channel", default = False)
    parser.add_option("--variable", dest = "variable", default = False)
    parser.add_option("--outputfolder", dest = "outputfolder", default = "plots")
    parser.add_option("--label", dest = "label", default = "trigger")
    parser.add_option("--cuts", dest = "cuts", default = "0")
    parser.add_option("--runmode", dest = "runmode", default = "multi")
    parser.add_option("--skim", dest = "skim_folder", default = "../ntupleanalyzer/skim_203_trigger_tightMuonJetDRp4_merged/")
    (options, args) = parser.parse_args()

    if not options.channel:

        cmds = []
                    
        cuts_mht = {
                #"mht_SingleEl_highmet":          "HT>300 && MHT>300 && n_goodjets>=1 && ",
                #"mht_SingleMu_highmet":          "HT>300 && MHT>300 && n_goodjets>=1 && ",
                #"mht_SingleEl":                  "HT>150 && MHT>150 && n_goodjets>=1 && ",
                #"mht_SingleEl_lowjets":          "HT>150 && MHT>150 && n_goodjets>=1 && n_goodjets<=2 && ",
                #"mht_SingleEl_highjets":         "HT>150 && MHT>150 && n_goodjets>=3 && ",
                #"mht_SingleMu":                  "HT>150 && MHT>150 && n_goodjets>=1 && ",
                #"mht_SingleMu_lowjets":          "HT>150 && MHT>150 && n_goodjets>=1 && n_goodjets<=2 && ",
                #"mht_SingleMu_highjets":         "HT>150 && MHT>150 && n_goodjets>=3 && ",
                #"mht_SingleEl_DtTurnon":          "HT>150 && MHT<250 && n_goodjets>=1 && (n_DTShort+n_DTLong)>=1 && ",
                #"mht_SingleEl_DtSideband":        "HT>150 && MHT>300 && n_goodjets>=1 && (n_DTEDepSideBandShort+n_DTEDepSideBandLong)>=1 && ",
                #"mht_SingleEl_DtTurnon":          "n_goodjets>=1 && (n_DTShort+n_DTLong)>=1 && ",
                #"mht_SingleEl_DtSideband":        "n_goodjets>=1 && (n_DTEDepSideBandShort+n_DTEDepSideBandLong)>=1 && ",
                #"mht_SingleEl_DtTurnon20mva0":    "n_goodjets>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep<20) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.20)) && ",
                #"mht_SingleEl_DtSideband20mva0":  "n_goodjets>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep>30 && leadingDT_Edep<300) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP>0.30 && leadingDT_EdepByP<3.00)) &&",
                #"mht_SingleEl_DtTurnon20mva0":    "n_goodjets>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep<20) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.20)) && ",
                #"mht_SingleEl_DtSideband20mva0":  "n_goodjets>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep>25 && leadingDT_Edep<300) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP>0.25 && leadingDT_EdepByP<3.00)) &&",
                #"mht_SingleEl_DtTurnon20mva0":    "n_goodjets>=1 && ((leadingDT_pixeltrack==1 && leadingDT_Edep<20) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.20)) && ",
                #"mht_SingleEl_DtSideband20mva0":  "n_goodjets>=1 && ((leadingDT_pixeltrack==1 && leadingDT_Edep>25 && leadingDT_Edep<300) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP>0.25 && leadingDT_EdepByP<3.00)) &&",
                #"mht_SingleEl_DtTurnon20alljets_combine":    "((leadingDT_pixeltrack==1 && leadingDT_Edep<20) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.20)) && ",
                #"mht_SingleEl_DtSideband20alljets_combine":  "((leadingDT_pixeltrack==1 && leadingDT_Edep>25 && leadingDT_Edep<300) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP>0.25 && leadingDT_EdepByP<3.00)) &&",
                #"mht_SingleEl_DtTurnon20mva0_short":    "n_goodjets>=1 && leadingDT_mva>=0 && ((leadingDT_pixeltrack==1 && leadingDT_Edep<20)) && ",
                #"mht_SingleEl_DtSideband20mva0_short":  "n_goodjets>=1 && leadingDT_mva>=0 && ((leadingDT_pixeltrack==1 && leadingDT_Edep>30 && leadingDT_Edep<100)) &&",
                #"mht_SingleEl_DtTurnon20mva01":   "HT>150 && MHT<250 && n_goodjets>=1 && leadingDT_mva>=-0.1 && ((leadingDT_pixeltrack==1 && leadingDT_Edep<20) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.20)) && ",
                #"mht_SingleEl_DtSideband20mva01": "HT>150 && MHT>300 && n_goodjets>=1 && leadingDT_mva>=-0.1 && ((leadingDT_pixeltrack==1 && leadingDT_Edep>30 && leadingDT_Edep<300) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP>0.30 && leadingDT_EdepByP<1.20)) &&",
                #"mht_SingleEl_DtTurnon20mva02":   "n_goodjets>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep<20) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.20)) && ",
                #"mht_SingleEl_DtSideband20mva02": "n_goodjets>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep>30 && leadingDT_Edep<300) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP>0.30 && leadingDT_EdepByP<1.20)) &&",
                #"mht-baseline":                  "HT>0 && ",
                #"mht-DtTurnon":                  "MHT<250 && (n_DTShort + n_DTLong)>=1 && ",
                #"mht-DtSideband":                "HT>250 && (n_DTEDepSideBandShort + n_DTEDepSideBandLong)>=1 && ",
                #"mht-baseline-fullcuts":         "n_goodelectrons==0 && n_goodmuons==0 && HT>150 && MHT>150 && n_goodjets>=1 && ",
                #"mht-baseline-fullcuts300":      "n_goodelectrons==0 && n_goodmuons==0 && HT>300 && MHT>150 && n_goodjets>=1 && ",
                   }

        cuts_sel = {
                #"sel_switchdenom":                     "HT>30 && MHT>30 && n_goodjets>=1 && n_goodelectrons>=1 && ",
                #"sel_JetHT":                           "HT>30 && MHT>30 && n_goodjets>=1 && n_goodelectrons>=1 && ",
                #"sel_switchdenom_DtTurnon20mva02":     "n_goodjets>=1 && n_goodelectrons>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep<20) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.20)) && ",
                #"sel_switchdenom_DtSideband20mva02":   "n_goodjets>=1 && n_goodelectrons>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep>30 && leadingDT_Edep<300) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP>0.30 && leadingDT_EdepByP<1.20)) &&",
                   }
                           
        cuts_smu = {
                "smu_switchdenom":                     "HT>30 && MHT>30 && n_goodjets>=1 && n_goodmuons>=1 && ",
                #"smu_JetHT":                           "HT>30 && MHT>30 && n_goodjets>=1 && n_goodmuons>=1 && ",
                #"smu_switchdenom_DtTurnon20mva02":     "n_goodjets>=1 && n_goodmuons>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep<20) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP<0.20)) && ",
                #"smu_switchdenom_DtSideband20mva02":   "n_goodjets>=1 && n_goodmuons>=1 && leadingDT_mva>=-0.2 && ((leadingDT_pixeltrack==1 && leadingDT_Edep>30 && leadingDT_Edep<300) || (leadingDT_pixeltrack==0 && leadingDT_EdepByP>0.30 && leadingDT_EdepByP<1.20)) &&",
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

