#!/usr/bin/env python
	
import sys 

# This script takes an alignment file (specifically from Kodon) and performs
# the McDonald-Kreitman test on the sequences in that alignment.  The input
# alignment file must contain only coding regions of the genomes.  A codon
# dictionary also must be input as a reference for codons and their 
# corresponding amino acids.

# if the incorrect number of arguments is given, explain correct usage
if (len(sys.argv) != 5) :
    print("Usage: python parseAlignments.py <codon chart file> <alignment file> <number of outgroup sequence> <total number of sequences>")
    sys.exit(0)

# set up I/O files
Codons = open(sys.argv[1], 'r')   # text file with one column of codons and another of amino acids
InFile1 = open(sys.argv[2], 'r')  # alignment file input
outGroupLine = int(sys.argv[3])   # number of out group sequence in alignment file
numSeqs = int(sys.argv[4])

AllSnps = open("allSnpsFromParse.txt", 'w')

codonDict = {} # dictionary of codons to amino acids
outData = [] # array of chars in outgroup sequence
inData = [] # array of chars in ingroup sequences, each sequence has own row

# make a dictionary of codons and the amino acids they represent
for line in Codons :
    line = line.strip()
    tokens = line.split('\t')
    codonDict[tokens[0]] = tokens[1]
print("Dictionary Done.")

# count the number of invdividual sequences in the file
#line = InFile1.readline()
#print(line)
#while(line != "\n") :
#    numSeqs = numSeqs + 1
#    line = InFile1.readline()
#numSeqs = numSeqs - 1   # because first line isn't a sequence
#print("Sequences counted.")

# make an array to hold all sequences, each with its own row
for i in range(numSeqs - 1) :
    inData.append([])

# start back at the beginning of file and go through all sequences
InFile1.seek(0)
counter = 0  # the line number
blankCounter = (-1 - numSeqs)
rowCounter = 0 # the row of the inGroup array where sequence should be added

for line in InFile1 :
    # out group sequences are at lines where line number % (numSequences + 2) = 1
    if ((counter%(numSeqs + 2)) == outGroupLine) :
        line = line.strip()
        tokens = line.split()
        for char in tokens[0] :
            outData.append(char)
    # if not an out group sequence or blank line or number line, add to ingroup
    elif ( ((blankCounter % (numSeqs + 2)) != 0) and ((counter % (numSeqs + 2)) != 0)) :
        line = line.strip()
        tokens = line.split()
        for char in tokens[0] :
            inData[rowCounter].append(char)
        rowCounter = rowCounter + 1
        if (rowCounter == numSeqs - 1) :
            rowCounter = 0
    counter = counter + 1
    blankCounter = blankCounter + 1
print("Data in data structures")

################################################ previous code
def countPoly(inData, outData) :
    # go through each base from each sequence one codon at a time
    # count the total number of divergent and polymorphic sites
    finalNPoly = 0
    finalSPoly = 0
    finalNDiv = 0
    finalSDiv = 0
    # need other variables for analysis
    tempNPoly = 0  # hold a temporary count of non-syn. and syn. polymorphisms
    tempSPoly = 0  # added to the total if not gaps are encountered in that codon
    tempNDiv = 0
    tempSDiv = 0
    gap = False              # becomes true if any of the current codons contain a gap 
    unknown = False          # becomes true if any of current codons contain an 'n'
    seqSize = len(inData[0]) # length of each sequence
    numCodons = seqSize/3    # number of codons in the sequences
    codonCount = 0           # loop induction variable -- iterate through all codons
    inCodons = []            # list of current codon in all in group sequences
    outCodons = []           # same for out group sequences
    tempCodons = []          # a list of all different codons found for each base
    baseList = []            # a list of all bases found at a particular location
    fixed = True             # true if current difference is fixed in pop.
    firstBaseDiff = False    # true if base of first sequence differs from reference
    inSeqs = numSeqs - 1
    outSeqs = 1
    totalCodons = 0	    # count for testing
    basePos = 0


    # iterate through all codons in all sequences
    while codonCount < numCodons :
        
        # make a list of selected in group codons and out group codons for comparison
        inCodons = []
        outCodons = []
        for i in range(inSeqs) :
            inCodons.append(inData[i][codonCount*3])
            inCodons.append(inData[i][codonCount*3 + 1])
            inCodons.append(inData[i][codonCount*3 + 2])
        for i in range(outSeqs) :
            outCodons.append(outData[codonCount*3])
            outCodons.append(outData[codonCount*3 + 1])
            outCodons.append(outData[codonCount*3 + 2])

        # first check for polymorphism
        # this is the reference codon for comparison
        refCodon = str(outCodons[0] + outCodons[1] + outCodons[2])
        if("-" in refCodon) :
            gap = True
        if("n" in refCodon) :
            unknown = True
       
        # use the current codon of first/reference sequence to compare to all other codons
        # iterate three times to compare all three bases of the codon
        for j in range(3) :
           
            # first check to see if the selected base is the same for all
            # in group sequences.  If not, the differece is not fixed
            compareBase = inCodons[j]
	    for k in range(j, len(inCodons), 3) :
                if (inCodons[k] != compareBase) :
                   fixed = False

            # now count up the number of polymorphisms
            compareBase = outCodons[j]  # current base of codon from reference sequence
            
            for k in range(j, len(inCodons), 3) :   
                                  
                if (inCodons[k] != compareBase) :
                    # find current codon for comparison
                    compareCodon = str(inCodons[k-j] + inCodons[k-j+1] + inCodons[k-j+2])
                    # check for gaps
                    if ("-" in compareCodon) :
                        gap = True
                    if ("n" in compareCodon) :
                        unknown = True              
                    # if no gap and have not already found this codon and diff not fixed
                    if (not(gap) and not(unknown) and (compareCodon not in tempCodons) and not(fixed)) :
			totalCodons += 1   # testing
                        if(codonDict[refCodon] != codonDict[compareCodon]) :
                            tempNPoly = tempNPoly + 1
                            AllSnps.write("NP " + str(basePos) + "\t\t" + refCodon + "\t" + compareCodon + "\t" + codonDict[refCodon] + "\t" + codonDict[compareCodon] + "\n")
                        else :
                            tempSPoly = tempSPoly + 1
                            AllSnps.write("SP "  + str(basePos) + "\t\t" + refCodon + "\t" + compareCodon + "\t" + codonDict[refCodon] + "\t" + codonDict[compareCodon] + "\n")
                    # if it is a fixed difference, count it as that instead
                    elif (not(gap) and not(unknown) and (compareCodon not in tempCodons) and fixed) :
			totalCodons += 1  # testing
                        if(codonDict[refCodon] != codonDict[compareCodon]) :
                            tempNDiv = tempNDiv + 1
                            AllSnps.write("ND " + str(basePos) + "\t\t" + refCodon + "\t" + compareCodon + "\t" + codonDict[refCodon] + "\t" + codonDict[compareCodon] + "\n")
                        else :
                            tempSDiv = tempSDiv + 1
                            AllSnps.write("SD " + str(basePos) + "\t\t" + refCodon + "\t" + compareCodon + "\t" + codonDict[refCodon] + "\t" + codonDict[compareCodon] + "\n")
                    # add codon to temporary list of found codons
                    tempCodons.append(compareCodon)            
          
            # clear temporary lists after every base
            tempCodons = []
            fixed = True
	    basePos += 1   # testing

  
        # update count for syn. and non-syn. polymorphisms unless gap is detected
        if(not(gap)) :
            finalNPoly = finalNPoly + tempNPoly
            finalSPoly = finalSPoly + tempSPoly
            finalNDiv = finalNDiv + tempNDiv
            finalSDiv = finalSDiv + tempSDiv
    
        # reset variables
        tempNPoly = 0
        tempSPoly = 0
        tempNDiv = 0
        tempSDiv = 0
        gap = False
        unknown = False
        fixed = True
        tempCodons = []
        # increment induction variable
        codonCount = codonCount + 1

    # test code
    print("Non-synonymous Poly:" + str(finalNPoly))
    print("Synonymous Poly:" + str(finalSPoly))
    print("Non-synonymous Div:" + str(finalNDiv))
    print("Synonymous Div:" + str(finalSDiv))
    print("Total Codons: " + str(totalCodons))
    result = [finalNPoly, finalSPoly, finalNDiv, finalSDiv]
    return result


# count polymorphisms
results = countPoly(inData, outData)
print(results)
