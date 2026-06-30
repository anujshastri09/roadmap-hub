import re

with open("tests/test_auth.py", "rb") as f:
    data = f.read()

for m in re.finditer(rb'"email": "[^"]*"', data):
    print(m.group())