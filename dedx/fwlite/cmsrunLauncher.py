import os, sys
from glob import glob
#from GridEngineTools import runParallel
from GridEngineTools_mod import runParallel
def do_submission(commands, output_folder, condorDir = "condor", executable = "construct_sv_candidates_protons.py", runmode = "grid", dontCheckOnJobs=True, confirm=True):

    print "Submitting \033[1m%s jobs\033[0m, output folder will be \033[1m%s\033[0m." % (len(commands), output_folder)
    os.system("mkdir -p %s" % output_folder)
    os.system("mkdir -p %s" % condorDir)
    os.system("cp %s %s/" % (executable, condorDir))

    return runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=False, confirm = confirm, babysit=False)
    #return runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=False, confirm = confirm, babysit=False, use_sl6=True)


try: fname = sys.argv[1]
except: fname = 'fileinfo/Run2016B_SingleElectron-07Aug17_ver2-v2_AOD.txt'
#except: fname = 'fileinfo/Run2016G_SingleElectron-07Aug17-v1_AOD.txt'
#except: fname = 'fileinfo/Run2017F_SingleElectron-17Nov2017-v1_AOD.txt'
#except: fname = 'fileinfo/Run2018C_EGamma-17Sep2018-v1_AOD.txt'
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

#output_folder = './EDM_output_test/'
output_folder = './EDM_output_Run2016B_SingleElectron/'
#output_folder = './EDM_output_Run2016G_SingleElectron_more/'
#output_folder = './EDM_output_Run2017F_SingleElectron_more/'
#output_folder = './EDM_output_Run2018C_EGamma/'
if not os.path.exists(output_folder):
    os.system('mkdir -p '+output_folder)

condordir='condor_Run2016B'
#condordir='condor_Run2016G'
#condordir='condor_Run2017F'

commands=[]
for line in lines[:50]:
#for line in lines:
    if line.startswith('#') : continue	# skip commented line
    if not line.strip(): continue   # skip empty line
    rootfile = line.strip()
    #command = 'cmsRun construct_sv_candidates_protons.py root://xrootd-cms.infn.it/'+rootfile
    command = 'cmsRun construct_sv_candidates_protons.py root://xrootd-cms.infn.it/'+rootfile+' '+output_folder
    #command = 'cd ~/dust/DisappearingTracks/CMSSW_10_5_0/src/; eval `scramv1 runtime -sh`; cd -; cmsRun construct_sv_candidates_protons.py root://xrootd-cms.infn.it/'+rootfile+'; cp *.root '+output_folder
    if 'higgsino' in rootfile or 'FastSim' in rootfile:
	command = 'cmsRun construct_sv_candidates_protons.py file://'+rootfile
    commands.append(command)
    #print command
    #os.system(command)

#submit
do_submission(commands, output_folder, condorDir=condordir)
