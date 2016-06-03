from collections import defaultdict
import re


def read(path):
    prison = defaultdict(list)
    current_block = prison
    stack = [current_block]
    with open(path, "r") as data:
        for line in data:
            is_name = True
            is_new_block = False
            for word in re.findall(r'".*?"|\S+', line):
                if word == "BEGIN":
                    stack.append(current_block)
                    is_new_block = True
                elif word == "END":
                    current_block = stack.pop()
                elif is_new_block:
                    name = word
                    new_block = defaultdict(list)
                    current_block[name].append(new_block)
                    current_block = new_block
                    is_new_block = False
                elif is_name:
                    name = word
                    is_name = False
                else:
                    current_block[name].append(word)
                    is_name = True
    return prison


def write(path, prison):
    '''Write the previous data structure back to prison format'''
    with open(path, "w") as target:
        for line in _unpack(prison):
            target.write(line)


def _unpack(block):
    for name, entry_list in block.items():
        for entry in entry_list:
            if isinstance(entry, defaultdict):
                yield "BEGIN    " + name + "\n"
                for line in _unpack(entry):
                    yield "    " + line
                yield "END\n"
            else:
                yield name + "    " + entry + "\n"

