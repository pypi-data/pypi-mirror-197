"""
VSOL - Versatile Simple Objective Language

"""

import re
import json


__version__ = '0.0.1'
__author__ = 'Md. Almas Ali'

# Tokens
NAME = re.compile(r'^\t?([a-zA-Z_][a-zA-Z0-9_]*)$')  # name
NUMBER = re.compile(r'^(\d+)$')  # number

INT = re.compile(r'^(\d+)$')  # int
FLOAT = re.compile(r'^(\d+\.\d+)$')  # float
STRING = re.compile(r'^\"(.*)\"$')  # string
BOOL = re.compile(r'^(\w+)\s*=\s*(true|false)$')  # bool
ARRAY = re.compile(r'^(\[.*\])$')  # array
NULL = re.compile(r'^(null)$')  # null

COMMENT = re.compile(r'^(\#.*)$')  # comment
NEWLINE = re.compile(r'^(\n)$')  # newline
INDENT = re.compile(r'^(\t)$')  # indent
EOF = re.compile(r'^(\Z)$')  # end of file

LBRACKET = re.compile(r'^(\[)$')  # left bracket
RBRACKET = re.compile(r'^(\])$')  # right bracket

OBJECT = re.compile(r'^\.([a-zA-Z_][a-zA-Z0-9_]*)$')  # .object
ATTRIBUTE = re.compile(r'^\t?(\w+)\s*=\s*(.*)$')  # attribute = value
CONSTANT = re.compile(r'^(@\w+\s*=\s*\w+)$')  # @constant = value


class VSOLParser:
    def __init__(self, vsol_str):
        self.vsol_str = vsol_str
        self.current_object = None
        self.line_number = 0
        self.result = {}

    def parse(self):
        lines = self.vsol_str.split('\n')
        lines = [line for line in lines if line.strip() != '']

        for line in lines:
            self.line_number += 1

            ######### working on here ##########
            if match := INDENT.match(line):
                print(match)
            line = line.strip()
            ####################################

            if match := OBJECT.match(line):
                self.current_object = match.group(1)
                self.result[self.current_object] = {}

            elif match := ATTRIBUTE.match(line):
                key = match.group(1)
                value = match.group(2)

                if self.current_object:

                    #########List parsing##########
                    # check if value contains a list
                    if '[' in value and ']' in value:
                        self.result[self.current_object][key] = list(
                            value.strip()[1:-1].split(','))
                    ################################

                    if value == 'true' or value == 'false':
                        self.result[self.current_object][key] = value

                    elif value == 'null':
                        self.result[self.current_object][key] = value

                    elif _value := STRING.match(value):
                        self.result[self.current_object][key] = _value.group(1)

                    elif _value := ARRAY.match(value):
                        self.result[self.current_object][key] = _value.group(1)

                    elif _value := INT.match(value):
                        self.result[self.current_object][key] = _value.group(1)

                    elif _value := FLOAT.match(value):
                        self.result[self.current_object][key] = _value.group(1)

                    else:
                        self.result[self.current_object][key] = value

                else:
                    if value == 'true' or value == 'false':
                        self.result[key] = value

                    elif value == 'null':
                        self.result[key] = value

                    elif _value := STRING.match(value):
                        self.result[key] = _value.group(1)

                    elif _value := ARRAY.match(value):
                        self.result[key] = _value.group(1)

                    elif _value := INT.match(value):
                        self.result[key] = _value.group(1)

                    elif _value := FLOAT.match(value):
                        self.result[key] = _value.group(1)

                    else:
                        self.result[key] = value

            elif match := COMMENT.match(line):
                pass
            else:
                print(f'Error: line no {self.line_number}: \"{line}\" !')

            # elif match := ATTRIBUTE.match(line):
            #     key = match.group(1)
            #     value = match.group(2)
            #     # check if value contains a list
            #     if '[' in value and ']' in value:
            #         # if so, parse the list and add it to the result
            #         values = value.strip()[1:-1].split(',')
            #         self.result[self.current_object][key] = [v.strip()
            #                                              for v in values]
            #     else:
            #         # otherwise, add the key-value pair to the result
            #         self.result[self.current_object][key] = value.strip()

        return self.result


class VSOL:
    def __init__(self) -> None:
        """
        Creates a VSOL object from a VSOL string.
        """

    def get(self, key: str) -> str:
        """
        Returns the value of the object with the given key.
        """
        return self.result.get(key)

    def set(self, key: str, value: str) -> None:
        """
        Sets the value of the object with the given key.
        """
        self.result[key] = value

    def dict(self) -> dict:
        """
        Returns a dictionary representation of the VSOL file.
        """
        return self.result

    def json(self) -> json:
        """
        Returns a JSON string.
        """
        return json.dumps(self.result)

    def pretty(self) -> json:
        """
        Returns a pretty-printed JSON string.
        """
        return json.dumps(self.result, indent=4)

    def load(self, file: str) -> None:
        """
        Parses the VSOL file.
        """
        with open(file, 'r') as f:
            self.__parser(f.read())

    def loads(self, vsol_str: str) -> None:
        """
        Parses the given VSOL string.
        """
        self.__parser(vsol_str)

    def __parser(self, vsol_str: str):
        """
        Parses the VSOL string.
        """
        self.vsol_str = vsol_str
        self.parser = VSOLParser(self.vsol_str)
        self.result = self.parser.parse()

    def __contains__(self, key: str) -> bool:
        """
        Returns True if the object with the given key exists in the VSOL file.
        """
        return key in self.result

    def __len__(self) -> int:
        """
        Returns the number of objects in the VSOL file.
        """
        return len(self.result)

    def __iter__(self) -> iter:
        """
        Returns an iterator over the objects in the VSOL file.
        """
        return iter(self.result)

    def __getitem__(self, key: str) -> str:
        """
        Returns the value of the object with the given key.
        """
        return self.result.get(key)

    def __setitem__(self, key: str, value: any) -> None:
        """
        Sets the value of the object with the given key.
        """
        self.result[key] = value

    def __str__(self) -> str:
        """
        Returns a string representation of the VSOL file.
        """
        return '<VSOL Object>'

    def __repr__(self) -> str:
        """
        Returns a string representation of the VSOL file.
        """
        return '<VSOL Object>'


if __name__ == '__main__':
    # with open('../example.vsol', 'r') as f:
    #     vsol_str = f.read()

    parser = VSOL()
    # parser.loads(vsol_str)
    parser.load('../example.vsol')
    # parser['project']['site_name'] = 'Deleted!'
    # parser.get('project')['site_name'] = 'Deleted!'
    # parser.get('project')
    # parser.set('project', {})
    print(
        parser.dict()
    )
