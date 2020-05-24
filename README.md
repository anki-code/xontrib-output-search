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

## Use cases
#### Get URL from output
```shell script
$ echo "Try https://github.com/xxh/xxh"
Try https://github.com/xxh/xxh
$ git clone xx<Alt+F>
$ git clone https://github.com/xxh/xxh
```

#### Get key or value from JSON, Python dict and JavaScript object
```shell script
$ echo '{"Try": "xontrib-output-search"}'
{"Try": "xontrib-output-search"}
$ echo I should try se<Alt+F>
$ echo I should try xontrib-output-search
```    

#### Get the path from environment
```shell script
$ env | grep ^PATH=
PATH=/one/two:/three/four
$ ls fo<Alt+F>
$ ls /three/four
```    

#### Complete the complex prefix

Get the URL from previous output after typing `git+`:
```shell script
$ echo "Try https://github.com/tokenizer/xontrib-output-search"
Try https://github.com/tokenizer/xontrib-output-search

$ pip install git+xo<Alt+F>
$ pip install git+https://github.com/tokenizer/xontrib-output-search
```
Get the port number from previous output while typing the URL:
```shell script
$ echo "The port number is 4242"
The port number is 4242

$ curl http://127.0.0.1:4<Alt+F>
$ curl http://127.0.0.1:4242
```

#### Get arguments from command help
```shell script
$ lolcat -h
...
$ lolcat --s<Alt+F>
$ lolcat --seed=SEED
```
## Development

The xontrib-output-search is using [tokenize-output](https://github.com/tokenizer/tokenize-output) for tokenizing.

Checking that `output_search` xontrib has been loaded:
```shell script
$ xontrib list output_search
output_search  installed  loaded

$ completer list | grep output_search
xontrib_output_search
```

## Known issues
#### `cat file` is not captured
Workaround: `cat file | head` or `cat file | grep text`.

#### Alt+F combination may not working in PyCharm terminal
Workaround: `f__` + <kbd>Tab</kbd>.

#### The Alt+F in the readline is to move forward
Workaround: set `$XONTRIB_OUTPUT_SEARCH_KEY='i'` before `xontrib load output_search`.

## Thanks
I was inspired by [xontrib-histcpy](https://github.com/con-f-use/xontrib-histcpy). Thanks @con-f-use!
