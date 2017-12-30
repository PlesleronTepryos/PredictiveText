from predictivetext import PredictiveText
import re

meink = PredictiveText(' '.join(re.findall(r'\S+', open('meinkampf.txt').read())), m='S')
print(meink.generate(1000))