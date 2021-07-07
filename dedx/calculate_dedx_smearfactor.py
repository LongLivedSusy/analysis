#!/bin/usr/env python
from ROOT import *

if __name__=='__main__':
    print 'Calculating dE/dx smear factor'

    gaussigma_barrel={}
    gaussigma_endcap={}
    smearfactor_barrel={}
    smearfactor_endcap={}

    # Barrel
    gaussigma_barrel['Phase0']=0.5973
    gaussigma_barrel['Phase1']=0.5368
    gaussigma_barrel['Summer16']=0.4451
    gaussigma_barrel['Fall17']=0.3515

    # Endcap
    gaussigma_endcap['Phase0']=0.4923
    gaussigma_endcap['Phase1']=0.4197
    gaussigma_endcap['Summer16']=0.4019
    gaussigma_endcap['Fall17']=0.3172

    smearfactor_barrel['Phase0'] = TMath.Sqrt(gaussigma_barrel['Phase0']**2-gaussigma_barrel['Summer16']**2)
    smearfactor_endcap['Phase0'] = TMath.Sqrt(gaussigma_endcap['Phase0']**2-gaussigma_endcap['Summer16']**2)
    smearfactor_barrel['Phase1'] = TMath.Sqrt(gaussigma_barrel['Phase1']**2-gaussigma_barrel['Fall17']**2)
    smearfactor_endcap['Phase1'] = TMath.Sqrt(gaussigma_endcap['Phase1']**2-gaussigma_endcap['Fall17']**2)

    print '\'Phase0 barrel\':', round(smearfactor_barrel['Phase0'],3), ','
    print '\'Phase0 endcap\':', round(smearfactor_endcap['Phase0'],3), ','
    print '\'Phase1 barrel\':', round(smearfactor_barrel['Phase1'],3), ','
    print '\'Phase1 endcap\':', round(smearfactor_endcap['Phase1'],3), ','
