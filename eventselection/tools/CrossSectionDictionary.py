from array import array
from ROOT import *
CrossSectionsPb = {}
def loadCrossSections(model = "T1"):
  if model=="T1":
	CrossSectionsPb["T1"]= {}
	CrossSectionsPb["T1"]["500"]= 0.338E+02
	CrossSectionsPb["T1"]["505"]= 0.319E+02
	CrossSectionsPb["T1"]["510"]= 0.301E+02
	CrossSectionsPb["T1"]["515"]= 0.284E+02
	CrossSectionsPb["T1"]["520"]= 0.268E+02
	CrossSectionsPb["T1"]["525"]= 0.253E+02
	CrossSectionsPb["T1"]["530"]= 0.240E+02
	CrossSectionsPb["T1"]["535"]= 0.227E+02
	CrossSectionsPb["T1"]["540"]= 0.214E+02
	CrossSectionsPb["T1"]["545"]= 0.203E+02
	CrossSectionsPb["T1"]["550"]= 0.192E+02
	CrossSectionsPb["T1"]["555"]= 0.182E+02
	CrossSectionsPb["T1"]["560"]= 0.172E+02
	CrossSectionsPb["T1"]["565"]= 0.163E+02
	CrossSectionsPb["T1"]["570"]= 0.155E+02
	CrossSectionsPb["T1"]["575"]= 0.147E+02
	CrossSectionsPb["T1"]["580"]= 0.139E+02
	CrossSectionsPb["T1"]["585"]= 0.132E+02
	CrossSectionsPb["T1"]["590"]= 0.126E+02
	CrossSectionsPb["T1"]["595"]= 0.119E+02
	CrossSectionsPb["T1"]["600"]= 0.113E+02
	CrossSectionsPb["T1"]["605"]= 0.108E+02
	CrossSectionsPb["T1"]["610"]= 0.102E+02
	CrossSectionsPb["T1"]["615"]= 0.974E+01
	CrossSectionsPb["T1"]["620"]= 0.926E+01
	CrossSectionsPb["T1"]["625"]= 0.881E+01
	CrossSectionsPb["T1"]["630"]= 0.839E+01
	CrossSectionsPb["T1"]["635"]= 0.799E+01
	CrossSectionsPb["T1"]["640"]= 0.761E+01
	CrossSectionsPb["T1"]["645"]= 0.725E+01
	CrossSectionsPb["T1"]["650"]= 0.690E+01
	CrossSectionsPb["T1"]["655"]= 0.658E+01
	CrossSectionsPb["T1"]["660"]= 0.627E+01
	CrossSectionsPb["T1"]["665"]= 0.598E+01
	CrossSectionsPb["T1"]["670"]= 0.571E+01
	CrossSectionsPb["T1"]["675"]= 0.544E+01
	CrossSectionsPb["T1"]["680"]= 0.520E+01
	CrossSectionsPb["T1"]["685"]= 0.496E+01
	CrossSectionsPb["T1"]["690"]= 0.474E+01
	CrossSectionsPb["T1"]["695"]= 0.452E+01
	CrossSectionsPb["T1"]["700"]= 0.432E+01
	CrossSectionsPb["T1"]["705"]= 0.413E+01
	CrossSectionsPb["T1"]["710"]= 0.395E+01
	CrossSectionsPb["T1"]["715"]= 0.377E+01
	CrossSectionsPb["T1"]["720"]= 0.361E+01
	CrossSectionsPb["T1"]["725"]= 0.345E+01
	CrossSectionsPb["T1"]["730"]= 0.330E+01
	CrossSectionsPb["T1"]["735"]= 0.316E+01
	CrossSectionsPb["T1"]["740"]= 0.302E+01
	CrossSectionsPb["T1"]["745"]= 0.289E+01
	CrossSectionsPb["T1"]["750"]= 0.277E+01
	CrossSectionsPb["T1"]["755"]= 0.265E+01
	CrossSectionsPb["T1"]["760"]= 0.254E+01
	CrossSectionsPb["T1"]["765"]= 0.243E+01
	CrossSectionsPb["T1"]["770"]= 0.233E+01
	CrossSectionsPb["T1"]["775"]= 0.223E+01
	CrossSectionsPb["T1"]["780"]= 0.214E+01
	CrossSectionsPb["T1"]["785"]= 0.205E+01
	CrossSectionsPb["T1"]["790"]= 0.197E+01
	CrossSectionsPb["T1"]["795"]= 0.188E+01
	CrossSectionsPb["T1"]["800"]= 0.181E+01
	CrossSectionsPb["T1"]["805"]= 0.173E+01
	CrossSectionsPb["T1"]["810"]= 0.166E+01
	CrossSectionsPb["T1"]["815"]= 0.160E+01
	CrossSectionsPb["T1"]["820"]= 0.153E+01
	CrossSectionsPb["T1"]["825"]= 0.147E+01
	CrossSectionsPb["T1"]["830"]= 0.141E+01
	CrossSectionsPb["T1"]["835"]= 0.136E+01
	CrossSectionsPb["T1"]["840"]= 0.130E+01
	CrossSectionsPb["T1"]["845"]= 0.125E+01
	CrossSectionsPb["T1"]["850"]= 0.120E+01
	CrossSectionsPb["T1"]["855"]= 0.115E+01
	CrossSectionsPb["T1"]["860"]= 0.111E+01
	CrossSectionsPb["T1"]["865"]= 0.107E+01
	CrossSectionsPb["T1"]["870"]= 0.103E+01
	CrossSectionsPb["T1"]["875"]= 0.986E+00
	CrossSectionsPb["T1"]["880"]= 0.948E+00
	CrossSectionsPb["T1"]["885"]= 0.912E+00
	CrossSectionsPb["T1"]["890"]= 0.877E+00
	CrossSectionsPb["T1"]["895"]= 0.844E+00
	CrossSectionsPb["T1"]["900"]= 0.812E+00
	CrossSectionsPb["T1"]["905"]= 0.781E+00
	CrossSectionsPb["T1"]["910"]= 0.752E+00
	CrossSectionsPb["T1"]["915"]= 0.723E+00
	CrossSectionsPb["T1"]["920"]= 0.696E+00
	CrossSectionsPb["T1"]["925"]= 0.670E+00
	CrossSectionsPb["T1"]["930"]= 0.646E+00
	CrossSectionsPb["T1"]["935"]= 0.622E+00
	CrossSectionsPb["T1"]["940"]= 0.599E+00
	CrossSectionsPb["T1"]["945"]= 0.577E+00
	CrossSectionsPb["T1"]["950"]= 0.556E+00
	CrossSectionsPb["T1"]["955"]= 0.535E+00
	CrossSectionsPb["T1"]["960"]= 0.516E+00
	CrossSectionsPb["T1"]["965"]= 0.497E+00
	CrossSectionsPb["T1"]["970"]= 0.479E+00
	CrossSectionsPb["T1"]["975"]= 0.462E+00
	CrossSectionsPb["T1"]["980"]= 0.445E+00
	CrossSectionsPb["T1"]["985"]= 0.430E+00
	CrossSectionsPb["T1"]["990"]= 0.414E+00
	CrossSectionsPb["T1"]["995"]= 0.399E+00
	CrossSectionsPb["T1"]["1000"]= 0.385E+00
	CrossSectionsPb["T1"]["1005"]= 0.372E+00
	CrossSectionsPb["T1"]["1010"]= 0.359E+00
	CrossSectionsPb["T1"]["1015"]= 0.346E+00
	CrossSectionsPb["T1"]["1020"]= 0.334E+00
	CrossSectionsPb["T1"]["1025"]= 0.322E+00
	CrossSectionsPb["T1"]["1030"]= 0.311E+00
	CrossSectionsPb["T1"]["1035"]= 0.300E+00
	CrossSectionsPb["T1"]["1040"]= 0.290E+00
	CrossSectionsPb["T1"]["1045"]= 0.280E+00
	CrossSectionsPb["T1"]["1050"]= 0.270E+00
	CrossSectionsPb["T1"]["1055"]= 0.261E+00
	CrossSectionsPb["T1"]["1060"]= 0.252E+00
	CrossSectionsPb["T1"]["1065"]= 0.243E+00
	CrossSectionsPb["T1"]["1070"]= 0.235E+00
	CrossSectionsPb["T1"]["1075"]= 0.227E+00
	CrossSectionsPb["T1"]["1080"]= 0.219E+00
	CrossSectionsPb["T1"]["1085"]= 0.212E+00
	CrossSectionsPb["T1"]["1090"]= 0.205E+00
	CrossSectionsPb["T1"]["1095"]= 0.198E+00
	CrossSectionsPb["T1"]["1100"]= 0.191E+00
	CrossSectionsPb["T1"]["1105"]= 0.185E+00
	CrossSectionsPb["T1"]["1110"]= 0.179E+00
	CrossSectionsPb["T1"]["1115"]= 0.173E+00
	CrossSectionsPb["T1"]["1120"]= 0.167E+00
	CrossSectionsPb["T1"]["1125"]= 0.162E+00
	CrossSectionsPb["T1"]["1130"]= 0.156E+00
	CrossSectionsPb["T1"]["1135"]= 0.151E+00
	CrossSectionsPb["T1"]["1140"]= 0.146E+00
	CrossSectionsPb["T1"]["1145"]= 0.141E+00
	CrossSectionsPb["T1"]["1150"]= 0.137E+00
	CrossSectionsPb["T1"]["1155"]= 0.132E+00
	CrossSectionsPb["T1"]["1160"]= 0.128E+00
	CrossSectionsPb["T1"]["1165"]= 0.124E+00
	CrossSectionsPb["T1"]["1170"]= 0.120E+00
	CrossSectionsPb["T1"]["1175"]= 0.116E+00
	CrossSectionsPb["T1"]["1180"]= 0.112E+00
	CrossSectionsPb["T1"]["1185"]= 0.109E+00
	CrossSectionsPb["T1"]["1190"]= 0.105E+00
	CrossSectionsPb["T1"]["1195"]= 0.102E+00
	CrossSectionsPb["T1"]["1200"]= 0.985E-01
	CrossSectionsPb["T1"]["1205"]= 0.953E-01
	CrossSectionsPb["T1"]["1210"]= 0.923E-01
	CrossSectionsPb["T1"]["1215"]= 0.894E-01
	CrossSectionsPb["T1"]["1220"]= 0.866E-01
	CrossSectionsPb["T1"]["1225"]= 0.838E-01
	CrossSectionsPb["T1"]["1230"]= 0.812E-01
	CrossSectionsPb["T1"]["1235"]= 0.786E-01
	CrossSectionsPb["T1"]["1240"]= 0.762E-01
	CrossSectionsPb["T1"]["1245"]= 0.738E-01
	CrossSectionsPb["T1"]["1250"]= 0.715E-01
	CrossSectionsPb["T1"]["1255"]= 0.692E-01
	CrossSectionsPb["T1"]["1260"]= 0.671E-01
	CrossSectionsPb["T1"]["1265"]= 0.650E-01
	CrossSectionsPb["T1"]["1270"]= 0.630E-01
	CrossSectionsPb["T1"]["1275"]= 0.610E-01
	CrossSectionsPb["T1"]["1280"]= 0.591E-01
	CrossSectionsPb["T1"]["1285"]= 0.573E-01
	CrossSectionsPb["T1"]["1290"]= 0.556E-01
	CrossSectionsPb["T1"]["1295"]= 0.539E-01
	CrossSectionsPb["T1"]["1300"]= 0.522E-01
	CrossSectionsPb["T1"]["1305"]= 0.506E-01
	CrossSectionsPb["T1"]["1310"]= 0.491E-01
	CrossSectionsPb["T1"]["1315"]= 0.476E-01
	CrossSectionsPb["T1"]["1320"]= 0.461E-01
	CrossSectionsPb["T1"]["1325"]= 0.447E-01
	CrossSectionsPb["T1"]["1330"]= 0.434E-01
	CrossSectionsPb["T1"]["1335"]= 0.421E-01
	CrossSectionsPb["T1"]["1340"]= 0.408E-01
	CrossSectionsPb["T1"]["1345"]= 0.396E-01
	CrossSectionsPb["T1"]["1350"]= 0.384E-01
	CrossSectionsPb["T1"]["1355"]= 0.372E-01
	CrossSectionsPb["T1"]["1360"]= 0.361E-01
	CrossSectionsPb["T1"]["1365"]= 0.350E-01
	CrossSectionsPb["T1"]["1370"]= 0.340E-01
	CrossSectionsPb["T1"]["1375"]= 0.330E-01
	CrossSectionsPb["T1"]["1380"]= 0.320E-01
	CrossSectionsPb["T1"]["1385"]= 0.310E-01
	CrossSectionsPb["T1"]["1390"]= 0.301E-01
	CrossSectionsPb["T1"]["1395"]= 0.292E-01
	CrossSectionsPb["T1"]["1400"]= 0.284E-01
	CrossSectionsPb["T1"]["1405"]= 0.275E-01
	CrossSectionsPb["T1"]["1410"]= 0.267E-01
	CrossSectionsPb["T1"]["1415"]= 0.259E-01
	CrossSectionsPb["T1"]["1420"]= 0.252E-01
	CrossSectionsPb["T1"]["1425"]= 0.244E-01
	CrossSectionsPb["T1"]["1430"]= 0.237E-01
	CrossSectionsPb["T1"]["1435"]= 0.230E-01
	CrossSectionsPb["T1"]["1440"]= 0.224E-01
	CrossSectionsPb["T1"]["1445"]= 0.217E-01
	CrossSectionsPb["T1"]["1450"]= 0.211E-01
	CrossSectionsPb["T1"]["1455"]= 0.205E-01
	CrossSectionsPb["T1"]["1460"]= 0.199E-01
	CrossSectionsPb["T1"]["1465"]= 0.193E-01
	CrossSectionsPb["T1"]["1470"]= 0.187E-01
	CrossSectionsPb["T1"]["1475"]= 0.182E-01
	CrossSectionsPb["T1"]["1480"]= 0.177E-01
	CrossSectionsPb["T1"]["1485"]= 0.172E-01
	CrossSectionsPb["T1"]["1490"]= 0.167E-01
	CrossSectionsPb["T1"]["1495"]= 0.162E-01
	CrossSectionsPb["T1"]["1500"]= 0.157E-01
	CrossSectionsPb["T1"]["1505"]= 0.153E-01
	CrossSectionsPb["T1"]["1510"]= 0.148E-01
	CrossSectionsPb["T1"]["1515"]= 0.144E-01
	CrossSectionsPb["T1"]["1520"]= 0.140E-01
	CrossSectionsPb["T1"]["1525"]= 0.136E-01
	CrossSectionsPb["T1"]["1530"]= 0.132E-01
	CrossSectionsPb["T1"]["1535"]= 0.128E-01
	CrossSectionsPb["T1"]["1540"]= 0.125E-01
	CrossSectionsPb["T1"]["1545"]= 0.121E-01
	CrossSectionsPb["T1"]["1550"]= 0.118E-01
	CrossSectionsPb["T1"]["1555"]= 0.115E-01
	CrossSectionsPb["T1"]["1560"]= 0.111E-01
	CrossSectionsPb["T1"]["1565"]= 0.108E-01
	CrossSectionsPb["T1"]["1570"]= 0.105E-01
	CrossSectionsPb["T1"]["1575"]= 0.102E-01
	CrossSectionsPb["T1"]["1580"]= 0.993E-02
	CrossSectionsPb["T1"]["1585"]= 0.966E-02
	CrossSectionsPb["T1"]["1590"]= 0.939E-02
	CrossSectionsPb["T1"]["1595"]= 0.912E-02
	CrossSectionsPb["T1"]["1600"]= 0.887E-02
	CrossSectionsPb["T1"]["1605"]= 0.862E-02
	CrossSectionsPb["T1"]["1610"]= 0.838E-02
	CrossSectionsPb["T1"]["1615"]= 0.815E-02
	CrossSectionsPb["T1"]["1620"]= 0.792E-02
	CrossSectionsPb["T1"]["1625"]= 0.770E-02
	CrossSectionsPb["T1"]["1630"]= 0.749E-02
	CrossSectionsPb["T1"]["1635"]= 0.728E-02
	CrossSectionsPb["T1"]["1640"]= 0.708E-02
	CrossSectionsPb["T1"]["1645"]= 0.689E-02
	CrossSectionsPb["T1"]["1650"]= 0.670E-02
	CrossSectionsPb["T1"]["1655"]= 0.651E-02
	CrossSectionsPb["T1"]["1660"]= 0.633E-02
	CrossSectionsPb["T1"]["1665"]= 0.616E-02
	CrossSectionsPb["T1"]["1670"]= 0.599E-02
	CrossSectionsPb["T1"]["1675"]= 0.583E-02
	CrossSectionsPb["T1"]["1680"]= 0.567E-02
	CrossSectionsPb["T1"]["1685"]= 0.551E-02
	CrossSectionsPb["T1"]["1690"]= 0.536E-02
	CrossSectionsPb["T1"]["1695"]= 0.521E-02
	CrossSectionsPb["T1"]["1700"]= 0.507E-02
	CrossSectionsPb["T1"]["1705"]= 0.493E-02
	CrossSectionsPb["T1"]["1710"]= 0.480E-02
	CrossSectionsPb["T1"]["1715"]= 0.467E-02
	CrossSectionsPb["T1"]["1720"]= 0.454E-02
	CrossSectionsPb["T1"]["1725"]= 0.442E-02
	CrossSectionsPb["T1"]["1730"]= 0.430E-02
	CrossSectionsPb["T1"]["1735"]= 0.418E-02
	CrossSectionsPb["T1"]["1740"]= 0.407E-02
	CrossSectionsPb["T1"]["1745"]= 0.396E-02
	CrossSectionsPb["T1"]["1750"]= 0.385E-02
	CrossSectionsPb["T1"]["1755"]= 0.375E-02
	CrossSectionsPb["T1"]["1760"]= 0.365E-02
	CrossSectionsPb["T1"]["1765"]= 0.355E-02
	CrossSectionsPb["T1"]["1770"]= 0.345E-02
	CrossSectionsPb["T1"]["1775"]= 0.336E-02
	CrossSectionsPb["T1"]["1780"]= 0.327E-02
	CrossSectionsPb["T1"]["1785"]= 0.318E-02
	CrossSectionsPb["T1"]["1790"]= 0.310E-02
	CrossSectionsPb["T1"]["1795"]= 0.301E-02
	CrossSectionsPb["T1"]["1800"]= 0.293E-02
	CrossSectionsPb["T1"]["1805"]= 0.286E-02
	CrossSectionsPb["T1"]["1810"]= 0.278E-02
	CrossSectionsPb["T1"]["1815"]= 0.271E-02
	CrossSectionsPb["T1"]["1820"]= 0.263E-02
	CrossSectionsPb["T1"]["1825"]= 0.256E-02
	CrossSectionsPb["T1"]["1830"]= 0.249E-02
	CrossSectionsPb["T1"]["1835"]= 0.243E-02
	CrossSectionsPb["T1"]["1840"]= 0.236E-02
	CrossSectionsPb["T1"]["1845"]= 0.230E-02
	CrossSectionsPb["T1"]["1850"]= 0.224E-02
	CrossSectionsPb["T1"]["1855"]= 0.218E-02
	CrossSectionsPb["T1"]["1860"]= 0.212E-02
	CrossSectionsPb["T1"]["1865"]= 0.207E-02
	CrossSectionsPb["T1"]["1870"]= 0.201E-02
	CrossSectionsPb["T1"]["1875"]= 0.196E-02
	CrossSectionsPb["T1"]["1880"]= 0.191E-02
	CrossSectionsPb["T1"]["1885"]= 0.186E-02
	CrossSectionsPb["T1"]["1890"]= 0.181E-02
	CrossSectionsPb["T1"]["1895"]= 0.176E-02
	CrossSectionsPb["T1"]["1900"]= 0.171E-02
	CrossSectionsPb["T1"]["1905"]= 0.167E-02
	CrossSectionsPb["T1"]["1910"]= 0.163E-02
	CrossSectionsPb["T1"]["1915"]= 0.158E-02
	CrossSectionsPb["T1"]["1920"]= 0.154E-02
	CrossSectionsPb["T1"]["1925"]= 0.150E-02
	CrossSectionsPb["T1"]["1930"]= 0.146E-02
	CrossSectionsPb["T1"]["1935"]= 0.142E-02
	CrossSectionsPb["T1"]["1940"]= 0.139E-02
	CrossSectionsPb["T1"]["1945"]= 0.135E-02
	CrossSectionsPb["T1"]["1950"]= 0.131E-02
	CrossSectionsPb["T1"]["1955"]= 0.128E-02
	CrossSectionsPb["T1"]["1960"]= 0.125E-02
	CrossSectionsPb["T1"]["1965"]= 0.121E-02
	CrossSectionsPb["T1"]["1970"]= 0.118E-02
	CrossSectionsPb["T1"]["1975"]= 0.115E-02
	CrossSectionsPb["T1"]["1980"]= 0.112E-02
	CrossSectionsPb["T1"]["1985"]= 0.109E-02
	CrossSectionsPb["T1"]["1990"]= 0.106E-02
	CrossSectionsPb["T1"]["1995"]= 0.104E-02
	CrossSectionsPb["T1"]["2000"]= 0.101E-02
	CrossSectionsPb["T1"]["2005"]= 0.983E-03
	CrossSectionsPb["T1"]["2010"]= 0.957E-03
	CrossSectionsPb["T1"]["2015"]= 0.933E-03
	CrossSectionsPb["T1"]["2020"]= 0.908E-03
	CrossSectionsPb["T1"]["2025"]= 0.885E-03
	CrossSectionsPb["T1"]["2030"]= 0.862E-03
	CrossSectionsPb["T1"]["2035"]= 0.840E-03
	CrossSectionsPb["T1"]["2040"]= 0.818E-03
	CrossSectionsPb["T1"]["2045"]= 0.797E-03
	CrossSectionsPb["T1"]["2050"]= 0.776E-03
	CrossSectionsPb["T1"]["2055"]= 0.756E-03
	CrossSectionsPb["T1"]["2060"]= 0.737E-03
	CrossSectionsPb["T1"]["2065"]= 0.718E-03
	CrossSectionsPb["T1"]["2070"]= 0.699E-03
	CrossSectionsPb["T1"]["2075"]= 0.681E-03
	CrossSectionsPb["T1"]["2080"]= 0.664E-03
	CrossSectionsPb["T1"]["2085"]= 0.647E-03
	CrossSectionsPb["T1"]["2090"]= 0.630E-03
	CrossSectionsPb["T1"]["2095"]= 0.614E-03
	CrossSectionsPb["T1"]["2100"]= 0.598E-03
	CrossSectionsPb["T1"]["2105"]= 0.583E-03
	CrossSectionsPb["T1"]["2110"]= 0.568E-03
	CrossSectionsPb["T1"]["2115"]= 0.553E-03
	CrossSectionsPb["T1"]["2120"]= 0.539E-03
	CrossSectionsPb["T1"]["2125"]= 0.525E-03
	CrossSectionsPb["T1"]["2130"]= 0.512E-03
	CrossSectionsPb["T1"]["2135"]= 0.499E-03
	CrossSectionsPb["T1"]["2140"]= 0.486E-03
	CrossSectionsPb["T1"]["2145"]= 0.473E-03
	CrossSectionsPb["T1"]["2150"]= 0.461E-03
	CrossSectionsPb["T1"]["2155"]= 0.449E-03
	CrossSectionsPb["T1"]["2160"]= 0.438E-03
	CrossSectionsPb["T1"]["2165"]= 0.427E-03
	CrossSectionsPb["T1"]["2170"]= 0.416E-03
	CrossSectionsPb["T1"]["2175"]= 0.405E-03
	CrossSectionsPb["T1"]["2180"]= 0.395E-03
	CrossSectionsPb["T1"]["2185"]= 0.385E-03
	CrossSectionsPb["T1"]["2190"]= 0.375E-03
	CrossSectionsPb["T1"]["2195"]= 0.365E-03
	CrossSectionsPb["T1"]["2200"]= 0.356E-03
	CrossSectionsPb["T1"]["2205"]= 0.347E-03
	CrossSectionsPb["T1"]["2210"]= 0.338E-03
	CrossSectionsPb["T1"]["2215"]= 0.330E-03
	CrossSectionsPb["T1"]["2220"]= 0.321E-03
	CrossSectionsPb["T1"]["2225"]= 0.313E-03
	CrossSectionsPb["T1"]["2230"]= 0.305E-03
	CrossSectionsPb["T1"]["2235"]= 0.297E-03
	CrossSectionsPb["T1"]["2240"]= 0.290E-03
	CrossSectionsPb["T1"]["2245"]= 0.283E-03
	CrossSectionsPb["T1"]["2250"]= 0.275E-03
	CrossSectionsPb["T1"]["2255"]= 0.268E-03
	CrossSectionsPb["T1"]["2260"]= 0.262E-03
	CrossSectionsPb["T1"]["2265"]= 0.255E-03
	CrossSectionsPb["T1"]["2270"]= 0.248E-03
	CrossSectionsPb["T1"]["2275"]= 0.242E-03
	CrossSectionsPb["T1"]["2280"]= 0.236E-03
	CrossSectionsPb["T1"]["2285"]= 0.230E-03
	CrossSectionsPb["T1"]["2290"]= 0.224E-03
	CrossSectionsPb["T1"]["2295"]= 0.219E-03
	CrossSectionsPb["T1"]["2300"]= 0.213E-03
	CrossSectionsPb["T1"]["2305"]= 0.208E-03
	CrossSectionsPb["T1"]["2310"]= 0.202E-03
	CrossSectionsPb["T1"]["2315"]= 0.197E-03
	CrossSectionsPb["T1"]["2320"]= 0.192E-03
	CrossSectionsPb["T1"]["2325"]= 0.187E-03
	CrossSectionsPb["T1"]["2330"]= 0.183E-03
	CrossSectionsPb["T1"]["2335"]= 0.178E-03
	CrossSectionsPb["T1"]["2340"]= 0.174E-03
	CrossSectionsPb["T1"]["2345"]= 0.169E-03
	CrossSectionsPb["T1"]["2350"]= 0.165E-03
	CrossSectionsPb["T1"]["2355"]= 0.161E-03
	CrossSectionsPb["T1"]["2360"]= 0.157E-03
	CrossSectionsPb["T1"]["2365"]= 0.153E-03
	CrossSectionsPb["T1"]["2370"]= 0.149E-03
	CrossSectionsPb["T1"]["2375"]= 0.145E-03
	CrossSectionsPb["T1"]["2380"]= 0.142E-03
	CrossSectionsPb["T1"]["2385"]= 0.138E-03
	CrossSectionsPb["T1"]["2390"]= 0.134E-03
	CrossSectionsPb["T1"]["2395"]= 0.131E-03
	CrossSectionsPb["T1"]["2400"]= 0.128E-03
	CrossSectionsPb["T1"]["2405"]= 0.125E-03
	CrossSectionsPb["T1"]["2410"]= 0.121E-03
	CrossSectionsPb["T1"]["2415"]= 0.118E-03
	CrossSectionsPb["T1"]["2420"]= 0.115E-03
	CrossSectionsPb["T1"]["2425"]= 0.113E-03
	CrossSectionsPb["T1"]["2430"]= 0.110E-03
	CrossSectionsPb["T1"]["2435"]= 0.107E-03
	CrossSectionsPb["T1"]["2440"]= 0.104E-03
	CrossSectionsPb["T1"]["2445"]= 0.102E-03
	CrossSectionsPb["T1"]["2450"]= 0.991E-04
	CrossSectionsPb["T1"]["2455"]= 0.966E-04
	CrossSectionsPb["T1"]["2460"]= 0.941E-04
	CrossSectionsPb["T1"]["2465"]= 0.918E-04
	CrossSectionsPb["T1"]["2470"]= 0.895E-04
	CrossSectionsPb["T1"]["2475"]= 0.872E-04
	CrossSectionsPb["T1"]["2480"]= 0.850E-04
	CrossSectionsPb["T1"]["2485"]= 0.829E-04
	CrossSectionsPb["T1"]["2490"]= 0.808E-04
	CrossSectionsPb["T1"]["2495"]= 0.788E-04
	CrossSectionsPb["T1"]["2500"]= 0.768E-04
	CrossSectionsPb["T1"]["2505"]= 0.749E-04
	CrossSectionsPb["T1"]["2510"]= 0.730E-04
	CrossSectionsPb["T1"]["2515"]= 0.712E-04
	CrossSectionsPb["T1"]["2520"]= 0.694E-04
	CrossSectionsPb["T1"]["2525"]= 0.677E-04
	CrossSectionsPb["T1"]["2530"]= 0.660E-04
	CrossSectionsPb["T1"]["2535"]= 0.643E-04
	CrossSectionsPb["T1"]["2540"]= 0.627E-04
	CrossSectionsPb["T1"]["2545"]= 0.611E-04
	CrossSectionsPb["T1"]["2550"]= 0.596E-04
	CrossSectionsPb["T1"]["2555"]= 0.581E-04
	CrossSectionsPb["T1"]["2560"]= 0.566E-04
	CrossSectionsPb["T1"]["2565"]= 0.552E-04
	CrossSectionsPb["T1"]["2570"]= 0.538E-04
	CrossSectionsPb["T1"]["2575"]= 0.525E-04
	CrossSectionsPb["T1"]["2580"]= 0.512E-04
	CrossSectionsPb["T1"]["2585"]= 0.499E-04
	CrossSectionsPb["T1"]["2590"]= 0.486E-04
	CrossSectionsPb["T1"]["2595"]= 0.474E-04
	CrossSectionsPb["T1"]["2600"]= 0.462E-04
	CrossSectionsPb["T1"]["2605"]= 0.451E-04
	CrossSectionsPb["T1"]["2610"]= 0.439E-04
	CrossSectionsPb["T1"]["2615"]= 0.428E-04
	CrossSectionsPb["T1"]["2620"]= 0.418E-04
	CrossSectionsPb["T1"]["2625"]= 0.407E-04
	CrossSectionsPb["T1"]["2630"]= 0.397E-04
	CrossSectionsPb["T1"]["2635"]= 0.387E-04
	CrossSectionsPb["T1"]["2640"]= 0.377E-04
	CrossSectionsPb["T1"]["2645"]= 0.368E-04
	CrossSectionsPb["T1"]["2650"]= 0.359E-04
	CrossSectionsPb["T1"]["2655"]= 0.350E-04
	CrossSectionsPb["T1"]["2660"]= 0.341E-04
	CrossSectionsPb["T1"]["2665"]= 0.332E-04
	CrossSectionsPb["T1"]["2670"]= 0.324E-04
	CrossSectionsPb["T1"]["2675"]= 0.316E-04
	CrossSectionsPb["T1"]["2680"]= 0.308E-04
	CrossSectionsPb["T1"]["2685"]= 0.300E-04
	CrossSectionsPb["T1"]["2690"]= 0.293E-04
	CrossSectionsPb["T1"]["2695"]= 0.285E-04
	CrossSectionsPb["T1"]["2700"]= 0.278E-04
	CrossSectionsPb["T1"]["2705"]= 0.271E-04
	CrossSectionsPb["T1"]["2710"]= 0.265E-04
	CrossSectionsPb["T1"]["2715"]= 0.258E-04
	CrossSectionsPb["T1"]["2720"]= 0.251E-04
	CrossSectionsPb["T1"]["2725"]= 0.245E-04
	CrossSectionsPb["T1"]["2730"]= 0.239E-04
	CrossSectionsPb["T1"]["2735"]= 0.233E-04
	CrossSectionsPb["T1"]["2740"]= 0.227E-04
	CrossSectionsPb["T1"]["2745"]= 0.221E-04
	CrossSectionsPb["T1"]["2750"]= 0.216E-04
	CrossSectionsPb["T1"]["2755"]= 0.211E-04
	CrossSectionsPb["T1"]["2760"]= 0.205E-04
	CrossSectionsPb["T1"]["2765"]= 0.200E-04
	CrossSectionsPb["T1"]["2770"]= 0.195E-04
	CrossSectionsPb["T1"]["2775"]= 0.190E-04
	CrossSectionsPb["T1"]["2780"]= 0.185E-04
	CrossSectionsPb["T1"]["2785"]= 0.181E-04
	CrossSectionsPb["T1"]["2790"]= 0.176E-04
	CrossSectionsPb["T1"]["2795"]= 0.172E-04
	CrossSectionsPb["T1"]["2800"]= 0.168E-04
	CrossSectionsPb["T1"]["2805"]= 0.163E-04
	CrossSectionsPb["T1"]["2810"]= 0.159E-04
	CrossSectionsPb["T1"]["2815"]= 0.155E-04
	CrossSectionsPb["T1"]["2820"]= 0.151E-04
	CrossSectionsPb["T1"]["2825"]= 0.148E-04
	CrossSectionsPb["T1"]["2830"]= 0.144E-04
	CrossSectionsPb["T1"]["2835"]= 0.140E-04
	CrossSectionsPb["T1"]["2840"]= 0.137E-04
	CrossSectionsPb["T1"]["2845"]= 0.133E-04
	CrossSectionsPb["T1"]["2850"]= 0.130E-04
	CrossSectionsPb["T1"]["2855"]= 0.127E-04
	CrossSectionsPb["T1"]["2860"]= 0.124E-04
	CrossSectionsPb["T1"]["2865"]= 0.121E-04
	CrossSectionsPb["T1"]["2870"]= 0.118E-04
	CrossSectionsPb["T1"]["2875"]= 0.115E-04
	CrossSectionsPb["T1"]["2880"]= 0.112E-04
	CrossSectionsPb["T1"]["2885"]= 0.109E-04
	CrossSectionsPb["T1"]["2890"]= 0.106E-04
	CrossSectionsPb["T1"]["2895"]= 0.104E-04
	CrossSectionsPb["T1"]["2900"]= 0.101E-04
	CrossSectionsPb["T1"]["2905"]= 0.986E-05
	CrossSectionsPb["T1"]["2910"]= 0.961E-05
	CrossSectionsPb["T1"]["2915"]= 0.937E-05
	CrossSectionsPb["T1"]["2920"]= 0.914E-05
	CrossSectionsPb["T1"]["2925"]= 0.891E-05
	CrossSectionsPb["T1"]["2930"]= 0.869E-05
	CrossSectionsPb["T1"]["2935"]= 0.848E-05
	CrossSectionsPb["T1"]["2940"]= 0.827E-05
	CrossSectionsPb["T1"]["2945"]= 0.806E-05
	CrossSectionsPb["T1"]["2950"]= 0.786E-05
	CrossSectionsPb["T1"]["2955"]= 0.767E-05
	CrossSectionsPb["T1"]["2960"]= 0.748E-05
	CrossSectionsPb["T1"]["2965"]= 0.729E-05
	CrossSectionsPb["T1"]["2970"]= 0.711E-05
	CrossSectionsPb["T1"]["2975"]= 0.694E-05
	CrossSectionsPb["T1"]["2980"]= 0.677E-05
	CrossSectionsPb["T1"]["2985"]= 0.660E-05
	CrossSectionsPb["T1"]["2990"]= 0.644E-05
	CrossSectionsPb["T1"]["2995"]= 0.628E-05
	CrossSectionsPb["T1"]["3000"]= 0.612E-05
	
	
  if model=="Higgsino":
	CrossSectionsPb["Higgsino"]= {}
	CrossSectionsPb["Higgsino"]["100"]= 16797.2/1000
	CrossSectionsPb["Higgsino"]["150"]= 3832.31/1000
	CrossSectionsPb["Higgsino"]["200"]= 1335.62/1000
	CrossSectionsPb["Higgsino"]["250"]= 577.314/1000
	CrossSectionsPb["Higgsino"]["300"]= 284.85/1000
	x, y = array( 'd' ), array( 'd' )
 	keys = sorted(CrossSectionsPb['Higgsino'].keys())
 	n = len(keys)
 	for key in keys:
 		x.append(float(key))
 		y.append(float(CrossSectionsPb['Higgsino'][key])) 		
 	gr = TGraph( n, x, y )
 	CrossSectionsPb["Higgsino"]['graph'] = gr
	
	
	
	
	
	