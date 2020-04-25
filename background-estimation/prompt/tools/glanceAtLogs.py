from glob import glob


shlist = glob('jobs/*.sh')
elist_ = glob('jobs/*.sh.e*')
elist = []
for e in elist_: elist.append(e.split('.sh.e')[0]+'.sh.e')


for ish, shfile in enumerate(shlist):
    recoerr = shfile.replace('.sh','.sh.e')
    if not recoerr in elist:
        print ish, 'no error file matched:'
        print recoerr
