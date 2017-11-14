from predictivetext import PredictiveText
import re

script = ' '.join(re.findall(r'\S+', open('manifesto.txt').read()))
monte = PredictiveText(script, m='S')
print('\n'.join([monte.generate('S') for i in range(10)]))