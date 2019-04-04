#!/bin/env python
from __future__ import division
from array import array
from ROOT import *
import os, sys, glob
import math
import numpy as np
from optparse import OptionParser

# convert event level trees to track level trees, chi gen matching, MC stitching and custom variables
# original auther viktor.kutzner@desy.de

# run with e.g.
# ./convert_to_tracklevel.py /nfs/dust/cms/user/kutznerv/DisappTrksSignalMC/CMSSW10/TREEMAKER/g1800_chi1400_27_200970_step5_50TREEMAKER_979.root_RA2AnalysisTree.root test.root all

def pass_background_stitching(file_name, madHT):
    passed = True
    if "DYJetsToLL_M-50_TuneCUETP8M1" in file_name and madHT>100 or \
       "TTJets_TuneCUETP8M1" in file_name and madHT>600 or \
       "_HT-100to200_" in file_name and (madHT<100 or madHT>200) or \
       "_HT-200to400_" in file_name and (madHT<200 or madHT>400) or \
       "_HT-400to600_" in file_name and (madHT<400 or madHT>600) or \
       "_HT-600to800_" in file_name and (madHT<600 or madHT>800) or \
       "_HT-800to1200_" in file_name and (madHT<800 or madHT>1200) or \
       "_HT-1200to2500_" in file_name and (madHT<1200 or madHT>2500) or \
       "_HT-2500toInf_" in file_name and madHT<2500:
            passed = False

    return passed


def is_signal(file_name):
    if "g1800_chi" in file_name or "signal" in file_name:
        return True
    else:
        return False


def convert_chiCands_to_tracktree(event_tree_filename, track_tree_output, category = "all", nevents = -1, treename = "TreeMaker2/PreSelection", treename_out = "tracks"):

    # use TChain if wildcard present in event_tree_filename:
    
    if "*" in event_tree_filename:
        tree = TChain(treename)
        tree.Add(event_tree_filename)
    else:
        fin = TFile(event_tree_filename)

        # check input file
        if fin.IsZombie(): # or fin.TestBit(TFile.kRecovered):
            print "input not properly closed:", event_tree_filename
            fin.Close()
            return event_tree_filename

        tree = fin.Get(treename)        
    
    print "Input:\t\t", event_tree_filename
    print "Output:\t\t", track_tree_output
    print "Tree:\t\t", treename
    print "Chi matching:\t", is_signal(event_tree_filename)

    fout = TFile(track_tree_output, "recreate")
    tout = TTree(treename_out, "tout")

    # check if chiCands/tracks are available in tree
    tracks_branch_label = ""
    for branch in tree:
        try:
            if branch.chiCands: tracks_branch_label = "chiCands"
        except:
            pass

        try:
            if branch.tracks: tracks_branch_label = "tracks"
        except:
            pass

        break

    if tracks_branch_label == "":
        quit("No tracks...")
    else:
        print "tracks_branch_label", tracks_branch_label

    # get number of events
    hnev = TH1D("Nev", "Nev", 1, 0, 1)

    # get variables of tree
    variables = []
    for i in range(len(tree.GetListOfBranches())):
        label = tree.GetListOfBranches()[i].GetName()

        if "%s_" % tracks_branch_label in label:
            label = label.replace("%s_" % tracks_branch_label, "")

            # reduce variables for CMSDAS:
            # if "passExo" in label: continue
            # if "trackQuality" in label and label != "trackQualityHighPurity": continue

            variables.append(label)

    print "Using variables", variables

    # prepare output tree
    tout_output_values = {}

    for variable in variables:
        # check for integer variables
        if "trackQuality" not in variable and "pass" not in variable and "nMissing" not in variable and "nValid" not in variable and "LayersWithMeasurement" not in variable:
            tout_output_values[variable] = array( 'f', [ 0 ] )
            tout.Branch( variable, tout_output_values[variable], '%s/F' % variable )
        else:
            tout_output_values[variable] = array( 'i', [ 0 ] )
            tout.Branch( variable, tout_output_values[variable], '%s/I' % variable )

    # add more variables, filled later
    for variable in ["pt", "eta", "phi", "madHT", "HT", "MET", "Weight", "ptErrOverPt2", "chiCandGenMatchingDR", "LabXYcm", "MHT", "MinDeltaPhiMhtJets"]:
        tout_output_values[variable] = array( 'f', [ 0 ] )
        tout.Branch( variable, tout_output_values[variable], '%s/F' % variable )
    for variable in ["event", "njets", "btags"]:
        tout_output_values[variable] = array( 'i', [ 0 ] )
        tout.Branch( variable, tout_output_values[variable], '%s/I' % variable )

    n_tree = tree.GetEntries()

    # loop over events
    for iEv, event in enumerate(tree):

        if nevents>0 and iEv+1>int(nevents):
            print "finished"
            break
        if (iEv+1) % 100 == 0:
            print "Processing event %s / %s" % (iEv+1, n_tree)

        hnev.Fill(0.0)

        tout_output_values["event"][0] = iEv+1
        tout_output_values["madHT"][0] = event.madHT
        tout_output_values["HT"][0] = event.HT
        tout_output_values["MHT"][0] = event.MHT
        tout_output_values["MET"][0] = event.MET
        tout_output_values["Weight"][0] = event.Weight
        tout_output_values["njets"][0] = len(event.Jets)
        tout_output_values["btags"][0] = event.BTags

        if not pass_background_stitching(event_tree_filename, tout_output_values["madHT"][0]):
            continue

        # MinDeltaPhiMhtJets
        csv_b = 0.8484
        metvec = TLorentzVector()
        metvec.SetPtEtaPhiE(event.MET, 0, event.METPhi, event.MET)
        mhtvec = TLorentzVector()
        mhtvec.SetPtEtaPhiE(event.MHT, 0, event.MHTPhi, event.MHT)
        mindphi = 9999
        nj = 0
        nb = 0
        for ijet, jet in enumerate(event.Jets):
                if not (abs(jet.Eta())<5.0 and jet.Pt()>30): continue
                nj+=1
                if event.Jets_bDiscriminatorCSV[ijet]>csv_b: nb+=1
                if abs(jet.DeltaPhi(mhtvec))<mindphi:
                        mindphi = abs(jet.DeltaPhi(mhtvec))
        MinDeltaPhiMhtJets = mindphi
        tout_output_values["MinDeltaPhiMhtJets"][0] = MinDeltaPhiMhtJets

        # loop over chiCands
        number_of_ChiCands = len(eval("event.%s" % tracks_branch_label))
        for iCand in xrange(number_of_ChiCands):

            # track categorization:
            if category == "all":
                pass
            elif category == "short" and eval("""event.%s_trackerLayersWithMeasurement[%s] == event.%s_pixelLayersWithMeasurement[%s]""" % (tracks_branch_label, iCand, tracks_branch_label, iCand)):
                pass
            elif category == "medium" and eval("""event.%s_trackerLayersWithMeasurement[%s] > event.%s_pixelLayersWithMeasurement[%s]""" % (tracks_branch_label, iCand, tracks_branch_label, iCand)):
                pass
            else:
                continue

            # read variables from tree
            for variable in variables:

                try:
                    value = eval("""event.%s_%s[%s]""" % (tracks_branch_label, variable, iCand))
                   
                    if isinstance(value, float):
                        tout_output_values[variable][0] = float(value)
                    elif isinstance(value, int):
                        tout_output_values[variable][0] = int(value)
                    else:
                        if bool(value):
                            tout_output_values[variable][0] = 1
                        else:
                            tout_output_values[variable][0] = 0
                except:
                    hello = eval("""event.%s_%s[%s]""" % (tracks_branch_label, variable, iCand))
                    print "Error with", variable, hello

            for variable in ["pt"]:
                tout_output_values["pt"][0] = eval("event.%s[%s].Pt()" % (tracks_branch_label, iCand))
                tout_output_values["eta"][0] = eval("event.%s[%s].Eta()" % (tracks_branch_label, iCand))
                tout_output_values["phi"][0] = eval("event.%s[%s].Phi()" % (tracks_branch_label, iCand))
           
            # redo PF lepton veto and correct passPFCandVeto variable:
            passed_PF_lepton_veto = 1
            for leptons in [event.Electrons, event.Muons]:
                for lepton in leptons:
                    deltaR = eval("event.%s[%s].DeltaR(lepton)" % (tracks_branch_label, iCand))
                    if deltaR < 0.01:
                        passed_PF_lepton_veto = 0
                        break
            tout_output_values["passPFCandVeto"][0] = passed_PF_lepton_veto

            # custom variables:
            tout_output_values["ptErrOverPt2"][0] = tout_output_values["ptError"][0] / tout_output_values["pt"][0]**2

            if is_signal(event_tree_filename):

                # looking at signal

                if tree.GetBranch("GenParticles"):

                    matched = False

                    # chargino matching:
                    for k in range(len(event.GenParticles)):
                        if abs(event.GenParticles_PdgId[k]) == 1000024 and event.GenParticles_Status[k] == 1:
                            deltaR = eval("event.%s[%s].DeltaR(event.GenParticles[%s])" % (tracks_branch_label, iCand, k))
                            if deltaR < 0.001:
                                tout_output_values["chiCandGenMatchingDR"][0] = deltaR
                                matched = True
                                break

                    # chargino matching with GenParticlesGeant collection:
                    try:
                        for k in range(len(event.GenParticlesGeant)):
                            if abs(event.GenParticlesGeant_PdgId[k]) == 1000024 and event.GenParticlesGeant_Status[k] == 1:
                                new_deltaR = eval("event.%s[%s].DeltaR(event.GenParticlesGeant[%s])" % (tracks_branch_label, iCand, k))
                                if new_deltaR == deltaR:
                                    tout_output_values["LabXYcm"][0] = event.GenParticlesGeant_LabXYcm[k]
                                    break
                    except: pass

                    if matched:
                        print "matched"
                        tout.Fill()
 
            else:

                # background
                tout.Fill()

    hnev.Write()
    fout.Write()
    fout.Close()

    if "*" not in event_tree_filename:
        fin.Close()


if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()

    if len(args) == 2:
        convert_chiCands_to_tracktree(args[0], args[1])
    elif len(args) == 3:
        convert_chiCands_to_tracktree(args[0], args[1], category = args[2])
    elif len(args) == 4:
        convert_chiCands_to_tracktree(args[0], args[1], category = args[2], nevents = args[3])

