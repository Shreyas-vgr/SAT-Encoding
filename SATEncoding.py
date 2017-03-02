input = open("Test_Cases/input1.txt",'r')
output = open("Test_Cases/output.txt",'w')

friends = []
enemies = []
list_clauses = []
global guests
global tables

def Cond1():
    for i in xrange(1,guests+1):
        clause = ""
        alt_clause = ""
        for j in xrange(1,tables+1):
            clause += "~X"+str(i)+str(j)
            alt_clause += "X"+str(i)+str(j)
            clause += "V"
            alt_clause += "V"
        list_clauses.append(clause[:-1])
        list_clauses.append(alt_clause[:-1])

def Cond2():
    for f in friends:
        a,b = f
        #print a,b
        for i in xrange(1,tables+1):
            clause = ""
            alt_clause = ""
            clause += "~X"+str(a)+str(i)+"VX"+str(b)+str(i)
            alt_clause += "X"+str(a)+str(i)+"V~X"+str(b)+str(i)
            list_clauses.append(clause)
            list_clauses.append(alt_clause)

def Cond3():
    

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
print list_clauses
