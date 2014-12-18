import sys, os, traceback, shutil, time, subprocess, datetime

from ccpnmodel.util import Path as modelPath
from ccpncore.util import Path as corePath

from ccpncore.util import Io as utilIo
from ccpncore.util import Logging

testDataPath = 'testdata/upgrade/'

alwaysSkipDirs = {'.svn', '.idea', 'ccp', 'ccpnmr', 'cambridge', 'CVS', 'molsim', 'utrecht',}
stdTempDir='temp'
stdOutDir='out'
stdJunkDir='junk'


def doTest(target=None, workDir=None, maskErrors=True):
  """ Wrapper routine for testing. 
  Accepts directory, .tgz or Implementation.xml file as target
  """
           
  # set up directories
  if workDir is None:
    workDir = os.getcwd()

  xx = datetime.date.today()
  today = '%02d%02d%02d' % (xx.year, xx.month, xx.day)
  testDir = 'compatibility_test_%s' % today
  testDir = os.path.join(workDir, testDir)
  if not os.path.exists(testDir):
    os.makedirs(testDir)

    
  if target:
    target = corePath.normalisePath(target)
  else:
    # We are testing all projects.
    target = modelPath.getDirectoryFromTop(testDataPath)
  
  if os.path.isfile(target):
  
    if target.endswith('.tgz'):
      newTarget = unzipFile(target, testDir)
      testProjects(newTarget, testDir, maskErrors=maskErrors)
                 
    elif target.endswith('.xml'):
      outDir = corePath.joinPath(testDir, stdOutDir)
      testProject(target, outDir)
    
    else:
      print('Not a valid testing target: ', target)
  
  else:
    testProjects(target=target, workDir=testDir, maskErrors=maskErrors)

def unzipFile(target, workDir):
  print('Unzipping %s ...' % target)
  tempDir = os.path.join(workDir, stdTempDir)
  junkDir = os.path.join(workDir, stdJunkDir)
  if os.path.exists(tempDir):
    if os.path.isdir(junkDir):
      shutil.rmtree(junkDir)
    shutil.move(tempDir, junkDir)
  os.makedirs(tempDir)
  
  subprocess.call(['tar', '-xzf', target, '-C', tempDir])
  #
  return tempDir


def testProjects(target, workDir, extraDirs=None, maskErrors=True):
  """ Test all potential projects (.../memops/Implementation/*.xml or *.tgz)
  within directory target, putting temporary directories in workDir
  """
  
  #print 'Testing Projects in %s' % target

  # # Make dummy project as location for logs
  # now ='_'.join((str(x) for x in datetime.datetime.now().timetuple()[:6]))
  # dummyProject = utilIo.newProject('Logs_%s' % now, path=workDir, removeExisting=True)
  logger = Logging.getLogger()

  outDir = corePath.joinPath(workDir, stdOutDir)
  if extraDirs:
    outDir = corePath.joinPath(outDir, extraDirs)
  
  work = None
  for dirpath, dirnames, filenames in os.walk(target):
    
    if dirpath.endswith('/memops/Implementation'):
      projDir = (os.path.dirname(os.path.dirname(dirpath)))
      # potential project:
      try:
        work = True
        logger.info("Testing %s ..." % projDir)
        testProject(projDir, corePath.joinPath(outDir, projDir[len(target)+1:]))
      except:
        if maskErrors:
          # print(">>>>Error>>>> %s" % projDir)
          # print(traceback.format_exception_only(sys.exc_info()[0],sys.exc_info()[1]))
          # print()
          logger.exception("Error in test of %s" % projDir)
        else:
          raise
    else:
      for fn in sorted(filenames):
        if fn.endswith('.tgz'):
          targetFile = corePath.joinPath(dirpath, fn)
          try:
            work = True
            newTarget = unzipFile(targetFile, workDir)
            xx = dirpath[len(target)+1:]
            if extraDirs:
              xx = os.path.join(extraDirs, xx)
            testProjects(newTarget, workDir, extraDirs=xx,
                         maskErrors=maskErrors)
          except:
            if maskErrors:
              logger.exception("Error in test of %s" % projDir)
              # print(">>>>Error>>>> %s" % targetFile)
              # print(traceback.format_exception_only(sys.exc_info()[0],sys.exc_info()[1]))
              # print()
            else:
              raise
        
          
    dirnames[:] = sorted([x for x in dirnames if x not in alwaysSkipDirs])
  #
  if work is None:
    raise Exception("Error, No work done in directory %s" % target)

def testProject(target, outDir):
  """ Test a single project
  target is the directory containing it, or the Implementation.xml file
  outDir the directory to which it is written
  """
  # print('Testing %s ...' % target)
  if target.endswith('.xml'):
    dirpath, fileName = os.path.split(target)
    projectName = fileName[:-4]
    target = os.path.dirname(os.path.dirname(dirpath))
  else:
    projectName = None

  t0 = time.time()
  ccpnProject = utilIo.loadProject(target, projectName=projectName)
  # t1 = time.time()
  utilIo.loadAllData(ccpnProject)
  # t2 = time.time()
  ccpnProject.checkAllValid(complete=True)
  # t3 = time.time()
  if not os.path.exists(outDir):
    os.makedirs(outDir)

  logger = Logging.getLogger()

  newPath = outDir
  for extra in (os.path.basename(target), ccpnProject.name):
    if extra not in newPath:
      newPath = corePath.joinPath(newPath, extra)
  logger.info('### saving %s to %s' % (ccpnProject.name, newPath))
  utilIo.saveProject(ccpnProject, newPath=newPath, newProjectName=ccpnProject.name,
                     removeExisting=True)
  t4 = time.time()
  #print ('+++ Project Load ', t1-t0)
  #print ('+++ AllData Load ', t2-t1)
  #print ('+++ Project Test ', t3-t2)
  #print ('+++ Load and test', t3-t0)
  #print ('+++ Project Save ', t4-t3)
  logger.info(('+++ Testing OK, project %s. Total time %s. %s  '
         % (ccpnProject.name , t4-t0, target)))
  utilIo.cleanupProject(ccpnProject)
  del ccpnProject
  

if __name__ == '__main__':

  if len(sys.argv) < 2:
    print(" Need either a .xml or .tgz package, a directory, or 'all' as input.")
    sys.exit()

  targetarg = sys.argv[1]

  if targetarg == 'all':
    doTest(maskErrors=False)
  else:
    doTest(targetarg, maskErrors=False)
    #doTest(targetarg)
  

