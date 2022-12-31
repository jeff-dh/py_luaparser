# py_luaparser
A basic lua parser written in python using ply. It contains a grammar that parses more or less the whole language (`[[multiline comments]]` are missing and maybe something else).

It think it's pretty decent but haven't tested / used it a lot.

The parser only emits the positions of the top level statements. All other productions are empty stubs.


The grammar is based on

https://github.com/johan-bjareholt/lua-interpreter/blob/master/src/grammar.yy

from Johan Bjäreholt's lua-interpreter.

## usage

```sh
$ python lua_lexer.py test.lua
$ python lua_parser.py test.lua
```
