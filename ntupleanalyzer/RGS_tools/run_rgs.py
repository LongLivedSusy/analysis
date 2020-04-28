#!/usr/bin/env python

import sys, os
from glob import glob

def maketable(Cut):
    print ("making table")
    txts = sorted(glob("LLSUSY_RGSOutput/result_*_%s.txt" %(Cut)))
    print txts
    with open ("LLSUSY_RGSOutput/table_%s.txt" %(Cut),"a") as ftable :
	for txt in txts :
    	    f = open(txt,"r")
    	    line = f.readline()
    	    ftable.write(line)
	ftable.write("==================================================\n")
    
def main():
    #Sigpoints = ["4_252033","5_448429","8_373637","10_374794","12_865833","13_547677","20_690321","22_237840","24_345416","27_969542","28_737434","37_569964_ctau250","37_569964_ctau750","44_855871","47_872207"]
    Sigpoints = ["4_252033","5_448429","8_373637","10_374794"]
    
    #Cuts = ["Mht_dPhi","Mht_Nj_dPhi","Mht_HT_dPhi","Mht_HT_Nb_dPhi","Mht_Nj_Nb_dPhi","Mht_Nj_Nl_dPhi"]
    Cuts = ["Mht_Nj_Nb_dPhi"]
    
    for Sigpoint in Sigpoints :
        for Cut in Cuts :
    	   os.system("python rgs_train.py %s %s" %(Sigpoint,Cut))
    	   os.system("python rgs_analysis.py %s %s" %(Sigpoint,Cut))
	   pass
    
    maketable("Mht_dPhi")
    maketable("Mht_Nj_dPhi")
    maketable("Mht_Nj_Nb_dPhi")
    maketable("Mht_Nj_Nl_dPhi")
    maketable("Mht_HT_dPhi")
    maketable("Mht_HT_Nb_dPhi")


if __name__ == "__main__" :
    main()
