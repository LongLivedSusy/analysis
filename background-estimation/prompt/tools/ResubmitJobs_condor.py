from glob import glob
import os, sys
from random import shuffle

def pause(str_='push enter key when ready'):
		import sys
		print str_
		sys.stdout.flush() 
		raw_input('')
		
		
#to move to 2017, to 2018, please see line 63, maybe +/- 5 by now (comment after line)
try: shkeys = str(sys.argv[1])
except: shkeys = 'jobs/*.sh'

istest = False


logfileversion = True
filecheckversion = True

shlist = glob(shkeys)
shuffle(shlist)
elist_ = glob(shkeys+'.e*')
elist = []
for e in elist_: elist.append(e.split('.sh.e')[0]+'.sh.e')

olist_ = glob(shkeys+'.o*')
olist = []
for o in olist_: olist.append(o.split('.sh.o')[0]+'.sh.o')
import commands

#shlist = sorted(shlist)
elist = sorted(elist)
olist = sorted(olist)

'''
for io, o in enumerate(olist):
	print io
	print 'fname attempt', o+'*'
	of = glob(o+'*')[0]
	os.system('tail '+of)
'''

listofmatchedfiles = []
for ish, shfile in enumerate(shlist):
	#print '=='*10, shfile
	noendgame = False
	nofilethere = False
	recoerr = shfile.replace('.sh','.sh.e')	
	if logfileversion:
		
		recoout = shfile.replace('.sh','.sh.o')
		fout = sorted(glob(recoout+'*'))
		lastoutlines = ''
		if len(fout)>0: 
			fout = fout[-1]
			lastoutlines =  commands.getstatusoutput('tail '+fout)
			noendgame = 'just created' not in lastoutlines[-1]
		else: noendgame = True
	if filecheckversion: 
		namechunk = shfile.split('/')[-1].replace('_RA2AnalysisTree','*').replace('.sh','').replace('.root','')
		#print 'namechunk', namechunk		
		inferredcodeproduct = '_'.join(namechunk.split('_')[0:-1]).split('With')[0].split('Maker')[0].split('yzer')[0]
		foutpiece = inferredcodeproduct+'_'+'_'.join(namechunk.split('Maker')[-1].split('With')[-1].split('_')[1:]).replace('Summer16.','*')#to move to 2017, to 2018, please stop replacing Summer16. here
		#print 'foutpiece', foutpiece
		keypiece = 'output/smallchunks/'+foutpiece
		keypiece = keypiece.replace('Anal','Hists')
		keypiece = keypiece.replace('Hist','Tree')
		foutlist = glob(keypiece+'*')
		nofilethere = len(foutlist)==0
		if nofilethere: print 'no file for glob("'+keypiece+'*'+'")', len(foutlist)	
	ferr = sorted(glob(recoerr+'*'))
	somethingmissing = False
	if len(ferr)>0:
		errf = open(ferr[-1])
		errtext = errf.read()
		errf.close()
		if 'does not exist' in errtext:
			somethingmissing = True
	#pause()					
	if (not recoerr in elist) or noendgame or somethingmissing or nofilethere:
		print 'resubmitting on grounds', (not recoerr in elist), noendgame, somethingmissing, nofilethere, shfile
		if filecheckversion: print 'searched file was', keypiece, glob(keypiece+'*')
		jobname = shfile.split('/')[-1].replace('.sh','')
		os.chdir('jobs')
		command = 'condor_qsub -cwd '+jobname+'.sh &'
		#print 'command', command
		if not istest: os.system(command)
		os.chdir('..')	
	else: print shfile, 'successfully completed'
	#pause()
	
#what happened with: 83 jobs/SimpleAnalyzer-Run2016C-17Jul2018-v1.METAOD_10000-7CFF4F11-529C-E711-BB57-A4BF01025568_RA2AnalysisTree_205--SmearLeps4Zed-False---nfpj-1
#?

#just created