import re

for path in ['tests/test_ai.py', 'tests/test_progress.py']:
    with open(path, 'rb') as f:
        data = f.read()

    fixed = data.replace(b'[email protected]', b'tester@example.com')

    with open(path, 'wb') as f:
        f.write(fixed)

    print(path, 'replaced:', data.count(b'[email protected]'))