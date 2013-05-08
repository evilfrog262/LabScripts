#!/usr/bin/env python

import sys

################
# Takes as input two text files: a list of start positions and a list of stop positions.
# Outputs two similar text files with the overlapping regions removed.
#####

if (len(sys.argv) != 5) :
    print("Usage: RemoveOverlap.py  <start positions>  <stop positions> <starts output> <stops output>")
    sys.exit(0)

inFile1 = sys.argv[1]
inFile2 = sys.argv[2]
outFile1 = sys.argv[3]
outFile2 = sys.argv[4]

start = open(inFile1, 'r')
end = open(inFile2, 'r')
outStarts = open(outFile1, 'w')
outStops = open(outFile2, 'w')

# put start and stop positions into two lists
starts = [int(pos.strip()) for pos in start]
stops = [int(pos.strip()) for pos in end]

# check that lists have the same length
if (len(starts) != len(stops)) :
    print("ERROR: Unequal number of start and stop positions.  Starts: " + str(len(starts)) + " Stops: " + str(len(stops)))
    sys.exit(0)

i = 0
# check for overlap at all positions
while (i < len(stops) - 1) :

    startPos = starts[i]
    stopPos = stops[i] 
    ###### TEST CODE #########
    #print("Starts : " + str(starts))
    #print("Stops : " + str(stops))
    print("starts[i] : " + str(starts[i]) + "  starts[i+1] : " + str(starts[i+1]) + "  stops[i] : " + str(stops[i]) + "  i : " + str(i))
    ###############
    # if there is overlap, remove the second region
    if (starts[i+1] < stopPos) :
	
	# if second region is inside first region, just keep first region
	if (stops[i] > stops[i + 1]) :
	    starts.pop(i + 1)
	    stops.pop(i + 1)
	# else take start position of first region and end of second region
	else :
	    starts.pop(i + 1)	
	    stops[i] = stops.pop(i + 1)  
        i = i - 1 
    i = i + 1      

print("Starts : " + str(starts))
print("Stops : " + str(stops))
# write to output file
for pos in starts :
    outStarts.write(str(pos) + "\n")

for pos in stops :
    outStops.write(str(pos) + "\n")

start.close()
end.close()
outStarts.close()
outStops.close()
