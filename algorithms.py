import cplex
import sys
import re
import time
import pandas as pd

def run_linear(datasetPath):
    """
    # Set datapath in argv
    if (len(sys.argv) == 1):
        print("Please give dataset path as a command argument")
        exit()

    datasetPath = sys.argv[1]
    """
    print("Loading " + datasetPath + " dataset")

    if (datasetPath.find(".txt") == -1):
        print("Please use a .txt dataset file")
        exit()
        
    nodeSet = []
    graph = dict({})
    with open(datasetPath, encoding='utf8') as file:
        for line in file:
            if (line != "" and line[0] != "#"): # ignore comments at  the beginning of datasets
                node = re.split(r"\s+", line.replace("\n", ""))
                #print(node)
                minNode = min(node[0], node[1])
                maxNode = max(node[0], node[1])

    leftNode = []
    rightNode = []
    with open(datasetPath, encoding='utf8') as file:
        for line in file:
            if (line != "" and line[0] != "#"): # ignore comments at the beginning of datasets
                node = re.split(r"\s+", line.replace("\n", ""))
                minNode = min(node[0], node[1])
                maxNode = max(node[0], node[1])

                leftNode.append(minNode)
                rightNode.append(maxNode)

    data = {
        'Left': leftNode,
        'Right': rightNode
    }

    df = pd.DataFrame(data=data)

    setGraph = df.groupby("Left")['Right'].apply(set)
    indexArray = setGraph.index.array
    valuesArray = setGraph.values

    nodeSet = []
    graph = dict({})
    for i in range (0, len(indexArray)):
        leftNode = indexArray[i]
        rightNodes = list(valuesArray[i])
        graph[leftNode] = rightNodes

        nodeSet.append(leftNode)
        for node in rightNodes:
            nodeSet.append(node)
    nodeSet = list(set(nodeSet))

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

    print('Starting resolution of the problem')

    start_time = time.time()

    # Solve the model
    myProblem.solve()

    print("done @ ", time.time() - start_time)

    values = myProblem.solution.get_values()
    real_names = [ 'x' + str(i) + '_' + str(j) for i in graph for j in graph[i] ]
    real_names += [ 'y' + str(i) for i in graph ]
    for i in graph:
        for j in graph[i]:
            if ('y' + str(j) not in real_names):
                real_names += [ 'y' + str(j) ]

    assert(len(values) == len(real_names))

    """
    # Print the answer
    print('\nObjective value :', myProblem.solution.get_objective_value())

    print('\nDecision variable values :')
    
    for i in range (len(real_names)):
        print(real_names[i] + ' = ' + str(values[i]))
    """

    file = open("./out/decision_variable_values.out", 'w')
    for i in range (len(real_names)):
        file.write(real_names[i] + ' = ' + str(values[i]) + '\n')
    file.close()

    return myProblem.solution.get_objective_value()

if __name__ == '__main__':
    dataset = "examples/example.txt" # CHEMIN DU DATASET CHOISI
    print('Objective value :', run_linear(dataset))