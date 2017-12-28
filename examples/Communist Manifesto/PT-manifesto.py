from predictivetext import PredictiveText
import re

manif = PredictiveText(' '.join(re.findall(r'\S+', open('manifesto.txt').read())), m='S')
print(manif.generate(1000))