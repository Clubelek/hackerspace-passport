import sys
import os
import re
import math
import json
import os.path
import itertools

DEFAULT_FILES = {
	"cover" : "$(SVGDIR)/pages/c_n.svg",
	"pages" : "$(SVGDIR)/pages/p_n.svg",
}

BUILD_RULE = "\t$(PPU) $^ $@\n"

DEFAULT_DEPFILE = "$(PDFDIR)/{0}.pdf : $(PDFDIR)/{0}_n_n.pdf\n" + BUILD_RULE + ".INTERMEDIATE : $(PDFDIR)/{0}.pdf $(PDFDIR)/{0}_n_n.pdf\n"

def listpages(path, type):
	lst = (f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and re.match(r'^[cp]_[0-9]+(,[0-9]+)*\.svg$', f))
	result = []
	for f in lst:
		for n in os.path.splitext(os.path.basename(f))[0].split('_')[-1].split(','):
			r = {
				"path" : os.path.join(path, f),
				"number" : int(os.path.splitext(os.path.basename(f))[0].split('_')[-1].split('-')[-1]),
				"suffix" : os.path.splitext(os.path.basename(f))[0].split('_', maxsplit=1)[1],
				"type" : {
					"c" : "cover",
					"p" : "pages"
				}[os.path.basename(f).split('_')[0]]
			}
			result.append(r)
	return result if type is 'both' else [f for f in result if f['type'] == type]

def hastemplates(path, mode):
	return any(re.match(r'^%s_[A-Za-z0-9\{\}\[\]]+\-[0-9]+(,[0-9]+)*\.svg$' % mode[0], f) for f in os.listdir(path))

def listemplates(path, id, pagepath, type):
	tmps = (f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and re.match(r'^[cp]_[A-Za-z0-9\{\}\[\]]+\-[0-9]+(,[0-9]+)*\.svg$', f))
	lst = [f.format(**id) for f in tmps]
	result = []
	for f in lst:
		for n in os.path.splitext(os.path.basename(f))[0].split('_')[-1].split(','):
			r = {
				"path" : os.path.join(pagepath, os.path.basename(f)),
				"number" : int(os.path.splitext(os.path.basename(f))[0].split('_')[-1].split('-')[-1]),
				"suffix" : os.path.splitext(os.path.basename(f))[0].split('_', maxsplit=1)[1],
				"type" : {
					"c" : "cover",
					"p" : "pages"
				}[os.path.basename(f).split('_')[0]]
			}
			result.append(r)
	return result if type is 'both' else [f for f in result if f['type'] == type]

def makedeps(pagelist):
	lst = sorted(pagelist, key= lambda d:d['number'])
	pagecount = len(lst)
	result = []
	for i in range(math.ceil(pagecount/2)):
		left = None if i >= pagecount else i
		right = None if pagecount - (i+1-(pagecount%2)) >= pagecount else pagecount - (i+1-(pagecount%2))
		if left is not None and right is not None and lst[left]['type'] != lst[right]['type']:
			raise ValueError("Pages %s and %s should be matched but have different type" % (lst[left]['path'], lst[right]['path']))
		if i % 2 == 0:
			left, right = right, left
		result.append('$(PDFDIR)/' + lst[left]['type'] + '_' + ('n' if left is None else lst[left]['suffix']) + '_' + ('n' if right is None else lst[right]['suffix']) + '.pdf')
	return result

if __name__ == "__main__":
	pagedir = sys.argv[1]
	tmpdir = sys.argv[2]
	iddir = sys.argv[3]
	mode = sys.argv[-1].split('.')[0]
	lst = listpages(pagedir, mode)
	if not hastemplates(tmpdir, mode):
		types = {d['type'] for d in lst}
		if mode not in types:
			with open('%s.mk' % mode, 'w', encoding='utf8') as f:
				f.write(DEFAULT_DEPFILE.format(mode))
		for t in types:
			with open('%s.mk' % t, 'w', encoding='utf8') as f:
				d = makedeps(d for d in lst if d['type'] == t)
				f.write('$(PDFDIR)/%s.pdf' % t)
				f.write(' : ')
				f.write(' '.join(d))
				f.write('\n')
				f.write(BUILD_RULE)
				f.write('.INTERMEDIATE : $(PDFDIR)/%s.pdf ' % t)
				f.write(' '.join(d))
				f.write('\n')
	else:
		ids = (f for f in os.listdir(iddir) if os.path.isfile(os.path.join(iddir, f)) and re.match(r'^[A-Za-z0-9]+\.json$', f))
		identities = []
		types = set()
		for i in ids:
			id = {'fname' : os.path.splitext(os.path.basename(i))[0]}
			with open(os.path.join(iddir, i), 'r', encoding='utf8') as f:
				id.update(json.load(f))
			l = lst + listemplates(tmpdir, id, pagedir, mode)
			identities.append((id['fname'], l))
			types.update({d['type'] for d in l})
		if mode not in types:
			with open('%s.mk' % mode, 'w', encoding='utf8') as f:
				f.write(DEFAULT_DEPFILE.format(mode))
		files = set()
		for t in types:
			with open('%s.mk' % t, 'w', encoding='utf8') as f:
				for i, l in identities:
					d = makedeps(d for d in l if d['type'] == t)
					f.write('$(PDFDIR)/%s_%s.pdf' % (t, i))
					f.write(' : ')
					f.write(' '.join(d))
					f.write('\n')
					f.write(BUILD_RULE)
					files.update(d)
				f.write('.INTERMEDIATE : %s ' % ' '.join(('$(PDFDIR)/%s_%s.pdf' % (t, i)) for i, _ in identities))
				f.write(' '.join(files))
				f.write('\n')
		
	