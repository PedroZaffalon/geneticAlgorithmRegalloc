import numpy
import itertools
import random
import sys

def createInitialPopulation(graph, nRegister, numberOfIndividuals = 8):
    nodesID = [x for x in graph["nodes"]]
    nNodes = len(graph["nodes"])
    population = numpy.empty(shape = (numberOfIndividuals, nNodes), dtype = numpy.uint8)
    for i in  range(numberOfIndividuals):
        for j in range(nNodes):
            population[i,j] = random.randint(0, nRegister)
    return nodesID, population

def fitness(individualChromosome, graph, nodesID, nRegister):
    validColors = 0
    nSpill = 0
    spillsum = 0
    totalspill = 0
    nNodes = len(individualChromosome)
    for i in range(nNodes):
        nodeID = nodesID[i]
        spillcost = spillCost(graph, nodeID)
        totalspill += spillcost
        if individualChromosome[i] == nRegister:
            spillsum += spillcost
            nSpill += 1
        else:
            validColors += 1
            for edge in graph["edges"]:
                flag = False
                if edge["node 1"] == nodeID:
                    adjNode = edge["node 2"]
                    flag = True
                elif edge["node 2"] == nodeID:
                    adjNode = edge["node 1"]
                    flag = True
                if flag:
                    adjNodeIndex = getNodeIndex(adjNode, nodesID)
                    if adjNodeIndex == -1:
                        sys.exit(1)
                    if individualChromosome[i] == individualChromosome[adjNodeIndex]:
                        individualChromosome[i] = nRegister
                        validColors -= 1
                        spillsum += spillcost
                        nSpill += 1
                        break
    #f = validColors/nNodes - 3 * spillsum/totalspill
    f =  1 - spillsum/totalspill
    return f, validColors, spillsum, (f == 1)

def selectMatingPool(population, qualities, pop_data, numberOfParents):
    parents = numpy.empty((numberOfParents, population.shape[1]), dtype = numpy.uint8)
    parents_data = numpy.zeros((numberOfParents,2), dtype = numpy.uint32)
    parents_qualities = numpy.zeros(numberOfParents)
    for parentNumber in range(numberOfParents):
        maxQualityId = numpy.where(qualities == numpy.max(qualities))
        maxQualityId = maxQualityId[0][0]
        parents[parentNumber, :] = population[maxQualityId, :]
        parents_data[parentNumber, :] = pop_data[maxQualityId, :]
        parents_qualities[parentNumber] = qualities[maxQualityId]
        qualities[maxQualityId] = -2
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
    newPopulation[0 : parents.shape[0], :] = parents
    numberNewlyGenerated = numberOfIndividuals - parents.shape[0]
    parentsPermutations = list(itertools.permutations(iterable = numpy.arange(0, parents.shape[0]), r = 2))
    selectedPermutations = random.sample(range(len(parentsPermutations)), numberNewlyGenerated)
    combId = parents.shape[0]
    for comb in range(len(selectedPermutations)):
        selectedCombId = selectedPermutations[comb]
        selectedComb = parentsPermutations[selectedCombId]
        halfSize = numpy.int32(newPopulation.shape[1] / 2)
        newPopulation[combId + comb, 0 : halfSize] = parents[selectedComb[0], 0 : halfSize]
        newPopulation[combId + comb, halfSize :] = parents[selectedComb[1], halfSize :]
    return newPopulation


def mutation(population, numberOfParentsMating, mutationPercent, nRegister):
    for id in range(numberOfParentsMating, population.shape[0]):
        randomId = numpy.uint32(numpy.random.random(size = numpy.uint32(mutationPercent / 100 * population.shape[1])) * population.shape[1])
        newValues = random.randint(0, nRegister)
        population[id, randomId] = newValues
    return population


def spillCost(graph, nodeID):
    node = graph["nodes"][nodeID]
    spillCost = 0
    for i in node["uses deepness"]:
        spillCost += 10**i
    return spillCost

def getNodeIndex(nodeID, nodesID):
    i = 0
    for node in nodesID:
        if nodeID == node:
            return i
        i += 1
    return -1