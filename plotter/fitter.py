#!/usr/bin/env python

from ROOT import *

def fit_background(hBkg, outputdir, cut, variable, outputformat):
    
    # 1.Normal method
    #x = RooRealVar("x","Log10_track_mass",1.5,5.0)
    #mean = RooRealVar("mean","mean",3,0,5)
    #sigma = RooRealVar("sigma","sigma",0,-10,10)
    #gauss = RooGaussian("gauss","gauss",x,mean,sigma)
    #alpha = RooRealVar("alpha","alpha",3,-10,10)
    #expo = RooExponential("expo","expo",x,alpha)
    #
    #l = RooArgList(x)
    #dh = RooDataHist("dh","dh",l,h)
    #
    #result = expo.fitTo(dh, RooFit.Save(), RooFit.PrintLevel(-1))
    #result.Print()
    #
    #c = TCanvas("c","",800,600)
    #xframe = x.frame()
    #dh.plotOn(xframe)
    #expo.plotOn(xframe)
    #xframe.Draw()
    #c.SaveAs("result_fit.png")

    # 2. Workspace method
    w = RooWorkspace("w")
    w.factory("Exponential::bkg(x[3,1,4.5],alpha[3,-10,10])")
    pdf = w.pdf("bkg")
    
    x = w.var("x")
    l = RooArgList(x)
    dh = RooDataHist("dh","dh",l,hBkg)
    fitresult = pdf.fitTo(dh,RooFit.Save(),RooFit.PrintLevel(-1))
    fitresult.Print()
    
    c = TCanvas("c","",800,600)
    xframe = x.frame()
    dh.plotOn(xframe)
    pdf.plotOn(xframe)
    xframe.Draw()
    c.SetLogy()
    c.SaveAs("%s/%s/FitBkg_%s.%s" % (outputdir, cut, variable,outputformat))

def fit_signal(hSig, outputdir, cut, variable, outputformat):
    
    w = RooWorkspace("w")
    w.factory("Gaussian::sig(x[1.5,5.0],mean[2.2],sigma[3,-10,10])")
    pdf = w.pdf("sig")
    
    x = w.var("x")
    l = RooArgList(x)
    dh = RooDataHist("dh","dh",l,h)
    fitresult = pdf.fitTo(dh,RooFit.Range(2.2,5),RooFit.Save(),RooFit.PrintLevel(-1))
    fitresult.Print()
    
    c = TCanvas("c","",800,600)
    xframe = x.frame()
    dh.plotOn(xframe)
    pdf.plotOn(xframe)
    xframe.Draw()
    c.SetLogy()
    c.SaveAs("%s/%s/FitSig_%s.%s" % (outputdir, cut, variable,outputformat))
