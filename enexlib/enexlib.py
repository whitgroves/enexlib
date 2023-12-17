import os
import re
import bs4

def read_enex(filename:str, text_only:bool=False, raw_text:bool=False,
              join_all:bool=False) -> list[tuple[str, str]]:
    """
    Parses the .enex or .xml file at `filename` and returns a list of notes.
    Args:
        `filename`: The file to extract. Must be `.enex` or `.xml`.
        `text_only`: If True, special characters will be removed.
        `raw_text`: If True, returns raw xml content. Overrides `text_only`.
        `join_all`: If True, combines all content into a single note.
    Returns:
        A list of (title, content) pairs.
    Raises:
        ValueError if input file is not an .enex or .xml file.
    """
    if filename[-5:] != '.enex' and filename[-4:] != '.xml':
        raise ValueError('Input file must be .enex or .xml')
    with open(filename, 'r', encoding='utf-8') as file:
        raw = file.read()
    soup = bs4.BeautifulSoup(raw, features='xml')
    titles = soup.find_all('title')
    contents = soup.find_all('content')
    notes = []
    for title, content in zip(titles, contents):
        title_ = re.compile(r'<.*?title>').sub('', str(title))
        content_ = content.get_text()
        note = content_ if raw_text else format_text(content_, text_only)
        notes.append((title_, note))
    return ('All Notes', ''.join(n for _, n in notes)) if join_all else notes

def format_text(text:str, text_only:bool=False) -> str:
    """ 
    Takes an xml-formatted string and returns it in plaintext format. 
    Args:
        `text_only`: If True, special characters will be removed.
    Returns:
        The reformatted text.
    """
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
        text = text.replace('\xa0', ' ')
        # strip out any whitespaces or remaining unicode
        if text_only:
            text = re.compile(r'[\t\n\r\f\v]').sub('', text)
            text = re.compile(r'u.{,4}').sub('', text)
        #remove all remaining special characters and tags
        text = re.compile(r'&#\d*;?').sub(' ', str(text))
        text = re.compile(r'<.*?>').sub(' ', text)
    return ' '.join(text.split()) # removes extra whitespaces

def export_to_markdown(filename:str, join_all:bool=False) -> None:
    """
    Reads the .enex file at `filename` and exports all notes to markdown files.
    Args:
        `filename`: The name of the .enex or .xml file to parse.
        `kwargs`: Keyword arguments for the internal call to read_enex().
    """
    dir_ = os.path.split(os.path.abspath(filename))[0]
    dir_ = os.path.join(dir_, 'exported-notes')
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    for title, content in read_enex(filename, raw_text=True, join_all=join_all):
        with open(f'{dir_}/{title}.md', mode='w', encoding='utf-8') as file:
            match = re.search(r'(?:<en-note>)([\s\S]*?)(?:</en-note>)', content)
            content = match[0] if match else '<[ No Content ]>'
            file.writelines(content)
