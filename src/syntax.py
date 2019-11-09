from src.consts import *
from random import randint

WHILE_STACK = []


def syntax_analysis(tokens):
    sentence = to_sentence(tokens)
    return statement(sentence)


'''
flag:
- 0: start
- 1: wait end
- 2: end(;)
'''


def to_sentence(tokens):
    if tokens[-1].unit_type != TOKEN_TYPE_ENUM.SEP:
        raise SyntaxError('[SYN] Source wrong EOF')
    r = []
    flag = 0
    sentence = []
    for i in tokens:
        if i.unit_type == TOKEN_TYPE_ENUM.SEP:
            if flag == 1:
                if len(sentence) > 0:
                    r.append(sentence)
                sentence = []
                flag = 2
            else:
                raise SyntaxError('[SYN] Wrong separator@{}'.format(sentence))
        else:
            sentence.append(i)
            flag = 1
    return r


def statement(states):
    r = []
    for j in states:
        if j[0].value == KEYWORDS_ENUM.WHILE:
            while_state = while_statement(j)
            goto_id = randint(10000, 99999)
            WHILE_STACK.append(goto_id)
            r.append([STATEMENT_TYPE_ENUM.GOTO_REL, goto_id])
            r.append([STATEMENT_TYPE_ENUM.RELATION, relation(while_state[0])])
            r.append([STATEMENT_TYPE_ENUM.GOTO_CJP, goto_id])
            r += statement([while_state[1]])
        elif j[-1].value == KEYWORDS_ENUM.ENDWHILE:
            if len(j) > 1:
                r += statement([j[:-1]])
            r.append([STATEMENT_TYPE_ENUM.GOTO_UJP, WHILE_STACK.pop()])
        elif j[0].value in [KEYWORDS_ENUM.READ, KEYWORDS_ENUM.WRITE]:
            if len(j) == 4 and j[1].value == '(' and j[3].value == ')' and j[2].unit_type == TOKEN_TYPE_ENUM.VAR:
                r.append(TokenUnit(j[0].value, j[2].value))
            else:
                raise SyntaxError('[SYN] Wrong syntax for READ/WRIT@{}'.format(j))
        elif j[0].unit_type == TOKEN_TYPE_ENUM.VAR and j[1].value == ':' and j[2].value == '=':
            r.append([STATEMENT_TYPE_ENUM.ASSIGN, j[0].value, simple_expression(j[3:])])
    return r


def while_statement(while_s):
    relate = []
    w = ''
    for i, w in enumerate(while_s[1:]):
        if w.value == KEYWORDS_ENUM.DO:
            return [relate, while_s[i + 2:]]
        else:
            relate.append(w)
    raise SyntaxError('[SYN] Wrong syntax for WHILE@{}'.format(w))


def relation(tokens):
    for i, w in enumerate(tokens):
        if w.value in ">=<":
            return [w.value, simple_expression(tokens[:i]), simple_expression(tokens[i + 1:])]
    raise SyntaxError('[SYN] Wrong syntax for comparison@{}'.format(w))


def simple_expression(tokens):
    r = []
    stack = []
    for i in tokens:
        if i.unit_type == TOKEN_TYPE_ENUM.NUMBER or i.unit_type == TOKEN_TYPE_ENUM.VAR:
            r += [i]
        elif i.unit_type == TOKEN_TYPE_ENUM.OP:
            if i.value == '(':
                stack.append(i)
            elif i.value == ')':
                while stack[-1].value != '(':
                    r.append(stack.pop())
                stack.pop()
            elif i.value in "+-":
                while len(stack) > 0 and stack[-1].value != '(':
                    r.append(stack.pop())
                stack.append(i)
            elif i.value in "*/":
                while len(stack) > 0 and stack[-1].value not in '(+-':
                    r.append(stack.pop())
                stack.append(i)
        else:
            raise SyntaxError('[SYN] Wrong syntax for expression@{}'.format(i))
    while len(stack) > 0:
        r.append(stack.pop())
    return r
