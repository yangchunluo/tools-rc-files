#!/usr/bin/env python

# called from git diff to:
#   1. make a review directory in /tmp/ using date and parent pid, if not already there
#   2. append file name in /tmp/<data_ppid>/_file.list
#   3. copy the old and new version of the files according to the relative path

import sys, os, datetime

# filler to make alignment nice; more context is better; I don't use icase, iwhite
vimdiff="vim +\":set nu\" +\":syntax off\" +\":set diffopt=vertical,filler,context:8\""

prefix="/tmp"

def Main():
   ppid = os.getppid()
   assert(ppid != 0)
   today = datetime.datetime.now().strftime("%Y%m%d")
   dir = "%s/%s_%05d"%(prefix, today, ppid)
   idxFilePath = "%s/_file.list"%dir
   gitFilePath = sys.argv[1]
   gitOldFilePath = sys.argv[2]
   gitNewFilePath = sys.argv[5]
   copyOldFilePath = "%s/%s.BASE"%(dir, gitFilePath)
   copyNewFilePath = "%s/%s"%(dir, gitFilePath)
   os.system("mkdir -p %s"%dir)
   os.system("touch %s"%idxFilePath)
   idxFile = open(idxFilePath, "a")
   if 0 == idxFile.tell():
      print(dir)
   idxFile.write("%s\n"%gitFilePath);
   idxFile.close()
   #print gitFilePath, gitOldFilePath, gitNewFilePath, copyOldFilePath, copyNewFilePath
   copyFile(gitOldFilePath, copyOldFilePath)
   copyFile(gitNewFilePath, copyNewFilePath)
   return

def copyFile(fromPath, toPath):
   # TODO (x): properly handle symlinked dirs.
   os.system("mkdir -p  \"%s\"" % os.path.dirname(toPath))
   if not os.path.isdir(os.path.dirname(toPath)):
       return
   fromFile = open(fromPath, "r")
   toFile = open(toPath, "w")
   for line in fromFile.readlines():
      toFile.write(line)
   fromFile.close()
   toFile.close()
   return

Main()

