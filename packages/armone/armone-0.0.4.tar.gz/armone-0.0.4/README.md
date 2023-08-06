# Armone

A powerful command-line tool to obfuscate python scripts effectively!

## Installation
```sh
pip install armone pipx
pipx ensurepath
pipx install armone
```
## Usage
Obfuscate `my_code.py` and generate a new file `obfuscated.py` in the cwd:
```sh
armone my_code.py
```
Specify the output file:
```sh
armone my_code.py -o obfuscated.py
```
## Features
* Removes all comments and docstrings
* Renames all the functions, classes, and variables
* Inflates code by inserting junk code [IN PROGRESS]
* Messes up the formatting and adds confusing comments [IN PROGRESS]
* Puts the code through up to 32 layers of encoding ranging from base 1 to base 90
* Uses zlib and LZMA for further obfuscation and to reduce file size [IN PROGRESS]