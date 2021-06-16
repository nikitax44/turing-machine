class turingmachine:
	def __init__(self, data, rules, lines):
		self.data=[line(i) for i in data]
		self.lines=lines
		while len(self.data)<self.lines:
			self.data.append(line())
		self.rules=rules
		self.rule='start'
		self.state=0

	def step(self):
		if self.state: # return if program is done
			return (self.rule, [self.data[i].get() for i in range(self.lines)], [0]*self.lines)

		try:
			rule_set=self.rules.get(self.rule) # try to get all of rules where rule is self.rule
		except:
			raise

		state=[self.data[i].get() for i in range(self.lines)] # get current state

		if rule_set==None: # unknown error
			print(self.rules, self.rule)
			rule_set=[]

		for rulea in rule_set:
			rule=rulea.get('state', ['*']*self.lines)
			for i in range(self.lines):
				a, b=rule[i], state[i]
				if a!=b: # check if this rule fits
					if a=='*':
						pass
					else:
						break
			else: # rule is ok
				todo=rulea
				break
		else: # rule not found
			self.state=2
			raise RuntimeError('invalid state', rule_set, state)

		mod=todo.get('mod', [None]*self.lines)
		motion=todo.get('move', [0]*self.lines)
		for i in range(self.lines): # edit all of the lines
			self.data[i].set(mod[i], motion[i])
		self.rule=todo.get('rule', self.rule)

		if self.rule=='done':
			self.state=1
		return (self.rule, mod, motion)

class line:
	def __init__(self, data=[], head=0):
		self.head=head
		if type(data)==dict:
			self.data=data
		else:
			self.data={} # change [1,2,3,4] to {0:1, 1:2, 2:3, 3:4}
			for i in range(len(data)):
				self.data[i]=data[i]

	def get(self, motion=0):
		buf=self.data.get(self.head, ' ')
		self.move(motion)
		return buf

	def set(self, value, motion=0):
		buf=self.get()
		if value==None:
			pass
		elif value!=' ':
			self.data[self.head]=value
		else:
			try:
				del self.data[self.head]
			except KeyError:
				pass
		self.move(motion)
		return buf

	def move(self, motion=0):
		self.head+=motion

	def __repr__(self):
		return f'[head: {self.head}; data: {self.data}]'

'''
rules={
	'start':{
		mod:[1, None], #set first line to 1 and not edit second
		move:[1, -2], # move heads
		rule:'copy',
	}
	'copy': ...
	...
	# to end set rule to 'done'
}
'''

def load_rule(file='rules.json'):
	try:
		with open(file) as f:
			text=f.read()
	except:
		raise

	try:
		return __import__('json').loads(text)
	except:
		try:
			import textruletojson as tr
			rules, lines=tr.t2j(text)
			return {'rules':rules, 'lines':lines}
		except:
			print('failed to load rules')
			raise

if __name__=='__main__':
	from sys import argv
	argv.pop(0)
	buf=load_rule(argv.pop(0) if len(argv) else input('file: '))
	lines=buf.get('lines')
	rules=buf.get('rules')
	init=argv.pop(0) if len(argv) else input('initial state: ')

	machine=turingmachine([list(init)], rules, lines)

	try:
		steps=0
		while not machine.state:
			machine.step()
			steps+=1
	except KeyboardInterrupt:
		print(machine.data, machine.state, machine.rule)
	except:
		raise
	else:
		for line in machine.data:
			buf=list(line.data.keys())
			if not len(buf):
				print('empty')
				continue
			print(str().join([line.data.get(i, ' ') for i in range(min(buf), max(buf)+1)]))
		print('head:', steps)
#		print([list(i.data.values()) for i in machine.data])
#		print(machine.data)
#	print(machine.data)
