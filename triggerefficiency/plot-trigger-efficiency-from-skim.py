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
            "n_goodjets":               [ 10, 0, 10, "number of jets"],
            "MHT":                      [ [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 700], 0, 700, "missing H_{T} (GeV)"],
            "leadinglepton_pt":         [ [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 176, 200, 250, 300], 0, 300, "leading p_{T}^{lep} (GeV)"],
            #"leadinglepton_pt:MHT":     [ [0, 50, 100, 150, 200, 300, 700], 0, 700, [0, 30, 60, 90, 200, 300], 0, 300, "missing H_{T} (GeV); leading p_{T}^{lep} (GeV)"],            
            ##"pass_baseline":          [1, 1, 2, "passed baseline cuts"],
            ##"HT":                     [ [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 350, 400, 450, 500, 700], 0, 700, "H_{T} (GeV)"],
            ##"MHT":                    [ [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 350, 400, 450, 500, 700], 0, 700, "missing H_{T} (GeV)"],
            ###"HT":                    [ [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 700], 0, 700, "missing H_{T} (GeV)"],
            ##"leadinglepton_eta:leadinglepton_phi": [ 20, -3.2, 3.2, "phi; eta" ],
           }

def savetoroot(obj, label, outputfolder, folderlabel):
    
    obj.SetName(label)
    fout = TFile(outputfolder + "/" + label + ".root", "recreate")
    fout.mkdir(folderlabel)
    fout.cd(folderlabel)
    obj.Write()
    fout.Write()
    fout.Close()


def stamp_cuts(cuts_channel, channel, variable):
            
    tl2 = TLatex()
    tl2.SetNDC()
    #tl2.SetTextFont(50)
    tl2.SetTextSize(0.027)
    if channel == "MHT":
        tl2.DrawLatex(0.15, 0.27, "#epsilon = #frac{n_{ev}(lepton trigger & MET trigger)}{n_{ev}(lepton trigger)} ")
                                
    elif channel == "Lep":
        tl2.DrawLatex(0.15, 0.27, "#epsilon = #frac{n_{ev}(lepton trigger & MET trigger)}{n_{ev}(MET trigger)} ")
    
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
    tl2.DrawLatex(0.15, 0.35, cuts_channel_minus1)


def combinedplots(channel, variable, outputfolder, folderlabel, cuts_channel):

    #skim_folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_112_triggerstudy_merged/"
    skim_folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_115_triggerstudy_merged/"
    
    #numevents = -1
    numevents = 500000

    if "jetht" in folderlabel:
        usejetht = True
    else:
        usejetht = False

    pdffile = "%s/triggereff_%s_%s.pdf" % (outputfolder, channel, variable.replace(":", "-"))
    
    histos = {}        
    
    for year in [
                2016,
                2017,
                2018,
                ]:

        if channel == "MHT":
            if year == 2018:
                globstring_sel = [
                                  "%s/Run%sA*EGamma*.root" % (skim_folder, year),
                                  "%s/Run%sB*EGamma*.root" % (skim_folder, year),
                                  "%s/Run%sC*EGamma*.root" % (skim_folder, year),
                                  "%s/Run%sD*EGamma*.root" % (skim_folder, year),
                                 ]
                globstring_smu = [
                                  "%s/Run%sA*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sB*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sC*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sD*SingleMuon*.root" % (skim_folder, year),
                                 ]
            else:
                globstring_sel = [
                                  "%s/Run%sA*SingleElectron*.root" % (skim_folder, year),
                                  "%s/Run%sB*SingleElectron*.root" % (skim_folder, year),
                                  "%s/Run%sC*SingleElectron*.root" % (skim_folder, year),
                                  "%s/Run%sD*SingleElectron*.root" % (skim_folder, year),
                                  "%s/Run%sE*SingleElectron*.root" % (skim_folder, year),
                                  "%s/Run%sF*SingleElectron*.root" % (skim_folder, year),
                                  "%s/Run%sG*SingleElectron*.root" % (skim_folder, year),
                                  "%s/Run%sH*SingleElectron*.root" % (skim_folder, year),
                                 ]
                globstring_smu = [
                                  "%s/Run%sA*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sB*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sC*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sD*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sE*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sF*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sG*SingleMuon*.root" % (skim_folder, year),
                                  "%s/Run%sH*SingleMuon*.root" % (skim_folder, year),
                                 ]
            
        elif channel == "Lep":
            globstring_sel = [
                              "%s/Run%sA*MET*.root" % (skim_folder, year),
                              "%s/Run%sB*MET*.root" % (skim_folder, year),
                              "%s/Run%sC*MET*.root" % (skim_folder, year),
                              "%s/Run%sD*MET*.root" % (skim_folder, year),
                              "%s/Run%sE*MET*.root" % (skim_folder, year),
                              "%s/Run%sF*MET*.root" % (skim_folder, year),
                              "%s/Run%sG*MET*.root" % (skim_folder, year),
                              "%s/Run%sH*MET*.root" % (skim_folder, year),
                             ]
            
            if usejetht:
                print "Adding JetHT to MET..."
                globstring_sel.append("%s/Run%sA*JetHT*.root" % (skim_folder, year))
                globstring_sel.append("%s/Run%sB*JetHT*.root" % (skim_folder, year))
                globstring_sel.append("%s/Run%sC*JetHT*.root" % (skim_folder, year))
                globstring_sel.append("%s/Run%sD*JetHT*.root" % (skim_folder, year))
                globstring_sel.append("%s/Run%sE*JetHT*.root" % (skim_folder, year))
                globstring_sel.append("%s/Run%sF*JetHT*.root" % (skim_folder, year))
                globstring_sel.append("%s/Run%sG*JetHT*.root" % (skim_folder, year))
                globstring_sel.append("%s/Run%sH*JetHT*.root" % (skim_folder, year))                 
            
            globstring_smu = list(globstring_sel)


        cuts_singleelectron = "n_goodelectrons>=1 && n_goodmuons==0 && "
        cuts_singlemuon = "n_goodmuons>=1 && n_goodelectrons==0 && "
        
        #cuts_singleelectron = "n_goodelectrons==1 && n_goodmuons==0 && "
        #cuts_singlemuon = "n_goodmuons==1 && n_goodelectrons==0 && "

        #cuts_singleelectron = "n_goodelectrons>=0 && "
        #cuts_singlemuon = "n_goodmuons>=0 && "

        
        if variable == "leadinglepton_eta:leadinglepton_phi":
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
            
        if usejetht:
            #mettriggerstring = "(HT>500 && (triggered_met==1 || triggered_ht==1))"
            mettriggerstring = "(triggered_met==1 || triggered_ht==1)"
        else:
            mettriggerstring = "triggered_met==1"
    
        histos["%s_%s_singleelectron_elmettrigger_%s" % (variable, channel, year)] =   plotting.get_all_histos(globstring_sel, "Events", variable, numevents=numevents, nMinus1=nMinus1, cutstring=cuts_channel + cuts_singleelectron + "triggered_singleelectron==1 && " + mettriggerstring , nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)
        histos["%s_%s_singlemuon_mumettrigger_%s" % (variable, channel, year)] =       plotting.get_all_histos(globstring_smu, "Events", variable, numevents=numevents, nMinus1=nMinus1, cutstring=cuts_channel + cuts_singlemuon + "triggered_singlemuon==1 && " + mettriggerstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)
        if channel == "Lep":
            histos["%s_%s_singleelectron_mettrigger_%s" % (variable, channel, year)] = plotting.get_all_histos(globstring_sel, "Events", variable, numevents=numevents, nMinus1=nMinus1, cutstring=cuts_channel + cuts_singleelectron + mettriggerstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)
            histos["%s_%s_singlemuon_mettrigger_%s" % (variable, channel, year)] =     plotting.get_all_histos(globstring_smu, "Events", variable, numevents=numevents, nMinus1=nMinus1, cutstring=cuts_channel + cuts_singlemuon + mettriggerstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)
        else:
            histos["%s_%s_singleelectron_eltrigger_%s" % (variable, channel, year)] =  plotting.get_all_histos(globstring_sel, "Events", variable, numevents=numevents, nMinus1=nMinus1, cutstring=cuts_channel + cuts_singleelectron + "triggered_singleelectron==1", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)
            histos["%s_%s_singlemuon_mutrigger_%s" % (variable, channel, year)] =      plotting.get_all_histos(globstring_smu, "Events", variable, numevents=numevents, nMinus1=nMinus1, cutstring=cuts_channel + cuts_singlemuon + "triggered_singlemuon==1", nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)
                
        for label in histos:
            histos[label].SetDirectory(0)
                  
    c1 = shared_utils.mkcanvas("c1")
    
    legend = TLegend(0.5, 0.2, 0.88, 0.4)
    legend.SetTextSize(0.035)
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
    
    if ":" not in variable:
        histo.Draw("hist")
        histo.GetYaxis().SetRangeUser(0,1.1)
        c1.SetLogy(False)
        c1.SetLogz(False)
    else:
        histo.Draw("colz")
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
        if channel == "MHT":
            num = histos["%s_%s_singlemuon_mumettrigger_%s" % (variable, channel, year)].Clone()
            denom = histos["%s_%s_singlemuon_mutrigger_%s" % (variable, channel, year)].Clone()
        elif channel == "Lep":
            num = histos["%s_%s_singlemuon_mumettrigger_%s" % (variable, channel, year)].Clone()
            denom = histos["%s_%s_singlemuon_mettrigger_%s" % (variable, channel, year)].Clone()
            
        h_effs["mu_%s" % year] = TEfficiency(num.Clone(), denom.Clone())
        
        if channel == "MHT":
            num = histos["%s_%s_singleelectron_elmettrigger_%s" % (variable, channel, year)].Clone()
            denom = histos["%s_%s_singleelectron_eltrigger_%s" % (variable, channel, year)].Clone()
            #savetoroot(histos["%s_%s_singleelectron_eltrigger_%s" % (variable, channel, year)], "h_%s_%s_singleelectron_eltrigger_%s" % (variable, channel, year), outputfolder, folderlabel)
        elif channel == "Lep":
            num = histos["%s_%s_singleelectron_elmettrigger_%s" % (variable, channel, year)].Clone()
            denom = histos["%s_%s_singleelectron_mettrigger_%s" % (variable, channel, year)].Clone()
            
        h_effs["el_%s" % year] = TEfficiency(num.Clone(), denom.Clone())
                      
        if ":" not in variable:
            h_effs["el_%s" % year].Draw("same")
            h_effs["el_%s" % year].SetLineWidth(2)
                            
            h_effs["mu_%s" % year].Draw("same")
            h_effs["mu_%s" % year].SetLineWidth(2)
        else:
            h_effs["el_%s" % year].Draw("colz same")
            stamp_cuts(cuts_channel, channel, variable)
            shared_utils.stamp()
            c1.SaveAs("%s/triggereff_%s_%s_eltrigger_%s.pdf" % (outputfolder, channel, variable.replace(":", "-"), year))
            savetoroot(h_effs["el_%s" % year], "h_triggereff_%s_%s_eltrigger_%s" % (channel, variable.replace(":", "-"), year), outputfolder, folderlabel)
            savetoroot(c1, "c_triggereff_%s_%s_eltrigger_%s" % (channel, variable.replace(":", "-"), year), outputfolder, folderlabel)
            h_effs["mu_%s" % year].Draw("colz same")
            stamp_cuts(cuts_channel, channel, variable)
            shared_utils.stamp()
            c1.SaveAs("%s/triggereff_%s_%s_mutrigger_%s.pdf" % (outputfolder, channel, variable.replace(":", "-"), year))
            savetoroot(h_effs["mu_%s" % year], "h_triggereff_%s_%s_mutrigger_%s" % (channel, variable.replace(":", "-"), year), outputfolder, folderlabel)
            savetoroot(c1, "c_triggereff_%s_%s_mutrigger_%s" % (channel, variable.replace(":", "-"), year), outputfolder, folderlabel)
           
    if ":" in variable:
        return
    
    h_effs["el_2016"].SetLineColor(kBlue)    
    legend.AddEntry(h_effs["el_2016"], "2016, lepton trigger: e")
    h_effs["el_2017"].SetLineColor(kRed)    
    legend.AddEntry(h_effs["el_2017"], "2017, lepton trigger: e")
    h_effs["el_2018"].SetLineColor(kGreen+2)    
    legend.AddEntry(h_effs["el_2018"], "2018, lepton trigger: e")

    h_effs["mu_2016"].SetLineColor(kAzure+1)    
    legend.AddEntry(h_effs["mu_2016"], "2016, lepton trigger: #mu")
    h_effs["mu_2017"].SetLineColor(kRed-9)    
    legend.AddEntry(h_effs["mu_2017"], "2017, lepton trigger: #mu")
    h_effs["mu_2018"].SetLineColor(kGreen-8)    
    legend.AddEntry(h_effs["mu_2018"], "2018, lepton trigger: #mu")
    
    stamp_cuts(cuts_channel, channel, variable)
    shared_utils.stamp()
  
    legend.Draw()
    
    c1.SetGrid(True)
    
    c1.SaveAs(pdffile)
    savetoroot(h_effs["el_2016"], "h_triggereff_%s_%s_el_2016" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)
    savetoroot(h_effs["el_2017"], "h_triggereff_%s_%s_el_2017" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)
    savetoroot(h_effs["el_2018"], "h_triggereff_%s_%s_el_2018" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)
    savetoroot(h_effs["mu_2016"], "h_triggereff_%s_%s_mu_2016" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)
    savetoroot(h_effs["mu_2017"], "h_triggereff_%s_%s_mu_2017" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)
    savetoroot(h_effs["mu_2018"], "h_triggereff_%s_%s_mu_2018" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)
    savetoroot(c1, "c_triggereff_%s_%s" % (channel, variable.replace(":", "-")), outputfolder, folderlabel)


if __name__ == "__main__":
       
    parser = OptionParser()
    parser.add_option("--channel", dest = "channel", default = False)
    parser.add_option("--variable", dest = "variable", default = False)
    parser.add_option("--outputfolder", dest = "outputfolder", default = "trigger")
    parser.add_option("--label", dest = "label", default = "trigger")
    parser.add_option("--cuts", dest = "cuts", default = "0")
    parser.add_option("--runmode", dest = "runmode", default = "grid")
    (options, args) = parser.parse_args()
    
    if not options.channel:

        cmds = []
  
        cuts_mht = {
                #"mht-nocuts":        "HT>0 && ",
                #"mht-baseline":       "HT>150 && MHT>150 && n_goodjets>=1 && ",
                #"mht-1jet":           "HT>150 && MHT>150 && n_goodjets==1 && ",
                #"mht-highjets":       "HT>150 && MHT>150 && n_goodjets>=2 && ",
                #"mht-only1jet":       "n_goodjets==1 && ",
                #"mht-2jet":          "HT>150 && MHT>150 && n_goodjets==2 && ",
                #"mht-lowjets":       "HT>150 && MHT>150 && n_goodjets>=1 && n_goodjets<3 && ",
                #"mht-highjets":      "HT>150 && MHT>150 && n_goodjets>=3 && ",
                #"sr_1_4":            "MHT>=150 && MHT<300 && n_btags==0 && n_goodjets>=1 && n_goodjets<3 && ",
                #"sr_5_8":            "MHT>=150 && MHT<300 && n_btags==0 && n_goodjets>=3 && ",
                #"sr_9_12":           "MHT>=150 && MHT<300 && n_btags>=1 && n_goodjets>=1 && n_goodjets<3 && ",
                #"sr_13_16":          "MHT>=150 && MHT<300 && n_btags>=1 && n_goodjets>=3 && ",
                #"sr_17_20":          "MHT>=300 && n_goodjets>=1 && n_goodjets<3 && ",
                #"sr_21_24":          "MHT>=300 && n_goodjets>=3 && ",
                   }

        cuts_lep = {
                #"lep-nocuts":        "HT>0 && ",
                #"lep-baseline":      "HT>30 && MHT>30 && n_goodjets>=1 && ",
                "lep-baseline-metjetht":      "HT>30 && MHT>30 && n_goodjets>=1 && ",
                #"lep-1jet":          "HT>30 && MHT>30 && n_goodjets==1 && ",
                #"lep-highjets":      "HT>30 && MHT>30 && n_goodjets>1 && ",
                #"sr_25_28":         "n_goodmuons==1 && n_goodelectrons==0 && MHT>=30 && MHT<150 && n_btags==0 && n_goodjets>=1 && ",
                #"sr_29_32":         "n_goodmuons==1 && n_goodelectrons==0 && MHT>=30 && MHT<150 && n_btags>=1 && n_goodjets>=1 && ",
                #"sr_33_36":         "n_goodmuons==1 && n_goodelectrons==0 && MHT>=150 && n_goodjets>=1 && ",
                #"sr_37_40":         "n_goodmuons==1 && n_goodelectrons==0 && MHT>=30 && MHT<150 && n_btags==0 && n_goodjets>=1 && ",
                #"sr_41_44":         "n_goodelectrons==1 && MHT>=30 && MHT<150 && n_btags>=1 && n_goodjets>=1 && ",
                #"sr_45_48":         "n_goodelectrons==1 && MHT>=150 && n_goodjets>=1 && ",
                   }

        for label in cuts_lep:
            channel = "Lep"
            for j_variable in binnings.keys():
                cmds.append("./plot-trigger-efficiency-from-skim.py --channel %s --variable %s --outputfolder %s-%s --label %s --cuts '%s' " % (channel, j_variable, options.outputfolder, label, label, cuts_lep[label]))

        for label in cuts_mht:
            channel = "MHT"
            for j_variable in binnings.keys():
                cmds.append("./plot-trigger-efficiency-from-skim.py --channel %s --variable %s --outputfolder %s-%s --label %s --cuts '%s' " % (channel, j_variable, options.outputfolder, label, label, cuts_mht[label]))

        GridEngineTools.runParallel(cmds, options.runmode)

    else:
        os.system("mkdir -p %s" % options.outputfolder)
        combinedplots(options.channel, options.variable, options.outputfolder, options.label, options.cuts)
    
