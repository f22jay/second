#!/usr/bin/python
import sys
i=0
for line in  open(sys.argv[1]):
	j=0
	k=0
	k=line.find("shtml")
	if k==-1:
		continue

	j=line[:k].rfind("http://")
	if j==-1:
		continue	
	k+=5
	print line[j:k]
	i+=1
