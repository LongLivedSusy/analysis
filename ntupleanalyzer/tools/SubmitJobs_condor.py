import os, sys
from glob import glob
from random import shuffle 
from time import sleep

test = False

import argparse
parser = argparse.ArgumentParser()
defaultfkey = 'Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_28'
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultfkey,help="file")
parser.add_argument("-jersf", "--JerUpDown", type=str, default='Nom',help="JER scale factor (Nom, Up, ...)")
parser.add_argument("-dtmode", "--dtmode", type=str, default='PixAndStrips',help="PixAndStrips, PixOnly, PixOrStrips")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
parser.add_argument("-smearvar", "--smearvar", type=str, default='Nom',help="use gen-kappa")
parser.add_argument("-doprefire", "--doprefire", type=bool, default=False,help="apply pre-firing weights")
parser.add_argument("-ps", "--processskims", type=bool, default=False,help="use gen-kappa")
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
parser.add_argument("-outdir", "--outdir", type=str, default='output/smallchunks')
parser.add_argument("-targetctau", "--targetctau", type=int, default=-1)
args = parser.parse_args()
nfpj = args.nfpj
fnamekeyword = args.fnamekeyword.strip()
filenames = fnamekeyword
analyzer = args.analyzer
processskims = args.processskims
analyzer = analyzer.replace('python/','').replace('tools/','')
JerUpDown = args.JerUpDown
smearvar = args.smearvar
outdir = args.outdir
targetctau = args.targetctau


#try: 
moreargs = ' '.join(sys.argv)
moreargs = moreargs.split('--fnamekeyword')[-1]
moreargs = ' '.join(moreargs.split()[1:])

cachelocal = True
if 'Pure' in outdir: cachelocal = True

args4name = moreargs.replace(' ','').replace('--','-')


moreargs = moreargs.strip()
print 'moreargs', moreargs

if cachelocal:
    if not os.path.isdir(outdir): os.system('mkdir '+outdir)
else: 
    cachedir = '/pnfs/desy.de/cms/tier2/store/user/sbein/HistFragments/'+outdir
    print('working with cachedir', cachedir)
    if not os.path.isdir(cachedir):
        print('attempting to create', cachedir)
        os.system('gfal-mkdir "srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN='+cachedir+'"')
        os.system('sleep 0.3')
    if not os.path.isdir(cachedir):
        print('something went wrong', cachedir)
        exit(0)
        
cwd = os.getcwd()
filelist = glob(filenames)
#shuffle(filelist)

import subprocess
def get_active_jobs(username):
    process = subprocess.Popen(['condor_q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    result = stdout.decode('utf-8')
    sumline = result.strip().split("\n")[:-1][-1]
    try: njobs = float(sumline.split(' jobs;')[0].split('beinsam: ')[-1].strip())
    except: 
        print('failed to convert', sumline.split(' jobs;')[0].split('beinsam: ')[-1].strip())
        exit(0)
    if njobs>4500: print('nearing limit with njobs=',njobs)
    return njobs
    
filesperjob = nfpj

print 'len(filelist)', len(filelist)
print 'filesperjob', filesperjob

def main():
	ijob = 1
	files = ''
	jobcounter_ = 0
	for ifname, fname in enumerate(filelist):
		files += fname+','
		if (ifname)%filesperjob==0: jname = fname
		if (ifname)%filesperjob==filesperjob-1 or ifname==len(filelist)-1:
			jobname = analyzer.replace('.py','')+'_'+jname[jname.rfind('/')+1:]#.replace('.root','_'+str(ijob))
			if len(args4name.split())>0: 
				jobname = jobname+args4name.replace(' ','-').replace('---','-').replace('--','-')
			fjob = open('jobs/'+jobname+'.sh','w')
			files = files[:-1]#this just drops the comma
			fjob.write(jobscript.replace('CWD',cwd).replace('FNAMEKEYWORD',files).replace('ANALYZER',analyzer).replace('MOREARGS',moreargs).replace('JOBNAME',jobname).replace('OUTDIR',outdir))
			fjob.close()
			os.chdir('jobs')
			command = 'condor_qsub -cwd '+jobname+'.sh &'
			jobcounter_+=1
			print 'command', command
			if not test: 
			    while get_active_jobs('beinsam') >= 4990: 
			        os.system('sleep 0.1')
			        print ('sleeping, waiting for job on file', fname)
			    os.system(command)
			os.chdir('..')
			files = ''
			ijob+=1
			sleep(0.1)
			#import sys
			#print 'press the any key'
			#sys.stdout.flush() 
			#raw_input('')
	print 'submitted', jobcounter_, 'jobs'

if cachelocal: movecommand = 'mv OUTDIR/*.root CWD/OUTDIR'
else: movecommand = '''
for root_file in OUTDIR/*.root; do
    gfal_command="gfal-copy -n 1 file:////$PWD/$root_file davs://dcache-cms-webdav-wan.desy.de:2880//pnfs/desy.de/cms/tier2/store/user/sbein/HistFragments/OUTDIR/"
    echo $gfal_command
    $gfal_command
    if [ $? -eq 0 ]; then
        echo "Successfully copied $root_file"
    else
        echo "Error copying $root_file"
    fi
    rm $root_file
done
'''

jobscript = '''#!/bin/zsh
source /etc/profile.d/modules.sh
source /afs/desy.de/user/b/beinsam/.bash_profile
module use -a /afs/desy.de/group/cms/modulefiles/
export X509_USER_PROXY=CWD/x509up_u27836
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
echo doing a good old pwd:
pwd
python tools/ANALYZER --fnamekeyword FNAMEKEYWORD MOREARGS
echo listing OUTDIR
eval `scram unsetenv -sh`
MOVECOMMAND
ls OUTDIR/
cd ../
rm -rf $timestamp
'''.replace('MOVECOMMAND',movecommand)

main()
