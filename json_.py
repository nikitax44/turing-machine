#!/usr/bin/env python3
from json import *
loads_=loads

def loads(text):
	b=text.split('\n')
	def n(line):
		for i in range(len(line)):
			c=line[i]
			if c!='#':
				continue
			if line[:i].count('"')%2==0:
				line=line[:i]
				break
		return line
	b=[n(i) for i in b if i and not i.startswith('#')]
	c='\n'.join(b)
	return loads_(c)
