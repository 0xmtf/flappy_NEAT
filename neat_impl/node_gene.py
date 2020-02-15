from enum import Enum


class NodeGene:
    def __init__(self, key, node_type):
        self.key = key
        self.node_type = node_type


class NodeTypes(Enum):
    INPUT = "input",
    OUTPUT = "output",
    HIDDEN = "hidden"
