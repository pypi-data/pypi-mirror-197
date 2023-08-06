import random
import argparse

from .encoder import encode, decode
from .cleaner import clean
from .renamer import rename

def main():

    parser = argparse.ArgumentParser(description = "A command line tool to obfuscate python scripts!")

    parser.add_argument("input", type = str, nargs = 1,
                    metavar = "input_file_path", default = None,
                    help = "The path to the file that is to be obfuscated")
    parser.add_argument("-o", "--output", type = str, nargs = 1,
                    metavar = "output_file_path", default = ["obfuscated.py"],
                    help = "The path to the file that is to be obfuscated")

    args = parser.parse_args()
    
    with open(args.input[0], 'r') as read_obj:
        code = read_obj.read()
        code = clean(code)
        code = rename(code)

    for _ in range(random.randint(1, 32)):

        base = random.randint(1, 90)
        encoded = encode(code, base)
        code = f"import armone\neval(compile(armone.decode(r'{encoded}', {base}), '<string>', 'exec'))"

    with open(args.output[0], "w") as write_obj:
        write_obj.write(code)