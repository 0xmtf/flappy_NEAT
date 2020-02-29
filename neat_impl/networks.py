import random


class FeedForwardNetwork:
    # get genome and unpack
    def __init__(self, config, inputs, outputs, hidden):
        self.in_nodes = inputs
        self.out_nodes = outputs
        self.hid_nodes = hidden
        self.input_pairs = []
        self.connection_pairs = []
        # will come from activator
        self.activation_func = max

    def activate(self, inputs=()):
        for k, v in zip(self.in_nodes, inputs):
            self.input_pairs.append((k, v))

        results = []
        for in_node_key, _, weight in self.connection_pairs:
            results.append(self.input_pairs[in_node_key][1] * weight)

        agg = sum(results)
        bias = random.randint(1, 5) * 1.0
        return self.activation_func(agg * bias)

