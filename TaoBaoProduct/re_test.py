import re

text = '共 100 页，'
print(text)
patter = re.compile('\d+')
print(re.search(patter, text).group())
for i in range(2, 500):
    print(i)

