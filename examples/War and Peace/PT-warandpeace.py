from predictivetext import PredictiveText
import re

warnp = PredictiveText(' '.join(re.findall(r'\S+', open('warandpeace.txt').read())), m='S')
print(warnp.generate(1000))