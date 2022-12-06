#!/bin/env python
from __future__ import division
import __main__ as main
from ROOT import *
import collections
import os
import shared_utils
from optparse import OptionParser
import glob

color_fakebg = kSpring - 1
color_promptbg = kAzure + 1
plot_data = True

def get_histo(root_file, label, lumi = False, title = False, color = False):

    if "Run2MET" in label or "Run2Single" in label or "Run2JetHT" in label:
        h_2016 = get_histo(root_file, label.replace("Run2MET", "Run2016MET").replace("Run2Single", "Run2016Single").replace("Run2JetHT", "Run2016JetHT"), lumi = 36170, title = title, color = color)
        h_2017 = get_histo(root_file, label.replace("Run2MET", "Run2017MET").replace("Run2Single", "Run2017Single").replace("Run2JetHT", "Run2017JetHT"), lumi = 41400, title = title, color = color)
        h_2018 = get_histo(root_file, label.replace("Run2MET", "Run2018MET").replace("Run2Single", "Run2018Single").replace("Run2JetHT", "Run2018JetHT"), lumi = 58400, title = title, color = color)
        h_2016.Add(h_2017)
        h_2016.Add(h_2018)
        return h_2016

    if "_combined" in label:
        h_combined = get_histo(root_file, label.replace("_combined", "_short"), lumi = lumi, title = title, color = color)
        h_long = get_histo(root_file, label.replace("_combined", "_long"), lumi = lumi, title = title, color = color)
        h_combined.Add(h_long)
        return h_combined
        
    fin = TFile(root_file, "read")
    histo = fin.Get(label)
    histo.SetDirectory(0)
    fin.Close()
    histo.SetLineWidth(2)
    shared_utils.histoStyler(histo)
    if not "Run201" in label and lumi:
        # this is MC, scale with lumi:
        histo.Scale(lumi)
        print "SCALING"
    #else:
    #    # this is data, scale up to Run-2 lumi....:
    #    histo.Scale(3.8)
    #    histo.SetTitle("Data (2016)")
    #    histo.SetTitle("Data")

    if title:
        histo.SetTitle(title)
    if color:
        histo.SetLineColor(color)
        histo.SetFillColor(color)

    return histo


def plot_prediction(variable, root_file, datalabel, category, lumi, region, pdffile, outputfolder):

    os.system("mkdir -p " + outputfolder)
    dataid = datalabel + "_" + variable + "_" + region
    
    histos = collections.OrderedDict()
   
    h_fakeprediction = 0
    h_promptprediction = 0
    
    ###############################
    # get predictions and geninfo #
    ###############################
    
    histos["fakeprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakeprediction_tracks_eta_" + category, lumi, "Fake prediction", color_fakebg)
    histos["promptprediction"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptprediction_tracks_pt_" + category, lumi, "Prompt prediction", color_promptbg)

    if variable == "region" and region == "HadBaseline":
        xroot_file = root_file.replace("MET", "SingleElectron")
        xdatalabel = datalabel.replace("MET", "SingleElectron")
        xregion = region.replace("HadBaseline", "SElBaseline")
        histos["fakeprediction"].Add( get_histo(xroot_file, xdatalabel + "_" + variable + "_" + xregion + "_fakeprediction_tracks_eta_" + category, lumi, "Fake prediction", color_fakebg) )
        histos["promptprediction"].Add( get_histo(xroot_file, xdatalabel + "_" + variable + "_" + xregion + "_promptprediction_tracks_pt_" + category, lumi, "Prompt prediction", color_promptbg) )

        xroot_file = root_file.replace("MET", "SingleMuon")
        xdatalabel = datalabel.replace("MET", "SingleMuon")
        xregion = region.replace("HadBaseline", "SMuBaseline")
        histos["fakeprediction"].Add( get_histo(xroot_file, xdatalabel + "_" + variable + "_" + xregion + "_fakeprediction_tracks_eta_" + category, lumi, "Fake prediction", color_fakebg) )
        histos["promptprediction"].Add( get_histo(xroot_file, xdatalabel + "_" + variable + "_" + xregion + "_promptprediction_tracks_pt_" + category, lumi, "Prompt prediction", color_promptbg) )


    
    if "Run2" not in datalabel:
        histos["srgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_genfake_" + category, lumi, "non-prompt MC Truth", color_fakebg)
        histos["srgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_genprompt_" + category, lumi, "prompt MC Truth", color_promptbg)
        histos["fakecrgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakecr_genfake_" + category, lumi, "non-prompt MC Truth", color_fakebg)
        histos["fakecrgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_fakecr_genprompt_" + category, lumi, "prompt MC Truth", color_promptbg)
        histos["promptcrgenfake"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloSideband_genfake_" + category, lumi, "non-prompt MC Truth", color_fakebg)
        histos["promptcrgenprompt"] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_promptECaloSideband_genprompt_" + category, lumi, "prompt MC Truth", color_promptbg)    
        
    def makeplot(stacked_histograms, datahist, plotlabel, ratiovalues = False, ratiolabel = False, ratio_limits = False, header = False):
       
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.4, x2 = 0.9, y2 = 0.8)
        
        if header:
            legend.SetHeader(header)
        else:
            legend.SetHeader("%s, %s tracks" % (region, category))
    
        ymin = 1e0; ymax = 1e2
        datahist.GetYaxis().SetRangeUser(ymin, ymax)
        for stacked_histogram in stacked_histograms:
            stacked_histogram.GetYaxis().SetRangeUser(ymin, ymax)
            stacked_histogram.GetYaxis().SetLimits(ymin, ymax)
    
        hratio, pads = shared_utils.FabDraw(canvas, legend, datahist, stacked_histograms, datamc = 'Data', lumi = lumi/1e3)
        stacked_histograms[-1].SetTitle("")
        
        if ratio_limits:
            hratio.GetYaxis().SetRangeUser(ratio_limits[0], ratio_limits[1])
        else:
            hratio.GetYaxis().SetRangeUser(-0.1,2.6)
        
        if "Run2" in dataid:
            hratio.GetYaxis().SetTitle('Data/prediction')
        else:
            hratio.GetYaxis().SetTitle('Fake pred./truth')
            
        if ratiolabel:
            hratio.GetYaxis().SetTitle(ratiolabel)
        
        xlabel = variable
        xlabel = xlabel.replace("leptons_mt", "m_{T}^{lepton} (GeV)")
        xlabel = xlabel.replace("leadinglepton_mt", "m_{T}^{lepton} (GeV)")
        hratio.GetXaxis().SetTitle(xlabel)
    
        for ibin in range(1,hratio.GetXaxis().GetNbins()+1):
            if ratiovalues:
                hratio.SetBinContent(ibin, ratiovalues.GetBinContent(ibin))
            else:
                if hratio.GetBinContent(ibin)==0:
                    hratio.SetBinContent(ibin,-999)
        hratio.SetMarkerColor(kBlack)
        
        os.system("mkdir -p " + foldername)
        canvas.SaveAs(foldername + "/" + pdffile + plotlabel + ".pdf")
        print "saving", foldername + "/" + pdffile + plotlabel + ".pdf"
                
    # predictions vs. data:
    
    if histos["promptprediction"].Integral() > histos["fakeprediction"].Integral():
        stacked_histograms = [
                           histos["fakeprediction"].Clone(),
                           histos["promptprediction"].Clone(),
                             ]
    else:
        stacked_histograms = [
                           histos["promptprediction"].Clone(),
                           histos["fakeprediction"].Clone(),
                             ]
                         
    #if "Validation" in region or "QCD" in region:
    if plot_data:
        datahist = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_sr_" + category)
 
        # add the rest
        if variable == "region" and region == "HadBaseline":
            xroot_file = root_file.replace("MET", "SingleElectron")
            xdatalabel = datalabel.replace("MET", "SingleElectron")
            xregion = region.replace("HadBaseline", "SElBaseline")
            datahist.Add( get_histo(xroot_file, xdatalabel + "_" + variable + "_" + xregion + "_sr_" + category) )

            xroot_file = root_file.replace("MET", "SingleMuon")
            xdatalabel = datalabel.replace("MET", "SingleMuon")
            xregion = region.replace("HadBaseline", "SMuBaseline")
            datahist.Add( get_histo(xroot_file, xdatalabel + "_" + variable + "_" + xregion + "_sr_" + category) )
    
        datahist.SetTitle("Data")
        makeplot(stacked_histograms, datahist, "")


        # plot prompt and fake CRs:
        ###########################
        canvas = shared_utils.mkcanvas()
        legend = shared_utils.mklegend(x1 = 0.6, y1 = 0.6, x2 = 0.9, y2 = 0.8)
        ymax = 0
        for i_crtype, crtype in enumerate(["fake", "prompt", "sr"]):
            if crtype == "prompt":
                colorbg = color_fakebg
                hlabel = "promptcr"
                llabel = "Prompt CR"
            elif crtype == "fake":
                colorbg = color_promptbg
                hlabel = "fakecr"
                llabel = "Fake CR"
            elif crtype == "sr":
                colorbg = kBlack
                hlabel = "sr"
                llabel = "Signal region"
            histos[hlabel] = get_histo(root_file, datalabel + "_" + variable + "_" + region + "_" + hlabel + "_" + category, lumi, hlabel, colorbg)
            histos[hlabel].SetTitle(";%s;Events" % variable)
            histos[hlabel].SetFillColor(kWhite)
            if i_crtype == 0:
                histos[hlabel].Draw("hist e")
            else:
                histos[hlabel].Draw("hist e same")
            legend.AddEntry(histos[hlabel], llabel)

            if histos[hlabel].GetMaximum() > ymax:
                ymax = histos[hlabel].GetMaximum()
        histos["fakecr"].GetYaxis().SetRangeUser(1e-2, 10.0*ymax)
        legend.Draw()
        shared_utils.stamp()
        os.system("mkdir -p %s_CR" % foldername)
        canvas.SetLogy()
        canvas.SaveAs(foldername + "_CR/" + pdffile + "_cr" + ".pdf")

    else:
        datahist = histos["promptprediction"]
        datahist.Add(histos["fakeprediction"])
        datahist.SetTitle("Added predictions")
        makeplot(stacked_histograms, datahist, "")
            
        
    if "Run2" not in datalabel:
        # genfake vs fakepred, genprompt vs promptpred, all gen vs. all pred:
        if histos["promptprediction"].Integral() > histos["fakeprediction"].Integral():
            stacked_histograms = [
                                   histos["srgenfake"].Clone(),
                                   histos["srgenprompt"].Clone(),
                                 ]
        else:
            stacked_histograms = [
                                   histos["srgenprompt"].Clone(),
                                   histos["srgenfake"].Clone(),
                                 ]
        datahist = histos["srgenprompt"]
        datahist.Add(histos["srgenfake"])
        datahist.SetTitle("Added predictions")
        makeplot(stacked_histograms, datahist, "MCSignal")
        
        # fake cr MC Truth:
        stacked_histograms = [
                               histos["fakecrgenprompt"].Clone(),
                               histos["fakecrgenfake"].Clone(),
                             ]
        datahist = histos["fakecrgenprompt"].Clone()
        datahist.Add(histos["fakecrgenfake"].Clone())
        datahist.SetTitle("Prompt+Fake MC Truth")
        h_sum = histos["fakecrgenprompt"].Clone()
        h_sum.Add(histos["fakecrgenfake"].Clone())
        h_ratio = histos["fakecrgenprompt"].Clone()
        h_ratio.Divide(h_sum)
        makeplot(stacked_histograms, datahist, "MCFakeCR", ratiovalues = h_ratio, ratiolabel = "Prompt cont. (%)", ratio_limits = (-0.01, 1.01), header = "Fake control region")
        
        # prompt cr MC Truth:
        stacked_histograms = [
                               histos["promptcrgenfake"].Clone(),
                               histos["promptcrgenprompt"].Clone(),
                             ]
        datahist = histos["promptcrgenprompt"].Clone()
        datahist.Add(histos["promptcrgenfake"].Clone())
        datahist.SetTitle("Prompt+Fake MC Truth")
        h_sum = histos["promptcrgenprompt"].Clone()
        h_sum.Add(histos["promptcrgenfake"].Clone())
        h_ratio = histos["promptcrgenfake"].Clone()
        h_ratio.Divide(h_sum)
        makeplot(stacked_histograms, datahist, "MCpromptcr", ratiovalues = h_ratio, ratiolabel = "Fake cont. (%)", ratio_limits = (-0.01, 1.01), header = "Prompt control region")

        # closure:
        stacked_histograms = [
                               histos["promptprediction"].Clone(),
                               histos["fakeprediction"].Clone(),
                             ]
        datahist = histos["srgenprompt"]
        datahist.Add(histos["srgenfake"])
        datahist.SetTitle("Prompt+Fake MC Truth")
        makeplot(stacked_histograms, datahist, "Closure")

        # prompt closure:
        stacked_histograms = [
                               histos["promptprediction"].Clone(),
                             ]
        datahist = histos["srgenprompt"]
        datahist.SetTitle("Prompt MC Truth")
        makeplot(stacked_histograms, datahist, "PromptClosure")
        
        # fake closure:
        stacked_histograms = [
                               histos["fakeprediction"].Clone(),
                             ]
        datahist = histos["srgenfake"]
        datahist.SetTitle("Non-prompt MC Truth")
        makeplot(stacked_histograms, datahist, "FakeClosure")
    

if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()

    if len(args)>0:
        histograms_folder = args[0]
    else:
        print "Usage: ./plot_prediction.py <folder>"
        quit()
        
    regions = [
                #"HadBaseline",
                #"SMuBaseline",
                #"SElBaseline",
                "QCDLowMHT",
                #"PromptDYEl",
                #"PromptDYMu",
                #"QCDLowMHT",
                #"PromptDY",
                #"Baseline",
                #"QCDLowMHT",
                #"QCDLowMHT",
                #"QCDLowMHTJets",
                #"QCDLowMHT50",
                #"HadBaseline",
                #"SMuBaseline",
                #"SElBaseline",
                #"QCDLowMHT",
                #"QCDLowMHTJet",
                #"QCDLowMHTValidation",
                #"QCDLowMHTVal",
                #"SMuValidationLowMT",
                #"SElValidationLowMT",
                #"SElValidationHighMT",
                #"SMuValidationHighMT",                
                #"SElValidationZLL",
                #"SMuValidationZLL",
                #"PromptDY",
                #"PromptDYenhanced",
                #"QCDLowMHT",
                #"QCDLowMHTJets",
              ]
    
    variables = [
                          "HT",
                          "MHT",
                          "n_goodjets",
                          "n_btags",
                          "leadinglepton_mt",
                          "invmass",
                          "tracks_mva_sep21v1_baseline_corrdxydz",
                          "tracks_pt",
                          "tracks_eta",
                          "tracks_deDxHarmonic2pixel",
                          "tracks_matchedCaloEnergy",
                          "tracks_nMissingOuterHits",
                          "n_tags",
                          "region",
                ]
                  
    categories = [
                "combined",
                "short",
                "long",
                 ]
                 
    # check data period:
    data_periods = []
    merged_files = glob.glob(histograms_folder + "/merged_*.root")
    for merged_file in merged_files:
        if "All" in merged_file: continue
        for period in [
                        #"Summer16",
                        #"Fall17",
                        #"Run2016",
                        #"Run2017",
                        #"Run2018",
                        "Run2",
                       ]:
            if period in merged_file and period not in data_periods:
                    data_periods.append(period)
                    print "Looking at %s" % period

    outputfolder = histograms_folder + "_plots"

    for region in regions:
        for variable in variables:
            for category in categories:

                if variable == "region" and category is not "combined":
                    continue
                if category == "combined" and not (variable == "region" or variable == "tracks_is_pixel_track"):
                    continue
                    
                print region, variable, category
                for data_period in data_periods:

                    lumi = 137000.0
                    #lumi = 35900

                    data_period_in_list = data_period
    
                    if "Run2" in data_period:

                        if "SEl" in region or "PromptDYEl" in region:
                            merged_histograms_file = histograms_folder + "/merged_%sSingleElectron.root" % data_period
                            data_period += "SingleElectron"
                        elif "SMu" in region or "PromptDYMu" in region:
                            merged_histograms_file = histograms_folder + "/merged_%sSingleMuon.root" % data_period
                            data_period += "SingleMuon"
                        elif "QCD" in region:
                            merged_histograms_file = histograms_folder + "/merged_%sJetHT.root" % data_period
                            data_period += "JetHT"
                        else:
                            merged_histograms_file = histograms_folder + "/merged_%sMET.root" % data_period
                            data_period += "MET"


                    elif "Summer16" in data_period:
                        merged_histograms_file = histograms_folder + "/merged_Summer16.root"
                    elif "Fall17" in data_period:
                        merged_histograms_file = histograms_folder + "/merged_Fall17.root"

                    foldername = outputfolder + "/%s/%s%s" % (data_period_in_list, category.replace("short", "Short").replace("long", "Long"), region)

                    if not os.path.exists(foldername + "/" + region + "_" + variable + "_" + category + ".pdf") or \
                       not os.path.exists(foldername + "_CR/" + region + "_" + variable + "_" + category + "_cr.pdf"):
                        plot_prediction(variable, merged_histograms_file, data_period, category, lumi, region, region + "_" + variable + "_" + category, foldername)     


    
                        

