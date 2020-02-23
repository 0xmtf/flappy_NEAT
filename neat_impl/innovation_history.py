class InnovationHistory:
    """
    :Tracks historical markers that identify each gene
    :New genes are assigned new increasingly higher numbers
    :TODO: test if numerical node representations
    :TODO: are enough for tracking old/new genes
    :TODO: might need to keep track of node_type too
    """

    def __init__(self):
        self.connections = []
        self.innovation = 0

    def get_innovation(self, in_node, out_node):
        if not self.connections:
            self._append(in_node, out_node)
            return self.innovation

        for cg in self.connections:
            if cg[0] == in_node and cg[1] == out_node:
                return cg[2]

        self._append(in_node, out_node)
        return self.innovation

    def _append(self, in_node, out_node):
        self.innovation += 1
        self.connections.append((in_node,
                                 out_node,
                                 self.innovation))
