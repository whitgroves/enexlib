# enexlib

A python3 module for converting Evernote backup files (.enex) to plaintext.

To use, import enexlib and call read_enex('Filename.enex') to import your notes
into basic text. This has several optional parameters:
 - text_only: False by default. Attempts to remove all special characters.
 - raw_text: False by default. Returns the raw content of the .enex file.
	Overrides text_only.
 - join_all: False by default. Combines all content into a single large note.
	Originally intended for frequency analysis over a large set of notes.

## Changelog
### Version 0.0.4
* Repo cleanup.
* Refactored `read_enex` to support `.xml` files.