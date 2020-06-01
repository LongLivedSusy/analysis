import os, sys

try: fname = sys.argv[1]
#except: fname = 'fileinfo/filelistT2bt_only30.txt'
except: fname = 'fileinfo/filelistFastSim_higgsino94x_susyall_mChipm100GeV_dm0p16GeV_pu35.txt'
#except: fname = 'fileinfo/filelistSingleEl2016G_only30.txt'
#except: fname = 'fileinfo/testfilelist.txt'
    
thefile = open(fname)
lines = thefile.readlines()
thefile.close()

output_folder = 'EDM_output'
if not os.path.exists(output_folder) : 
    print 'Making output_folder : ', output_folder
    os.system('mkdir -p '+output_folder)

commands=[]
for line in lines:
    rootfile = line.strip()
    #command = 'cmsRun construct_sv_candidates_protons.py root://cmsxrootd.fnal.gov/'+rootfile+' '+output_folder
    command = 'cmsRun construct_sv_candidates_protons.py file://'+rootfile+' '+output_folder
    print command
    commands.append(command)
    os.system(command)

