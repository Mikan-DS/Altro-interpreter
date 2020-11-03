from lexer import lex
from source.Treegen import Gen
from pickle import dump
from sys import argv

filename = "script.apy"

if len(argv) > 1:
    filename = argv[1]

analyze = Gen(lex)

with open(filename, encoding="utf-8") as file:
    for line in file: #подготавливает код к обработки

        tags = lex(line)

        if tags: analyze + tags
    else: #Обработка и запись в файл
        dump(analyze(), open(filename + "c", "wb"))

