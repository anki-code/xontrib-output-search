#!/usr/bin/env xonsh

import re
import json

output_search_prefix = 'f__'
add_previous_cmd_to_output = True

clean_regexp = re.compile(r'[\n\r\t]')
def _tokenizer_split(text, text_cmd='', substring='', current_cmd={}):
    tokens = clean_regexp.sub(' ', text).strip().split(' ')
    substring_lower = substring.lower()
    selected_tokens = [t for t in tokens if len(t) > 1 and substring_lower in t.lower()]
    return set(selected_tokens) if selected_tokens != [text] else set()


framed_regexp = re.compile(r'^["\'({\[,:;]+(.+?)[,})\]"\':;]+$')
def _tokenizer_strip(text, text_cmd='', substring='', current_cmd={}):
    g = framed_regexp.match(text)
    if g:
        token = g.group(1)
        if token == text:
            return []
        elif len(token) > 1 and substring.lower() in token:
            return set([token])
    return set()


env_regexp = re.compile(r'^([a-zA-Z0-9_]+?)=(.*)$')
def _tokenizer_env(text, text_cmd='', substring='', current_cmd={}):
    if len(text) < 4:
        return set()

    tokens = []
    g = env_regexp.match(text)
    if g:
        env_var = g.group(1)
        value = g.group(2)
        values = value.split(':')
        tokens = values + [env_var, value]
    substring_lower = substring.lower()
    return set([t for t in tokens if len(t) > 1 and substring_lower in t.lower()])


def _dict_keys_values(d):
    if type(d) in [dict, list]:
        result = []
        for i in d:
            result += _dict_keys_values(i)
            if type(d) == dict:
                result += _dict_keys_values(d[i])
        return result
    if d is None:
        return []
    else:
        return [str(d)]

def _tokenizer_json(text, text_cmd='', substring='', current_cmd={}):
    if len(text) < 6:
        return set()

    if text[:1]+text[-1:] in ['{}', '[]']:
        try:
            j = json.loads(text)
            tokens = list(set(_dict_keys_values(j)))
            substring_lower = substring.lower()
            selected_tokens = [t for t in tokens if len(t) > 1 and substring_lower in t.lower()]
            return set(selected_tokens)
        except:
            pass

    return set()


_tokenizers = {
    'split': _tokenizer_split,
    'strip': _tokenizer_strip,
    'json': _tokenizer_json,
    'env': _tokenizer_env
}


def _parse(text, text_cmd='', substring='', current_cmd={}):
    tokenizer_tokens = []
    for name, tokenizer in _tokenizers.items():
        for token in tokenizer(text, text_cmd=text_cmd, substring=substring, current_cmd=current_cmd):
            if len(token) > 2:
                tokenizer_tokens += [token] + list(_parse(token, text_cmd=text_cmd, substring=substring, current_cmd=current_cmd))

    if tokenizer_tokens == []:
        return set()

    return set(tokenizer_tokens)


def _xontrib_output_search_completer(prefix, line, begidx, endidx, ctx):
    """
    Get new arguments from previous command output use Alt+F hotkey or f__ prefix before tab key.
    """
    if __xonsh__.xontrib_output_search_completion or prefix.startswith(output_search_prefix):
        __xonsh__.xontrib_output_search_completion = False
        current_cmd = {'prefix': prefix, 'line': line, 'begidx': begidx, 'endidx': endidx}
        prev = __xonsh__.xontrib_output_search_previous_output
        if 'output' in prev:
            cmd = prev['cmd']
            output = prev['output']
            tokens = _parse(text=output, text_cmd=cmd, substring=prefix, current_cmd=current_cmd)

            if add_previous_cmd_to_output:
                tokens = set.union(tokens, _parse(text=cmd, text_cmd=cmd, substring=prefix, current_cmd=current_cmd))

            tokens = tokens if tokens else set([prefix])
            return (tokens, len(prefix))


__xonsh__.completers['xontrib_output_search'] = _xontrib_output_search_completer
__xonsh__.completers.move_to_end('xontrib_output_search', last=False)


color_regexp = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
__xonsh__.xontrib_output_search_previous_output = None
@events.on_postcommand
def _save_output(cmd: str, rtn: int, out: str or None, ts: list):
    if out is not None:
        out = out.strip()
        if out:
            __xonsh__.xontrib_output_search_previous_output = {'output': color_regexp.sub('', out), 'cmd': cmd}

__xonsh__.xontrib_output_search_completion=False
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
