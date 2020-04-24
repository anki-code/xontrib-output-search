#!/usr/bin/env xonsh

import re

output_search_prefix = 'f__'
clean_regexp = re.compile(r'[\n\r\t]')
color_regexp = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
env_regexp = re.compile(r'^([A-Z0-9_]+?)=(.*)$')


def _tokenizer_simple_splitter(text, text_cmd='', substring='', current_cmd={}):
    tokens = clean_regexp.sub(' ', color_regexp.sub('', str(text))).strip().split(' ')
    substring_lower = substring.lower()
    selected_tokens = [t for t in tokens if len(t) > 1 and substring_lower in t.lower()]
    return set(selected_tokens) if selected_tokens != [text] else set()


framed_regexp = re.compile(r'^["\'{,:]*(.+?)[,}"\':]*$')
def _generator_frame_stripping(token, substring=''):
    g = framed_regexp.match(token)
    if g:
        tokens = [g.group(1)]
        substring_lower = substring.lower()
        return [t for t in tokens if len(t) > 1 and substring_lower in t.lower()]
    return []


def _generator_env(token, substring=''):
    tokens = []
    g = env_regexp.match(token)
    if g:
        env_var = g.group(1)
        value = g.group(2)
        values = value.split(':')
        tokens = values + [env_var, value] + tokens
    substring_lower = substring.lower()
    return [t for t in tokens if len(t) > 1 and substring_lower in t.lower()]


_tokenizers = {
    'simple_splitter': _tokenizer_simple_splitter
}

_generators = {
    'frame_stripping': _generator_frame_stripping,
    'env': _generator_env
}

def _parse(text, text_cmd='', substring='', current_cmd={}):
    tokenizer_tokens = []
    for name, tokenizer in _tokenizers.items():
        for token in tokenizer(text, text_cmd, substring, current_cmd):
            if len(token) > 2:
                tokenizer_tokens += [token]

    if tokenizer_tokens == []:
        return set()

    result_tokens = []
    for token in tokenizer_tokens:
        result_tokens += [token]
        for name, generator in _generators.items():
            for gen_token in generator(token, substring=substring):
                if len(gen_token) > 2:
                    result_tokens += [gen_token]

    for token in result_tokens:
        result_tokens += list(_parse(token, text_cmd=text_cmd, substring=substring, current_cmd=current_cmd))

    return set(result_tokens)


def _xontrib_output_search_completer(prefix, line, begidx, endidx, ctx):
    """
    Get new arguments from previous command output use Alt+F hotkey or f__ prefix before tab key.
    """
    if prefix.startswith(output_search_prefix):
        current_cmd = {'prefix': prefix, 'line': line, 'begidx': begidx, 'endidx': endidx}
        prefix_text = prefix[len(output_search_prefix):]
        prev = __xonsh__.xontrib_output_search_previous_output
        output = prev['output'] if 'output' in prev else None
        cmd = prev['cmd'] if 'cmd' in prev else None
        tokens = _parse(text=output, text_cmd=cmd, substring=prefix_text, current_cmd=current_cmd) if output else []
        tokens = tokens if tokens else set([prefix_text])
        return (tokens, len(prefix))


__xonsh__.completers['xontrib_output_search'] = _xontrib_output_search_completer
__xonsh__.completers.move_to_end('xontrib_output_search', last=False)

__xonsh__.xontrib_output_search_previous_output = None
@events.on_postcommand
def _save_output(cmd: str, rtn: int, out: str or None, ts: list):
    if out is not None and str(out).strip() != '':
        __xonsh__.xontrib_output_search_previous_output = {'output': out, 'cmd': cmd}


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
