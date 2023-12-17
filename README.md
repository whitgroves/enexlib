# enexlib
[![Test](https://github.com/whitgroves/enexlib/actions/workflows/run-tests.yml/badge.svg)](https://github.com/whitgroves/enexlib/actions/workflows/run-tests.yml)

A python3 module for converting Evernote backup files (.enex) to plaintext.

## Usage
```
pip install enexlib
```

```
import enexlib as nx

for title, note in nx.read_enex('<filename>.enex'):
	# do something

plain_text = nx.read_enex('<filename>.enex', text_only=True)
raw_content = nx.read_enex('<filename>.enex', raw_text=True)
all_combined = nx.read_enex('<filename>.enex', join_all=True)
```
