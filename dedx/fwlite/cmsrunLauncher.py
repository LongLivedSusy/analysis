import os, sys
from GridEngineTools import runParallel

def do_submission(commands, output_folder, condorDir = "condor", executable = "construct_sv_candidates_protons.py", runmode = "grid", dontCheckOnJobs=True, confirm=True):

    print "Submitting \033[1m%s jobs\033[0m, output folder will be \033[1m%s\033[0m." % (len(commands), output_folder)
    os.system("mkdir -p %s" % output_folder)
    os.system("cp %s %s/" % (executable, output_folder))
    return runParallel(commands, runmode, condorDir=condorDir, dontCheckOnJobs=dontCheckOnJobs, use_more_mem=False, use_more_time=False, confirm = confirm)


try: fname = sys.argv[1]
except: fname = 'fileinfo/filelist_T2btFastSim.txt'
#except: fname = 'fileinfo/filelistFastSim_higgsino94x_susyall_mChipm100GeV_dm0p16GeV_pu35.txt'
#except: fname = 'fileinfo/filelistSingleEl2016G_only30.txt'
#except: fname = 'fileinfo/filelistFastSim_higgsino94x_susyall.txt'
#except: fname = 'fileinfo/testfilelist.txt'
    
thefile = open(fname)
lines = thefile.readlines()
thefile.close()

output_folder = './EDM_output/'
if not os.path.exists(output_folder):
    os.system('mkdir -p '+output_folder)

commands=[]
for line in lines:
    if line.startswith('#') : continue	# skip commented line
    if not line.strip(): continue   # skip empty line
    rootfile = line.strip()
    #command = 'cmsRun construct_sv_candidates_protons.py root://cmsxrootd.fnal.gov/'+rootfile
    #command = 'cmsRun construct_sv_candidates_protons.py root://xrootd-cms.infn.it/'+rootfile
    if 'higgsino' in rootfile or 'T2bt' in rootfile:
	command = 'cmsRun construct_sv_candidates_protons.py file://'+rootfile
    #command = 'python construct_sv_candidates_protons.py file://'+rootfile
    commands.append(command)
    print command

#os.system(commands[1])
#submit
do_submission(commands, output_folder, condorDir='condor')
