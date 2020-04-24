from output_search import _parse

def parse(*args, **kwargs):
    r = list(_parse(*args, **kwargs))
    r = sorted(r)
    return r

def test_parse_empty():
    assert parse('') == []

def test_parse_one_2_three_4():
    assert parse('one 2 three 4') == ['one', 'three']

def test_parse_specials():
    assert parse('\n\t\r one \n\t\r two \n\t\r three \n\t\r') == ['one', 'three', 'two']

def test_parse_substring():
    assert parse('one two three four five six', substring='e') == ['five', 'one', 'three']


def test_parse_env():
    assert parse('SHELL=bash\nPATH=/a/b:/c/d') == ['/a/b', '/a/b:/c/d', '/c/d', 'PATH', 'PATH=/a/b:/c/d', 'SHELL', 'SHELL=bash', 'bash']

def test_parse_env_substrig():
    assert parse('SHELL=bash\nPATH=/a/b:/c/d', substring='/c') == ['/a/b:/c/d', '/c/d', 'PATH=/a/b:/c/d']


def test_qwe():
    assert parse('Try ssh with "https://github.com/xxh/xxh"') == 1
