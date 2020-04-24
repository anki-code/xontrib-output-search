#!/usr/bin/env xonsh

import re
import json

output_search_prefix = 'f__'

clean_regexp = re.compile(r'[\n\r\t]')
def _tokenizer_split(text, text_cmd='', substring='', current_cmd={}):
    tokens = clean_regexp.sub(' ', text).strip().split(' ')
    substring_lower = substring.lower()
    selected_tokens = [t for t in tokens if len(t) > 1 and substring_lower in t.lower()]
    return set(selected_tokens) if selected_tokens != [text] else set()


framed_regexp = re.compile(r'^["\'{,:]*(.+?)[,}"\':]*$')
def _tokenizer_strip(text, text_cmd='', substring='', current_cmd={}):
    g = framed_regexp.match(text)
    if g:
        token = g.group(1)
        if token == text:
            return []
        elif len(token) > 1 and substring.lower() in token:
            return set(token)
    return set()


env_regexp = re.compile(r'^([A-Z0-9_]+?)=(.*)$')
def _tokenizer_env(text, text_cmd='', substring='', current_cmd={}):
    tokens = []
    g = env_regexp.match(text)
    if g:
        env_var = g.group(1)
        value = g.group(2)
        values = value.split(':')
        tokens = values + [env_var, value]
    substring_lower = substring.lower()
    return set([t for t in tokens if len(t) > 1 and substring_lower in t.lower()])


def _tokenizer_json(text, text_cmd='', substring='', current_cmd={}):
    if len(text) > 0 and text[:1] == '{' and text[-1:] == '}':
        try:
            j = json.loads(text)
            tokens = list(j.keys()) + [str(v) for v in j.values()]
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
        for token in tokenizer(text, text_cmd, substring, current_cmd):
            if len(token) > 2:
                tokenizer_tokens += [token] + list(_parse(token, text_cmd=text_cmd, substring=substring, current_cmd=current_cmd))

    if tokenizer_tokens == []:
        return set()

    return set(tokenizer_tokens)


def _xontrib_output_search_completer(prefix, line, begidx, endidx, ctx):
    """
    Get new arguments from previous command output use Alt+F hotkey or f__ prefix before tab key.
    """
    if prefix.startswith(output_search_prefix):
        current_cmd = {'prefix': prefix, 'line': line, 'begidx': begidx, 'endidx': endidx}
        prefix_text = prefix[len(output_search_prefix):]
        prev = __xonsh__.xontrib_output_search_previous_output
        cmd = prev['cmd'] if 'cmd' in prev else None
        output = prev['output'] if 'output' in prev else None
        tokens = _parse(text=output, text_cmd=cmd, substring=prefix_text, current_cmd=current_cmd) if output else []
        tokens = tokens if tokens else set([prefix_text])
        return (tokens, len(prefix))


__xonsh__.completers['xontrib_output_search'] = _xontrib_output_search_completer
__xonsh__.completers.move_to_end('xontrib_output_search', last=False)


color_regexp = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
__xonsh__.xontrib_output_search_previous_output = None
@events.on_postcommand
def _save_output(cmd: str, rtn: int, out: str or None, ts: list):
    if out is not None and out.strip() != '':
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
                text = event.current_buffer.text
                splitted = str(text).split(' ')
                space = '' if text == '' or len(splitted) == 1 else ' '
                prefix = splitted[-1]
                text_with_completer = ' '.join(splitted[:-1]) + f'{space}{output_search_prefix}{prefix}'
                event.current_buffer.reset()
                event.current_buffer.insert_text(text_with_completer)
                event.current_buffer.start_completion(select_first=True)

except Exception as e:
    print('xontrib-output-search: Cannot set shortcuts')
    raise
