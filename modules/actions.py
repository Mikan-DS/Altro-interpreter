from .extra import create_keyboard, PYTHON

###############################################################################
# типы actions
###############################################################################


class Input:
    """
        Tип события, после которого игра будет ждать реакции от пользователя. пр. Menu()
    """

    def __init__(self):
        pass


class Output:
    """
        Tип события, после которого игра будет ждать реакции от пользователя. пр. Menu()
    """

    def __init__(self):
        pass


class Internal:
    """
        Tип события, после которого игра будет ждать реакции от пользователя. пр. Menu()
    """

    def __init__(self):
        pass


###############################################################################
# actions
###############################################################################


###############################################################################
# События навигации глав
###############################################################################

class Label(Internal):
    """Нужны для корректных перемещений по сценарию

        Jump - переходит на другой Label на том же уровне, передает родительский уровень сестринскому
        Block - переходит на другой Label на уровень выше, в случае конца возвращается к изначальному Label
        Return - насильный вовзрат на родительский уровень, является дефолтным концом всех Label'ов

    """

    def __init__(self, block: list):
        super().__init__()
        self.block = block

    def __getitem__(self, item):
        try:
            return self.block[item]
        except:
            return Return()

    def __len__(self):
        return len(self.block)

    def __call__(self, player, *args):
        player.traceback.insert(0, [self, -1])


class Jump(Internal):
    """
    Перепрыгивает на другой Label на том же уровне, передает родительский уровень сестринскому

    """

    def __init__(self, label):
        super().__init__()

        self.label = label

    def __call__(self, player, *args):
        if isinstance(self.label, str):
            try:
                self.label = player.find_label_by_name(self.label)
            except Exception as e:
                print("EXCEPTION! : " + str(e))

        player.traceback[0] = [self.label, -1]


class Return(Internal):
    """
    Насильный вовзрат на родительский уровень, является дефолтным концом всех Label'ов
    """
    def __init__(self):
        super().__init__()

    def __call__(self, player, *args):

        if player.traceback:
            player.traceback[0][1] = len(player.traceback[0][0])




###############################################################################
# Output actions
###############################################################################


class Say(Output):
    """
    Say(what, who=None, name=None) => action

    где:

        what - речь персонажа
        who - имя или id персонажа


    """

    def __init__(self, what, who=None, name=None):
        super().__init__()
        self.text = what
        self.who = who
        self.name = name

    def __call__(self, player):
        """Возвращает инструкцию для сендера. => dict"""
        text = (self.who + ":\n\n       ") if self.who else ""
        text += self.text

        return {"message": text}

    def __str__(self):
        return self.text


class Show(Output):
    """
    Show(src) => action

    где:

        src (str) - vk image/video/audio url, that contains
        type-user_id-source_id. пр. "photo-194303024_457239055"

    """

    def __init__(self, src):

        super().__init__()
        self.source = src

    def __call__(self, *args):
        """Возвращает инструкцию для сендера. => dict"""

        return {"attachment": self.source}



###############################################################################
# Input actions
###############################################################################


class Menu(Input):
    """
    Menu(buttons, label) => action

    buttons (dict) - {name_1: action_1, name_2: action_2, ... }

        где:

            name - имя кнопки
            action - событие кнопки

    label - Сообщение которое пошлется вместе с меню


    """

    def __init__(self, buttons, label="Выбор:"):
        super().__init__()

        if isinstance(buttons, dict): #Лень скрипт менять
            buttons = list(zip(buttons.keys(), buttons.values()))

        self.keyboard = create_keyboard(buttons)
        self.label = label
        self.actions = [Jump(i[1]) if isinstance(i[1], str) else i[1] for i in buttons]#[i[1] for i in buttons]

    def __call__(self, player):

        player.mode = "choice"

        return {"keyboard": self.keyboard, "message": self.label}

    def click(self, n):
        print(len(self.actions), n)
        if len(self.actions) > n:
            return self.actions[n]
        return False


###############################################################################
# Internal actions
###############################################################################

class Assign(Internal):
    """
    Assign(value, dst) => action

    где:

    value - имя значения которое будет изменено
    dst (function) - Функция (lambda), возрат запуска которой будет новым значение для value-name

        Функция dst обязана принимать один аргумент. Пр.

                lambda player: player.values["yuri_love"] + 1

    """

    def __init__(self, value, dst):
        super().__init__()
        self.value = value
        self.dst = dst

    def __call__(self, player):
        """assign value"""

        if isinstance(self.dst, str):
            dst = PYTHON(self.dst, player)
        else:
            dst = self.dst(player)

        player.values[self.value] = dst


class If(Internal):
    """
    If(condition, action, else_action) => action

    condition (function) - function (lambda) that would be executed,
    whose return value must be bool (using for python "if")
        function must take one argument, example

            lambda player: 3 > 2

    action - can be label name, or mpy action. would be executed
    if condition return value be True
    else_action - can be label name, mpy action or None. would be executed
    if condition return value be False, or pass if else_action is None


    """

    def __init__(self, condition, action, else_action=None):
        super().__init__()
        self.condition = condition
        self.action = action
        self.else_action = else_action

    def __call__(self, player):
        """
        Check condition and execute


        """

        if isinstance(self.condition, str):
            condition = PYTHON(self.condition, player)
        else:
            condition = self.condition(player)

        if condition:
            player.action = self.action
            player.manager.new_action(player)
            return True
        elif self.else_action:
            player.action = self.else_action
            player.manager.new_action(player)
            return True
