from src.consts import *


def generating_analysis(syntax_tokens):
    asm_tokens = generate_asm(syntax_tokens)
    return fill_jump(asm_tokens)


def generate_asm(syntax_tokens):
    r = []
    for i in syntax_tokens:
        if i[0] == STATEMENT_TYPE_ENUM.WRITE:
            r.append(TokenUnit("PUT", VARS.index(i[1])))
        elif i[0] == STATEMENT_TYPE_ENUM.READ:
            r.append(TokenUnit("GET", VARS.index(i[1])))
        elif i[0] == STATEMENT_TYPE_ENUM.ASSIGN:
            r += assign(i)
        elif i[0] == STATEMENT_TYPE_ENUM.RELATION:
            r += relation(i)
        elif i[0] == STATEMENT_TYPE_ENUM.GOTO_REL:
            r[-1].flag = True
        elif i[0] == STATEMENT_TYPE_ENUM.GOTO_CJP:
            r.append(TokenUnit("CJP", i[1]))
        elif i[0] == STATEMENT_TYPE_ENUM.GOTO_UJP:
            r.append(TokenUnit("UJP", i[1]))
    return r


def fill_jump(asm_tokens):
    i = 0
    j = len(asm_tokens) - 1
    while True:
        while i < j and asm_tokens[i].flag != True:
            i += 1
        jpd = i
        i+=1
        while i < j and asm_tokens[i].unit_type != "CJP":
            i += 1
        while i < j and asm_tokens[j].unit_type != "UJP":
            j -= 1
        if i >= j:
            break
        asm_tokens[jpd].flag = False
        asm_tokens[i].value = j + 1
        asm_tokens[j].value = jpd + 1
        j-=1
    return asm_tokens


def assign(syntax):
    r = []
    r += polish(syntax[2])
    r.append(TokenUnit("STR", VARS.index(syntax[1])))
    return r


def polish(syntax):
    r = []
    if len(syntax) == 1:
        return [lodldc(syntax[0])]
    for i in syntax:
        if i.unit_type in [TOKEN_TYPE_ENUM.VAR, TOKEN_TYPE_ENUM.NUMBER]:
            r.append(lodldc(i))
        else:
            op = OP_MAP[i.value]
            r.append(TokenUnit(op))
    return r


def lodldc(x):
    if x.unit_type == TOKEN_TYPE_ENUM.VAR:
        return TokenUnit("LOD", VARS.index(x[1]))
    elif x.unit_type == TOKEN_TYPE_ENUM.NUMBER:
        return TokenUnit("LDC", x.value)


def egl(x):
    return TokenUnit(REL_MAP[x])


def relation(syntax):
    r = []
    r += polish(syntax[1][1])
    r += polish(syntax[1][2])
    r.append(egl(syntax[1][0]))
    return r
