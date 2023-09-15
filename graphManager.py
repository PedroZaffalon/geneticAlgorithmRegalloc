import json
import numpy
import geneticAlgorithm
from tqdm import tqdm

def read_graphs(input_file_name, output_file_name, nIndividuals, interval, registers, mating, mutation, generations):
    graphs = ler_arquivo_json(input_file_name)
    flag = False
    for graphName in graphs:
        with open(output_file_name, 'r') as outputFile:
            print(graphName + ":")
            if flag:
                outputFile.write("\n")
            else:
                flag = True
            outputFile.write(graphName + ":\n")
            graph = graphs[graphName]

            optimal = False
            bestSolution = [[], 0, 0, 0]
            nodesID, newPopulation = geneticAlgorithm.createInitialPopulation(graph, registers, nIndividuals)
            for iteration in tqdm(range(generations)):

                qualities = numpy.zeros(newPopulation.shape[0])
                spills = numpy.zeros(newPopulation.shape[0])
                for individualNumber in range(newPopulation.shape[0]):
                    qualitie, spill, valid = geneticAlgorithm.fitness(newPopulation[individualNumber, :], graph, nodesID, registers)
                    if valid:
                        outputFile.write("Optimal solution find in interation " + str(iteration), + ":")
                        outputFile.write(str(newPopulation[individualNumber, :]))
                        optimal = True
                        break
                    if qualitie > bestSolution[1] or (qualitie == bestSolution[1] and spill < bestSolution[2]):
                        bestSolution = [newPopulation[individualNumber, :], qualitie, spill, iteration]
                    qualities[individualNumber] = qualitie
                    spills[individualNumber] = spill
                    
                parents, parents_qualitie, parents_spill = geneticAlgorithm.selectMatingPool(newPopulation, qualities, spills, mating)

                if iteration % interval == 0:
                    outputFile.write("Manting population:")
                    for i in range(len(parents_spill)):
                        outputFile.write("Solution: " + str(parents[i, :]) + ", Qualitie: " + str(parents_qualitie[i]) + ", Spill cost: " + str(parents_spill[i]))

                newPopulation = geneticAlgorithm.crossover(parents, nIndividuals)
                newPopulation = geneticAlgorithm.mutation(newPopulation, mating, mutation)

            if not optimal:
                outputFile.write("Best solution:")
                outputFile.write("Solution: " + str(bestSolution[0]))
                outputFile.write("Qualitie: " + str(bestSolution[1]))   
                outputFile.write("Spill cost: " + str(bestSolution[2]))   
                outputFile.write("Iteration: " + str(bestSolution[3]))     
        



def ler_arquivo_json(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            dados = json.load(arquivo)
            return dados
    except FileNotFoundError:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"O arquivo '{nome_arquivo}' não é um JSON válido.")
        return {}

def spillCost(graph, nodeId, nodesID):
    node = graph["nodes"][nodesID[nodeId][0]]
    spillCost = 0
    for i in node["uses deepness"]:
        spillCost += 10**i
    return spillCost

def getNodeIndex(nodeId, nodesID):
    i = 0
    for node in nodesID:
        if nodeId == node:
            return i
        i += 1
    return -1
