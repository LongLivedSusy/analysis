#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import os
import collections
import shared_utils
import glob
import multiprocessing
import copy

if True:
    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
    tl = TLatex()
    tl.SetNDC()
    cmsTextFont = 61
    extraTextFont = 50
    lumiTextSize = 0.6
    lumiTextOffset = 0.2
    cmsTextSize = 0.75
    cmsTextOffset = 0.1
    regularfont = 42
    originalfont = tl.GetTextFont()
    epsi = "#scale[1.3]{#font[122]{e}}"
    epsilon = 0.0001
    basesize = tl.GetTextSize()

    datamc = 'Data'
    def stamp(lumi='35.9', showlumi = False, WorkInProgress = True):
        
        tl.SetTextFont(cmsTextFont)
        tl.SetTextSize(0.98*tl.GetTextSize())
        tl.DrawLatex(0.15,0.845, 'CMS')
        tl.SetTextFont(extraTextFont)
        tl.SetTextSize(1.0/0.98*tl.GetTextSize())
        xlab = 0.235
        if WorkInProgress: tl.DrawLatex(xlab,0.845, ' Work in Progress')
        else: tl.DrawLatex(xlab,0.845, ('MC' in datamc)*' simulation '+'preliminary')
        tl.SetTextFont(regularfont)
        tl.SetTextSize(0.81*tl.GetTextSize())    
        thingy = ''
        if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
        xthing = 0.57
        if not showlumi: xthing+=0.13
        tl.DrawLatex(xthing-0.02,0.845,thingy)
        tl.SetTextSize(1.0/0.81*tl.GetTextSize())


if __name__ == "__main__":
   
    #folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_signalLabXY_merged"
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/ntupleanalyzer/skim_SmsGenLoop5_merged"
    

    outputfolder = "plots_labxy_jul20_run2"
    use_noMC = True
    variables = {
                  #'tracks_chiLabXY':                         [25, 0, 1250, "transverse decay length (lab. frame, mm)"],
                  #'tracks_pt':                                [20, 0, 6000, "p_{T}^{#chi} (GeV)"],
                  'tracks_chiLabXY':                          [23, 0, 1250, "transverse decay length (lab. frame, mm)"],
                  #'tracks_pt:tracks_chiLabXY':                [12, 0, 1200, 10, 0, 5000, "transverse decay length (lab. frame, mm); p_{T}^{#chi} (GeV)"],
                  #'tracks_chiPt':                             [20, 0, 10000, "p_{T}^{#chi} (GeV)"],
                  #'tracks_trackerLayersWithMeasurement':      [25, 0, 25, "number of tracker layers"],
                 }   

    datasets = {}
    datasets["2016"] = collections.OrderedDict()
    datasets["2017"] = collections.OrderedDict()
    datasets["2018"] = collections.OrderedDict()            
    datasets["Run2"] = collections.OrderedDict()            
    #datasets["2016"]["short: (2.0, 1.975) TeV"] = [["RunIISummer16MiniAODv3.SMS-T1qqqq"], kOrange, "tracks_is_pixel_track==1 && tracks_pt>25 && tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2000 && signal_lsp_mass==1975"]
    #datasets["2016"]["short: (2.5, 2.475) TeV"] = [["RunIISummer16MiniAODv3.SMS-T1qqqq"], kGreen,  "tracks_is_pixel_track==1 && tracks_pt>25 && tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2500 && signal_lsp_mass==2475"]
    #datasets["2016"]["short: (2.8, 2.775) TeV"] = [["RunIISummer16MiniAODv3.SMS-T1qqqq"], kTeal,   "tracks_is_pixel_track==1 && tracks_pt>25 && tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2800 && signal_lsp_mass==2775"]
    #datasets["2016"]["long: (2.0, 1.975) TeV"] = [["RunIISummer16MiniAODv3.SMS-T1qqqq"], kOrange,  "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2000 && signal_lsp_mass==1975"]
    #datasets["2016"]["long: (2.5, 2.475) TeV"] = [["RunIISummer16MiniAODv3.SMS-T1qqqq"], kGreen,   "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2500 && signal_lsp_mass==2475"]
    #datasets["2016"]["long: (2.8, 2.775) TeV"] = [["RunIISummer16MiniAODv3.SMS-T1qqqq"], kTeal,    "tracks_is_pixel_track==0 && tracks_pt>40 && tracks_nMissingOuterHits>=2 && tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2800 && signal_lsp_mass==2775"]
    #datasets["2016"]["T2bt: (2.0, 1.9) TeV"] = [["RunIISummer16MiniAODv3.SMS-T2bt-LLChipm"], kAzure, "tracks_chiCandGenMatchingDR<0.01 && signal_stop_mass==2000 && signal_lsp_mass==1900"]
    #datasets["2016"]["T2bt: (2.0, 1.4) TeV"] = [["RunIISummer16MiniAODv3.SMS-T2bt-LLChipm"], kTeal, "tracks_chiCandGenMatchingDR<0.01 && signal_stop_mass==2500 && signal_lsp_mass==1400"]

    #datasets["2017"]["T1qqqq: (2.0,    1.975) TeV"] = [["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq"], kRed+2, "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2000 && signal_lsp_mass==1975"]
    #datasets["2017"]["T1qqqq: (2.8, 1.4) TeV"] = [["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq"], kOrange,  "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2800 && signal_lsp_mass==1400"]
    #datasets["2017"]["T1qqqq: (1.2, 0.2) TeV"] = [["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq"], kTeal,  "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==1200 && signal_lsp_mass==200"]
    #datasets["2017"]["T1qqqq: (2.5, 2.475) TeV"] = [["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq"], kOrange+2,  "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2500 && signal_lsp_mass==2475"]
    #datasets["2017"]["T1qqqq: (2.8, 2.775) TeV"] = [["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq"], kAzure,   "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==2800 && signal_lsp_mass==2775"]
    #datasets["2017"]["T1qqqq"] = [["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq"], kBlack,  "tracks_chiCandGenMatchingDR<0.01"]

    datasets["2016"]["T6btLL (2016)"] = [["RunIISummer16MiniAODv3.SMS-T1qqqq"], kAzure,  "tracks_chiCandGenMatchingDR<0.01"]
    datasets["2016"]["T2btLL (2016)"] = [["RunIISummer16MiniAODv3.SMS-T2bt-LLChipm"], kRed,  "tracks_chiCandGenMatchingDR<0.01"]

    datasets["2017"]["T6btLL (2017)"] = [["RunIIFall17FSv3.SMS-T1btbt"], kAzure,  "tracks_chiCandGenMatchingDR<0.01"]
    datasets["2017"]["T2btLL (2017)"] = [["RunIIFall17FSv3.SMS-T2bt"], kRed,  "tracks_chiCandGenMatchingDR<0.01"]
    #datasets["2017"]["TChi (2017)"] = [["higgsino*Fall17"], kGreen,  "tracks_chiCandGenMatchingDR<0.01"]
    #datasets["2017"]["T2tbLL (2017)"] = [["RunIIFall17FSv3.SMS-T2tb"], kOrange,  "tracks_chiCandGenMatchingDR<0.01"]

    datasets["2018"]["T6btLL (2018)"] = [["RunIIAutumn18FSv3.SMS-T1btbt"], kAzure,  "tracks_chiCandGenMatchingDR<0.01"]
    datasets["2018"]["T2btLL (2018)"] = [["RunIIAutumn18FSv3.SMS-T2bt"], kRed,  "tracks_chiCandGenMatchingDR<0.01"]
    #datasets["2018"]["TChi (2018)"] = [["higgsino*Autumn18"], kGreen,  "tracks_chiCandGenMatchingDR<0.01"]
    #datasets["2018"]["T2tbLL (2018)"] = [["RunIIAutumn18FSv3.SMS-T2tb"], kOrange,  "tracks_chiCandGenMatchingDR<0.01"]

    datasets["Run2"]["T6btLL (2016)"] = [["RunIISummer16MiniAODv3.SMS-T1qqqq"], kAzure,  "tracks_chiCandGenMatchingDR<0.01"]
    datasets["Run2"]["T2btLL (2016)"] = [["RunIISummer16MiniAODv3.SMS-T2bt-LLChipm"], kRed,  "tracks_chiCandGenMatchingDR<0.01"]
    datasets["Run2"]["T6btLL (2017)"] = [["RunIIFall17FSv3.SMS-T1btbt"], kAzure,  "tracks_chiCandGenMatchingDR<0.01"]
    datasets["Run2"]["T2btLL (2017)"] = [["RunIIFall17FSv3.SMS-T2bt"], kRed,  "tracks_chiCandGenMatchingDR<0.01"]
    datasets["Run2"]["T6btLL (2018)"] = [["RunIIAutumn18FSv3.SMS-T1btbt"], kAzure,  "tracks_chiCandGenMatchingDR<0.01"]
    datasets["Run2"]["T2btLL (2018)"] = [["RunIIAutumn18FSv3.SMS-T2bt"], kRed,  "tracks_chiCandGenMatchingDR<0.01"]

    #datasets["2017"]["T1qqqq: (1.2, 0.2) TeV"] = [["RunIIFall17MiniAODv2.FastSim-SMS-T1qqqq"], kTeal,  "tracks_chiCandGenMatchingDR<0.01 && signal_gluino_mass==1200 && signal_lsp_mass==200"]
    #RunIISummer16MiniAODv3.SMS-T1qqqq

    for efficiencystudy in [
                            #"preselection",
                            "preselectionAndTag",
                            #"preselectionAndTagAllChi",
                           ]:  

        for phase in [
                      #"2016",
                      #"2017",
                      #"2018",
                      "Run2",
                     ]:  

            for category in [
                             "combined",
                             "short",
                             "long",
                            ]:

                for variable in variables:

                    histos = collections.OrderedDict()
                    histosNum = collections.OrderedDict()
                    histosDenom = collections.OrderedDict()
                    labels = datasets[phase]
                    binnings = variables[variable]

                    canvas = shared_utils.mkcanvas()
                    if ":" not in variable:
                        canvas.SetLogy(False)
                    else:
                        canvas.SetLogz(False)
                    legend = shared_utils.mklegend(x1 = 0.45, y1 = 0.7, x2 = 0.88, y2 = 0.88)
                    legend.SetTextSize(0.035)
                    canvas.SetFillColorAlpha(0,0)    

                    for label in labels:

                        globstring = labels[label][0][0]
                        color = labels[label][1]
                        histos[label] = 0
                        input_files = glob.glob(folder + "/" + globstring + "*root")

                        #chiCandGenMatchingDR

                        if efficiencystudy == "preselection":
                            yaxislabel = "pre-selection efficiency"
                            legendlabel = "denominator = all #chi_{1}^{#pm} in event"
                            
                            # all charginos:
                            denominator = "tracks_chiCandGenMatchingDR>=-1"
                            # matched charginos, pre-selection:
                            numerator = "tracks_category==1 && tracks_baseline==1 && tracks_chiCandGenMatchingDR<0.01"
                                                        
                        elif efficiencystudy == "preselectionAndTag":
                            yaxislabel = "pre-selection + DT tag"
                            legendlabel = "denominator = all #chi_{1}^{#pm} in event"
                            if phase == "2016":
                                shortTag = "tracks_mva_sep21v1_baseline_corrdxydz>0.1 && tracks_matchedCaloEnergy<15"
                                LongTag = "tracks_mva_sep21v1_baseline_corrdxydz>0.12 && tracks_matchedCaloEnergy/tracks_p<0.2"
                            else:
                                shortTag = "tracks_mva_sep21v1_baseline_corrdxydz>0.15 && tracks_matchedCaloEnergy<15"
                                LongTag = "tracks_mva_sep21v1_baseline_corrdxydz>0.08 && tracks_matchedCaloEnergy/tracks_p<0.2"
                            
                            # all charginos:
                            denominator = "tracks_chiCandGenMatchingDR>=-1"
                            # matched charginos, pre-selection and tag:
                            numerator = "tracks_category==1 && tracks_baseline==1 && tracks_chiCandGenMatchingDR<0.01 && ((tracks_is_pixel_track==1 && %s) || (tracks_is_pixel_track==0 && %s))" % (shortTag, LongTag)
                                                        
                            #    #denom:
                            if category == "short":
                                numerator += " && tracks_is_pixel_track==1 "
                            elif category == "long":
                                numerator += " && tracks_is_pixel_track==0 "

                        legend.SetHeader(legendlabel)

                        numevents = -1

                        if len(binnings) > 4:
                            currenthisto =       plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=numerator, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2], nBinsY=binnings[3], ymin=binnings[4], ymax=binnings[5], numevents=numevents)
                            currenthisto_denom = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=denominator, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2], nBinsY=binnings[3], ymin=binnings[4], ymax=binnings[5], numevents=numevents)
                        else:
                            
                            if variable == "tracks_pt":
                                numerator += " && tracks_chiLabXY<1100"
                                denominator += " && tracks_chiLabXY<1100"
                            
                            currenthisto =       plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=numerator, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2], numevents=numevents)
                            currenthisto_denom = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=denominator, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2], numevents=numevents)
                        
                        histosNum[label] = currenthisto.Clone()
                        histosDenom[label] = currenthisto_denom.Clone()
                                            
                    # scale years:
                    histosNum["T6btLL (2016)"].Scale(36.3/136.76)
                    histosNum["T6btLL (2017)"].Scale(41.37/136.76)
                    histosNum["T6btLL (2018)"].Scale(59.09/136.76)
                    histosNum["T2btLL (2016)"].Scale(36.3/136.76)
                    histosNum["T2btLL (2017)"].Scale(41.37/136.76)
                    histosNum["T2btLL (2018)"].Scale(59.09/136.76)
                    histosDenom["T6btLL (2016)"].Scale(36.3/136.76)
                    histosDenom["T6btLL (2017)"].Scale(41.37/136.76)
                    histosDenom["T6btLL (2018)"].Scale(59.09/136.76)
                    histosDenom["T2btLL (2016)"].Scale(36.3/136.76)
                    histosDenom["T2btLL (2017)"].Scale(41.37/136.76)
                    histosDenom["T2btLL (2018)"].Scale(59.09/136.76)
                    
                    # combine years:
                    histosNumNew = collections.OrderedDict()
                    histosNumNew["T6btLL"] = histosNum["T6btLL (2016)"].Clone()                
                    histosNumNew["T6btLL"].Add(histosNum["T6btLL (2017)"])                
                    histosNumNew["T6btLL"].Add(histosNum["T6btLL (2018)"])                
                    histosNumNew["T2btLL"] = histosNum["T2btLL (2016)"].Clone()
                    histosNumNew["T2btLL"].Add(histosNum["T2btLL (2017)"])
                    histosNumNew["T2btLL"].Add(histosNum["T2btLL (2018)"])
                    histosNum = histosNumNew 
                    
                    histosDenomNew = collections.OrderedDict()
                    histosDenomNew["T6btLL"] = histosDenom["T6btLL (2016)"].Clone()                
                    histosDenomNew["T6btLL"].Add(histosDenom["T6btLL (2017)"])                
                    histosDenomNew["T6btLL"].Add(histosDenom["T6btLL (2018)"])                
                    histosDenomNew["T2btLL"] = histosDenom["T2btLL (2016)"].Clone()
                    histosDenomNew["T2btLL"].Add(histosDenom["T2btLL (2017)"])
                    histosDenomNew["T2btLL"].Add(histosDenom["T2btLL (2018)"])
                    histosDenom = histosDenomNew 
                    
                    histos = collections.OrderedDict()
                    histos["T6btLL"] = 0
                    histos["T2btLL"] = 0
                    
                    print "histos[]", histos
                                    
                    labels = ["T6btLL", "T2btLL"]
                    
                    for label in labels:

                        if label == "T6btLL":
                            color = kBlue
                        if label == "T2btLL":
                            color = kRed

                        histosNum[label].Divide(histosDenom[label])
                        shared_utils.histoStyler(histosNum[label])
                        histos[label] = histosNum[label].Clone()
                        histos[label].SetDirectory(0)
                        histos[label].GetXaxis().SetLabelSize(0.6 * histos[label].GetXaxis().GetLabelSize())
                        #histos[label].GetXaxis().SetTitleSize(0. * histos[label].GetXaxis().GetTitleSize())
                        histos[label].GetYaxis().SetLabelSize(histos[label].GetXaxis().GetLabelSize())
                        histos[label].GetZaxis().SetLabelSize(0.6 * histos[label].GetYaxis().GetLabelSize())
                        histos[label].GetYaxis().SetTitleSize(0.7 * histos[label].GetYaxis().GetTitleSize())
                        histos[label].GetYaxis().SetMaxDigits(4)
                        
                        histos[label].SetTitleSize(0.6 * histos[label].GetTitleSize())
                        histos[label].SetTitle(label)
                        histos[label].SetLineColor(color)
                        if len(binnings) > 4:
                            #histos[label].SetTitle(";%s;#epsilon (%s)" % (binnings[6], yaxislabel))
                            histos[label].SetTitle(";%s;efficiency" % (binnings[6]))
                            histos[label].GetZaxis().SetRangeUser(0,1.0)
                        else:
                            #histos[label].SetTitle(";%s;#epsilon (%s)" % (binnings[3], yaxislabel))
                            histos[label].SetTitle(";%s;efficiency" % (binnings[3]))

                        # normalize:
                        #if histos[label].Integral()>0:
                        #    histos[label].Scale(1.0/histos[label].Integral())
                        histos[label].GetXaxis().SetNdivisions(6)


                    if ":" in variable:
                        
                        for i_label, label in enumerate(histos):
                            histos[label].Draw("colz")
                            #histos[label].GetYaxis().SetRangeUser(0,1.2)
                            #legend.AddEntry(histos[label], label)            
                            #canvas.SetLogz(False)
                            shared_utils.stamp(datamc_="mc")
                            os.system("mkdir -p %s" % outputfolder)
                            pdfname = "%s/%s_%s_%s_%s_%s.pdf" % (outputfolder, variable.replace("/", "_").replace("*", "times").replace("/", "by"), label, category, phase, efficiencystudy)
                            pdfname = pdfname.replace(":", "_")
                            canvas.SaveAs(pdfname)
                            canvas.SaveAs(pdfname.replace(".pdf", ".root"))
                        
                    else:

                        for i_label, label in enumerate(histos):
                            if not i_label:
                                histos[label].Draw("hist")
                            else:
                                histos[label].Draw("hist same")
                            if "XXX" in label:
                                histos[label].SetLineStyle(2)
                            else:
                               histos[label].SetLineStyle(1)
                            #histos[label].GetYaxis().SetRangeUser(1e-4,2e0)
                            histos[label].GetYaxis().SetRangeUser(0,1.0)
                            legend.AddEntry(histos[label], label)            
                        
                        #canvas.SetGridx(True)
                        canvas.SetGridy(True)
                        canvas.SetLogy(False)
                        
                        if category == "short":
                            legend.SetHeader("short tracks")
                        if category == "long":
                            legend.SetHeader("long tracks")
                        legend.Draw()
                        shared_utils.stamp(datamc_="mc")
                                
                        os.system("mkdir -p %s" % outputfolder)
                        pdfname = "%s/%s_%s_%s_%s.pdf" % (outputfolder, variable.replace("/", "_").replace("*", "times").replace("/", "by"), category, phase, efficiencystudy)
                            
                        pdfname = pdfname.replace(":", "_")
                        
                        canvas.SaveAs(pdfname)
                        canvas.SaveAs(pdfname.replace(".pdf", ".root"))
                        
                        #fout = TFile(pdfname.replace(".pdf", "_histos.root"), "recreate")
                        fout = TFile(pdfname.replace(".pdf", "_histos.root"), "recreate")
                        for i_label, label in enumerate(histos):
                            hname = variable + "_" + phase + "_" + category
                            histos[label].SetName(hname)
                            histos[label].Write()
                        fout.Close()
                        
                        
