import os, sys
from glob import glob
from random import shuffle 
from time import sleep

test = False

try: analyzer = sys.argv[1]
except: analyzer = 'SkimTreeMaker.py'
analyzer = analyzer.replace('python/','').replace('tools/','')
    
try: filenames = sys.argv[2]
#except: filenames = '/nfs/dust/cms/user/beinsam/CommonNtuples/MC_SM/*.root'
except: filenames = '/pnfs/desy.de/cms/tier2/store/user/sbein/CommonNtuples/Summer16.*.root'

try: otherargs = sys.argv[3:]
except: otherargs = ['']

cwd = os.getcwd()
filelist = glob(filenames)
shuffle(filelist)


filesperjob = 1

def main():
    ijob = 1
    files = ''
    for ifname, fname in enumerate(filelist):
        files += fname+','
        print fname
        if (ifname+1)%filesperjob==filesperjob-1:
            print '==='*3
            jobname = analyzer.replace('.py','')+'-'+fname[fname.rfind('/')+1:].replace('.root','_'+str(ijob))
            fjob = open('bird/'+jobname+'.sh','w')
            files = files[:-1]
            fjob.write(jobscript.replace('CWD',cwd).replace('INFILE',files).replace('ANALYZER',analyzer).replace('OTHERARGS',' '.join(otherargs)))
            fjob.close()
            os.chdir('bird')
            command = 'condor_qsub -cwd '+jobname+'.sh &'
            print command
            if not test: os.system(command)
            os.chdir('..')
            files = ''
            ijob+=1
            if test: break
            sleep(0.2)
        
jobscript = '''#!/bin/zsh
source /etc/profile.d/modules.sh
source /afs/desy.de/user/b/beinsam/.bash_profile
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
export THISDIR=$PWD
echo "$QUEUE $JOB $HOST"
source /afs/desy.de/user/b/beinsam/.bash_profile
cd CWD
cmsenv
cd $THISDIR
export timestamp=$(date +%Y%m%d_%H%M%S%N)
mkdir $timestamp
cd $timestamp
cp -r CWD/tools .
cp -r CWD/usefulthings .
python tools/ANALYZER "INFILE" OTHERARGS
mv *.root CWD/output/smallchunks
cd ../
rm -rf $timestamp

'''

main()
