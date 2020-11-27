import DataFormats.FWLite as fwlite
import ROOT 
import math
import numpy as np
#from commons import findMinDr_track, invariantMassTracks, findMatch_tracktrack_new, invariantMassTracksAsPions
import os,sys
from glob import glob
from shared_utils import *
#############################################
##    Looking at secondary vertices        ##
#############################################

ROOT.TH1.SetDefaultSumw2(True)
    
try: 
    inputfiles = glob(sys.argv[1])
except: 
    #inputfiles = glob("./EDM_output_merged/edm_Run2016G*.root")
    inputfiles = glob("./EDM_output_merged/edm_RunIISummer16DR80Premix_T2bt.root")
    #inputfiles = glob("./EDM_output_merged/edm_higgsino94x_susyall_mChipm250GeV*.root")
    #inputfiles = glob("./EDM_output_merged/edm_SUS-RunIISummer15GS-00734_T2btLLFastSim_*.root")
    #inputfiles = glob("./EDM_output_merged/edm_SUS-RunIISummer15GS-00734_T2btLLFastSim_NoPU_SVstuff.root")
    #inputfiles = glob("./EDM_output_merged/edm_SUS-RunIISummer15GS-00734_T2btLLFastSim_StandardMixing_SVstuff.root")


if 'Run201' in inputfiles[0] or 'Single' in inputfiles[0] : 
	dedxcalib_barrel = DedxCorr_Pixel_barrel['Run2016G']
	dedxcalib_endcap = DedxCorr_Pixel_endcap['Run2016G']
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

tlegend = ROOT.TLegend(0.17, 0.77, 0.51, 0.88)

if not os.path.exists('./SV_rootfiles'):
    os.system('mkdir -p SV_rootfiles')

fnew = ROOT.TFile('./SV_rootfiles/'+inputfiles[0].replace('EDM_output_merged','').replace('edm','vertex').replace('*',''), 'recreate')

# Primary
mass_primary = ROOT.TH1F("mass_primary", "primary vertex invariant mass; invariant mass [GeV];", 200, 0, 2) # invariant mass of all vertices

# Kshort
mass_highPurity = ROOT.TH1F("mass_highPurity", "Kshort mass", 1000, 0.4, 0.6)

# Lambda
P_Lambda = ROOT.TH1F("P_Lambda","Total momentum of Lambda",300,0,30)
P_good_Lambda = ROOT.TH1F("P_good_Lambda","Total momentum of Lambda",300,0,30)
P_good_Lambda_nodedx = ROOT.TH1F("P_good_Lambda_nodedx","Total momentum of Lambda",300,0,30)
P_good_Lambda_dedxexist = ROOT.TH1F("P_good_Lambda_dedxexist","Total momentum of Lambda",300,0,30)
pt_Lambda = ROOT.TH1F("pt_Lambda","Transverse momentum of Lambda",300,0,30)
pt_good_Lambda = ROOT.TH1F("pt_good_Lambda","Transverse momentum of Lambda",300,0,30)
pt_good_Lambda_nodedx = ROOT.TH1F("pt_good_Lambda_nodedx","Transverse momentum of Lambda",300,0,30)
pt_good_Lambda_dedxexist = ROOT.TH1F("pt_good_Lambda_dedxexist","Transverse momentum of Lambda",300,0,30)
eta_good_Lambda_nodedx = ROOT.TH1F("eta_good_Lambda_nodedx","Pseudorapidity of Lambda",100,-2.5,2.5)
eta_good_Lambda_dedxexist = ROOT.TH1F("eta_good_Lambda_dedxexist","Pseudorapidity of Lambda",100,-2.5,2.5)
mass_Lambda = ROOT.TH1F("mass_Lambda", "reconstructed #Lambda^{0} invariant mass; invariant mass [GeV]; no. of reconstructed SV", 1000, 1.08, 1.16) # invariant mass of all vertices
mass_good_Lambda = ROOT.TH1F("mass_good_Lambda", "invariant mass [GeV];no. of reconstructed SV;", 100,  1.11, 1.12) 
mass_good_Lambda_nodedx = ROOT.TH1F("mass_good_Lambda_nodedx", "invariant mass [GeV];no. of reconstructed SV;", 100,  1.11, 1.12) 
mass_good_Lambda_dedxexist = ROOT.TH1F("mass_good_Lambda_dedxexist", "invariant mass [GeV];no. of reconstructed SV;", 100,  1.11, 1.12) 
radialDistance_Lambda= ROOT.TH1F("radialDistance_Lambda", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
radialDistance_good_Lambda= ROOT.TH1F("radialDistance_good_Lambda", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
radialDistance_good_Lambda_nodedx= ROOT.TH1F("radialDistance_good_Lambda_nodedx", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
radialDistance_good_Lambda_dedxexist= ROOT.TH1F("radialDistance_good_Lambda_dedxexist", "#Lambda^{0} vertex radial distance; radial distance [cm]; no. of reconstructed SV", 1000,0.0, 20.0) 
CosAngle = ROOT.TH1F("bestCosAngle","best cosine angle between displacement vector and Lambda momentum", 1000,0.99,1)
CosAngle_good_Lambda = ROOT.TH1F("bestCosAngle_good_Lambda","best cosine angle between displacement vector and Lambda momentum", 1000,0.99999,1)
CosAngle_good_Lambda_nodedx = ROOT.TH1F("bestCosAngle_good_Lambda_nodedx","best cosine angle between displacement vector and Lambda momentum", 1000,0.99999,1)
CosAngle_good_Lambda_dedxexist = ROOT.TH1F("bestCosAngle_good_Lambda_dedxexist","best cosine angle between displacement vector and Lambda momentum", 1000,0.99999,1)

# Proton
P_proton = ROOT.TH1F("P_proton","Total momentum[GeV]|proton",300,0,30)
P_good_proton = ROOT.TH1F("P_good_proton", "Total momentum[GeV]|proton;", 300, 0, 30) 
P_good_proton_nodedx = ROOT.TH1F("P_good_proton_nodedx", "Total momentum[GeV]|proton;", 300, 0, 30) 
P_good_proton_dedxexist = ROOT.TH1F("P_good_proton_dedxexist", "Total momentum[GeV]|proton;", 300, 0, 30) 
P_good_proton_dedxexist_barrel = ROOT.TH1F("P_good_proton_dedxexist_barrel", "Total momentum[GeV]|proton;", 300, 0, 30) 
P_good_proton_dedxexist_endcap = ROOT.TH1F("P_good_proton_dedxexist_endcap", "Total momentum[GeV]|proton;", 300, 0, 30) 

pt_proton = ROOT.TH1F("pt_proton","Transverse momentum[GeV]|proton",300,0,30)
pt_good_proton = ROOT.TH1F("pt_good_proton", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
pt_good_proton_nodedx = ROOT.TH1F("pt_good_proton_nodedx", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
pt_good_proton_dedxexist = ROOT.TH1F("pt_good_proton_dedxexist", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
pt_good_proton_dedxexist_barrel = ROOT.TH1F("pt_good_proton_dedxexist_barrel", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
pt_good_proton_dedxexist_endcap = ROOT.TH1F("pt_good_proton_dedxexist_endcap", "Transverse momentum[GeV]|proton;", 300, 0, 30) 
eta_good_proton_nodedx = ROOT.TH1F("eta_good_proton_nodedx", "Pseudorapidity|proton;", 100,-2.5,2.5) 
eta_good_proton_dedxexist = ROOT.TH1F("eta_good_proton_dedxexist", "Pseudorapidity|proton;", 100, -2.5, 2.5) 

dedxpixel_proton = ROOT.TH1F("dedxpixel_proton", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_proton = ROOT.TH1F("dedxpixelCalib_proton", "Calibrated pixel dedx|proton;", 200, 0, 10) 
dedxstrips_proton = ROOT.TH1F("dedxstrips_proton", "strips dedx|proton;", 200, 0, 10) 

dedxpixel_good_proton = ROOT.TH1F("dedxpixel_good_proton", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_nodedx = ROOT.TH1F("dedxpixel_good_proton_nodedx", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_dedxexist = ROOT.TH1F("dedxpixel_good_proton_dedxexist", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_dedxexist_P0to5 = ROOT.TH1F("dedxpixel_good_proton_dedxexist_P0to5", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_dedxexist_P5toInf = ROOT.TH1F("dedxpixel_good_proton_dedxexist_P5toInf", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_dedxexist_barrel = ROOT.TH1F("dedxpixel_good_proton_dedxexist_barrel", "pixel dedx|proton;", 200, 0, 10) 
dedxpixel_good_proton_dedxexist_endcap = ROOT.TH1F("dedxpixel_good_proton_dedxexist_endcap", "pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_dedxexist = ROOT.TH1F("dedxpixelCalib_good_proton_dedxexist", "Calibrated pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_dedxexist_P0to5 = ROOT.TH1F("dedxpixelCalib_good_proton_dedxexist_P0to5", "Calibrated pixel dedx|proton;", 200, 0, 10) 
dedxpixelCalib_good_proton_dedxexist_P5toInf = ROOT.TH1F("dedxpixelCalib_good_proton_dedxexist_P5toInf", "Calibrated pixel dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton = ROOT.TH1F("dedxstrips_good_proton", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton_nodedx = ROOT.TH1F("dedxstrips_good_proton_nodedx", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton_dedxexist = ROOT.TH1F("dedxstrips_good_proton_dedxexist", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton_dedxexist_barrel = ROOT.TH1F("dedxstrips_good_proton_dedxexist_barrel", "strips dedx|proton;", 200, 0, 10) 
dedxstrips_good_proton_dedxexist_endcap = ROOT.TH1F("dedxstrips_good_proton_dedxexist_endcap", "strips dedx|proton;", 200, 0, 10) 

massdedxpixel_proton = ROOT.TH1F("massdedxpixel_proton", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixelCalib_proton = ROOT.TH1F("massdedxpixelCalib_proton", "Calibrated pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_proton = ROOT.TH1F("massdedxstrips_proton", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 

massdedxpixel_good_proton = ROOT.TH1F("massdedxpixel_good_proton", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixel_good_proton_nodedx = ROOT.TH1F("massdedxpixel_good_proton_nodedx", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixel_good_proton_dedxexist = ROOT.TH1F("massdedxpixel_good_proton_dedxexist", "pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxpixelCalib_good_proton_dedxexist = ROOT.TH1F("massdedxpixelCalib_good_proton_dedxexist", "Calibrated pixel dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_good_proton = ROOT.TH1F("massdedxstrips_good_proton", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_good_proton_nodedx = ROOT.TH1F("massdedxstrips_good_proton_nodedx", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 
massdedxstrips_good_proton_dedxexist = ROOT.TH1F("massdedxstrips_good_proton_dedxexist", "strips dedx-derived mass [GeV];no. of reconstructed SV;", 200, 0, 10) 


rho_z_histogram = ROOT.TH2F("rho_z", "rho_z", 100, 0.0, 30.0, 100, 0.0, 10.0) # horizontal axis will represent z, the direction parallel to the beamline, and the vertical axis will represent rho, the distance from the beamline
h2_P_protonVsDeDxPixel = ROOT.TH2F("h2_P_protonVsDeDxPixel", "proton total momentum VS pixel dedx", 100, 0.0, 30, 100, 0.0, 5) 
h2_P_protonVsDeDxPixelCalib = ROOT.TH2F("h2_P_protonVsDeDxPixelCalib", "proton total momentum VS calibrated pixel dedx", 100, 0.0, 30, 100, 0.0, 5) 
h2_P_protonVsDeDxStrips = ROOT.TH2F("h2_P_protonVsDeDxStrips", "proton total momentum VS strip dedx", 100, 0.0, 30, 100, 0.0, 5) 


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

    if i > 9999999: break
    #if i > 500000: break
    #if i > 2000: break
    
    if i%1000==0:print 'passing {}th event'.format(i)
    #if i%1==0: print i, "   Primary vertices per event:", primaryVertices.product().size()
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
        if (radDis > 0.2) and (radDis <= 2.1) and abs(secondary.mass()-1.11604e+00)<2.13880e-03 and bestCosAngle > 0.999994 and abs(protrack.eta()) < 2.4:
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
            
            h2_P_protonVsDeDxPixel.Fill(protrack.p(),dedxpixel)
            h2_P_protonVsDeDxPixelCalib.Fill(protrack.p(),dedxpixelCalib)
            h2_P_protonVsDeDxStrips.Fill(protrack.p(),dedxstrips)
    	
	    if dedxpixel>0 and dedxstrips>0 : 
		print 'both pixel/strips dedx exist'
		radialDistance_good_Lambda_dedxexist.Fill(radDis)
	    	CosAngle_good_Lambda_dedxexist.Fill(bestCosAngle)
	        P_good_Lambda_dedxexist.Fill(secondary.p())
	        pt_good_Lambda_dedxexist.Fill(secondary.pt())
	        eta_good_Lambda_dedxexist.Fill(secondary.eta())
	        mass_good_Lambda_dedxexist.Fill(secondary.mass())
	        P_good_proton_dedxexist.Fill(protrack.p())
	        pt_good_proton_dedxexist.Fill(protrack.pt())
	        eta_good_proton_dedxexist.Fill(protrack.eta())
		dedxpixel_good_proton_dedxexist.Fill(dedxpixel)
		dedxpixelCalib_good_proton_dedxexist.Fill(dedxpixelCalib)
		if protrack.p() < 5 : 
		    dedxpixel_good_proton_dedxexist_P0to5.Fill(dedxpixel)
		    dedxpixelCalib_good_proton_dedxexist_P0to5.Fill(dedxpixelCalib)
		if protrack.p() >=5 : 
		    dedxpixel_good_proton_dedxexist_P5toInf.Fill(dedxpixel)
		    dedxpixelCalib_good_proton_dedxexist_P5toInf.Fill(dedxpixelCalib)
            	dedxstrips_good_proton_dedxexist.Fill(dedxstrips)
            	massdedxpixel_good_proton_dedxexist.Fill(massfromdedxpixel)
	    	massdedxpixelCalib_good_proton_dedxexist.Fill(massfromdedxpixelCalib)
            	massdedxstrips_good_proton_dedxexist.Fill(massfromdedxstrips)
		if abs(protrack.eta()) < 1.5 :
		    P_good_proton_dedxexist_barrel.Fill(protrack.p())
	            pt_good_proton_dedxexist_barrel.Fill(protrack.pt())
		    dedxpixel_good_proton_dedxexist_barrel.Fill(dedxpixel)
		    dedxstrips_good_proton_dedxexist_barrel.Fill(dedxstrips)
		elif abs(protrack.eta()) >= 1.5 and abs(protrack.eta()) < 2.4 :
		    P_good_proton_dedxexist_endcap.Fill(protrack.p())
	            pt_good_proton_dedxexist_endcap.Fill(protrack.pt())
		    dedxpixel_good_proton_dedxexist_endcap.Fill(dedxpixel)
		    dedxstrips_good_proton_dedxexist_endcap.Fill(dedxstrips)
		else : print 'out of eta range, shouldnt see this message'
	    
	    elif dedxpixel==0 or dedxstrips==0 : # when there are no dedx 
		print 'dedx doesnt exist at least one of pixel or strips'
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

	    else : print 'What is this?'

fnew.cd()
fnew.Write()
print 'just created', fnew.GetName()
fnew.Close()
