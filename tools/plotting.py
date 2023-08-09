#!/bin/env python
from __future__ import division
import glob
from ROOT import *
import uuid
import multiprocessing
from array import array

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

# a collection of generic functions to retrieve a 1D or 2D histogram from a collection of files containing a TTree
# comments @ viktor.kutzner@desy.de


def get_nMinus1_cuts(cuts, variable):
    
    #if variable not in cuts:
    #    return cuts
    
    position = -1
    for i_item, item in enumerate(cuts.split()):
        i_var = item.split(">=")[0].split("<=")[0].split(">")[0].split("<")[0].split("==")[0].split("!=")[0]
        if variable == i_var:
            position = i_item
            
    #print variable, ":", cuts, ":", position
    
    if position == -1:
        return cuts
    elif position == 0 and len(cuts.split()) == 1:
        return ""
    elif position == 0:
        return " ".join(cuts.split()[2:])
    elif position == len(cuts.split())-1:
        return " ".join(cuts.split()[:-2])
    else:
        return " ".join(cuts.split()[:position-1] + cuts.split()[position+1:]) 

def get_histogram_from_tree(tree, var, cutstring="", drawoptions="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, numevents=-1, add_overflow = True, nMinus1=False):

    if nMinus1:
        if ":" not in var:
            cutstring_corrected = get_nMinus1_cuts(cutstring, var)
        else:
            cutstring_corrected = get_nMinus1_cuts(cutstring, var.split(":")[0])
            cutstring_corrected = get_nMinus1_cuts(cutstring_corrected, var.split(":")[1])

        cutstring = cutstring_corrected

    hName = str(uuid.uuid1()).replace("-", "")

    canvas = TCanvas("c_" + hName)

    if not nBinsY:
        if isinstance(nBinsX, list):
            histo = TH1F(hName, hName, len(nBinsX) - 1, array('d', nBinsX) )                    
        else:
            histo = TH1F(hName, hName, nBinsX, xmin, xmax)
    else:
        if isinstance(nBinsX, list) and isinstance(nBinsY, list):
            histo = TH2F(hName, hName, len(nBinsX) - 1, array('d', nBinsX), len(nBinsY) - 1, array('d', nBinsY))
        elif isinstance(nBinsX, list):
            histo = TH2F(hName, hName, len(nBinsX) - 1, array('d', nBinsX), nBinsY, ymin, ymax)
        elif isinstance(nBinsY, list):
            histo = TH2F(hName, hName, nBinsX, xmin, xmax, len(nBinsY) - 1, array('d', nBinsY))
        else:
            histo = TH2F(hName, hName, nBinsX, xmin, xmax, nBinsY, ymin, ymax)

    if numevents>0:
        tree.Draw("%s>>%s" % (var, hName), cutstring, drawoptions, numevents)
    else:
        tree.Draw("%s>>%s" % (var, hName), cutstring, drawoptions)

    # add overflow bin(s) for 1D and 2D histograms:
    if add_overflow:
        if not nBinsY:
            jbin = histo.GetNbinsX()+1
            overflow = histo.GetBinContent(jbin)
            #histo.AddBinContent((jbin-1), overflow)
            histo.SetBinContent(jbin-1, histo.GetBinContent(jbin-1) + overflow)
        else:
            binX = histo.GetNbinsX()+1
            binY = histo.GetNbinsX()+1
        
            # read and set overflow x values:
            for x in range(0, binX-1):
                overflow_up = histo.GetBinContent(x, binY)
                bin = histo.GetBin(x, binY-1)
                histo.SetBinContent(bin, overflow_up)
        
            # read and set overflow y values:
            for y in range(0, binY-1):
                overflow_right = histo.GetBinContent(binX, y)
                bin = histo.GetBin(binX-1, y)
                histo.SetBinContent(bin, overflow_right)
        
            # read and set overflow diagonal values:
            overflow_diag = histo.GetBinContent(binX, binY)
            bin = histo.GetBin(binX-1, binY-1)
            histo.SetBinContent(bin, overflow_diag)
   
    histo.SetDirectory(0)
    return histo


def get_histogram_from_file(tree_files, tree_folder_name, variable, lowStats=False, cutstring="1", scaling="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, numevents=-1, unweighted=False, nMinus1=False):

    #print "tree_files", tree_files
    
    if "*" in tree_files:
        tree_files = glob.glob(tree_files)

    if lowStats and lowStats>0:
        print lowStats
        tree_files = tree_files[:lowStats]

    if not isinstance(tree_files, list):
        tree_files = [tree_files]
        
    if len(tree_files)==0:
        print "empty histogram..."
        if not nBinsY:
            if isinstance(nBinsX, list):
                return TH1F("empty", "empty", len(nBinsX) - 1, array('d', nBinsX) )                    
            else:
                return TH1F("empty", "emtpy", nBinsX, xmin, xmax)
        else:
            if isinstance(nBinsX, list) and isinstance(nBinsY, list):
                return TH2F("empty", "emtpy", len(nBinsX) - 1, array('d', nBinsX), len(nBinsY) - 1, array('d', nBinsY))
            else:
                return TH2F("empty", "emtpy", nBinsX, xmin, xmax, nBinsY, ymin, ymax)
                
    is_data = False
    if "Run201" in tree_files[0]:
        is_data = True      

    nev = 0
    ignore_files =  []
    for tree_file in tree_files:
        try:
            fin = TFile(tree_file)
            fin.Get("nev")
            fin.Get(tree_folder_name)
        except:
            fin.Close()
            "Ignoring file: %s" % tree_file
            ignore_files.append(ignore_files)
            print "Ignoring", tree_file
            continue

        if not is_data:
            #fin = TFile(tree_file)
            h_nev = fin.Get("nev")
            try:
                nev += h_nev.GetBinContent(1)
            except:
                pass
            fin.Close()


    tree = TChain(tree_folder_name)       
    for i, tree_file in enumerate(tree_files):
        if not tree_file in ignore_files:
            tree.Add(tree_file)

    if nMinus1:
        if ":" not in variable:
            cutstring_corrected = get_nMinus1_cuts(cutstring, variable)
        else:
            cutstring_corrected = get_nMinus1_cuts(cutstring, variable.split(":")[0])
            cutstring_corrected = get_nMinus1_cuts(cutstring_corrected, variable.split(":")[1])
        cutstring = cutstring_corrected
    
    ## xsection and puweight scaling:
    if not is_data and not unweighted:
        # MC
        if scaling != "":
            cutstring = "(%s)*CrossSection*puWeight*%s" % (cutstring, scaling)
        else:
            cutstring = "(%s)*CrossSection*puWeight" % (cutstring)
    else:
        # Data
        if scaling != "":
            cutstring = "(%s)*%s" % (cutstring, scaling)

    if numevents>0:
        print "Limiting to %s events" % numevents

    if not nBinsY:
        histo = get_histogram_from_tree(tree, variable, cutstring=cutstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax, numevents=numevents)
    else:
        histo = get_histogram_from_tree(tree, variable, cutstring=cutstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, numevents=numevents)

    #print "cutstring:", cutstring
    if not is_data and not unweighted and nev>0:
        histo.Scale(1.0/nev)
    return histo



        

def get_all_histos(tree_files, tree_folder_name, variable, lowStats=False, nMinus1=False, cutstring="1", scaling="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, numevents=-1, unweighted=False):

    if nMinus1:
        if ":" not in variable:
            cutstring_corrected = get_nMinus1_cuts(cutstring, variable)
        else:
            cutstring_corrected = get_nMinus1_cuts(cutstring, variable.split(":")[0])
            cutstring_corrected = get_nMinus1_cuts(cutstring_corrected, variable.split(":")[1])

        cutstring = cutstring_corrected

    if ":" in variable and not nBinsY:
        # symmetric 2D plot if no dedicated ranges are given
        nBinsY = nBinsX
        ymin = xmin
        ymax = xmax

    h_output = False
    for i, tree_file in enumerate(tree_files):
                
        h_tmp = get_histogram_from_file(tree_file, tree_folder_name, variable, lowStats=lowStats, cutstring=cutstring, scaling=scaling, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, numevents=numevents, unweighted=unweighted)    
        if not h_output:
            h_output = h_tmp
        else:
            h_output.Add(h_tmp)
    
    print "%s, N_ev=%s, Int()=%s" % (variable, h_output.GetEntries(), h_output.Integral())
    
    return h_output

