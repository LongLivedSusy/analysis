#!/bin/env python
from __future__ import division
import glob
from ROOT import *
import uuid

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

# a collection of generic functions to retrieve a 1D or 2D histogram from a collection of files containing a TTree

def stamp_plot():

    # from Sam:
    showlumi = False
    lumi = 150
    tl = TLatex()
    tl.SetNDC()
    cmsTextFont = 61
    extraTextFont = 52
    lumiTextSize = 0.6
    lumiTextOffset = 0.2
    cmsTextSize = 0.75
    cmsTextOffset = 0.1
    regularfont = 42
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(0.85*tl.GetTextSize())
    tl.DrawLatex(0.135,0.915, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(1.0/0.85*tl.GetTextSize())
    xlab = 0.213
    tl.DrawLatex(xlab,0.915, ' preliminary')
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
    xthing = 0.6202
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.915,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())


def get_histogram_from_tree(tree, var, cutstring="", drawoptions="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False):

    hName = str(uuid.uuid1()).replace("-", "")

    if not nBinsY:
        histo = TH1F(hName, hName, nBinsX, xmin, xmax)
    else:
        histo = TH2F(hName, hName, nBinsX, xmin, xmax, nBinsY, ymin, ymax)

    tree.Draw("%s>>%s" % (var, hName), cutstring, drawoptions)

    # add overflow bin(s) for 1D and 2D histograms:
    if not nBinsY:
        bin = histo.GetNbinsX()+1
        overflow = histo.GetBinContent(bin)
        histo.AddBinContent((bin-1), overflow)
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


def get_histogram_from_file(tree_files, tree_folder_name, variable, cutstring=False, scaling="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, file_contains_histograms=False, is_data=False):

    tree = TChain(tree_folder_name)       
    for tree_file in tree_files:
        tree.Add(tree_file)

    # xsection and puweight scaling:
    if not is_data:
        cutstring = "(%s)*CrossSection*puWeight%s" % (cutstring, scaling)
    elif len(scaling)>0:
        cutstring = "(%s)%s" % (cutstring, scaling)

    if not nBinsY:
        histo = get_histogram_from_tree(tree, variable, cutstring=cutstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax)
    else:
        histo = get_histogram_from_tree(tree, variable, cutstring=cutstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)

    # divide by number of total events in sample
    if not is_data:
        nev = 0
        for tree_file in tree_files:
            fin = TFile(tree_file)
            hnev = fin.Get("nev")
            nev += hnev.GetBinContent(1)
            fin.Close()
        if nev > 0:
            histo.Scale(1.0/nev)

    return histo


def get_histogram(variable, cutstring, scaling="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, path="./output_tautrack", is_data=False, selected_sample = "Run2016"):

    print "Getting histogram for %s, cut = %s (sample: %s)" % (variable, cutstring, selected_sample)

    if "Run201" in selected_sample:
        is_data = True
    else:
        is_data = False

    unique = str(uuid.uuid1())
    
    histograms = {}
    h_combined = 0
    file_names = glob.glob(path + "/*root")
    
    samples = []
    for file_name in file_names:
        identifier = "_".join(file_name.split("_")[:-3])
    
        selectors = selected_sample.split("*")
        count = 0
        for selector in selectors:
            if selector in identifier:
                count += 1
        if count == len(selectors):
            samples.append(identifier)
            
    samples = list(set(samples))

    for sample in samples:

        filenames = glob.glob(sample + "*root")

        if not nBinsY:
            histogram = get_histogram_from_file(filenames, "Events", variable, nBinsX=nBinsX, xmin=xmin, xmax=xmax, cutstring=cutstring, is_data=is_data, scaling=scaling).Clone()
        else:
            histogram = get_histogram_from_file(filenames, "Events", variable, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, cutstring=cutstring, is_data=is_data, scaling=scaling).Clone()

        histogram.SetDirectory(0)
        histogram.SetName(unique)
               
        if h_combined == 0:
            h_combined = histogram
        else:
            h_combined.Add(histogram)

    return h_combined

