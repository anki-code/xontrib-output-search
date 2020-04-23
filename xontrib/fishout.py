#!/usr/bin/env xonsh

import re

fishout_prefix = 'f__'
clean_regexp = re.compile(r'[\n\r\t]')
color_regexp = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
framed_regexp = re.compile(r'^["\'{,:]*(.+?)[,}"\':]*$')

def _generator(token):
    """
    Create alternatives for token. Example: token '"Value"' has unquoted 'Value' alternative.
    """
    token_variation = []
    if len(token) > 2:
        g = framed_regexp.match(token)
        if g:
            token_variation += [g.group(1)]
    return token_variation if token_variation != [token] else []


def _tokenizer(text, substring=''):
    """
    Split text to tokens.
    """
    tokens = clean_regexp.sub(' ', color_regexp.sub('', str(text))).strip().split(' ')
    selected_tokens = []
    for t in tokens:
        if len(t) > 1 and substring.lower() in t.lower():
            selected_tokens += [t] + _generator(t)
    return set(selected_tokens)


def _xontrib_fishout_completer(prefix, line, begidx, endidx, ctx):
    """
    To get suggestion of latest output tokens use Alt+F hotkey or f__ prefix before tab key.
    """
    if prefix.startswith(fishout_prefix):
        prefix_text = prefix[len(fishout_prefix):]
        text = __xonsh__.xontrib_fishout_previous_output
        tokens = _tokenizer(text, substring=prefix_text) if text else []
        if tokens:
            return (tokens, len(prefix))
        else:
            return (set([prefix_text]), len(prefix))


__xonsh__.completers['xontrib_fishout'] = _xontrib_fishout_completer
__xonsh__.completers.move_to_end('xontrib_fishout', last=False)

__xonsh__.xontrib_fishout_previous_output = None
@events.on_postcommand
def _save_output(cmd: str, rtn: int, out: str or None, ts: list):
    if out is not None and str(out).strip() != '':
        __xonsh__.xontrib_fishout_previous_output = out


try:
    @events.on_ptk_create
    def outout_keybindings(prompter, history, completer, bindings, **kw):
        if __xonsh__.env.get('SHELL_TYPE') in ["prompt_toolkit", "prompt_toolkit2"]:
            handler = bindings.add
        else:
            handler = bindings.registry.add_binding

        @bindings.add('escape', 'f')
        def _(event):
            if __xonsh__.xontrib_fishout_previous_output is not None:
                text = event.current_buffer.text
                splitted = str(text).split(' ')
                space = '' if text == '' or len(splitted) == 1 else ' '
                prefix = splitted[-1]
                text_with_completer = ' '.join(splitted[:-1]) + f'{space}{fishout_prefix}{prefix}'
                event.current_buffer.reset()
                event.current_buffer.insert_text(text_with_completer)
                event.current_buffer.start_completion(select_first=True)

except Exception as e:
    print('xontrib-fishout: Cannot set shortcuts')
    raise
