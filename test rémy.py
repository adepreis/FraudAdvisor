import cplex
import sys
import json

if (len(sys.argv) == 1):
    print("Please give dataset path as a command argument")
    exit()

datasetPath = sys.argv[1]
print("Loading " + datasetPath + " dataset")

if (datasetPath.find(".txt") == -1):
    print("Please use a .txt dataset file")
    exit()

nodeSet = []
graph = dict({})
with open(datasetPath, encoding='utf8') as file:
    for line in file:
        node = line.replace("\n", "").split("   ")
        minNode = min(node[0], node[1])
        maxNode = max(node[0], node[1])

        if (minNode not in nodeSet):
            nodeSet.append(minNode)
        if (maxNode not in nodeSet):
            nodeSet.append(maxNode)

        if (minNode in graph):
            set = graph.get(minNode)
            if (maxNode not in set):
                set.append(maxNode)
                graph[minNode] = set
        else:
            graph[minNode] = [maxNode]

numberOfNode= len(nodeSet)
numberOfGraphEdges = 0
for key in graph:
    for el in graph[key]:
        numberOfGraphEdges += 1

print('\nGraph :', graph)
print('Number of graph edge : ',numberOfGraphEdges, ', Number of nodes = ', numberOfNode, '\n')

# ============================================================

# Input all the data and parameters here
num_decision_var = numberOfNode + numberOfGraphEdges
num_constraints = numberOfGraphEdges * 2 + 1

constraint_type = ["L", "G", "E"] # Less, Greater, Equal

print('Number of decision var :', num_decision_var, ', Number of constraints :', num_constraints, '\n')

# ============================================================

# Establish the Linear Programming Model
myProblem = cplex.Cplex()

# Add the decision variables and set their lower bound and upper bound (if necessary)
myProblem.variables.add(names= ["x"+str(i) for i in range(num_decision_var)])
for i in range(num_decision_var):
    myProblem.variables.set_lower_bounds(i, 0.0) # pour tout x, on a x >= 0

# Set the type of each variables
#myProblem.variables.set_types(0, myProblem.variables.type.integer)
#myProblem.variables.set_types(1, myProblem.variables.type.continuous)

# Add constraints
# CONSTRAINT (4)
global_counter = 1
local_counter = 0
for i in graph:
    for j in graph[i]:
        print('i =', i, '; j =', j)
        myProblem.linear_constraints.add(
            #lin_expr= [['x' + str(counter), 'x' + str(numberOfGraphEdges + nodeSet.index(i))], [1.0, -1.0]],
            lin_expr= [cplex.SparsePair(ind = ['x' + str(local_counter), 'x' + str(numberOfGraphEdges + nodeSet.index(i))], val = [1.0, -1.0])],
            rhs= [0],
            names = ['c'+str(global_counter)],
            senses = ['L']
        )
        local_counter += 1
        global_counter += 1
# CONSTRAINT (5)
local_counter = 0
for i in graph:
    for j in graph[i]:
        myProblem.linear_constraints.add(
            #lin_expr= [[['x' + str(counter), 'x' + str(numberOfGraphEdges + nodeSet.index(j))], [1.0, -1.0]]],
            lin_expr= [cplex.SparsePair(ind = ['x' + str(local_counter), 'x' + str(numberOfGraphEdges + nodeSet.index(i))], val = [1.0, -1.0])],
            rhs= [0],
            names = ['c'+str(global_counter)],
            senses = ['L']
        )
        local_counter += 1
        global_counter += 1
# CONSTRAINT (6)
myProblem.linear_constraints.add(
    lin_expr = [cplex.SparsePair(ind = ['x' + str(i) for i in range(numberOfGraphEdges, numberOfGraphEdges + numberOfNode)], val = [1.0] * numberOfNode)],
    senses = ['L']
)

# Add objective function and set its sense
for i in range(numberOfGraphEdges):
    myProblem.objective.set_linear([(i, 1.0)])
myProblem.objective.set_sense(myProblem.objective.sense.maximize)

# CHECK
print('\nCHECK')
print('Linear constraints :')
print(' > num :', myProblem.linear_constraints.get_num())
print(' > rhs :', myProblem.linear_constraints.get_rhs())
print(' > senses :', myProblem.linear_constraints.get_senses())
print(' > range_values :', myProblem.linear_constraints.get_range_values())
#print(' > coefficients :', myProblem.linear_constraints.get_coefficients())
print(' > rows :', myProblem.linear_constraints.get_rows())
print(' > names', myProblem.linear_constraints.get_names())



print('Objectives :', myProblem.objective.get_linear())

# Solve the model and print the answer
myProblem.solve()
print(myProblem.solution.get_objective_value())
print(myProblem.solution.get_values())


"""
# OLD VERSION :

# ============================================================
# This file gives us a sample to use Cplex Python API to
# establish a Linear Programming model and then solve it.
# The Linear Programming problem displayed bellow is as:
#                  min z = cx
#    subject to:      Ax = b
# ============================================================

# ============================================================
# Input all the data and parameters here
num_decision_var = numberOfGraphEdges * 2
num_constraints = numberOfNode

A = [
    [1.0, -2.0, 1.0],
    [-4.0, 1.0, 2.0],
    [-2.0, 0, 1.0],
]
b = [11.0, 3.0, 1.0]
c = [-3.0, 1.0, 1.0]

constraint_type = ["L", "G", "E"] # Less, Greater, Equal
# ============================================================

# Establish the Linear Programming Model
myProblem = cplex.Cplex()

# Add the decision variables and set their lower bound and upper bound (if necessary)
myProblem.variables.add(names= ["x"+str(i) for i in range(num_decision_var)])
for i in range(num_decision_var):
    myProblem.variables.set_lower_bounds(i, 0.0) # pour tout x, on a x >= 0

# Add constraints
for i in range(num_constraints):
    myProblem.linear_constraints.add(
        lin_expr= [cplex.SparsePair(ind= [j for j in range(num_decision_var)], val= A[i])],
        rhs= [b[i]],
        names = ["c"+str(i)],
        senses = [constraint_type[i]]
    )

# Add objective function and set its sense
for i in range(num_decision_var):
    myProblem.objective.set_linear([(i, c[i])])
myProblem.objective.set_sense(myProblem.objective.sense.maximize)

# Solve the model and print the answer
myProblem.solve()
print(myProblem.solution.get_values())
"""