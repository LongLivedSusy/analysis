#!/bin/env python
from __future__ import division
import __main__ as main
import GridEngineTools
from ROOT import *
import plotting
import collections
import glob
import os
from optparse import OptionParser

def getBinContent_with_overflow(histo, xval, yval = False):
    
    if not yval:
        # overflow for TH1Fs:
        if xval >= histo.GetXaxis().GetXmax():
            value = histo.GetBinContent(histo.GetXaxis().GetNbins())
        else:
            value = histo.GetBinContent(histo.GetXaxis().FindBin(xval))
        return value
    else:
        # overflow for TH2Fs:
        if xval >= histo.GetXaxis().GetXmax() and yval < histo.GetYaxis().GetXmax():
            xbins = histo.GetXaxis().GetNbins()
            value = histo.GetBinContent(xbins, histo.GetYaxis().FindBin(yval))
        elif xval < histo.GetXaxis().GetXmax() and yval >= histo.GetYaxis().GetXmax():
            ybins = histo.GetYaxis().GetNbins()
            value = histo.GetBinContent(histo.GetXaxis().FindBin(xval), ybins)
        elif xval >= histo.GetXaxis().GetXmax() or yval >= histo.GetYaxis().GetXmax():
            xbins = histo.GetXaxis().GetNbins()
            ybins = histo.GetYaxis().GetNbins()
            value = histo.GetBinContent(xbins, ybins)
        else:
            value = histo.GetBinContent(histo.GetXaxis().FindBin(xval), histo.GetYaxis().FindBin(yval))
        return value


def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]


def fakerate_rebin(histo, variable, category):

    if variable == "HT_n_allvertices":
        if category == "short":
            histo = histo.RebinX(3)
            histo = histo.RebinY(3)
        else:
            histo = histo.RebinX(3)
            histo = histo.RebinY(3)
    elif variable == "HT":
        if category == "short":
            histo = histo.Rebin(10)
        else:
            histo = histo.Rebin(2)
    elif variable == "n_allvertices":
        histo = histo.Rebin(5)
    elif variable == "n_goodjets":
        histo = histo.Rebin(2)
    elif variable == "MinDeltaPhiMhtJets":
        histo = histo.Rebin(2)

    return histo
    

def calculate_fakerate(variables, folder, output_file, datasets, regions, region_fakeids):
        
    os.system("hadd -f fakerate_numdenom.root %s/*root" % folder)
    os.system("rm %s" % output_file)

    for dataset in datasets:
        for variable in variables:
            variable = variable.replace(":", "_")
            for category in ["short", "long"]:
                for region in regions:
                    for region_fakeid in region_fakeids:

                        dedx = ""
                        fin = TFile("fakerate_numdenom.root", "read")       
                                                
                        numerator = fin.Get("%s_%s_%s_sr%s_%s" % (dataset, variable, region, dedx, category))
                        numerator.SetDirectory(0)
                        numerator = fakerate_rebin(numerator, variable, category)
                        
                        denominator = fin.Get("%s_%s_%s_fakecr%s%s_%s" % (dataset, variable, region, region_fakeid, dedx, category))
                        denominator.SetDirectory(0)
                        denominator = fakerate_rebin(denominator, variable, category)
                        
                        fin.Close()
                        
                        fakerate = numerator.Clone()
                        fakerate.Divide(denominator)
                        fakerate.SetName(fakerate.GetName().replace("_sr", "_fakerate" + region_fakeid).replace("JetHT", ""))
                        fakerate.SetTitle(fakerate.GetTitle().replace("_sr", "_fakerate" + region_fakeid).replace("JetHT", ""))
                        
                        fout = TFile(output_file, "update")
                        fakerate.Write()                        
                        fout.Close()


def write_histogram_to_file(variable, binnings, cuts, scaling, h_suffix, folder, label, globstrings, output_folder, fakerate_file):

    h_name = label + "_" + variable + "_" + h_suffix
    h_name = h_name.replace(":", "_")

    if os.path.exists(output_folder + "/" + h_name + ".root"):
        print "Already done"
        return

    # if scaling is specified, get histogram from fakerate.root file:

    if scaling == "":
        histo = False
        for globstring in globstrings:
            input_files = glob.glob(folder + "/" + globstring + "*.root")
            if len(input_files) > 0:
                if not ":" in variable:
                    current_histo = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cuts, scaling=scaling, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2])
                else:
                    current_histo = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cuts, scaling=scaling, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2], nBinsY=binnings[3], ymin=binnings[4], ymax=binnings[5])
        
            if not histo:
                histo = current_histo.Clone()
                histo.SetDirectory(0)
            else:
                histo.Add(current_histo.Clone())
    
    else:
        
        fin = TFile(fakerate_file, "open")
        if "Run2016" in label:
            h_fakerate = fin.Get("Run2016GH_" + scaling)
        else:
            h_fakerate = fin.Get(label + "_" + scaling)
        h_fakerate.SetDirectory(0)
        fin.Close()

        # evaluate 2D HT-PU fakerate map:

        bins = []
        for ibinx in range(1,h_fakerate.GetXaxis().GetNbins()+1):
            for ibiny in range(1,h_fakerate.GetYaxis().GetNbins()+1):
                value = h_fakerate.GetBinContent(ibinx, ibiny)
                x_low = h_fakerate.GetXaxis().GetBinLowEdge(ibinx)
                x_high = x_low + h_fakerate.GetXaxis().GetBinWidth(ibinx)
                y_low = h_fakerate.GetYaxis().GetBinLowEdge(ibiny)  
                y_high = y_low + h_fakerate.GetYaxis().GetBinWidth(ibiny)
                bins.append( [x_low, x_high, y_low, y_high, value] )
                
        histo = False
        for ibin in bins:
            
            mycuts = cuts + " && n_allvertices>%s && n_allvertices<%s && HT>%s && HT<%s" % (ibin[0], ibin[1], ibin[2], ibin[3])
            mycuts = mycuts.replace(" && HT<900.0", "")
            mycuts = mycuts.replace(" && n_allvertices<45.0", "")
            scalingfactor = ibin[4]
            
            for globstring in globstrings:
                input_files = glob.glob(folder + "/" + globstring + "*.root")
                if len(input_files) > 0:
                    if not ":" in variable:
                        current_histo = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=mycuts, scaling=scalingfactor, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2])
                    else:
                        current_histo = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=mycuts, scaling=scalingfactor, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2], nBinsY=binnings[3], ymin=binnings[4], ymax=binnings[5])
            
                if not histo:
                    histo = current_histo.Clone()
                    histo.SetDirectory(0)
                else:
                    histo.Add(current_histo.Clone())

    fout = TFile(output_folder + "/" + h_name + ".root", "recreate")
    histo.SetName(h_name)
    histo.SetTitle(h_name)
    histo.Write()
    fout.Close()



if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index")
    parser.add_option("--plots_per_job", dest = "plots_per_job", default = 1)
    parser.add_option("--type", dest = "type", default = "analysis")
    parser.add_option("--folder", dest = "output_folder", default = "ddbg")
    parser.add_option("--runmode", dest = "runmode", default = "multi")
    parser.add_option("--hadd", dest = "hadd", action = "store_true")
    parser.add_option("--runall", dest = "runall", action = "store_true")
    parser.add_option("--calculatefakerate", dest = "calculatefakerate", action = "store_true")
    (options, args) = parser.parse_args()
    
    this_scripts_name = main.__file__

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
    
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/skim_09_cand_merged"
    
    binnings = {}
    binnings["analysis"] = {}
    binnings["analysis"]["LepMT"] = [50, 0, 100]
    #binnings["analysis"]["LepMT"] = [16, 0, 160]
    binnings["analysis"]["leptons_mt"] = binnings["analysis"]["LepMT"]
    binnings["analysis"]["leadinglepton_mt"] = binnings["analysis"]["LepMT"]
    binnings["analysis"]["InvMass"] = [50, 0, 200]
    binnings["analysis"]["tracks_invmass"] = binnings["analysis"]["InvMass"]
    binnings["analysis"]["Ht"] = [35 , 0, 700]
    binnings["analysis"]["HT"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["Met"] = [35 , 0, 700]
    binnings["analysis"]["MET"] = binnings["analysis"]["Met"]
    binnings["analysis"]["Mht"] = [35 , 0, 700]
    binnings["analysis"]["MHT"] = binnings["analysis"]["Mht"]
    binnings["analysis"]["tracks_pt"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["leadinglepton_pt"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["leadinglepton_eta"] = [15, 0, 3]
    binnings["analysis"]["tracks_eta"] = [15, 0, 3]
    binnings["analysis"]["tracks_dxyVtx"] = [20, 0, 0.1]
    binnings["analysis"]["DeDxAverage"] = [60, 0, 6]
    binnings["analysis"]["tracks_massfromdeDxPixel"] = binnings["analysis"]["DeDxAverage"]
    binnings["analysis"]["DeDxAverageCorrected"] = binnings["analysis"]["DeDxAverage"]
    binnings["analysis"]["tracks_deDxHarmonic2pixel"] = binnings["analysis"]["DeDxAverage"]
    binnings["analysis"]["tracks_deDxHarmonic2pixelCorrected"] = binnings["analysis"]["DeDxAverage"]
    binnings["analysis"]["BinNumber"] = [ 88, 1, 89]
    binnings["analysis"]["region"] = binnings["analysis"]["BinNumber"]
    binnings["analysis"]["n_tags"] = [ 3, 0, 3]
    binnings["analysis"]["n_goodjets"] = [ 10, 0, 10]
    binnings["analysis"]["n_btags"] = binnings["analysis"]["n_goodjets"]
    binnings["analysis"]["n_goodelectrons"] = [ 5, 0, 5]
    binnings["analysis"]["n_goodmuons"] = [ 5, 0, 5]
    binnings["analysis"]["MinDeltaPhiMhtJets"] = [ 16, 0, 3.2]
    binnings["analysis"]["BTags"] = [ 4, 0, 4]
    binnings["analysis"]["Track1MassFromDedx"] = [ 25, 0, 1000]
    binnings["analysis"]["Log10DedxMass"] = [10, 0, 5]
    binnings["analysis"]["regionCorrected"] = [54,1,55]
    binnings["analysis"]["regionCorrected_sideband"] = binnings["analysis"]["regionCorrected"]
    binnings["analysis"]["region"] = binnings["analysis"]["regionCorrected"]
    binnings["analysis"]["region_sideband"] = binnings["analysis"]["regionCorrected"]

    binnings["fakerate"] = {}
    binnings["fakerate"]["tracks_pt"] = [20, 0, 1000]
    binnings["fakerate"]["HT"] = [10, 0, 1000]
    binnings["fakerate"]["MHT"] = [10, 0, 1000]
    binnings["fakerate"]["n_allvertices"] = [25, 0, 50]
    binnings["fakerate"]["n_goodjets"] = [20, 0, 20]
    binnings["fakerate"]["n_btags"] = [10, 0, 10]
    binnings["fakerate"]["MinDeltaPhiMhtJets"] = [100, 0, 5]
    binnings["fakerate"]["tracks_eta"] = [12, -3, 3]
    binnings["fakerate"]["tracks_phi"] = [16, -4, 4]
    binnings["fakerate"]["HT:n_allvertices"] = [10, 0, 50, 10, 0, 1000]

    dEdxSidebandLow = 1.6
    dEdxLow = 2.1
    dEdxMid = 4.0

    # construct all histograms:
    zones = collections.OrderedDict()
    for dedx in ["", "_SidebandDeDx", "_MidDeDx", "_HighDeDx"]:
        if dedx == "_SidebandDeDx":
            lower = dEdxSidebandLow; upper = dEdxLow
        elif dedx == "_MidDeDx":
            lower = dEdxLow; upper = dEdxMid
        elif dedx == "_MidHighDeDx":
            lower = dEdxLow; upper = 9999
        elif dedx == "_HighDeDx":
            lower = dEdxMid; upper = 9999
        elif dedx == "":
            lower = 0; upper = 9999
        
        for is_pixel_track, category in enumerate(["long", "short"]):

            morecuts = " && tracks_is_pixel_track==%s && tracks_deDxHarmonic2pixelCorrected>%s && tracks_deDxHarmonic2pixelCorrected<%s" % (is_pixel_track, lower, upper)

            zones["sr%s_%s" % (dedx, category)] = [" && tracks_SR_%s==1 && %s" % (category, morecuts), ""]
            zones["srgenfake%s_%s" % (dedx, category)] = [" && tracks_SR_%s==1 && tracks_fake==1 && %s" % (category, morecuts), ""]
            zones["srgenprompt%s_%s" % (dedx, category)] = [" && tracks_SR_%s==1 && tracks_fake==0 && %s" % (category, morecuts), ""]
            zones["fakecr%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && %s" % (category, morecuts), ""]
            zones["fakeprediction%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && %s" % (category, morecuts), "HT_n_allvertices_QCDLowMHT_fakerate_%s" % category]
            
            # add more variations:
            region_fakeids = collections.OrderedDict()
            region_fakeids["MVA"] = "tracks_mva_loose>-0.2"
            region_fakeids["EDep10"] = "tracks_matchedCaloEnergy<10"
            for region_fakeid in region_fakeids:
                zones["srgenfake%s%s_%s" % (region_fakeid, dedx, category)] = [" && tracks_SR_%s==1 && tracks_fake==1 && %s && %s" % (category, morecuts, region_fakeids[region_fakeid]), ""]
                zones["fakecr%s%s_%s" % (region_fakeid, dedx, category)] = [" && tracks_CR_%s==1 && %s && %s" % (category, morecuts, region_fakeids[region_fakeid]), ""]
                zones["fakeprediction%s%s_%s" % (region_fakeid, dedx, category)] = [" && tracks_CR_%s==1 && %s && %s" % (category, morecuts, region_fakeids[region_fakeid]), "HT_n_allvertices_QCDLowMHT_fakerate%s_%s" % (region_fakeid, category)]
            
            #zones["PromptEl%s" % dedx] = [" && leadinglepton_dedx>%s && leadinglepton_dedx<%s" % (lower, upper), ""]
            #zones["prompt"] = ["(tracks_SR_short+tracks_SR_long)==0", ""]
            #zones["promptMu%s" % dedx] = [" && (tracks_SR_short+tracks_SR_long)==0 && n_goodelectrons==0 && n_goodmuons==1 && leadinglepton_dedx>%s && leadinglepton_dedx<%s" % (lower, upper), ""]

    # remove superfluous zone cuts:
    for zone_label in zones:
        for delstring in ["&& tracks_deDxHarmonic2pixelCorrected<9999", "&& tracks_deDxHarmonic2pixelCorrected>0"]:
            if delstring in zones[zone_label][0]:
                zones[zone_label][0] = zones[zone_label][0].replace(delstring, "")
   
    event_selections = {}
    event_selections["analysis"] = collections.OrderedDict()
    event_selections["analysis"]["Baseline"] =          "(n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))"
    ##event_selections["analysis"]["BaselineElectrons"] = "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90"
    ##event_selections["analysis"]["BaselineMuons"] =     "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110 && leadinglepton_mt>90"
    event_selections["analysis"]["HadBaseline"] =       "HT>150 && MHT>150 && n_goodjets>=1 && n_goodleptons==0"
    event_selections["analysis"]["SMuBaseline"] =       "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leadinglepton_mt>90"
    event_selections["analysis"]["SMuValidationZLL"] =  "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90"
    event_selections["analysis"]["SMuValidationMT"] =   "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<70"
    event_selections["analysis"]["SElBaseline"] =       "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90"
    event_selections["analysis"]["SElValidationZLL"] =  "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90"
    event_selections["analysis"]["SElValidationMT"] =   "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leadinglepton_mt<70"
    #event_selections["analysis"]["PromptEl"] =         "n_goodelectrons==1 && n_goodmuons==0"
    #event_selections["analysis"]["PromptDiEl"] =        "dilepton_invmass>0 && n_goodelectrons==2 && n_goodmuons==0"

    event_selections["fakerate"] = collections.OrderedDict()
    event_selections["fakerate"]["QCDLowMHT"] =         "n_goodleptons==0 && MHT<150"
    
    variables = {}
    
    variables["analysis"] = [
                              "leadinglepton_mt",
                              "tracks_invmass",
                              "tracks_is_pixel_track",
                              "tracks_pt",
                              "tracks_eta",
                              "HT",
                              "MHT",
                              "tracks_deDxHarmonic2pixelCorrected",
                              "n_goodjets",
                              "n_btags",
                              "regionCorrected",
                              "regionCorrected_sideband",
                            ]
    variables["fakerate"] = [
                              #"tracks_pt",
                              #"HT",
                              #"MHT",
                              #"n_goodjets",
                              #"n_allvertices",
                              #"n_btags",
                              #"MinDeltaPhiMhtJets",
                              "HT:n_allvertices",
                            ]
                      
    os.system("mkdir -p %s" % options.output_folder)
    
    Summer16 = [
                "Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1",
                "Summer16.QCD_HT200to300_TuneCUETP8M1",
                "Summer16.QCD_HT300to500_TuneCUETP8M1",
                "Summer16.QCD_HT500to700_TuneCUETP8M1",
                "Summer16.QCD_HT700to1000_TuneCUETP8M1",
                "Summer16.QCD_HT1000to1500_TuneCUETP8M1",
                "Summer16.QCD_HT1500to2000_TuneCUETP8M1",
                "Summer16.QCD_HT2000toInf_TuneCUETP8M1",
                "Summer16.TTJets_DiLept",
                "Summer16.TTJets_SingleLeptFromT",
                "Summer16.WJetsToLNu_HT-200To400_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-400To600_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-600To800_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-800To1200_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-1200To2500_TuneCUETP8M1",
                "Summer16.WJetsToLNu_HT-2500ToInf_TuneCUETP8M1",
                "Summer16.WJetsToLNu_TuneCUETP8M1",
                "Summer16.ZZ_TuneCUETP8M1",
                "Summer16.WW_TuneCUETP8M1",
                "Summer16.WZ_TuneCUETP8M1",
                "Summer16.ZJetsToNuNu_HT-100To200_13TeV",
                "Summer16.ZJetsToNuNu_HT-200To400_13TeV",
                "Summer16.ZJetsToNuNu_HT-400To600_13TeV",
                "Summer16.ZJetsToNuNu_HT-600To800_13TeV",
                "Summer16.ZJetsToNuNu_HT-800To1200_13TeV",
                "Summer16.ZJetsToNuNu_HT-1200To2500_13TeV",
                "Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV",
                ]

    Summer16QCDZJets = [
                "Summer16.QCD_HT200to300_TuneCUETP8M1",
                "Summer16.QCD_HT300to500_TuneCUETP8M1",
                "Summer16.QCD_HT500to700_TuneCUETP8M1",
                "Summer16.QCD_HT700to1000_TuneCUETP8M1",
                "Summer16.QCD_HT1000to1500_TuneCUETP8M1",
                "Summer16.QCD_HT1500to2000_TuneCUETP8M1",
                "Summer16.QCD_HT2000toInf_TuneCUETP8M1",
                "Summer16.ZJetsToNuNu_HT-100To200_13TeV",
                "Summer16.ZJetsToNuNu_HT-200To400_13TeV",
                "Summer16.ZJetsToNuNu_HT-400To600_13TeV",
                "Summer16.ZJetsToNuNu_HT-600To800_13TeV",
                "Summer16.ZJetsToNuNu_HT-800To1200_13TeV",
                "Summer16.ZJetsToNuNu_HT-1200To2500_13TeV",
                "Summer16.ZJetsToNuNu_HT-2500ToInf_13TeV",
                ]
                
    Run2016GHJetHT = [
                "Run2016G*JetHT",
                "Run2016H*JetHT",
                ]

    parameters = []
    for variable in variables[options.type]:            
        for event_selection in event_selections[options.type]:
            for zone in zones:

                h_suffix = event_selection + "_" + zone

                cuts = event_selections[options.type][event_selection] + zones[zone][0]
                scaling = zones[zone][1]
                                
                # don't do any scaling for fakerate determination:
                if scaling != "" and options.type == "fakerate":
                    continue
                if "DeDx" in h_suffix and options.type == "fakerate":
                    continue
                    
                fakerate_file = "fakerate_%s.root" % options.output_folder

                parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Summer16", Summer16, options.output_folder, fakerate_file])
                
                if options.type == "analysis":
                    if "SEl" in h_suffix and not "genfake" in h_suffix and not "genprompt" in h_suffix:
                        parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016SingleElectron", ["Run2016*SingleElectron"], options.output_folder, fakerate_file])
                    if "SMu" in h_suffix and not "genfake" in h_suffix and not "genprompt" in h_suffix:
                        parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016SingleMuon", ["Run2016*SingleMuon"], options.output_folder, fakerate_file])
                    if event_selection == "Baseline":
                        parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016", ["Run2016*SingleElectron", "Run2016*SingleMuon", "Run2016*MET"], options.output_folder, fakerate_file])
                    if event_selection == "HadBaseline":
                        parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016MET", ["Run2016*MET"], options.output_folder, fakerate_file])
                elif options.type == "fakerate":
                    parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Summer16QCDZJets", Summer16QCDZJets, options.output_folder, fakerate_file])
                    parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016JetHT", ["Run2016*JetHT"], options.output_folder, fakerate_file])
                    parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016GHJetHT", Run2016GHJetHT, options.output_folder, fakerate_file])
                 
    region_fakeids = ["", "MVA", "EDep10"]
    #region_fakeids = [""]
    
    # run script:
    if options.index:
        print "%s / %s" (options.index, len(parameters)) 
        write_histogram_to_file(*parameters[int(options.index)])

    elif options.hadd:
        os.system("hadd -f histograms_%s.root %s/*.root" % (options.output_folder, options.output_folder))

    elif options.calculatefakerate:
        calculate_fakerate(variables["fakerate"], options.output_folder, "fakerate_%s.root" % options.output_folder, ["Summer16", "Run2016JetHT", "Run2016GHJetHT"], event_selections["fakerate"].keys(), region_fakeids)

    elif options.runall:
        os.system("%s --folder %s --type fakerate --runmode multi" % (this_scripts_name, options.output_folder) )
        os.system("%s --folder %s --type fakerate --calculatefakerate" % (this_scripts_name, options.output_folder) )
        os.system("%s --folder %s --type analysis --runmode multi" % (this_scripts_name, options.output_folder) )
        os.system("%s --folder %s --hadd" % (this_scripts_name, options.output_folder) )

        # plot validation in data and MC:
        for region_fakeid in region_fakeids:
            os.system("./plot_validation.py --histograms histograms_%s.root --regionfakeid '%s'" % (options.output_folder, region_fakeid) )
        
    else:
        
        commands = []      
        chunks_of_parameters = chunks(range(len(parameters)), int(options.plots_per_job))
        for chunks_of_parameter in chunks_of_parameters:
            subcommand = ""
            for param_index in chunks_of_parameter:
                subcommand += "%s --index %s --folder %s --type %s; " % (this_scripts_name, param_index, options.output_folder, options.type)
            commands.append(subcommand)

        GridEngineTools.runParallel(commands, options.runmode, "%s.condor" % options.output_folder, confirm=True)

