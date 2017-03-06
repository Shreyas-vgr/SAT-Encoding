input = open("Test_Cases/input3.txt",'r')
output = open("Test_Cases/output.txt",'w')

friends = []
enemies = []
list_clauses = []
symbols = set()
global guests
global tables


def Answer(result):
    list_of_strings = []
    for key,value in sorted(result.items()):
        string = ""
        if value == True:
            string += str(key[1]) + " " +str(key[2:]) + "\n"
            list_of_strings.append(string)
    list_of_strings[-1]  = list_of_strings[-1][:-1]
    output.writelines(list_of_strings)


def Cond1():
    for i in xrange(1,guests+1):
        clause = []
        alt_clause = []
        for j in xrange(1,tables+1):
            clause.append("~X"+str(i)+str(j))
            alt_clause.append("X"+str(i)+str(j))
            #symbols.add("~X"+str(i)+str(j))
            symbols.add("X"+str(i)+str(j))
        list_clauses.append(alt_clause)
        if tables > 1:
            list_clauses.append(clause)

def Cond2():
    for f in friends:
        a,b = f
        for i in xrange(1,tables+1):
            clause = []
            alt_clause = []
            clause.extend(["~X"+str(a)+str(i),"X"+str(b)+str(i)])
            alt_clause.extend(["X"+str(a)+str(i),"~X"+str(b)+str(i)])
            #symbols.add("~X"+str(a)+str(i))
            symbols.add("X"+str(b)+str(i))
            symbols.add("X"+str(a)+str(i))
            #symbols.add("~X"+str(b)+str(i))
            list_clauses.append(clause)
            list_clauses.append(alt_clause)

def Cond3():
    for e in enemies:
        a,b = e
        for i in xrange(1,tables+1):
            clause = []
            clause.extend(["~X"+str(a)+str(i),"~X"+str(b)+str(i)])
            #symbols.add("~X"+str(a)+str(i))
            #symbols.add("~X"+str(b)+str(i))
            list_clauses.append(clause)

def ModelCheck(clause,model):
    unresolved = False
    for element in clause:
        sym = literal_symbol(element)
        if sym not in model:
            unresolved = True
            #return None
        else:
            if model[sym] == True and (element[0] != "~"):
                return True
            elif model[sym] == False and (element[0] == "~"):
                return True
            else:
                continue
    if unresolved:
        return None
    else:
        return False

def PureSymbol(symbols,clauses):
    for s in symbols:
        pos , neg = False ,False
        for c in clauses:
            if not pos and s in c: pos = True
            if not neg and "~"+s in c: neg = True
        if pos != neg:
            return s, pos
        return None, None

def UnitClause(clauses,model):
    for clause in clauses:
        unit = 0
        for ele in clause:
            sym = literal_symbol(ele)
            if sym not in model:
                unit = unit + 1
                P, value = sym , (ele[0] != "~")
        if unit == 1:
            return P, value
    return None, None


def Determine(clause,model):
    for ele in clause:
        if ele[0] == "~":
            ele = ele[1:]
        if ele not in model:
            return None
        else:
            bool = model[ele]
            if bool:
                return True
    return False


def remove(symbols,P):
    symbols.discard(P)
    return symbols

def Union(model,P,value):
    s = model.copy()
    s[P] = value
    return s

def literal_symbol(l):
    if l[0] == "~":
        return l[1:]
    else:
        return l

def Dpll(clauses,symbols,model):
    unknown_clauses = []
    for c in clauses:
        result = ModelCheck(c,model)
        # print "\nIN Dpll"
        # print "clauses: ",clauses
        # print "symbols: ",symbols
        # print "model : ",model
        if result == False:
            return False
        if result != True:
            unknown_clauses.append(c)
    if not unknown_clauses or not symbols:
        return model
    P ,value = PureSymbol(symbols, unknown_clauses)
    if P:
        # print "Added Pure SYmbols",P
        # print 'Model now is',model
        return Dpll(clauses, remove(symbols, P), Union(model,P,value))
    P, value = UnitClause(clauses,model)
    if P:
        # print "Added Unit",P
        # print 'Model now is', model
        return Dpll(clauses, remove(symbols, P), Union(model,P,value))

    P = symbols.pop()
    # model_1 = deepcopy(model)
    # model[P] = True
    # model_1[P] = False
    #print "Added not both of them", model, model_1
    return (Dpll(clauses,symbols, Union(model, P, True)) or Dpll(clauses,symbols, Union(model, P, False)))

def DpllSatisfiable():
    #model = Set([])
    list_symbols = symbols
    model = {}
    result = Dpll(list_clauses,list_symbols,model)
    #print result
    if result:
        print "yes"
        output.write("yes\n")
        Answer(result)
    else:
        output.write("no")
        print "no"

guests,tables = [int(x) for x in input.readline().strip().split(" ")]
#print guests, tables
for l in input.readlines():
    temp = l.strip().split(" ")
    if temp[2] == 'F':
        friends.append([temp[0],temp[1]])
    else:
        enemies.append([temp[0], temp[1]])


Cond1()
Cond2()
Cond3()
#print list_clauses
DpllSatisfiable()


