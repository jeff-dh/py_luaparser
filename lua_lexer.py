import ply.lex as lex

keywords = {
    "nil": "NIL",
    "return": "RETURN",
    "do": "DO",
    "end": "END",
    "false": "FALSE",
    "true": "TRUE",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "while": "WHILE",
    "break": "BREAK",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "elseif": "ELSEIF",
    "local": "LOCAL",
    "function": "FUNCTION",
    "repeat": "REPEAT",
    "until": "UNTIL",
    "for": "FOR",
    "in": "IN",
}

tokens = [
    'IDENTIFIER',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LT',
    'GT',
    'LTE',
    'GTE',
    'NE',
    'EQUALS',
    'HASH',
    'CONCAT',
    'TDOT',
    'CIRCUMFLEX',
    'STRING',
]

literals = ["{", "}", "[", "]", "(", ")", '=', ';', ':',
            ',', '.', '\'', '"', '%']

tokens += keywords.values()

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LT = r'<'
t_GT = r'>'
t_LTE = r'<='
t_GTE = r'>='
t_NE = r'~='
t_EQUALS = r'=='
t_HASH = r'\#'
t_CONCAT = r'\.\.'
t_TDOT = r'\.\.\.'
t_CIRCUMFLEX = r'\^'

# copy & past from
#https://stackoverflow.com/questions/36597386/match-c-strings-and-string-literals-using-regex-in-python
t_STRING = r'(?P<prefix>(?:\bu8|\b[LuU])?)(?:"(?P<dbl>[^"\\]*(?:\\.[^"\\]*)*)"|\'(?P<sngl>[^\'\\]*(?:\\.[^\'\\]*)*)\')|R"([^"(]*)\((?P<raw>.*?)\)\4"'

t_ignore = " \t"

def t_NUMBER(t):
    r'([0-9]*[.][0-9]+)|([0-9]+)'
    if "." in t.value:
        t.value = float(t.value)
        return t
    else:
        t.value = int(t.value)
        return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'--[^\n]*'
    pass

def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} <lua_file>')
        sys.exit(-1)

    with open(sys.argv[1]) as f:
        source = f.read()

    lexer = lex.lex(debug=False)
    lexer.input(source)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
