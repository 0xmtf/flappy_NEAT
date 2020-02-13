from neat_impl import genome


class Configurator:
    def __init__(self, config_file):
        """
        :param config_file: configuration params
        """
        self.genome = genome.Genome(params=None)
        self.reproduction = None
        self.species = None
        self.stagnation = None
