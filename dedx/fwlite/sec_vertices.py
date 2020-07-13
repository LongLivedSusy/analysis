import DataFormats.FWLite as fwlite
import ROOT 
import math
import numpy as np
from commons import findMinDr_track, invariantMassTracks, findMatch_tracktrack_new, invariantMassTracksAsPions
import os,sys
from glob import glob
from shared_utils import *
#############################################
##    Looking at secondary vertices        ##
#############################################

#python tools/sec_vertices.py "edm_RunIISummer16DR80Premix*.root"
#python tools/sec_vertices.py "edm_Run2016G*.root"
    
try: 
    inputfiles = glob(sys.argv[1])
except: 
    inputfiles = glob("./EDM_output/edm_RunIISummer*.root")
    #inputfiles = glob("./EDM_output/edm_higgsino94x_susyall_mChipm250GeV*.root")
    #inputfiles = glob("./EDM_output/edm_Run2016G*.root")


if 'Run201' in inputfiles[0] or 'Single' in inputfiles[0] : 
	dedxcalib_barrel = Dedxcalibdict_Muon_barrel['Run2016G']
	dedxcalib_endcap = Dedxcalibdict_Muon_endcap['Run2016G']
else: 
	dedxcalib_barrel = 1
	dedxcalib_endcap = 1

print 'barrel, endcap calibs', dedxcalib_barrel, dedxcalib_endcap


events = fwlite.Events(inputfiles)


primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")
secondaryVertices_Lambda = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")
tracks_handle = fwlite.Handle("std::vector<reco::Track>")
protonIndices_handle = fwlite.Handle("std::vector<int>")

dEdxPixelTrackHandle = fwlite.Handle ("edm::ValueMap<reco::DeDxData>");
dEdxStripsTrackHandle = fwlite.Handle ("edm::ValueMap<reco::DeDxData>");
#label_dEdXtrack = 'dedxPixelHarmonic2'
#label_dEdXtrack = 'dedxHarmonic2'


tlegend = ROOT.TLegend(0.17, 0.77, 0.51, 0.88)

if not os.path.exists('./SV_rootfiles'):
    os.system('mkdir -p SV_rootfiles')

fnew = ROOT.TFile(inputfiles[0].replace('EDM_output','SV_rootfiles').replace('edm','vertex').replace('*',''), 'recreate')

# Primary
mass_primary = ROOT.TH1F("mass_primary", "primary vertex invariant mass; invariant mass [GeV];", 200, 0, 2) # invariant mass of all vertices

# Kshort
mass_highPurity = ROOT.TH1F("mass_highPurity", "Kshort mass", 1000, 0.4, 0.6)

# Lambda
P_Lambda = ROOT.TH1F("P_Lambda","Total momentum of Lambda",300,0,30)
P_good_Lambda = ROOT.TH1F("P_good_Lambda","Total momentum of Lambda",300,0,30)
P_good_Lambda_nodedx = ROOT.TH1F("P_good_Lambda_nodedx","Total momentum of Lambda",300,0,30)
P_good_Lambda_yesdedx = ROOT.TH1F("P_good_Lambda_yesdedx","Total momentum of Lambda",300,0,30)
pt_Lambda = ROOT.TH1F("pt_Lambda","Transverse momentum of Lambda",300,0,30)
pt_good_Lambda = ROOT.TH1F("pt_good_Lambda","Transverse momentum of Lambda",300,0,30)
pt_good_Lambda_nodedx = ROOT.TH1F("pt_good_Lambda_nodedx","Transverse momentum of Lambda",300,0,30)
pt_good_Lambda_yesdedx = ROOT.TH1F("pt_good_Lambda_yesdedx","Transverse momentum of Lambda",300,0,30)
eta_good_Lambda_nodedx = ROOT.TH1F("eta_good_Lambda_nodedx","Pseudorapidity of Lambda",100,-2.5,2.5)
eta_good_Lambda_yesdedx = ROOT.TH1F("eta_good_Lambda_yesdedx","Pseudorapidity of Lambda",100,-2.5,2.5)
mass_Lambda = ROOT.TH1F("mass_Lambda", "reconstructed #Lambda^{0} invariant mass; invariant mass [GeV]; no. of reconstructed SV", 1000, 1.08, 1.16) # invariant mass of all vertices
mass_good_Lambda = ROOT.TH1F("mass_good_Lambda", "invariant mass [GeV];no. of reconstructed SV;", 100,  1.11, 1.12) 
mass_good_Lambda_nodedx = ROOT.TH1F("mass_good_Lambda_nodedx", "invariant mass [GeV];no. of reconstructed SV;", 100,  1.11, 1.12) 
mass_good_Lambda_yesdedx = ROOT.TH1F("mass_good_Lambda_yesdedx", "invariant mass [GeV];no. of reconstructed SV;", 100,  1.11, 1.12) 
radialDistance_Lambda= ROOT.TH1F("radialDistance_Lambda", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
radialDistance_good_Lambda= ROOT.TH1F("radialDistance_good_Lambda", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
radialDistance_good_Lambda_nodedx= ROOT.TH1F("radialDistance_good_Lambda_nodedx", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
radialDistance_good_Lambda_yesdedx= ROOT.TH1F("radialDistance_good_Lambda_yesdedx", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
CosAngle = ROOT.TH1F("bestCosAngle","best cosine angle between displacement vector and Lambda momentum", 1000,0.99,1)
CosAngle_good_Lambda = ROOT.TH1F("bestCosAngle_good_Lambda","best cosine angle between displacement vector and Lambda momentum", 1000,0.99999,1)
CosAngle_good_Lambda_nodedx = ROOT.TH1F("bestCosAngle_good_Lambda_nodedx","best cosine angle between displacement vector and Lambda momentum", 1000,0.99999,1)
CosAngle_good_Lambda_yesdedx = ROOT.TH1F("bestCosAngle_good_Lambda_yesdedx","best cosine angle between displacement vector and Lambda momentum", 1000,0.99999,1)

# Proton
P_proton = ROOT.TH1F("P_proton","Total momentum[GeV]|proton",300,0,30)
P_good_proton = ROOT.TH1F("P_good_proton", "Total momentum[GeV]|proton;", 300, 0, 30) 
P_good_proton_nodedx = ROOT.TH1F("P_good_proton_nodedx", "Total momentum[GeV]|proton;", 300, 0, 30) 
P_good_proton_yesdedx = ROOT.TH1F("P_good_proton_yesdedx", "Total momentum[GeV]|proton;", 300, 0, 30) 

pt_proton = ROOT.TH1F("pt_proton","Transverse momentum[GeV]|proton",300,0,30)
pt_good_proton = ROOT.TH1F("pt_good_proton", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
pt_good_proton_nodedx = ROOT.TH1F("pt_good_proton_nodedx", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
pt_good_proton_yesdedx = ROOT.TH1F("pt_good_proton_yesdedx", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
eta_good_proton_nodedx = ROOT.TH1F("eta_good_proton_nodedx", "Pseudorapidity|proton;", 100,-2.5,2.5) 
eta_good_proton_yesdedx = ROOT.TH1F("eta_good_proton_yesdedx", "Pseudorapidity|proton;", 100, -2.5, 2.5) 

dedxpixel_proton = ROOT.TH1F("dedxpixel_proton", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_proton = ROOT.TH1F("dedxpixelCalib_proton", "Calibrated pixel dedx|proton;", 200, 0, 10) 
dedxstrips_proton = ROOT.TH1F("dedxstrips_proton", "strips dedx|proton;", 200, 0, 10) 

dedxpixel_good_proton = ROOT.TH1F("dedxpixel_good_proton", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_nodedx = ROOT.TH1F("dedxpixel_good_proton_nodedx", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_yesdedx = ROOT.TH1F("dedxpixel_good_proton_yesdedx", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton = ROOT.TH1F("dedxpixelCalib_good_proton", "Calibrated pixel dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton = ROOT.TH1F("dedxstrips_good_proton", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton_nodedx = ROOT.TH1F("dedxstrips_good_proton_nodedx", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton_yesdedx = ROOT.TH1F("dedxstrips_good_proton_yesdedx", "strips dedx|proton;", 200, 0, 10) 

massdedxpixel_proton = ROOT.TH1F("massdedxpixel_proton", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixelCalib_proton = ROOT.TH1F("massdedxpixelCalib_proton", "Calibrated pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_proton = ROOT.TH1F("massdedxstrips_proton", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 

massdedxpixel_good_proton = ROOT.TH1F("massdedxpixel_good_proton", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixel_good_proton_nodedx = ROOT.TH1F("massdedxpixel_good_proton_nodedx", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixel_good_proton_yesdedx = ROOT.TH1F("massdedxpixel_good_proton_yesdedx", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixelCalib_good_proton = ROOT.TH1F("massdedxpixelCalib_good_proton", "Calibrated pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_good_proton = ROOT.TH1F("massdedxstrips_good_proton", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_good_proton_nodedx = ROOT.TH1F("massdedxstrips_good_proton_nodedx", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_good_proton_yesdedx = ROOT.TH1F("massdedxstrips_good_proton_yesdedx", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 


rho_z_histogram = ROOT.TH2F("rho_z", "rho_z", 100, 0.0, 30.0, 100, 0.0, 10.0) # horizontal axis will represent z, the direction parallel to the beamline, and the vertical axis will represent rho, the distance from the beamline
hDeDxPixelVsP_proton = ROOT.TH2F("hDeDxPixelVsP_proton", "", 100, 0.0, 5, 100, 0.0, 11) 
hDeDxPixelCalibVsP_proton = ROOT.TH2F("hDeDxPixelCalibVsP_proton", "", 100, 0.0, 5, 100, 0.0, 11) 


#pt_good_Rando = ROOT.TH1F("pt_good_Rando", "radial distance 0.5 - 1.5 cm;transverse momentum[GeV];", 200, 0, 200) 
#massdedx_to1p5_Rando = ROOT.TH1F("massdedx_to1p5_Rando", "radial distance 0.5 - 1.5 cm;dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
#hDeDxVsP_Rando = ROOT.TH2F("hDeDxVsP_Rando", "", 100, 0.0, 5, 100, 0.0, 11) 

events.toBegin()
findMatch = 0
for i, event in enumerate(events):

    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    event.getByLabel("SecondaryVerticesFromHighPurityTracks", "Kshort", secondaryVertices)
    event.getByLabel("SecondaryVerticesFromHighPurityTracks", "Lambda", secondaryVertices_Lambda)
    event.getByLabel("SecondaryVerticesFromHighPurityTracks", "ProtonTrackIndices", protonIndices_handle)
    event.getByLabel("generalTracks", tracks_handle)
    event.getByLabel("dedxPixelHarmonic2", dEdxPixelTrackHandle)
    event.getByLabel("dedxHarmonic2", dEdxStripsTrackHandle)
    
    #print i,' th event pv:{}, sv:{}'.format(primaryVertices,secondaryVertices_Lambda)
    #print i,' th event len(pv.product):{} len(sv.product):{}'.format(len(primaryVertices.product()),len(secondaryVertices_Lambda.product()))

    #if i > 9999999: break
    if i > 100000: break
    #if i > 2000: break
    if i%1000==0:print 'passing {}th event'.format(i)
    #if i%1==0: print i, "   Secondary vertices per event:", secondaryVertices_Lambda.product().size()

    tracks = tracks_handle.product()
    dEdxPixelTrack = dEdxPixelTrackHandle.product()
    dEdxStripsTrack = dEdxStripsTrackHandle.product()
    protonIndices = protonIndices_handle.product()

    # particle mass from primary vertex		
    #for pv in primaryVertices.product():
	#mass_primary.Fill(pv.mass())
    
    # kShort
    for sv in secondaryVertices.product():
        mass_highPurity.Fill(sv.mass())	
    
    # Lambda loop		
    for j, secondary in enumerate(secondaryVertices_Lambda.product()):
        ## invariant mass of all vertices	
	P_Lambda.Fill(secondary.p())
	pt_Lambda.Fill(secondary.pt())
        mass_Lambda.Fill(secondary.mass())
	
	# compute displacement vectors and compare them with Lambda momentum vectors
        px = secondary.px()
        py = secondary.py()
        pz = secondary.pz()
        p = secondary.p()
        bestCosAngle = -1 
        radDis = -1
	
	for primary in primaryVertices.product():
            dx = secondary.vx() - primary.x()
            dy = secondary.vy() - primary.y()
            dz = secondary.vz() - primary.z()
            dl = math.sqrt(dx**2 + dy**2 + dz**2)
            dxy = math.sqrt(dx**2 + dy**2)
            #if i % 100 == 0: print "Normalized momentum:", px/p, py/p, pz/p,
            #if i % 100 == 0: print "Normalized displacement:", dx/dl, dy/dl, dz/dl
            dotProduct = px*dx + py*dy + pz*dz
	    if p==0 or dl==0 : continue
            cosAngle = dotProduct / p / dl
            if cosAngle > bestCosAngle:
                bestCosAngle = cosAngle # update it if you've found a better one
                radDis = dxy
	radialDistance_Lambda.Fill(radDis)
	CosAngle.Fill(bestCosAngle)

	# proton track and dEdx
        protonIdx = protonIndices[j]
        protrack = tracks[protonIdx]
        #if not protrack.charge()>0: continue
        
        P, pt, eta = protrack.p(),  protrack.pt(), protrack.eta()
	dedxpixel = dEdxPixelTrack.get(protonIdx).dEdx()
	dedxstrips = dEdxStripsTrack.get(protonIdx).dEdx()
	
	#massfromdedx = ROOT.TMath.Log10(ROOT.TMath.Sqrt((dedx-3.01)*pow(pt*ROOT.TMath.CosH(eta),2)/1.74))
        massfromdedxpixel = ROOT.TMath.Sqrt((dedxpixel-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)
        massfromdedxstrips = ROOT.TMath.Sqrt((dedxstrips-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)
	
	if abs(eta)<1.5: 
	    dedxpixelCalib = dedxcalib_barrel*dedxpixel
	    massfromdedxpixelCalib = ROOT.TMath.Sqrt((dedxpixelCalib-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)
        else: 
	    dedxpixelCalib = dedxcalib_endcap*dedxpixel
	    massfromdedxpixelCalib = ROOT.TMath.Sqrt((dedxpixelCalib-2.557)*pow(pt*ROOT.TMath.CosH(eta),2)/2.579)
                
	P_proton.Fill(protrack.p())
	pt_proton.Fill(protrack.pt())
	
	#print 'pdgid:',secondary.pdgId(), '\t number of daughters:',secondary.numberOfDaughters()
	#print 'secondary pT:%.2f \tsv daughter(0) pT:%.2f \tsv daughter(1) pT:%.2f \tproton pT:%.2f'%(secondary.pt(),secondary.daughter(0).pt(),secondary.daughter(1).pt(),protrack.pt())
	    
	# more tight selection
        if (radDis <= 2.1) and (radDis > 0.2) and abs(secondary.mass()-1.11604e+00)<2.13880e-03 and bestCosAngle > 0.999994:
            radialDistance_good_Lambda.Fill(radDis)
	    CosAngle_good_Lambda.Fill(bestCosAngle)
	    P_good_Lambda.Fill(secondary.p())
            pt_good_Lambda.Fill(secondary.pt())
            mass_good_Lambda.Fill(secondary.mass())
            P_good_proton.Fill(protrack.p())
            pt_good_proton.Fill(protrack.pt())
            dedxpixel_good_proton.Fill(dedxpixel)
            dedxstrips_good_proton.Fill(dedxstrips)
            massdedxpixel_good_proton.Fill(massfromdedxpixel)
            massdedxstrips_good_proton.Fill(massfromdedxstrips)
            
            #hDeDxPixelVsP_proton.Fill(protrack.p(),dedxpixel)
            #hDeDxPixelCalibVsP_proton.Fill(protrack.p(),dedxpixelCalib)
    	
	    #if dedxpixel==0 or dedxstrips==0 : # when there are no dedx 
	    if dedxpixel==0 : # when there are no dedx 
		radialDistance_good_Lambda_nodedx.Fill(radDis)
	    	CosAngle_good_Lambda_nodedx.Fill(bestCosAngle)
		P_good_Lambda_nodedx.Fill(secondary.p())
		pt_good_Lambda_nodedx.Fill(secondary.pt())
		eta_good_Lambda_nodedx.Fill(secondary.eta())
               	mass_good_Lambda_nodedx.Fill(secondary.mass())
               	P_good_proton_nodedx.Fill(protrack.p())
               	pt_good_proton_nodedx.Fill(protrack.pt())
               	eta_good_proton_nodedx.Fill(protrack.eta())
		dedxpixel_good_proton_nodedx.Fill(dedxpixel)
            	dedxstrips_good_proton_nodedx.Fill(dedxstrips)
            	massdedxpixel_good_proton_nodedx.Fill(massfromdedxpixel)
            	massdedxstrips_good_proton_nodedx.Fill(massfromdedxstrips)
	    
	    else :
		radialDistance_good_Lambda_yesdedx.Fill(radDis)
	    	CosAngle_good_Lambda_yesdedx.Fill(bestCosAngle)
	        P_good_Lambda_yesdedx.Fill(secondary.p())
	        pt_good_Lambda_yesdedx.Fill(secondary.pt())
	        eta_good_Lambda_yesdedx.Fill(secondary.eta())
	        mass_good_Lambda_yesdedx.Fill(secondary.mass())
	        P_good_proton_yesdedx.Fill(protrack.p())
	        pt_good_proton_yesdedx.Fill(protrack.pt())
	        eta_good_proton_yesdedx.Fill(protrack.eta())
		dedxpixel_good_proton_yesdedx.Fill(dedxpixel)
		dedxpixelCalib_good_proton.Fill(dedxpixelCalib)
            	dedxstrips_good_proton_yesdedx.Fill(dedxstrips)
            	massdedxpixel_good_proton_yesdedx.Fill(massfromdedxpixel)
	    	massdedxpixelCalib_good_proton.Fill(massfromdedxpixelCalib)
            	massdedxstrips_good_proton_yesdedx.Fill(massfromdedxstrips)

                    
                    
        #newj = protonIdx-1
        #if newj<0: newj = protonIdx+1
        #protrack2 = tracks[newj]
        #pt2, eta2 = protrack2.pt(), protrack2.eta()
        #dedx2 = 1.5*dEdxTrack.get(newj).dEdx()
        ##massfromdedx = ROOT.TMath.Log10(ROOT.TMath.Sqrt((dedx-3.01)*pow(pt*ROOT.TMath.CosH(eta),2)/1.74))
        #massfromdedx2 = ROOT.TMath.Sqrt((dedx2-2.557)*pow(pt2*ROOT.TMath.CosH(eta2),2)/2.579)        
	        #hDeDxVsP_Rando.Fill(protrack2.p(),dedx2)
	        #massdedx_to1p5_Rando.Fill(massfromdedx2)
	        #pt_to1p5_Rando.Fill(pt2)                    

fnew.cd()
fnew.Write()
print 'just created', fnew.GetName()
fnew.Close()
