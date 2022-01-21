import datetime
import sys
import random

def graphGenerator(nodeNumber, edgeNumber):
    print("Generating a random graph with ", nodeNumber, " nodes and ", edgeNumber, " edges.")

    graph = dict({})
    for egdeIndex in range(0, edgeNumber):
        choice1 = random.randint(0, nodeNumber)
        choice2 = random.randint(0, nodeNumber)
        while (choice1 == choice2):
            choice2 = random.randint(0, nodeNumber)
        
        minNode = min(choice1, choice2)
        maxNode = max(choice1, choice2)

        if (minNode in graph):
            arr = graph[minNode]
            arr.append(maxNode)
            graph[minNode] = arr
        else:
            graph[minNode] = [maxNode]

    print(graph)

    res = ""
    for key in graph:
        edges = list(set(graph[key]))
        for edge in edges:
            res = res + str(key) + "   " + str(edge) + "\n"

    fileName = str(datetime.datetime.now()).replace("-", "").replace(":", "").replace(" ", "").split(".")[0] + ".txt"
    f = open("dataset/" +  fileName, "a")
    f.write(res)
    f.close()

    print(fileName + " has been generating !")

    return "dataset/" +  fileName

if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print("Please give a number of nodes & edges")
        exit()

    nodeNumber = int(sys.argv[1])
    edgeNumber = int(sys.argv[2])

    graphGenerator(nodeNumber, edgeNumber)