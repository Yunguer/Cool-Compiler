import sys

from lexico import tokens, lexer
from ply.yacc import yacc
import os

VERBOSE = 1

def p_program(p):
    '''program : class_list
                | empty'''
    #p[0] = p[1]
    pass

def p_class_list(p):
    '''class_list : class_list class PONTOVIRGULA
                | class PONTOVIRGULA'''
    pass

def p_class(p):
    '''class : CLASS ID INHERITS ID ABRECHAVES feature_list FECHACHAVES
            | CLASS ID ABRECHAVES feature_list FECHACHAVES
            '''
    pass

def p_feature_list(p):
    '''feature_list : feature_list feature PONTOVIRGULA
                    | empty'''
    pass

def p_feature(p):
    '''feature : ID ABREPARENTESES formal_list FECHAPARENTESES DOISPONTOS ID ABRECHAVES expr FECHACHAVES
            | ID ABREPARENTESES FECHAPARENTESES DOISPONTOS ID ABRECHAVES expr FECHACHAVES
            | ID DOISPONTOS ID SETA expr
            | ID DOISPONTOS ID
            | empty
            '''
    pass

def p_formal_list(p):
    '''formal_list : formal_list VIRGULA formal
                    | empty
                    | formal
                    '''
    pass

def p_formal(p):
    'formal : ID DOISPONTOS ID'
    #p[0] = p[1] : p[3]
    pass

def p_expr_1(p):
    '''expr : ID SETA expr
            | NEW ID
            | ISVOID expr
            | expr MAIS expr
            | expr MENOS expr
            | expr MULTIPLICA expr
            | expr DIVISAO expr
            | COMPLEMENTO expr
            | expr MENOR expr
            | expr MENORIGUAL expr
            | expr IGUAL expr
            | NOT expr
            | ABREPARENTESES expr FECHAPARENTESES
            | ID
            | NUMERO
            | STRING
            | TRUE
            | FALSE
            '''
    pass

def p_expr_arroba(p):
    '''expr : expr ARROBA ID PONTO ID ABREPARENTESES expr_list FECHAPARENTESES
            | expr PONTO ID ABREPARENTESES expr_list FECHAPARENTESES'''
    pass

def p_id_expr(p):
    'expr : ID ABREPARENTESES expr_list FECHAPARENTESES'
    pass

def p_expr_list(p):
    '''expr_list : expr_list VIRGULA expr
                | expr
                | empty
            '''
    pass

def p_if_expr(p):
    'expr : IF expr THEN expr ELSE expr FI'
    pass

def p_while_expr(p):
    'expr : WHILE expr LOOP expr POOL'
    pass

def p_expr_2(p):
    'expr : ABRECHAVES expr_list_mais FECHACHAVES'
    pass

def p_expr_list_mais(p):
    '''expr_list_mais : expr_list_mais expr PONTOVIRGULA
            | expr PONTOVIRGULA
            '''
    pass

def p_let_expr(p):
    '''expr : LET ID DOISPONTOS ID SETA expr id_type_list IN expr
            | LET ID DOISPONTOS ID id_type_list IN expr
            '''
    pass

def p_id_type_list(p):
    '''id_type_list : id_type_list id_type
                    | id_type
                    '''
    pass

def p_id_type(p):
    '''id_type : VIRGULA ID DOISPONTOS ID SETA expr
                    | VIRGULA ID DOISPONTOS ID
                    | empty
                    '''
    pass

def p_case_expr(p):
    'expr : CASE expr OF id_type_list_2 ESAC'
    pass

def p_id_type_list_2(p):
    '''id_type_list_2 : id_type_list_2 id_type_2
                    | id_type_2'''
    pass

def p_id_type_2(p):
    'id_type_2 : ID DOISPONTOS ID IGUALMAIOR expr PONTOVIRGULA'
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
aux = parser.parse(data, lexer=lexer)
print(aux)
