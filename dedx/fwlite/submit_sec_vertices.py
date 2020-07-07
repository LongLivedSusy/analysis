import os, sys
from GridEngineTools import runParallel

samples_to_submit=[
	"'./EDM_output/edm_RunIISummer*.root'",
	"'./EDM_output/edm_higgsino94x_susyall_mChipm250GeV*.root'",
	"'./EDM_output/edm_Run2016G*.root'"
	]

commands=[]
for sample in samples_to_submit:
    command = 'python sec_vertices.py '+sample
    #commands.append(command)
    print command
    os.system(command)
