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
    numberOfGraphEdges += len(graph[key])

"""
# CHECK
print('\nXXXXXXXXXX\n\nCHECK\n')

print('Graph :', graph)
print ('nodeSet :', nodeSet)
print('Number of nodes : ', numberOfNode)
print('Number of graph edges : ',numberOfGraphEdges)
"""

# ============================================================

# Input all the data and parameters here
num_decision_var = numberOfNode + numberOfGraphEdges
num_constraints = numberOfGraphEdges * 2 + 1
constraint_types = ["L", "G", "E"] # Less, Greater, Equal

# ============================================================

# Establish the Linear Programming Model
myProblem = cplex.Cplex()

# Add the decision variables and set their lower bound and upper bound (if necessary)
myProblem.variables.add(names= ["x"+str(i) for i in range(num_decision_var)])
for i in range(num_decision_var):
    myProblem.variables.set_types(i, myProblem.variables.type.continuous)
    myProblem.variables.set_lower_bounds(i, 0) # pour tout x, on a x >= 0
    myProblem.variables.set_upper_bounds(i, cplex.infinity)

# Set the type of each variables
#myProblem.variables.set_types(id, myProblem.variables.type.integer)
#myProblem.variables.set_types(id, myProblem.variables.type.continuous)

# Add constraints
# CONSTRAINT (4)
global_counter = 0
local_counter = 0
for i in graph:
    for j in graph[i]:
        #print('i =', i, '; j =', j)
        myProblem.linear_constraints.add(
            lin_expr= [cplex.SparsePair(ind = ['x' + str(local_counter), 'x' + str(numberOfGraphEdges + nodeSet.index(i))], val = [1.0, -1.0])],
            rhs = [0],
            names = ['c'+str(global_counter)],
            senses = constraint_types[0]
        )
        local_counter += 1
        global_counter += 1
# CONSTRAINT (5)
local_counter = 0
for i in graph:
    for j in graph[i]:
        myProblem.linear_constraints.add(
            lin_expr= [cplex.SparsePair(ind = ['x' + str(local_counter), 'x' + str(numberOfGraphEdges + nodeSet.index(j))], val = [1.0, -1.0])],
            rhs= [0],
            names = ['c'+str(global_counter)],
            senses = constraint_types[0]
        )
        local_counter += 1
        global_counter += 1
# CONSTRAINT (6)
myProblem.linear_constraints.add(
    lin_expr = [cplex.SparsePair(ind = ['x' + str(i) for i in range(numberOfGraphEdges, numberOfGraphEdges + numberOfNode)], val = [1.0] * numberOfNode)],
    rhs = [1],
    names = ['c'+str(global_counter)],
    senses = constraint_types[0]
)

# Add objective function and set its sense
for i in range(numberOfGraphEdges):
    myProblem.objective.set_linear([(i, 1.0)])
myProblem.objective.set_sense(myProblem.objective.sense.maximize)

"""
print('Objectives :', myProblem.objective.get_linear())

print('\nDecision variables')
print(' > number :', myProblem.variables.get_num())
print(' > names :', myProblem.variables.get_names())
print(' > lower bounds :', myProblem.variables.get_lower_bounds())
print(' > upper bounds :', myProblem.variables.get_upper_bounds())

print('\nLinear constraints :')
print(' > number :', myProblem.linear_constraints.get_num())
print(' > names :', myProblem.linear_constraints.get_names())
print(' > rhs :', myProblem.linear_constraints.get_rhs())
print(' > senses :', myProblem.linear_constraints.get_senses())
print(' > range_values :', myProblem.linear_constraints.get_range_values())
print(' > rows :')
for i in myProblem.linear_constraints.get_rows():
    print(i)
#print(' > num_nonzeros :', myProblem.linear_constraints.get_num_nonzeros())
print(' > histogram :', myProblem.linear_constraints.get_histogram())

print('\nXXXXXXXXXX\n')
"""

# Solve the model and print the answer
myProblem.solve()
print('\nObjective value :', myProblem.solution.get_objective_value())
print('Decision variable values :', myProblem.solution.get_values())