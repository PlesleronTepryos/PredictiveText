from predictivetext import PredictiveText
import re

jinko = PredictiveText(' '.join(re.findall(r'\S+', open('jinkobeach.txt').read())), m='W')
print(jinko.generate(1000))