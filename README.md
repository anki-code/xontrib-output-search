Fish out tokens from previous command output in xonsh.

## Install
```bash
xpip install git+https://github.com/anki-code/xontrib-fishout
```

## Usage
```
$ xonsh
> $XONSH_STORE_STDOUT = True
> xontrib load fishout
```
This command adds new completer to search by text in tokens from the previous output. Type in command line:
*  `o-[text]` and press tab to search the text as substring
*  `o=[text]` and press tab to search the text as a beginning of token

Example: 
```
> echo "Fish out from any output with https://github.com/anki-code/xontrib-fishout"
Fish out from any output with https://github.com/anki-code/xontrib-fishout
> curl o=htt<tab>
```

## Environment
| Environment variable          | Default |
| ----------------------------- | ------- |
| `XONTRIB_FISHOUT_DEPTH`       | 1       |
| `XONTRIB_FISHOUT_SYMBOL`      | `o`     |
| `XONTRIB_FISHOUT_FUNCTIONS`   | `{'in': '-', 'startswith': '='}` |

## Thanks
* I was inspired by @con-f-use`s [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks!
