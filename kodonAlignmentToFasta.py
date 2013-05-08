#!/usr/bin/env python

import sys

InFileName = sys.argv[1]      # alignment file
OutFileName = sys.argv[2]     # in group FASTA file
OutFile2Name = sys.argv[3]    # out group FASTA file
numSeqs = int(sys.argv[4])    # total number of sequences
outGroup = int(sys.argv[5])   # location of the outgroup sequence

InFile = open(InFileName, 'r')
OutFile = open(OutFileName, 'w')
OutFile2 = open(OutFile2Name, 'w')

rowCounter = 0
inData = []
seqNames = []
lineNum = 0

for i in range(numSeqs + 2) :
    inData.append([])

for line in InFile :
    row = rowCounter % (numSeqs + 2)
    if (lineNum <= numSeqs) :
        line = line.strip()
        name = line[0:9]
        seq = line[10:]
        seqNames.append(name)
        inData[row].append(seq)
        lineNum = lineNum + 1
    else :  
        line = line.strip()
        inData[row].append(line)
    rowCounter = rowCounter + 1

print(seqNames)

for i in range(1, numSeqs) :
    if (i == outGroup) :
        OutFile2.write(">" + seqNames[i] + "\n")
        for line in inData[i] :
            OutFile2.write(line + '\n')
    else :
        OutFile.write(">" + seqNames[i] + "\n")
        for line in inData[i] :
            OutFile.write(line + '\n')
        OutFile.write('\n')

