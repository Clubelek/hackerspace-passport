
import os.path
import sys
import json

identity = sys.argv[1]
template = sys.argv[2]
outfile = sys.argv[3]

data = {'fname' : os.path.splitext(os.path.basename(identity))[0]}
text = ''
with open(identity, 'r', encoding='utf8') as f:
	data.update(json.load(f))
with open(template, 'r', encoding='utf8') as f:
	text = f.read()
with open(outfile, 'w', encoding='utf8') as f:
	f.write(text.format(**data))