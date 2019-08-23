#!/usr/bin/env python
import os, glob, sys, math
from array import array
from ROOT import *

import scipy.constants as scc
from utilitiesII import *
import fileinput
import datetime




def GetContours(g, color, style):
    contours = [1.0]
    g.GetHistogram().SetContour(1,array('d',contours));
    g.Draw("cont z list"); 
    contLevel = g.GetContourList(1.0);
    max_points = -1
    for cont in contLevel:
        n_points = cont.GetN()
        if n_points > max_points:
            max_points = n_points
            cont.SetLineColor(color)
            cont.SetLineStyle(style)
            cont.SetLineWidth(5)
            out = cont
        
            #cont.Draw("same")

    return out



def GetContoursSmooth(g, color, style, n_smooth  = 4):
    
    if(n_smooth>0):
        g2 = g.Clone()
        histo2d = g2.GetHistogram();
        htemp = TH2D("", "",
                     100, histo2d.GetXaxis().GetXmin(), histo2d.GetXaxis().GetXmax(),
                     100, histo2d.GetYaxis().GetXmin(), histo2d.GetYaxis().GetXmax());
        for binx in range(1,htemp.GetNbinsX()):
            x = htemp.GetXaxis().GetBinCenter(binx)
            for biny in range(1,htemp.GetNbinsY()):
                y = htemp.GetYaxis().GetBinCenter(biny)
                z = g2.Interpolate(x,y);
                if(z!=0.):
                    htemp.SetBinContent(htemp.GetBin(binx, biny), z)

        for ind in range(0,n_smooth):
            htemp.Smooth(1,"k5b");

    
        vx=[]; vy=[]; vz=[];
        glu_lsp = 225
        for binx in range(1,htemp.GetNbinsX()):
            x = htemp.GetXaxis().GetBinCenter(binx)
            for biny in range(1,htemp.GetNbinsY()):
                y = htemp.GetYaxis().GetBinCenter(biny);
                z = htemp.GetBinContent(htemp.GetBin(binx,biny));
        
                vx.append(x)
                vy.append(y)
                if ((x-y) > (glu_lsp+85)):
                   vz.append(z)
                else:
                    vz.append(g2.Interpolate(x,y));
        ax = array("d", vx) 
        ay = array("d", vy) 
        az = array("d", vz) 
        gsmooth =  TGraph2D ("gsmooth", "Cross-Section Limit", len(vx), ax, ay, az)
    else:
        gsmooth = g.Clone()

    contours = [1.0]
    gsmooth.GetHistogram().SetContour(1,array('d',contours));
    gsmooth.Draw("cont z list"); 
    contLevel = gsmooth.GetContourList(1.0);
    max_points = -1
    #find the contour with the most points
    outSM = TGraph()
    for i,cont in enumerate(contLevel):
        n_points = cont.GetN()
        if n_points > max_points:
            max_points = n_points
            outSM = cont

    #get the unsmoothed contour anyway for the last diagonal point
    contours = [1.0]
    g.GetHistogram().SetContour(1,array('d',contours));
    contLevel = g.GetContourList(1.0);
    max_points = -1
    outnSM = TGraph()
    #find the contour with the most points
    for i,cont in enumerate(contLevel):
        n_points = cont.GetN()
        if n_points > max_points:
            max_points = n_points
            outnSM = cont


    outnSM.SetLineColor(color)
    outnSM.SetLineStyle(style)
    outnSM.SetLineWidth(5)

    glu_lsp = 225
    #First: remove line above the diagonal    
    if n_smooth > 0:
        for point in range(0,outSM.GetN()):                                                                                                     
            mglu, mlsp = Double(0), Double(0)                                                                                                  
            outSM.GetPoint(point, mglu, mlsp);                                                                                                 
            if(mlsp > mglu-glu_lsp-5):                                                                                                          
                while(point <= outSM.GetN() and point!=0):                                                                                       
                    outSM.RemovePoint(outSM.GetN()-1)                                                                                        
    #Second:extend line down to LSP =0
#    outSM.Sort() #sorting doesn't really work
        endglu, endlsp = Double(0), Double(0)
        outSM.GetPoint(1, endglu, endlsp)
        outSM.SetPoint(1, endglu, 0)

    #Extend line on the diagonal
#        iniglu, inilsp = Double(0), Double(0)
       # outSM.GetPoint(outSM.GetN()-1, iniglu, inilsp)
       # outSM.SetPoint(outSM.GetN()-1, inilsp+225, inilsp)



    outSM.SetLineColor(color)
    outSM.SetLineStyle(style)
    outSM.SetLineWidth(5)
    return outSM

def getxsecGlu():
    xsecGlu = {} # dict for xsecs 
    xsecFile = "usefulthings/glu_xsecs_13TeV.txt"

    with open(xsecFile,"r") as xfile:                            
        lines = xfile.readlines() 
        print 'Found %i lines in %s' %(len(lines),xsecFile)
        for line in lines:
            if line[0] == '#': continue
            (mGo,xsec,err) = line.split()
            xsecGlu[int(mGo)] = (float(xsec),float(err))
            #print 'Importet', mGo, xsec, err, 'from', line 
    return xsecGlu

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    ## Create Yield Storage
    
#    pattern = "datacardsABCD_2p1bins_fullscan2"
#    os.chdir(pattern)
    dirList = glob.glob('T1tttt*')
    samples = [x[x.find('/')+1:] for x in dirList]    
    xsecGlu = getxsecGlu()
    if 1==1:
        fileList = glob.glob(pattern+'/limitOutput/*root')
        hexp = TH2F('hexp','hexp', 113,-12.5,2812.5, 113,-12.5,2812.5)
        hexpdown = TH2F('hexpdown','hexpdown', 113,-12.5,2812.5, 113,-12.5,2812.5)
        hexpup = TH2F('hexpup','hexpup', 113,-12.5,2812.5, 113,-12.5,2812.5)
        hobs = TH2F('hobs','hobs', 113,-12.5,2812.5, 113,-12.5,2812.5)
        vmx=[]; vmy = []; vxsec = []; vobs = [];  vobsup = []; vobsdown = []; vexp = []; vup = []; vdown = []; vlim = [];
        for x in fileList:
            print x
            mGo = int(x[x.find('_g')+2:x.find('_chi')])
            mLSP = int(x[x.find('_chi')+4:x.find('.As')])
            print 'mGo', mGo
            print 'mLSP', mLSP
            pause()
            f = TFile.Open(x, 'read')
            t = f.Get('limit')
            xsec = xsecGlu[mGo][0]
            theorySys = xsecGlu[mGo][1]
            #print theorySys
            rExp = 0
            rObs = 0
            rExp1SigmaDown = 0
            rExp1SigmaUp = 0
            factor = 1.0
            if mGo < 1400:
                factor = 100.0
            for entry in t:
                q = entry.quantileExpected
                if q == 0.5: rExp = entry.limit/factor
                if q == -1: rObs = entry.limit/factor
                if q < 0.4 and q > 0.14 : rExp1SigmaDown = entry.limit/factor
                if q < 0.14 : rExp2SigmaDown = entry.limit/factor
                if q > 0.6 and q < 0.9 : rExp1SigmaUp = entry.limit/factor
                if q > 0.9 : rExp2SigmaUp = entry.limit/factor

            hexp.Fill(mGo,mLSP,rExp)
            hexpdown.Fill(mGo,mLSP,rExp1SigmaDown)
            hexpup.Fill(mGo,mLSP,rExp1SigmaUp)
            hobs.Fill(mGo,mLSP,rObs)
            vmx.append(mGo)
            vmy.append(mLSP)
            vxsec.append(xsec)
            vlim.append(xsec * rObs)
            vobs.append(rObs)
            vobsup.append(rObs*(1+theorySys/100.0))
            vobsdown.append(rObs*(1-theorySys/100.0))
            vexp.append(rExp)
            vup.append(rExp1SigmaUp)
            vdown.append(rExp1SigmaDown)
            f.Close()

        hexp.SaveAs(pattern+'/testexp_'+pattern+'.root')
        hobs.SaveAs(pattern+'/testobs_'+pattern+'.root')
        aexp = array("d", vexp) 
        alim = array("d", vlim) 
        aup = array("d", vup) 
        adown = array("d", vdown) 
        aobs = array("d", vobs) 
        aobsup = array("d", vobsup) 
        aobsdown = array("d", vobsdown) 
        amx = array("d", vmx) 
        amy = array("d", vmy) 

        glim = TGraph2D("glim", "Cross-section limt", len(vlim), amx, amy, alim)
        gexp = TGraph2D("gexp", "Expected Limit", len(vexp), amx, amy, aexp)
        gup = TGraph2D("gup", "Expected Limit 1sigma up", len(vup), amx, amy, aup)
        gdown = TGraph2D("gdown", "Expected Limit 1sigma down", len(vdown), amx, amy, adown)
        gobs = TGraph2D("gobs", "Observed Limit", len(vobs), amx, amy, aobs)
        gobsup = TGraph2D("gobsup", "theory 1sigma up", len(vobsup), amx, amy, aobsup)
        gobsdown = TGraph2D("gobsdown", "theory 1sigma down", len(vobsdown), amx, amy, aobsdown)
        c = TCanvas("c","c",800,600)
        
        xmin = min(vmx)
        xmax = max(vmx)
        ymin = min(vmy)
        ymax = max(vmy)
        bin_size = 12.5;
        nxbins = max(1, min(500, (math.ceil((xmax-xmin)/bin_size))))
        nybins = max(1, min(500, (math.ceil((ymax-ymin)/bin_size))))
        glim.SetNpx(int(nxbins))
        glim.SetNpy(int(nybins))
        
        
        cexp = GetContoursSmooth(gexp, 2,1)
        cup = GetContoursSmooth(gup,2,2)
        cdown = GetContoursSmooth(gdown,2,2)
        cobs = GetContoursSmooth(gobs,1,1)
        cobsup = GetContoursSmooth(gobsup,1,2)
        cobsdown = GetContoursSmooth(gobsdown,1,2)

        hlim = glim.GetHistogram()
        hlim.SetTitle(";m_{gluino} [GeV];m_{LSP} [GeV]");
        hlim.Draw("colz")
        cexp.Draw("same")
        cup.Draw("same")
        cdown.Draw("same")
        cobs.Draw("same")
        cobsup.Draw("same")
        cobsdown.Draw("same")
        flimit = TFile(pattern+"/limit_scan.root","recreate")

        cobs.SetTitle("Observed Limit");
        cobsup.SetTitle("Observed -1#sigma Limit");
        cobsdown.SetTitle("Observed +1#sigma Limit");
        cexp.SetTitle("Expected  Limit");
        cup.SetTitle("Expected -1#sigma Limit");
        cdown.SetTitle("Expected +1#sigma Limit");


        hlim.Write("T1ttttObservedExcludedXsec");
        cobs.Write("T1ttttObservedLimit");
        cobsup.Write("T1ttttObservedLimitDown");
        cobsdown.Write("T1ttttObservedLimitUp");
        cexp.Write("T1ttttExpectedLimit");
        cup.Write("T1ttttExpectedLimitDown");
        cdown.Write("T1ttttExpectedLimitUp");

        c.SaveAs(pattern+'/canvas_'+pattern+'.root')


    
