import numpy
import itertools
import random
import graphManager

def createInitialPopulation(graph, nRegister, numberOfIndividuals = 8):
    nodesID = [[x,0] for x in graph["nodes"]]
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
        spillcost = graphManager.spillCost(graph, nodeID, nodesID)
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
                adjNodeIndex = graphManager.getNodeIndex(adjNode, nodesID)
                if individualChromosome[i] == individualChromosome[adjNodeIndex]:
                    validColors -= 1
                    break
    f = validColors/(nNodes - nSpill)  - 2 * spillsum/totalspill
    return f, spillsum, (validColors == nNodes)

def selectMatingPool(population, qualities, spills, numberOfParents):
    parents = numpy.empty((numberOfParents, population.shape[1]), dtype = numpy.uint8)
    parents_spill = numpy.empty((numberOfParents), dtype = numpy.uint8)
    parents_qualitie = numpy.empty((numberOfParents), dtype = numpy.uint8)
    for parentNumber in range(numberOfParents):
        maxQualityId = numpy.where(qualities == numpy.max(qualities))
        maxQualityId = maxQualityId[0][0]
        parents[parentNumber, :] = population[maxQualityId, :]
        parents_spill[parentNumber] = spills[maxQualityId]
        parents_qualitie[parentNumber] = qualities[maxQualityId]
        qualities[maxQualityId] = -2
    return parents, parents_qualitie, parents_spill

def crossover(parents, numberOfIndividuals = 8):
    newPopulation = numpy.empty(shape = (numberOfIndividuals, parents.shape[0]), dtype = numpy.uint8)
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