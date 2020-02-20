from neat_impl.node_gene import NodeGene, NodeTypes
from neat_impl.connection_gene import ConnectionGene
import random


class Genome:
    def __init__(self, params):
        self.connection_genes = []  # connection of the node genes => phenotype
        self.nodes = []  # represents input/output node genes

        self.fitness = None

    def mutate(self):
        pass

    def crossover(self, parent1, parent2):
        offspring = Genome({})

        if not parent1.fitness > parent1.fitness:
            parent1, parent2 = parent2, parent1

        for node in parent1.nodes:
            offspring.nodes.append(NodeGene(node.key, node.node_type))

        for parent1_cg in parent1.connection_genes:
            cg_idx = self.matching_gene(parent2, parent1_cg.innovation_number)
            if cg_idx >= 0:
                if random.randint(1) < 0.5:
                    offspring.add_conn(parent1_cg.in_node, parent1_cg.out_node)
                else:
                    parent2_cg = parent2.connection_genes[cg_idx]
                    offspring.add_conn(parent2_cg.in_node, parent2_cg.out_node)
            else:
                # disjoint / excess genes
                offspring.add_conn(parent1_cg.in_node, parent1_cg.out_node)

        return offspring

    def full_connect(self):
        for i in range(3):
            self.nodes.append(NodeGene(i + 1, NodeTypes.INPUT))

        self.nodes.append(NodeGene(4, NodeTypes.OUTPUT))
        self.nodes.append(NodeGene(5, NodeTypes.HIDDEN))

        self.add_conn(self.nodes[0], self.nodes[3])
        self.add_conn(self.nodes[1], self.nodes[3])
        self.add_conn(self.nodes[2], self.nodes[4])
        self.add_conn(self.nodes[4], self.nodes[3])

    def add_conn(self, n_in, n_out):
        weight = random.randrange(-30, 30)
        self.connection_genes \
            .append(ConnectionGene(n_in, n_out, weight, 0))

    def _mutate_add_connection(self):
        in_node = self.nodes[random.randint(len(self.nodes))]
        out_node = self.nodes[random.randint(len(self.nodes))]
        weight = random.randrange(-1, 1)

        if in_node.node_type == NodeTypes.HIDDEN and \
                out_node.node_type == NodeTypes.INPUT:
            in_node, out_node = out_node, in_node

        if in_node.node_type == NodeTypes.OUTPUT and \
                out_node.node_type == NodeTypes.HIDDEN:
            in_node, out_node = out_node, in_node

        if in_node.node_type == NodeTypes.OUTPUT and \
                out_node.node_type == NodeTypes.INPUT:
            in_node, out_node = out_node, in_node

        self.connection_genes \
            .append(ConnectionGene(in_node, out_node, weight, 0))

    def _mutate_add_node(self):
        rand_con = random.randint(len(self.connection_genes))
        connection = self.connection_genes[rand_con]
        self.connection_genes[rand_con].disable()

        in_node = connection.in_node
        out_node = connection.out_node

        new_node = NodeGene(len(self.nodes), NodeTypes.HIDDEN)

        in_to_new = ConnectionGene(in_node, new_node, 1, 0)
        new_to_out = ConnectionGene(new_node, out_node, connection.weight, 0)

        self.nodes.append(new_node)
        self.connection_genes.append([in_to_new, new_to_out])

    @staticmethod
    def matching_gene(parent, innovation):
        for cg_idx, cg in enumerate(parent.connection_genes):
            if innovation == cg.innovation_number:
                return cg_idx

        return -1
