#!/usr/bin/env xonsh

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
    
    text = __xonsh__.xontrib_fishout_previous_output
    tokens = _tokenizer(text, prefix=prefix, func=catch_function) if text else []
    return (set(tokens), len(prefix))

__xonsh__.completers['xontrib_fishout'] = _xontrib_fishout_completer
__xonsh__.completers.move_to_end('xontrib_fishout', last=False)

__xonsh__.xontrib_fishout_previous_output = None
@events.on_postcommand
def _save_output(cmd: str, rtn: int, out: str or None, ts: list):
    if out is not None:
        __xonsh__.xontrib_fishout_previous_output = out
