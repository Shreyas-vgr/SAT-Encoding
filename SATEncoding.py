from copy import deepcopy
import copy

input = open("Test_Cases/input5.txt",'r')
output = open("Test_Cases/output.txt",'w')

friends = []
enemies = []
list_clauses = []
symbols = set()
file_logs = ""
global guests
global tables

def Cond1():
    for i in xrange(1,guests+1):
        clause = []
        alt_clause = []
        for j in xrange(1,tables+1):
            clause.append("~X" + "-" + str(i) + "-" + str(j))
            alt_clause.append("X"+ "-" + str(i)+ "-" +str(j))
            #symbols.add("~X"+str(i)+str(j))
            symbols.add("X"+ "-" + str(i) + "-" + str(j))
        list_clauses.append(alt_clause)
        if tables > 1:
            list_clauses.append(clause)

def Cond2():
    for f in friends:
        a,b = f
        for i in xrange(1,tables+1):
            clause = []
            alt_clause = []
            clause.extend(["~X"+ "-" +str(a)+ "-" +str(i),"X" + "-" + str(b) + "-" +str(i)])
            alt_clause.extend(["X"+ "-" + str(a) + "-" +str(i),"~X"+ "-"+ str(b)+"-"+ str(i)])
            #symbols.add("~X"+str(a)+str(i))
            symbols.add("X"+ "-" +str(b)+ "-" +str(i))
            symbols.add("X"+ "-" +str(a)+ "-" +str(i))
            #symbols.add("~X"+str(b)+str(i))
            list_clauses.append(clause)
            list_clauses.append(alt_clause)

def Cond3():
    for e in enemies:
        a,b = e
        for i in xrange(1,tables+1):
            clause = []
            clause.extend(["~X"+ "-" +str(a)+ "-"+str(i),"~X"+ "-"+ str(b)+ "-" +str(i)])
            #symbols.add("~X"+str(a)+str(i))
            #symbols.add("~X"+str(b)+str(i))
            list_clauses.append(clause)

def remove(symbols,P):
    temp = set()
    if P[0] == "~":
        symbols.discard(P[1:])
    else:
        symbols.discard(P)
        for s in symbols:
            if s[0:3] == P[0:3]:
                temp.add(s)
        for i in temp:
            symbols.discard(i)

def Union(model,P,type):
    if type:
        model.add(P)
    else:
        model.add("~"+P)
    return copy.deepcopy(model)

def Answer(model):
    global guests
    global file_logs
    for i in xrange(guests):
        for j in model:
            element = str(j).split("-")
            if element[0] == "X" and element[1] == str(i+1):
                file_logs += "\n" + element[1] + " " + element[2]

def ModelCheck(clauses, model):
    #clauses = deepcopy(old_clause)
    if not model:
        return "None"

    remove_clauses = []
    for mod_element in model:
        for clause_element in clauses:
            if not clause_element:
                return False
            if mod_element in clause_element:
                remove_clauses.append(clause_element)
                #clauses.remove(clause_element)
            else:
                if mod_element[0] == "~":
                    if mod_element[1:] in clause_element:
                        clause_element.remove(mod_element[1:])
                else:
                    if ("~" + mod_element) in clause_element:
                        clause_element.remove("~" + mod_element)
            if not clause_element:
                return False

    if not clauses:
        Answer(model)
        return True

    for clause_ele in clauses:
        if not clause_ele:
            return False

    for clause in remove_clauses:
        clauses.remove(clause)
    return "Cont"

def PureSymbol(symbols,clauses,model):
    pure_symbol = 0
    remove_clauses = []
    if not symbols:
        return None
    for clause_element in clauses:
        pure_symbol = 1
        for del_clause in clause_element:
            for element in clauses:
                if del_clause[0] == "~":
                    if del_clause[1:] in element:
                        pure_symbol = 0
                        break
                else:
                    if ("~" + del_clause) in element:
                        pure_symbol = 0
                        break
            if pure_symbol:
                for items in clauses:
                    if del_clause in items:
                        remove_clauses.append(items)
                for element in remove_clauses:
                    clauses.remove(element)
                return del_clause
    return None

def UnitClause(clauses,model):
    remove_clauses = []
    for clause_element in clauses:
        if len(clause_element) == 1:
            model.add(clause_element[0])
            for del_clause in clauses:
                if clause_element[0] in del_clause:
                    remove_clauses.append(del_clause)
                else:
                    if clause_element[0][0] == "~":
                        if clause_element[0][1:] in del_clause:
                            del_clause.remove(clause_element[0][1:])
                    else:
                        if ("~" + clause_element[0]) in del_clause:
                            del_clause.remove("~" + clause_element[0])
            for item in remove_clauses:
                clauses.remove(item)
            return clause_element[0]
    return None

def Dpll(clauses,symbols,model):

    if not clauses:
        Answer(model)
        return True

    result = ModelCheck(clauses,model)

    if result == True:
        Answer(model)
        return True
    elif result == False:
        return False
    else:
        P = PureSymbol(symbols,clauses,model)
        if P:
            model.add(str(P))
            if symbols:
                remove(symbols,P)
            return Dpll(clauses, symbols, model)
        P = UnitClause(clauses,model)
        if P:
            model.add(str(P))
            if symbols:
                remove(symbols,P)
            return Dpll(clauses, symbols, model)

        if not symbols:
            Answer(model)
            return True

        if not clauses:
            Answer(model)
            return True

        P = symbols.pop()
        remove(symbols,P)

        return Dpll(clauses,copy.deepcopy(symbols),Union(model,P,True)) or \
               Dpll(clauses,copy.deepcopy(symbols),Union(model,P,False))

def DpllSatisfiable():
    list_symbols = symbols
    model = set()
    result = Dpll(list_clauses,list_symbols,model)
    if result:
        print "yes"
        output.write("yes\n")
    else:
        output.write("no\n")
        print "no"
    print file_logs[1:]
    output.write(file_logs[1:])

guests,tables = [int(x) for x in input.readline().strip().split(" ")]
for line in input.readlines():
    temp = line.strip().split(" ")
    if temp[2] == 'F':
        friends.append([temp[0],temp[1]])
    else:
        enemies.append([temp[0], temp[1]])

Cond1()
Cond2()
Cond3()
DpllSatisfiable()


