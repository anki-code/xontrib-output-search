"""Get identifiers, paths, URLs and words from the previous command output and use them for the next command in xonsh shell. """

import re, subprocess
from tokenize_output.tokenize_output import tokenize_output

if not __xonsh__.env.get('XONSH_CAPTURE_ALWAYS', False) and not "TMUX" in __xonsh__.env:
    print('xontrib-output-search: Capturing is not working. Please read https://github.com/tokenizer/xontrib-output-search#note')

_key_meta = __xonsh__.env.get('XONTRIB_OUTPUT_SEARCH_KEY_META', 'escape')
_key = __xonsh__.env.get('XONTRIB_OUTPUT_SEARCH_KEY', 'f')
_key_binding = __xonsh__.env.get('XONTRIB_OUTPUT_SEARCH_KEY_BINDING', None)

if _key_binding is None and _key_meta == 'escape' and _key == 'f':
    from xonsh.platform import ON_DARWIN
    if ON_DARWIN:
        _key_binding = __xonsh__.env['XONTRIB_OUTPUT_SEARCH_KEY_BINDING'] = 'c-f'
        _key_meta = __xonsh__.env['XONTRIB_OUTPUT_SEARCH_KEY_META'] = None

_add_previous_cmd_to_output = True
_support_special_chars_in_prefix = True

_output_search_prefix = _key + '__'

def prev_special_char_pos(s, chars=':;+-_~=/\\{[(<>|#"\'^$%&?!.,'):
    for i in reversed(range(0, len(s))):
        if s[i] in chars:
            return i
    return None


__xonsh__.xontrib_output_search_completion = False
__xonsh__.xontrib_output_search_previous_output = None

def _xontrib_output_search_completer(prefix, line, begidx, endidx, ctx):
    """
    Get new arguments from previous command output use Alt+F hotkey or f__ prefix before tab key.
    """
    is_output_search_prefix = prefix.startswith(_output_search_prefix)
    if __xonsh__.xontrib_output_search_completion or is_output_search_prefix:
        __xonsh__.xontrib_output_search_completion = False
        current_cmd = {'prefix': prefix, 'line': line, 'begidx': begidx, 'endidx': endidx}
        prev = __xonsh__.xontrib_output_search_previous_output
        if prev and 'output' in prev:
            cmd = prev['cmd']
            output = prev['output']
            substring = prefix[len(_output_search_prefix):] if is_output_search_prefix else prefix
            tokens = tokenize_output(text=output, text_cmd=cmd, substring=substring, current_cmd=current_cmd)
            if _add_previous_cmd_to_output:
                tokens = set.union(tokens, tokenize_output(text=cmd, text_cmd=cmd, substring=substring, current_cmd=current_cmd))

            if _support_special_chars_in_prefix and tokens == set() and not is_output_search_prefix:
                sc_pos = prev_special_char_pos(prefix)
                if sc_pos is not None:
                    prefix_after_char = prefix[sc_pos + 1:]
                    prefix_before_char = prefix[:sc_pos + 1]
                    if prefix_before_char != _output_search_prefix:
                        tokens = tokenize_output(text=output, text_cmd=cmd, substring=prefix_after_char, current_cmd=current_cmd)
                        if _add_previous_cmd_to_output:
                            tokens = set.union(tokens, tokenize_output(text=cmd, text_cmd=cmd, substring=prefix, current_cmd=current_cmd))
                        tokens = set([prefix_before_char + t for t in tokens])

            tokens = tokens if tokens else set([prefix])
            return (tokens, len(prefix))


__xonsh__.completers['xontrib_output_search'] = _xontrib_output_search_completer
__xonsh__.completers.move_to_end('xontrib_output_search', last=False)

def _tmux_current_pane_contents():
    if not "TMUX" in __xonsh__.env:
        return None
    else:
        try:
            return subprocess.check_output(["tmux", "capture-pane", "-p"], timeout=1).decode()
        except:
            return None

_color_regexp = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
@events.on_postcommand
def _save_output(cmd: str, rtn: int, out: str or None, ts: list, **kwargs):
    out = out or _tmux_current_pane_contents()
    if out is not None:
        out = out.strip()
        if out:
            __xonsh__.xontrib_output_search_previous_output = {'output': _color_regexp.sub('', out), 'cmd': cmd}

try:
    @events.on_ptk_create
    def outout_keybindings(prompter, history, completer, bindings, **kw):
        if __xonsh__.env.get('SHELL_TYPE') in ["prompt_toolkit", "prompt_toolkit2"]:
            handler = bindings.add
        else:
            handler = bindings.registry.add_binding

        bind = (_key_binding,) if _key_binding else (_key_meta, _key)

        @bindings.add(*bind)
        def _(event):
            if __xonsh__.xontrib_output_search_previous_output is not None:
                __xonsh__.xontrib_output_search_completion=True
                event.current_buffer.start_completion(select_first=True)

except Exception as e:
    print('xontrib-output-search: Cannot set shortcuts')
    raise
