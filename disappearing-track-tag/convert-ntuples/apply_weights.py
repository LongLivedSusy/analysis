#!/bin/env python
from __future__ import division
from array import array
from ROOT import *
import os, sys, glob
import math
import numpy as np
from optparse import OptionParser
import best_tmva_significance

# update tree with BDT values

# contains variables used for TMVA
tmva_variables = {}

# general set up training/spectator variables for TMVA
def prepareReader(xmlfilename, vars_training, vars_spectator):

    reader = TMVA.Reader()
    for label in vars_training + vars_spectator:
        if label not in tmva_variables:
            tmva_variables[label] = array('f',[0])

    for label in vars_training:
        reader.AddVariable(label, tmva_variables[label])
    for label in vars_spectator:
        reader.AddSpectator(label, tmva_variables[label])
    reader.BookMVA("BDT", xmlfilename)

    return reader


def update_tree(tree_filename, bdt_folder, treename = "PreSelection"):

    print "Update input tree with BDT weights"
    print "Tree:\t\t", tree_filename
    print "BDT folder:\t\t", bdt_folder

    fin = TFile(tree_filename, "update")
    tree = fin.Get(treename)

    # get variables of tree
    variables = []
    for i in range(len(tree.GetListOfBranches())):
        label = tree.GetListOfBranches()[i].GetName()
        variables.append(label)
    print "Available branches of input tree:\n", variables

    # initialize BDT
    bdt_bestcut = best_tmva_significance.get_get_bdt_cut_value(bdt_folder + '/output.root')["best_cut_value"]
    print "BDT cut with highest significance: BDT >", bdt_bestcut

    # get training and spectator variables:
    vars_training = []
    vars_spectator = []
    with open(bdt_folder + '/tmva.cxx') as f_macro:
        for line in f_macro:
            if "AddVariable" in line and "//" not in line:
                vars_training.append(line.split('"')[1])
            if "AddSpectator" in line and "//" not in line:
                vars_spectator.append(line.split('"')[1])

    print vars_training
    print vars_spectator

    tmvareader = prepareReader(bdt_folder + '/weights/TMVAClassification_BDT.weights.xml', vars_training, vars_spectator)
    bdt = array( 'f', [ 0 ] )
    branch = tree.Branch( "bdt", bdt, 'bdt/F' )

    entries = tree.GetEntries()
    
    # loop over tree entries:
    for iTrack, track in enumerate(tree):

        if iTrack % 2000 == 0:
            print "track %s / %s" % (iTrack, entries)

        for var in vars_training:
            tmva_variables[var][0] = eval("track.%s" % var)

        bdt[0] = tmvareader.EvaluateMVA("BDT")

        # fill BDT branches
        branch.Fill()

        # don't loop past all entries
        if iTrack+1 == entries: break

    fin.Write()
    fin.Close()


if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()

    if len(args) == 2:
        update_tree(args[0], args[1])
    else:
        print "Usage: ./apply_weights.py <input_tree.root> <bdt_folder>"


