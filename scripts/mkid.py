
import os.path
import sys
import json

identity = sys.argv[1]
template = sys.argv[2]
outfile = sys.argv[3]

def xmlescape(s):
	if isinstance(s, str):
		return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
	elif isinstance(s, list):
		return [xmlescape(l) for l in s]
	elif isinstance(s, tuple):
		return tuple(xmlescape(l) for l in s)
	elif isinstance(s, set):
		return {xmlescape(l) for l in s}
	elif isinstance(s, dict):
		return {k: xmlescape(v) for k, v in s.items()}
	return s

data = {'fname' : os.path.splitext(os.path.basename(identity))[0]}
text = ''
with open(identity, 'r', encoding='utf8') as f:
	data.update(json.load(f))
with open(template, 'r', encoding='utf8') as f:
	text = f.read()
xmldata = {k: xmlescape(v) for k, v in data.items()}
with open(outfile, 'w', encoding='utf8') as f:
	f.write(text.format(**xmldata))