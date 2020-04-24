from output_search import _parse

# TODO: tests beginning from _save_output

def parse(*args, **kwargs):
    r = list(_parse(*args, **kwargs))
    r = sorted(r)
    return r

def test_parse_empty():
    assert parse('') == []

def test_parse_one_2_three_4():
    assert parse('one 2 three 4') == ['one', 'three']

def test_parse_specials():
    assert parse('\n\t\r one \n\t\r "two" \n\t\r three \n\t\r') == ['"two"', 'one', 'three', 'two']

def test_parse_substring():
    assert parse('one two three four five six', substring='e') == ['five', 'one', 'three']


def test_parse_env():
    assert parse('SHELL=bash\nPATH=/a/b:/c/d') == ['/a/b', '/a/b:/c/d', '/c/d', 'PATH', 'PATH=/a/b:/c/d', 'SHELL', 'SHELL=bash', 'bash']

def test_parse_env_substrig():
    assert parse('SHELL=bash\nPATH=/a/b:/c/d', substring='/c') == ['/a/b:/c/d', '/c/d', 'PATH=/a/b:/c/d']


def test_parse_json():
    assert parse('{"Hello": "hello world"}') == ['"hello','Hello','Hello":','Hello": "hello world','hello','hello world','world','world"}','{"Hello":']

