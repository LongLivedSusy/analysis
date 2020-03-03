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

histos = collections.OrderedDict()

# get signal region:
histos["_sr_short"] = [" && tracks_SR_short==1", ""]
histos["_sr_long"] = [" && tracks_SR_long==1", ""]
histos["_srSideband_short"] = [" && tracks_SR_short==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxSidebandLow, dEdxLow), ""]
histos["_srSideband_long"] = [" && tracks_SR_long==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxSidebandLow, dEdxLow), ""]
histos["_srMid_short"] = [" && tracks_SR_short==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxLow, dEdxMid), ""]
histos["_srMid_long"] = [" && tracks_SR_long==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxLow, dEdxMid), ""]
histos["_srMidHighDeDx_short"] = [" && tracks_SR_short==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxLow), ""]
histos["_srMidHighDeDx_long"] = [" && tracks_SR_long==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxLow), ""]
histos["_srHighDeDx_short"] = [" && tracks_SR_short==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxMid), ""]
histos["_srHighDeDx_long"] = [" && tracks_SR_long==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxMid), ""]

# get nonprompt CR and nonprompt prediction
histos["_fakecr_short"] = [" && tracks_CR_short==1", ""]
histos["_fakecr_long"] = [" && tracks_CR_long==1", ""]
histos["_fakecrSideband_short"] = [" && tracks_CR_short==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxSidebandLow, dEdxLow), ""]
histos["_fakecrSideband_long"] = [" && tracks_CR_long==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxSidebandLow, dEdxLow), ""]
histos["_fakecrMid_short"] = [" && tracks_CR_short==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxLow, dEdxMid), ""]
histos["_fakecrMid_long"] = [" && tracks_CR_long==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxLow, dEdxMid), ""]
histos["_fakecrMidHighDeDx_short"] = [" && tracks_CR_short==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxLow), ""]
histos["_fakecrMidHighDeDx_long"] = [" && tracks_CR_long==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxLow), ""]
histos["_fakecrHighDeDx_short"] = [" && tracks_CR_short==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxMid), ""]
histos["_fakecrHighDeDx_long"] = [" && tracks_CR_long==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxMid), ""]
histos["_fakeprediction_short"] = [" && tracks_CR_short==1", "fakerate_short"]
histos["_fakeprediction_long"] = [" && tracks_CR_long==1", "fakerate_long"]
histos["_fakepredictionSideband_short"] = [" && tracks_CR_short==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxSidebandLow, dEdxLow), "fakerate_short"]
histos["_fakepredictionSideband_long"] = [" && tracks_CR_long==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxSidebandLow, dEdxLow), "fakerate_long"]
histos["_fakepredictionMid_short"] = [" && tracks_CR_short==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxLow, dEdxMid), "fakerate_short"]
histos["_fakepredictionMid_long"] = [" && tracks_CR_long==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxLow, dEdxMid), "fakerate_long"]
histos["_fakepredictionMidHighDeDx_short"] = [" && tracks_CR_short==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxLow), "fakerate_short"]       # **** need to rerun before using that
histos["_fakepredictionMidHighDeDx_long"] = [" && tracks_CR_long==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxLow), "fakerate_long"]
histos["_fakepredictionHighDeDx_short"] = [" && tracks_CR_short==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxMid), "fakerate_short"]
histos["_fakepredictionHighDeDx_long"] = [" && tracks_CR_long==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxMid), "fakerate_long"]

# get prompt background ABCD histograms:
histos["_lowDeDxPromptElectron"] = [" && (tracks_SR_short+tracks_SR_long)==0 && n_goodelectrons==1 && n_goodmuons==0 && leptons_dedx>%s && leptons_dedx<%s" % (dEdxSidebandLow, dEdxLow), ""]
histos["_highDeDxPromptElectron"] = [" && (tracks_SR_short+tracks_SR_long)==0 && n_goodelectrons==1 && n_goodmuons==0 && leptons_dedx>%s" % (dEdxLow), ""]
histos["_lowDeDxDTnoLep"] = [" && (tracks_SR_short+tracks_SR_long)==1 && n_goodleptons==0 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxSidebandLow, dEdxLow), ""]
histos["_highDeDxDTnoLep"] = [" && (tracks_SR_short+tracks_SR_long)==1 && n_goodleptons==0 && tracks_deDxHarmonic2pixel>%s" % (dEdxLow), ""]
histos["_lowDeDxDT"] = [" && (tracks_SR_short+tracks_SR_long)==1 && tracks_deDxHarmonic2pixel>%s && tracks_deDxHarmonic2pixel<%s" % (dEdxSidebandLow, dEdxLow), ""]
histos["_highDeDxDT"] = [" && (tracks_SR_short+tracks_SR_long)==1 && tracks_deDxHarmonic2pixel>%s" % (dEdxMid), ""]

# get MC Truth histograms for closure
histos["_srgenfakes_short"] = [" && tracks_SR_short==1 && tracks_fake==1", ""]
histos["_srgenfakes_long"] = [" && tracks_SR_long==1 && tracks_fake==1", ""]
histos["_srgenprompt_short"] = [" && tracks_SR_short==1 && tracks_fake==0", ""]
histos["_srgenprompt_long"] = [" && tracks_SR_long==1 && tracks_fake==0", ""]


def write_histogram_to_file(variable, cuts, scaling, label, h_suffix, folder, globstrings, output_root_file):

    h_name = variable + "_" + label + h_suffix
    print h_name

    input_files = []
    for globstring in globstrings:
       input_files += glob.glob(folder + "/" + globstring + "*.root")
    
    histo = plotting.get_histogram_from_file(input_files, "Events", variable, cutstring=cuts, scaling=scaling, nBinsX=binnings[variable][0], xmin=binnings[variable][1], xmax=binnings[variable][2])

    fout = TFile(output_root_file, "recreate")
    histo.SetName(h_name)
    histo.SetTitle(h_name)
    histo.Write()
    fout.Close()


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--index", dest = "index")
    parser.add_option("--folder", dest = "output_folder", default = "ddbg")
    parser.add_option("--hadd", dest = "hadd", action = "store_true")
    (options, args) = parser.parse_args()
    
    folder = "/nfs/dust/cms/user/kutznerv/shorttrack/analysis/eventselection/tools/skim_69_merged"
   
    event_selections = {
                "Baseline":               "(n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "BaselineJetsNoLeptons":  "n_goodjets>=1 && n_goodleptons==0",
                "BaselineNoLeptons":      "n_goodleptons==0",
                "BaselineElectrons":      "n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "BaselineMuons":          "n_goodelectrons==0 && n_goodmuons>=1 && tracks_invmass>110 && leadinglepton_mt>90",
                "HadBaseline":            "HT>150 && MHT>150 && n_goodjets>=1 && (n_goodleptons==0 || (tracks_invmass>110 && leadinglepton_mt>90))",
                "SMuBaseline":            "HT>150 && n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SMuValidationZLL":       "n_goodjets>=1 && n_goodmuons>=1 && n_goodelectrons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElBaseline":            "HT>150 && n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>110 && leadinglepton_mt>90",
                "SElValidationZLL":       "n_goodjets>=1 && n_goodelectrons>=1 && n_goodmuons==0 && tracks_invmass>65 && tracks_invmass<110 && leptons_mt>90",
                "SElValidationMT":        "n_goodjets>=1 && n_goodelectrons==1 && n_goodmuons==0 && leptons_mt<70",
                "SMuValidationMT":        "n_goodjets>=1 && n_goodmuons==1 && n_goodelectrons==0 && leptons_mt<70",
                "FakeRateDetQCDJetHT":    "MHT<200",
                      }

    regions = collections.OrderedDict()
    regions["SElValidationMT"] = ["leptons_mt", "tracks_invmass", "HT", "MHT", "DeDxAverageCorrected", "n_goodjets", "n_btags", "MinDeltaPhiMhtJets", "region"]
    regions["SElValidationZLL"] = regions["SElValidationMT"]
    regions["SMuValidationMT"] = regions["SElValidationMT"]
    regions["SMuValidationZLL"] = regions["SElValidationMT"]
    #regions["FakeRateDetQCDJetHT"] = ["HT", "n_allvertices"]
    #regions["Baseline"] = regions["SElValidationMT"]
    #regions["HadBaseline"] = regions["SElValidationMT"]
    #regions["SElBaseline"] = regions["SElValidationMT"]
    
    os.system("mkdir -p %s" % options.output_folder)
    output_root_file = "%s/ddbg_%s.root" % (options.output_folder, options.index)

    parameters = []
    for region in regions:
        for variable in regions[region]:
            for h_suffix in histos:

                cuts = histos[h_suffix][0]
                scaling = histos[h_suffix][1]

                if "FakeRateDetQCDJetHT" in region:
                    if "_fakecr_" in h_suffix or "_sr_" in h_suffix:
                        parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16QCD", h_suffix, folder, ["Summer16.QCD"], output_root_file])
                        parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016JetHT", h_suffix, folder, ["Run2016*JetHT"], output_root_file])
                        continue

                parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16", h_suffix, folder, ["Summer16"], output_root_file])
                parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016MET", h_suffix, folder, ["Run2016*MET"], output_root_file])
                if "Baseline" in region:
                    parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Summer16QCDZJets", h_suffix, folder, ["Summer16.QCD", "Summer16.ZJets"], output_root_file])
                if not "SMu" in region:
                    parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016SingleElectron", h_suffix, folder, ["Run2016*SingleElectron"], output_root_file])
                if not "SEl" in region:
                    parameters.append([variable, event_selections[region] + cuts, scaling, region + "_Run2016SingleMuon", h_suffix, folder, ["Run2016*SingleMuon"], output_root_file])

    # run script:

    if options.index:
        write_histogram_to_file(*parameters[int(options.index)])

    elif options.hadd:
        os.system("hadd -f %s.root %s/ddbg_*.root" % (options.output_folder, options.output_folder))

    else:

        import __main__ as main
        this_scripts_name = main.__file__

        commands = []
        for i_parameter in range(len(parameters)):
            commands.append("%s --index %s --folder %s" % (this_scripts_name, i_parameter, options.output_folder))
        GridEngineTools.runParallel(commands, "grid", "%s.condor" % this_scripts_name.split("/")[-1].split(".")[0], use_more_time=15000)

