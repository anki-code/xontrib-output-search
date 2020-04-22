Fish out tokens from previous command output in xonsh.

## Install
```bash
xpip install -U git+https://github.com/anki-code/xontrib-fishout
```

## Usage
```
$ xonsh
> xontrib load fishout
```
Now you can use magic combinations `o-` and `o=` and tab button to show tokens list. Token is a something like word from previous output. 
* `o-` is for searching by substring in token 
* `o=` is for searching by beginning of token 

To keep in mind the magic combinations imagine fishing. Symobol `o` is the lake and `-` is fishing rod. On the standard the keyboard this buttons are very close.

For example to get the token which exactly starts from `htt` you can do: 
```
> echo "Fish out from any output with https://github.com/anki-code/xontrib-fishout"
Fish out from any output with https://github.com/anki-code/xontrib-fishout
> curl o=htt<press tab>
```
As result the `o=htt` combination will be replaced to full URL from previous output. 

## Environment
| Environment variable          | Default | Description |
| ----------------------------- | ------- | ----------- |
| `XONTRIB_FISHOUT_SYMBOL`      | `'o'`     | First symbol to init the completer. |
| `XONTRIB_FISHOUT_FUNCTIONS`   | `{'in': '-', 'startswith': '='}` | Function and the second symbol to init the completer. | 

## Use cases
### cat
Use `cat file | head` because for `cat file`  the output will not be captured by xonsh.

## Thanks
* I was inspired by @con-f-use`s [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks!
