#!/usr/bin/env python
import os, glob, sys, math
from array import array
from ROOT import *
import scipy.constants as scc
import fileinput
import datetime
import shared_utils
from optparse import OptionParser

# original code by Akshansh, adapted by Viktor

def myround(x, base=5):
    return int(base * round(float(x)/base))


def get_sbottom_antisbottom_cross_section(mass):

    # xsections in pb from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVstopsbottom

    xsections = {
        100: "0.177E+04 pm 6.77",
        105: "0.145E+04 pm 6.74",
        110: "0.120E+04 pm 6.71",
        115: "0.998E+03 pm 6.69",
        120: "0.832E+03 pm 6.67",
        125: "0.697E+03 pm 6.65",
        130: "0.586E+03 pm 6.63",
        135: "0.495E+03 pm 6.61",
        140: "0.419E+03 pm 6.59",
        145: "0.357E+03 pm 6.58",
        150: "0.304E+03 pm 6.57",
        155: "0.261E+03 pm 6.55",
        160: "0.224E+03 pm 6.54",
        165: "0.194E+03 pm 6.53",
        170: "0.168E+03 pm 6.52",
        175: "0.146E+03 pm 6.52",
        180: "0.127E+03 pm 6.51",
        185: "0.111E+03 pm 6.51",
        190: "0.973E+02 pm 6.5",
        195: "0.856E+02 pm 6.5",
        200: "0.755E+02 pm 6.5",
        205: "0.668E+02 pm 6.5",
        210: "0.593E+02 pm 6.5",
        215: "0.527E+02 pm 6.5",
        220: "0.470E+02 pm 6.5",
        225: "0.420E+02 pm 6.51",
        230: "0.377E+02 pm 6.51",
        235: "0.338E+02 pm 6.52",
        240: "0.305E+02 pm 6.52",
        245: "0.275E+02 pm 6.53",
        250: "0.248E+02 pm 6.54",
        255: "0.225E+02 pm 6.54",
        260: "0.204E+02 pm 6.55",
        265: "0.186E+02 pm 6.56",
        270: "0.169E+02 pm 6.57",
        275: "0.155E+02 pm 6.58",
        280: "0.141E+02 pm 6.6",
        285: "0.129E+02 pm 6.61",
        290: "0.119E+02 pm 6.62",
        295: "0.109E+02 pm 6.63",
        300: "0.100E+02 pm 6.65",
        305: "0.918E+01 pm 6.66",
        310: "0.843E+01 pm 6.67",
        315: "0.775E+01 pm 6.69",
        320: "0.713E+01 pm 6.7",
        325: "0.657E+01 pm 6.71",
        330: "0.606E+01 pm 6.73",
        335: "0.559E+01 pm 6.74",
        340: "0.517E+01 pm 6.76",
        345: "0.478E+01 pm 6.78",
        350: "0.443E+01 pm 6.79",
        355: "0.410E+01 pm 6.81",
        360: "0.381E+01 pm 6.83",
        365: "0.354E+01 pm 6.85",
        370: "0.329E+01 pm 6.87",
        375: "0.306E+01 pm 6.89",
        380: "0.285E+01 pm 6.91",
        385: "0.265E+01 pm 6.93",
        390: "0.247E+01 pm 6.95",
        395: "0.231E+01 pm 6.97",
        400: "0.215E+01 pm 6.99",
        405: "0.201E+01 pm 7.01",
        410: "0.188E+01 pm 7.04",
        415: "0.176E+01 pm 7.06",
        420: "0.164E+01 pm 7.09",
        425: "0.154E+01 pm 7.11",
        430: "0.144E+01 pm 7.14",
        435: "0.135E+01 pm 7.16",
        440: "0.126E+01 pm 7.19",
        445: "0.119E+01 pm 7.22",
        450: "0.111E+01 pm 7.25",
        455: "0.105E+01 pm 7.27",
        460: "0.983E+00 pm 7.3",
        465: "0.925E+00 pm 7.33",
        470: "0.870E+00 pm 7.36",
        475: "0.819E+00 pm 7.38",
        480: "0.771E+00 pm 7.41",
        485: "0.727E+00 pm 7.44",
        490: "0.685E+00 pm 7.47",
        495: "0.646E+00 pm 7.5",
        500: "0.609E+00 pm 7.53",
        505: "0.575E+00 pm 7.56",
        510: "0.543E+00 pm 7.58",
        515: "0.513E+00 pm 7.61",
        520: "0.484E+00 pm 7.64",
        525: "0.458E+00 pm 7.67",
        530: "0.433E+00 pm 7.7",
        535: "0.409E+00 pm 7.73",
        540: "0.387E+00 pm 7.75",
        545: "0.367E+00 pm 7.78",
        550: "0.347E+00 pm 7.81",
        555: "0.329E+00 pm 7.84",
        560: "0.312E+00 pm 7.87",
        565: "0.296E+00 pm 7.9",
        570: "0.280E+00 pm 7.93",
        575: "0.266E+00 pm 7.96",
        580: "0.252E+00 pm 7.99",
        585: "0.240E+00 pm 8.02",
        590: "0.228E+00 pm 8.05",
        595: "0.216E+00 pm 8.08",
        600: "0.205E+00 pm 8.12",
        605: "0.195E+00 pm 8.15",
        610: "0.186E+00 pm 8.18",
        615: "0.177E+00 pm 8.21",
        620: "0.168E+00 pm 8.25",
        625: "0.160E+00 pm 8.28",
        630: "0.152E+00 pm 8.31",
        635: "0.145E+00 pm 8.35",
        640: "0.138E+00 pm 8.38",
        645: "0.131E+00 pm 8.42",
        650: "0.125E+00 pm 8.45",
        655: "0.119E+00 pm 8.49",
        660: "0.114E+00 pm 8.52",
        665: "0.108E+00 pm 8.56",
        670: "0.103E+00 pm 8.59",
        675: "0.987E-01 pm 8.63",
        680: "0.942E-01 pm 8.66",
        685: "0.899E-01 pm 8.7",
        690: "0.858E-01 pm 8.73",
        695: "0.820E-01 pm 8.77",
        700: "0.783E-01 pm 8.8",
        705: "0.748E-01 pm 8.84",
        710: "0.715E-01 pm 8.88",
        715: "0.683E-01 pm 8.91",
        720: "0.653E-01 pm 8.95",
        725: "0.624E-01 pm 8.98",
        730: "0.597E-01 pm 9.02",
        735: "0.571E-01 pm 9.05",
        740: "0.546E-01 pm 9.09",
        745: "0.523E-01 pm 9.13",
        750: "0.500E-01 pm 9.16",
        755: "0.479E-01 pm 9.2",
        760: "0.459E-01 pm 9.24",
        765: "0.439E-01 pm 9.27",
        770: "0.421E-01 pm 9.31",
        775: "0.403E-01 pm 9.35",
        780: "0.386E-01 pm 9.38",
        785: "0.370E-01 pm 9.42",
        790: "0.355E-01 pm 9.46",
        795: "0.340E-01 pm 9.5",
        800: "0.326E-01 pm 9.53",
        805: "0.313E-01 pm 9.57",
        810: "0.300E-01 pm 9.61",
        815: "0.288E-01 pm 9.65",
        820: "0.276E-01 pm 9.69",
        825: "0.265E-01 pm 9.73",
        830: "0.254E-01 pm 9.77",
        835: "0.244E-01 pm 9.81",
        840: "0.234E-01 pm 9.85",
        845: "0.225E-01 pm 9.89",
        850: "0.216E-01 pm 9.93",
        855: "0.208E-01 pm 9.97",
        860: "0.199E-01 pm 10.01",
        865: "0.192E-01 pm 10.05",
        870: "0.184E-01 pm 10.09",
        875: "0.177E-01 pm 10.13",
        880: "0.170E-01 pm 10.17",
        885: "0.164E-01 pm 10.21",
        890: "0.157E-01 pm 10.25",
        895: "0.151E-01 pm 10.29",
        900: "0.145E-01 pm 10.33",
        905: "0.140E-01 pm 10.38",
        910: "0.135E-01 pm 10.42",
        915: "0.129E-01 pm 10.46",
        920: "0.125E-01 pm 10.5",
        925: "0.120E-01 pm 10.54",
        930: "0.115E-01 pm 10.59",
        935: "0.111E-01 pm 10.63",
        940: "0.107E-01 pm 10.67",
        945: "0.103E-01 pm 10.71",
        950: "0.991E-02 pm 10.76",
        955: "0.954E-02 pm 10.8",
        960: "0.919E-02 pm 10.84",
        965: "0.885E-02 pm 10.89",
        970: "0.853E-02 pm 10.93",
        975: "0.822E-02 pm 10.97",
        980: "0.792E-02 pm 11.02",
        985: "0.763E-02 pm 11.06",
        990: "0.735E-02 pm 11.11",
        995: "0.709E-02 pm 11.15",
        1000: "0.683E-02 pm 11.2",
        1005: "0.659E-02 pm 11.24",
        1010: "0.635E-02 pm 11.29",
        1015: "0.613E-02 pm 11.33",
        1020: "0.591E-02 pm 11.38",
        1025: "0.570E-02 pm 11.42",
        1030: "0.550E-02 pm 11.47",
        1035: "0.530E-02 pm 11.51",
        1040: "0.511E-02 pm 11.56",
        1045: "0.493E-02 pm 11.6",
        1050: "0.476E-02 pm 11.65",
        1055: "0.460E-02 pm 11.7",
        1060: "0.444E-02 pm 11.74",
        1065: "0.428E-02 pm 11.79",
        1070: "0.413E-02 pm 11.84",
        1075: "0.399E-02 pm 11.88",
        1080: "0.385E-02 pm 11.93",
        1085: "0.372E-02 pm 11.98",
        1090: "0.359E-02 pm 12.03",
        1095: "0.347E-02 pm 12.07",
        1100: "0.335E-02 pm 12.12",
        1105: "0.324E-02 pm 12.17",
        1110: "0.313E-02 pm 12.22",
        1115: "0.302E-02 pm 12.27",
        1120: "0.292E-02 pm 12.32",
        1125: "0.282E-02 pm 12.37",
        1130: "0.272E-02 pm 12.42",
        1135: "0.263E-02 pm 12.47",
        1140: "0.254E-02 pm 12.52",
        1145: "0.246E-02 pm 12.57",
        1150: "0.238E-02 pm 12.62",
        1155: "0.230E-02 pm 12.67",
        1160: "0.222E-02 pm 12.72",
        1165: "0.215E-02 pm 12.77",
        1170: "0.208E-02 pm 12.82",
        1175: "0.201E-02 pm 12.87",
        1180: "0.194E-02 pm 12.93",
        1185: "0.188E-02 pm 12.98",
        1190: "0.182E-02 pm 13.03",
        1195: "0.176E-02 pm 13.08",
        1200: "0.170E-02 pm 13.13",
        1205: "0.164E-02 pm 13.19",
        1210: "0.159E-02 pm 13.24",
        1215: "0.154E-02 pm 13.29",
        1220: "0.149E-02 pm 13.34",
        1225: "0.144E-02 pm 13.4",
        1230: "0.139E-02 pm 13.45",
        1235: "0.135E-02 pm 13.5",
        1240: "0.131E-02 pm 13.55",
        1245: "0.126E-02 pm 13.61",
        1250: "0.122E-02 pm 13.66",
        1255: "0.118E-02 pm 13.72",
        1260: "0.115E-02 pm 13.77",
        1265: "0.111E-02 pm 13.82",
        1270: "0.107E-02 pm 13.88",
        1275: "0.104E-02 pm 13.93",
        1280: "0.101E-02 pm 13.99",
        1285: "0.976E-03 pm 14.04",
        1290: "0.945E-03 pm 14.1",
        1295: "0.915E-03 pm 14.15",
        1300: "0.887E-03 pm 14.21",
        1305: "0.859E-03 pm 14.26",
        1310: "0.832E-03 pm 14.32",
        1315: "0.806E-03 pm 14.38",
        1320: "0.781E-03 pm 14.43",
        1325: "0.756E-03 pm 14.49",
        1330: "0.733E-03 pm 14.55",
        1335: "0.710E-03 pm 14.61",
        1340: "0.688E-03 pm 14.66",
        1345: "0.667E-03 pm 14.72",
        1350: "0.646E-03 pm 14.78",
        1355: "0.626E-03 pm 14.84",
        1360: "0.607E-03 pm 14.9",
        1365: "0.588E-03 pm 14.95",
        1370: "0.570E-03 pm 15.01",
        1375: "0.553E-03 pm 15.07",
        1380: "0.536E-03 pm 15.13",
        1385: "0.519E-03 pm 15.19",
        1390: "0.503E-03 pm 15.25",
        1395: "0.488E-03 pm 15.31",
        1400: "0.473E-03 pm 15.37",
        1405: "0.459E-03 pm 15.43",
        1410: "0.445E-03 pm 15.49",
        1415: "0.431E-03 pm 15.55",
        1420: "0.418E-03 pm 15.62",
        1425: "0.406E-03 pm 15.68",
        1430: "0.393E-03 pm 15.74",
        1435: "0.382E-03 pm 15.8",
        1440: "0.370E-03 pm 15.86",
        1445: "0.359E-03 pm 15.93",
        1450: "0.348E-03 pm 15.99",
        1455: "0.338E-03 pm 16.05",
        1460: "0.328E-03 pm 16.11",
        1465: "0.318E-03 pm 16.18",
        1470: "0.308E-03 pm 16.24",
        1475: "0.299E-03 pm 16.31",
        1480: "0.290E-03 pm 16.37",
        1485: "0.282E-03 pm 16.43",
        1490: "0.273E-03 pm 16.5",
        1495: "0.265E-03 pm 16.56",
        1500: "0.257E-03 pm 16.63",
        1505: "0.250E-03 pm 16.69",
        1510: "0.242E-03 pm 16.76",
        1515: "0.235E-03 pm 16.82",
        1520: "0.228E-03 pm 16.89",
        1525: "0.222E-03 pm 16.95",
        1530: "0.215E-03 pm 17.02",
        1535: "0.209E-03 pm 17.08",
        1540: "0.203E-03 pm 17.15",
        1545: "0.197E-03 pm 17.21",
        1550: "0.191E-03 pm 17.28",
        1555: "0.185E-03 pm 17.35",
        1560: "0.180E-03 pm 17.41",
        1565: "0.175E-03 pm 17.48",
        1570: "0.170E-03 pm 17.55",
        1575: "0.165E-03 pm 17.62",
        1580: "0.160E-03 pm 17.68",
        1585: "0.155E-03 pm 17.75",
        1590: "0.151E-03 pm 17.82",
        1595: "0.146E-03 pm 17.89",
        1600: "0.142E-03 pm 17.96",
        1605: "0.138E-03 pm 18.03",
        1610: "0.134E-03 pm 18.1",
        1615: "0.130E-03 pm 18.17",
        1620: "0.127E-03 pm 18.24",
        1625: "0.123E-03 pm 18.31",
        1630: "0.119E-03 pm 18.38",
        1635: "0.116E-03 pm 18.45",
        1640: "0.113E-03 pm 18.52",
        1645: "0.109E-03 pm 18.59",
        1650: "0.106E-03 pm 18.67",
        1655: "0.103E-03 pm 18.74",
        1660: "0.100E-03 pm 18.81",
        1665: "0.974E-04 pm 18.88",
        1670: "0.946E-04 pm 18.96",
        1675: "0.920E-04 pm 19.03",
        1680: "0.893E-04 pm 19.1",
        1685: "0.868E-04 pm 19.18",
        1690: "0.843E-04 pm 19.25",
        1695: "0.819E-04 pm 19.33",
        1700: "0.796E-04 pm 19.4",
        1705: "0.774E-04 pm 19.48",
        1710: "0.752E-04 pm 19.55",
        1715: "0.731E-04 pm 19.63",
        1720: "0.710E-04 pm 19.7",
        1725: "0.690E-04 pm 19.78",
        1730: "0.671E-04 pm 19.85",
        1735: "0.652E-04 pm 19.93",
        1740: "0.633E-04 pm 20.01",
        1745: "0.616E-04 pm 20.08",
        1750: "0.598E-04 pm 20.16",
        1755: "0.582E-04 pm 20.24",
        1760: "0.565E-04 pm 20.31",
        1765: "0.550E-04 pm 20.39",
        1770: "0.534E-04 pm 20.47",
        1775: "0.519E-04 pm 20.55",
        1780: "0.505E-04 pm 20.63",
        1785: "0.491E-04 pm 20.71",
        1790: "0.477E-04 pm 20.79",
        1795: "0.464E-04 pm 20.86",
        1800: "0.451E-04 pm 20.94",
        1805: "0.438E-04 pm 21.02",
        1810: "0.426E-04 pm 21.1",
        1815: "0.414E-04 pm 21.19",
        1820: "0.403E-04 pm 21.27",
        1825: "0.392E-04 pm 21.35",
        1830: "0.381E-04 pm 21.43",
        1835: "0.370E-04 pm 21.51",
        1840: "0.360E-04 pm 21.59",
        1845: "0.350E-04 pm 21.68",
        1850: "0.340E-04 pm 21.76",
        1855: "0.331E-04 pm 21.84",
        1860: "0.322E-04 pm 21.92",
        1865: "0.313E-04 pm 22.01",
        1870: "0.304E-04 pm 22.09",
        1875: "0.296E-04 pm 22.18",
        1880: "0.288E-04 pm 22.26",
        1885: "0.280E-04 pm 22.34",
        1890: "0.272E-04 pm 22.43",
        1895: "0.265E-04 pm 22.52",
        1900: "0.258E-04 pm 22.6",
        1905: "0.250E-04 pm 22.69",
        1910: "0.244E-04 pm 22.77",
        1915: "0.237E-04 pm 22.86",
        1920: "0.230E-04 pm 22.95",
        1925: "0.224E-04 pm 23.03",
        1930: "0.218E-04 pm 23.12",
        1935: "0.212E-04 pm 23.21",
        1940: "0.206E-04 pm 23.3",
        1945: "0.201E-04 pm 23.38",
        1950: "0.195E-04 pm 23.47",
        1955: "0.190E-04 pm 23.56",
        1960: "0.185E-04 pm 23.65",
        1965: "0.180E-04 pm 23.74",
        1970: "0.175E-04 pm 23.83",
        1975: "0.170E-04 pm 23.92",
        1980: "0.165E-04 pm 24.01",
        1985: "0.161E-04 pm 24.1",
        1990: "0.157E-04 pm 24.2",
        1995: "0.152E-04 pm 24.29",
        2000: "0.148E-04 pm 24.38",
        2005: "0.144E-04 pm 24.47",
        2010: "0.140E-04 pm 24.56",
        2015: "0.137E-04 pm 24.66",
        2020: "0.133E-04 pm 24.75",
        2025: "0.129E-04 pm 24.84",
        2030: "0.126E-04 pm 24.94",
        2035: "0.122E-04 pm 25.03",
        2040: "0.119E-04 pm 25.13",
        2045: "0.116E-04 pm 25.22",
        2050: "0.113E-04 pm 25.32",
        2055: "0.110E-04 pm 25.42",
        2060: "0.107E-04 pm 25.51",
        2065: "0.104E-04 pm 25.61",
        2070: "0.101E-04 pm 25.71",
        2075: "0.984E-05 pm 25.8",
        2080: "0.957E-05 pm 25.9",
        2085: "0.931E-05 pm 26.0",
        2090: "0.906E-05 pm 26.1",
        2095: "0.882E-05 pm 26.2",
        2100: "0.858E-05 pm 26.3",
        2105: "0.835E-05 pm 26.4",
        2110: "0.813E-05 pm 26.5",
        2115: "0.791E-05 pm 26.6",
        2120: "0.770E-05 pm 26.7",
        2125: "0.749E-05 pm 26.8",
        2130: "0.729E-05 pm 26.9",
        2135: "0.710E-05 pm 27.01",
        2140: "0.691E-05 pm 27.11",
        2145: "0.672E-05 pm 27.21",
        2150: "0.655E-05 pm 27.32",
        2155: "0.637E-05 pm 27.42",
        2160: "0.620E-05 pm 27.52",
        2165: "0.604E-05 pm 27.63",
        2170: "0.587E-05 pm 27.73",
        2175: "0.572E-05 pm 27.84",
        2180: "0.557E-05 pm 27.95",
        2185: "0.542E-05 pm 28.05",
        2190: "0.527E-05 pm 28.16",
        2195: "0.513E-05 pm 28.27",
        2200: "0.500E-05 pm 28.38",
        2205: "0.486E-05 pm 28.48",
        2210: "0.473E-05 pm 28.59",
        2215: "0.461E-05 pm 28.7",
        2220: "0.449E-05 pm 28.81",
        2225: "0.437E-05 pm 28.92",
        2230: "0.425E-05 pm 29.03",
        2235: "0.414E-05 pm 29.14",
        2240: "0.403E-05 pm 29.25",
        2245: "0.392E-05 pm 29.36",
        2250: "0.382E-05 pm 29.47",
        2255: "0.372E-05 pm 29.58",
        2260: "0.362E-05 pm 29.7",
        2265: "0.352E-05 pm 29.81",
        2270: "0.343E-05 pm 29.92",
        2275: "0.334E-05 pm 30.04",
        2280: "0.325E-05 pm 30.15",
        2285: "0.316E-05 pm 30.27",
        2290: "0.308E-05 pm 30.38",
        2295: "0.300E-05 pm 30.5",
        2300: "0.292E-05 pm 30.62",
        2305: "0.284E-05 pm 30.74",
        2310: "0.277E-05 pm 30.85",
        2315: "0.269E-05 pm 30.97",
        2320: "0.262E-05 pm 31.09",
        2325: "0.255E-05 pm 31.21",
        2330: "0.249E-05 pm 31.33",
        2335: "0.242E-05 pm 31.46",
        2340: "0.236E-05 pm 31.58",
        2345: "0.229E-05 pm 31.7",
        2350: "0.223E-05 pm 31.82",
        2355: "0.217E-05 pm 31.95",
        2360: "0.212E-05 pm 32.07",
        2365: "0.206E-05 pm 32.2",
        2370: "0.201E-05 pm 32.32",
        2375: "0.195E-05 pm 32.45",
        2380: "0.190E-05 pm 32.58",
        2385: "0.185E-05 pm 32.7",
        2390: "0.180E-05 pm 32.83",
        2395: "0.176E-05 pm 32.96",
        2400: "0.171E-05 pm 33.09",
        2405: "0.166E-05 pm 33.22",
        2410: "0.162E-05 pm 33.35",
        2415: "0.158E-05 pm 33.48",
        2420: "0.154E-05 pm 33.61",
        2425: "0.150E-05 pm 33.75",
        2430: "0.146E-05 pm 33.88",
        2435: "0.142E-05 pm 34.01",
        2440: "0.138E-05 pm 34.15",
        2445: "0.135E-05 pm 34.28",
        2450: "0.131E-05 pm 34.42",
        2455: "0.128E-05 pm 34.55",
        2460: "0.124E-05 pm 34.69",
        2465: "0.121E-05 pm 34.83",
        2470: "0.118E-05 pm 34.97",
        2475: "0.115E-05 pm 35.11",
        2480: "0.112E-05 pm 35.25",
        2485: "0.109E-05 pm 35.39",
        2490: "0.106E-05 pm 35.53",
        2495: "0.103E-05 pm 35.67",
        2500: "0.100E-05 pm 35.82",
        2505: "0.977E-06 pm 35.96",
        2510: "0.952E-06 pm 36.1",
        2515: "0.927E-06 pm 36.25",
        2520: "0.902E-06 pm 36.4",
        2525: "0.879E-06 pm 36.54",
        2530: "0.856E-06 pm 36.69",
        2535: "0.833E-06 pm 36.84",
        2540: "0.811E-06 pm 36.99",
        2545: "0.790E-06 pm 37.14",
        2550: "0.769E-06 pm 37.29",
        2555: "0.749E-06 pm 37.45",
        2560: "0.730E-06 pm 37.6",
        2565: "0.710E-06 pm 37.76",
        2570: "0.692E-06 pm 37.91",
        2575: "0.674E-06 pm 38.07",
        2580: "0.656E-06 pm 38.23",
        2585: "0.639E-06 pm 38.39",
        2590: "0.622E-06 pm 38.55",
        2595: "0.606E-06 pm 38.71",
        2600: "0.590E-06 pm 38.87",
        2605: "0.574E-06 pm 39.04",
        2610: "0.559E-06 pm 39.2",
        2615: "0.545E-06 pm 39.37",
        2620: "0.530E-06 pm 39.54",
        2625: "0.516E-06 pm 39.71",
        2630: "0.503E-06 pm 39.88",
        2635: "0.490E-06 pm 40.05",
        2640: "0.477E-06 pm 40.23",
        2645: "0.464E-06 pm 40.4",
        2650: "0.452E-06 pm 40.58",
        2655: "0.440E-06 pm 40.75",
        2660: "0.429E-06 pm 40.93",
        2665: "0.418E-06 pm 41.11",
        2670: "0.407E-06 pm 41.29",
        2675: "0.396E-06 pm 41.47",
        2680: "0.386E-06 pm 41.65",
        2685: "0.375E-06 pm 41.83",
        2690: "0.366E-06 pm 42.01",
        2695: "0.356E-06 pm 42.2",
        2700: "0.347E-06 pm 42.38",
        2705: "0.338E-06 pm 42.57",
        2710: "0.329E-06 pm 42.76",
        2715: "0.320E-06 pm 42.95",
        2720: "0.312E-06 pm 43.14",
        2725: "0.304E-06 pm 43.33",
        2730: "0.296E-06 pm 43.53",
        2735: "0.288E-06 pm 43.72",
        2740: "0.280E-06 pm 43.91",
        2745: "0.273E-06 pm 44.11",
        2750: "0.266E-06 pm 44.3",
        2755: "0.259E-06 pm 44.5",
        2760: "0.252E-06 pm 44.69",
        2765: "0.246E-06 pm 44.89",
        2770: "0.239E-06 pm 45.09",
        2775: "0.233E-06 pm 45.28",
        2780: "0.227E-06 pm 45.48",
        2785: "0.221E-06 pm 45.68",
        2790: "0.215E-06 pm 45.88",
        2795: "0.209E-06 pm 46.08",
        2800: "0.204E-06 pm 46.27",
        2805: "0.199E-06 pm 46.46",
        2810: "0.193E-06 pm 46.65",
        2815: "0.188E-06 pm 46.85",
        2820: "0.183E-06 pm 47.04",
        2825: "0.179E-06 pm 47.23",
        2830: "0.174E-06 pm 47.42",
        2835: "0.169E-06 pm 47.61",
        2840: "0.165E-06 pm 47.8",
        2845: "0.161E-06 pm 48.0",
        2850: "0.157E-06 pm 48.19",
        2855: "0.152E-06 pm 48.39",
        2860: "0.148E-06 pm 48.58",
        2865: "0.145E-06 pm 48.78",
        2870: "0.141E-06 pm 48.98",
        2875: "0.137E-06 pm 49.18",
        2880: "0.134E-06 pm 49.38",
        2885: "0.130E-06 pm 49.58",
        2890: "0.127E-06 pm 49.78",
        2895: "0.123E-06 pm 49.98",
        2900: "0.120E-06 pm 50.19",
        2905: "0.117E-06 pm 50.4",
        2910: "0.114E-06 pm 50.6",
        2915: "0.111E-06 pm 50.81",
        2920: "0.108E-06 pm 51.02",
        2925: "0.105E-06 pm 51.24",
        2930: "0.103E-06 pm 51.45",
        2935: "0.999E-07 pm 51.67",
        2940: "0.972E-07 pm 51.89",
        2945: "0.947E-07 pm 52.11",
        2950: "0.922E-07 pm 52.33",
        2955: "0.898E-07 pm 52.56",
        2960: "0.875E-07 pm 52.79",
        2965: "0.852E-07 pm 53.02",
        2970: "0.830E-07 pm 53.25",
        2975: "0.808E-07 pm 53.48",
        2980: "0.787E-07 pm 53.72",
        2985: "0.766E-07 pm 53.96",
        2990: "0.746E-07 pm 54.2",
        2995: "0.727E-07 pm 54.45",
        3000: "0.708E-07 pm 54.7"
    }

    for i_mass in xsections:
        xsections[i_mass] = float(xsections[i_mass].split()[0])

    mass = myround(int(mass), base=5)

    if mass in xsections:
        return xsections[mass]
    else:
        return -1

def GetContours(g, color, style):
    contours = [1.0]
    g.GetHistogram().SetContour(1,array('d',contours))
    g.Draw("cont z list")
    contLevel = g.GetContourList(1.0);
    max_points = -1
    for cont in contLevel:
        
        try:
            n_points = cont.GetN()
        except:
            continue
            
        if n_points > max_points:
            max_points = n_points
            cont.SetLineColor(color)
            cont.SetLineStyle(style)
            cont.SetLineWidth(5)
            out = cont

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
    # outSM.Sort() #sorting doesn't really work
        endglu, endlsp = Double(0), Double(0)
        outSM.GetPoint(1, endglu, endlsp)
        outSM.SetPoint(1, endglu, 0)

    #Extend line on the diagonal
       # iniglu, inilsp = Double(0), Double(0)
       # outSM.GetPoint(outSM.GetN()-1, iniglu, inilsp)
       # outSM.SetPoint(outSM.GetN()-1, inilsp+225, inilsp)

    outSM.SetLineColor(color)
    outSM.SetLineStyle(style)
    outSM.SetLineWidth(5)
    return outSM


def TryToGetContours(g, color, style, smoothing = False, n_smooth  = 4):

    try:
        if smoothing:
            return GetContoursSmooth(g, color, style)
        else:
            return GetContours(g, color, style)
    except:
        return TH2F('hello','hello', 113,-12.5,2812.5, 113,-12.5,2812.5)


def getxsecGlu():
    xsecGlu = {} # dict for xsecs 
    xsecFile = "glu_xsecs_13TeV.txt"

    with open(xsecFile,"r") as xfile:                            
        lines = xfile.readlines() 
        print 'Found %i lines in %s' %(len(lines),xsecFile)
        for line in lines:
            if line[0] == '#': continue
            (mGo,xsec,err) = line.split()
            xsecGlu[int(mGo)] = (float(xsec),float(err))
    return xsecGlu


def produce_limit_plot(pattern = "T1qqqqLL_allbins", draw_xsecs=True, smoothing = False):

    xsecGlu = getxsecGlu()

    hexp =     TH2F('hexp','hexp', 113,-12.5,2812.5, 113,-12.5,2812.5)
    hexpdown = TH2F('hexpdown','hexpdown', 113,-12.5,2812.5, 113,-12.5,2812.5)
    hexpup =   TH2F('hexpup','hexpup', 113,-12.5,2812.5, 113,-12.5,2812.5)
    hobs =     TH2F('hobs','hobs', 113,-12.5,2812.5, 113,-12.5,2812.5)

    vmx=[]; vmy = []; vxsec = []; vobs = [];  vobsup = []; vobsdown = []; vexp = []; vup = []; vdown = []; vlim = [];

    for signal_point_file in glob.glob(pattern + '/higgsCombine*root'):

        print signal_point_file
        mGo = int(signal_point_file.split("Signalg")[-1].split("_chi")[0])
        mLSP = int(signal_point_file.split("_chi")[-1].split(".AsymptoticLimits")[0])
        print 'mGo', mGo
        print 'mLSP', mLSP

        f = TFile.Open(signal_point_file, 'read')
        t = f.Get('limit')

        try:
            entries = t.GetEntries()
        except:
            continue
    
        if "T1qqqq" in pattern:
            xsec = xsecGlu[mGo][0]
            theorySys = xsecGlu[mGo][1]
        elif "T2bt" in pattern:
            xsec = get_sbottom_antisbottom_cross_section(mGo)
            theorySys = get_sbottom_antisbottom_cross_section(mGo)
            
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

    #hexp.SaveAs(pattern + '/testexp_' + pattern + '.root')
    #hobs.SaveAs(pattern + '/testobs_' + pattern + '.root')
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
    c = TCanvas("c", "c", 900, 800)
    c.SetLeftMargin(0.15)
    c.SetRightMargin(0.15)
    c.SetTopMargin(0.1)
    c.SetLogz(True)
    
    xmin = min(vmx)
    xmax = max(vmx)
    ymin = min(vmy)
    ymax = max(vmy)
    bin_size = 12.5;
    nxbins = max(1, min(500, (math.ceil((xmax-xmin)/bin_size))))
    nybins = max(1, min(500, (math.ceil((ymax-ymin)/bin_size))))
    glim.SetNpx(int(nxbins))
    glim.SetNpy(int(nybins))
    
    cexp = TryToGetContours(gexp, 2,1, smoothing = smoothing)
    cup = TryToGetContours(gup,2,2, smoothing = smoothing)
    cdown = TryToGetContours(gdown,2,2, smoothing = smoothing)
    cobs = TryToGetContours(gobs,1,1, smoothing = smoothing)
    cobsup = TryToGetContours(gobsup,1,2, smoothing = smoothing)
    cobsdown = TryToGetContours(gobsdown,1,2, smoothing = smoothing)

    hlim = glim.GetHistogram()
    
    if "T1qqqq" in pattern:
        hlim.SetTitle(";m_{gluino} [GeV];m_{LSP} [GeV]");
    elif "T2bt" in pattern:
        hlim.SetTitle(";m_{stop} [GeV];m_{LSP} [GeV]");
        
    hlim.Draw("colz")
    #hlim.Draw("text")
    if "T2bt" in pattern:
        hlim.GetXaxis().SetRangeUser(0,2000)
        hlim.GetYaxis().SetRangeUser(50,2000)
    cexp.Draw("same")
    cup.Draw("same")
    cdown.Draw("same")
    #cobs.Draw("same")
    #cobsup.Draw("same")
    #cobsdown.Draw("same")
    flimit = TFile(pattern + "/limit_scan.root", "recreate")

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

    shared_utils.stamp()

    label = pattern.split("/")[-1].replace("_", ", ")

    latex_label=TLatex()
    latex_label.SetNDC()
    latex_label.SetTextColor(kBlack)
    latex_label.SetTextAlign(11)
    latex_label.SetTextSize(0.035)
    latex_label.DrawLatex(0.2, 0.8, label)

    c.SaveAs("../" + pattern.split("/")[-1]+'.pdf')


if __name__ == "__main__":

    parser = OptionParser()
    (options, args) = parser.parse_args()

    if len(args)>0:
        pattern = args[0]
        if pattern[-1] == "/":
            pattern = pattern[:-1]
        gROOT.SetBatch(1)
        produce_limit_plot(pattern)
    else:
        print "Run with ./plot_limit.py ../T2bt_noleptons, where the folder contains the Higgs combine output."

