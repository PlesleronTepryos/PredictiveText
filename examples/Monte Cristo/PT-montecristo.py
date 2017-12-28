from predictivetext import PredictiveText
import re

monte = PredictiveText(' '.join(re.findall(r'\S+', open('montecristo.txt').read())), m='S')
print(monte.generate(1000))