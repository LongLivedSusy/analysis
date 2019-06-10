#!/bin/env python
from __future__ import division
import glob
from ROOT import *
import uuid
import multiprocessing 
import os

#gROOT.SetBatch(True)
#gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()

# a collection of generic functions to retrieve a 1D or 2D histogram from a collection of files containing a TTree
# comments @ viktor.kutzner@desy.de

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

    # add underflow/overflow bin(s) for 1D and 2D histograms:
    if not nBinsY:
        underflow = histo.GetBinContent(0)
        overflowbin = histo.GetNbinsX()+1
        overflow = histo.GetBinContent(overflowbin)
        histo.AddBinContent(1, underflow)
        histo.AddBinContent((overflowbin-1), overflow)
    else:
	#FIXME (underflow/overflow for 2D hist)
        overflowbinX = histo.GetNbinsX()+1
        overflowbinY = histo.GetNbinsX()+1

        # read and set overflow x values:
        for x in range(0, binX-1):
            overflow_up = histo.GetBinContent(x, overflowbinY)
            overflowbin = histo.GetBin(x, overflowbinY-1)
            histo.SetBinContent(overflowbin, overflow_up)

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


def get_histogram_from_file(tree_files, tree_folder_name, variable, cutstring=False, scaling="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, file_contains_histograms=False, numevents=-1):

    tree = TChain(tree_folder_name)       
    for i, tree_file in enumerate(tree_files):
        tree.Add(tree_file)

    if "Run201" in tree_files[0]:
        is_data = True
    else:
        is_data = False

    # xsection and puweight scaling:
    if not is_data:
        cutstring = "(%s)*CrossSection*puWeight%s" % (cutstring, scaling)
    else:
        if scaling != "":
            cutstring = "(%s)*%s" % (cutstring, scaling)

    if numevents>0:
        print "Limiting to %s events" % numevents
        cutstring += " && Entry$<%s " % numevents


    if not nBinsY:
        histo = get_histogram_from_tree(tree, variable, cutstring=cutstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax)
    else:
        histo = get_histogram_from_tree(tree, variable, cutstring=cutstring, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax)

    # divide by number of total events in sample
    if not is_data:
        try:
            # check for nev histogram
            nev = 0
            for tree_file in tree_files:
                fin = TFile(tree_file)
                hnev = fin.Get("nev")
                nev += hnev.GetBinContent(1)
                fin.Close()
        except:
            # otherwise, take number of entries of tree
            print "## using tree.GetEntries() for weighting"
            nev = tree.GetEntries()

        if nev > 0:
            histo.Scale(1.0/nev)
   

    return histo

#FIXME
#def get_eventlist(tree_files,cutstring):
#   
#    print 'get eventlist tree_file:%s, cut:%s'%(tree_files,cutstring)
#    os.system('mkdir -p eventlist')
#    # TEventList
#    tree.Draw(">>myList", cutstring)
#    evlist = gDirectory.Get("myList")
#    evlistout = TFile("evlistout.root","recreate")
#    evlist.Write()


def get_histogram_from_file_wrapper(args):

    tree_files = args[0]
    tree_folder_name  = args[1]
    variable = args[2]
    nBinsX = args[3]
    xmin = args[4]
    xmax = args[5]
    nBinsY = args[6]
    ymin = args[7]
    ymax = args[8]
    cutstring = args[9]
    scaling = args[10]
    numevents = args[11]

    print "Thread started..."

    #eventlist = get_eventlist(tree_files,cutstring)

    histogram = get_histogram_from_file(tree_files, tree_folder_name, variable, cutstring=cutstring, scaling=scaling, nBinsX=nBinsX, xmin=xmin, xmax=xmax, nBinsY=nBinsY, ymin=ymin, ymax=ymax, file_contains_histograms=False, numevents=numevents)

    unique = str(uuid.uuid1())
    histogram.SetDirectory(0)
    histogram.SetName(unique)

    return histogram 


def get_histogram(variable, cutstring, tree_folder_name="Events", scaling="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, path="./output_tautrack", selected_sample = "Run2016", numevents=-1, threads=-1):

    print "[multithreaded] Getting histogram for %s, cut = %s" % (variable, cutstring)

    unique = str(uuid.uuid1())
    
    histograms = {}
    h_combined = 0
    file_names = glob.glob(path + "/*root")
    
    samples = []
    for file_name in file_names:
        
        if "merged" not in path:
            identifier = "_".join(file_name.split("_")[:-3])
        else:
            identifier = file_name.replace(".root", "")
    
        selectors = selected_sample.split("*")
        count = 0
        for selector in selectors:

            if "|" in selector:
                for or_selector in selector.split("|"):
                    if or_selector in identifier:
                        count += 1
                        break
            elif selector in identifier:
                count += 1
        if count == len(selectors):
            samples.append(identifier)

    samples = list(set(samples))
    print "selected_sample:", selected_sample
    print "Found samples matching ''%s'':" % selected_sample, samples

    pool_args = []
    for i_sample, sample in enumerate(samples):

        filenames = glob.glob(sample + "*root")
        if not nBinsY:
            pool_args.append( [filenames, tree_folder_name, variable, nBinsX, xmin, xmax, False, False, False, cutstring, scaling, numevents] )
        else:
            pool_args.append( [filenames, tree_folder_name, variable, nBinsX, xmin, xmax, nBinsY, ymin, ymax, cutstring, scaling, numevents] )
    try:

        if threads == -1:
            pool = multiprocessing.Pool(int(multiprocessing.cpu_count()*0.5))
        else:
            pool = multiprocessing.Pool(threads)
        
        all_histograms = pool.map(get_histogram_from_file_wrapper, pool_args)
        
	for histogram in all_histograms:   
        
            if h_combined == 0:
                h_combined = histogram
            else:
                h_combined.Add(histogram)
        
        pool.close()
        
    except Exception, error:    
        
        print str(error)
        quit()

    return h_combined

def get_histograms_from_folder(folder, samples, variable, cutstring, nBinsX, xmin, xmax):

    histos = {}

    for label in samples:
        histos[label] = get_histogram(variable, cutstring, tree_folder_name="Events", nBinsX=nBinsX, xmin=xmin, xmax=xmax, path=folder, selected_sample=samples[label]["select"])

    return histos
