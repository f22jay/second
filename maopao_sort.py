#!/usr/bin/python
import random
for i in range(9,0):
	print i
print 3/2
def maopao(a,n):
	for i in range(0,n):
		for j in range(0,n-1-i):
			if a[j]>a[j+1]:
				temp=a[j]
				a[j]=a[j+1]
				a[j+1]=temp
			else:
				continue

n=15
a=[]
for i in range(0,n):
	a.append(random.randint(1,100))
	print a[i],i
maopao(a,n)
print len(a)
print "after sort"
for i in range(0,n):
	print a[i], i

