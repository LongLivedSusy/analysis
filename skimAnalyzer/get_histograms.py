#!/bin/env python
from __future__ import division
import __main__ as main
import GridEngineTools
from ROOT import *
import plotting
import collections
import glob
import commands
import os
from optparse import OptionParser

def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]


def fakerate_rebin(histo, variable, category):

    if variable == "HT_n_allvertices":
        histo = histo.RebinX(3)
        histo = histo.RebinY(3)
    elif variable == "n_allvertices":
        histo = histo.Rebin(5)
    elif variable == "n_goodjets":
        histo = histo.Rebin(2)
    elif variable == "MinDeltaPhiMhtJets":
        histo = histo.Rebin(2)
    elif variable == "tracks_pt":
        histo = histo.Rebin(2)

    return histo
    

def calculate_fakerate(variables, folder, output_file, datasets, regions):
        
    haddstring = "hadd -fk %s/fakerate_numdenom.root " % folder
    for region in regions:
        haddstring += folder + "/*" + region + "*root "
    os.system("hadd -fk %s/fakerate_numdenom.root %s/*QCDLowMHT*root %s/*Dilepton*root" % (folder, folder, folder))
    os.system(haddstring)
    os.system("rm %s" % output_file)

    for dataset in datasets:
        for variable in variables:
            variable = variable.replace(":", "_")
            for region in regions:
                h_numerator_added = 0
                h_denom_added = 0
                for category in ["short", "long", ""]:                

                    dedx = ""
                    fin = TFile("%s/fakerate_numdenom.root" % folder, "read")       
                                                                                   
                    if category != "":
                        numerator = fin.Get("%s_%s_%s_sr%s_%s" % (dataset, variable, region, dedx, category))
                        numerator.SetDirectory(0)
                        numerator = fakerate_rebin(numerator, variable, category)
                        
                        denominator = fin.Get("%s_%s_%s_fakecr%s_%s" % (dataset, variable, region, dedx, category))
                        denominator.SetDirectory(0)
                        denominator = fakerate_rebin(denominator, variable, category)
                        
                    else:
                        numerator = h_numerator_added
                        denominator = h_denom_added
                    
                    if category != "":
                        if h_numerator_added == 0:
                            h_numerator_added = numerator.Clone()
                            h_numerator_added.SetDirectory(0)
                            h_numerator_added.SetName(h_numerator_added.GetName().replace("_long", "").replace("_short", ""))
                            h_numerator_added.SetTitle(h_numerator_added.GetTitle().replace("_long", "").replace("_short", ""))
                        else:
                            h_numerator_added.Add(numerator)
                        if h_denom_added == 0:
                            h_denom_added = denominator.Clone()
                            h_denom_added.SetDirectory(0)
                            h_denom_added.SetName(h_denom_added.GetName().replace("_long", "").replace("_short", ""))
                            h_denom_added.SetTitle(h_denom_added.GetTitle().replace("_long", "").replace("_short", ""))
                        else:
                            h_denom_added.Add(denominator)
                    
                    fin.Close()
                    
                    fakerate = numerator.Clone()
                    fakerate.Divide(denominator)
                    fakerate.SetName(fakerate.GetName().replace("_sr", "_fakerate").replace("JetHT", ""))
                    fakerate.SetTitle(fakerate.GetTitle().replace("_sr", "_fakerate").replace("JetHT", ""))
                    
                    fout = TFile(output_file, "update")
                    fakerate.Write()                        
                    fout.Close()


def write_histogram_to_file(variable, binnings, cuts, scaling, h_suffix, folder, label, globstrings, output_folder, fakerate_file, overwrite):

    h_name = label + "_" + variable + "_" + h_suffix
    h_name = h_name.replace(":", "_")

    #status, out = commands.getstatusoutput("grep '%s.root' %s/files" % (h_name, output_folder))
    #if status != 0:
    if not overwrite:
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
            else:
                print "Empty inputfiles:", input_files, globstrings
        
            if not histo:
                histo = current_histo.Clone()
                histo.SetDirectory(0)
            else:
                histo.Add(current_histo.Clone())
    
    else:
                
        fin = TFile(fakerate_file, "open")
        if "Run2016" in label:
            h_fakerate = fin.Get("Run2016_" + scaling.replace(":", "_").replace("-", "_"))
        elif "Run2017" in label:
            h_fakerate = fin.Get("Run2017_" + scaling.replace(":", "_").replace("-", "_"))
        elif "Run2018" in label:
            h_fakerate = fin.Get("Run2018_" + scaling.replace(":", "_").replace("-", "_"))
        elif "Summer16QCDZJets" in label:
            h_fakerate = fin.Get("Summer16_" + scaling.replace(":", "_").replace("-", "_"))
        elif "Fall17QCDZJets" in label:
            h_fakerate = fin.Get("Fall17_" + scaling.replace(":", "_").replace("-", "_"))
        else:
            h_fakerate = fin.Get(label + "_" + scaling.replace(":", "_").replace("-", "_"))
        h_fakerate.SetDirectory(0)
        fin.Close()

        # evaluate 2D HT-PU fakerate map:

        if ":" in scaling.split("-")[0]:
            
            xvariable = scaling.split("-")[0].split(":")[0]
            yvariable = scaling.split("-")[0].split(":")[1]

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
                
                mycuts = cuts + " && %s>=%s && %s<%s && %s>=%s && %s<%s" % (yvariable, ibin[0], yvariable, ibin[1], xvariable, ibin[2], xvariable, ibin[3])
                mycuts = mycuts.replace(" && %s<900.0" % xvariable, "")
                mycuts = mycuts.replace(" && %s<45.0" % yvariable, "")
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
                        
        else:
                    
            xvariable = scaling.split("-")[0]
            
            bins = []
            for ibinx in range(1,h_fakerate.GetXaxis().GetNbins()+1):
                value = h_fakerate.GetBinContent(ibinx)
                x_low = h_fakerate.GetXaxis().GetBinLowEdge(ibinx)
                x_high = x_low + h_fakerate.GetXaxis().GetBinWidth(ibinx)
                bins.append( [x_low, x_high, value] )
                            
            histo = False
            for ibin in bins:
                
                mycuts = cuts + " && %s>=%s && %s<%s" % (xvariable, ibin[0], xvariable, ibin[1])
                scalingfactor = ibin[2]
                                
                for globstring in globstrings:
                    input_files = glob.glob(folder + "/" + globstring + "*.root")
                    if len(input_files) > 0:
                        current_histo = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=mycuts, scaling=scalingfactor, nBinsX=binnings[0], xmin=binnings[1], xmax=binnings[2])
                
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
    parser.add_option("--overwrite", dest = "overwrite", action = "store_true")
    parser.add_option("--calculatefakerate", dest = "calculatefakerate", action = "store_true")
    (options, args) = parser.parse_args()
    
    this_scripts_name = main.__file__

    gStyle.SetOptStat(0)
    TH1D.SetDefaultSumw2()
        
    binnings = {}
    binnings["analysis"] = {}
    binnings["analysis"]["LepMT"] = [16, 0, 160]
    binnings["analysis"]["leptons_mt"] = binnings["analysis"]["LepMT"]
    binnings["analysis"]["leadinglepton_mt"] = binnings["analysis"]["LepMT"]
    binnings["analysis"]["InvMass"] = [20, 0, 200]
    #binnings["analysis"]["InvMass"] = [50, 0, 200]
    binnings["analysis"]["tracks_invmass"] = binnings["analysis"]["InvMass"]
    #binnings["analysis"]["Ht"] = [35 , 0, 700]
    #binnings["analysis"]["Ht"] = [7 , 0, 700]
    binnings["analysis"]["Ht"] = [10, 0, 1000]
    binnings["analysis"]["HT"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["Met"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["MET"] = binnings["analysis"]["Met"]
    binnings["analysis"]["Mht"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["MHT"] = binnings["analysis"]["Mht"]
    binnings["analysis"]["tracks_pt"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["leadinglepton_pt"] = binnings["analysis"]["Ht"]
    binnings["analysis"]["leadinglepton_eta"] = [15, 0, 3]
    binnings["analysis"]["tracks_eta"] = [15, 0, 3]
    binnings["analysis"]["tracks_dxyVtx"] = [20, 0, 0.1]
    #binnings["analysis"]["DeDxAverage"] = [60, 0, 6]
    binnings["analysis"]["DeDxAverage"] = [7, 0, 7]
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
    binnings["analysis"]["tracks_is_pixel_track"] = [ 2, 0, 2]
    binnings["analysis"]["Track1MassFromDedx"] = [ 25, 0, 1000]
    binnings["analysis"]["Log10DedxMass"] = [10, 0, 5]
    binnings["analysis"]["regionCorrected"] = [54,1,55]
    binnings["analysis"]["regionCorrected_sideband"] = binnings["analysis"]["regionCorrected"]
    binnings["analysis"]["region"] = binnings["analysis"]["regionCorrected"]
    binnings["analysis"]["tracks_matchedCaloEnergy"] = [25, 0, 50]
    binnings["analysis"]["tracks_trkRelIso"] = [20, 0, 0.2]

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
    binnings["fakerate"]["tracks_is_pixel_track"] = [ 2, 0, 2]
    
    dEdxSidebandLow = 1.6
    dEdxLow = 2.0
    dEdxMid = 4.0

    # construct all histograms:
    zones = collections.OrderedDict()
    #for dedx in ["", "_SidebandDeDx", "_MidDeDx", "_HighDeDx"]:
    for dedx in ["", "_MidHighDeDx", "_MidDeDx", "_HighDeDx"]:
        if dedx == "_SidebandDeDx":
            lower = dEdxSidebandLow; upper = dEdxLow
        elif dedx == "_MidDeDx":
            lower = dEdxLow; upper = dEdxMid
        elif dedx == "_MidHighDeDx":
            lower = dEdxLow; upper = 9999
        elif dedx == "_HighDeDx":
            lower = dEdxMid; upper = 9999
        elif dedx == "_MidHighDeDx":
            lower = dEdxLow; upper = 9999
        elif dedx == "":
            lower = 0; upper = 9999
        
        tags = collections.OrderedDict()
        tags["SR_short"] = "tracks_mva_loose>(tracks_dxyVtx*(0.65/0.01) - 0.5) && tracks_trkRelIso<0.01"
        tags["SR_long"] = "tracks_mva_loose>(tracks_dxyVtx*(0.7/0.01) - 0.05) && tracks_trkRelIso<0.01"
        tags["CR_short"] = "tracks_dxyVtx>0.02" 
        tags["CR_long"] = "tracks_dxyVtx>0.02"
        
        for is_pixel_track, category in enumerate(["long", "short"]):

            # apply cuts to all regions:
            morecuts = " && tracks_is_pixel_track==%s && tracks_matchedCaloEnergy<10 && tracks_deDxHarmonic2pixelCorrected>%s && tracks_deDxHarmonic2pixelCorrected<%s" % (is_pixel_track, lower, upper)
            
            zones["sr%s_%s" % (dedx, category)] = [" && %s %s" % (tags["SR_" + category], morecuts), ""]
            zones["srgenfake%s_%s" % (dedx, category)] = [" && %s && tracks_fake==1 %s" % (tags["SR_" + category], morecuts), ""]
            zones["srgenprompt%s_%s" % (dedx, category)] = [" && %s && tracks_fake==0 %s" % (tags["SR_" + category], morecuts), ""]
            
            zones["fakecr%s_%s" % (dedx, category)] = [" && %s %s" % (tags["CR_" + category], morecuts), ""]
            zones["fakeprediction-QCDLowMHT-%s_%s" % (dedx, category)] = [" && %s %s" % (tags["CR_" + category], morecuts), "HT:n_allvertices-QCDLowMHT_fakerate_%s" % (category)]
            zones["fakeprediction-QCDLowMHTHT-%s_%s" % (dedx, category)] = [" && %s %s" % (tags["CR_" + category], morecuts), "HT-QCDLowMHT_fakerate_%s" % (category)]
            zones["fakeprediction-QCDLowMHTSimple-%s_%s" % (dedx, category)] = [" && %s %s" % (tags["CR_" + category], morecuts), "tracks_is_pixel_track-QCDLowMHT_fakerate_%s" % (category)]
            #zones["fakeprediction-QCDLowMHTHT-%s_%s" % (dedx, category)] = [" && %s %s" % (tags["CR_" + category], morecuts), "HT-QCDLowMHT_fakerate_%s" % (category)]
                        
            zones["PromptEl%s" % (dedx)] = [" && (tracks_SR_short+tracks_SR_long)==0 && tracks_deDxHarmonic2pixelCorrected>%s && tracks_deDxHarmonic2pixelCorrected<%s" % (lower, upper), ""]

    # remove superfluous zone cuts:
    for zone_label in zones:
        for delstring in ["&& tracks_deDxHarmonic2pixelCorrected<9999", "&& tracks_deDxHarmonic2pixelCorrected>0"]:
            if delstring in zones[zone_label][0]:
                zones[zone_label][0] = zones[zone_label][0].replace(delstring, "")
   
    event_selections = {}
    event_selections["analysis"] = collections.OrderedDict()
    event_selections["analysis"]["Baseline"] =          "(n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))"
    event_selections["analysis"]["HadBaseline"] =       "HT>150 && MHT>150 && n_goodjets>=1 && n_goodleptons==0"
    event_selections["analysis"]["SMuBaseline"] =       "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leadinglepton_mt>90"
    event_selections["analysis"]["SMuValidationZLL"] =  "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90"
    event_selections["analysis"]["SMuValidationMT"] =    "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<70"
    event_selections["analysis"]["QCDLowMHT"] =          "n_goodleptons==0 && MHT<150"
    event_selections["analysis"]["SElBaseline"] =       "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90"
    event_selections["analysis"]["SElValidationZLL"] =  "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90"
    event_selections["analysis"]["SElValidationMT"] =   "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leadinglepton_mt<70"
    event_selections["analysis"]["PromptEl"] =          "n_goodelectrons==1 && n_goodmuons==0"
    event_selections["analysis"]["PromptDiEl"] =        "n_goodelectrons==2 && n_goodmuons==0 && dilepton_invmass>71 && dilepton_invmass<111"

    event_selections["fakerate"] = collections.OrderedDict()
    event_selections["fakerate"]["QCDLowMHT"] =          "n_goodleptons==0 && MHT<150"
    #event_selections["fakerate"]["Dilepton"] =           "dilepton_invmass>60 && dilepton_invmass<120"
    #event_selections["fakerate"]["DileptonLowMHT"] =     "dilepton_invmass>70 && dilepton_invmass<110 && MHT<150"
    #event_selections["fakerate"]["DileptonEl"] =         "dilepton_leptontype==11 && dilepton_invmass>70 && dilepton_invmass<110"
    #event_selections["fakerate"]["DileptonMu"] =         "dilepton_leptontype==13 && dilepton_invmass>70 && dilepton_invmass<110"
        
    variables = {}
    variables["analysis"] = [
                              "HT",
                              "MHT",
                              "n_goodjets",
                              "n_btags",
                              "regionCorrected",
                              "regionCorrected_sideband",
                              "leadinglepton_mt",
                              "tracks_invmass",
                              "tracks_is_pixel_track",
                              "tracks_pt",
                              "tracks_eta",
                              "tracks_deDxHarmonic2pixelCorrected",
                              "tracks_matchedCaloEnergy",
                              "tracks_trkRelIso",
                            ]
    variables["fakerate"] = [
                              "tracks_pt",
                              "tracks_is_pixel_track",
                              "HT",
                              "MHT",
                              "n_goodjets",
                              "n_allvertices",
                              "n_btags",
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
                
    Fall17 = [
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",
                #"RunIIFall17MiniAODv2.TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
                #"RunIIFall17MiniAODv2.TTGamma_Dilept_TuneCP5_PSweights_13TeV_madgraph_pythia8",
                #"RunIIFall17MiniAODv2.TTGamma_SingleLeptFromT_TuneCP5_PSweights_13TeV_madgraph_pythia8",
                #"RunIIFall17MiniAODv2.TTGamma_SingleLeptFromTbar_TuneCP5_PSweights_13TeV_madgraph_pythia8",
                #"RunIIFall17MiniAODv2.TTHH_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.TTJets_DiLept_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.TTJets_SingleLeptFromT_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.TTJets_SingleLeptFromTbar_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.TTJets_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8",
                #"RunIIFall17MiniAODv2.TTTW_TuneCP5_13TeV-madgraph-pythia8",
                #"RunIIFall17MiniAODv2.TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8",
                #"RunIIFall17MiniAODv2.TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8",
                #"RunIIFall17MiniAODv2.TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8",
                #"RunIIFall17MiniAODv2.TTWZ_TuneCP5_13TeV-madgraph-pythia8",
                #"RunIIFall17MiniAODv2.TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
                #"RunIIFall17MiniAODv2.TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8",
                #"RunIIFall17MiniAODv2.TTZZ_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",
                "RunIIFall17MiniAODv2.WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
                #"RunIIFall17MiniAODv2.WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_v2",
                #"RunIIFall17MiniAODv2.WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
                "RunIIFall17MiniAODv2.WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
                "RunIIFall17MiniAODv2.WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8",
                "RunIIFall17MiniAODv2.ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8",
                ]
                
    Fall17QCDZJets = [
                "RunIIFall17MiniAODv2.QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-100To200_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-1200To2500_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-200To400_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-400To600_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-600To800_13TeV-madgraph",
                "RunIIFall17MiniAODv2.ZJetsToNuNu_HT-800To1200_13TeV-madgraph",
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

    Run2016GHSingleElectron = [
                "Run2016G*SingleElectron",
                "Run2016H*SingleElectron",
                ]

    Run2016GHSingleMuon = [
                "Run2016G*SingleMuon",
                "Run2016H*SingleMuon",
                ]
                
    do_phase0 = True 
    do_phase1 = True

    parameters = []
    for variable in variables[options.type]:            
        for event_selection in event_selections[options.type]:
            
            if "Prompt" in event_selection:
                folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/skim_11_dilepton_merged"
                do_phase1 = False
            else:
                folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/skim_09_cand_merged"
                do_phase1 = True
                
                        
            for zone in zones:

                h_suffix = event_selection + "_" + zone

                cuts = event_selections[options.type][event_selection] + zones[zone][0]
                scaling = zones[zone][1]
                                
                # don't do any scaling for fakerate determination:
                if scaling != "" and options.type == "fakerate":
                    continue
                if "DeDx" in h_suffix and options.type == "fakerate":
                    continue
                    
                fakerate_file = "%s/fakerate.root" % options.output_folder

                if do_phase0: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Summer16", Summer16, options.output_folder, fakerate_file])
                if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Fall17", Fall17, options.output_folder, fakerate_file])
                
                if options.type == "analysis":
                    if "SEl" in h_suffix and not "genfake" in h_suffix and not "genprompt" in h_suffix:
                        if do_phase0: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016SingleElectron", ["Run2016*SingleElectron"], options.output_folder, fakerate_file])
                        if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2017SingleElectron", ["Run2017*SingleElectron"], options.output_folder, fakerate_file])
                        if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2018SingleElectron", ["Run2018*EGamma"], options.output_folder, fakerate_file])
                    if "SMu" in h_suffix and not "genfake" in h_suffix and not "genprompt" in h_suffix:
                        if do_phase0: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016SingleMuon", ["Run2016*SingleMuon"], options.output_folder, fakerate_file])
                        if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2017SingleMuon", ["Run2017*SingleMuon"], options.output_folder, fakerate_file])
                        if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2018SingleMuon", ["Run2018*SingleMuon"], options.output_folder, fakerate_file])
                    if event_selection == "Baseline":
                        if do_phase0: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Summer16QCDZJets", Summer16QCDZJets, options.output_folder, fakerate_file])
                        if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Fall17QCDZJets", Fall17QCDZJets, options.output_folder, fakerate_file])
                        if "region" in variable:
                            if do_phase0: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016", ["Run2016*SingleElectron", "Run2016*SingleMuon", "Run2016*MET"], options.output_folder, fakerate_file])
                            if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2017", ["Run2017*SingleElectron", "Run2017*SingleMuon", "Run2017*MET"], options.output_folder, fakerate_file])
                            if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2018", ["Run2018*EGamma", "Run2018*SingleMuon", "Run2018*MET"], options.output_folder, fakerate_file])
                    if event_selection == "HadBaseline":
                        if do_phase0: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016MET", ["Run2016*MET"], options.output_folder, fakerate_file])
                        if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2017MET", ["Run2017*MET"], options.output_folder, fakerate_file])
                        if do_phase1: parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2018MET", ["Run2018*MET"], options.output_folder, fakerate_file])
                elif options.type == "fakerate":
                    # due to the 2016 trigger inefficiency issue, calculate FR just with Runs G and H...
                    if do_phase0:
                        
                        if "Dilepton" in event_selection:
                            parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016SingleElectron", Run2016GHSingleElectron, options.output_folder, fakerate_file])
                            parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016SingleMuon", Run2016GHSingleMuon, options.output_folder, fakerate_file])
                            parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016AllSingleElectron", ["Run2016*SingleElectron"], options.output_folder, fakerate_file])
                            parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016AllSingleMuon", ["Run2016*SingleMuon"], options.output_folder, fakerate_file])
                        else:
                            parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016JetHT", Run2016GHJetHT, options.output_folder, fakerate_file])
                            parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2016AllJetHT", ["Run2016*JetHT"], options.output_folder, fakerate_file])
                    if do_phase1:
                        parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2017JetHT", ["Run2017*JetHT"], options.output_folder, fakerate_file])
                        parameters.append([variable, binnings[options.type][variable], cuts, scaling, h_suffix, folder, "Run2018JetHT", ["Run2018*JetHT"], options.output_folder, fakerate_file])
    
    # run script:
    if options.index:
        print "%s / %s" % (options.index, len(parameters)) 
        try:
            parameters[int(options.index)].append(options.overwrite)
            write_histogram_to_file(*parameters[int(options.index)])
        except Exception as e:
            print "Failed job"
            erroutput = options.index + "\n" + str(e) + "\n" + str(parameters[int(options.index)]) + "\n======\n"        
            print erroutput
            os.system("touch %s/failedfiles" % options.output_folder)
            with open(options.output_folder + "/failedfiles", "a") as fout:
                fout.write(erroutput)
            
    elif options.hadd:
        os.system("hadd -fk %s/histograms_Run2016.root %s/Run2016*.root" % (options.output_folder, options.output_folder))
        os.system("hadd -fk %s/histograms_Run2017.root %s/Run2017*.root" % (options.output_folder, options.output_folder))
        os.system("hadd -fk %s/histograms_Run2018.root %s/Run2018*.root" % (options.output_folder, options.output_folder))
        os.system("hadd -fk %s/histograms_Summer16.root %s/Summer16*.root " % (options.output_folder, options.output_folder))
        os.system("hadd -fk %s/histograms_Fall17.root %s/Fall17*.root" % (options.output_folder, options.output_folder))
        os.system("hadd -fk %s/histograms.root %s/histograms_*root" % (options.output_folder, options.output_folder))

    elif options.calculatefakerate:
        datasets = [
                    "Summer16",
                    "Run2016AllJetHT",
                    "Run2016JetHT",
                    ]
                    
        if do_phase1:
            datasets += [
                        "Fall17",
                        "Run2017JetHT",
                        "Run2018JetHT",
                        ]
                        
        calculate_fakerate(variables["fakerate"], options.output_folder, "%s/fakerate.root" % options.output_folder, datasets, event_selections["fakerate"].keys())

    elif options.runall:
        
        if options.overwrite:
            overwritetext = "--overwrite"
        else:
            overwritetext = ""
        
        #os.system("%s --folder %s --type fakerate --runmode multi %s" % (this_scripts_name, options.output_folder, overwritetext) )
        #os.system("%s --folder %s --type fakerate --calculatefakerate" % (this_scripts_name, options.output_folder) )
        os.system("%s --folder %s --type analysis --runmode multi %s" % (this_scripts_name, options.output_folder, overwritetext) )
        os.system("%s --folder %s --hadd" % (this_scripts_name, options.output_folder,) )
        #os.system("./plot_validation.py --histograms histograms_%s.root" % (options.output_folder) )
        
    else:
        
        commands = []      
        chunks_of_parameters = chunks(range(len(parameters)), int(options.plots_per_job))
        for chunks_of_parameter in chunks_of_parameters:
            subcommand = ""
            for param_index in chunks_of_parameter:
                if options.overwrite:
                    overwritetext = "--overwrite"
                else:
                    overwritetext = ""
                subcommand += "%s --index %s --folder %s --type %s %s; " % (this_scripts_name, param_index, options.output_folder, options.type, overwritetext)
                
            commands.append(subcommand)
        
        os.system("cd %s; ls > filelist; cd -" % (options.output_folder))

        #commands = []      
        #for param_index in [9, 15, 2]:
        #    commands.append("%s --index %s --folder %s --type %s; " % (this_scripts_name, param_index, options.output_folder, options.type))

        GridEngineTools.runParallel(commands, options.runmode, "%s.condor" % options.output_folder, confirm=True)

