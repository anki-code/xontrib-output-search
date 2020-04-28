#!/usr/bin/env python3

import re
import json
import demjson
import ast
import logging
from collections.abc import Iterable

def filter_tokens(tokens, substring='', len_min=2):
    substring_lower = substring.lower()
    result = []
    for t in tokens:
        len_t = len(t)
        if len_t <= len_min:  # Skip short tokens
            continue
        if len(set(t)) <= 2:  # Skip tokens with repeated characters ('+-+-+')
            continue
        if substring_lower not in t.lower():  # Skip by substring
            continue
        result.append(t)
    return set(result)

framed_regexp = re.compile(r'^["\'({\[,:;]*(.+?)[,})\]"\':;]*$')
def tokenizer_strip(text, text_cmd='', substring='', current_cmd={}):
    tokens = {'final': set(), 'new': set()}
    g = framed_regexp.match(text)
    if g:
        token = g.group(1)
        if token == text:
            return tokens
        else:
            tokens = {'final': set(), 'new': set([token])}
            return tokens
    return tokens

clean_regexp = re.compile(r'[\n\r\t]')
def tokenizer_split(text, text_cmd='', substring='', current_cmd={}):
    text = clean_regexp.sub(' ', text).strip()

    split_combinations = [' ', '":"']
    for sc in split_combinations:
        tokens = text.split(sc)
        if len(tokens) > 1:
            break

    if tokens != [text]:
        tokens = {'final': set(), 'new': set(tokens)}
    else:
        tokens = {'final': set(), 'new': set()}
    return tokens


env_regexp = re.compile(r'^([a-zA-Z0-9_]+?)=(.*)$')
def tokenizer_env(text, text_cmd='', substring='', current_cmd={}):
    tokens = {'final': set(), 'new': set()}
    if len(text) < 4:
        return tokens
    g = env_regexp.match(text)
    if g:
        var = g.group(1)
        value = g.group(2)
        values = value.split(':')
        tokens = {
            'final': set([var, value] + values),
            'new': set([value])
        }
    return tokens


def dict_keys_values(d, target='values'):
    result = {'keys': [], 'values': []}
    if d is None:
        return result
    elif type(d) is dict:
        for k in d:
            result['keys'] += [k]
            val_result = dict_keys_values(d[k], 'values')
            result['keys'] += val_result['keys']
            result['values'] += val_result['values']
        return result
    elif type(d) in [list, set]:
        for v in d:
            val_result = dict_keys_values(v, 'values')
            result['keys'] += val_result['keys']
            result['values'] += val_result['values']
        return result
    else:
        result[target] += [d]
        return result

def list_str(lst):
    if isinstance(lst, Iterable):
        return [str(l) for l in lst]
    else:
        return str(lst)

def tokenizer_dict(text, text_cmd='', substring='', current_cmd={}):
    tokens = {'final': set(), 'new': set()}
    if len(text) < 6:
        return tokens
    if text[:1]+text[-1:] not in ['{}', '[]']:
        return tokens

    dct = None
    try:  # JSON
        dct = json.loads(text)
    except:
        pass

    if dct is None:
        try:  # Python dict
            dct = ast.literal_eval(text)
        except:
            pass

    if dct is None:
        try:  # JavaScript Object
            dct = demjson.decode(text)
        except:
            pass

    if dct is not None:
        dct_tokens = dict_keys_values(dct)
        values = list_str(dct_tokens['values'])
        tokens = {
            'final': set(list_str(dct_tokens['keys']) + values),
            'new': set(values)
        }
        return tokens

    return tokens


tokenizers_all = {
    'dict': tokenizer_dict,
    'env': tokenizer_env,
    'split': tokenizer_split,
    'strip': tokenizer_strip
}


def tokenize_output(text, text_cmd='', substring='', current_cmd={}, tokenizers=['dict', 'env', 'split', 'strip'], recursion_level=1):
    spacing = ' ' * recursion_level * 2
    recursion_level_num = f" {recursion_level:02d}"
    logging.debug(f"{recursion_level_num}{spacing}TEXT: {text}")
    result_tokens = []
    found_tokens = False
    for tokenizer_name in tokenizers:
        tokenizer = tokenizers_all[tokenizer_name]
        tokens = tokenizer(text, text_cmd=text_cmd, substring=substring, current_cmd=current_cmd)
        if len(tokens['final']) > 0 or len(tokens['new']) > 0:
            found_tokens = True
        tokens = {
            'final': filter_tokens(tokens['final'], substring),
            'new': filter_tokens(tokens['new'], substring)
        }
        logging.debug(f"{recursion_level_num}{spacing*2}{tokenizer_name} {tokens}")
        result_tokens += list(tokens['final'])
        if len(tokens['new']) > 0:
            for token in tokens['new']:
                result_tokens += list(
                    tokenize_output(token, text_cmd=text_cmd, substring=substring, current_cmd=current_cmd,
                                    recursion_level=(recursion_level + 1), tokenizers=tokenizers))
            break

    if result_tokens == []:
        r = set([text] if not found_tokens and substring.lower() in text.lower() else []) if text != '' else set()
        logging.debug(f"{recursion_level_num}{spacing}RETURN {r}")
        return r

    r = set(result_tokens)
    logging.debug(f"{recursion_level_num}{spacing}RETURN {r}")
    return r

def tokenize_output_sorted(*args, **kwargs):
    r = list(tokenize_output(*args, **kwargs))
    r = sorted(r)
    return r

if __name__ == '__main__':
    import sys
    import argparse
    logging.getLogger().setLevel(logging.DEBUG)

    argp = argparse.ArgumentParser(description="Tokenize output")
    argp.add_argument('--pipe', '-p', action='store_true')
    args = argp.parse_args()

    if args.pipe:
        stdin = '\n'.join(sys.stdin.readlines())
    else:
        print('Usage: echo "Hello world" | python tokenizer_outupt.py --pipe', file=sys.stderr)
        print('Example: \n', file=sys.stderr)
        stdin = '"Hello" {world}'

    tokens = tokenize_output_sorted(stdin.strip())
    print(tokens)
