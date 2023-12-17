import os
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

def test_export_to_markdown() -> None:
    for filetype in ['enex']: #, 'xml']:
        nx.export_to_markdown(f'Test.{filetype}')
        dir_ = os.path.join(os.getcwd(), 'exported-notes')
        assert os.path.exists(dir_)
        for file in os.listdir(dir_):
            assert 'Enexlib' in file # title should become filename
            with open(f'{dir_}/{file}', mode='r', encoding='utf-8') as file_:
                content = file_.read()
                assert '<[ No Content ]>' not in content # content should save
