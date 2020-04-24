#!/usr/bin/env xonsh

import re

output_search_prefix = 'f__'
clean_regexp = re.compile(r'[\n\r\t]')
color_regexp = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
framed_regexp = re.compile(r'^["\'{,:]*(.+?)[,}"\':]*$')
env_regexp = re.compile(r'^([A-Z0-9_]+?)=(.*)$')

def _generator(token, substring):
    """
    Create alternatives for token.
    """
    tokens = [token]
    if len(token) > 2:
        g = framed_regexp.match(token)
        if g:
            tokens = [g.group(1)] + tokens
        g = env_regexp.match(token)
        if g:
            env_var = g.group(1)
            value = g.group(2)
            values = value.split(':')
            tokens = values + [env_var, value] + tokens
    return [t for t in tokens if substring in t]


def _tokenizer(text, substring=''):
    """
    Split text to tokens.
    """
    tokens = clean_regexp.sub(' ', color_regexp.sub('', str(text))).strip().split(' ')
    selected_tokens = []
    for t in tokens:
        if len(t) > 1 and substring.lower() in t.lower():
            selected_tokens += _generator(t, substring)
    return set(selected_tokens)


def _xontrib_output_search_completer(prefix, line, begidx, endidx, ctx):
    """
    Get new arguments from previous command output use Alt+F hotkey or f__ prefix before tab key.
    """
    if prefix.startswith(output_search_prefix):
        prefix_text = prefix[len(output_search_prefix):]
        text = __xonsh__.xontrib_output_search_previous_output
        tokens = _tokenizer(text, substring=prefix_text) if text else []
        if tokens:
            return (tokens, len(prefix))
        else:
            return (set([prefix_text]), len(prefix))


__xonsh__.completers['xontrib_output_search'] = _xontrib_output_search_completer
__xonsh__.completers.move_to_end('xontrib_output_search', last=False)

__xonsh__.xontrib_output_search_previous_output = None
@events.on_postcommand
def _save_output(cmd: str, rtn: int, out: str or None, ts: list):
    if out is not None and str(out).strip() != '':
        __xonsh__.xontrib_output_search_previous_output = out


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
