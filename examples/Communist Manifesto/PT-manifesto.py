from predictivetext import PredictiveText
import re

script = ' '.join(re.findall(r'\S+', open('manifesto.txt').read()))
manif = PredictiveText(script, m='S')
print('\n'.join([manif.generate('S') for i in range(10)]))