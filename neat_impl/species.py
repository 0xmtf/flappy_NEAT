from neat_impl.reproduction import Reproduction
from statistics import mean
import random


class Species:
    def __init__(self):
        self.members = []  # list(Genome)
        self.avg_fitness = None  # avg performance for this species
        self.champion = None  # best performing genome from this species
        self.staleness = 0  # no idea how to compute this yet

    def update(self, new_members, champion):
        self.members.clear()
        self.members.append(new_members)
        if champion.fitness > self.champion.fitness:
            self.champion = champion

        self._update_avg_fitness()

    def _update_avg_fitness(self):
        self.avg_fitness = mean([member.fitness for member in self.members])
