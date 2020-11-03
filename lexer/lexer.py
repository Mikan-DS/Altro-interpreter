import re
import sys
from .tokens import token_exprs


def lex(characters):
    """Эта функция разбивает строку на теги, или же лексиомы. пр.

    bg = "photo-199827634_457239018" => [("bg", "ID"), ("=", "ASSIGN"), ("photo-199827634_457239018", "STR")]

    """
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens


