import graphManager
import click
import os
import shutil

@click.command()
@click.option('--dir', '-d', default="", help='Path to directory with .ll input files.')
@click.option('--output', '-o', default="", help='Path to output directory.')
@click.option('--population', '-p', default=32, help='Solutions per Population.')
@click.option('--interval', '-i', default=100, help='Savepoint interval to write output file.')
@click.option('--registers', '-r', default=16, help='Number of registers.')
@click.option('--mating', '-m', default=8, help='Number of Parents Mating.')
@click.option('--mutation', '-d', default=0.01, help='Mutation Percent.')
@click.option('--generations', '-g', default=50000, help='Number of generations.')
@click.option('--clear', '-c', is_flag=True, default=False, help='Remove files in output directory.')

def cli(dir, output, population, interval, registers, mating, mutation, generations, clear):
    if dir == "":
        dir = os.getcwd()
    
    if output == "":
        output = dir
        clear = False

    if clear:
        if os.path.exists(output):
        # Percorre todos os arquivos e pastas dentro do diretório
            for item in os.listdir(output):
                item_path = os.path.join(output, item)

                # Verifica se é um arquivo
                if os.path.isfile(item_path):
                    os.remove(item_path)
                # Verifica se é uma pasta
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

    if not os.path.exists(output):
        os.makedirs(output)
    
    for file_name in os.listdir(dir):
        if file_name.endswith(".json"):
            print("aaa")
            input_file_name = os.path.join(dir, file_name)
            output_file_name = os.path.join(output, file_name[:-3] + ".txt")
            graphManager.read_graphs(input_file_name, output_file_name, population, interval, registers, mating, mutation, generations)



    