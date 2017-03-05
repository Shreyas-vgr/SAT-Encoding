from sets import Set

from boto.dynamodb.condition import NULL

input = open("Test_Cases/input3.txt",'r')
output = open("Test_Cases/output.txt",'w')

friends = []
enemies = []
list_clauses = []
symbols = Set([])
global guests
global tables

def Cond1():
    for i in xrange(1,guests+1):
        clause = []
        alt_clause = []
        for j in xrange(1,tables+1):
            clause.append("~X"+str(i)+str(j))
            alt_clause.append("X"+str(i)+str(j))
            symbols.add("~X"+str(i)+str(j))
            symbols.add("X"+str(i)+str(j))
        list_clauses.append(clause)
        list_clauses.append(alt_clause)

def Cond2():
    for f in friends:
        a,b = f
        clause = []
        alt_clause = []
        for i in xrange(1,tables+1):
            clause.extend(["~X"+str(a)+str(i),"X"+str(b)+str(i)])
            alt_clause.extend(["X"+str(a)+str(i),"~X"+str(b)+str(i)])
            symbols.add("~X"+str(a)+str(i))
            symbols.add("X"+str(b)+str(i))
            symbols.add("X"+str(a)+str(i))
            symbols.add("~X"+str(b)+str(i))
            list_clauses.append(clause)
            list_clauses.append(alt_clause)

def Cond3():
    for e in enemies:
        a,b = e
        clause = []
        for i in xrange(1,tables+1):
            clause.extend(["~X"+str(a)+str(i),"~X"+str(b)+str(i)])
            symbols.add("~X"+str(a)+str(i))
            symbols.add("~X"+str(b)+str(i))
            list_clauses.append(clause)

def ModelCheck(old_clauses,model):
    clauses = deepcopy(old_clauses)
    for m in model:
        for c in clauses:
            if m in c:
                clauses.remove(c)
            else:
                c.remove("~"+str(m))
            if not c:
                return False
    if not clauses:
        return True
    else:
        return "Done"

def PureSymbol(symbols,clauses,model):
    pass

def UnitClause(clauses,model):
    pass

def remove(symbols,P):
    symbols.discard(P)
    return

def Dpll(clauses,symbols,model):
    #print clauses,symbols,model
    result = ModelCheck(clauses,model)
    if result == True:
        return True
    elif result == False:
        return False
    else:
        P = PureSymbol(symbols,clauses,model)
        if not P:
            return Dpll(clauses, remove(symbols, P), model.add(str(P)))
        P = UnitClause(clauses,model)
        if not P:
            return Dpll(clauses, remove(symbols, P), model.add(str(P)))
        P = symbols.pop()
        return Dpll(clauses,symbols,model.add(str(P))) or \
               Dpll(clauses,symbols,model.add("~"+str(P)))

def DpllSatisfiable():
    return Dpll(list_clauses,symbols,Set([]))

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
#DpllSatisfiable()
#print len(list_clauses),list_clauses

