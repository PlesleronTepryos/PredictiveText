from collections import Counter
import numpy as np
import re


class PredictiveTextError(Exception):
    pass


class PredictiveText:
    def __init__(self, script, m='S', t='Unspecified', silent=True, lb=2):
        self.script = script
        self.lb = lb
        self.title = t
        self.m = m
        o = self.script[-1]
        if not (o == '.' or o == '!' or o == '?'):
            self.script += '.'
        if self.m == 'S':
            b = [' '.join(self.script.split(' ')[0:self.lb])] + re.findall(r'(?<=[\.\?\!] )\S+' + (r'\s\S+' * (self.lb - 1)), self.script)
            bc = Counter(b)
            bw = [[J, bc[J] / len(b)] for J in bc.keys()]
            self.S_begins = [[H[0] for H in bw], [G[1] for G in bw]]

            g = self.script.split(' ')
            f = [[' '.join([g[i + e] for e in range(self.lb)]), g[i + self.lb]] for i in range(len(g) - self.lb)]
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

        elif self.m == 'W':
            b = [''.join(k) for k in re.findall(r'(?<=\W)([^aeiouyAEIOUY\W])+?([aeiouyAEIOUY])([^aeiouyAEIOUY\W])?', self.script)]
            bc = Counter(b)
            bw = [[J, bc[J] / len(b)] for J in bc.keys()]
            self.W_begins = [[H[0] for H in bw], [G[1] for G in bw]]

            W = re.findall(r"\w+", self.script)
            L = [[''.join(k) for k in re.findall(r'([^aeiouyAEIOUY])?([aeiouyAEIOUY])([^aeiouyAEIOUY])?', w)] for w in W]
            f = [[v[0], v[1]] for u in [[y[i:i + 2] for i in range(len(y) - 1)] for y in L] for v in u]
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

        else:
            raise PredictiveTextError("'{}' is not a valid mode.".format(m))
        if not silent:
            print("Finished: {}".format(self.title))

    def generate(self, n=1, s=None, k=4):
        k = 1.56487/(k-1)**1.1695
        if isinstance(s, int):
            np.random.seed(s)
        o = ''
        for i in range(n):
            if self.m == 'S':
                s = np.random.choice(
                    a=self.S_begins[0], p=self.S_begins[1]).split(' ')
                while isinstance(s, list):
                    last = ' '.join([s[e-self.lb] for e in range(self.lb)])
                    if last[-1] == '.' or last[-1] == '?' or last[-1] == '!':
                        s = ' '.join(s)
                    else:
                        s.append(np.random.choice(a=self.S_follows[
                                 0][last], p=self.S_follows[1][last]))
                else:
                    o += ' ' + s

            elif self.m == 'W':
                w = [np.random.choice(a=self.W_begins[0], p=self.W_begins[1])]
                while isinstance(w, list):
                    last = w[-1]
                    if last in self.W_follows[0].keys():
                        w.append(np.random.choice(a=self.W_follows[
                                 0][last], p=self.W_follows[1][last]))
                    if np.random.rand() < (k*len(w))**2/(k*len(w)+1)**2:
                        w = ''.join(w)
                else:
                    o += ' ' + w
            else:
                raise PredictiveTextError("'{}' is not a valid mode.".format(m))
        return o

    def __add__(self, axiom):
        if self.m == axiom.m:
            return PredictiveText((self.script + " " + axiom.script), m=self.m, t=(self.title + ' & ' + axiom.title))
        else:
            raise PredictiveTextError("Incompatible modes.")

