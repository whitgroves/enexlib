import pytest
import enexlib as nx

def test_read_enex() -> None:
    for filetype in ['enex', 'xml']:
        notes = nx.read_enex(f'Test.{filetype}')
        assert isinstance(notes, list)
        title, content = notes[0]
        assert 'Enexlib' in title
        assert not any(x in title for x in ['<title>', '</title>'])
        assert all(x in content for x in ['Priority 1',
                                          'requirements issue',
                                          'Follow up',
                                          'https://dev.evernote.com/doc/'])
        assert not any(x in content for x in ['<content>', '</content>'])

def test_format_text() -> None:
    test_input = '  &quot;Ben&nbsp;&&#160;Jerry&apos;s&quot;  '
    test_output = nx.format_text(test_input)
    assert test_output == '"Ben & Jerry\'s"'
