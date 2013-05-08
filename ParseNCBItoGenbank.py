#!/bin/usr/env python

import sys
import re

# Takes an NCBI genbank file as input as well as a list of gene names in a text file 
# that should be in the following format :
# RV0001
# RV0002
# RV0003, etc.
# All genes in this list will be kept, others will be eliminated.  Output is a genbank
# file with the same format.

if len(sys.argv) != 4 :
    print("Usage: ParseNCBIToFasta.py  <input genbank file>  <gene list>  <output file name>")
    sys.exit(0)

# open files for I/O
genBankFileName = sys.argv[1]
geneListName = sys.argv[2]
outFileName = sys.argv[3]
gbFile = open(genBankFileName, 'r')
geneFile = open(geneListName, 'r')
outFile = open(outFileName, 'w')

seqStart = False    # true when fasta sequence has been reached
lookForName = False # true when have found gene locus but not name
geneStart = False
geneName = ""
lineNum = 0
startPos = 0
currLoc = 1	    # the start position for the next kept gene
startDict = {}      # dictionary of start positions with gene names as keys
stopDict = {}       # dictionary of stop positions with gene names as keys
newStartsList = {}	    # dictionary of updated start positions
newStopsList = {}	    # dictionary of updated stop positions
geneOffsets = {}	    # dictionary of genes and thier offset from original position
wholeSeq = []	    # list of all bases in sequence
keepSeq = []	    # list of bases in sequence that are kept
geneList = []	    # list of gene names that we want to keep
geneAndLineNum = []

# make a list of names of genes we want to keep
for gene in geneFile :
    gene = gene.strip()
    geneList.append(gene)
geneFile.seek(0)

# skip over header -- start with first "gene" line
for line in gbFile :
    # process gene info until scanner reaches start of fasta sequence
    if not(seqStart) :
        # check whether scanner has hit beginning of Fasta sequence
        originCheck = line.strip()
        if(originCheck == "ORIGIN") :
	    seqStart = True
        # obtain start and stop base positions for current gene
        if 'gene' in line :
	    if "complement" in line :
		line = line.strip()
                tokens = re.split(r'[ .()]+', line)
	        if (tokens[0] == "gene") :
	            currStart = int(tokens[2])
	            currStop = int(tokens[3])
	            lookForName = True
		    geneStart = True;
		    # keep track of start position to associate it with gene name
                    startPos = lineNum
	    else :
	        line = line.strip()
                tokens = re.split(r'[ .]+', line)
	        if (tokens[0] == "gene") :
	            currStart = int(tokens[1])
	            currStop = int(tokens[2])
	            lookForName = True
		    geneStart = True;
		    # keep track of start position to associate it with gene name
                    startPos = lineNum
        # check if the line may contain a gene name
        if lookForName and "locus_tag" in line :  
	    line = line.strip()
	    tokens = line.split("\"")
	    geneName = tokens[1]
	    # get the gene name and add its start and stop locations to dictionaries
	    startDict[geneName] = currStart - 1  # subtract 1 b/c array index starts at 0
	    stopDict[geneName] = currStop - 1
	    lookForName = False
	    # if it is a gene we want to keep, get its information
	    if (geneName in geneList) :
		# calculate the updated start and stop positions (with other parts removed)
		currLength = currStop - currStart
		newStart = currLoc
		newStop = currLoc + currLength
		currLoc += (currLength + 1)
		offset = currStop - newStop
		# add tuple of found gene name and position to list
	        tup = geneName, startPos
                geneAndLineNum.append(tup)
		# add updated start and stop positions to dictionaries
		newStartsList[geneName] = newStart
		newStopsList[geneName] = newStop
		# add gene name and its offset to dictionary
		geneOffsets[geneName] = offset
	# print all header text
        if (not geneStart) :
            outFile.write(line)
    # put each base from fasta sequence into an array
    else :
	line = line.strip()
	tokens = line.split()
	for i in range(1, len(tokens)) :
	    word = tokens[i]
	    for char in word :
		wholeSeq.append(char)
    lineNum += 1

# reset variables
seqStart = False    # true when fasta sequence has been reached
printLine = False   # true when desired gene line is found
lineNum = 0
listIndex = 0
# iterate through file again and print out desired genes
gbFile.seek(0)
for line in gbFile :
    # info to check if beginng of dna sequence has been reached
    originCheck = line.strip()
    originCheck = originCheck.split()
    if len(originCheck) > 0 :
        originCheck = originCheck[0]
    # check if line begins info about a new gene
    if 'gene' in line :
        tempLine = line.strip()
        tokens = re.split(r'[ .]+', tempLine)
	if (tokens[0] == "gene") :
            if (listIndex < len(geneAndLineNum) and lineNum in geneAndLineNum[listIndex]) :
		# if it does, print out the updated position
		name = geneAndLineNum[listIndex][0]
	        listIndex += 1
		if "complement" in line :
		    outFile.write("     gene\t     " + "complement(" + str(newStartsList[name]) + ".." + str(newStopsList[name]) + ")\n")
		else :
		    outFile.write("     gene\t     " + str(newStartsList[name]) + ".." + str(newStopsList[name]) + "\n")
		printLine = True
	    else :
		printLine = False
        elif (printLine) :
	    outFile.write(line)
    elif ("CDS" in line) and (printLine) :
	# update position in all CDS lines
	tempLine = line.strip()
	tokens = line.split()
	if (tokens[0] == "CDS") :
	    name = geneAndLineNum[listIndex - 1][0]
	    if "complement" in line :
		    outFile.write("     CDS\t     " + "complement(" + str(newStartsList[name]) + ".." + str(newStopsList[name]) + ")\n")
	    else :
		    outFile.write("     CDS\t     " + str(newStartsList[name]) + ".." + str(newStopsList[name]) + "\n")
    elif ("misc_feature" in line) and (printLine) :
	# update positions of all miscellaneous features
	tokens = line.strip()
	tokens = re.split(r'[ .()]+', tokens)
	name = geneAndLineNum[listIndex - 1][0]
	tempOffset = geneOffsets[name]
	if "complement" in line :
	    miscStart = int(tokens[2])
	    miscStop = int(tokens[3])
	    outFile.write("     misc_feature    complement(" + str(miscStart - tempOffset) + ".." + str(miscStop - tempOffset) + ")\n")
	else :
	    miscStart = int(tokens[1])
	    miscStop = int(tokens[2])
	    outFile.write("     misc_feature    " + str(miscStart - tempOffset) + ".." + str(miscStop - tempOffset) + "\n")
    # if start of dna sequence has been reached, stop printing
    elif originCheck == "ORIGIN" :
	printLine = False
    else :
	if printLine :
	    outFile.write(line)
    lineNum += 1

# go through sequence and put genes to keep into new array
for gene in geneFile :
    gene = gene.strip()
    start = startDict[gene]
    stop = stopDict[gene]
    for i in range(start, stop + 1) :
        keepSeq.append(wholeSeq[i])

# output the sequence into the new genbank file
outFile.write("ORIGIN")
baseCount = 0
for char in keepSeq :
    # if reached end of one line of sequence
    if (baseCount%60 == 0) :
        outFile.write("\n")
	myStr = str(baseCount+1)
	myStr = myStr.rjust(9)
        outFile.write(myStr + " ")
    # add a space between every ten bases
    elif (baseCount%10 == 0) :
        outFile.write(" ")
    outFile.write(char)
    baseCount += 1
