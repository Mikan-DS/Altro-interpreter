"""

Токены для определения тегов

"""


RESERVED = 'RESERVED'
STR = 'STR'
INT = 'INT'
ID = 'ID'
BOOL = "BOOL"

LOGICAL = "LOGICAL"
IF = "IF"

SPECIAL = "SPECIAL"


token_exprs = [

    (r'    ',                   "TAB"),
    (r'\$[^\n]*',               "PYTHON"),

    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'\*',                    RESERVED),
    (r'/',                     RESERVED),

    (r':',                       "ENDBLOCK"),


    (r'==|!=|<=|>=|<|>',          LOGICAL),

    (r'\+|\-|\*|\/',              "OPERATOR"),


    (r'=',                        "ASSIGN"),

    (r'label|menu',               "BLOCK"),

    (r'default|Show|return|Jump', SPECIAL),


    (r'if|else',                  IF),

    (r'and|not|or',               LOGICAL),


    (r'[0-9]+',                   INT),
    (r'True|False',               BOOL),
    (r'"[^"]+"',                  STR),
    (r'[A-Za-z][A-Za-z0-9_]*',    ID),
]
