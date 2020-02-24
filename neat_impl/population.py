from neat_impl.reproduction import Reproduction
from neat_impl.species import Species
from statistics import mean


class Population:
    def __init__(self, config):
        self.config = config

        self.reproduction = Reproduction(config.reproduction_params)

        # TODO: replace dumb way of assigning func
        if config.fitness_criterion == "max":
            self.fitness_criterion = max
        elif config.fitness_criterion == "mean":
            self.fitness_criterion = mean

        self.population = self.reproduction.create(config.genome_params)
        # self.species = Species()
        self.generation = 0

        self.species = self._speciate()

        self.champion = None

    def evaluate(self, func, iterations=0):
        champion = None
        curr_iteration = 0
        while curr_iteration < iterations:
            curr_iteration += 1

            func(self.population, self.config)

            best = None
            for genome in self.population:
                if best is None or genome.fitness > best.fitness:
                    best = genome

            if self.champion is None or best.fitness > self.champion.fitness:
                self.champion = best

    def _speciate(self):
        """
        :no exact idea how to do this so will move to separate class later
        :return: population divided into species using individual compatibility distance
        """
        if self.generation == 0:
            return self.population

        new_species = []
        for member in self.species:
            for new_member in self.population:
                compatibility = member.compatibility_distance(member, new_member)

                if compatibility < self.config.genome_params.compatibility_threshold:
                    new_species.append(new_member)

        return []
