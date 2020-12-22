import os, sys
from GridEngineTools import runParallel

def do_submission(commands, output_folder, condorDir = "condor", executable = "construct_sv_candidates_protons.py", runmode = "grid", dontCheckOnJobs=True, confirm=True):

    print "Submitting \033[1m%s jobs\033[0m, output folder will be \033[1m%s\033[0m." % (len(commands), output_folder)
    os.system("mkdir -p %s" % output_folder)
    os.system("cp %s %s/" % (executable, output_folder))
    return runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=False, confirm = confirm)


try: fname = sys.argv[1]
#except: fname = 'fileinfo/Run2016G_SingleElectron_only100.txt'
#except: fname = 'fileinfo/SingleElectron_Run2017E-17Nov2017-v1_AOD_only100.txt'
except: fname = 'fileinfo/SingleElectron_Run2017F-17Nov2017-v1_AOD_only100.txt'
#except: fname = 'fileinfo/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_only100.txt'
#except: fname = 'fileinfo/SMS-T1qqqq-LLChipm_ctau-200_mLSP-1100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt'
#except: fname = 'fileinfo/SMS-T2bt-LLChipm_ctau-200_mLSP-900.txt'
#except: fname = 'fileinfo/SMS-T2bt-LLChipm_ctau-200_mLSP-1000.txt'
#except: fname = 'fileinfo/filelistFastSim_higgsino94x_susyall_mChipm100GeV_dm0p16GeV_pu35.txt'
#except: fname = 'fileinfo/filelistSingleEl2016G_only30.txt'
#except: fname = 'fileinfo/filelistFastSim_higgsino94x_susyall.txt'
#except: fname = 'fileinfo/testfilelist.txt'
    
thefile = open(fname)
lines = thefile.readlines()
thefile.close()

output_folder = '/nfs/dust/cms/user/spak/DisappearingTracks/CMSSW_10_5_0/src/analysis/dedx/fwlite/EDM_output/'
if not os.path.exists(output_folder):
    os.system('mkdir -p '+output_folder)

commands=[]
for line in lines:
    if line.startswith('#') : continue	# skip commented line
    if not line.strip(): continue   # skip empty line
    rootfile = line.strip()
    #command = 'cmsRun construct_sv_candidates_protons.py root://cmsxrootd.fnal.gov/'+rootfile
    command = 'cmsRun construct_sv_candidates_protons.py root://xrootd-cms.infn.it/'+rootfile
    if 'higgsino' in rootfile or 'FastSim' in rootfile:
	command = 'cmsRun construct_sv_candidates_protons.py file://'+rootfile
    commands.append(command)
    print command
    #os.system(command)

#submit
#do_submission(commands, output_folder, condorDir='condor_Run2017F')
