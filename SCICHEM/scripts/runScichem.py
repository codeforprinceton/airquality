#!/bin/python

import os
import re
import sys
import platform
import subprocess

print 
if platform.system() == "Linux":
  binDir      = "/home/user/bnc/scipuff/Repository/export/EPRI/SCICHEM_3.0/SCICHEM_3.1_161013/bin/linux/ifort"
  hdfDir      = "/home/user/sid/hdf5-1.8.7-linux-x86_64-shared/lib"
  iniFile     = "../../../scipuff.ini"
elif platform.system() == "Windows":
  binDir      = "C:\\EPRI\\SCICHEM3.0\\bin\\windows\\x64"
  hdfDir      = "C:\\EPRI\\SCICHEM3.0\\bin\\windows\\x64"
  iniFile     = "C:\\EPRI\\SCICHEM3.0\\bin\\windows\\x64\\scipuff.ini"
else:
  print 'Unknown system ',platform.system()
  sys.exit()
  
env     = os.environ.copy()
env["LD_LIBRARY_PATH"] = "%s:%s" % (binDir,hdfDir)
runSciCmd  = [os.path.join(binDir,'runSCI'),'-I:%s'%iniFile]
sciPostCmd = [os.path.join(binDir,'sciDOSpost'),'-I:%s'%iniFile,'-i']

def checkRun(prjName):
  logName = "%s.log"%prjName
  runSuccess = False
  if os.path.exists(logName):
    tLines = []
    with open(logName) as logFile:
      for line in logFile:
        tLine = re.findall(r'Normal termination detected at Time',line)
        if tLine:
          tLines.append(tLine)
    if len(tLines) == 2:
      runSuccess = True
    logFile.close()
  return runSuccess
  
def runSci(prjName):
  cwd = os.getcwd()
  runsci_out = open('scipp.output','w')
  runsci_err = open('scipp.error','w')
  cmd = runSciCmd + ['-P:%s'%prjName]
  print 'Running "%s" in "%s"'%(cmd,cwd)
  h = subprocess.Popen(cmd, env=env, bufsize=0, shell=False,stdout=runsci_out,stderr=runsci_err)
  h.communicate()
  runsci_out.close()
  runsci_err.close()

def runScipp(sciPostinp):
  cwd = os.getcwd()
  scipp_out = open('scipp.output','w')
  scipp_err = open('scipp.error','w')
  cmd = sciPostCmd + [sciPostinp]
  print 'Running "%s" in "%s"'%(cmd,cwd)
  h = subprocess.Popen(cmd, env=env, bufsize=0, shell=False,stdout=scipp_out,stderr=scipp_err)
  h.communicate()
  scipp_out.close()
  scipp_err.close()
  
if __name__ == '__main__':

  # Set project name for running SCICHEM
  prjName = 'no2-2005-mc'
  #os.chdir('no2_mc_2005')
  
  # Check if already successfully run. If so confirm rewrite.
  reRun = True
  if checkRun(prjName):
    ans = raw_input('Project successfully completed earlier. Rerun project again? (Y/N) : ')
    if ans[0].upper() == 'Y':
      reRun = True
    else:
      reRun = False
  
  # Run the SCICHEM model for prjName  
  if reRun:
    runSci(prjName)
  
  # Set input file for sciDOSPost post processor
  sciPostinp = 'sciDOSpost.inp'
  
  # Run sciDOSPost SCICHEM postprocessor with SciPostinp input file
  runScipp(sciPostinp)
