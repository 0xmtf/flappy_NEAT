from neat_impl.genome import Genome
from neat_impl.config import Config
import unittest
import os


class GenomeTest(unittest.TestCase):
    def setUp(self):
        curr_dir = os.path.dirname(__file__)
        path = os.path.join(curr_dir, "test_config\crossover_test_config.json")
        config = Config(config_file=path)
        self.genome_params = config.genome_params

    def test_crossover(self):
        genome1 = Genome(self.genome_params)
        genome2 = Genome(self.genome_params)
        genome1.connect()
        genome2.connect()

        genome1.fitness = 5
        genome2.fitness = 20

        genome2.mutate()

        assert len(genome2.nodes) == 4
        assert len(genome2.connection_genes) == 4
        assert genome2.connection_genes[3].innovation_number == 4

        disabled_gene = None
        for idx, cg in enumerate(genome2.connection_genes):
            if not cg.enabled:
                disabled_gene = idx
                break

        child = genome2.crossover(genome1, genome2)

        # child inherited fittest parent nodes
        assert len(child.nodes) == len(genome2.nodes)
        # should be of same length despite some being disjoint genes
        assert len(child.connection_genes) == len(genome2.connection_genes)
        # check child got disabled gene transferred
        assert child.connection_genes[disabled_gene].enabled == False

if __name__ == "__main__":
    unittest.main()
