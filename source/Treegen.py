from .BLOCKS import *


class Gen:

    def __init__(self, lexer):

        self.treedeep = 0
        self.mustraise = False
        self.treepath = []
        self.block = []

        self.tree = {}

        self.defaults, self.variables = {}, {}

        self.lexer = lexer

    def __add__(self, tags):

        lexs = [i[1] for i in tags]
        level = lexs.count("TAB")

        if level < self.treedeep:

            for i in range(self.treedeep - level):
                self.treepath.pop(-1)

            self.treedeep = level

        elif level == self.treedeep and not self.mustraise:
            pass

        elif self.mustraise and level == self.treedeep:
            self.mustraise = False

        else:
            raise Exception("Wrong structure: " + str(tags))

        print("path", self.treepath)

        if 'ENDBLOCK' in lexs:
            self.treedeep += 1
            self.mustraise = True

            old = self.get_element_from_block
            self.treepath.append(len(self.get_element_from_block))
            old.append([])

        for i in range(level):
            tags.remove(('    ', 'TAB'))
            lexs.remove('TAB')

        self.get_element_from_block.append(tags)

    def __call__(self):

        print("GEN")

        self.treepath.clear()

        for block in self.block:

            if isinstance(block[0], list):
                # print("new block")

                label_name = None
                if block[0][0][0] == "label":
                    label_name = block[0][1][0]
                else:
                    raise SyntaxError("In root block only label can be definded!")

                self.treepath.append(label_name)
                block = self.interp(block, 1, "Book_name")

                self.tree[label_name] = block()


            else:
                print(block)

                self.get_action(block)

        return {i: (v[0][1:-1] if v[1] == "STR" else int(v[0]))
                for i, v in zip(self.defaults, self.defaults.values())
                }, self.tree

    def interp(self, block, i=0, parrent=None, lastblock=None):

        Block = self.get_block(i, block, parrent, lastblock)
        child = str(Block)

        lastblock = None

        print("BLOCK:", child)

        for e in block:

            if isinstance(e[0], list):

                e = self.interp(e, 1, child, lastblock)

                b = e()

                if b:
                    Block + b
                    lastblock = e

            else:
                print(e)

                e = self.get_action(e)

                if e:
                    Block + e

        return Block

    def get_action(self, tags):

        lexs = [i[1] for i in tags]

        if 'ASSIGN' in lexs:
            print("ASSIGN")

            if lexs[0] == 'ID' and len(tags) > 2:
                self.variables[tags[0][0]] = self.PYTHON(tags[2:])
            elif tags[0][0] == "default" and lexs[1] == 'ID' and len(tags) > 3:
                self.defaults[tags[1][0]] = self.PYTHON(tags[3:])
            else:
                raise Exception("Cannot assign value")

        else:

            tagst, lexst = tags.copy(), lexs.copy()

            if not tags[0][0] == "Jump":
                self.undefind(tagst, lexst)

            if lexst[0] == "STR":  # ACTION SAY
                kwargs = {"what": tagst[0][0][1:-1]}
                if len(lexs) - 1 and lexst[1] == "STR":
                    kwargs["what"], kwargs["who"] = tagst[1][0][1:-1], kwargs["what"]

                return Say(**kwargs)

            elif lexs[0] == "SPECIAL":
                if tags[0][0] == "Show":

                    if len(tagst) != 2:

                        raise SyntaxError("Show must take one argument")

                    elif tagst[1][1] != "STR":

                        raise ValueError("Wrong argument for Show")

                    return Show(tagst[1][0][1:-1])
                elif tags[0][0] == "Jump":

                    if len(tags) != 2:

                        raise SyntaxError("Jump must take one argument")

                    elif tags[1][1] != "ID":

                        raise ValueError("Wrong argument for Jump")

                    return Jump(tags[1][0])

                elif tags[0][0] == "return":

                    if len(tags) != 1:
                        raise SyntaxError("return takes no argument")

                    return Return()

                else:
                    raise SyntaxError("Syntax error 2")

            elif lexs[0] == "PYTHON":
                print(tags[0][0][1:])
                tags = self.lexer(tags[0][0][1:])

                return Assign(tags[0][0], create_python_function(tags))

            else:
                raise SyntaxError("Syntax error 1" + str(lexs))

    def get_block(self, i, block, parrent, lastblock=None):

        Block = block.pop(0)[:-1]
        print(Block)

        if Block[0][0] == "menu":
            Block = menu(Block)
        elif Block[0][1] == "STR" and parrent == "menu":
            Block = menu_e(Block)

        elif Block[0][0] == "label":
            if i > 1:
                raise SyntaxError("Cannot defind label here!")
            Block = label(Block)

        elif Block[0][0] == "if":

            Block = iF(Block)

        elif Block[0][0] == "else":

            print("LB", lastblock)

            if isinstance(lastblock, iF):

                Block = Else(lastblock.action)

            else:
                raise SyntaxError("else statement can be only after if statement")

        else:
            raise KeyError("KeyError 1")

        return Block

    @property
    def get_element_from_block(self):

        element = self.block

        for p in self.treepath:
            element = element[p]

        return element

    def str(self, tags):

        txt = ""

        for tag in tags:
            txt += tag[0] + " "

        return txt

    def PYTHON(self, EVAL):

        code = ''
        for c in EVAL:
            if c[1] == "ID":
                co = self.value(c[0])[0]
            else:
                co = c[0]

            if c[1] != "ID":
                if not (c[1] == "STR" or c[1] == "INT"):
                    raise Exception("For this version it can assign only str and int")

            code += co

        code = eval(code)
        STR = '"' if isinstance(code, str) else ""
        return f'{STR}{str(code)}{STR}', "STR" if STR else "INT"

    def value(self, ID):

        if ID in self.variables:
            value = self.variables[ID]
        elif ID in self.defaults:
            value = self.defaults[ID]
        else:
            raise ValueError(f"{ID} is not defined")

        return value

    def undefind(self, tags, lexs):
        for i, element in enumerate(tags):

            if element[1] == "ID":
                tags[i] = self.value(element[0])
                lexs[i] = tags[i][1]
