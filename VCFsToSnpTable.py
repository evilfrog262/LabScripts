#!/bin/usr/env python

import sys

#####################
# This script takes a variable number of input vcf files.  Each vcf file must contain
# snp information about only one strain.  At least one input file must be supplied.  The
# name of an output file must also be supplied, and output is in snpt able format.  The 
# output contains the combined information about all strains.
# NOTE : position for indels is the locus before the insertion or deletion
#############

snpDict = {}
locs = []

# check for correct number of inputs
if len(sys.argv) < 3 :
     print("Usage: VCFsToSnpTable.py <input vcf 1> ... <input vcf n> <output file>")
     System.exit(0)

###################
# This function parses data from a given file and adds it to a dictionary indexed
# by snp position.  Each entry is a list of tuples (strain, ref base, and snp) with
# info about snps that occur at that position.
#####
def getData(inFile, snpDict, locs) :

    for line in inFile :
	if ("#" in line) :
	    if ("CHROM" in line and "POS" in line and "ID" in line) :
	        line = line.strip()
		tokens = line.split()
		strain = tokens[9]
        else :
            line = line.strip()
	    tokens = line.split()
            # each tuple contains strain name, reference base and snp
	    tup = strain, tokens[3], tokens[4]
	    # if key already in dictionary, add tuple to that list
	    if (tokens[1] in snpDict.keys()) :
               snpDict[tokens[1]].append(tup)
	    # if not, make new list associated with that key and add tuple
            else :
		snpDict[tokens[1]] = []
		snpDict[tokens[1]].append(tup)
	        # add locus to list if not already there
	        locs.append(tokens[1])

    return snpDict


#########
# start of main execution, process all input ifles
#####
for n in sys.argv[1:(len(sys.argv) - 1)] :
    
    inFile = open(n, "r")

    # parse data into a dictionary indexed by locus of snp
    getData(inFile, snpDict, locs)

    inFile.close()

# open output file for writing

outFile = open(sys.argv[(len(sys.argv) - 1)], 'w')

# print out data from snp dictionary
for loc in locs :
    if (len(snpDict[loc][0][1]) <= 1) :
        for tup in snpDict[loc] :
	    outFile.write(tup[0] + "\tlocus " + loc + "\t" + tup[1] + "->" + tup[2] + "\n")
    else :
        length = len(snpDict[loc][0][1])
	outFile.write("\t\t\t\tdel " + str(length) + "bp\n")
	for tup in snpDict[loc] :  
	    outFile.write(tup[0] + "\tlocus " + loc + "\t" + tup[1] + "->" + tup[2] + "\n")

outFile.close()

