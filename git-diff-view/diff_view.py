#!/usr/bin/env python3

# Take a review directory, like /tmp/20080813_14450,
#   1 read _file.list
#   2 print out a list of files for reviews
#   3 use vimdiff to review the diff

import sys, string, re, os
import argparse

# vertical filler to make alignment nice; more context is better; I don't use icase, iwhite
vimdiff="vim +\":set nu\" +\":set nospell\" +\":syntax off\" +\":set diffopt=vertical,filler,context:8\""

def Main():
   parser = argparse.ArgumentParser()
   parser.add_argument("-l", "--localDiff", action='store_true', help="diff local dir")
   parser.add_argument("-k", "--tkDiff", action='store_true', help="use tkdiff instead of vim diff")
   parser.add_argument("-n", "--autoNext", action='store_true', help="automatically open next file")
   parser.add_argument("reviewDir", nargs="?", help="review dir") 
   args = parser.parse_args()

   if not args.reviewDir:
      parser.print_help()
      sys.exit(10)

   needToDeleteDiffDir = False
   reviewDir = args.reviewDir

   # Untar if needed
   if os.path.isfile(reviewDir):
      os.system("tar zxvf %s -C /tmp >/dev/null"%reviewDir)
      reviewDir = "/tmp/%s"%(os.path.basename(reviewDir)[:-4])
      needToDeleteDiffDir = True
   else:
      assert(os.path.isdir(reviewDir))
   # Parse _file.list from reviewDir
   idxFileName = "%s/_file.list"%reviewDir
   if not os.path.isfile(idxFileName):
      print("Cannot find _file.list in the review directory!")
      sys.exit(1)
   f = open(idxFileName)
   prefix = reviewDir
   files = []
   for line in f.readlines():
      files.append(line[:-1])
   f.close()
   # Now invoke vimdiff
   i = -1;
   while i < len(files):
      if args.autoNext:
         i += 1
      else:
         printFiles(files);
         print("Next/Previous/exit(N/p/x/<number>)?")
         input = sys.stdin.readline();
         try:
            i = int(input)
         except:
            if (input.lower() == "x\n"):
               break
            elif (input.lower() == "p\n"):
               i = i - 1
               if i < 0:
                  i = 0
            else:
               i += 1
      if not (i >= 0 and i < len(files)):
         break
      file = files[i]
      absFile = "%s/%s"%(prefix, file)
      if args.localDiff:
         absFile = FindLocalFile(file)
      if args.tkDiff:
         runInBackground = "&"
         if args.autoNext:
            runInBackground = ""
         os.system("tkdiff %s/%s.BASE %s %s" % (prefix, file, absFile, runInBackground)) 
      else:
         os.system("%s %s +\":silent diffsplit %s/%s.BASE\" +\":set nonu\""%(vimdiff, absFile, prefix, file))
   if needToDeleteDiffDir:
      os.system("rm -rf %s"%reviewDir)

def FindLocalFile(filename):
   tok = filename.split('/')
   for i in range(len(tok)):
      f = "/".join(tok[i:])
      if os.path.exists(f):
         return f
   assert(0)

def printFiles(files):
   i = 0;
   while i < len(files):
      print("%s [%d]"%(files[i], i))
      i += 1
   return

Main()

