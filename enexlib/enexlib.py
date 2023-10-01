from bs4 import BeautifulSoup
from re import compile

def read_enex(filename:str, text_only:bool=False, raw_text:bool=False, join_all:bool=False) -> list[tuple[str, str]]:
	'''
	Parses an .enex or .xml file and returns a list of notes in the format (title, content).
	Flags:
		<text_only>	: False by default. If True, special characters will be removed from each note.
		<raw_text>	: False by default. If True, the raw content of each note is returned. Overrides <text_only>.
		<join_all>	: False by default. If True, all content is combined into a single note.
	'''

	if filename[-5:] != '.enex' and filename[-4:] != '.xml':
		raise ValueError('Input file must be .enex or .xml')
	
	with open(filename, 'r', encoding='utf-8') as file:
		raw = file.read()

	soup = BeautifulSoup(raw, features='xml')
	titles = soup.find_all('title')
	contents = soup.find_all('content')

	notes = [] 
	for title, content in zip(titles, contents):
		note = content.get_text() if raw_text else format_text(content.get_text(), text_only)
		notes.append((title, note))

	return ('All Notes', ''.join(n for _, n in notes)) if join_all else notes

def format_text(text:str, text_only:bool=False) -> str:
	''' 
	Takes an xml-formatted string and returns it in plaintext format. 
	Flags:
		<text_only>	: False by default. Attempts to remove all special characters.
	'''
	if len(text) > 0:
		newline_char = ' ' if text_only else '\n'
		listitem_char = ' ' if text_only else ' - '
			
		# convert divs (used for spaces) and list items
		text = text.replace('</div><div>', newline_char)
		text = text.replace('</li>', newline_char)
		text = compile(r'<li.*?>').sub(listitem_char, text)
		
		# convert any special characters
		text = text.replace('&quot;', '"')
		text = text.replace('&amp;', '&')
		text = text.replace('¶', newline_char)
		text = text.replace('&nbsp;', ' ')
		text = text.replace('&#160;', ' ')
		text = text.replace('&#8212;', '—')
		text = text.replace('&apos;', "'")
		text = text.replace('&lt;', '<')
		text = text.replace('&gt;', '>')
		text = text.replace('&le;', '≤')
		text = text.replace('&ge;', '≥')
		text = text.replace(u'\xa0', ' ')
		
		# strip out any whitespaces or remaining unicode
		if text_only:
			text = compile(r'[\t\n\r\f\v]').sub('', text)
			text = compile(r'u.{,4}').sub('', text)
		
		#remove all remaining special characters and tags
		text = compile(r'&#\d*;?').sub(' ', str(text))
		text = compile(r'<.*?>').sub(' ', text)
	
	return ' '.join(text.split()) # removes extra whitespaces
