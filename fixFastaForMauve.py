#!/usr/bin/env python

import sys

# check for proper input
if len(sys.argv) != 3 :
    print("Usage: fixFastaForMauve.py <input fasta> <output file>")
    sys.exit(-1)

# set up I/O files
InFileName = sys.argv[1]
OutFileName = sys.argv[2]

# open files for editing
InFile = open(InFileName, 'r')
OutFile = open(OutFileName, 'w')

# count number of lines to be kept
Counter = 0
FinalCount = 0
for Line in InFile :
   Line = Line.upper()
   if (Line != "+\n") :
       Counter = Counter + 1
   if (Line == "+\n") :
       FinalCount = Counter
print(str(Counter) + '\n' + str(FinalCount)) 

# copy the needed lines into the output file
InFile.seek(0)
Counter = 0
for Line in InFile :
    # replace first '@' with '>'
    if (Counter == 0) :
        Line = Line.replace('@','>',1)
    # convert remaining lines to upper case
    else :
        Line = Line.upper()
    if (Counter < FinalCount) :
        OutFile.write(Line)
        Counter = Counter + 1

