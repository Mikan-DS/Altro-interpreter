"""

"Камеры хранения" для блоков кода

"""


from modules.actions import *
from .extra import create_python_function


class label:
    def __init__(self, args):


        if len(args) != 2:
            raise SyntaxError("Label is defined wrong " + str(args))

        self.name = args[1]

        self.block = []

    def __add__(self, other):

        self.block.append(other)

        return self

    def __call__(self):

        return Label(self.block)

    def __str__(self):

        return "label"

class menu:
    def __init__(self, args):

        if len(args) > 1:
            raise SyntaxError("Menu not have any arguments!")

        self.block = []

        self.label = None

    def __add__(self, other):

        if isinstance(other, Say):

            if self.label:
                raise SyntaxError("Incorrect Syntax")

            self.label = other(None)["message"]

        else:
            self.block.append(other)

        return self

    def __call__(self):

        kwargs = {}

        if self.label:
            kwargs["label"] = self.label

        kwargs["buttons"] = {}

        for name, action in self.block:
            kwargs["buttons"][name[0][1:-1]] = action


        return Menu(**kwargs)

    def __str__(self):

        return "menu"



class menu_e:

    def __init__(self, args):

        if len(args) > 1:
            raise SyntaxError("Menu elements not have any arguments!")

        self.name = args[0]
        self.block = []

    def __add__(self, other):
        self.block.append(other)

        return self

    def __call__(self):

        return [self.name, Label(self.block) if self.block.__len__() > 1 else self.block[0]]

    def __str__(self):
        return "menu_e"


class iF:

    def __init__(self, args):

        if len(args) == 1:

            raise SyntaxError("condition is not defined!")

        self.condition = create_python_function(args[1:])

        self.block = []

        self.action = None

    def __add__(self, other):

        self.block.append(other)

        return self

    def __call__(self):

        self.action = If(self.condition, Label(self.block) if self.block.__len__() > 1 else self.block[0])

        return self.action

    def __str__(self):
        return "if"


class Else:
    def __init__(self, IF):

        self.orig = IF
        self.block = []

    def __add__(self, other):

        self.block.append(other)

        return self

    def __call__(self):

        self.orig.else_action = Label(self.block) if self.block.__len__() > 1 else self.block[0]

    def __str__(self):
        return "else"
