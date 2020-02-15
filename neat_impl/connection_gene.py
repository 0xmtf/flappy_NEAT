class ConnectionGene:
    def __init__(self, in_node, out_node, weight, innovation_number):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = True
        self.innovation_number = innovation_number

    def disable(self):
        self.enabled = False
