from output_search import _tokenizer

def test_tokenizer_empty():
    assert _tokenizer('') == set()

def test_tokenizer_one_2_three_4():
    assert _tokenizer('one 2 three 4') == {'one', 'three'}

def test_tokenizer_json():
    assert _tokenizer('{"ssh": "https://github.com/xxh/xxh"}') == {'https://github.com/xxh/xxh', '"https://github.com/xxh/xxh"}', 'ssh', '{"ssh":'}

def test_tokenizer_specials():
    assert _tokenizer('\n\t\r one \n\t\r two \n\t\r three \n\t\r') == {'one', 'two', 'three'}

def test_tokenizer_substring():
    assert _tokenizer('one two three four five six', substring='e') == {'one', 'three', 'five'}
