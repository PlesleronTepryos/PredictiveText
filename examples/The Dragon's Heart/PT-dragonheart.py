from predictivetext import PredictiveText
import re

script = ' '.join(re.findall(r'\S+', open('dragonheart.txt').read()))
dragon = PredictiveText(script, m='S')
print('\n'.join([dragon.generate('S') for i in range(10)]))