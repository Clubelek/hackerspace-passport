
import PIL
import io
import base64
import secrets
import string

BASIC_CHARS = string.digits + string.ascii_lowercase

PASSPORT_DATE_FORMAT = '%d %m %Y'

MRZ_DATE_FORMAT = '%y%m%d'

MRZ_DOUBLE_TABLE = set()

MRZ_REPLACE_TABLE = {
	'\u003C' : '<', # <
	'\u002D' : '<', # -
	'\u002C' : '<', # ,
	'\u002F' : '<', # /
	'\u00C1' : 'A', # Á
	'\u00C0' : 'A', # À
	'\u00C2' : 'A', # Â
	'\u00C4' : 'A', # Ä
	'\u00C3' : 'A', # Ã
	'\u0102' : 'A', # Ă
	'\u00C5' : 'A', # Å
	'\u0100' : 'A', # Ā
	'\u0104' : 'A', # Ą
	'\u0106' : 'C', # Ć
	'\u0108' : 'C', # Ĉ
	'\u010C' : 'C', # Č
	'\u010A' : 'C', # Ċ
	'\u00C7' : 'C', # Ç
	'\u0110' : 'D', # Ð
	'\u010E' : 'D', # Ď
	'\u00C9' : 'E', # É
	'\u00C8' : 'E', # È
	'\u00CA' : 'E', # Ê
	'\u00CB' : 'E', # Ë
	'\u011A' : 'E', # Ě
	'\u0116' : 'E', # Ė
	'\u0112' : 'E', # Ē
	'\u0118' : 'E', # Ę
	'\u0114' : 'E', # Ĕ
	'\u011C' : 'G', # Ĝ
	'\u011E' : 'G', # Ğ
	'\u0120' : 'G', # Ġ
	'\u0122' : 'G', # Ģ
	'\u0126' : 'H', # Ħ
	'\u0124' : 'H', # Ĥ
	'\u00CD' : 'I', # Í
	'\u00CC' : 'I', # Ì
	'\u00CE' : 'I', # Î
	'\u00CF' : 'I', # Ï
	'\u0128' : 'I', # Ĩ
	'\u0130' : 'I', # İ
	'\u012A' : 'I', # Ī
	'\u012E' : 'I', # Į
	'\u012C' : 'I', # Ĭ
	'\u0134' : 'J', # Ĵ
	'\u0136' : 'K', # Ķ
	'\u0141' : 'L', # Ł
	'\u0139' : 'L', # Ĺ
	'\u013D' : 'L', # Ľ
	'\u013B' : 'L', # Ļ
	'\u013F' : 'L', # Ŀ
	'\u0143' : 'N', # Ń
	'\u00D1' : 'N', # Ñ
	'\u0147' : 'N', # Ň
	'\u0145' : 'N', # Ņ
	'\u014B' : 'N', # η
	'\u00D8' : 'OE',# Ø
	'\u00D3' : 'O', # Ó
	'\u00D2' : 'O', # Ò
	'\u00D4' : 'O', # Ô
	'\u00D6' : 'O', # Ö
	'\u00D5' : 'O', # Õ
	'\u0150' : 'O', # Ő
	'\u014C' : 'O', # Ō
	'\u014E' : 'O', # Ŏ
	'\u0154' : 'R', # Ŕ
	'\u0158' : 'R', # Ř
	'\u0156' : 'R', # Ŗ
	'\u015A' : 'S', # Ś
	'\u015C' : 'S', # Ŝ
	'\u0160' : 'S', # Š
	'\u015E' : 'S', # Ş
	'\u0166' : 'T', # Ŧ
	'\u0164' : 'T', # Ť
	'\u0162' : 'T', # Ţ
	'\u00DA' : 'U', # Ú
	'\u00D9' : 'U', # Ù
	'\u00DB' : 'U', # Û
	'\u00DC' : 'U', # Ü
	'\u0168' : 'U', # Ũ
	'\u016C' : 'U', # Ŭ
	'\u0170' : 'U', # Ű
	'\u016E' : 'U', # Ů
	'\u016A' : 'U', # Ū
	'\u0172' : 'U', # Ų
	'\u0174' : 'W', # Ŵ
	'\u00DD' : 'Y', # Ý
	'\u0176' : 'Y', # Ŷ
	'\u0178' : 'Y', # Ÿ
	'\u0179' : 'Z', # Ź
	'\u017D' : 'Z', # Ž
	'\u017B' : 'Z', # Ż
	'\u00FE' : 'TH',# Þ
	'\u00C6' : 'AE',# Æ
	'\u0132' : 'IJ',# Ĳ
	'\u0152' : 'OE',# Œ
	'\u00DF' : 'SS',# ß
}

def mrzcheckdigit(s):
	if s == len(s) * '<':
		return '<'
	cval = {'<' : 0}
	cval.update({chr(48 + i) : i for i in range(10)})
	cval.update({chr(55 + i) : i for i in range(10, 36)})
	weights = [7, 3, 1]
	check = 0
	for i, c in enumerate(s):
		check += cval[c] * weights[i % len(weights)]
	return str(check % 10)

def mrzescape(s):
	r = io.TextIO()
	s = s.upper()
	for i, c in enumerate(s):
		if c in MRZ_DOUBLE_TABLE and i != 0:
			r.write(MRZ_REPLACE_TABLE.get(s[i-1], '')
		else:
			r.write(MRZ_REPLACE_TABLE.get(c, ''))
	return r.getValue()

def getimgdata(imgpath, maxheight = 450, maxwidth = 350):
	img = PIL.Image.open(imgpath)
	hratio = maxheight / img.height
	wratio = maxwidth / img.width
	ratio = min(hratio, wratio)
	size = (img.width * ratio, img.height * ratio)
	filter = PIL.Image.LANCZOS #if ratio < 1 else PIL.Image.BICUBIC
	data = io.BytesIO()
	img.resize(size, filter).save(data, 'png', optimize = True)
	uri = 'data:image/png;base64,'
	return {
		'uri' : uri + base64.b64encode(data.getValue()).decode('ascii'),
		'width' : size[0],
		'height' : size[1],
	}

def buildMRZ(passport, person, namescheme = 'famfirst'):
	name = mrzescape({
		'famfirst' : person['name'] + '<<' + person['firstnames'],
		'firstfam' : person['firstnames'] + '<<' + person['name'],
		'first' : person['firstnames'],
		'fam' : person['name'],
		'full' : person['fullname'],
		'fullcomma' : person['fullname'].replace(', ', '<<', 1),
		'mrz' : person['mrzname'].replace('#', '<<', 1),
	}.get(namescheme, person['name'] + '<<' + person['firstnames']))
	number = passport['number'] and passport['number'].rjust(9, '<')[:9] or '<<<<<<<<<'
	bdate = person['birthday-date'] and person['birthday-date'].strftime(MRZ_DATE_FORMAT) or '<<<<<<'
	edate = passport['expiry-date'] and passport['expiry-date'].strftime(MRZ_DATE_FORMAT) or '<<<<<<'
	top = (passport['type'].rjust(2, '<')[:2] + passport['country'].rjust(3, '<')[:3] + name).rjust(44, '<')[:44]
	bottom = ''.join((
		number,
		mrzcheckdigit(number),
		bdate,
		mrzcheckdigit(bdate),
		person['gender'] or '<',
		edate,
		mrzcheckdigit(edate),
	)).rjust(43, '<')[:43]
	bottom += mrzcheckdigit(bottom)
	return {'TOP':top, 'BOTTOM':bottom}
	
def buildpassport(number = None, issuedate = None, expiredate = None):
	if not number:
		number = ''.join(secrets.choice(BASIC_CHARS) for _ in range(9))
	return {
		'issuance-date' : issuedate,
		'expiry-date' : expiredate,
		'issuance' : issuedate and issuedate.strftime(PASSPORT_DATE_FORMAT) or 'XX XX XXXX',
		'expiry' : expiredate and expiredate.strftime(PASSPORT_DATE_FORMAT) or 'XX XX XXXX',
		'number' : number
	}


	

