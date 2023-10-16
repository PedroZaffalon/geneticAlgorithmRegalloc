import numpy
import itertools
import random
import sys

def createInitialPopulation(graph, nRegister, numberOfIndividuals = 8, randomspill = False):
    nMax = nRegister
    if not randomspill:
        nMax -= 1
    nodesID = [x for x in graph["nodes"]]
    interference = [createAdjList(graph, x, nodesID) for x in graph["nodes"]]
    spillcosts = [spillCost(graph["nodes"], x) for x in graph["nodes"]]
    totalspillcost = sum(spillcosts)
    nNodes = len(graph["nodes"])
    population = numpy.empty(shape = (numberOfIndividuals, nNodes), dtype = numpy.uint8)
    for i in  range(numberOfIndividuals):
        for j in range(nNodes):
            population[i,j] = random.randint(0, nMax)
    return population, interference, spillcosts, totalspillcost

def fitness(individualChromosome, nRegister, interference, spillcosts, totalspillcost):
    validColors = 0
    spillsum = 0
    nNodes = len(individualChromosome)
    for i in range(nNodes):
        spillcost = spillcosts[i]
        if individualChromosome[i] == nRegister:
            spillsum += spillcost
        else:
            validColors += 1
            for adjNode in interference[i]:
                if individualChromosome[i] == individualChromosome[adjNode]:
                    individualChromosome[i] = nRegister
                    validColors -= 1
                    spillsum += spillcost
                    break
    #f = validColors/nNodes - 3 * spillsum/totalspillcost
    f =  1 - spillsum/totalspillcost
    return f, validColors, spillsum, (f == 1)

def getRandomParent(qualities):
    total = numpy.sum(qualities)
    n = random.uniform(0, 1)
    p_sum = 0
    for i, q in enumerate(qualities):
        p_sum += q/total
        if n <= p_sum:
            return i

def selectMatingPool(population, qualities, pop_data, numberOfParents):
    parents = numpy.empty((numberOfParents, population.shape[1]), dtype = numpy.uint8)
    parents_data = numpy.zeros((numberOfParents,2), dtype = numpy.uint32)
    parents_qualities = numpy.zeros(numberOfParents)
    for parentNumber in range(numberOfParents):
        maxQualityId = getRandomParent(qualities)
        parents[parentNumber, :] = population[maxQualityId, :]
        parents_data[parentNumber, :] = pop_data[maxQualityId, :]
        parents_qualities[parentNumber] = qualities[maxQualityId]
        qualities[maxQualityId] = 0
    return parents, parents_qualities, parents_data

def alternative_crossover(parents, numberOfIndividuals = 8):
    nRegister = parents.shape[1]
    newPopulation = numpy.empty(shape = (numberOfIndividuals, nRegister), dtype = numpy.uint8)
    for i in range(numberOfIndividuals):
        for j in range(nRegister):
            newPopulation[i,j] = parents[random.randint(0, parents.shape[0] - 1), j]
    return newPopulation


def crossover(parents, numberOfIndividuals = 8):
    newPopulation = numpy.empty(shape = (numberOfIndividuals, parents.shape[1]), dtype = numpy.uint8)
    numberNewlyGenerated = numberOfIndividuals
    parentsPermutations = list(itertools.permutations(iterable = numpy.arange(0, parents.shape[0]), r = 2))
    selectedPermutations = random.sample(range(len(parentsPermutations)), numberNewlyGenerated)
    for comb in range(len(selectedPermutations)):
        selectedCombId = selectedPermutations[comb]
        selectedComb = parentsPermutations[selectedCombId]
        halfSize = numpy.int32(newPopulation.shape[1] / 2)
        newPopulation[comb, 0 : halfSize] = parents[selectedComb[0], 0 : halfSize]
        newPopulation[comb, halfSize :] = parents[selectedComb[1], halfSize :]
    return newPopulation

def mutation(population, numberOfParentsMating, mutationPercent, nRegister, randomspill = False):
    nMax = nRegister
    if not randomspill:
        nMax -= 1
    for id in range(numberOfParentsMating, population.shape[0]):
        randomId = numpy.uint32(numpy.random.random(size = numpy.uint32(mutationPercent / 100 * population.shape[1])) * population.shape[1])
        newValues = random.randint(0, nMax)
        population[id, randomId] = newValues
    return population

def spillCost(nodes, nodeID):
    node = nodes[nodeID]
    spillCost = 0
    for i in node["uses deepness"]:
        spillCost += 10**i
    return spillCost

def createAdjList(graph, nodeID, nodesID):
    adjList = []
    for edge in graph["edges"]:
        adjNode = None
        if edge["node 1"] == nodeID:
            adjNode = edge["node 2"]
        elif edge["node 2"] == nodeID:
            adjNode = edge["node 1"]
        if adjNode is not None:
            adjNodeIndex = getNodeIndex(adjNode, nodesID)
            if adjNodeIndex == -1:
                sys.exit(1)
            adjList.append(adjNodeIndex)
    return adjList
        
def getNodeIndex(nodeID, nodesID):
    i = 0
    for node in nodesID:
        if nodeID == node:
            return i
        i += 1
    return -1