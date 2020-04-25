#!/usr/bin/env xonsh

import re
import json
import ast
from collections.abc import Iterable

output_search_prefix = 'f__'
add_previous_cmd_to_output = True
support_special_chars_in_prefix = True

__xonsh__.xontrib_output_search_completion = False
__xonsh__.xontrib_output_search_previous_output = None

def filter_tokens(tokens, substring='', len_min=1):
    substring_lower = substring.lower()
    return {
        'final': set([t for t in tokens['final'] if len(t) > len_min and substring_lower in t.lower()]),
        'new': set([t for t in tokens['new'] if len(t) > len_min and substring_lower in t.lower()])
    }


clean_regexp = re.compile(r'[\n\r\t]')
def _tokenizer_split(text, text_cmd='', substring='', current_cmd={}):
    tokens = clean_regexp.sub(' ', text).strip().split(' ')
    if tokens != [text]:
        tokens = {'final': set(), 'new': set(tokens)}
    else:
        tokens = {'final': set(), 'new': set()}
    return tokens


framed_regexp = re.compile(r'^["\'({\[,:;]+(.+?)[,})\]"\':;]+$')
def _tokenizer_strip(text, text_cmd='', substring='', current_cmd={}):
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

env_regexp = re.compile(r'^([a-zA-Z0-9_]+?)=(.*)$')
def _tokenizer_env(text, text_cmd='', substring='', current_cmd={}):
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


def _dict_keys_values(d, target='values'):
    result = {'keys': [], 'values': []}
    if d is None:
        return result
    elif type(d) is dict:
        for k in d:
            result['keys'] += [k]
            val_result = _dict_keys_values(d[k], 'values')
            result['keys'] += val_result['keys']
            result['values'] += val_result['values']
        return result
    elif type(d) in [list, set]:
        for v in d:
            val_result = _dict_keys_values(v, 'values')
            result['keys'] += val_result['keys']
            result['values'] += val_result['values']
        return result
    else:
        result[target] += [d]
        return result

def _list_str(lst):
    if isinstance(lst, Iterable):
        return [str(l) for l in lst]
    else:
        return str(lst)

def _tokenizer_dict(text, text_cmd='', substring='', current_cmd={}):
    tokens = {'final': set(), 'new': set()}
    if len(text) < 6:
        return tokens

    if text[:1]+text[-1:] in ['{}', '[]']:
        dct = None
        try:
            dct = json.loads(text)
        except:
            pass

        if dct is None:
            try:
                dct = ast.literal_eval(text)
            except:
                pass

        if dct is not None:
            dct_tokens = _dict_keys_values(dct)
            values = _list_str(dct_tokens['values'])
            tokens = {
                'final': set(_list_str(dct_tokens['keys']) + values),
                'new': set(values)
            }
            return tokens

    return tokens


_tokenizers = {
    'dict': _tokenizer_dict,
    'env': _tokenizer_env,
    'split': _tokenizer_split,
    'strip': _tokenizer_strip
}


def _parse(text, text_cmd='', substring='', current_cmd={}, first=True):
    # print(f"TEXT: text")
    result_tokens = []
    found_tokens = False
    for tokenizer_name, tokenizer in _tokenizers.items():
        tokens = tokenizer(text, text_cmd=text_cmd, substring=substring, current_cmd=current_cmd)
        if len(tokens['final']) > 0 or len(tokens['new']) > 0:
            found_tokens = True
        tokens = filter_tokens(tokens, substring)
        # print(f"    {tokenizer_name}: {tokens}")
        result_tokens += list(tokens['final'])
        if len(tokens['new']) > 0:
            for token in tokens['new']:
                result_tokens += list(_parse(token, text_cmd=text_cmd, substring=substring, current_cmd=current_cmd, first=False))
            break

    if result_tokens == []:
        return set([text] if not found_tokens and substring.lower() in text.lower() else []) if text != '' else set()

    return set(result_tokens)


def prev_special_char_pos(s, chars=':;+-_~=/\\{[(<>|#"\'^$%&?!.,'):
    for i in reversed(range(0, len(s))):
        if s[i] in chars:
            return i
    return None


def _xontrib_output_search_completer(prefix, line, begidx, endidx, ctx):
    """
    Get new arguments from previous command output use Alt+F hotkey or f__ prefix before tab key.
    """
    is_output_search_prefix = prefix.startswith(output_search_prefix)
    if __xonsh__.xontrib_output_search_completion or is_output_search_prefix:
        __xonsh__.xontrib_output_search_completion = False
        current_cmd = {'prefix': prefix, 'line': line, 'begidx': begidx, 'endidx': endidx}
        prev = __xonsh__.xontrib_output_search_previous_output
        if 'output' in prev:
            cmd = prev['cmd']
            output = prev['output']
            substring = prefix[len(output_search_prefix):] if is_output_search_prefix else prefix
            tokens = _parse(text=output, text_cmd=cmd, substring=substring, current_cmd=current_cmd)
            if add_previous_cmd_to_output:
                tokens = set.union(tokens, _parse(text=cmd, text_cmd=cmd, substring=substring, current_cmd=current_cmd))

            if support_special_chars_in_prefix and tokens == set() and not is_output_search_prefix:
                sc_pos = prev_special_char_pos(prefix)
                if sc_pos is not None:
                    prefix_after_char = prefix[sc_pos + 1:]
                    prefix_before_char = prefix[:sc_pos + 1]
                    if prefix_before_char != output_search_prefix:
                        tokens = _parse(text=output, text_cmd=cmd, substring=prefix_after_char, current_cmd=current_cmd)
                        if add_previous_cmd_to_output:
                            tokens = set.union(tokens, _parse(text=cmd, text_cmd=cmd, substring=prefix, current_cmd=current_cmd))
                        tokens = set([prefix_before_char + t for t in tokens])

            tokens = tokens if tokens else set([prefix])
            return (tokens, len(prefix))


__xonsh__.completers['xontrib_output_search'] = _xontrib_output_search_completer
__xonsh__.completers.move_to_end('xontrib_output_search', last=False)


color_regexp = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
@events.on_postcommand
def _save_output(cmd: str, rtn: int, out: str or None, ts: list):
    if out is not None:
        out = out.strip()
        if out:
            __xonsh__.xontrib_output_search_previous_output = {'output': color_regexp.sub('', out), 'cmd': cmd}

try:
    @events.on_ptk_create
    def outout_keybindings(prompter, history, completer, bindings, **kw):
        if __xonsh__.env.get('SHELL_TYPE') in ["prompt_toolkit", "prompt_toolkit2"]:
            handler = bindings.add
        else:
            handler = bindings.registry.add_binding

        @bindings.add('escape', 'f')
        def _(event):
            if __xonsh__.xontrib_output_search_previous_output is not None:
                __xonsh__.xontrib_output_search_completion=True
                event.current_buffer.start_completion(select_first=True)

except Exception as e:
    print('xontrib-output-search: Cannot set shortcuts')
    raise
