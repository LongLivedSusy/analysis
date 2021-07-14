#!/bin/usr/env python
from ROOT import *

if __name__=='__main__':
    print 'Calculating dE/dx smear factor'

    gaussigma={}
    smearfactor={}

    # Barrel
    gaussigma['Phase0']=0.598
    gaussigma['Phase1']=0.5026
    gaussigma['Summer16']=0.4661
    gaussigma['Fall17']=0.3759

    smearfactor['Phase0'] = TMath.Sqrt(gaussigma['Phase0']**2-gaussigma['Summer16']**2)
    smearfactor['Phase1'] = TMath.Sqrt(gaussigma['Phase1']**2-gaussigma['Fall17']**2)

    print '\'Phase0 barrel\':', round(smearfactor['Phase0'],3), ','
    print '\'Phase1 barrel\':', round(smearfactor['Phase1'],3), ','
