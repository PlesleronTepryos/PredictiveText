from predictivetext import PredictiveText
import re

dragn = PredictiveText(' '.join(re.findall(r'\S+', open('dragonheart.txt').read())), m='S')
print(dragn.generate(1000))