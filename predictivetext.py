from collections import Counter
import numpy as np
import re

def cleanlines(filename):
	u = open(filename).read().splitlines()
	li = [re.findall(r"\S+", K)[2:] for K in u]
	for L in li:
		if re.fullmatch(r'\d+:\d+', L[0]):
			L.pop(0)
	return ' '.join([K for L in li for K in L])


class PredictiveText:
	def __init__(self, script):
		self.script = script
		
		b = [script.split(' ')[0]] + re.findall(r'(?<=\. )\w+', script)
		bc = Counter(b)
		bw = [[J, bc[J] / len(b)] for J in bc.keys()]
		self.S_begins = [[H[0] for H in bw], [G[1] for G in bw]]

		e = re.findall(r'\w+(?=\. )', script)
		ec = Counter(e)
		self.S_ends = dict([[J, ec[J] / len(e)] for J in ec.keys()])

		f = [F.split(' ') for F in re.findall(r'\w+ \w+', script)]
		pw = dict([[H[0], []] for H in f])
		for k in f:
			pw[k[0]].append(k[1])
		fc = {}
		for k in pw.keys():
			fc[k] = Counter(pw[k])
		fw = {}
		for k in fc.keys():
			fw[k] = [[j, fc[k][j] / len(pw[k])] for j in fc[k].keys()]
		self.S_follows = [{}, {}]
		for k in fw.keys():
			self.S_follows[0][k] = [H[0] for H in fw[k]]
			self.S_follows[1][k] = [H[1] for H in fw[k]]
	
	def generate(self, m='s'):
		if m == 's':
			s = [np.random.choice(a=self.S_begins[0], p=self.S_begins[1])]
			while isinstance(s, list):
				if s[-1] in self.S_follows[0].keys():
					s.append(np.random.choice(a=self.S_follows[0][s[-1]], p=self.S_follows[1][s[-1]]))
				else:
					s = ' '.join(s) + '.'
				if isinstance(s, list):
					if s[-1] in self.S_ends.keys():
						if np.random.rand() <= self.S_ends[s[-1]] * (len(s) ** 0.5):
							s = ' '.join(s) + '.'
			else:
				return s
		if m == 'w':
			return 'Sorry! Word generation is not implemented yet!'
		else:
			pass

boble = PredictiveText(cleanlines('bible.txt'))
#print(boble.generate('s'))


