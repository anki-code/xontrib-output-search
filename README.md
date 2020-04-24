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
Tokenizer is the function which extract tokens (words) from the output. After this every token go to the generator function to search alternatives.

For example:
```shell script
$ echo 'Try ssh with "https://github.com/xxh/xxh"'
Try ssh with "https://github.com/xxh/xxh"
$ <Alt+F>
```
The tokenizer will return tokens `Try`, `ssh`, `with` and `"https://github.com/xxh/xxh"` then generator found that some text framed 
into special charecters. It will clean the tokens and return `https://github.com/xxh/xxh` as the new token. The result list will be sorted 
and you will get the list with:
```
https://github.com/xxh/xxh
"https://github.com/xxh/xxh"
ssh
Try
with
```

## Known issues
#### `cat` is not captured
Workaround: `cat file | head`.

#### Alt+F may not working in PyCharm terminal
Workaround: `f__` + <kbd>Tab</kbd>.

## Thanks
* I was inspired by [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks @con-f-use!
