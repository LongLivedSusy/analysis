#!/bin/env python
from __future__ import division
from ROOT import *
from array import array
from optparse import OptionParser
import tmva_tools
import collections

gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

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

def isBaselineTrack(track, itrack, c, hMask):
	if not abs(track.Eta())< 2.4 : return False
	if not (abs(track.Eta()) < 1.4442 or abs(track.Eta()) > 1.566): return False
	if not bool(c.tracks_trackQualityHighPurity[itrack]) : return False
	if not (c.tracks_ptError[itrack]/(track.Pt()*track.Pt()) < 10): return False
	if not abs(c.tracks_dxyVtx[itrack]) < 0.1: return False
	if not abs(c.tracks_dzVtx[itrack]) < 0.1 : return False
	if not c.tracks_trkRelIso[itrack] < 0.2: return False
	if not (c.tracks_trackerLayersWithMeasurement[itrack] >= 2 and c.tracks_nValidTrackerHits[itrack] >= 2): return False
	if not c.tracks_nMissingInnerHits[itrack]==0: return False
	if not c.tracks_nMissingMiddleHits[itrack]==0: return False	
	if hMask!='':
		xax, yax = hMask.GetXaxis(), hMask.GetYaxis()
		ibinx, ibiny = xax.FindBin(track.Phi()), yax.FindBin(track.Eta())
		if hMask.GetBinContent(ibinx, ibiny)==0: return False
	return True

def passQCDHighMETFilter(t):
    metvec = mkmet(t.MET, t.METPhi)
    for ijet, jet in enumerate(t.Jets):
        if not (jet.Pt() > 200): continue
        if not (t.Jets_muonEnergyFraction[ijet]>0.5):continue 
        if (abs(jet.DeltaPhi(metvec)) > (3.14159 - 0.4)): return False
    return True  
    
def mkmet(metPt, metPhi):
    met = TLorentzVector()
    met.SetPtEtaPhiE(metPt, 0, metPhi, metPt)
    return met

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


def loop(event_tree_filenames, track_tree_output, nevents = -1, treename = "TreeMaker2/PreSelection", maskfile = "Masks.root", region_fakerate = False, region_signalcontrol = True, verbose = False, iEv_start = False):

    if region_signalcontrol:
        print "\nConfigured for inclusive SR / CR!\n"
    if region_fakerate:
        print "\nConfigured for fake rate estimation region!\n"

    tree = TChain(treename)
    for iFile in event_tree_filenames:
        tree.Add(iFile)
    
    fout = TFile(track_tree_output, "recreate")

    # write number of events to histogram:
    nev = tree.GetEntries()
    h_nev = TH1F("nev", "nev", 1, 0, 1)
    h_nev.Fill(0, nev)
    h_nev.Write()
    #xsec_written = False

    # check if data:
    data_period = ""
    is_data = False
    if "Summer16" in event_tree_filenames[0]:
        data_period = "Summer16"
    elif "Fall17" in event_tree_filenames[0]:
        data_period = "Fall17"
    elif "Run2016" in event_tree_filenames[0]:
        data_period = "2016"
        is_data = True
    elif "Run2017" in event_tree_filenames[0]:
        data_period = "2017"
        is_data = True
    elif "Run2018" in event_tree_filenames[0]:
        data_period = "2018"
        is_data = True
    else:
        print "Can't determine data/MC era"
        quit(1)
    print "data_period", data_period, "is_data", is_data

    tout = TTree("Events", "tout")
 
    # get variables of tree
    variables = []
    for i in range(len(tree.GetListOfBranches())):
        label = tree.GetListOfBranches()[i].GetName()
        if "tracks_" in label:
            label = label.replace("tracks_", "")
            variables.append(label)

    # prepare variables for output tree   
    float_branches = []
    if not is_data:
        float_branches.append("madHT")
        float_branches.append("CrossSection")
        float_branches.append("puWeight")
        float_branches.append("NumInteractions")
    float_branches.append("MET")
    float_branches.append("MHT")
    float_branches.append("HT")
    float_branches.append("MinDeltaPhiMhtJets")
    float_branches.append("PFCaloMETRatio")
    if region_fakerate:
        float_branches.append("dilepton_invmass")
        float_branches.append("MHT_cleaned")
        float_branches.append("HT_cleaned")
        float_branches.append("MinDeltaPhiMhtJets_cleaned")
       
    integer_branches = []
    integer_branches.append("n_DT")
    integer_branches.append("n_DT_actualfake")
    integer_branches.append("n_jets")
    integer_branches.append("n_btags")
    integer_branches.append("n_leptons")
    integer_branches.append("n_allvertices")
    integer_branches.append("n_NVtx")
    integer_branches.append("EvtNumEven")
    if region_fakerate:
        integer_branches.append("n_jets_cleaned")
        integer_branches.append("n_btags_cleaned")
        integer_branches.append("dilepton_CR")
        integer_branches.append("qcd_CR")
        integer_branches.append("qcd_sideband_CR")
        integer_branches.append("dilepton_leptontype")
    if region_signalcontrol: 
        integer_branches.append("region")
        integer_branches.append("region_noDT")
        integer_branches.append("region_noDT_ext")
        integer_branches.append("region_noDT_ext2")
        integer_branches.append("meta_CR")
    integer_branches.append("hemfailure_electron")
    integer_branches.append("hemfailure_jet")
    integer_branches.append("hemfailure_dt")
    integer_branches.append("passesUniversalSelection")

    for i in range(1,4):
        integer_branches.append("DT%i_is_pixel_track" % i)
        integer_branches.append("DT%i_pixelLayersWithMeasurement" % i)
        integer_branches.append("DT%i_trackerLayersWithMeasurement" % i)
        integer_branches.append("DT%i_nMissingInnerHits" % i)
        integer_branches.append("DT%i_nMissingMiddleHits" % i)
        integer_branches.append("DT%i_nMissingOuterHits" % i)
        integer_branches.append("DT%i_trackQualityHighPurity" % i)
        integer_branches.append("DT%i_nValidPixelHits" % i)
        integer_branches.append("DT%i_nValidTrackerHits" % i)
        integer_branches.append("DT%i_actualfake" % i)
        integer_branches.append("DT%i_promptbg" % i)
        integer_branches.append("DT%i_taubg" % i)
        integer_branches.append("DT%i_hemfailure" % i)
        float_branches.append("DT%i_dxyVtx" % i)
        float_branches.append("DT%i_dzVtx" % i)
        float_branches.append("DT%i_matchedCaloEnergy" % i)
        float_branches.append("DT%i_trkRelIso" % i)
        float_branches.append("DT%i_ptErrOverPt2" % i)
        float_branches.append("DT%i_mva" % i)
        float_branches.append("DT%i_pt" % i)
        float_branches.append("DT%i_eta" % i)
        float_branches.append("DT%i_phi" % i)

    tree_branch_values = {}
    for variable in float_branches:
        tree_branch_values[variable] = array( 'f', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/F' % variable )
    for variable in integer_branches:
        tree_branch_values[variable] = array( 'i', [ -1 ] )
        tout.Branch( variable, tree_branch_values[variable], '%s/I' % variable )
        
    # BDT configuration:
    readerPixelOnly = 0
    readerPixelStrips = 0
    preselection_pixelonly = ""
    preselection_pixelstrips = ""

    tmva_variables = {}

    if data_period == "Summer16" or data_period == "2016":
        bdt_folders = ["../../disappearing-track-tag/2016-short-tracks", "../../disappearing-track-tag/2016-long-tracks"]
    elif data_period == "Fall17" or data_period == "2017" or data_period == "2018":
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

    # load data mask file:
    mask = ""
    if maskfile:
        mask_file = TFile(maskfile, "open")
        if "Run2016" in event_tree_filenames[0]:
            mask = mask_file.Get("hEtaVsPhiDT_maskedData-2016Data-2016")

    if region_signalcontrol:
        
        # load fakerate maps:
        fakerate_file = TFile("fakerate.root", "open")
                   
        fakerate_regions = ["dilepton", "qcd", "qcd_sideband"]
        fakerate_variables = ["HT:n_allvertices", "n_allvertices", "HT", "MHT", "MHT:n_allvertices"] #, "HT:n_NVtx", "n_NVtx"]

        # get all fakerate histograms:
        h_fakerates = {}
        for region in fakerate_regions:
                for category in ["short", "long"]:
                    for variable in fakerate_variables:
                        if region == "dilepton":
                            variable = variable.replace("HT", "HT_cleaned")
                        else:
                            variable = variable.replace("_cleaned", "")
                        hist_name = region + "/" + data_period + "/" + category + "/fakerate_" + variable.replace(":", "_")
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

    # loop over events
    for iEv, event in enumerate(tree):

        if iEv_start and iEv < begin_event:
            continue

        if nevents > 0 and iEv > nevents:
            break
        
        if (iEv+1) % 500 == 0:
            PercentProcessed = int( 20 * iEv / nev )
            line = "[" + PercentProcessed*"#" + (20-PercentProcessed)*" " + "]\t" + "Processing event %s / %s" % (iEv + 1, nev)
            print line

        if region_signalcontrol:
                        
            # check if in meta CR:
            meta_CR = False
            if event.BTags >= 1 and event.MHT>100 and event.MHT<300:
                # check for well-reconstructed electron:
                if (len(event.Electrons)>0 and (event.Electrons[0].Pt() > 30) and bool(event.Electrons_mediumID[0]) and bool(event.Electrons_passIso[0])) or \
                   (len(event.Muons)>0 and (event.Muons[0].Pt() > 30) and bool(event.Muons_tightID[0]) and bool(event.Muons_passIso[0])):
                   meta_CR = True
                   tree_branch_values["meta_CR"][0] = meta_CR

        # do HT-binned background stitching:
        current_file_name = tree.GetFile().GetName()
        madHT = -1
        if tree.GetBranch("madHT"):
            madHT = event.madHT
            if (madHT>0) and \
               ("DYJetsToLL_M-50_Tune" in current_file_name and madHT>100) or \
               ("TTJets_Tune" in current_file_name and madHT>600) or \
               ("100to200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("100To200_" in current_file_name and (madHT<100 or madHT>200)) or \
               ("200to300_" in current_file_name and (madHT<200 or madHT>300)) or \
               ("200To300_" in current_file_name and (madHT<200 or madHT>300)) or \
               ("200to400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("200To400_" in current_file_name and (madHT<200 or madHT>400)) or \
               ("300to500_" in current_file_name and (madHT<300 or madHT>500)) or \
               ("300To500_" in current_file_name and (madHT<300 or madHT>500)) or \
               ("400to600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("400To600_" in current_file_name and (madHT<400 or madHT>600)) or \
               ("500to700_" in current_file_name and (madHT<500 or madHT>700)) or \
               ("500To700_" in current_file_name and (madHT<500 or madHT>700)) or \
               ("600to800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("600To800_" in current_file_name and (madHT<600 or madHT>800)) or \
               ("700to1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
               ("700To1000_" in current_file_name and (madHT<700 or madHT>1000)) or \
               ("800to1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("800To1200_" in current_file_name and (madHT<800 or madHT>1200)) or \
               ("1000to1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
               ("1000To1500_" in current_file_name and (madHT<1000 or madHT>1500)) or \
               ("1200to2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("1200To2500_" in current_file_name and (madHT<1200 or madHT>2500)) or \
               ("1500to2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
               ("1500To2000_" in current_file_name and (madHT<1500 or madHT>2000)) or \
               ("2500toInf_" in current_file_name and madHT<2500) or \
               ("2500ToInf_" in current_file_name and madHT<2500):
                continue
                  
        # reset all branch values:
        for label in tree_branch_values:
            if "fakerate" in label:
                tree_branch_values[label][0] = 0
            else:
                tree_branch_values[label][0] = -1

        if region_fakerate:

            # to get the fake rate, consider dilepton region or QCD-only events. Check which applies for this event

            # set selection flags (veto event later if it does not fit into any selection):
            dilepton_CR = False
            qcd_CR = False
            qcd_sideband_CR = False

            # do the following for all MC, but only for SingleLepton datastreams:
            if not is_data or "SingleElectron" in current_file_name or "SingleMuon" in current_file_name:
                min_lepton_pt = 30.0
                invariant_mass = 0
                if (len(event.Electrons) == 2 and len(event.Muons) == 0):
                    if (event.Electrons[0].Pt() > min_lepton_pt):
                        if bool(event.Electrons_mediumID[0]) and bool(event.Electrons_mediumID[1]):
                            if (event.Electrons_charge[0] * event.Electrons_charge[1] < 0):
                                invariant_mass = (event.Electrons[0] + event.Electrons[1]).M()
                                if invariant_mass > (91.19 - 10.0) and invariant_mass < (91.19 + 10.0):
                                    if bool(event.Electrons_passIso[0]) and bool(event.Electrons_passIso[1]):
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

            # CHECK: event selection
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

        for iCand in xrange(len(event.tracks)):

            # set up booleans
            charged_genparticle_in_track_cone = False
            is_disappearing_track = False
            is_a_PF_lepton = False

            # re-check PF lepton veto:
            for k in range(len(event.Muons)):
                deltaR = event.tracks[iCand].DeltaR(event.Muons[k])
                if deltaR < 0.01:
                    is_a_PF_lepton = True
            for k in range(len(event.Electrons)):
                deltaR = event.tracks[iCand].DeltaR(event.Electrons[k])
                if deltaR < 0.01:
                    is_a_PF_lepton = True

            if is_a_PF_lepton: continue

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
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
                    continue

            if is_tracker_track and not (event.tracks[iCand].Pt() > 30 and \
                abs(event.tracks[iCand].Eta()) < 2.4 and \
                event.tracks_trkRelIso[iCand] < 0.2 and \
                event.tracks_dxyVtx[iCand] < 0.1 and \
                event.tracks_dzVtx[iCand] < 0.1 and \
                ptErrOverPt2 < 10 and \
                event.tracks_nMissingOuterHits[iCand] >= 2 and \
                event.tracks_nMissingMiddleHits[iCand] == 0 and \
                bool(event.tracks_trackQualityHighPurity[iCand]) == 1):
                    continue

            # evaluate BDT:
            tmva_variables["dxyVtx"][0] = event.tracks_dxyVtx[iCand]
            tmva_variables["dzVtx"][0] = event.tracks_dzVtx[iCand]
            tmva_variables["matchedCaloEnergy"][0] = event.tracks_matchedCaloEnergy[iCand]
            tmva_variables["trkRelIso"][0] = event.tracks_trkRelIso[iCand]
            tmva_variables["nValidPixelHits"][0] = event.tracks_nValidPixelHits[iCand]
            tmva_variables["nValidTrackerHits"][0] = event.tracks_nValidTrackerHits[iCand]
            tmva_variables["nMissingOuterHits"][0] = event.tracks_nMissingOuterHits[iCand]
            tmva_variables["ptErrOverPt2"][0] = ptErrOverPt2

            if is_pixel_track:
                mva = readerPixelOnly.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelonly:
                    is_disappearing_track = True

            elif is_tracker_track:
                mva = readerPixelStrips.EvaluateMVA("BDT")
                if mva>bdt_cut_pixelstrips:
                    is_disappearing_track = True

            # apply baseline DT selection:
            if is_disappearing_track and not isBaselineTrack(event.tracks[iCand], iCand, event, mask):
                if verbose: print "Failed baseline DT selection"
                is_disappearing_track = False

            # check if actual fake track (no genparticle in cone around track):
            charged_genparticle_in_track_cone = False
            is_prompt_bg = False
            is_tau_bg = False
            if is_disappearing_track and tree.GetBranch("GenParticles"):
                for k in range(len(event.GenParticles)):

                    if charged_genparticle_in_track_cone: break

                    deltaR = event.tracks[iCand].DeltaR(event.GenParticles[k])
                    if deltaR < 0.02:
                           
                        gen_track_cone_pdgid = abs(event.GenParticles_PdgId[k])
                        if (gen_track_cone_pdgid == 11 or gen_track_cone_pdgid == 13) and event.GenParticles_Status[k] == 1:
                            charged_genparticle_in_track_cone = True
                            is_prompt_bg = True
                            break
                        elif gen_track_cone_pdgid == 15 and tree.GetBranch("GenTaus_LeadTrk"):
                            # if genTau, check if the track matches with a GenTaus_LeadTrk track:
                            for l in range(len(event.GenTaus_LeadTrk)):
                                deltaR = event.tracks[iCand].DeltaR(event.GenTaus_LeadTrk[l])
                                if deltaR < 0.02:
                                    print "That's a tau leading track"
                                    charged_genparticle_in_track_cone = True
                                    is_tau_bg = True
                                    break
                
            if is_disappearing_track:
               
                n_DT += 1
                if not charged_genparticle_in_track_cone:
                    n_DT_actualfake += 1
                #print "found a fake DT! event", iEv, is_pixel_track
                #else:
                #    print "found a prompt DT! event", iEv, is_pixel_track

                # save track-level properties:
                tree_branch_values["DT%i_is_pixel_track" % n_DT][0] = is_pixel_track
                tree_branch_values["DT%i_pixelLayersWithMeasurement" % n_DT][0] = event.tracks_pixelLayersWithMeasurement[iCand]
                tree_branch_values["DT%i_trackerLayersWithMeasurement" % n_DT][0] = event.tracks_trackerLayersWithMeasurement[iCand]
                tree_branch_values["DT%i_actualfake" % n_DT][0] = not charged_genparticle_in_track_cone
                tree_branch_values["DT%i_nMissingInnerHits" % n_DT][0] = event.tracks_nMissingInnerHits[iCand]
                tree_branch_values["DT%i_nMissingMiddleHits" % n_DT][0] = event.tracks_nMissingMiddleHits[iCand]
                tree_branch_values["DT%i_nMissingOuterHits" % n_DT][0] = event.tracks_nMissingOuterHits[iCand]
                tree_branch_values["DT%i_trackQualityHighPurity" % n_DT][0] = bool(event.tracks_trackQualityHighPurity[iCand])
                tree_branch_values["DT%i_nValidPixelHits" % n_DT][0] = event.tracks_nValidPixelHits[iCand]
                tree_branch_values["DT%i_nValidTrackerHits" % n_DT][0] = event.tracks_nValidTrackerHits[iCand]
                tree_branch_values["DT%i_dxyVtx" % n_DT][0] = event.tracks_dxyVtx[iCand]
                tree_branch_values["DT%i_dzVtx" % n_DT][0] = event.tracks_dzVtx[iCand]
                tree_branch_values["DT%i_matchedCaloEnergy" % n_DT][0] = event.tracks_matchedCaloEnergy[iCand]
                tree_branch_values["DT%i_trkRelIso" % n_DT][0] = event.tracks_trkRelIso[iCand]
                tree_branch_values["DT%i_ptErrOverPt2" % n_DT][0] = ptErrOverPt2
                tree_branch_values["DT%i_mva" % n_DT][0] = mva
                tree_branch_values["DT%i_pt" % n_DT][0] = event.tracks[iCand].Pt()
                tree_branch_values["DT%i_eta" % n_DT][0] = event.tracks[iCand].Eta()
                tree_branch_values["DT%i_phi" % n_DT][0] = event.tracks[iCand].Phi()
                tree_branch_values["DT%i_promptbg" % n_DT][0] = is_prompt_bg
                tree_branch_values["DT%i_taubg" % n_DT][0] = is_tau_bg                

                if verbose:
                    print "**************** DT track info ****************"
                    print "file =", current_file_name
                    print "event =", iEv
                    for item in tree_branch_values:
                        if "DT%i" % n_DT in item:
                           print "%s = %s" % (item, tree_branch_values[item][0])
                    print "***********************************************"

                # for each DT, check if in HEM failure region:
                if event.RunNum >= 319077:
                    if -3.0<event.tracks[iCand].Eta() and event.tracks[iCand].Eta()<-1.4 and -1.57<event.tracks[iCand].Phi() and event.tracks[iCand].Phi()<-0.87:
                        tree_branch_values["DT%i_hemfailure" % n_DT][0] = 1
                        tree_branch_values["hemfailure_dt"][0] = 1


        # check HEM failure for electrons and jets:
        def GetHighestHemObjectPt(particles):
            highestPt = 0
            for particle in particles:
                if -3.0<particle.Eta() and particle.Eta()<-1.4 and -1.57<particle.Phi() and particle.Phi()<-0.87:
                    if particle.Pt()>highestPt:
                        highestPt = particle.Pt()
            return highestPt

        if event.RunNum >= 319077:
            if GetHighestHemObjectPt(event.Jets) > 30:
                tree_branch_values["hemfailure_jet"][0] = 1
            if GetHighestHemObjectPt(event.Electrons) > 10:
                tree_branch_values["hemfailure_electron"][0] = 1


        if region_signalcontrol:

            # check signal/control region bin:
            if n_DT > 0:
                is_pixel_track = tree_branch_values["DT1_is_pixel_track"][0]
                region = get_signal_region(event, MinDeltaPhiMhtJets, n_DT, is_pixel_track)
                tree_branch_values["region"][0] = region
            elif n_DT == 0:
                region_noDT = get_signal_region(event, MinDeltaPhiMhtJets, 1, False)
                if region_noDT > 0:
                    tree_branch_values["region_noDT"][0] = region_noDT
                    tree_branch_values["region_noDT_ext"][0] = region_noDT + 15
                region_noDT_multiple = get_signal_region(event, MinDeltaPhiMhtJets, 2, False)
                if region_noDT_multiple > 0:
                    tree_branch_values["region_noDT_ext2"][0] = region_noDT_multiple

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

            # fill all fakerate branches:      
            for variable in fakerate_variables:
                for fr_region in fakerate_regions:
                    if fr_region == "dilepton":
                        variable = variable.replace("HT", "HT_cleaned")
                    else:
                        variable = variable.replace("_cleaned", "")
                        
                    if is_pixel_track:
                        category = "short"
                    else:
                        category = "long"
                        
                    hist_name = fr_region + "/" + data_period + "/" + category + "/fakerate_" + variable.replace(":", "_")
                    
                    try:                 
                        if ":" in variable:
                            xvalue = eval("event.%s" % variable.replace("n_allvertices", "nAllVertices").replace("_cleaned", "").replace("n_NVtx", "NVtx").split(":")[1])
                            yvalue = eval("event.%s" % variable.replace("n_allvertices", "nAllVertices").replace("_cleaned", "").replace("n_NVtx", "NVtx").split(":")[0])
                            FR = getBinContent_with_overflow_2D(h_fakerates[hist_name], xvalue, yvalue)
                        else:
                            value = eval("event.%s" % variable.replace("n_allvertices", "nAllVertices").replace("_cleaned", "").replace("n_NVtx", "NVtx"))
                            FR = getBinContent_with_overflow_1D(h_fakerates[hist_name], value)
                        
                        branch_name = "fakerate_%s_%s" % (fr_region, variable.replace(":", "_"))
                        tree_branch_values[branch_name][0] = FR
                    except:
                        pass

        # event-level variables:
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
     
        tout.Fill()
     
    fout.cd()

    if region_signalcontrol:
        fakerate_file.Close()
    if mask != "":
        mask_file.Close()

    fout.cd()
    fout.Write()

    fout.Close()

if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()
    
    iFile = args[0].split(",")
    out_tree = args[1]
    nev = int(args[2])
    region = int(args[3])

    if nev == 0:
        nev = -1

    region_fakerate = False
    region_signalcontrol = False
    if region == 0:
        region_fakerate = True
    elif region == 1:
        region_signalcontrol = True

    loop(iFile, out_tree, nevents = nev, region_fakerate = region_fakerate, region_signalcontrol = region_signalcontrol)

