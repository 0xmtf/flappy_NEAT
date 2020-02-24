from neat_impl.genome import Genome


class Reproduction:
    def __init__(self, params):
        self.params = params

    def create(self, genome_params):
        genomes = []
        for i in range(genome_params.population_size):
            g = Genome(genome_params)
            genomes.append(g.connect())

        return genomes

    def reproduce(self):
        """
        crossover, mutate and i'm lost -_-
        :return: new population
        """
