from predictivetext import PredictiveText
import re

script = ' '.join(re.findall(r'\S+', open('meinkampf.txt').read()))
meink = PredictiveText(script, m='S')
print('\n'.join([meink.generate('S') for i in range(10)]))
print(meink)