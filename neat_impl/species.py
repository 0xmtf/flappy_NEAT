from neat_impl.reproduction import Reproduction
from statistics import mean
import random


class Species:
    def __init__(self):
        self.members = []  # list(Genome)
        self.avg_fitness = None  # avg performance for this species
        self.champion = None  # best performing genome from this species
        self.staleness = 0  # no idea how to compute this yet

    def update(self, new_member):
        self.members.append(new_member)
        if self.champion is None or \
                new_member.fitness > self.champion.fitness:
            self.champion = new_member
        else:
            self.staleness += 5

    def update_avg_fitness(self):
        self.avg_fitness = mean([member.fitness for member in self.members])
