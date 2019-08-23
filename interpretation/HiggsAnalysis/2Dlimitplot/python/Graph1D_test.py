from ROOT import *
import sys
import numpy as np
from glob import glob
from utilitiesII import *
import math
#gROOT.SetBatch()
gROOT.SetStyle('Plain')



c1 = mkcanvas('1D graph')


#c1.SetFillColor( 42 )
c1.SetGrid()


#n = 20
x, y = array( 'd' ), array( 'd' )
z = array( 'd' )


mus = [[1800,1400,0.85],[1800,1000,0.9],[1800,400,0.95], [1900,1400,1], [1850,1200,0.99],[1950,1400,01.3], [2020,1400,01.5]]

n = len(mus)
for imu, mu in enumerate(mus):

   x.append(mu[0])
   y.append(mu[1])
   z.append(mu[2])
   print(' imu %imu %f %f %f ' % (imu,x[imu],y[imu],z[imu]))

#for i in range( n ):
 #  x.append( 0.1*i )
  # y.append( 10*math.sin( x[i]+0.2 ) )
   #z.append(0.1*i+5)
#   print(' i %i %f %f %f ' % (i,x[i],y[i],z[i]))


print x
print y



gr = TGraph2D( n, x, y, z )

gr.SetLineColor( 2 )
gr.SetLineWidth( 4 )
gr.SetMarkerColor( 4 )
gr.SetMarkerStyle( 21 )
gr.SetTitle( 'a simple graph' )
gr.GetXaxis().SetTitle( 'X title' )
gr.GetYaxis().SetTitle( 'Y title' )
gr.GetZaxis().SetTitle( 'z title' )
gr.Draw( 'colz' )


# TCanvas.Update() draws the frame, after which one can change it
c1.Update()

c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 12 )
c1.Modified()
pause()
c1.Update()

