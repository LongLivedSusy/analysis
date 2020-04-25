from ROOT import *
from utils import *
import os, sys

try: 	
	f = TFile(sys.argv[1])
	print 'just opened', f.GetName(), 'as f'
except:
	print "we're ready to go"
	
