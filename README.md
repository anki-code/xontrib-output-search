Fish out tokens from the previous command output and use them for the next command.

* You'll forget about selecting identifiers/names/urls by mouse.
* You'll forget about searching autocomplete plugins for every app you use. 

For example if you're using docker 
just run `docker ps` and you ready to inspect container by ID with `docker inspect <Alt+F>`. Then you see json data with
`"NetworkID":"06f82ee31"` and you can just type `echo NetworkID is 06<Alt+F>` to get it. It's really great! 

## Install
```shell script
xpip install -U git+https://github.com/anki-code/xontrib-fishout
echo 'xontrib load fishout' >> ~/.xonshrc
```

## Usage
After `xontrib load fishout` you can select tokens from latest output:
* Press <kbd>Alt</kbd> + <kbd>F</kbd> hotkey
* Or type `f__` and press <kbd>Tab</kbd> key  

For example to get the tokens which contains `xon`: 
```shell script
$ echo "Fish out from any output with https://github.com/anki-code/xontrib-fishout"
Fish out from any output with https://github.com/anki-code/xontrib-fishout
$ git clone xon<Alt+F>
```
As result the `xon` will be replaced to full URL from previous output. 

Another example:
```shell script
$ echo '{"Try": "xontrib-fishout"}' # JSON data
{"Try": "xontrib-fishout"}
$ echo I should try x<Alt+F>
```
As result the `x` will be replaced to `xontrib-fishout`.  

## Tokenizer and generator
Tokenizer is the function which extract tokens (words) from the output. After this every token go to generator to search alternatives.

For example:
```shell script
$ echo '{"ssh": "https://github.com/xxh/xxh"}' # JSON data
{"ssh": "https://github.com/xxh/xxh"}
$ <Alt+F>
```
The tokenizer will return two tokens `{"ssh":` and `"https://github.com/xxh/xxh"}` then generator found that some text framed 
into special charecters. It will clean the tokens and return new `ssh` and `https://github.com/xxh/xxh` ones. The result list will be sorted 
and you will get the list with:
* `ssh` (generated token)
* `https://github.com/xxh/xxh` (generated token)
* `{"ssh":` (original token)
* `"https://github.com/xxh/xxh"}` (original token)

It's really cool! 

You can enrich tokenizer and generator for your tasks! Feel free to make pool request with improvements or if you need 
completely different behavior of tokenizer and generator let's think how to create ability to elegant replace the default functions.  

## Known issues
### `cat` is not captured
Use `cat file | head` instead.

## Thanks
* I was inspired by [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks @con-f-use!
