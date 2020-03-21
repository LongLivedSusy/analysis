#!/bin/env python
from __future__ import division
import __main__ as main
from ROOT import *
import plotting
import collections
import glob
import os
from optparse import OptionParser
import GridEngineTools
import time

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

binnings = {}
binnings["LepMT"] = [16, 0, 160]
binnings["leptons_mt"] = binnings["LepMT"]
binnings["leadinglepton_mt"] = binnings["LepMT"]
binnings["InvMass"] = [50, 0, 200]
binnings["tracks_invmass"] = binnings["InvMass"]
binnings["Ht"] = [35 , 0, 700]
binnings["HT"] = binnings["Ht"]
binnings["Met"] = [35 , 0, 700]
binnings["MET"] = binnings["Met"]
binnings["Mht"] = [35 , 0, 700]
binnings["MHT"] = binnings["Mht"]
binnings["DeDxAverage"] = [60, 0, 6]
binnings["tracks_massfromdeDxPixel"] = binnings["DeDxAverage"]
binnings["DeDxAverageCorrected"] = binnings["DeDxAverage"]
binnings["tracks_deDxHarmonic2pixel"] = binnings["DeDxAverage"]
binnings["tracks_deDxHarmonic2pixelCorrected"] = binnings["DeDxAverage"]
binnings["BinNumber"] = [ 88, 1, 89]
binnings["region"] = binnings["BinNumber"]
binnings["n_tags"] = [ 3, 0, 3]
binnings["n_goodjets"] = [ 10, 0, 10]
binnings["n_btags"] = binnings["n_goodjets"]
binnings["n_goodelectrons"] = [ 5, 0, 5]
binnings["n_goodmuons"] = [ 5, 0, 5]
binnings["MinDeltaPhiMhtJets"] = [ 16, 0, 3.2]
binnings["BTags"] = [ 4, 0, 4]
binnings["Track1MassFromDedx"] = [ 25, 0, 1000]
binnings["Log10DedxMass"] = [10, 0, 5]
binnings["regionCorrected"] = [100, 0, 100]
binnings["regionCorrected_sideband"] = binnings["regionCorrected"]

#binnings = {
#               "tracks_pt": [20, 0, 1000],
#               "HT": [10, 0, 1000],
#               "MHT": [10, 0, 1000],
#               "n_allvertices": [25, 0, 50],
#               "n_goodjets": [20, 0, 20],
#               "n_btags": [10, 0, 10],
#               "MinDeltaPhiMhtJets": [100, 0, 5],
#               #"tracks_eta": [12, -3, 3],
#               #"tracks_phi": [16, -4, 4],
#               #"HT:n_allvertices": ["variable", [0,20,40,1000], [0,200,400,1000]],
#               "HT:n_allvertices": [10, 0, 50, 10, 0, 1000],
#            }

dEdxSidebandLow = 1.6
dEdxLow = 2.1
dEdxMid = 4.0

# construct all histograms:
histos = collections.OrderedDict()
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
        
    for category in ["short", "long"]:
        histos["_sr%s_%s" % (dedx, category)] = [" && tracks_SR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), ""]
        histos["_srgenfake%s_%s" % (dedx, category)] = [" && tracks_SR_%s==1 && tracks_fake==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), ""]
        histos["_srgenprompt%s_%s" % (dedx, category)] = [" && tracks_SR_%s==1 && tracks_fake==0 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), ""]
        histos["_fakecr%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), ""]
        histos["_fakeprediction%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), "fakerate_HT_n_allvertices_FakeRateDet_fakerate_%s" % category]

        # added iso cut on FR CR:
        histos["_fakecrIso%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_trkRelIso<0.01 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), ""]
        histos["_fakepredictionIso%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_trkRelIso<0.01 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), "fakerate_HT_n_allvertices_FakeRateDet_fakerateIso_%s" % category]

        # added iso cut on FR CR and cut on MVA:
        histos["_fakecrIsoMVA%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_trkRelIso<0.01 && tracks_mva_loose>-0.2 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), ""]
        histos["_fakepredictionIsoMVA%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_trkRelIso<0.01 && tracks_mva_loose>-0.2 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), "fakerate_HT_n_allvertices_FakeRateDet_fakerateIso_%s" % category]

        ## other FRs:
        #histos["_fakeprediction_HT%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), "fakerate_HT_FakeRateDet_fakerate_%s" % category]
        #histos["_fakeprediction_n_allvertices%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), "fakerate_n_allvertices_FakeRateDet_fakerate_%s" % category]
        #histos["_fakeprediction_n_goodjets%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), "fakerate_n_goodjets_FakeRateDet_fakerate_%s" % category]
        #histos["_fakeprediction_MinDeltaPhiMhtJets%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), "fakerate_MinDeltaPhiMhtJets_FakeRateDet_fakerate_%s" % category]
    
    histos["_promptEl%s" % dedx] = [" && (tracks_SR_short+tracks_SR_long)==0 && n_goodelectrons==1 && n_goodmuons==0 && leptons_dedx>%s && leptons_dedx<%s" % (lower, upper), ""]
    #histos["_promptMu%s" % dedx] = [" && (tracks_SR_short+tracks_SR_long)==0 && n_goodelectrons==0 && n_goodmuons==1 && leptons_dedx>%s && leptons_dedx<%s" % (lower, upper), ""]


def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]


def write_histogram_to_file(variable, cuts, scaling, label, h_suffix, folder, globstrings, output_root_file):

    h_name = variable + "_" + label + h_suffix
    h_name = h_name.replace(":", "_")

    histo = False
    for globstring in globstrings:
        input_files = glob.glob(folder + "/" + globstring + "*.root")
        if len(input_files) > 0:
            print h_name, input_files
            if not ":" in variable:
                current_histo = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cuts, scaling=scaling, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2])
            else:
                current_histo = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cuts, scaling=scaling, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2], nBinsY=binnings[variable][3], ymin=binnings[variable][4], ymax=binnings[variable][5])

        if not histo:
            histo = current_histo.Clone()
            histo.SetDirectory(0)
        else:
            histo.Add(current_histo.Clone())
    
    fout = TFile(output_root_file, "recreate")
    histo.SetName(h_name)
    histo.SetTitle(h_name)
    histo.Write()
    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index")
    parser.add_option("--plots_per_job", dest = "plots_per_job", default = 4)
    parser.add_option("--folder", dest = "output_folder", default = "ddbg")
    parser.add_option("--hadd", dest = "hadd", action = "store_true")
    (options, args) = parser.parse_args()
    
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/tools/skim_06_onlytagged"
   
    event_selections = {
                "Baseline":               "(n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0 && MHT>150",
                "BaselineNoLeptons":      "n_goodleptons==0 && MHT>150",
                "BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110 && leadinglepton_mt>90",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leadinglepton_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<70",
                "FakeRateDet":            "n_goodleptons==0 && MHT<150",
                      }

    #regions = ["SElValidationMT", "SElValidationZLL", "SMuValidationMT", "SMuValidationZLL", "BaselineJetsNoLeptons", "BaselineNoLeptons", "SElBaseline", "SMuBaseline", "HadBaseline", "BaselineElectrons", "BaselineMuons"]
    #variables = ["leadinglepton_mt", "tracks_invmass", "HT", "MHT", "tracks_deDxHarmonic2pixel", "tracks_deDxHarmonic2pixelCorrected", "n_goodjets", "n_btags", "MinDeltaPhiMhtJets", "regionCorrected", "regionCorrected_sideband"]
    variables = ["leadinglepton_mt", "tracks_invmass", "HT", "MHT", "tracks_deDxHarmonic2pixelCorrected", "n_goodjets", "n_btags", "regionCorrected", "regionCorrected_sideband", "FakeRateDet"]
    regions = ["SElValidationMT", "SMuValidationMT", "BaselineJetsNoLeptons", "SElBaseline", "SMuBaseline", "HadBaseline", "BaselineElectrons", "BaselineMuons"]
    #variables = ["leadinglepton_mt", "tracks_invmass", "HT", "MHT"]

    ##regions = ["SElValidationMT", "SMuValidationMT"]
    #variables = ["leadinglepton_mt"]


    #variables = [
    #             "tracks_pt",
    #             "HT",
    #             "MHT",
    #             "n_goodjets",
    #             "n_allvertices",
    #             "n_btags",
    #             "MinDeltaPhiMhtJets",
    #             "HT:n_allvertices",
    #             #"tracks_eta:tracks_phi",
    #            ]
    
    os.system("mkdir -p %s" % options.output_folder)
    output_root_file = "%s/ddbg_%s.root" % (options.output_folder, options.index)

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
                "Summer16.TT_TuneCUETP8M2T4",
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

    Summer16DY = [
                "Summer16.DYJetsToLL_M-50_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1",
                "Summer16.DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1",
                ]

    parameters = []
    for region in regions:
        for variable in variables:
            for h_suffix in histos:

                cuts = histos[h_suffix][0]
                scaling = histos[h_suffix][1]

                parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16", h_suffix, folder, Summer16, output_root_file])
                if "Baseline" in region:
                    parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16QCDZJets", h_suffix, folder, Summer16QCDZJets, output_root_file])
                    #parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16DY", h_suffix, folder, Summer16DY, output_root_file])
                    if not "genfake" in h_suffix and not "genprompt" in h_suffix:
                        parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016MET", h_suffix, folder, ["Run2016*MET"], output_root_file])
                elif "SEl" in region or "SMu" in region:
                    if not "genfake" in h_suffix and not "genprompt" in h_suffix:
                        parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016SingleElectron", h_suffix, folder, ["Run2016*SingleElectron"], output_root_file])
                        parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016SingleMuon", h_suffix, folder, ["Run2016*SingleMuon"], output_root_file])
                elif region == "FakeRateDet":
                    parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16", h_suffix, folder, Summer16, output_root_file])

                    selected_datasets = ["Run2016", "Run2017", "Run2018", "Run2016B", "Run2016C", "Run2016D", "Run2016E", "Run2016F", "Run2016G", "Run2016H", "Run2017B", "Run2017C", "Run2017D", "Run2017E", "Run2017F", "Run2018A", "Run2018B", "Run2018C", "Run2018D"]
                    for selected_dataset in selected_datasets:
                        parameters.append([variable, event_selections[region] + cuts, scaling, region + "_%sJetHT" % selected_dataset, h_suffix, folder, ["%s*JetHT" % selected_dataset], output_root_file])
                    
    # run script:
    if options.index:
        if not os.path.exists(output_root_file):
            write_histogram_to_file(*parameters[int(options.index)])
        else:
            print "Already done"

    elif options.hadd:
        os.system("hadd -f %s.root %s/ddbg_*.root" % (options.output_folder, options.output_folder))

    else:
        this_scripts_name = main.__file__
        
        commands = []      
        chunks_of_parameters = chunks(range(len(parameters)), int(options.plots_per_job))
        for chunks_of_parameter in chunks_of_parameters:
            subcommand = ""
            for param_index in chunks_of_parameter:
                subcommand += "%s --index %s --folder %s; " % (this_scripts_name, param_index, options.output_folder)
            commands.append(subcommand)

        #GridEngineTools.runParallel(commands, "grid", "%s.condor" % options.output_folder, use_more_time=15000)
        #time.sleep(10)
        #GridEngineTools.runParallel(commands, "grid", "%s.condor" % options.output_folder, confirm=True)
        print "jobs:", len(commands)
        GridEngineTools.runParallel(commands, "grid", "%s.condor" % options.output_folder, confirm=True)

