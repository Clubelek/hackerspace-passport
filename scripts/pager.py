import sys
import os.path

template = sys.argv[1]
left = {
	"path" : os.path.abspath(sys.argv[2]),
	"over" : str(os.path.splitext(os.path.basename(sys.argv[2]))[0].split('_')[-1].endswith('-1')).lower(),
	"number" : os.path.splitext(os.path.basename(sys.argv[2]))[0].split('_')[-1],
}
right = {
	"path" : os.path.abspath(sys.argv[3]),
	"number" : os.path.splitext(os.path.basename(sys.argv[3]))[0].split('_')[-1],
}
bg = {
	"path" : os.path.abspath(sys.argv[4]),
}
cropmarks = {
	"path" : os.path.abspath(sys.argv[5]),
}

output = sys.argv[-1]

temptext = ''

with open(template, 'r') as tmp:
	temptext = tmp.read()
outtext = temptext.format(
	left = left,
	right = right,
	bg = bg,
	cropmarks = cropmarks
)
with open(output, 'w', encoding='utf8') as out:
	out.write(outtext)