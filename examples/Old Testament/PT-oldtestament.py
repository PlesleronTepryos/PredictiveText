from predictivetext import PredictiveText
import re

def cleanlines(filename):
	u = open(filename).read().splitlines()
	li = [re.findall(r"\S+", K)[2:] for K in u]
	for L in li:
		if re.fullmatch(r'\d+:\d+', L[0]):
			L.pop(0)
		if re.fullmatch(r'\d+:\d+', L[1]):
			L.pop(0)
			L.pop(0)
	return ' '.join([K for L in li for K in L])

#boble = PredictiveText(cleanlines('oldtestament.txt'), m='W')
print(len(cleanlines('oldtestament.txt')))
#print(boble.generate(1000))
