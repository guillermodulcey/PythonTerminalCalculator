
# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

import math as m

tokens = (
    'NAME','NUMBER','DECIMAL',
    'PLUS','MINUS','TIMES','DIVIDE','EXP','EQUALS',
    'LPAREN','RPAREN','DOT','COMMA',
    'LOG','LN','SQRT','MOD',
    'COS','SEN','TAN','SEC','CSC','COT',
    'ACOS','ASEN','ATAN',
    'COSH','SENH','TANH','SECH','CSCH','COTH',
    'ACOSH','ASENH','ATANH'
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EXP     = r'\^'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_DOT     = r'\.'
t_COMMA   = r','
t_LOG     = r'log|LOG'
t_LN      = r'ln|LN'
t_SQRT    = r'sqrt|SQRT'
t_MOD     = r'%'
##Reserved words######
##Trigonometry

t_COS     = r'cos|COS'
t_SEN     = r'sen|SEN'
t_TAN     = r'tan|TAN'
t_SEC     = r'sec|SEC'
t_CSC     = r'csc|CSC'
t_COT     = r'cot|COT'
t_ACOS     = r'acos|ACOS'
t_ASEN     = r'asen|ASEN'
t_ATAN     = r'atan|ATAN'

##Hyperbólicas
t_COSH    = r'cosh|COSH'
t_SENH    = r'senh|SENH'
t_TANH    = r'tanh|TANH'
t_SECH    = r'sech|SECH'
t_CSCH    = r'csch|CSCH'
t_COTH    = r'coth|COTH'
t_ACOSH    = r'acosh|ACOSH'
t_ASENH    = r'asenh|ASENH'
t_ATANH    = r'atanh|ATANH'

############################

ln = 'ln|LN'
log = 'log|LOG'
sqrt = 'sqrt|SQRT'
mod = '%'

coseno = 'cos|COS'
seno = 'sen|SEN'
tangente = 'tan|TAN'
secante = 'sec|SEC'
cosecante = 'csc|CSC'
cotangente = 'cot|COT'
coseno_hyper = 'cosh|COSH'
seno_hyper = 'senh|SENH'
tangente_hyper = 'tanh|TANH'
secante_hyper = 'sech|SECH'
cosecante_hyper = 'csch|CSCH'
cotangente_hyper = 'coth|COTH'

arccoseno = 'acos|ACOS'
arcseno = 'asen|ASEN'
arctangente = 'atan|ATAN'

arccoseno_hyper = 'acosh|ACOSH'
arcseno_hyper = 'asenh|ASENH'
arctangente_hyper = 'atanh|ATANH'


palabras_trigonometria = coseno+'|'+seno+'|'+tangente+'|'+secante+'|'+cosecante+'|'+cotangente
palabras_hyperbolicas = coseno_hyper+'|'+seno_hyper+'|'+tangente_hyper+'|'+secante_hyper+'|'+cosecante_hyper+'|'+cotangente_hyper

palabras_inv_trigonometria = arccoseno+'|'+arcseno+'|'+arctangente
palabras_inv_hyperbolicas = arccoseno_hyper+'|'+arcseno_hyper+'|'+arctangente_hyper
palabras_funciones = log+'|'+ln+'|'+sqrt+'|'+mod

palabras_reservadas = palabras_trigonometria+'|'+palabras_hyperbolicas+'|'+palabras_inv_trigonometria+'|'+palabras_inv_hyperbolicas+'|'+palabras_funciones

caracteres_aceptados = '[a-zA-Z_][a-zA-Z0-9_]'
###########################
t_NAME    = r'((?!('+palabras_reservadas+'))('+caracteres_aceptados+'*))|(('+palabras_reservadas+')'+caracteres_aceptados+'+)'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MOD'),
    ('left','EXP','SQRT'),
    ('left','COS','SEN','TAN','SEC','CSC','COT','COSH','SENH','TANH','SECH','CSCH','COTH','ACOS','ASEN','ATAN','ACOSH','ASENH','ATANH'),
    ('left','LOG','LN'),
    ('left','COMMA'),
    ('left','DOT'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_statement_decimal(t):
    'expression : expression DOT expression'
    result = ""+str(t[1])+"."+str(t[3])
    t[0] = float(result)

def p_statement_logarithm(t):
    'expression : LOG expression COMMA expression'
    t[0] = m.log(t[2],t[4])

def p_statement_natural_logarithm(t):
    'expression : LN expression'
    t[0] = m.log(t[2])

def p_statement_square_root(t):
    'expression : SQRT expression'
    t[0] = m.sqrt(t[2])

def p_statement_module(t):
    'expression : expression MOD expression'
    t[0] = t[1] % t[3]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EXP expression
                  '''
    if t[2] == '+'  : t[0] = t[1] +  t[3]
    elif t[2] == '-': t[0] = t[1] -  t[3]
    elif t[2] == '*': t[0] = t[1] *  t[3]
    elif t[2] == '/': t[0] = t[1] /  t[3]
    elif t[2] == '^': t[0] = t[1] ** t[3]

##Trigonometry####################################################
def p_expression_trig(t):
    '''expression : COS expression
                  | SEN expression
                  | TAN expression
                  | SEC expression
                  | CSC expression
                  | COT expression
                  | COSH expression
                  | SENH expression
                  | TANH expression
                  | SECH expression
                  | CSCH expression
                  | COTH expression
                  | ACOS expression
                  | ASEN expression
                  | ATAN expression
                  | ACOSH expression
                  | ASENH expression
                  | ATANH expression
                  '''
    if t[1] == 'cos' or t[1] == 'COS' : t[0] = m.cos(t[2])
    elif t[1] == 'sen' or t[1] == 'SEN' : t[0] = m.sin(t[2])
    elif t[1] == 'tan' or t[1] == 'TAN' : t[0] = m.tan(t[2])
    elif t[1] == 'sec' or t[1] == 'SEC' : t[0] = 1/m.cos(t[2])
    elif t[1] == 'csc' or t[1] == 'CSC' : t[0] = 1/m.sin(t[2])
    elif t[1] == 'cot' or t[1] == 'COT' : t[0] = 1/m.tan(t[2])
    ##Hiperbólicas
    elif t[1] == 'cosh' or t[1] == 'COSH' : t[0] = m.cosh(t[2])
    elif t[1] == 'senh' or t[1] == 'SENH' : t[0] = m.sinh(t[2])
    elif t[1] == 'tanh' or t[1] == 'TANH' : t[0] = m.tanh(t[2])
    elif t[1] == 'sech' or t[1] == 'SECH' : t[0] = 1/m.cosh(t[2])
    elif t[1] == 'csch' or t[1] == 'CSCH' : t[0] = 1/m.sinh(t[2])
    elif t[1] == 'coth' or t[1] == 'COTH' : t[0] = 1/m.tanh(t[2])
    ##Inversas
    elif t[1] == 'acos' or t[1] == 'ACOS' : t[0] = m.acos(t[2])
    elif t[1] == 'asen' or t[1] == 'ASEN' : t[0] = m.asin(t[2])
    elif t[1] == 'atan' or t[1] == 'ATAN' : t[0] = m.atan(t[2])
    ##Inversas hiperbolicas
    elif t[1] == 'acosh' or t[1] == 'ACOSH': 
        try:
            t[0] = m.acosh(t[2])
        except:
            print("Math error: acosh(%s)" %t[2])
            t[0] = 0
    elif t[1] == 'asenh' or t[1] == 'ASENH': 
        try:
            t[0] = m.asinh(t[2])
        except:
            print("Math error: asenh(%s)" %t[2])
            t[0] = 0
    elif t[1] == 'atanh' or t[1] == 'ATANH': 
        try:
            t[0] = m.atanh(t[2])
        except:
            print("Math error: atanh(%s)" %t[2])
            t[0] = 0

##################################################################

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_decimal(t):
    'expression : DECIMAL'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)
