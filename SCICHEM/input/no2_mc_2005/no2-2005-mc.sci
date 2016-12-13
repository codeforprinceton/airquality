**
****************************************
**
** EPRI NO2 Example for SCICHEM 3.0(Beta3)
** Created by Ramboll-ENVIRON & Sage-Xator
** Multicomponent simulation with near-source NO-NO2-O3 chemistry
**
****************************************
**
**
****************************************
** SCICHEM Control Pathway
****************************************
**
**
CO STARTING
   TITLEONE EPRI NO2 Example/Tutorial with Short Range Chemistry
   TITLETWO hourly O3 data
   POLLUTID TRAC
   PROJECTN UTM WGS84 11 N KM
** xMin xMax yMin yMax zMax
   DOMAIN  560.38 560.78 4824.7 4825.1 2000.
   TIMEZONE -7   
   STARTEND 2005 1 1 0  2005 12 31 24
CO FINISHED

MA STARTING
MA MATCLASS trac Gas
MA DESCRPTN This is ignored
MA DENSITY  trac 1.2
MA GASDEPOS trac 0.0
MA IMCFILE  'no2.imc'
MA FINISHED

**
****************************************
** SCICHEM Source Pathway
****************************************
**
**
SO STARTING
** Source Location **
** Source ID -              Type       X Coord. Y Coord. Z Coord.**
   LOCATION FIREPUMP        POINT      560.58  4824.85  848.000
** Multicomponent species ** must come before SRCPARAM and after LOCATION
   MULTCOMP  NO2 NO
** Source Parameters **
**                          emis   hgt    tmp    vel    dia     species emissions (corresponding to MULTCOMP list)
   SRCPARAM FIREPUMP        1.0e3  8.53   622.0  57.4   0.127  0.375525 1.387583
** Hourly emissions file
   HOUREMIS no2-2005-mc.emi
SO FINISHED
**

** Receptors
**RE STARTING
** Species to be output in sampler file
***RE MULTLIST (NO2,NO,O3)
***RE ELEVUNIT METERS
*** Use post processor SCIPP with no2-2005-mc.sam
**RE FINISHED

** Meteorology
ME STARTING
ME SCISFC KBOI2005.SFC
ME SCIPRF KBOI2005.PRF
ME FINISHED
