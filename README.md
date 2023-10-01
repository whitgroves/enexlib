# enexlib

A python3 module for converting Evernote backup files (.enex) to plaintext.

## Usage
```
pip install enexlib
```
```
from enexlib import read_enex

read_enex('<filename>.enex') # returns (<note title>, <note content>)
```
`read_enex` has 3 optional flags (all `false` by default) that modify its behavior:

 - `text_only` — Attempts to remove all special characters.

 - `raw_text` — Returns the raw content of the .enex file instead of parsing it.
	Overrides `text_only`.

 - `join_all` — Combines all content into a single large note. 