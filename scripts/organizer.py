import sys
import os
import re
import math
import os.path
import itertools

DEFAULT_FILES = {
	"cover" : "$(SVGDIR)/pages/c_n.svg",
	"pages" : "$(SVGDIR)/pages/p_n.svg",
}

BUILD_RULE = "\t$(PPU) $^ $@\n"

DEFAULT_DEPFILE = "$(PDFDIR)/{0}.pdf : $(PDFDIR)/{0}_n_n.pdf\n" + BUILD_RULE

def listfiles(path, type):
	lst = (f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and re.match(r'^[cp]_[0-9]+\.svg$', f))
	result = []
	for f in lst:
		r = {
			"path" : os.path.join(path, f),
			"number" : int(os.path.splitext(os.path.basename(f))[0].split('_')[-1]),
			"type" : {
				"c" : "cover",
				"p" : "pages"
			}[os.path.splitext(os.path.basename(f))[0].split('_')[0]]
		}
		result.append(r)
	return result if type is 'both' else [f for f in result if f['type'] == type]

def makedeps(pagelist):
	lst = sorted(pagelist, key= lambda d:d['number'])
	pagecount = len(lst)
	result = []
	for i in range(math.ceil(pagecount/2)):
		left = None if i > pagecount else i
		right = None if pagecount - (i+1) > pagecount else pagecount - (i+1)
		if left is not None and right is not None and lst[left]['type'] != lst[right]['type']:
			raise ValueError("Pages %s and %s should be matched but have different type" % (lst[left]['path'], lst[right]['path']))
		result.append('$(PDFDIR)/' + lst[left]['type'] + '_' + ('n' if left is None else str(left)) + '_' + ('n' if right is None else str(right)) + '.pdf')
	return result

if __name__ == "__main__":
	pagedir = sys.argv[1]
	mode = sys.argv[2].split('.')[0]
	lst = listfiles(pagedir, mode)
	types = {d['type'] for d in lst}
	if mode not in types:
		with open('%s.mk' % mode, 'w', encoding='utf8') as f:
			f.write(DEFAULT_DEPFILE.format(mode))
	for t in types:
		with open('%s.mk' % t, 'w', encoding='utf8') as f:
			f.write('$(PDFDIR)/%s.pdf' % t)
			f.write(' : ')
			f.write(' '.join(makedeps(d for d in lst if d['type'] == t)))
			f.write('\n')
			f.write(BUILD_RULE)
	