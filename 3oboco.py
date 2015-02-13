#copy in same filesystem use mv for chunks
import sys
import subprocess
import os
import errno
import glob

FILE_SIZE_ONEMEGA=1048576
FILE_CHUNKS=32

def generateTempDirectoryForFile(name):
    print "analyzing %s"%name
    fileName, fileExtension = os.path.splitext(name)
    name = "tmp" + fileName
    #create a tmp directory on were to split the file
    error = True
    while error:
        try:
            os.makedirs(name)
            error = False
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
            name=name + "0"
    print "returning name:%s" % name
    return name
  
def calculateChunksSize(name):
    sourceSize = os.stat(name).st_size
    chunks = sourceSize/FILE_SIZE_ONEMEGA
    chunkSize=sourceSize/chunks
    if (chunks>FILE_CHUNKS):
        chunkSize = sourceSize/FILE_CHUNKS
    return chunkSize
    
    
def splitFileWhileCopyChunks(chunkSize, sourceName, sourcePath, destPath):
    #run a split of the file to copy in backgraound
    splitProcess = subprocess.Popen(["split", "--bytes=%s" % chunkSize, sourceName, sourcePath + "/"]) 
    copies = []
    #while splitting poll every chunk, when ready copy to dest directory
    while splitProcess.poll() is None:
        for filename in os.listdir(sourcePath):
            if not filename in copies and os.stat(sourcePath+"/"+filename).st_size == chunkSize:
                copies.append(filename)
                subprocess.Popen("mv %s/%s %s/%s" % (sourcePath,filename,destPath,filename), shell=True)
   
                 
def multiCopyChunks(chunkSize, sourceName, destName):
    commands = []
    offset = 0
    fileSize = sourceSize = os.stat(sourceName).st_size;
    while offset < fileSize:
        commands.append("dd if=%s of=%s bs=1M seek=%s" % (sourceName,destName,offset))
        offset = offset + chunkSize
    print commands
    for p in [subprocess.Popen(cmd, shell=True)
    for cmd in commands]: p.wait()
    print 'wait until next'  


#split the content into up to 32 chunks(value set on FILE_CHUNKS)
def splitFile(chunkSize, name, path):														
    subprocess.call(["split", "--bytes=%s" % chunkSize, name, path + "/"]) 

def mergeChunks(path, filename):
    command = "cat "+path+"/*  > " +filename;
    subprocess.call(command, shell=True)
    
def copyChunks(sourcePath, filename, destPath):
    commands = []
    for filename in os.listdir(sourcePath):
        commands.append("cp %s/%s %s/%s" % (sourcePath,filename,destPath,filename))
    for p in [subprocess.Popen(cmd, shell=True)
    for cmd in commands]: p.wait()
    print 'wait until next'
    
    
try:
    sourceFile=sys.argv[1]
    destFile=sys.argv[2]
    #sourceDirectory = generateTempDirectoryForFile(sourceFile)
    #destDirectory = generateTempDirectoryForFile(destFile)
    chunkSize = calculateChunksSize(sourceFile)
    #splitFile(chunkSize, sourceFile, sourceDirectory)    
    #copyChunks(sourceDirectory, sourceFile, destDirectory)
    #splitFileWhileCopyChunks(chunkSize, sourceFile, sourceDirectory, destDirectory)
    multiCopyChunks(chunkSize, sourceFile, destFile)
    #mergeChunks(destDirectory, destFile)
    #os.spawnl(os.P_NOWAIT, ["rm", "-rf", sourceDirectory])
    #os.spawnl(os.P_NOWAIT, ["rm", "-rf", destDirectory])
except IndexError:
    print "you should specify the source and dest file in that way 3oboco.py source dest"
  
