import json_ as json


def modify_empty(m):
	if m=='_':
		m=' '
	elif m==' ':
		m=None
	return m


def t2j(text):
	rules={}
	ld=True
	lines=None
	for i in text.split('\n'):
		i=i.strip()
#		print(i)
		if i.startswith('//'):
			continue
		elif ': ' in i:
			if i.startswith('init: '):
				rules['start']=[{'rule':i.strip('init: ')}]
			elif i.startswith('accept: '):
				rules[i.strip('accept: ')]=[{'rule':'done'}]
			continue
		elif i=='':
			continue

		buf=i.split(',')
		if ld:
			rulename=buf.pop(0)
			if lines==None:
				lines=len(buf)
			else:
				assert lines==len(buf), 'line count does not match: '+i
			if rulename not in rules:
				rules[rulename]=[]
			state=list(map(modify_empty,buf))
			rules[rulename].append({'state':state})
		else:
			nextrule=buf.pop(0)
			assert lines*2==len(buf), 'line count does not match: '+i
			mod, move=[], []
			for i in range(lines*2):
				m=buf[i]
				if i<lines:
					mod.append(modify_empty(m))
				else:
					if m=='<':
						m=-1
					elif m=='>':
						m=1
					elif m=='-':
						m=0
					else:
						m=int(m)
					move.append(m)
			buf=rules[rulename][-1]
			if nextrule!=rulename :
				buf['rule']=nextrule
			if move!=[0]*lines:
				buf['move']=move
			if mod!=state:
				buf['mod']=mod
		ld=not ld

	assert ld, 'line count does not match'
	return rules, lines

def convert(infile, outfile=None):
	if outfile==None:
		buf=infile.split('.')
		buf.pop()
		outfile='.'.join(buf)+'.json'

	with open(infile) as f:
		rules, lines=t2j(f.read())
	data={
		'rules':rules,
		'lines':lines
	}
	json.dump(data, open(outfile, 'w'), indent='\t')
	return outfile

if __name__=='__main__':
	print('\noutput:', convert(input('file: ')))
