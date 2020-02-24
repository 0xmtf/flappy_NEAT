from neat_impl.node_gene import NodeGene, NodeTypes
from neat_impl.connection_gene import ConnectionGene
from neat_impl.innovation_history import InnovationHistory
import random


class Genome:
    def __init__(self, params):
        self.connection_genes = []  # connection of the node genes => phenotype
        self.nodes = []  # represents input/output node genes
        self.fitness = None

        self.params = params
        self.innovation_history = InnovationHistory()

    def mutate(self):
        if random.randint(1) < self.params.mutate_weight_proba:
            for cg in self.connection_genes:
                cg.mutate_weight()

        if random.randint(1) < self.params.add_conn_proba:
            self._mutate_add_connection()

        if random.randint(1) < self.params.add_node_proba:
            self._mutate_add_node()

    def crossover(self, parent1, parent2):
        offspring = Genome(self.params)

        if not parent1.fitness > parent2.fitness:
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

    def connect(self):
        if self.params.connection_type.lower() == "full" and \
                not self.params.hidden_nodes_count:
            self._full_connect_direct()

    def add_conn(self, in_node, out_node, weight=None):
        if weight is None:
            weight = random.randrange(self.params.min_weight,
                                      self.params.max_weight)

        innovation_number = self.innovation_history \
            .get_innovation(in_node.key, out_node.key)

        self.connection_genes.append(ConnectionGene(in_node,
                                                    out_node,
                                                    weight,
                                                    innovation_number))

    def compatibility_distance(self, genome1, genome2):
        disjoint_distance = (self._disjoint_genes_count(genome1, genome2) *
                             self.params.disjoint_coefficient)
        genes_count = max(len(genome1.connection_genes),
                          len(genome2.connection_genes))
        avg_weight = self._avg_weight_diff(genome1, genome2)

        return (disjoint_distance /
                genes_count +
                avg_weight)

    def _full_connect_direct(self):
        for in_num in range(1, self.params.input_nodes_count + 1):
            self.nodes.append(NodeGene(in_num, NodeTypes.INPUT))

        for out_num in range(1, self.params.output_nodes_count + 1):
            self.nodes.append(NodeGene(in_num + out_num, NodeTypes.OUTPUT))

        in_nodes = [node for node in self.nodes
                    if node.node_type == NodeTypes.INPUT]
        out_nodes = [node for node in self.nodes
                     if node.node_type == NodeTypes.OUTPUT]

        for in_node in in_nodes:
            for out_node in out_nodes:
                self.add_conn(in_node, out_node)

    def _mutate_add_connection(self):
        in_node = self.nodes[random.randint(len(self.nodes))]
        out_node = self.nodes[random.randint(len(self.nodes))]

        if in_node.node_type == NodeTypes.HIDDEN and \
                out_node.node_type == NodeTypes.INPUT:
            in_node, out_node = out_node, in_node

        if in_node.node_type == NodeTypes.OUTPUT and \
                out_node.node_type == NodeTypes.HIDDEN:
            in_node, out_node = out_node, in_node

        if in_node.node_type == NodeTypes.OUTPUT and \
                out_node.node_type == NodeTypes.INPUT:
            in_node, out_node = out_node, in_node

        self.add_conn(in_node, out_node)

    def _mutate_add_node(self):
        rand_con = random.randint(len(self.connection_genes))
        connection = self.connection_genes[rand_con]
        self.connection_genes[rand_con].disable()

        in_node = connection.in_node
        out_node = connection.out_node

        new_node = NodeGene(len(self.nodes), NodeTypes.HIDDEN)

        self.add_conn(in_node, new_node, weight=1)
        self.add_conn(new_node, out_node, weight=connection.weight)

        self.nodes.append(new_node)

    def _disjoint_genes_count(self, genome1, genome2):
        disjoint_nodes = abs(len(genome1.nodes) - len(genome2.nodes))

        if len(genome1.connection_genes) < len(genome2.connection_genes):
            genome1, genome2 = genome2, genome1

        disjoint_connections = 0.0
        inno_numbers1 = [connection.innovation_number
                         for connection in genome1.connection_genes]
        inno_numbers2 = [connection.innovation_number
                         for connection in genome2.connection_genes]

        for inno_number in set(inno_numbers1 + inno_numbers2):
            if inno_number not in inno_numbers1 or \
                    inno_number not in inno_numbers2:
                disjoint_connections += 1

        return disjoint_nodes + disjoint_connections

    def _avg_weight_diff(self, genome1, genome2):
        match_count = 0
        total_diff = 0

        if len(genome1) < len(genome2):
            genome1, genome2 = genome2, genome1

        for cg1 in genome1.connection_genes:
            for cg2 in genome2.connection_genes:
                if cg1.innovation_numbers == cg2.innovation_number:
                    total_diff = abs(cg1.weight - cg2.weight)
                    match_count += 1
                    break

        if match_count == 0:
            return random.randrange(50, 100)

        return total_diff / match_count

    @staticmethod
    def matching_gene(parent, innovation):
        for cg_idx, cg in enumerate(parent.connection_genes):
            if innovation == cg.innovation_number:
                return cg_idx

        return -1
