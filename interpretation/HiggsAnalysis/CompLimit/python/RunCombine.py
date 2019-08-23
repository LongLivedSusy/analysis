from ROOT import *
import os, sys
from glob import glob
gStyle.SetOptStat(0)
gROOT.SetBatch(1)
from time import sleep
#from utils import *                                           
from utilitiesII import *

lumi = 35900.0
istest = False

try: inputflist = glob(sys.argv[1])
except: inputflist = glob('datacard*.txt')

print 'No key provided for datacard: running combine on all datacards'

if not os.path.exists("limitOutput"):
    print 'creating dir: limitOutput'
    os.system('mkdir limitOutput')

for inputname in inputflist:
    massPoint = inputname.split('datacard')[-1].split('LT10cm.txt')[0]
    command = 'combine -M AsymptoticLimits '+inputname+' --name '+ massPoint+'_10cm'+' --noFitAsimov' #' --run both' #+' --run blind'
    print command
    os.system(command)
#    pause()
    trans = 'mv *.AsymptoticLimits.mH120.root limitOutput/ '
    os.system(trans)
