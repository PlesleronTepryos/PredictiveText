from collections import Counter
import numpy as np
import re


class PredictiveText:

	def __init__(self, script, m='S'):
		self.script = script
		if 'S' in m:
			b = [' '.join(script.split(' ')[0:2])] + \
			              re.findall(r'(?<=\. )\S+\s\S+', script)
			bc = Counter(b)
			bw = [[J, bc[J] / len(b)] for J in bc.keys()]
			self.S_begins = [[H[0] for H in bw], [G[1] for G in bw]]

			g = script.split(' ')
			f = [[g[i] + ' ' + g[i + 1], g[i + 2]] for i in range(len(g) - 2)]
			q = list(set([G[0] for G in f]))
			pw = dict([[H, []] for H in q])
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

		if 'W' in m:
			b = re.findall(r"(?<=\W)\w\w", script)
			bc = Counter(b)
			bw = [[J, bc[J] / len(b)] for J in bc.keys()]
			self.W_begins = [[H[0] for H in bw], [G[1] for G in bw]]

			e = re.findall(r'\w\w(?=\W)', script)
			ec = Counter(e)
			self.W_ends = dict([[J, ec[J] / len(e)] for J in ec.keys()])

			g = re.findall(r'\w+', script)
			f = [[K[0:2], K[2]] for L in [[y[i:i + 3]
			    for i in range(len(y) - 3)] for y in g if len(y) > 3] for K in L]
			q = list(set([G[0] for G in f]))
			pw = dict([[H, []] for H in q])
			for k in f:
				pw[k[0]].append(k[1])
			fc = {}
			for k in pw.keys():
				fc[k] = Counter(pw[k])
			fw = {}
			for k in fc.keys():
				fw[k] = [[j, fc[k][j] / len(pw[k])] for j in fc[k].keys()]
			self.W_follows = [{}, {}]
			for k in fw.keys():
				self.W_follows[0][k] = [H[0] for H in fw[k]]
				self.W_follows[1][k] = [H[1] for H in fw[k]]

	def generate(self, m='S'):
		if m == 'S':
			s = np.random.choice(a=self.S_begins[0], p=self.S_begins[1]).split(' ')
			while isinstance(s, list):
				last = s[-2] + ' ' + s[-1]
				if last[-1] == '.':
					s = ' '.join(s)
				else:
					s.append(np.random.choice(a=self.S_follows[
					         0][last], p=self.S_follows[1][last]))
			else:
				return s
		if m == 'W':
			# return "Word generation is still kinda broken."
			w = list(np.random.choice(a=self.W_begins[0], p=self.W_begins[1]))
			while isinstance(w, list):
				last = w[-2] + w[-1]
				if last in self.W_follows[0].keys():
					w.append(np.random.choice(a=self.W_follows[
					         0][last], p=self.W_follows[1][last]))
				if last in self.W_ends.keys():
					if np.random.rand() <= self.W_ends[last] * len(w):
						w = ''.join(w)
			else:
				return w
		else:
			return 'Not a valid mode!'

	def __str__(self):
		return """
PredictiveText object
Basis script of length: {0} characters & {1} words
{2} unique word pairs; {3} of which begin sentences
""".format(len(self.script), len(self.script.split(' ')), len(self.S_follows[0].keys()), len(self.S_begins[1]))
