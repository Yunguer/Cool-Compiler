from sintatico import tree

Operandos = {
    '+' : 'add',
    '-' : 'sub',
    '/' : 'div',
    '*' : 'mul'
}

Comparadores = {
    '<=' : 'le',
    '<' : 'lt',
    '=' : 'eq'
}

def geraFeatureRetornoParametro(t):
    metodo = '@' + t[1] + '( ' 
    for formal in t[2]:
        metodo += formal[1] + ' : ' + formal[2] + ', '
    metodo = metodo [:-2] + ')'
    return metodo

def geraFeatureRetorno(t):
    metodo = '@' + t[1] + '()'
    return metodo

def geraCallMetodo(t):
    if t[1] == 'out_int':
        return 'print ' + str(t[2][0][1]) + ';'
    callmetodo = 'call @' + t[1] + ' '
    for id in t[2]:
        callmetodo+= str(id[1]) + ' '
    callmetodo = callmetodo [:-1] + ';'
    return callmetodo

def geraFeatureAnonima(t, listaIds):
    if t[3][0] != 'op' and t[3][0] != 'comp':
        valor = getId(t[3][1], listaIds)[1] if getId(t[3][1], listaIds) != None else t[3][1]
        id = str(t[1]) + ' : ' + str(t[2]) + ' = ' + 'const ' + str(valor) + ';'
        return id
    else:
        return str(t[1]) + ' : ' + str(t[2]) + ' = '

def geraOp(t):
    return Operandos[t[1]] + ' ' + str(t[2][1]) + ' ' + str(t[3][1]) + ';'

def geraComp(t):
    return Comparadores[t[1]] + ' ' + str(t[2][1]) + ' ' + str(t[3][1]) + ';'

def getId(nome, lista):
    for item in lista:
        if item[0] == nome:
            return item
    return None

'''@out_int_IO(this: int) {
  print this;
}
@main {
  v0: int = const 10;
  call @out_int_IO v0;
}'''
