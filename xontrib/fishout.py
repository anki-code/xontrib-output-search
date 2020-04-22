#!/usr/bin/env xonsh

import re

_symbol = str(__xonsh__.env.get('XONTRIB_FISHOUT_SYMBOL') or 'o')
_functions = dict(__xonsh__.env.get('XONTRIB_FISHOUT_FUNCTIONS') or {'in': '-', 'startswith': '='})

clean_regexp = re.compile(r'[\n\r\t]')
color_regexp = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
framed_regexp = re.compile(r'^["\'{,:](.+?)[,}"\':]+$')

def _generator(token):
    """
    Create alternatives for token. Example: token '"Value"' has unquoted 'Value' alternative.
    """
    token_variation = []
    if len(token) > 2:
        g = framed_regexp.match(token)
        if g:
            token_variation += [g.group(1)]
    return token_variation

def _tokenizer(text, prefix='', func='in'):
    """
    Split text to tokens.
    """
    tokens = clean_regexp.sub(' ', color_regexp.sub('', str(text))).strip().split(' ')
    selected_tokens = []
    for t in tokens:
        if len(t) > 1:
            if func == 'in' and prefix[2:].lower() in t.lower():
                selected_tokens += [t] + _generator(t)
            elif func == 'startswith' and t.lower().startswith(prefix[2:].lower()):
                selected_tokens += [t]
    return selected_tokens

def _xontrib_fishout_completer(prefix, line, begidx, endidx, ctx):
    catch_function = None
    for f, s in _functions.items():
        begin = f'{_symbol}{s}'
        if prefix.startswith(begin):
            catch_function = f
            break
    if not catch_function:
        return None
    
    text = __xonsh__.xontrib_fishout_previous_output
    tokens = _tokenizer(text, prefix=prefix, func=catch_function) if text else []
    return (set(tokens), len(prefix))

__xonsh__.completers['xontrib_fishout'] = _xontrib_fishout_completer
__xonsh__.completers.move_to_end('xontrib_fishout', last=False)

__xonsh__.xontrib_fishout_previous_output = None
@events.on_postcommand
def _save_output(cmd: str, rtn: int, out: str or None, ts: list):
    if out is not None and str(out).strip() != '':
        __xonsh__.xontrib_fishout_previous_output = out
