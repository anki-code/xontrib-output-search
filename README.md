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
If you like the idea of xontrib-output-search click ⭐ on the repo and stay tuned.
</p>

## Install
```shell script
xpip install -U git+https://github.com/anki-code/xontrib-output-search
echo 'xontrib load output_search' >> ~/.xonshrc
# Reload xonsh
```

## Usage
After `xontrib load output_search` you have two ways to select tokens from latest not empty output:
* Press <kbd>Alt</kbd> + <kbd>F</kbd> hotkeys
* Type `f__` and press <kbd>Tab</kbd> key  

## Features
#### Word tokenizing
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

#### JSON and Python dict tokenizing
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
### Clone and test
```shell script
cd ~
git clone https://github.com/anki-code/xontrib-output-search
cd xontrib-output-search
pytest
```

### Tokenizers
Tokenizers are functions which extract tokens from the output. You can create your tokenizer and add it to `_tokenizers`.

Current tokenizers: 
```python
tokenizers = {
    'dict': tokenizer_dict,    # Extract keys and values from python dict or json
                               # Example: '{"key": "val as str"}' -> ['key', 'val as str']

    'env': tokenizer_env       # Extract name and values from env-like text
                               # Example: 'PATH=/bin:/etc' -> ['PATH', '/bin:/etc', '/bin', '/etc']
    
    'split': tokenizer_split,  # Splitting text by white spaces (space, tab, new line)
                               # Example: 'Split  me \n now!' -> ['Split', 'me', 'now!']

    'strip': tokenizer_strip,  # Extract values from special charecters
                               # Example: '{Hello}' -> ['Hello']
}
```
## Known issues
#### `cat` is not captured
Workaround: `cat file | head`.

#### Alt+F combination may not working in PyCharm terminal
Workaround: `f__` + <kbd>Tab</kbd>.

## Thanks
I was inspired by [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks @con-f-use!
