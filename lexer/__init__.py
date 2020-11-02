"""

Лексер для того что бы определять теги строчки кода


"""

from .lexer import lex

if __name__ == "__main__":

    while True:
        print(lex(input(">>>")))
