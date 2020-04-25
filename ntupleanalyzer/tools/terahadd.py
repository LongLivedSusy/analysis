#!/bin/env python
import ROOT
from optparse import OptionParser

def merge(file_output, file_list):

    print "Merging", file_output

    print "Max tree size", ROOT.TTree.GetMaxTreeSize()
    ROOT.TTree.SetMaxTreeSize(500000000000) # 500 Gb
    print "Updated tree size", ROOT.TTree.GetMaxTreeSize()

    rm = ROOT.TFileMerger(False)
    rm.SetFastMethod(True)

    print "Input file list:",file_list
    print "Output file:",file_output

    for F in file_list:
        print "Adding ->",F
        rm.AddFile(F)
    rm.OutputFile(file_output)
    rm.Merge()

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-f", dest="overwrite", action="store_true")
    (options, args) = parser.parse_args()

    file_output = args[0]
    file_list = args[1:]

    merge(file_output, file_list)
