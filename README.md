<p align="center">
Get tokens (identifiers/names/paths/URLs) from the previous command output and use them for the next command in <a href="https://xon.sh">xonsh</a>.
</p>
<p align="center">
Forget about using mouse to select identifiers, names, paths or URLs.<br> 
Forget about searching autocomplete plugins for every app you use.<br> 
</p>

<p align="center">  
If you like the idea of xontrib-output-search click ⭐ on the repo and stay tuned.
</p>

## Install
```shell script
xpip install -U git+https://github.com/anki-code/xontrib-output-search
echo 'xontrib load output_search' >> ~/.xonshrc
```

## Usage
After `xontrib load output_search` you can select tokens from latest output:
* Press <kbd>Alt</kbd> + <kbd>F</kbd> hotkey
* Or type `f__` and press <kbd>Tab</kbd> key  

Text example:
```shell script
$ echo "Hello world"
Hello world
$ echo The second word is wo<Alt+F>
$ echo The second word is world
```

URL example: 
```shell script
$ echo "Try https://github.com/xxh/xxh"
Try https://github.com/xxh/xxh
$ git clone xx<Alt+F>
$ git clone https://github.com/xxh/xxh
```

JSON example:
```shell script
$ echo '{"Try": "xontrib-output-search"}' # JSON data
{"Try": "xontrib-output-search"}
$ echo I should try x<Alt+F>
$ echo I should try xontrib-output-search
```    

ENV example:
```shell script
$ env | grep ^PATH=
PATH=/one/two:/three/four
$ ls fo<Alt+F>
$ ls /three/four
```    

## Development
### Clone and test
```shell script
cd ~
git clone https://github.com/anki-code/xontrib-output-search
cd xontrib-output-search
pytest
```

### Tokenizer and generator
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
#### `cat` is not captured
Workaround: `cat file | head`.

#### Alt+F may not working in PyCharm terminal
Workaround: `f__` + <kbd>Tab</kbd>.

## Thanks
* I was inspired by [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks @con-f-use!
