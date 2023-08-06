import ast
import re
import random

class NameGenerator:

    def __init__(self):

        self.names = []
    
    def get_name(self):

        name = [random.choice(["O", "0"]) for i in range(75)]
        name.append("O")
        name.reverse()

        if not name in self.names:
            self.names.append(name)
            return ''.join(name)

        return self.get_name()


def get_strings(code):

    str_regex = "(('[^']*')|(\"[^\"]*\"))"
    strs = [tuple_[0] for tuple_ in re.findall(str_regex, code)]

    return strs

def insert_strings(strs, code):

    str_regex = "(('[^']*')|(\"[^\"]*\"))"

    for idx, tuple_ in enumerate(re.findall(str_regex, code)):
        code = code.replace(tuple_[0], strs[idx])
    
    return code


def rename(code):

    strs = get_strings(code)
    parsed = ast.parse(code)

    funcs = {node for node in ast.walk(parsed) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    classes = {node for node in ast.walk(parsed) if isinstance(node, ast.ClassDef)}
    args = {node.id for node in ast.walk(parsed) if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load)}
    attrs = {node.attr for node in ast.walk(parsed) if isinstance(node, ast.Attribute) and not isinstance(node.ctx, ast.Load)}

    for func in funcs:

        if func.args.args:
            for arg in func.args.args: args.add(arg.arg)
        if func.args.kwonlyargs:
            for arg in func.args.kwonlyargs: args.add(arg.arg)

        if func.args.vararg: args.add(func.args.vararg.arg)
        if func.args.kwarg: args.add(func.args.kwarg.arg)

    pairs = dict()
    gen = NameGenerator()

    for func in funcs:

        if func.name == "__init__": continue
        pairs[func.name] = gen.get_name()

    for _class in classes: pairs[_class.name] = gen.get_name()
    for arg in args: pairs[arg] = gen.get_name()
    for attr in attrs: pairs[attr] = gen.get_name()

    for key, value in pairs.items(): code = code.replace(key, value)

    return insert_strings(strs, code)
