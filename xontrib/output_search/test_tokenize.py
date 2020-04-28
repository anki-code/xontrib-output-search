from output_search.tokenize_output import tokenize_output_sorted

def test_tokenize_empty():
    assert tokenize_output_sorted('') == []

def test_tokenize_one():
    assert tokenize_output_sorted('one') == ['one']

def test_tokenize_empty_prefix():
    assert tokenize_output_sorted('one two three', substring='none') == []

def test_tokenize_one_2_three_4():
    assert tokenize_output_sorted('one 2 three 4') == ['one', 'three']

def test_tokenize_repeated():
    assert tokenize_output_sorted("""
        +-------+-------+
        | one   | two   |
        | ----- | ----- |
        | three | 12345 |
        +-------+-------+
    """) == ['12345', 'one', 'three', 'two']

def test_tokenize_specials():
    assert tokenize_output_sorted('\n\t\r one \n\t\r "two" \n\t\r three \n\t\r') == ['one', 'three', 'two']

def test_tokenize_substring():
    assert tokenize_output_sorted('one two three four five six', substring='e') == ['five', 'one', 'three']


def test_tokenize_env():
    assert tokenize_output_sorted('SHELL=bash\nPATH=/a/b:/c/d') == ['/a/b', '/a/b:/c/d', '/c/d', 'PATH', 'SHELL', 'bash']

def test_tokenize_env_substrig():
    assert tokenize_output_sorted('SHELL=bash\nPATH=/a/b:/c/d', substring='/c') == ['/a/b:/c/d', '/c/d']


def test_tokenize_json():
    assert tokenize_output_sorted('{"Hello": "hello world", "test": None}') == ['Hello', 'hello', 'hello world', 'test', 'world']

def test_tokenize_json_partial():
    assert tokenize_output_sorted('"test": "1",') == ['test']


def test_tokenize_javascript():
    assert tokenize_output_sorted("{Hello: 'hello world', test:null}") == ['Hello', 'hello', 'hello world', 'test', 'world']


def test_tokenize_complex():
    assert tokenize_output_sorted('one "two" Three=four {"qwe":"hello world"}') == ['Three', 'four', 'hello', 'one', 'qwe', 'two', 'world']
