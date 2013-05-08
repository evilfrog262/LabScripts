#!/usr/bin/env python

import sys

# Takes pileup file as input as well as two text files: one with a list of the start positions of
# PPE regions and one with a list of stop positions of PPE regions.  It produces a pileup file
# as output with the snps in PPE regions removed.

# check for correct commandline arguments
if len(sys.argv) != 5 :
	print("Usage:  PileupPPERemoval.py  <pileup file>  <text file start locations> <text file end locations>  <text file output>")
	sys.exit(0)

# obtain proper I/O files
InFileFastaName = sys.argv[1]
InFileStartName = sys.argv[2]
InFileEndName = sys.argv[3]
OutFileName = sys.argv[4]

# open I/O files for editing
InPile = open(InFileFastaName, 'r')
InStart = open(InFileStartName, 'r')
InEnd = open(InFileEndName, 'r')
OutFile = open(OutFileName, 'w')

# make two integer lists--one for start locations and one for end locations
StartList = []
EndList = []
for Line in InStart :
    Line = Line.strip('\n')
    StartList.append(int(Line))
for Line in InEnd :
    Line = Line.strip('\n')
    EndList.append(int(Line))

PPE = False
EndCount = 0
# iterate through all the lines of the file
for Line in InPile :
    Tokens = Line.split()
    Position = int(Tokens[1])
    # check if base is in a PPE region
    for End in EndList :
        if (Position <= End and Position >= StartList[EndCount]) :
            PPE = True
            print(StartList[EndCount], Position, End)
        EndCount = EndCount + 1
    # if not in PPE region, print to output file
    if not(PPE) :
         OutFile.write(Line)
    PPE = False
    EndCount = 0

# close all used files
OutFile.close()
InStart.close()
InEnd.close()
InPile.close()

