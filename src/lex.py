import re
from src.utils import *
from src.consts import *


def lex_analysis(source):
    file_c = open_file(source, COMPILE_ENUM.SOURCE)
    splits = split_content(file_c)
    return to_token(splits)


def split_content(content):
    r = []
    s = re.split(r'[\s]', ''.join(content))
    for i in s:
        r += re.split(r'([-\(\)+*/.;:<=>])', i)
    return list(filter(lambda it: it != '', r))


def to_token(splits):
    r = []
    for i in splits:
        if i in KEYWORDS:
            r.append(TokenUnit(TOKEN_TYPE_ENUM.KEYWORD, KEYWORD_MAP[i]))
        elif i in ';.':
            r.append(TokenUnit(TOKEN_TYPE_ENUM.SEP, i))
        elif i in OPS:
            r.append(TokenUnit(TOKEN_TYPE_ENUM.OP, i))
        elif re.match(r'\d+', i):
            r.append(TokenUnit(TOKEN_TYPE_ENUM.NUMBER, int(i)))
        elif len(i) == 1 and i in VARS:
            r.append(TokenUnit(TOKEN_TYPE_ENUM.VAR, i))
        else:
            raise SyntaxError('[LAX] Wrong token@{}'.format(i))
    return r
