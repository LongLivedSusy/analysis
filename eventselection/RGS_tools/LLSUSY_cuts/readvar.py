#!/usr/bin/env python

import os, sys, re
from ROOT import *

NAME = 'LLSUSY_4_252033'

def main() :
    global cut 
    
    print "="*80
    print "\t=== SO1: find best staircase cuts ==="
    print "="*80
    
    treename = "RGS"
    #varfilename  = "%s.cuts" % NAME
    varfilename = "%s.cuts" %sys.argv[1]
    resultsfilename= "../../LLSUSY_RGSOutput/%s_%s.root" % (NAME,sys.argv[1])
    
    print "\n\topen RGS file: %s"  % resultsfilename
    
    f = TFile(resultsfilename)
    f.ls()
    t = f.Get(treename)
    
    leaves = []
    for leaf in t.GetListOfLeaves() :
        leaves.append(leaf.GetName())
    print leaves

    var =[]
    with open(varfilename) as fvar:
	for line in fvar:
	    if "#" in line:
		continue
	    var.append(line.split()[0])
	#print var

    commonvar=list(set(var).intersection(set(leaves)))
    print len(commonvar)

    n = t.leaf[1]

   
   
   
   
   
   
   
   
   
   
   # if commonvar :
   #     nj = t.NJets
   #     nb = t.BTags
        #with open ("LLSUSY_RGSOutput/%s.txt" %("result_"+sys.argv[1]+"_"+sys.argv[2]),"w") as flog :
        #    flog.write("%s  %.2f    %.2f    %.2f    %.2f    %.2f    %.2f\n" % (sys.argv[1],met,nj,nb,s,b,z))
    #elif "NJets" in leaves and "NLeptons" in leaves :
    #    nj = t.NJets
    #    nl = t.NLeptons
    #    with open ("LLSUSY_RGSOutput/%s.txt" %("result_"+sys.argv[1]+"_"+sys.argv[2]),"w") as flog :
    #        flog.write("%s  %.2f    %.2f    %.2f    %.2f    %.2f    %.2f\n" % (sys.argv[1],met,nj,nl,s,b,z))

#    if var in leaves : 
#	print("hahahah") 

if __name__ == "__main__" :
    main()
