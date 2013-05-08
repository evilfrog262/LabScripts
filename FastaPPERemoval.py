#!/usr/bin/env python

import sys

# Removes desired regions of the genome from FASTA file input.  Specifically for
# use on PE/PPE genes and IS regions.  Requires two input files: one that lists
# the starting locations of all the removal regions and one that lists all the
# ending locations of all the removal regions.  In both files, each number should
# have its own line, and nothing else should be in the file.  Produces FASTA
# output.  A blank file "intermediate.txt" should exist in the directory where
# the program is running for use by the program.

# check for correct commandline arguments
if len(sys.argv) != 6 :
	print("Usage:  FastaPPERemoval.py  <FASTA file>  <text file start locations> <text file end locations>  <text file output>  intermediate.txt")
	sys.exit(0)

# obtain proper I/O files
InFileFastaName = sys.argv[1]
InFileStartName = sys.argv[2]
InFileEndName = sys.argv[3]
OutFileName = sys.argv[4]
IntFileName = sys.argv[5]

# open I/O files for editing
InFasta = open(InFileFastaName, 'r')
InStart = open(InFileStartName, 'r')
InEnd = open(InFileEndName, 'r')
OutFile = open(OutFileName, 'w')
IntFile = open(IntFileName, 'r+')

# remove first line of FASTA and all newlines
Header = ""  # store file header for later re-print
First = True
for Line in InFasta :
    if First :
        Header = Line
        First = False
    else :
        Line = Line.strip('\n')
        IntFile.write(Line)
# reset position to beginning of file
IntFile.write('\n')
IntFile.seek(0)
OutFile.write(Header)

# make two integer lists--one for start locations and one for end locations
StartList = []
EndList = []
for Line in InStart :
    Line = Line.strip('\n')
    StartList.append(int(Line))
for Line in InEnd :
    Line = Line.strip('\n')
    EndList.append(int(Line))

# iterate through each character in the FASTA file and remove unwanted regions
CharCount = 1
ListCount = 0
Start = 0
End = 0
PPE = False
for Line in IntFile :
    for char in Line :
        if CharCount in StartList :
            Start = StartList[ListCount]
            End = EndList[ListCount]
            ListCount = ListCount + 1
            PPE = True
        if PPE :
            if CharCount >= End :
                PPE = False
                OutFile.write(str(char))
        else :
            OutFile.write(str(char))
        CharCount = CharCount + 1
    else :
        break   
        
