import click
import os
import shutil
from subdir import percorrer_subdiretorios, search_dir

@click.command()
@click.option('--dir', '-d', default="", help='Path to directory with .ll input files.')
@click.option('--output', '-o', default="", help='Path to output directory.')
@click.option('--population', '-p', default=64, help='Solutions per Population.')
@click.option('--interval', '-i', default=0, help='Savepoint interval to write output file.')
@click.option('--registers', '-r', default=16, help='Number of registers.')
@click.option('--mating', '-m', default=8, help='Number of Parents Mating.')
@click.option('--alternative_crossover', '-a', is_flag=False, help='Alternative crossover method.')
@click.option('--mutation', '-x', default=5, help='Mutation Percent.')
@click.option('--generations', '-g', default=150, help='Number of generations.')
@click.option('--subdirectorys', '-s', is_flag=True, default=False, help='Iterate all subdirectories and search for .ll files.')
@click.option('--keepfolders', '-k', is_flag=True, default=False, help='Keep folders structure in output directory if --subdirectorys is True.')
@click.option('--clear', '-c', is_flag=True, default=False, help='Remove files in output directory.')

def cli(dir, output, population, interval, registers, mating, alternative_crossover, mutation, generations, subdirectorys, keepfolders, clear):
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

    if subdirectorys:
        # chama a função para percorrer todos os subdiretórios e salvar os caminhos em uma lista
        subdirs = percorrer_subdiretorios(dir)

        # loop para executar o comando com cada subdiretório como argumento
        for subdir in subdirs:
            if keepfolders:
                path_rel = os.path.relpath(subdir, dir)
                aux_dir = os.path.join(output, path_rel)
                if not os.path.exists(aux_dir):
                    os.makedirs(aux_dir)
            else:
                aux_dir = output
            search_dir(subdir, aux_dir, population, interval, registers, mating, mutation, generations, alternative_crossover)
    search_dir(dir, output, population, interval, registers, mating, mutation, generations, alternative_crossover)



if __name__ == '__main__':
    cli()