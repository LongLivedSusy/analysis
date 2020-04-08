#!/bin/env python
from __future__ import division
import glob
from ROOT import *
import uuid
import multiprocessing 

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
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
    tl.DrawLatex(xlab,0.915, ' Work in Progress')
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
    xthing = 0.6202
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.915,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())


def get_histogram_from_tree(tree, var, cutstring="", drawoptions="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, numevents=-1, add_overflow = False):

    hName = str(uuid.uuid1()).replace("-", "")

    canvas = TCanvas("c_" + hName)

    if not nBinsY:
        histo = TH1F(hName, hName, nBinsX, xmin, xmax)
    else:
        histo = TH2F(hName, hName, nBinsX, xmin, xmax, nBinsY, ymin, ymax)

    if numevents>0:
        tree.Draw("%s>>%s" % (var, hName), cutstring, drawoptions, numevents)
    else:
        tree.Draw("%s>>%s" % (var, hName), cutstring, drawoptions)

    # add overflow bin(s) for 1D and 2D histograms:
    if add_overflow:
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


def get_histogram_from_file(tree_files, tree_folder_name, variable, cutstring="1", scaling="", nBinsX=False, xmin=False, xmax=False, nBinsY=False, ymin=False, ymax=False, file_contains_histograms=False, numevents=-1):
    
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
            nev += h_nev.GetBinContent(1)
            fin.Close()

    tree = TChain(tree_folder_name)       
    for i, tree_file in enumerate(tree_files):
        if not tree_file in ignore_files:
            tree.Add(tree_file)

    ## xsection and puweight scaling:
    if not is_data:
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
    if not is_data:
        histo.Scale(1.0/nev)
        #print "Scaled with nev = ", nev
    return histo


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

    #print "Thread started..."

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
        
        #if "merged" not in path:
        #    identifier = "_".join(file_name.split("_")[:-3])
        #else:scaling
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

        all_histograms = []

        if threads != 1:
            if threads == -1:
                # start thread pool with half of all cores
                pool = multiprocessing.Pool(int(multiprocessing.cpu_count()*0.5))
            else:
                # start thread pool with specified number of cores
                pool = multiprocessing.Pool(threads)
            all_histograms = pool.map(get_histogram_from_file_wrapper, pool_args)       
           
            pool.close()

        else:
            # don't use multithreading
            for pool_arg in pool_args:
                all_histograms.append( get_histogram_from_file_wrapper(pool_arg) )

        for histogram in all_histograms:   
        
            if h_combined == 0:
                h_combined = histogram
            else:
                h_combined.Add(histogram)
        
    except Exception, error:    
        
        print str(error)
        quit()

    try:
        print "n_total=%s" % h_combined.GetEntries()
        return h_combined
    except:
        print "Empty histogram"
        return False

