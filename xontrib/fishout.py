#!/usr/bin/env xonsh

if __xonsh__.env.get('XONSH_STORE_STDOUT') is not True:
    raise ValueError("To use xontrib-fishout set $XONSH_STORE_STDOUT=True")

if __xonsh__.env.get('XONSH_HISTORY_BACKEND') != 'json':
    raise ValueError("To use xontrib-fishout set $XONSH_HISTORY_BACKEND='json'")

_depth = int(__xonsh__.env.get('XONTRIB_FISHOUT_DEPTH') or 1)
_symbol = str(__xonsh__.env.get('XONTRIB_FISHOUT_SYMBOL') or 'o')
_functions = dict(__xonsh__.env.get('XONTRIB_FISHOUT_FUNCTIONS') or {'in': '-', 'startswith': '='})

def _tokenizer(text, prefix='', func='in'):
    tokens = str(text).strip().replace('\n', ' ').replace('\r', ' ').split(' ')
    selected_tokens = []
    for t in tokens:
        if len(t) > 1:
            if func == 'in' and prefix[2:].lower() in t.lower():
                selected_tokens.append(t)
            elif func == 'startswith' and t.lower().startswith(prefix[2:].lower()):
                selected_tokens.append(t)
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
    
    words = []
    i = 0
    for h in reversed(__xonsh__.history):
        text = str(h.out).strip()
        if h.out is not None and text != '':
            words += _tokenizer(text, prefix=prefix, func=catch_function)
        i += 1
        if i >= _depth:
            break

    return (set(words), len(prefix))

__xonsh__.completers['xontrib_fishout'] = _xontrib_fishout_completer
__xonsh__.completers.move_to_end('xontrib_fishout', last=False)
