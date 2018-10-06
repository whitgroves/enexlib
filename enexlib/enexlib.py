from bs4 import BeautifulSoup
import re

def read_enex(filename, text_only=False, raw_text=False, join_all=False):
	''' (str) -> list[string, string]
	Reads in an .enex file as xml and parses to a list of title, content tuples.
	'''
	if filename[-5:] != '.enex':
		raise ValueError('Input file must be of type .enex')
		
	with open(filename, 'r', encoding='utf8') as file:
		raw = file.read()
		
	soup = BeautifulSoup(raw, features='xml')
	titles = soup.find_all('title')
	contents = soup.find_all('content')
	
	if len(titles) != len(contents):
		raise ValueError('Failed to parse titles or contents correctly')
	
	# ideally this would be a dict, but we have to account for duplicate titles
	notes = []
	for i in range(len(titles)):
		title = titles[i].get_text()
		if raw_text:
			content = contents[i].get_text()
		else:
			content = format_text(contents[i].get_text(), text_only)
		notes.append((title, content))
	
	if join_all:
		return ('All Notes', ''.join([n[1] for n in notes]))
	
	return notes

 
def format_text(text, text_only=False):
	''' (str) -> str
	Takes an xml-formatted string and returns it in plaintext format.
	'''
	if len(text) > 0:
		newline_char = ' ' if text_only else '\n'
		listitem_char = ' ' if text_only else ' - '
			
		# convert divs (used for spaces) and list items
		text = text.replace('</div><div>', newline_char)
		text = text.replace('</li>', newline_char)
		text = re.compile(r'<li.*?>').sub(listitem_char, text)
		
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
			text = re.compile(r'[\t\n\r\f\v]').sub('', text)
			text = re.compile(r'u.{,4}').sub('', text)
		
		#remove all remaining special characters and tags
		text = re.compile(r'&#\d*;?').sub(' ', str(text))
		text = re.compile(r'<.*?>').sub(' ', text)
	
	return ' '.join(text.split()) # removes extra whitespaces

