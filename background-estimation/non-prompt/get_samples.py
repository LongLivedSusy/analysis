#!/bin/env python
import os, glob
from optparse import OptionParser

def get_samples(folder):
    samples = []
    for item in glob.glob(folder + "/*root"):
        sample_name = "_".join( item.split("/")[-1].split(".root")[0].split("_")[:-2] )
        samples.append(sample_name)

    samples = sorted(list(set(samples)))

    return samples


def get_userlist():

    # get list of users with NtupleHub at DESY:

    userlist = []
    hub_folders = glob.glob("/pnfs/desy.de/cms/tier2/store/user/*/NtupleHub/")
    for hub_folder in hub_folders:
        userlist.append(hub_folder.split("/")[-3])

    return userlist


if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()
    folders = []
    if len(args) > 0:
        for folder in args:
            folders.append(folder)

    else:
        print "Getting all samples from all users..."
      
        #for user in get_userlist():

    for folder in folders:
        for item in get_samples(folder):
            print '"' + item + '",'

