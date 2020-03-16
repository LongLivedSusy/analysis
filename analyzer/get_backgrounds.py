#!/bin/env python
from __future__ import division
from ROOT import *
import plotting
import collections
import glob
import os
from optparse import OptionParser
import GridEngineTools

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
binnings["DeDxAverageCorrected"] = [60, 0, 6]
binnings["BinNumber"] = [ 88, 1, 89]
binnings["region"] = binnings["BinNumber"]
binnings["n_tags"] = [ 3, 0, 3]
binnings["n_goodjets"] = [ 10, 0, 10]
binnings["n_goodelectrons"] = [ 5, 0, 5]
binnings["n_goodmuons"] = [ 5, 0, 5]
binnings["MinDeltaPhiMhtJets"] = [ 16, 0, 3.2]
binnings["BTags"] = [ 4, 0, 4]
binnings["Track1MassFromDedx"] = [ 25, 0, 1000]
binnings["Log10DedxMass"] = [10, 0, 5]

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
        histos["_fakeprediction%s_%s" % (dedx, category)] = [" && tracks_CR_%s==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (category, lower, upper), "fakerate_%s" % category]

    histos["_promptEl%s" % dedx] = [" && (tracks_SR_short+tracks_SR_long)==0 && n_goodelectrons==1 && n_goodmuons==0 && leptons_dedx>%s && leptons_dedx<%s" % (lower, upper), ""]
    histos["_promptMu%s" % dedx] = [" && (tracks_SR_short+tracks_SR_long)==0 && n_goodelectrons==0 && n_goodmuons==1 && leptons_dedx>%s && leptons_dedx<%s" % (lower, upper), ""]
    

def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]


def write_histogram_to_file(variable, cuts, scaling, label, h_suffix, folder, globstrings, output_root_file):

    h_name = variable + "_" + label + h_suffix

    input_files = []
    for globstring in globstrings:
       input_files += glob.glob(folder + "/" + globstring + "*.root")
    
    print h_name, input_files
    
    histo = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cuts, scaling=scaling, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2])

    fout = TFile(output_root_file, "recreate")
    histo.SetName(h_name)
    histo.SetTitle(h_name)
    histo.Write()
    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index")
    parser.add_option("--plots_per_job", dest = "plots_per_job", default = 1)
    parser.add_option("--folder", dest = "output_folder", default = "ddbg")
    parser.add_option("--hadd", dest = "hadd", action = "store_true")
    (options, args) = parser.parse_args()
    
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/tools/skim_01_merged"
   
    event_selections = {
                "Baseline":               "(n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0",
                "BaselineNoLeptons":      "n_goodleptons==0",
                "BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110 && leadinglepton_mt>90",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leadinglepton_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leadinglepton_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leadinglepton_mt<70",
                "FakeRateDetQCDJetHT":    "MHT<200",
                      }

    regions = collections.OrderedDict()
    regions["SElValidationMT"] = ["leadinglepton_mt", "tracks_invmass"]
    regions["SElValidationZLL"] = ["leadinglepton_mt", "tracks_invmass"]
    regions["SMuValidationMT"] = ["leadinglepton_mt", "tracks_invmass"]
    regions["SMuValidationZLL"] = ["leadinglepton_mt", "tracks_invmass"]
    #regions["FakeRateDetQCDJetHT"] = ["HT", "n_allvertices"]
    #regions["Baseline"] = ["leadinglepton_mt", "tracks_invmass", "HT", "MHT", "tracks_deDxHarmonic2pixel", "n_goodjets", "n_btags", "MinDeltaPhiMhtJets", "region", "region_sideband"]
    #regions["HadBaseline"] = regions["SElValidationMT"]
    #regions["SElBaseline"] = regions["SElValidationMT"]
    regions["Baseline"] = ["HT", "MHT", "tracks_deDxHarmonic2pixel", "n_goodjets", "n_btags", "MinDeltaPhiMhtJets"]
    
    os.system("mkdir -p %s" % options.output_folder)
    output_root_file = "%s/ddbg_%s.root" % (options.output_folder, options.index)
    allmc = ["Summer16.QCD", "Summer16.WJets", "Summer16.ZJets", "Summer16.TT", "Summer16.DY", "Summer16.WW", "Summer16.WZ", "Summer16.ZZ"]

    parameters = []
    for region in regions:
        for variable in regions[region]:
            for h_suffix in histos:

                cuts = histos[h_suffix][0]
                scaling = histos[h_suffix][1]

                if "FakeRateDetQCDJetHT" in region:
                    if "_fakecr" in h_suffix or "_sr" in h_suffix:
                        parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16QCD", h_suffix, folder, ["Summer16.QCD"], output_root_file])
                        parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016JetHT", h_suffix, folder, ["Run2016*JetHT"], output_root_file])
                        continue

                parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16", h_suffix, folder, allmc, output_root_file])
                parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016MET", h_suffix, folder, ["Run2016*MET"], output_root_file])
                if "Baseline" in region:
                    parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16QCDZJets", h_suffix, folder, ["Summer16.QCD", "Summer16.ZJets"], output_root_file])
                    parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16DY", h_suffix, folder, ["Summer16.DY"], output_root_file])
                if not "SMu" in region:
                    parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016SingleElectron", h_suffix, folder, ["Run2016*SingleElectron"], output_root_file])
                if not "SEl" in region:
                    parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016SingleMuon", h_suffix, folder, ["Run2016*SingleMuon"], output_root_file])

    # run script:

    if options.index:

        if not os.path.exists(output_root_file):
            write_histogram_to_file(*parameters[int(options.index)])
        else:
            print "Already done"

    elif options.hadd:
        os.system("hadd -f %s.root %s/ddbg_*.root" % (options.output_folder, options.output_folder))

    else:

        import __main__ as main
        this_scripts_name = main.__file__
        
        commands = []      
        chunks_of_parameters = chunks(range(len(parameters)), int(options.plots_per_job))
        for chunks_of_parameter in chunks_of_parameters:
            subcommand = ""
            for param_index in chunks_of_parameter:
                subcommand += "%s --index %s --folder %s; " % (this_scripts_name, param_index, options.output_folder)
            commands.append(subcommand)

        GridEngineTools.runParallel(commands, "grid", "%s.condor" % options.output_folder, use_more_time=15000)

