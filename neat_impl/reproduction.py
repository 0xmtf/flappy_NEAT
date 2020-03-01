from neat_impl.genome import Genome
from math import floor
import random


class Reproduction:
    def __init__(self, config):
        self.genome_params = config.genome_params
        self.stagnation_params = config.stagnation_params
        self.reproduction_params = config.reproduction_params

    def create(self):
        genomes = []
        for i in range(self.genome_params.population_size):
            g = Genome(self.genome_params)
            g.connect()
            genomes.append(g)

        return genomes

    def breed(self, species):
        performing_species = []
        for s in species:
            if not s.staleness > self.stagnation_params.max_stagnation:
                performing_species.append(s)

        if not performing_species:
            raise Exception()

        species_members_count = tuple([len(s.members) for s in performing_species])

        new_society = []
        # use the best performing species, if any
        for idx, s in enumerate(performing_species):
            spec_members = s.members
            if species_members_count[idx] == 1:
                new_society.append(spec_members[0])
            elif species_members_count[idx] == 2:
                parent1 = spec_members[0]
                parent2 = spec_members[1]
                if parent1.fitness < parent2.fitness:
                    parent1, parent2 = parent2, parent1

                new_society.append(parent1)
                offspring = Genome(self.genome_params)
                offspring.connect()
                offspring = offspring.crossover(parent1, parent2)
                offspring.mutate()
                new_society.append(offspring)
            else:
                added = 0
                spec_members.sort(key=lambda e: e.fitness,
                                  reverse=True)
                if self.reproduction_params.elitism > 0:
                    # this must be changed
                    elite_top_idx = self.reproduction_params.elitism
                    if not floor(species_members_count[idx] / 2) >= self.reproduction_params.elitism:
                        elite_top_idx = 1

                    for elite in spec_members[:elite_top_idx]:
                        new_society.append(elite)
                        spec_members.remove(elite)
                        added += 1
                # use some sort of criteria to ensure
                # there'll be at least 2 parents breeding
                # otherwise it'll breed a genetically identical offspring
                cull_count = max(round(self.reproduction_params.survival_threshold * len(spec_members)), 2)

                spec_members = spec_members[:cull_count]
                while added < species_members_count[idx]:
                    r1 = random.randint(0, len(spec_members) - 1)
                    r2 = random.randint(0, len(spec_members) - 1)
                    parent1 = spec_members[r1]
                    parent2 = spec_members[r2]
                    offspring = Genome(self.genome_params)
                    offspring.connect()
                    offspring = offspring.crossover(parent1, parent2)
                    offspring.mutate()
                    new_society.append(offspring)
                    added += 1

        return new_society
