import sys

from lexico import tokens, lexer
from ply.yacc import yacc
import os

VERBOSE = 1

def p_program(p):
    '''program : class_list
                | empty'''
    p[0] = [p[1]]
    pass

def p_class_list(p):
    '''class_list : class_list class PONTOVIRGULA
                | class PONTOVIRGULA'''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]

    pass

def p_class(p):
    '''class : CLASS ID INHERITS ID ABRECHAVES feature_list FECHACHAVES
            | CLASS ID ABRECHAVES feature_list FECHACHAVES
            '''
    if len(p) == 8:
        p[0] = ('classInh', p[2], p[4], p[6])
    else:
        p[0] = ('class', p[2], p[4])
    pass

def p_feature_list(p):
    '''feature_list : feature_list feature PONTOVIRGULA
                    | empty'''
    if len(p) == 4:
        p[0] = [p[1]]
        p[0].append(p[2])
    elif len(p) == 2:
        p[0] = None

    pass

def p_feature(p):
    '''feature : ID ABREPARENTESES formal_list FECHAPARENTESES DOISPONTOS ID ABRECHAVES expr FECHACHAVES
            | ID ABREPARENTESES FECHAPARENTESES DOISPONTOS ID ABRECHAVES expr FECHACHAVES
            | ID DOISPONTOS ID SETA expr
            | ID DOISPONTOS ID
            | empty
            '''
    if len(p) == 10:
        p[0] = ('featureRetornoParametro',p[1],p[3],p[6],p[8])
    elif len(p) == 9:
        p[0] = ('featureRetorno',p[1],p[5],p[7])
    elif len(p) == 6:
        p[0] = ('featureAnonima',p[1],p[3],p[5])
    elif len(p) == 4:
        p[0] = ('featureDeclaration',p[1],p[3])
    elif len(p) == 2:
        p[0] = None
    pass

def p_formal_list(p):
    '''formal_list : formal_list VIRGULA formal
                    | formal
                    | empty
                    '''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = None
    pass

def p_formal(p):
    'formal : ID DOISPONTOS ID'
    p[0] = ('formal', p[1], p[3])
    pass

def p_expr_new(p):
    'expr : NEW ID'        
    p[0] = ('exprNew', p[1],p[2])
    pass

def p_expr_void(p):
    'expr : ISVOID expr'        
    p[0] = ('exprVoid', p[1],p[2])
    pass

def p_expr_not(p):
    '''expr : NOT expr
            | COMPLEMENTO expr 
            '''
    p[0] = ('exprNot', p[1] ,p[2])
    pass

def p_expr_2(p):
    '''expr : STRING
            | TRUE
            | FALSE
            '''
    p[0] = ('exprValores', p[1])
    pass

def p_expr_num(p):
    'expr : NUMERO'
    p[0] = ('exprValores', tryParseInt(p[1]))
    pass

def p_expr_id(p):
    'expr : ID'
    p[0] = ('exprID', p[1])
    pass

def p_expr_3(p):
    '''expr : expr MAIS expr
            | expr MENOS expr
            | expr MULTIPLICA expr
            | expr DIVISAO expr
            '''
    p[0] = ('op', p[2], p[1], p[3])
    pass

def p_expr_comp(p):
    '''expr : expr MENOR expr
            | expr MENORIGUAL expr
            | expr IGUAL expr
            '''
    p[0] = ('comp', p[2], p[1], p[3])
    pass

def p_expr_4(p):
    'expr :  ID SETA expr'
    p[0] = ('exprSeta', p[1], p[2], p[3])

    pass

def p_expr_5(p):
    'expr :  ABREPARENTESES expr FECHAPARENTESES'
    p[0] = ('exprEntreParenteses', p[2])
    pass

def p_id_expr(p):
    'expr : ID ABREPARENTESES expr_list FECHAPARENTESES'
    p[0] = ('exprCallMetodo', p[1], p[3])
    pass

def p_expr_arroba(p):
    '''expr : expr ARROBA ID PONTO expr
            | expr PONTO expr'''
    if len(p) == 9:
        p[0] = ('exprArroba', p[1], p[3], p[5])
    else:
        p[0] = ('exprSemArroba', p[1], p[3])
    pass


def p_expr_list(p):
    '''expr_list : expr_list VIRGULA expr
                | expr
                | empty
            '''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = None
    pass

def p_if_expr(p):
    'expr : IF expr THEN expr ELSE expr FI'
    p[0] = ('exprIf', p[2], p[4], p[6])
    pass

def p_while_expr(p):
    'expr : WHILE expr LOOP expr POOL'
    p[0] = ('exprWhile', p[2], p[4])
    pass

def p_expr_6(p):
    'expr : ABRECHAVES expr_list_mais FECHACHAVES'
    p[0] = ('exprEntreChaves', p[2])
    pass

def p_expr_list_mais(p):
    '''expr_list_mais : expr_list_mais expr PONTOVIRGULA
            | expr PONTOVIRGULA
            '''
    if len(p) > 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass

def p_let_expr(p):
    '''expr : LET ID DOISPONTOS ID SETA expr id_type_list IN expr
            | LET ID DOISPONTOS ID id_type_list IN expr
            '''
    if len(p) > 9:
        p[0] = ('exprLetSeta', p[2], p[4], p[6], p[7], p[9])
    else:
        p[0] = ('exprLet', p[2], p[4], p[5], p[7])
    pass

def p_id_type_list(p):
    '''id_type_list : id_type_list id_type
                    | id_type
                    '''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass

def p_id_type(p):
    '''id_type : VIRGULA ID DOISPONTOS ID SETA expr
                    | VIRGULA ID DOISPONTOS ID
                    | empty
                    '''
    if len(p) == 7:
        p[0] = ('exprType', p[2], p[4], p[6])
    elif len(p) == 5:
        p[0] = ('exprType', p[2], p[4])
    else:
        p[0] = None
    pass

def p_case_expr(p):
    'expr : CASE expr OF id_type_list_2 ESAC'
    p[0] = ('exprCase', p[2], p[4])
    pass

def p_id_type_list_2(p):
    '''id_type_list_2 : id_type_list_2 id_type_2
                    | id_type_2'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass

def p_id_type_2(p):
    'id_type_2 : ID DOISPONTOS ID IGUALMAIOR expr PONTOVIRGULA'
    p[0] = ('idType', p[1], p[3], p[5])
    pass

def p_empty(p):
    'empty : '
    pass

def p_error(p):
    if VERBOSE:
        if p is not None:
            print ("Erro no Sintatico linha: " + str(lexer.lineno)+"  Erro de Contexto: " + str(p.value))
        else:
            print ("Erro no Lexico linha: " + str(lexer.lineno))
    else:
        raise Exception('Syntax', 'error')

def tryParseInt(s):
    try:
        return int(s)
    except:
        return s

parser = yacc()

#Caso prefira usar o nome do arquivo em vez do argv so descomentar a parte a baixo e comentar a outra parte

'''arq = "complex.cl"
f = open(arq,'r')
data = f.read()
#"print (data)
#parser.parse(data, tracking=True)
aux = parser.parse(data, lexer=lexer)
print(aux)
'''

if (len(sys.argv) > 1):
    arq = sys.argv[1]
else:
    arq = 'helloworld.cl'

f = open(arq,'r')
data = f.read()
tree = parser.parse(data, lexer=lexer)
#print(tree)