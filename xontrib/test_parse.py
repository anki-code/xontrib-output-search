from output_search import _parse, _dict_keys_values

# TODO: tests beginning from _save_output

def parse(*args, **kwargs):
    r = list(_parse(*args, **kwargs))
    r = sorted(r)
    return r

def test_parse_empty():
    assert parse('') == []

def test_parse_empty_prefix():
    assert parse('one two three', substring='none') == []

def test_parse_one_2_three_4():
    assert parse('one 2 three 4') == ['one', 'three']

def test_parse_specials():
    assert parse('\n\t\r one \n\t\r "two" \n\t\r three \n\t\r') == ['one', 'three', 'two']

def test_parse_substring():
    assert parse('one two three four five six', substring='e') == ['five', 'one', 'three']


def test_parse_env():
    assert parse('SHELL=bash\nPATH=/a/b:/c/d') == ['/a/b', '/a/b:/c/d', '/c/d', 'PATH', 'SHELL', 'bash']

def test_parse_env_substrig():
    assert parse('SHELL=bash\nPATH=/a/b:/c/d', substring='/c') == ['/a/b:/c/d', '/c/d']


def test_parse_json():
    assert parse('{"Hello": "hello world"}') == ['Hello', 'hello', 'hello world', 'world']


def test_dict_keys_values():
    assert _dict_keys_values([{'abc':{'b':{'c':123}}, 'd':[[1,2,3], None, True, {'e':1}]},4]) == {'keys': ['abc', 'b', 'c', 'd', 'e'], 'values': [123, 1, 2, 3, True, 1, 4]}
