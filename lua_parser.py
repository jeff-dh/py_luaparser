'''The grammar is based on
Johan Bjäreholt - lua-interpreter
https://github.com/johan-bjareholt/lua-interpreter/blob/master/src/grammar.yy
MIT License
'''

from lua_lexer import *
from lua_lexer import tokens as lexerTokens
from ply.yacc import yacc
from ply.lex import lex

class LuaParser:
    tokens = lexerTokens

    def __init__(self, filename):
        self.error = None

        self.lexer = lex(debug=False)
        self.lexer.filename = filename

        self.parser = yacc(module=self, debug=False)

    def parse(self, source):
        return self.parser.parse(source, lexer=self.lexer, tracking=True)

    def p_block(self, p):
        '''block	: chunk'''
        p[0] = p[1]

    def p_chunk(self, p):
        '''chunk	: chunk2 laststat
                    | chunk2
                    | laststat'''
        p[0] = p[1]
        if len(p) > 2:
            p[0] += p[2]

    def p_chunk2(self, p):
        '''chunk2	: stat optsemi
                    | chunk stat optsemi '''
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            assert len(p) == 4
            p[0] = p[1] + [p[2]]

    def p_optsemi(self, _):
        '''optsemi	: ';'
                    | empty'''
        pass

    def p_laststa(self, p):
        '''laststat : RETURN explist optsemi
                    | RETURN optsemi
                    | BREAK optsemi'''
        p[0] = [(p.lineno(0), p.lexpos(0))]

    def p_stat(self, p):
        '''stat	: varlist '=' explist
                | LOCAL namelist '=' explist
                | LOCAL namelist
                | FUNCTION funcname funcbody
                | LOCAL FUNCTION name funcbody
                | functioncall
                | DO block END
                | WHILE exp DO block END
                | REPEAT block UNTIL exp
                | if elseiflist else END
                | FOR name '=' exp ',' exp DO block END
                | FOR name '=' exp ',' exp ',' exp DO block END
                | FOR namelist IN explist DO block END'''
        p[0] = (p.lineno(0), p.lexpos(0))

    def p_if(self, _):
        '''if		: IF exp THEN block'''
        pass

    def p_elseiflis(self, _):
        '''elseiflist : elseif
                    | elseiflist elseif
                    | empty'''
        pass

    def p_elseif(self, _):
        '''elseif	: ELSEIF exp THEN block'''
        pass

    def p_else(self, _):
        '''else	: ELSE block
                | empty'''
        pass

    def p_var	(self, _):
        '''var		: name
                    | prefixexp '[' exp ']'
                    | prefixexp '.' name'''
        pass

    def p_varlist(self, _):
        '''varlist	: var
                | varlist ',' var'''
        pass

    def p_name(self, _):
        '''name	: IDENTIFIER'''
        pass

    def p_funcname(self, _):
        '''funcname : funcname2
                | funcname2 ':' name'''
        pass

    def p_funcname2(self, _):
        '''funcname2 : name
                | funcname2 '.' name'''
        pass

    def p_namelist(self, _):
        '''namelist : name
                | namelist ',' name'''
        pass

    def p_exp(self, _):
        '''exp		: NIL
                | FALSE
                | TRUE
                | NUMBER
                | string
                | TDOT
                | function
                | prefixexp
                | tableconstructor
                | op'''
        pass

    def p_explist(self, _):
        '''explist	: exp
                | explist ',' exp'''
        pass

    def p_prefixexp(self, _):
        '''prefixexp : var
                | functioncall
                | '(' exp ')' '''
        pass

    def p_function(self, _):
        '''function : FUNCTION funcbody'''
        pass

    def p_functioncall(self, _):
        '''functioncall : prefixexp args
                | prefixexp ':' name args'''
        pass

    def p_funcbody(self, _):
        '''funcbody : '(' parlist ')' block END
                | '(' ')' block END'''
        pass

    def p_parlist(self, _):
        '''parlist	: namelist
                | namelist ',' TDOT
                | TDOT'''
        pass

    def p_args(self, _):
        '''args	: '(' ')'
                | '(' explist ')'
                | tableconstructor
                | string'''
        pass

    def p_tableconstructor(self, _):
        '''tableconstructor : '{' fieldlist '}'
                | '{' '}' '''
        pass

    def p_field(self, _):
        '''field	: '[' exp ']' '=' exp
                | name '=' exp
                | exp'''
        pass

    def p_fieldlist(self, _):
        '''fieldlist : fieldlist2 optfieldsep'''
        pass

    def p_fieldlist2(self, _):
        '''fieldlist2 : field
                | fieldlist2 fieldsep field'''
        pass

    def p_optfieldsep(self, _):
        '''optfieldsep : fieldsep
                | empty'''
        pass

    def p_fieldsep(self, _):
        '''fieldsep : ','
                | ';' '''
        pass

    def p_string(self, _):
        '''string	: STRING'''
        pass

    def p_op(self, _):
        '''op      : op_1'''
        pass

    def p_op_1(self, _):
        '''op_1    : op_1 OR op_2
                | op_2'''
        pass

    def p_op_2(self, _):
        '''op_2    : op_2 AND op_3
                | op_3'''
        pass

    def p_op_3(self, _):
        '''op_3    : op_3 LT op_4
                | op_3 LTE op_4
                | op_3 GT op_4
                | op_3 GTE op_4
                | op_3 NE op_4
                | op_3 EQUALS op_4
                | op_4'''
        pass

    def p_op_4(self, _):
        '''op_4    : op_4 CONCAT op_5
                | op_5'''
        pass

    def p_op_5(self, _):
        '''op_5    : op_5 PLUS op_6
                | op_5 MINUS op_6
                | op_6'''
        pass

    def p_op_6(self, _):
        '''op_6    : op_6 TIMES op_7
                | op_6 DIVIDE op_7
                | op_6 '%' op_7
                | op_7'''
        pass

    def p_op_7(self, _):
        '''op_7    : NOT op_8
                | HASH op_8
                | MINUS op_8
                | op_8'''
        pass

    def p_op_8(self, _):
        '''op_8    : op_8 CIRCUMFLEX op_9
                | op_9'''
        pass

    def p_op_9(self, _):
        '''op_9    : exp'''
        pass

    def p_empty(self, _):
        '''empty : '''
        pass

    def p_error(self, p):
        e = SyntaxError('SyntaxError')
        if p:
            e.lineno = p.lineno
        else:
            e.lineno = -1
        self.error = e


def parse(source, filename):
    parser = LuaParser(filename)
    pos = parser.parse(source)
    if parser.error:
        return parser.error

    return pos

def getSourceChunks(source, filename):
    def _makeChunk(source, lastLineno, lastPos, pos):
        sourceChunk = source[lastPos: pos].rstrip()

        posRange = range(lastPos, lastPos + len(sourceChunk)+1)
        lineRange = range(lastLineno, lastLineno + sourceChunk.count('\n') + 1)
        return ((lineRange, posRange), sourceChunk)

    chunkPositions = parse(source, filename)
    if isinstance(chunkPositions, SyntaxError):
        # Syntax Error
        return chunkPositions

    chunks = []
    print(chunkPositions)
    lastLineno, lastPos = chunkPositions[0]
    for lineno, pos in chunkPositions[1:]:
        chunks.append(_makeChunk(source, lastLineno, lastPos, pos-1))

        lastPos = pos
        lastLineno = lineno

    chunks.append(_makeChunk(source, lastLineno, lastPos, -1))

    return chunks

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} <lua_file>')
        sys.exit(-1)

    with open(sys.argv[1]) as f:
        source = f.read()

    chunks = getSourceChunks(source, sys.argv[1])
    if isinstance(chunks, SyntaxError):
        print(chunks)
    else:
        for lineAndPosInfo, csource in chunks:
            print('--------------')
            print(csource)

