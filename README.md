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

### Tokenizers
Tokenizers are functions which extract tokens from the output. You can create your tokenizer and add it to `_tokenizers`.

Current tokenizers:
```python
_tokenizers = {
    
    'split': _tokenizer_split,  # Splitting text by white spaces (space, tab, new line)
                                # Example: 'Split  me \n now!' -> ['Split', 'me', 'now!']

    'strip': _tokenizer_strip,  # Extract values from special charecters
                                # Example: '{Hello}' -> ['Hello']
 
    'json': _tokenizer_json,    # Extract keys and values from JSON
                                # Example: '{"key": "val as str"}' -> ['key', 'val as str']

    'env': _tokenizer_env       # Extract name and values from env-like text
                                # Example: 'PATH=/bin:/etc' -> ['PATH', '/bin:/etc', '/bin', '/etc']
}
```
## Known issues
#### `cat` is not captured
Workaround: `cat file | head`.

#### Alt+F may not working in PyCharm terminal
Workaround: `f__` + <kbd>Tab</kbd>.

## Thanks
* I was inspired by [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks @con-f-use!
