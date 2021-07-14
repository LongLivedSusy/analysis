#!/usr/bin/env python

if __name__=='__main__' :
    print 'Calculating dE/dx intercalibration scale factor'
    
    gausmean={}
    scalefactor={}
   
    # gaus fit mean
    gausmean['Summer16'] = 2.866
    gausmean['Fall17'] = 2.958
    
    gausmean['Run2016B'] = 2.434
    gausmean['Run2016G'] = 2.083
    
    gausmean['Run2017F'] = 2.515
    
    gausmean['Run2018C'] = 2.384
    
    # scale factor
    scalefactor['Summer16']=gausmean['Summer16']/gausmean['Summer16']
    scalefactor['Fall17']  =gausmean['Summer16']/gausmean['Fall17']
    scalefactor['Run2016B']=gausmean['Summer16']/gausmean['Run2016B']
    scalefactor['Run2016G']=gausmean['Summer16']/gausmean['Run2016G']

    scalefactor['Run2017F']=gausmean['Summer16']/gausmean['Run2017F']

    scalefactor['Run2018C']=gausmean['Summer16']/gausmean['Run2018C']

    print '=====Barrel====='
    print '# Run2016'
    print '\'Run2016B\':', round(scalefactor['Run2016B'],3), ','
    print '\'Run2016G\':', round(scalefactor['Run2016G'],3), ','
    print ''
    print '# Run2017'
    print '\'Run2017F\':', round(scalefactor['Run2017F'],3), ','
    print ''
    print '# Run2018'
    print '\'Run2018C\':', round(scalefactor['Run2018C'],3), ','
    print ''
    print '# Summer16 MC'
    print '\'Summer16\':', round(scalefactor['Summer16'],3), ','
    print ''
    print '# Fall17 MC'
    print '\'Fall17\':', round(scalefactor['Fall17'],3), ','
    print ''

