
#!/bin/env python
import os
import sys
import socket
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import sqlite3
import shutil

compName = socket.gethostname()
env      = os.environ.copy()

# Local modules
if  compName == 'linux4':
  sys.path.append('/home/user/bnc/python')
  
import run_cmd
import measure
import utilDb
import setSCIparams as SCI
import pltChemistry
import pltAvgValuesFromNPZ
import pltAERMOD

def getImcName(inpFile):
  imcName = None
  inpFile = open(inpFile,'r')
  for line in inpFile:
    if 'FILE_NAME' in line:
      imcName = line.split('=')[1].split("'")[1]
  inpFile.close()
  return imcName

class Project(object):
    
  def __init__(self,valDir,rType,runSCI,INIfile,ymdhm=None):
    self.runSCI   = runSCI
    self.INIfile  = INIfile
    self.rType    = rType
    if rType == 'Chemistry':
      self.prjNames = ['tva_980825','tva_980826','tva_990706','tva_990715']
      self.inpDir,self.outDir,self.pltDir = pltChemistry.setChemDir(valDir,ymdhm=ymdhm)
    if rType == 'AERMOD':
      self.prjNames = ['baldwin','bowline','clifty','kinso2','Martin','pgrass','tracy']
      self.inpDir,self.outDir,self.pltDir = pltAERMOD.setAerModDir(valDir,ymdhm=ymdhm)
    if not os.path.exists(self.pltDir):
      os.makedirs(self.pltDir)
      print 'Creating plot directory ',self.pltDir
    print self.inpDir

  def runPrj(self,cpInp=True,oDir='SCICHEM'):
    curDir = os.getcwd()
    for prjName in self.prjNames:
      runDir = os.path.join(self.outDir,prjName,oDir)
      if not os.path.exists(runDir):
        os.makedirs(runDir)
        print 'Creating run directory ',runDir
      os.chdir(runDir)
      # Run SCICHEM
      print 'Running ',prjName,' in ',runDir
      prjDname = os.path.join(self.inpDir,prjName,'SCICHEM',prjName)
      if cpInp:
        if rType == 'Chemistry':
          extList = ['inp','scn','msc','sam']
        else: 
          extList = ['sci'] 
        
        reRun = False
        for ext in extList:
          fName = prjDname+'.'+ ext
          tName = prjName+'.' + ext
          if os.path.exists(fName):
            if not os.path.exists(tName) or os.path.getmtime(tName) < os.path.getmtime(fName):
              reRun = True
              shutil.copy(fName,tName)
              print 'Copy %s to %s'%(fName,tName)
            else:
              print 'Skip copying older %s(%g) to %s(%g)'%(fName,os.path.getmtime(fName),tName,os.path.getmtime(tName))
              logFile = prjName + '.log'
              if not os.path.exists(logFile) or os.path.getmtime(tName) < os.path.getmtime(fName):
                reRun = True
          else:
            print 'Cannot find input file %s'%fName

        if rType == 'Chemistry':
          imcFile = getImcName(prjName+'.inp').strip()
          print 'Copy imc file %s to %s'%(os.path.join(self.inpDir,prjName,'SCICHEM',imcFile),imcFile)
          shutil.copy(os.path.join(self.inpDir,prjName,'SCICHEM',imcFile),imcFile)
      if reRun:
        run_cmd.Command(env,self.runSCI,prjName+'\n','\n')
        print 'Done running ',prjName,' in ',runDir
      else:
        print 'Skip running ',prjName,' in ',runDir,' as reRun is ',reRun
    os.chdir(curDir)
    print 'Done runPrj for ',self.rType
    return
  
  def cmpPrj(self):
    curDir = os.getcwd()
    for prjName in self.prjNames:
      self.setPrjDir(prjName)
      os.chdir(self.prjDir) 
    return
  
  def pltPrj(self,oDir='SCICHEM',pltDir=True,cpSmp=None):
            
    curDir = os.getcwd()
    for prjName in self.prjNames:
      
      if cpSmp is not None:
        if prjName not in cpSmp:
          print prjName,' not in ',cpSmp 
          continue
        else:
          print 'Found ',prjName,' in ',cpSmp
        if os.path.exists(cpSmp):
          fName = os.path.basename(cpSmp)
          ans = raw_input('Copy %s to %s? '%(cpSmp,prjName+'.smp'))
          if len(ans) == 0 or ans[0].upper() == 'Y':
            runDir = os.path.join(self.outDir,prjName,oDir)
            if not os.path.exists(runDir):
              os.makedirs(runDir)
            os.chdir(runDir)            
            shutil.copy(cpSmp,prjName+'.smp')
          else:
            sys.exit()
       
      runDir = os.path.join(self.outDir,prjName,oDir)
      os.chdir(runDir)
      if pltDir:
        dstDir = self.pltDir
      else:
        dstDir = None
      print 'pltDir = ',runDir  
      if rType == 'Chemistry':
        pltChemistry.cmpTva(self.inpDir,prjName)
        pltChemistry.createSubPlots(prjName,dstDir=dstDir,skip99=True,color=True)
        pltAvgValuesFromNPZ.pltAvgData(prjName)
      else:
        inpDir = os.path.join(self.inpDir,prjName)
        pltAERMOD.cmpAerMod(inpDir,prjName,dstDir=dstDir,color=True)
      
    os.chdir(curDir)
    print 'Done pltPrj'
    return
    
#########################################
#Main loop for TVA Validation 
#########################################
if __name__ == '__main__':

  # Use to copy an existing sampler for plots
  cpSmp  = None
  outDir = None

  if compName == 'linux':    
    valDir          = '/home/user/bnc/TestSCICHEM'
    SCIPUFF_BASEDIR = '/home/user/bnc/SCICHEM_3.0/bin/linux/ifort'
    INIfile         = '/home/user/bnc/SCICHEM_3.0/scidata/scipuff.ini'
    env["LD_LIBRARY_PATH"] = "/home/user/bnc/SCICHEM3.0/lib/linux/hdf/hdf5-1.8.7-linux-x86_64-shared/lib"
    env["LD_LIBRARY_PATH"] = env["LD_LIBRARY_PATH"] + ':' + SCIPUFF_BASEDIR
    print "LD_LIBRARY_PATH = " + env["LD_LIBRARY_PATH"] 
  
  runSCI    = os.path.join(SCIPUFF_BASEDIR,'runsci')
  INIfile   = "-I:" + INIfile
  runSCI    = [runSCI,INIfile]
  scriptDir = os.path.join(valDir,'Scripts')
  
  # Set Logicals
  
  lrunPrj = True
  lcmpPrj = False
  
  if cpSmp is not None:
    lrunPrj = False
    
  lpltPrj = True
  outDir  = '170327'
  
  # Set Types
  runTypes = ['AERMOD','Chemistry']
  
  # Project
  for rType in runTypes:
    
    myProjects = Project(valDir,rType,runSCI,INIfile,ymdhm=outDir)
    
    if lrunPrj:
      myProjects.runPrj(cpInp=True,oDir='SCICHEM')
      print 'Run projects completed'
    if lcmpPrj:
      myProjects.cmpPrj()
    if lpltPrj:
      myProjects.pltPrj(oDir='SCICHEM',pltDir='Plots',cpSmp=cpSmp)
      print 'Plot projects completed'  
      
  print 'Done ;)'
