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

print(["x = ",numberOfGraphEdges, ", y = ", numberOfNode])

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