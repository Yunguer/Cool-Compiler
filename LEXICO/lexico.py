import ply.lex as lex
import os

reserved = {
    'class':'CLASS',
    'else': 'ELSE',
    'false':'FALSE',
    'fi':'FI',
    'if': 'IF',
    'in':'IN',
    'inherits':'INHERITS',
    'isvoid':'ISVOID',
    'let':'LET',
    'loop':'LOOP',
    'pool':'POOL',
    'then':'THEN',
    'while':'WHILE',
    'case':'CASE',
    'esac':'ESAC',
    'new':'NEW',
    'of':'OF',
    'not':'NOT',
    'true':'TRUE'
}

tokens = [
    'ID',
    'COMPLEMENTO',
    'NUMERO',
    'STRING',
    'MAIS',
    'MENOS',
    'MULTIPLICA',
    'DIVISAO',
    'MENOR',
    'MENORIGUAL',
    'IGUAL',
    'SETA',
    'PONTO',
    'VIRGULA',
    'DOISPONTOS',
    'PONTOVIRGULA',
    'ABREPARENTESES',
    'FECHAPARENTESES',
    'ABRECHAVES',
    'FECHACHAVES',
    'ARROBA',
    'IGUALMAIOR'
] + list(reserved.values())

t_COMPLEMENTO = r'\~'
t_MAIS = r'\+'
t_MENOS = r'\-'
t_MULTIPLICA = r'\*'
t_DIVISAO = r'\/'
t_MENOR = r'\<'
t_MENORIGUAL = r'\<\='
t_IGUAL = r'\='
t_SETA = r'\<\-'
t_PONTO = r'\.'
t_VIRGULA =r'\,'
t_DOISPONTOS = r'\:'
t_PONTOVIRGULA = r'\;'
t_ABREPARENTESES = r'\('
t_FECHAPARENTESES = r'\)'
t_ABRECHAVES = r'\{'
t_FECHACHAVES = r'\}'
t_ARROBA = r'\@'
t_IGUALMAIOR = r'\=\>'

def t_STRING(t): #TOKENS DE STRING
    r'\"[^"]*\"'
    return t

def t_ID(t): #TOKENS DE ID
    r'[a-zA-Z_]+([a-zA-Z0-9_]*)'
    t.type = reserved.get(t.value.lower(), 'ID') #CHECAR PARA PALAVRA RESERVADA
    return t

def t_NUMERO(t): #TOKENS DE NUMEROS
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMENTARIO(t): #IGNORAR COMENTARIOS
    r'(\(\*(.|\n)*?\*\))|(--.*)'
    pass

def t_newline(t): #CONTAR AS LINHAS DOS TOKENS
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t): #MENSAGEM DE ERRO PARA TOKENS INVALIDOS
    print("Token invalido'%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = ' \t' #IGNORAR ESPAÇOS E TABULAÇÕES

lexer = lex.lex()

'''

    if (len(sys.argv) > 1):
        arq = sys.argv[1]
    else:
        arq = 'helloworld.cl'

    f = open(arq,'r')
    codigo = f.read()'''