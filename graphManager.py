import json
import numpy
import geneticAlgorithm
from tqdm import tqdm

def read_graphs(input_file_name, output_file_name, nIndividuals, interval, registers, mating, mutation, generations):
    graphs = ler_arquivo_json(input_file_name)
    flag = False
    with open(output_file_name, 'w') as outputFile:
        for graphName in graphs:    
            print(graphName + ":")
            if flag:
                outputFile.write("\n\n")
            else:
                flag = True
            outputFile.write(graphName + ":\n")
            graph = graphs[graphName]
            print(len(graph["nodes"]), " nodes and ", len(graph["edges"]), " edges")
            outputFile.write(str(len(graph["nodes"])) + " nodes and " +  str(len(graph["edges"])) + " edges\n\n")
            optimal = False
            bestSolution = [[], 0, 0, 0, 0]
            nodesID, newPopulation = geneticAlgorithm.createInitialPopulation(graph, registers, nIndividuals)
            for iteration in tqdm(range(generations)):

                qualities = numpy.zeros(newPopulation.shape[0])
                pop_data = numpy.zeros((newPopulation.shape[0],2))
                for individualNumber in range(newPopulation.shape[0]):
                    qualitie, validColors, spill, valid = geneticAlgorithm.fitness(newPopulation[individualNumber, :], graph, nodesID, registers)
                    if valid:
                        print("\nOptimal solution found in interation " + str(iteration) + ":\n")
                        outputFile.write("Optimal solution found in interation " + str(iteration) + ":\n")
                        outputFile.write(str(newPopulation[individualNumber, :]))
                        optimal = True
                        break
                    if qualitie > bestSolution[1]:
                        bestSolution = [newPopulation[individualNumber, :], qualitie, validColors, spill, iteration]
                    qualities[individualNumber] = qualitie
                    pop_data[individualNumber, :] = [validColors, spill]

                if optimal:
                    break

                parents, parents_qualities, parents_data = geneticAlgorithm.selectMatingPool(newPopulation, qualities, pop_data, mating)

                if iteration % interval == 0:
                    outputFile.write("Manting population:\n")
                    for i in range(len(parents_data)):
                        outputFile.write("Solution: " + str(parents[i, :]) + ", Qualitie: " + str(parents_qualities[i]) + ", Valid Colors: " + str(parents_data[i,0])  + ", Spill cost: " + str(parents_data[i,1])  + "\n")

                newPopulation = geneticAlgorithm.crossover(parents, nIndividuals)
                newPopulation = geneticAlgorithm.mutation(newPopulation, mating, mutation, registers)

            if not optimal:
                outputFile.write("Best solution:\n")
                outputFile.write("Solution: " + str(bestSolution[0]) + "\n")
                outputFile.write("Qualitie: " + str(bestSolution[1]) + "\n")
                outputFile.write("Valid Colors: " + str(bestSolution[2]) + "\n")      
                outputFile.write("Spill cost: " + str(bestSolution[3]) + "\n")   
                outputFile.write("Iteration: " + str(bestSolution[4]))     

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
