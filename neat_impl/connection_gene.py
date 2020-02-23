import numpy as np
import random


class ConnectionGene:
    def __init__(self, in_node, out_node, weight, innovation_number):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = True
        self.innovation_number = innovation_number

    def mutate_weight(self):
        if random.randint(1) < .1:
            self.weight = random.randrange(-30, 30)
        else:
            mu, sigma = 0, .1
            bias = np.random.normal(mu, sigma)
            self.weight += bias

    def disable(self):
        self.enabled = False
