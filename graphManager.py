import json
import numpy
import geneticAlgorithm
import os
from tqdm import tqdm

def read_graphs(input_file_name, output_file_name, nIndividuals, interval, registers, mating, mutation, randomspill, generations, alternativeCrossover, singlegraph):
    
    crossoverFunction = geneticAlgorithm.crossover
    if alternativeCrossover:
        crossoverFunction = geneticAlgorithm.alternative_crossover  
    graphs = ler_arquivo_json(input_file_name)
    print(os.path.basename(input_file_name), "\n")

    if singlegraph:
        graphs = {1 : graphs}

    i = 0
    for graphName in graphs:
        i += 1
        output_file = output_file_name
        if not singlegraph:   
            print(graphName + ":")
            output_file += "_" + str(i)
              
        outputResults = {}
        if interval != 0:
            outputResults['Parcial solutions'] = {} 
        graph = graphs[graphName]
        print(len(graph["nodes"]), " nodes and ", len(graph["edges"]), " edges")
        outputResults["nodes number"]  = len(graph["nodes"])
        outputResults["edges number"]  = len(graph["edges"])
        optimal = False
        bestSolution = [[], 0, 0, 0, 0]
        newPopulation, interference, spillcosts, totalspillcost = geneticAlgorithm.createInitialPopulation(graph, registers, nIndividuals, randomspill)
        for iteration in tqdm(range(generations)):
            qualities = numpy.zeros(newPopulation.shape[0])
            pop_data = numpy.zeros((newPopulation.shape[0],2))
            for individualNumber in range(newPopulation.shape[0]):
                qualitie, validColors, spill, valid = geneticAlgorithm.fitness(newPopulation[individualNumber, :], registers, interference, spillcosts, totalspillcost)
                if valid:
                    print("\nOptimal solution found in iteration " + str(iteration) + ":\n")
                    outputResults["Solution"] = newPopulation[individualNumber, :].tolist()
                    outputResults["Qualitie"]  = 1
                    outputResults["Valid colors"]  = len(graph["nodes"])
                    outputResults["Spill cost"]  = 0
                    outputResults["Iteration"]  = iteration
                    optimal = True
                    break
                if qualitie > bestSolution[1]:
                    bestSolution = [newPopulation[individualNumber, :], qualitie, validColors, spill, iteration]
                qualities[individualNumber] = qualitie
                pop_data[individualNumber, :] = [validColors, spill]

            if optimal:
                break

            parents, parents_qualities, parents_data = geneticAlgorithm.selectMatingPool(newPopulation, qualities, pop_data, mating)

            if interval != 0 and iteration % interval == 0:
                outputResults[i] = []
                for i in range(len(parents_data)):
                    obj = {}
                    obj["Solution"] = parents[i, :].tolist()
                    obj["Qualitie"]  = parents_qualities[i]
                    obj["Valid colors"] = parents_data[i,0]
                    obj["Spill cost"]  = parents_data[i,1]
                    outputResults[i].append(obj)

            newPopulation = crossoverFunction(parents, nIndividuals)
            newPopulation = geneticAlgorithm.mutation(newPopulation, mating, mutation, registers, randomspill)

        if not optimal:
            outputResults["Solution"] = bestSolution[0].tolist()
            outputResults["Qualitie"]  = bestSolution[1]
            outputResults["Valid colors"] = bestSolution[2]
            outputResults["Spill cost"]  = bestSolution[3]
            outputResults["Iteration"]  = bestSolution[4]

        output_file += ".json"
        with open(output_file, 'w') as outputFile:
            json.dump(outputResults, outputFile, indent = 4)

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
