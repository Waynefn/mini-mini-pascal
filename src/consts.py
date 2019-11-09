ROOT_PATH = '..\\etc\\'


class TokenUnit:
    def __init__(self, unit_type, value=''):
        self.unit_type = unit_type
        self.value = value
        self.flag = False
    def __repr__(self):
        return "{}:{}".format(self.unit_type, self.value)
    def __getitem__(self, i):
        if i ==0:
            return self.unit_type
        elif i==1:
            return self.value
        else:
            raise ValueError('Wrong TokenUnit index: {}'.format(i))


class CompileStage:
    def __init__(self):
        self.SOURCE = '.PAS'
        self.TOKENS = '.TKS'
        self.GRAMMAR = '.GRM'
        self.ASSEMBLE = '.OBJ'


class KeywordsType:
    def __init__(self):
        self.READ = 'READ'
        self.WRITE = 'WRITE'
        self.WHILE = 'WHILE'
        self.DO = 'DO'
        self.ENDWHILE = 'ENDWHILE'


class TokenType:
    def __init__(self):
        self.NUMBER = 'NUMBER'
        self.KEYWORD = 'KEYWORD'
        self.VAR = 'VAR'
        self.OP = 'OP'
        self.SEP = 'SEP'


class StatementType:
    def __init__(self):
        self.READ = KEYWORDS_ENUM.READ
        self.WRITE = KEYWORDS_ENUM.WRITE
        self.ASSIGN = 'ASSIGN'
        self.GOTO_REL = "GOTO_REL"
        self.GOTO_CJP = 'GOTO_CJP'
        self.GOTO_UJP = 'GOTO_UJP'
        self.RELATION = 'RELATION'


COMPILE_ENUM = CompileStage()
KEYWORDS_ENUM = KeywordsType()
TOKEN_TYPE_ENUM = TokenType()
STATEMENT_TYPE_ENUM = StatementType()

KEYWORDS = list(KEYWORDS_ENUM.__dict__.keys())
TOKENS = list(TOKEN_TYPE_ENUM.__dict__.keys())
STATEMENTS = list(STATEMENT_TYPE_ENUM.__dict__.keys())
OPS = ['+', '-', '*', '/', '(', ')', ':=', ':', '=', '>', '<']
VARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def generate_enum_map(l, e):
    m = {}
    for i in l:
        m[i] = e.__getattribute__(i)
    return m


STATEMENT_MAP = generate_enum_map(STATEMENTS, STATEMENT_TYPE_ENUM)
KEYWORD_MAP = generate_enum_map(KEYWORDS, KEYWORDS_ENUM)
TOKEN_MAP = generate_enum_map(TOKENS, TOKEN_TYPE_ENUM)
OP_MAP = {'+': 'ADD', '-': 'SUB', '*': 'MLT', '/': 'DIV'}
REL_MAP = {'>': 'GRT', '=': 'EQL', '<': 'LES'}
