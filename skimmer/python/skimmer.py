#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import tmva_tools
import collections
import json

#gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

# store runs for JSON output:
runs = {}

def get_signal_region(event, MinDeltaPhiMhtJets, n_DT, is_pixel_track):
  
    NJets = len(event.Jets)
    MHT = event.MHT
    n_btags = event.BTags
    is_tracker_track = not is_pixel_track

    binnumbers = collections.OrderedDict()
    #           'Ht',             'Mht',                'NJets',            'BTags',            'NTags',            'NPix',             'NPixStrips',       'MinDPhiMhtJets'
    binnumbers[((0,float("inf")), (250,400),            (1,1),              (0,float("inf")),   (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 1
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (0,0),              (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 2
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (1,5),              (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 3
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (0,0),              (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 4
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (1,float("inf")),   (1,1),              (0,0),              (1,1),              (0.5,float("inf")))] = 5
    binnumbers[((0,float("inf")), (400,700),            (1,1),              (0,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 6
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 7
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (1,5),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 8
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 9
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (1,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 10
    binnumbers[((0,float("inf")), (700,float("inf")),   (1,1),              (0,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 11
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 12
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (1,5),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 13
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (0,0),              (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 14
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (1,float("inf")),   (1,1),              (0,0),              (1,1),              (0.3,float("inf")))] = 15
    binnumbers[((0,float("inf")), (250,400),            (1,1),              (0,float("inf")),   (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 16
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (0,0),              (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 17
    binnumbers[((0,float("inf")), (250,400),            (2,5),              (1,5),              (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 18
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (0,0),              (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 19
    binnumbers[((0,float("inf")), (250,400),            (6,float("inf")),   (1,float("inf")),   (1,1),              (1,1),              (0,0),              (0.5,float("inf")))] = 20
    binnumbers[((0,float("inf")), (400,700),            (1,1),              (0,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 21
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 22
    binnumbers[((0,float("inf")), (400,700),            (2,5),              (1,5),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 23
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 24
    binnumbers[((0,float("inf")), (400,700),            (6,float("inf")),   (1,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 25
    binnumbers[((0,float("inf")), (700,float("inf")),   (1,1),              (0,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 26
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 27
    binnumbers[((0,float("inf")), (700,float("inf")),   (2,5),              (1,5),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 28
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (0,0),              (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 29
    binnumbers[((0,float("inf")), (700,float("inf")),   (6,float("inf")),   (1,float("inf")),   (1,1),              (1,1),              (0,0),              (0.3,float("inf")))] = 30
    binnumbers[((0,float("inf")), (250,400),            (1,float("inf")),   (0,float("inf")),   (2,float("inf")),   (0,float("inf")),   (0,float("inf")),   (0.0,float("inf")))] = 31
    binnumbers[((0,float("inf")), (400,float("inf")),   (1,float("inf")),   (0,float("inf")),   (2,float("inf")),   (0,float("inf")),   (0,float("inf")),   (0.0,float("inf")))] = 32

    region = 0
    for binkey in binnumbers:
        if MHT >= binkey[1][0] and MHT <= binkey[1][1] and \
           NJets >= binkey[2][0] and NJets <= binkey[2][1] and \
           n_btags >= binkey[3][0] and n_btags <= binkey[3][1] and \
           n_DT >= binkey[4][0] and n_DT <= binkey[4][1] and \
           is_pixel_track >= binkey[5][0] and is_pixel_track <= binkey[5][1] and \
           is_tracker_track >= binkey[6][0] and is_tracker_track <= binkey[6][1] and \
           MinDeltaPhiMhtJets >= binkey[7][0] and MinDeltaPhiMhtJets <= binkey[7][1]:
            region = binnumbers[binkey]
            break

    return region


def isBaselineTrack(track, itrack, c, hMask, loose_dxy = False):
	if not abs(track.Eta())< 2.4 : return False
	if not (abs(track.Eta()) < 1.4442 or abs(track.Eta()) > 1.566): return False
	if not bool(c.tracks_trackQualityHighPurity[itrack]) : return False
	if not (c.tracks_ptError[itrack]/(track.Pt()*track.Pt()) < 10): return False
	if not loose_dxy and (not abs(c.tracks_dxyVtx[itrack]) < 0.1): return False
	if not abs(c.tracks_dzVtx[itrack]) < 0.1 : return False
	if not c.tracks_trkRelIso[itrack] < 0.2: return False
	if not (c.tracks_trackerLayersWithMeasurement[itrack] >= 2 and c.tracks_nValidTrackerHits[itrack] >= 2): return False
	if not c.tracks_nMissingInnerHits[itrack]==0: return False
	if not c.tracks_nMissingMiddleHits[itrack]==0: return False	
	if hMask:
		xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
    		ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
		if hMask.GetBinContent(ibinx, ibiny)==0: return False
	return True

def mkmet(metPt, metPhi):
    met = TLorentzVector()
    met.SetPtEtaPhiE(metPt, 0, metPhi, metPt)
    return met


def passQCDHighMETFilter(t):
    metvec = mkmet(t.MET, t.METPhi)
    for ijet, jet in enumerate(t.Jets):
        if not (jet.Pt() > 200): continue
        if not (t.Jets_muonEnergyFraction[ijet]>0.5):continue 
        if (abs(jet.DeltaPhi(metvec)) > (3.14159 - 0.4)): return False
    return True  
    

def passesUniversalSelection(t):
    if not (bool(t.JetID) and  t.NVtx>0): return False
    if not  passQCDHighMETFilter(t): return False
    if not t.PFCaloMETRatio<2: return False
    #if not t.globalSuperTightHalo2016Filter: return False
    if not t.globalTightHalo2016Filter: return False
    if not t.HBHEIsoNoiseFilter: return False
    if not t.HBHENoiseFilter: return False
    if not t.BadChargedCandidateFilter: return False
    if not t.BadPFMuonFilter: return False
    if not t.CSCTightHaloFilter: return False
    #if not t.ecalBadCalibFilter: return False #this says it's deprecated
    if not t.EcalDeadCellTriggerPrimitiveFilter: return False
    if not t.eeBadScFilter: return False 
    return True


# get fake rate for event:
def getBinContent_with_overflow_2D(histo, xval, yval):
    # get bin content from 2D histogram with overflows:
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
    

# get bin content from 2D histogram with overflows:
def getBinContent_with_overflow_1D(histo, xval):
    if xval >= histo.GetXaxis().GetXmax():
        value = histo.GetBinContent(histo.GetXaxis().GetNbins())
    else:
        value = histo.GetBinContent(histo.GetXaxis().FindBin(xval))
    return value


def loop(event_tree_filenames, track_tree_output, fakerate_file = False, nevents = -1, treename = "TreeMaker2/PreSelection", mask_file = False, only_fakerate = False, verbose = False, iEv_start = False, loose_dxy = False):

    # load tree
    tree = TChain(treename)
    for iFile in event_tree_filenames:
        tree.Add(iFile)
   
    fout = TFile(track_tree_output, "recreate")

    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()

    # check if data:
    data_period = ""
    is_data = False
    for label in ["Summer16", "Fall17", "Autumn18", "Run2016", "Run2017", "Run2018"]:
        if label in event_tree_filenames[0]:
            data_period = label
            if "Run201" in label:
                is_data = True
    if len(data_period) == 0:
        print "Can't determine data/MC era"
        quit(1)
    print "data_period:", data_period

    tout = TTree("Events", "tout")

    # prepare variables for output tree   
    float_branches = ["MET", "MHT", "HT", "MinDeltaPhiMhtJets", "PFCaloMETRatio", "dilepton_invmass"]
    integer_branches = ["n_DT", "n_DT_actualfake", "n_jets", "n_btags", "n_leptons", "n_allvertices", "n_NVtx", "EvtNumEven", "dilepton_CR", "qcd_CR", "qcd_sideband_CR", "meta_CR", "dilepton_leptontype", "passesUniversalSelection", "n_genLeptons", "n_genElectrons", "n_genMuons", "n_genTaus"]

    if not is_data:
        float_branches.append("madHT")
        float_branches.append("CrossSection")
        float_branches.append("puWeight")
        float_branches.append("NumInteractions")
    if only_fakerate:
        float_branches.append("MHT_cleaned")
        float_branches.append("HT_cleaned")
        float_branches.append("MinDeltaPhiMhtJets_cleaned")
        integer_branches.append("n_jets_cleaned")
        integer_branches.append("n_btags_cleaned")

    tree_branch_values = {}
    for variable in float_branches:
        tree_branch_values[variable] = array( 'f', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/F' % variable )
    for variable in integer_branches:
        tree_branch_values[variable] = array( 'i', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/I' % variable )

    # add regions vector:
    region_output = []
    region_noDT_output = []
    tree_branch_values["region"] = 0
    tree_branch_values["region_noDT"] = 0
    tout.Branch("region", 'std::vector<int>', tree_branch_values["region"])
    tout.Branch("region_noDT", 'std::vector<int>', tree_branch_values["region_noDT"])

    # get variables of tree
    track_variables = []
    for i in range(len(tree.GetListOfBranches())):
        label = tree.GetListOfBranches()[i].GetName()
        if "tracks_" in label:
            track_variables.append(label)

    # todo: use track_variables to get all track properties automatically

    # add our track vectors:
    tree_branch_values["tracks"] = 0
    tout.Branch('tracks', 'std::vector<TLorentzVector>', tree_branch_values["tracks"])

    vector_int_branches = ['tracks_is_pixel_track', 'tracks_is_tracker_track', 'tracks_pixelLayersWithMeasurement', 'tracks_trackerLayersWithMeasurement', 'tracks_nMissingInnerHits', 'tracks_nMissingMiddleHits', 'tracks_nMissingOuterHits', 'tracks_trackQualityHighPurity', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_nValidPixelHits', 'tracks_nValidTrackerHits', 'tracks_actualfake', 'tracks_promptbg', 'tracks_promptelectron', 'tracks_promptmuon', 'tracks_prompttau', 'tracks_prompttau_wideDR', 'tracks_passpionveto', 'tracks_is_baseline_track', 'tracks_is_disappearing_track', 'tracks_is_reco_lepton', 'tracks_passPFCandVeto', 'tracks_charge']
    for branch in vector_int_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<int>', tree_branch_values[branch])

    vector_float_branches = ['tracks_dxyVtx', 'tracks_dzVtx', 'tracks_matchedCaloEnergy', 'tracks_trkRelIso', 'tracks_ptErrOverPt2', 'tracks_mva', 'tracks_pt', 'tracks_P', 'tracks_eta', 'tracks_phi', 'tracks_trkMiniRelIso', 'tracks_trackJetIso', 'tracks_ptError', 'tracks_neutralPtSum', 'tracks_neutralWithoutGammaPtSum', 'tracks_minDrLepton', 'tracks_matchedCaloEnergyJets', 'tracks_deDxHarmonic2pixel', 'tracks_deDxHarmonic2strips', 'tracks_deDxHarmonics2WeightedByValidHits', 'tracks_mass_Pixel', 'tracks_mass_Strips', 'tracks_mass_WeightedDeDx','tracks_mass_WeightedByValidHits', 'tracks_chi2perNdof', 'tracks_chargedPtSum']
    for branch in vector_float_branches:
        tree_branch_values[branch] = 0
        tout.Branch(branch, 'std::vector<double>', tree_branch_values[branch])

    # BDT configuration:
    readerPixelOnly = 0
    readerPixelStrips = 0
    preselection_pixelonly = ""
    preselection_pixelstrips = ""

    tmva_variables = {}

    if data_period == "Summer16" or data_period == "Run2016":
        if not loose_dxy:
            bdt_folders = ["../../disappearing-track-tag/2016-short-tracks", "../../disappearing-track-tag/2016-long-tracks"]
        else:
            bdt_folders = ["../../disappearing-track-tag/2016-short-tracks-loose", "../../disappearing-track-tag/2016-long-tracks-loose"]
    elif data_period == "Fall17" or data_period == "Autumn18" or data_period == "Run2017" or data_period == "Run2018":
        bdt_folders = ["../../disappearing-track-tag/2017-short-tracks", "../../disappearing-track-tag/2017-long-tracks"]

    for i_category, category in enumerate(["pixelonly", "pixelstrips"]):

        bdt_infos = tmva_tools.get_tmva_info(bdt_folders[i_category])

        if category == "pixelonly":
            readerPixelOnly = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelonly = bdt_infos["preselection"]
            bdt_cut_pixelonly = 0.1
        elif category == "pixelstrips":
            readerPixelStrips = tmva_tools.prepareReader(bdt_folders[i_category] + '/weights/TMVAClassification_BDT.weights.xml', bdt_infos["variables"], bdt_infos["spectators"], tmva_variables)
            preselection_pixelstrips = bdt_infos["preselection"]
            bdt_cut_pixelstrips = 0.25

    # load and configure data mask:
    if mask_file:
        mask_file = TFile(mask_file, "open")
        if "Run2016" in event_tree_filenames[0]:
            h_mask = mask_file.Get("hEtaVsPhiDT_maskedData-2016Data-2016")
    else:
        h_mask = False

    # load fake rate histograms:
    fakerate_regions = ["dilepton", "qcd", "qcd_sideband"]
    fakerate_variables = ["HT", "n_allvertices", "HT:n_allvertices", "HT:n_allvertices_interpolated", "n_DT"]
    if not only_fakerate and fakerate_file:
        
        # load fakerate maps:
        fakerate_file = TFile(fakerate_file, "open")

        # get all fakerate histograms:
        h_fakerates = {}
        for region in fakerate_regions:
                for category in ["", "short", "long"]:
                    for variable in fakerate_variables:
                        if region == "dilepton":
                            variable = variable.replace("HT", "HT_cleaned")
                        else:
                            variable = variable.replace("_cleaned", "")

                        hist_name = region + "/" + data_period + "/" + category + "/fakerate_" + variable.replace(":", "_")
                        hist_name = hist_name.replace("//", "/")
                        try:
                            h_fakerates[hist_name] = fakerate_file.Get(hist_name)
                        except:
                            print "Error reading fakerate:", hist_name

        # add all raw fakerate branches:        
        for region in fakerate_regions:
            for variable in fakerate_variables:
                if region == "dilepton":
                    variable = variable.replace("HT", "HT_cleaned")
                else:
                    variable = variable.replace("_cleaned", "")

                branch_name = "fakerate_%s_%s" % (region, variable.replace(":", "_"))
                tree_branch_values[branch_name] = array( 'f', [ 0 ] )
                tout.Branch( branch_name, tree_branch_values[branch_name], '%s/F' % branch_name )

    # main loop over events:
    for iEv, event in enumerate(tree):

        if iEv_start and iEv < begin_event:
            continue

        if int(nevents) > 0 and iEv > int(nevents):
            break
        
        if (iEv+1) % 500 == 0:
            PercentProcessed = int( 20 * iEv / nev )
            line = "[" + PercentProcessed*"#" + (20-PercentProcessed)*" " + "]\t" + "Processing event %s / %s" % (iEv + 1, nev)
            print line

        # collect lumisections:
        if is_data:
            runnum = event.RunNum
            lumisec = event.LumiBlockNum
            if runnum not in runs:
                runs[runnum] = []
            if lumisec not in runs[runnum]:
                runs[runnum].append(lumisec)

        # do HT-binned background stitching:
        current_file_name = tree.GetFile().GetName()
        madHT = -1
        if tree.GetBranch("madHT"):
            madHT = event.madHT
            if (madHT>0) and \
               ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
               ("WJetsToLNu_TuneCUETP8M1_13TeV" in current_file_name and madHT>100) or \
               ("HT-100to200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("HT-200to300_" in current_file_name and (madHT<200 or madHT>300)) or \
               ("HT-200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("HT-300to500_" in current_file_name and (madHT<300 or madHT>500)) or \
               ("HT-400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("HT-600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("HT-800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("HT-1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("HT-2500toInf_" in current_file_name and madHT<2500) or \
               ("HT-500to700_" in current_file_name and (madHT<500 or madHT>700)) or \
               ("HT-700to1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
               ("HT-1000to1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
               ("HT-1500to2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
               ("HT-100To200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("HT-200To300_" in current_file_name and (madHT<200 or madHT>300)) or \
               ("HT-200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("HT-300To500_" in current_file_name and (madHT<300 or madHT>500)) or \
               ("HT-400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("HT-500To700_" in current_file_name and (madHT<500 or madHT>700)) or \
               ("HT-600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("HT-700To1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
               ("HT-800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("HT-1000To1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
               ("HT-1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("HT-1500To2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
               ("HT-2500ToInf_" in current_file_name and madHT<2500):
                continue
                  
        # reset all branch values:
        for label in tree_branch_values:
            if "tracks" in label or "region" in label:
                continue
            if "fakerate" in label:
                tree_branch_values[label][0] = 0
            else:
                tree_branch_values[label][0] = -1

        # set selection flags (veto event later if it does not fit into any selection):
        dilepton_CR = False
        qcd_CR = False
        qcd_sideband_CR = False

        min_lepton_pt = 30.0
        invariant_mass = 0
        if (len(event.Electrons) == 2 and len(event.Muons) == 0):
            if (event.Electrons[0].Pt() > min_lepton_pt):
                if bool(event.Electrons_mediumID[0]) and bool(event.Electrons_mediumID[1]):
                    if (event.Electrons_charge[0] * event.Electrons_charge[1] < 0):
                        invariant_mass = (event.Electrons[0] + event.Electrons[1]).M()
                        if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                            if bool(event.Electrons_passIso[0]) and bool(event.Electrons_passIso[1]):
                                if abs(event.Electrons[0].Eta()) < 2.4 and abs(event.Electrons[1].Eta()):
                                    tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                    tree_branch_values["dilepton_leptontype"][0] = 11
                                    tree_branch_values["dilepton_CR"][0] = 1
                                    dilepton_CR = True       
        elif (len(event.Muons) == 2 and len(event.Electrons) == 0):
            if (event.Muons[0].Pt() > min_lepton_pt):
                if (bool(event.Muons_tightID[0]) and bool(event.Muons_tightID[1])):
                    if (event.Muons_charge[0] * event.Muons_charge[1] < 0):
                        invariant_mass = (event.Muons[0] + event.Muons[1]).M()            
                        if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                            if bool(event.Muons_passIso[0]) and bool(event.Muons_passIso[1]):
                                if abs(event.Muons[0].Eta()) < 2.4 and abs(event.Muons[1].Eta()):
                                    tree_branch_values["dilepton_invmass"][0] = invariant_mass
                                    tree_branch_values["dilepton_leptontype"][0] = 13
                                    tree_branch_values["dilepton_CR"][0] = 1
                                    dilepton_CR = True

        # check if low-MHT, QCD-only samples:
        if "QCD" in current_file_name or "JetHT" in current_file_name:
            if event.MHT < 200:
                tree_branch_values["qcd_CR"][0] = 1
                qcd_CR = True
            if event.MHT > 100 and event.MHT < 200:
                tree_branch_values["qcd_sideband_CR"][0] = 1
                qcd_sideband_CR = True

        # event selection for fake rate determination
        if only_fakerate:
            if not dilepton_CR and not qcd_CR and not qcd_sideband_CR: continue
                
            # for the dilepton CR, clean event (recalculate HT, MHT, n_Jets without the two leptons):
            if dilepton_CR:
                csv_b = 0.8838
                metvec = TLorentzVector()
                metvec.SetPtEtaPhiE(event.MET, 0, event.METPhi, event.MET)
                mhtvec = TLorentzVector()
                mhtvec.SetPtEtaPhiE(0, 0, 0, 0)
                jets = []
                nb = 0
                HT_cleaned = 0
                
                for ijet, jet in enumerate(event.Jets):
                    
                    if not (abs(jet.Eta()) < 5 and jet.Pt() > 30): continue
                    
                    # check if lepton is in jet, and veto jet if that is the case
                    lepton_is_in_jet = False
                    for leptons in [event.Electrons, event.Muons]:
                        for lepton in leptons:
                            if jet.DeltaR(lepton) < 0.05:
                                lepton_is_in_jet = True
                    if lepton_is_in_jet: continue
                    
                    mhtvec-=jet
                    if not abs(jet.Eta()) < 2.4: continue

                    jets.append(jet)
                    HT_cleaned+=jet.Pt()        
                    if event.Jets_bDiscriminatorCSV[ijet] > csv_b: nb+=1
                    
                n_btags_cleaned = nb        
                n_jets_cleaned = len(jets)
                MHT_cleaned = mhtvec.Pt()

                MinDeltaPhiMhtJets_cleaned = 9999   
                for jet in jets: 
                    if abs(jet.DeltaPhi(mhtvec)) < MinDeltaPhiMhtJets_cleaned:
                        MinDeltaPhiMhtJets_cleaned = abs(jet.DeltaPhi(mhtvec))

                tree_branch_values["n_btags_cleaned"][0] = n_btags_cleaned
                tree_branch_values["n_jets_cleaned"][0] = n_jets_cleaned
                tree_branch_values["MHT_cleaned"][0] = MHT_cleaned
                tree_branch_values["HT_cleaned"][0] = HT_cleaned
                tree_branch_values["MinDeltaPhiMhtJets_cleaned"][0] = MinDeltaPhiMhtJets_cleaned

        # calculate MinDeltaPhiMhtJets:
        csv_b = 0.8838
        mhtvec = TLorentzVector()
        mhtvec.SetPtEtaPhiE(event.MHT, 0, event.MHTPhi, event.MHT)
        MinDeltaPhiMhtJets = 9999
        nj = 0
        nb = 0
        for ijet, jet in enumerate(event.Jets):
            if not (abs(jet.Eta())<2.4 and jet.Pt()>30): continue
            nj+=1
            if event.Jets_bDiscriminatorCSV[ijet]>csv_b: nb+=1
            if abs(jet.DeltaPhi(mhtvec))<MinDeltaPhiMhtJets:
                MinDeltaPhiMhtJets = abs(jet.DeltaPhi(mhtvec))
     
        # loop over tracks (tracks):
        n_DT = 0
        n_DT_actualfake = 0

        # for each event, first fill this list for each track         
        track_level_output = []

        for iCand in range(len(event.tracks)):

            # set up booleans
            is_disappearing_track = False
            is_reco_lepton = False

            # re-check PF lepton veto:
            for k in range(len(event.Muons)):
                deltaR = event.tracks[iCand].DeltaR(event.Muons[k])
                if deltaR < 0.01:
                    is_reco_lepton = True
            for k in range(len(event.Electrons)):
                deltaR = event.tracks[iCand].DeltaR(event.Electrons[k])
                if deltaR < 0.01:
                    is_reco_lepton = True

            # fill custom variables:
            ptErrOverPt2 = event.tracks_ptError[iCand] / (event.tracks[iCand].Pt()**2)

            # check for category:
            is_pixel_track = False
            is_tracker_track = False
            if event.tracks_trackerLayersWithMeasurement[iCand] == event.tracks_pixelLayersWithMeasurement[iCand]:
                is_pixel_track = True
            elif event.tracks_trackerLayersWithMeasurement[iCand] > event.tracks_pixelLayersWithMeasurement[iCand]:
                is_tracker_track = True
                            
            # apply TMVA preselection:
            if is_pixel_track and not (event.tracks[iCand].Pt() > 30 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                (loose_dxy or event.tracks_dxyVtx[iCand] < 0.1) and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
                    continue

            if is_tracker_track and not (event.tracks[iCand].Pt() > 30 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                (loose_dxy or event.tracks_dxyVtx[iCand] < 0.1) and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingOuterHits[iCand] >= 2 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
                    continue

            # evaluate BDT:
            if not loose_dxy: tmva_variables["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
            tmva_variables["dzVtx"][0] = event.tracks_dzVtx[iCand]
            tmva_variables["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
            tmva_variables["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
            tmva_variables["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
            tmva_variables["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
            tmva_variables["nMissingOuterHits"][0] = event.tracks_nMissingOuterHits[iCand]
            tmva_variables["ptErrOverPt2"][0] = ptErrOverPt2

            is_baseline_track = isBaselineTrack(event.tracks[iCand], iCand, event, h_mask, loose_dxy=loose_dxy)

            if is_pixel_track:
                mva = readerPixelOnly.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelonly and is_baseline_track:
                    is_disappearing_track = True
            elif is_tracker_track:
                mva = readerPixelStrips.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelstrips and is_baseline_track: 
                    is_disappearing_track = True

            # select which tracks to keep
            keep_track = is_disappearing_track

            # check if actual fake track (no genparticle in cone around track):
            charged_genlepton_in_track_cone = False
            is_prompt_bg = False
            is_prompt_electron = False
            is_prompt_muon = False
            is_tau_bg = False
            is_tau_bg_wideDR = False
            if keep_track:

                #print "Found DT"

                # check MC Truth for prompt/non-prompt background:
                if not is_data:
                    for k in range(len(event.GenParticles)):

                        if charged_genlepton_in_track_cone: break

                        deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                        gen_track_cone_pdgid = abs(event.GenParticles_PdgId[k])

                        if deltaR < 0.02:
                              
                            if (gen_track_cone_pdgid == 11 or gen_track_cone_pdgid == 13) and event.GenParticles_Status[k] == 1:
                                charged_genlepton_in_track_cone = True
                                is_prompt_bg = True
                                if gen_track_cone_pdgid == 11: 
                                    is_prompt_electron = True
                                if gen_track_cone_pdgid == 13: 
                                    is_prompt_muon = True
                                break
                            elif gen_track_cone_pdgid == 15:
                                # if genTau, check if the track matches with a GenTaus_LeadTrk track:
                                for l in range(len(event.GenTaus_LeadTrk)):
                                    deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                    if deltaR < 0.04:
                                        print "That's a tau leading track"
                                        charged_genlepton_in_track_cone = True
                                        is_tau_bg = True
                                        break

                        # if track seems to be fake, check again with wider DR for gentau:
                        if gen_track_cone_pdgid == 15 and deltaR < 0.4:
                            is_tau_bg_wideDR = True
                            print "Found tau within a wide cone"
                            charged_genlepton_in_track_cone = True
                            break
           

                passpionveto = True
                for k in range(len(event.TAPPionTracks)):
                    deltaR = event.tracks[iCand].DeltaR(event.TAPPionTracks[k])
                    if deltaR < 0.03:
                        passpionveto = False
                        break

                # disappearing track counters:
                if is_disappearing_track and passpionveto and not is_reco_lepton:
                    n_DT += 1
                    if not charged_genlepton_in_track_cone:
                        n_DT_actualfake += 1
		    
		    # Weighted average of pixel/strips dE/dx
                    tracks_deDxHarmonics2WeightedByValidHits = (event.tracks_deDxHarmonic2pixel[iCand]*event.tracks_nValidPixelHits[iCand] + event.tracks_deDxHarmonic2strips[iCand]*event.tracks_nValidTrackerHits[iCand])/(event.tracks_nValidPixelHits[iCand] + event.tracks_nValidTrackerHits[iCand])
		    
		    # Track mass calculation using pixel/strips dE/dx
		    tracks_mass_Pixel = TMath.Sqrt((event.tracks_deDxHarmonic2pixel[iCand]-2.557)*pow(event.tracks[iCand].P(),2)/2.579)
            	    tracks_mass_Strips = TMath.Sqrt((event.tracks_deDxHarmonic2strips[iCand]-2.557)*pow(event.tracks[iCand].P(),2)/2.579)
            	    tracks_mass_WeightedDeDx = TMath.Sqrt((tracks_deDxHarmonics2WeightedByValidHits-2.557)*pow(event.tracks[iCand].P(),2)/2.579)
            	    tracks_mass_WeightedByValidHits = (tracks_mass_Pixel * event.tracks_nValidPixelHits[iCand] + tracks_mass_Strips*event.tracks_nValidTrackerHits[iCand])/(event.tracks_nValidPixelHits[iCand] + event.tracks_nValidTrackerHits[iCand])
            	    
            	    if not tracks_deDxHarmonics2WeightedByValidHits > 0: tracks_deDxHarmonics2WeightedByValidHits = -1
            	    if not tracks_mass_Pixel > 0: tracks_mass_Pixel = -1
            	    if not tracks_mass_Strips > 0: tracks_mass_Strips = -1
            	    if not tracks_mass_WeightedDeDx > 0: tracks_mass_WeightedDeDx = -1
            	    if not tracks_mass_WeightedByValidHits > 0: tracks_mass_WeightedByValidHits = -1
                    
		    print "Found disappearing track in event %s, charged genLeptons in cone: %s" % (iEv, charged_genlepton_in_track_cone)

                    track_level_output.append(
                                           {
                                             "tracks": event.tracks[iCand],
                                             "tracks_is_pixel_track": is_pixel_track,
                                             "tracks_is_tracker_track": is_tracker_track,
                                             "tracks_pixelLayersWithMeasurement": event.tracks_pixelLayersWithMeasurement[iCand],
                                             "tracks_trackerLayersWithMeasurement": event.tracks_trackerLayersWithMeasurement[iCand],
                                             "tracks_actualfake": not charged_genlepton_in_track_cone,
                                             "tracks_nMissingInnerHits": event.tracks_nMissingInnerHits[iCand],
                                             "tracks_nMissingMiddleHits": event.tracks_nMissingMiddleHits[iCand],
                                             "tracks_nMissingOuterHits": event.tracks_nMissingOuterHits[iCand],
                                             "tracks_trackQualityHighPurity": bool(event.tracks_trackQualityHighPurity[iCand]),
                                             "tracks_nValidPixelHits": event.tracks_nValidPixelHits[iCand],
                                             "tracks_nValidTrackerHits": event.tracks_nValidTrackerHits[iCand],
                                             "tracks_dxyVtx": event.tracks_dxyVtx[iCand],
                                             "tracks_dzVtx": event.tracks_dzVtx[iCand],
                                             "tracks_matchedCaloEnergy": event.tracks_matchedCaloEnergy[iCand],
                                             "tracks_trkRelIso": event.tracks_trkRelIso[iCand],
                                             "tracks_ptErrOverPt2": ptErrOverPt2,
                                             "tracks_mva": mva,
                                             "tracks_pt": event.tracks[iCand].Pt(),
                                             "tracks_P": event.tracks[iCand].P(),
                                             "tracks_eta": event.tracks[iCand].Eta(),
                                             "tracks_phi": event.tracks[iCand].Phi(),
                                             "tracks_promptbg": is_prompt_bg,
                                             "tracks_promptelectron": is_prompt_electron,
                                             "tracks_promptmuon": is_prompt_muon,
                                             "tracks_prompttau": is_tau_bg,
                                             "tracks_prompttau_wideDR": is_tau_bg_wideDR,
                                             "tracks_passpionveto": passpionveto,
                                             "tracks_is_baseline_track": is_baseline_track,
                                             "tracks_is_disappearing_track": is_disappearing_track,
                                             "tracks_is_reco_lepton": is_reco_lepton,
                                             "tracks_trkMiniRelIso": event.tracks_trkMiniRelIso[iCand],
                                             "tracks_trackJetIso": event.tracks_trackJetIso[iCand],
                                             "tracks_ptError": event.tracks_ptError[iCand],
                                             "tracks_passPFCandVeto": bool(event.tracks_passPFCandVeto[iCand]),
                                             "tracks_neutralPtSum": event.tracks_neutralPtSum[iCand],
                                             "tracks_neutralWithoutGammaPtSum": event.tracks_neutralWithoutGammaPtSum[iCand],
                                             "tracks_minDrLepton": event.tracks_minDrLepton[iCand],
                                             "tracks_matchedCaloEnergyJets": event.tracks_matchedCaloEnergyJets[iCand],
                                             "tracks_deDxHarmonic2pixel": event.tracks_deDxHarmonic2pixel[iCand],
                                             "tracks_deDxHarmonic2strips": event.tracks_deDxHarmonic2strips[iCand],
                                             "tracks_deDxHarmonics2WeightedByValidHits": tracks_deDxHarmonics2WeightedByValidHits,
                                             "tracks_mass_Pixel": tracks_mass_Pixel,
                                             "tracks_mass_Strips": tracks_mass_Strips,
                                             "tracks_mass_WeightedDeDx": tracks_mass_WeightedDeDx,
                                             "tracks_mass_WeightedByValidHits": tracks_mass_WeightedByValidHits,
                                             "tracks_chi2perNdof": event.tracks_chi2perNdof[iCand],
                                             "tracks_chargedPtSum": event.tracks_chargedPtSum[iCand],
                                             "tracks_charge": event.tracks_charge[iCand],
                                           }
                                          )

        # for loose selection, don't store events without DTs
        #if only_fakerate and loose_dxy and n_DT==0:
        #    continue

        # evaluate fake rate for each event:
        if not only_fakerate and fakerate_file:

            # check signal/control region bin:
            if n_DT > 0:
                is_pixel_track = track_level_output[0]["tracks_is_pixel_track"]
                region = get_signal_region(event, MinDeltaPhiMhtJets, n_DT, is_pixel_track)
                tree_branch_values["region"][0] = region
            elif n_DT == 0:
                region_noDT = get_signal_region(event, MinDeltaPhiMhtJets, 1, False)
                if region_noDT > 0:
                    region_noDT_output.append(region_noDT)
                    region_noDT_output.append(region_noDT + 15)
                region_noDT_multiple = get_signal_region(event, MinDeltaPhiMhtJets, 2, False)
                if region_noDT_multiple > 0:
                    region_noDT_output.append(region_noDT_multiple)

            # fill all fakerate branches:
            for variable in fakerate_variables:
                for fr_region in fakerate_regions:
                    if fr_region == "dilepton":
                        variable = variable.replace("HT", "HT_cleaned")
                    else:
                        variable = variable.replace("_cleaned", "")
                    
                    #FIXME: no interpolation available for dilepton FRR
                    if fr_region == "dilepton" and "interpolated" in variable:
                        continue
                    
                    hist_name = fr_region + "/" + data_period + "/fakerate_" + variable.replace(":", "_")
                    
                    if variable == "n_DT":
                        FR = getBinContent_with_overflow_1D(h_fakerates[hist_name], 1)

                    elif ":" in variable:
                        xvalue = eval("event.%s" % variable.replace("_interpolated", "").replace("n_allvertices", "nAllVertices").replace("_cleaned", "").replace("n_NVtx", "NVtx").split(":")[1])
                        yvalue = eval("event.%s" % variable.replace("_interpolated", "").replace("n_allvertices", "nAllVertices").replace("_cleaned", "").replace("n_NVtx", "NVtx").split(":")[0])
                                                
                        FR = getBinContent_with_overflow_2D(h_fakerates[hist_name], xvalue, yvalue)
                    else:
                        value = eval("event.%s" % variable.replace("n_allvertices", "nAllVertices").replace("_cleaned", "").replace("n_NVtx", "NVtx"))
                        FR = getBinContent_with_overflow_1D(h_fakerates[hist_name], value)
                    
                    branch_name = "fakerate_%s_%s" % (fr_region, variable.replace(":", "_"))
                    tree_branch_values[branch_name][0] = FR

        # check if genLeptons are present in event:
        if not only_fakerate and not is_data:

            n_genLeptons = 0
            n_genElectrons = 0
            n_genMuons = 0
            n_genTaus = 0
            for k in range(len(event.GenParticles)):

                absPdgId = abs(event.GenParticles_PdgId[k])
                
                if absPdgId == 11:
                    n_genElectrons += 1
                    n_genLeptons += 1
                elif absPdgId == 13:
                    n_genMuons += 1
                    n_genLeptons += 1
                elif absPdgId == 15:
                    n_genTaus += 1
                    n_genLeptons += 1
                    
                tree_branch_values["n_genLeptons"][0] = n_genLeptons
                tree_branch_values["n_genElectrons"][0] = n_genElectrons
                tree_branch_values["n_genMuons"][0] = n_genMuons
                tree_branch_values["n_genTaus"][0] = n_genTaus

        # check if in meta CR:
        meta_CR = False
        if event.BTags >= 1 and event.MHT>100 and event.MHT<300:
            # check for well-reconstructed electron:
            if (len(event.Electrons)>0 and (event.Electrons[0].Pt() > 30) and bool(event.Electrons_mediumID[0]) and bool(event.Electrons_passIso[0])) or \
               (len(event.Muons)>0 and (event.Muons[0].Pt() > 30) and bool(event.Muons_tightID[0]) and bool(event.Muons_passIso[0])):
               meta_CR = True
               tree_branch_values["meta_CR"][0] = meta_CR


        # save event-level variables:
        tree_branch_values["passesUniversalSelection"][0] = passesUniversalSelection(event)
        tree_branch_values["n_leptons"][0] = len(event.Electrons) + len(event.Muons)
        tree_branch_values["n_btags"][0] = event.BTags
        tree_branch_values["n_DT"][0] = n_DT
        tree_branch_values["n_DT_actualfake"][0] = n_DT_actualfake
        tree_branch_values["n_jets"][0] = len(event.Jets)
        tree_branch_values["n_allvertices"][0] = event.nAllVertices
        tree_branch_values["PFCaloMETRatio"][0] = event.PFCaloMETRatio
        tree_branch_values["MET"][0] = event.MET
        tree_branch_values["MHT"][0] = event.MHT
        tree_branch_values["HT"][0] = event.HT
        tree_branch_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets
        tree_branch_values["n_NVtx"][0] = event.NVtx
        if not is_data:
            tree_branch_values["madHT"][0] = madHT
            tree_branch_values["CrossSection"][0] = event.CrossSection
            tree_branch_values["puWeight"][0] = event.puWeight
            tree_branch_values["NumInteractions"][0] = event.NumInteractions
        if event.EvtNum % 2 == 0:
            tree_branch_values["EvtNumEven"][0] = 1
        else:
            tree_branch_values["EvtNumEven"][0] = 0
     
        # tree-level variables:
        n_tracks = len(track_level_output)
        tree_branch_values["tracks"] = ROOT.std.vector(TLorentzVector)(n_tracks)
      
        for branch in vector_int_branches:
            tree_branch_values[branch] = ROOT.std.vector(int)(n_tracks)
        for branch in vector_float_branches:
            tree_branch_values[branch] = ROOT.std.vector(double)(n_tracks)

        # register track-level branches:
        for label in tree_branch_values:
            if "tracks" in label:
                tout.SetBranchAddress(label, tree_branch_values[label])

        # save track-level properties:
        for i, track_output_dict in enumerate(track_level_output):
            for label in track_output_dict:
                tree_branch_values[label][i] = track_output_dict[label]

        tout.Fill()
     
    fout.cd()

    if not only_fakerate and fakerate_file:
        fakerate_file.Close()
    if mask_file:
        mask_file.Close()

    fout.cd()
    fout.Write()
    fout.Close()

    # write JSON containing lumisections:
    if len(runs) > 0:
        runs_compacted = {}
        for run in runs:
            if run not in runs_compacted:
                runs_compacted[run] = []
            for lumisec in runs[run]:
                if len(runs_compacted[run]) > 0 and lumisec == runs_compacted[run][-1][-1]+1:
                    runs_compacted[run][-1][-1] = lumisec
                else:
                    runs_compacted[run].append([lumisec, lumisec])

        json_content = json.dumps(runs_compacted)
        with open(track_tree_output.replace(".root", ".json"), "w") as fo:
            fo.write(json_content)


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--input", dest="inputfiles")
    parser.add_option("--output", dest="outputfiles")
    parser.add_option("--only_fakerate", dest="only_fakerate", action="store_true", default=False)
    parser.add_option("--mask", dest="maskfile", default=False)
    parser.add_option("--nev", dest="nev", default=-1)
    parser.add_option("--fakerate_file", dest="fakerate_file", default=False)
    parser.add_option("--iEv_start", dest="iEv_start", default=0)
    parser.add_option("--loose_dxy", dest="loose_dxy", action="store_true", default=False)    
    (options, args) = parser.parse_args()
    
    options.inputfiles = options.inputfiles.split(",")

    loop(options.inputfiles,
         options.outputfiles,
         nevents = options.nev,
         only_fakerate = options.only_fakerate,
         mask_file = options.maskfile,
         iEv_start = options.iEv_start,
         fakerate_file = options.fakerate_file,
         loose_dxy = options.loose_dxy)

