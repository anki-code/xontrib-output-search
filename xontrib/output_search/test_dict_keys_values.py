from output_search.tokenize_output import dict_keys_values

def test_dict_keys_values():
    assert dict_keys_values([{'abc':{'b':{'c':123}}, 'd':[[1,2,3], None, True, {'e':1}]},4]) == {'keys': ['abc', 'b', 'c', 'd', 'e'], 'values': [123, 1, 2, 3, True, 1, 4]}