#!/usr/bin/env python

# This program takes a text file as input.  This text file should be output from Mauve that 
# lists SNPs from all the sequences.  It produces a text file as output that is identical
# to the original Mauve output except that all SNPs involving ambiguous N's are removed.

import sys

# check for correct commandline arguments
if len(sys.argv) != 3:
    print("Usage: MauveSnpsWithNRemoval.py <input file> <output file>")
    sys.exit(0)

# obtain and open input/output files
InFileName = sys.argv[1]
OutFileName = sys.argv[2]
InFile = open(InFileName, 'r')
OutFile = open(OutFileName, 'w')

# iterate through and check all lines in the file
firstLine = True
for Line in InFile :
    # copy the first line into the output file
    if firstLine :
        OutFile.write(Line)
        firstLine = False  
    # if the other lines contain valid SNPs, copy them too
    else :
        elements = Line.split("\t")
        SNPS = elements[0]
        if ('A' in SNPS and 'C' in SNPS) or ('A' in SNPS and 'G' in SNPS) or ('A' in SNPS and 'T' in SNPS) or ('C' in SNPS and 'G' in SNPS) or ('C' in SNPS and 'T' in SNPS) or ('G' in SNPS and 'T' in SNPS):
            OutFile.write(Line)
        
InFile.close()
OutFile.close()
             
