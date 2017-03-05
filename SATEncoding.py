from sets import Set
from copy import deepcopy

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
    newClause = deepcopy(old_clauses)
    if not model:
        return "None"
    for mod_ele in model:
        for clause_ele in newClause:
            if not clause_ele:
                return False
            if mod_ele in clause_ele:
                newClause.remove(clause_ele)
            else:
                if mod_ele[0] == "~":
                    if mod_ele[1:] in clause_ele:
                        newClause.remove(mod_ele[1:])
                else:
                    if ("~" + mod_ele) in clause_ele:
                        newClause.remove("~" + mod_ele)
            if not clause_ele:
                return False

    if not newClause:
        return True

    for c in newClause:
        if not c:
            return False

    return "Cont"

def PureSymbol(symbols,clauses,model):
    isPure = 0
    if not symbols:
        return None
    for clause_ele in clauses:
        isPure = 1
        for del_clause in clause_ele:
            if del_clause[0] == "~":
                if del_clause[1:] in symbols:
                    isPure = 0
                    break
            else:
                if ("~" + del_clause) in symbols:
                    isPure = 0
                    break
            if isPure:
                model.add(del_clause)
                for j in clauses:
                    if del_clause in j:
                        clauses.remove(j)
                return del_clause
    return None

def UnitClause(clauses,model):
    for clause_ele in clauses:
        if len(clause_ele) == 1:
            model.add(clause_ele[0])
            for del_clause in clauses:
                if clause_ele[0] in del_clause:
                    clauses.remove(del_clause)
                else:
                    if clause_ele[0][0] == "~":
                        if clause_ele[0][1:] in del_clause:
                            del_clause.remove(clause_ele[0][1:])
                    else:
                        if ("~" + clause_ele[0]) in del_clause:
                            del_clause.remove("~" + clause_ele[0])
            return clause_ele[0]
    return None

def remove(symbols,P):
    if symbols:
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
print DpllSatisfiable()
#print len(list_clauses),list_clauses

