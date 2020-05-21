<p align="center">
Get identifiers, names, paths, URLs and words from the previous command output and use them for the next command in <a href="https://xon.sh">xonsh</a>.
</p>

<table width="100%">
<col style="width:33%">
<col style="width:33%">
<col style="width:33%">
<tbody>
<tr>
<td valign="top">
<b>Save time</b>. Forget about using mouse, touchpad or trackball to get any words from output to the next command.
</td>
<td valign="top">
<b>Secure</b>. The xontrib-output-search is not writing any output on the hard disk. Only latest not empty output stored in the memory. It works the same way as xonsh shell and the security level is the same.
</td>
<td valign="top">
<b>Universal</b>. Forget about searching autocomplete plugins for every app you use and get the identifiers from the output.
</td>
</tr>
</tbody>
</table>

<p align="center">  
If you like the idea of xontrib-output-search click ⭐ on the repo and stay tuned by watching releases.
</p>

## Install
```shell script
xpip install -U xontrib-output-search
echo 'xontrib load output_search' >> ~/.xonshrc
# Reload xonsh
```

## Usage
After `xontrib load output_search` you have two ways to select tokens from latest not empty output:
* Press <kbd>Alt</kbd> + <kbd>F</kbd> hotkeys
* Type `f__` and press <kbd>Tab</kbd> key  

If you use this key combination for another function and your muscle memory is strong just change the key before loading the xontrib:
```
$XONTRIB_OUTPUT_SEARCH_KEY='i'
xontrib load output_search
```

## Features
#### Words tokenizing
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

#### JSON, Python dict and JavaScript object tokenizing
```shell script
$ echo '{"Try": "xontrib-output-search"}'
{"Try": "xontrib-output-search"}
$ echo I should try se<Alt+F>
$ echo I should try xontrib-output-search
```    

#### env tokenizing
```shell script
$ env | grep ^PATH=
PATH=/one/two:/three/four
$ ls fo<Alt+F>
$ ls /three/four
```    

#### Complex prefixes autocomplete

Get the URL from previous output after typing `git+`:
```shell script
$ echo "Try https://github.com/anki-code/xontrib-output-search"
Try https://github.com/anki-code/xontrib-output-search

$ pip install git+xo<Alt+F>
$ pip install git+https://github.com/anki-code/xontrib-output-search
```
Get the port number from previous output while typing the URL:
```shell script
$ echo "The port number is 4242"
The port number is 4242

$ curl http://127.0.0.1:4<Alt+F>
$ curl http://127.0.0.1:4242
```

## Development

### Tokenizers
Tokenizer is a functions which extract tokens from the text.

| Priority | Tokenizer  | Text  | Tokens |
| ---------| ---------- | ----- | ------ |
| 1        | **dict**   | `{"key": "val as str"}` | `['key', 'val as str']` |
| 2        | **env**    | `PATH=/bin:/etc` | `['PATH', '/bin:/etc', '/bin', '/etc']` |   
| 3        | **split**  | `Split  me \n now!` | `['Split', 'me', 'now!']` |   
| 4        | **strip**  | `{Hello}` | `['Hello']` |   

You can create your tokenizer and add it to `tokenizers_all` in `tokenize_output.py`.

Tokenizing is a recursive process where every tokenizer returns `final` and `new` tokens. 
The `final` tokens directly go to the result list of tokens. The `new` tokens go to all 
tokenizers again to find new tokens. As result if there is a mix of json and env data 
in the output it will be found and tokenized in appropriate way.  

### Test and debug
Run tests:
```shell script
cd ~
git clone https://github.com/anki-code/xontrib-output-search
cd xontrib-output-search
pytest
```
To debug the tokenizer:
```shell script
echo "Hello world" | python tokenize_outupt.py --pipe
```
Check that `output_search` loaded:
```shell script
$ xontrib list output_search
output_search  installed  loaded

$ completer list | grep output_search
xontrib_output_search
```

## Known issues
#### `cat file` is not captured
Workaround: `cat file | head`.

#### Alt+F combination may not working in PyCharm terminal
Workaround: `f__` + <kbd>Tab</kbd>.

## Thanks
I was inspired by [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks @con-f-use!
