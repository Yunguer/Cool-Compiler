from sintatico import tree
import copy

listaTipos = [('Object', None, [('abort',[],'Object'),('type_name',[],'String'),('copy',[],'SELF_TYPE')], [('self', 'Object')]),
              ('SELF_TYPE',None,[],[]),
              ('IO', 'Object', [('out_string',[('x','String')],'SELF_TYPE'),('out_int',[('x','Int')],'SELF_TYPE'),('in_string',[],'String'),('in_int',[],'Int')], []),
              ('Int', 'IO', [], []),
              ('String', 'IO', [('length',[],'Int'),('concat',[('s','String')],'String'),('substr',[('i','Int'), ('l','Int')],'String')], []),
              ('Bool', 'IO', [], [])
            ]
listaMetodos = []
listaIds = []

escopo = 'program'


for tipo in listaTipos:
    for metodo in tipo[2]:
        listaMetodos.append(metodo)

for tipo in listaTipos:
    for id in tipo[3]:
        listaIds.append(id)

def percorreArvore(t):
    if type(t) == list or type(t) == tuple:
        for filho in t:
            percorreArvore(filho)
        print(t[0])
    
#percorreArvore(tree)
#print(tree)

def chamaFuncao(t, listaIds, listaMetodos, listaTipos):
    
    if t == None:
        return

    newListaTipos = []
    newListaIds = []
    newListaMetodos = []
    newListaTipos = listaTipos
    if isNewEscopoClasse(t[0]):
        global escopo
        escopo = t[1]
        newListaMetodos = copy.deepcopy(listaMetodos)
        newListaIds = listaIds
    elif isNewEscopoMetodo(t[0]) or isNewEscopoLet(t[0]):
        newListaIds = copy.deepcopy(listaIds)
        newListaMetodos = listaMetodos
        
    else:
        newListaTipos = listaTipos
        newListaIds = listaIds
        newListaMetodos = listaMetodos
        
    
    
    if t[0] == 'idType': 
        manipulaIdType(t, newListaIds, newListaTipos)
    elif t[0] == 'exprCase': #To do
        manipulaExprCase(t)
    elif t[0] == 'exprID':
        manipulaExprId(t, newListaIds)
    elif t[0] == 'exprType': 
        manipulaExprType(t) #To do
    elif t[0] == 'exprLetSeta': 
        manipulaExprLetSeta(t, newListaIds, newListaTipos)
        chamaFuncao(t[5], newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'exprLet': 
        manipulaExprLet(t, newListaIds, newListaTipos)
        chamaFuncao(t[4], newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'exprEntreChaves':
        chamaFuncao(t[1], newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'exprWhile': 
        manipulaExprWhile(t, newListaIds)
        chamaFuncao(t[3], newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'exprIf':
        manipulaExprIf(t, newListaIds)
        chamaFuncao(t[2], newListaIds, newListaMetodos, newListaTipos)
        chamaFuncao(t[3], newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'exprCallMetodo':
        manipulaExprCallMetodo(t, newListaMetodos, newListaIds)
    elif t[0] == 'exprArroba':
        nome = None
        nomeMetodo = None
        if t[1][0] == 'exprCallMetodo':
            nome = getMetodo(t[1][1], newListaMetodos)[2]
            nomeMetodo = t[1][1]
        else:
            aux = getId(t[1][1], newListaIds)
            nomeMetodo = t[2][1]
            if aux != None:
                nome = aux[1]
        if nome != None:
            tipo = getType(nome, newListaTipos)
            if nome == 'SELF_TYPE':
                configSelfType(newListaIds, newListaMetodos, newListaTipos) 
            if not isInListMetodo(t[2][1], tipo[2]):
                raise SyntaxError("erro de chamada: metodo %s não pertence ao tipo %s" % nomeMetodo, nome)
        chamaFuncao(t[1], newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'exprSemArroba':
        nome = None
        nomeMetodo = None
        if t[1][0] == 'exprCallMetodo':
            nome = getMetodo(t[1][1], newListaMetodos)[2]
            nomeMetodo = t[1][1]
        else:
            aux = getId(t[1][1], newListaIds)
            nomeMetodo = t[2][1]
            if aux != None:
                nome = aux[1]
        if nome != None:
            tipo = getType(nome, newListaTipos)
            if nome == 'SELF_TYPE':
                configSelfType(newListaIds, newListaMetodos, newListaTipos)
            if not isInListMetodo(nomeMetodo, tipo[2]):
                raise SyntaxError("erro de chamada: metodo %s não pertence ao tipo %s" % nomeMetodo, nome) 
        chamaFuncao(t[1], newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'exprEntreParenteses':
        chamaFuncao(t[1], newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'exprSeta':
        manipulaExprSeta(t, newListaIds)
    elif t[0] == 'op':
        manipulaOp(t, newListaIds)
    elif t[0] == 'comp':
        manipulaComp(t, newListaIds)
    elif t[0] == 'exprNew': 
        manipulaExprNew(t, newListaTipos)
    elif t[0] == 'exprVoid':
        manipulaExprVoid(t, newListaIds)
    elif t[0] == 'exprNot':
        manipulaExprNot(t, newListaIds)
    elif t[0] == 'formal':
        manipulaFormal(t, newListaIds, newListaTipos)
    elif t[0] == 'featureRetornoParametro':
        manipulaFeatureRetornoParametro(t, newListaIds, newListaMetodos, newListaTipos)
        for formal in t[4]:
            chamaFuncao(formal, newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'featureRetorno':
        manipulaFeatureRetorno(t, newListaMetodos, newListaTipos)
        chamaFuncao(t[3], newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'featureAnonima':
        manipulafeatureAnonima(t, newListaIds, newListaTipos)
        for formal in t[2]:
            chamaFuncao(formal, newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'featureDeclaration':
        manipulaFeatureDeclaration(t, newListaIds, newListaTipos)
    elif t[0] == 'class':
        for formal in t[2]:
            chamaFuncao(formal, newListaIds, newListaMetodos, newListaTipos)
    elif t[0] == 'classInh':
        manipulaClasseInh(t, newListaTipos)
        for formal in t[3]:
            if type(formal) == list:
                for i in formal:
                    chamaFuncao(i, newListaIds, newListaMetodos, newListaTipos)
            else:
                chamaFuncao(formal, newListaIds, newListaMetodos, newListaTipos)
    else:
        if type(t) == list:
                for i in t:
                    chamaFuncao(i, newListaIds, newListaMetodos, newListaTipos)
            

def manipulaIdType(t, listaIds, listaTipos):
    if len(t) == 4:
        aux = ('featureAnonima', t[1], t[2], t[3])
        manipulafeatureAnonima(aux, listaIds, listaTipos)
    elif len(t) == 3:
        aux = ('featureDeclaration', t[1], t[2])
        manipulaFeatureDeclaration(aux, listaIds, listaTipos)
    pass

def manipulaExprCase(t):
    pass

def manipulaExprType(t):
    pass

def manipulaExprId(t, listaIds):
    if not isInListId(t[1], listaIds):
        raise SyntaxError("erro de declaração: %s não foi declarado" % t[1])

def manipulaExprLetSeta(t, listaIds, listaTipos):
    aux = ('featureAnonima', t[1], t[2], t[3])
    manipulafeatureAnonima(aux, listaIds, listaTipos)
    for fanonima in t[4]:
        if fanonima != None:
            manipulaIdType(fanonima, listaIds, listaTipos)

def manipulaExprLet(t, listaIds, listaTipos):
    aux = ('featureDeclaration', t[1], t[2])
    manipulaFeatureDeclaration(aux, listaIds, listaTipos)
    for fanonima in t[3]:
        if fanonima != None:
            manipulaIdType(fanonima, listaIds, listaTipos)


def manipulaExprWhile(t, listaIds):
    if t[1][0] == 'comp':
        manipulaComp(t[1], listaIds)
        return
    if t[1][0] == 'exprNot':
        manipulaExprNot(t[1], listaIds)
        return
    raise SyntaxError("erro de declaração: expressão %s não é booleano" % t[1])
    
def manipulaExprIf(t, listaIds):
    if t[1][0] == 'comp':
        manipulaComp(t[1], listaIds)
        return
    if t[1][0] == 'exprNot':
        manipulaExprNot(t[1], listaIds)
        return
    raise SyntaxError("erro de declaração: expressão %s não é booleano" % t[1])

def manipulaExprCallMetodo(t, listaMetodos, listaIds):
    if not isInListMetodo(t[1], listaMetodos):
        raise SyntaxError("erro de chamada: metodo %s não declarado" % t[1])
    verificaParametroCall(t[2], getMetodo(t[1], listaMetodos), listaIds)

def manipulaExprEntreParenteses(t):
    pass

def manipulaExprSeta(t, listaIds):

    if getId(t[1], listaIds) == None:
        raise SyntaxError("erro de atribuição: %s não foi declarada" % t[1])
    elif t[3][0] == 'op':
        manipulaOp(t[3], listaIds)
    elif t[3][0] == 'exprID':  
        id = getId(t[3][1], listaIds)
        if id == None:
            raise SyntaxError("erro de atribuição: %s não foi declarada" % t[3][1])
    return t[1]

def manipulaOp(t, listaIds):
    id1 = getId(t[2], listaIds)
    id2 = getId(t[3], listaIds)

    if id1 == None:
        tryParseInt(t[2][1], listaIds)
    elif id1[1] != "Int":
        raise SyntaxError("erro de operação: %s deve ser do tipo Int" % id1[0])
    if id2 == None:
        tryParseInt(t[3][1], listaIds)
    elif id2[1] != "Int":
        raise SyntaxError("erro de operação: %s deve ser do tipo Int" % id2[0])

def manipulaComp(t, listaIds):
    if t[2][0] == 'exprNot':
        id1 = getId(t[2][2][1], listaIds)
    elif t[2][0] == 'op':
        manipulaOp(t[2], listaIds)
        id1 = (0, 'Int') 
    else:
        id1 = getId(t[2][1], listaIds)
    if t[3][0] == 'exprNot':
        id2 = getId(t[3][2][1], listaIds)
    elif t[3][0] == 'op':
        manipulaOp(t[3], listaIds)
        id2 = (0, 'Int')
    else:
        id2 = getId(t[3][1], listaIds)

    if id1 == None:
        if type(tryConvertInt(t[2][1])) != int:
            raise SyntaxError("erro de declaração: %s não foi declarado" % t[2][1])
        id1 = (str(tryConvertInt(t[2][1])),'Int')
    if id2 == None:
        if type(tryConvertInt(t[3][1])) != int:
            raise SyntaxError("erro de declaração: %s não foi declarado" % t[3][1])
        id2 = (str(tryConvertInt(t[3][1])),'Int')    
    if id1[1] != id2[1]:
        raise SyntaxError("erro de comparação: %s %s devem ser do mesmo tipo" % id1[0], id2[0])


def manipulaExprNew(t, listaTipos):
    if not isInListType(t[2], listaTipos):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])

def manipulaExprVoid(t, listaIds):
    if not isInListId(t[2], listaIds):
        raise SyntaxError("erro de declaração: %s não foi declarado" % t[2])

def manipulaExprNot(t, listaIds):
    if t[2][0] == 'comp':
        manipulaComp(t[2], listaIds)
        return
    raise SyntaxError("erro de declaração: expressão %s não é booleano" % t[2])

def manipulaFormal(t, listaIds, listaTipos):
    if isInListId(t[1], listaIds):
        raise SyntaxError("erro de declaração: %s já declarado" % t[1])
    if not isInListType(t[2], listaTipos):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])
    listaIds.append((t[1], t[2]))

def manipulaFeatureRetornoParametro(t, listaIds, listaMetodos, listaTipos):
    if isInListMetodo(t[1], listaMetodos):
        raise SyntaxError("erro de declaração: metodo %s já declarado" % t[1])
    if not isInListType(t[3], listaTipos):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[3])
    verificaParametro(t[2], listaTipos)
    metodo = (t[1], [], t[3])
    tipo = getType(escopo, listaTipos)
    if tipo != None:
        tipo[2].append(metodo)
    for id in t[2]:
        newId = (id[1], id[2])
        listaIds.append(newId)
        metodo[1].append(newId)
    listaMetodos.append(metodo)

def manipulaFeatureRetorno(t, listaMetodos, listaTipos):
    if isInListMetodo(t[1], listaMetodos):
        raise SyntaxError("erro de declaração: metodo %s já declarado" % t[1])
    if not isInListType(t[2], listaTipos):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])
    metodo = (t[1], [], t[2])
    tipo = getType(escopo, listaTipos)
    if tipo != None:
        tipo[2].append(metodo)
    listaMetodos.append(metodo)

def manipulafeatureAnonima(t, listaIds, listaTipos):
    if isInListId(t[1], listaIds):
        raise SyntaxError("erro de declaração: variavel %s já declarada" % t[1])
    if not isInListType(t[2], listaTipos):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])
    if t[2] == 'String':
        if type(t[3][1]) != str:
            raise SyntaxError("erro de declaração: valor incompativel com a variavel %s" % t[1])
    if t[2] == 'Int':
        if type(t[3][1]) != int:
            raise SyntaxError("erro de declaração: valor incompativel com a variavel %s" % t[1])

    listaIds.append((t[1], t[2]))

def manipulaFeatureDeclaration(t, listaIds, listaTipos):
    if isInListId(t[1], listaIds):
        raise SyntaxError("erro de declaração: variavel %s já declarada" % t[1])
    if not isInListType(t[2], listaTipos):
        raise SyntaxError("erro de declaração: tipo %s não foi declarado" % t[2])        
    listaIds.append((t[1], t[2]))

def manipulaClasseInh(t, listaTipos):
    inherits = getType(t[2], listaTipos)
    classe = getType(t[1], listaTipos)
    for metodo in inherits[2]:
        classe[2].append(metodo)
    for id in inherits[3]:  
        classe[3].append(id)    

def isInListType(item, lista):
    for i in lista:
            if item == i[0]:
                return True
    return False


def isInListId(item, lista):
    for i in lista:
        if item == i[0]:
            return True
    return False

def getId(nome, lista):
    for item in lista:
        if item[0] == nome:
            return item
    return None

def tryParseInt(valor, listaIds):
    try:
        valor = int(valor)
    except:
        if isInListId(valor, listaIds):
            tipo = getId(valor, listaIds)[1]
            if tipo == 'Int':
                return
        raise SyntaxError("erro de conversão: %s não é do tipo inteiro" % valor)

def tryConvertInt(s):
    try:
        return int(s)
    except:
        return s

def isInListMetodo(metodo, lista):
    for i in lista:
            if metodo == i[0]:
                return True
    return False

def verificaParametro(parametros, listaTipos):
    idsParametros = []
    for parametro in parametros:
        if not isInListType(parametro[2], listaTipos):
            raise SyntaxError("erro de declaração: tipo %s não foi declarado" % parametro[2])
        if parametro[1] in idsParametros:
            raise SyntaxError("erro de declaração: id %s já utilizado por outro parametro" % parametro[1])
        idsParametros.append(parametro[1])

def verificaParametroCall(parametros, metodo, listaIds):
    if parametros[0] == None:
        del(parametros[0])
    if len(parametros) != len(metodo[1]):
        raise SyntaxError("erro de chamada: metodo %s deve conter %d parametros" % metodo[0], len(metodo[1]))
    for i in range(0,len(parametros)):
        if not isInListId(parametros[i][1], listaIds):
            if metodo[1][i][1] == 'Int':
                tryParseInt(parametros[i][1], listaIds)
            elif metodo[1][i][1] != 'String':   
                raise SyntaxError("erro de chamada: parametro %s de tipo incorreto" % parametros[i][1])
            if parametros[i][0] != 'exprValores':
                raise SyntaxError("erro de chamada: id %s não foi declarado" % parametros[i][1])   
        else:
            parametro = getId(parametros[i][1], listaIds)
            if parametro[1] != metodo[1][i][1]:
                raise SyntaxError("erro de chamada: parametro %s de tipo incorreto" % parametros[i][1])


def getMetodo(nome, listaMetodos):
    for metodo in listaMetodos:
        if nome == metodo[0]:
            return metodo
    return None            

def getType(nome, listaTipos):
    for tipo in listaTipos:
        if nome == tipo[0]:
            return tipo
    return None

def isNewEscopoClasse(s):
    return s == 'classInh' or s == 'class'

def isNewEscopoMetodo(s):
    return s == 'featureRetornoParametro' or s == 'featureRetorno'

def isNewEscopoLet(s):
    return s == 'exprLetSeta' or s == 'exprLet'

def configSelfType(listaIds, listaMetodos, listaTipos):
    selftype = getType('SELF_TYPE', listaTipos)
    selftype[2].clear()
    selftype[3].clear()
    for metodo in listaMetodos:
        selftype[2].append(metodo)
    for id in listaIds:
        selftype[3].append(id)
                


for filho in tree[0]:
    if type(filho) == tuple:
        if isInListType(filho[1], listaTipos):
            raise SyntaxError("erro de declaração: tipo %s já foi declarado" % filho[1])
        if filho[0] == 'class':
            listaTipos.append((filho[1],None,[],[]))
        elif filho[0] == 'classInh':
            listaTipos.append((filho[1],filho[2],[],[]))

for filho in tree[0]:
    chamaFuncao(filho, listaIds, listaMetodos, listaTipos)
    #print(filho)