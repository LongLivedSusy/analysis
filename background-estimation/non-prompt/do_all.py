#!/bin/env python
import os
import check_jobs
import commands

# get fakerates + do predictions + plot everything in one go

do_fakerate = True
do_prediction = True
do_closure = True

if do_fakerate:
    print "Getting fakerate (configuration inside)..."
    os.system("rm -rf get_fakerate.condor")
    os.system("./get_fakerate.py --start")
    jobstats = check_jobs.get_info("get_fakerate.condor")
    if jobstats["percent_done"]<0.9:
        print "Need to resubmit some jobs...?"
        quit()
    os.system("mv fakerate.root fakerate.root.bak")
    os.system("./get_fakerate.py --hadd")

if do_prediction:
    print "Getting prediction (configuration inside)..."
    os.system("rm -rf get_prediction.condor")
    os.system("rm -rf next_prediction.bak; mv next_prediction next_prediction.bak")
    os.system("./get_prediction.py --start --input ../skims/current/ --prediction_folder next_prediction --jobs_per_file 40")
    jobstats = check_jobs.get_info("get_prediction.condor")
    if jobstats["percent_done"]<0.9:
        print "Need to resubmit some jobs...?"
        quit()

if do_closure:
    print "Merging predictions and plot..."
    os.system("rm prediction*.root")
    os.system("rm closure*.root")
    os.system("./get_closure.py --path next_prediction --hadd --pdf")
