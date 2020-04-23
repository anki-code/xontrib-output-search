Fish out tokens from previous command output in xonsh.

## Install
```bash
xpip install -U git+https://github.com/anki-code/xontrib-fishout
```

## Usage
```
xontrib load fishout
```
Now you can use:
* `Alt`+`F` hotkey
* `f__` prefix with tab button 

to show tokens list from latest output. Token is a something like word from previous output. 

For example to get the token which exactly starts from `htt` you can do: 
```
> echo "Fish out from any output with https://github.com/anki-code/xontrib-fishout"
Fish out from any output with https://github.com/anki-code/xontrib-fishout
> curl htt<Alt+F>
```
As result the `htt` will be replaced to full URL from previous output. 

Another example:
```
> echo "Fish out from any output with https://github.com/anki-code/xontrib-fishout"
Fish out from any output with https://github.com/anki-code/xontrib-fishout
> curl  htt<Alt+F>
```
As result the `htt` will be replaced to full URL from previous output. 

## Tokenizer and generator
Tokenizer is the function which extract tokens (words) from the output. After this every token go to generator to search alternatives.

For example:
```
$ echo '{"Some_json_data": 123}'
{"Some_json_data": 123}
$ <Alt+F>
```
The tokenizer will return two tokens `{"Some_json_data":` and `123}` then generator found that some text framed 
into special charecters. It will clean it and return new `Some_json_data` and `123` tokens. The result list will be sorted 
and you will get the list with:
* `123` (generated token)
* `Some_json_data` (generated token)
* `{"Some_json_data":` (original token)
* `123}":` (original token)

It's really cool! 

You can enrich tokenizer and generator for your tasks! Feel free to make pool request with improvements or if you need 
completely different behavior of tokenizer and generator let's think how to create ability to elegant replace the default functions.  

## Known issues
### `cat` is not captured
Use `cat file | head` instead.

## Thanks
* I was inspired by @con-f-use`s [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks!
