from neat_impl.genome import Genome
from neat_impl.node_gene import NodeTypes
import pygame

gen = Genome({})
gen.full_connect()
active = True
font = pygame.font.SysFont("calibri", 30)
screen = pygame.display.set_mode((800, 800))

while active:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    circle_size = 22
    in_len = len([node for node in gen.nodes
                  if node.node_type == NodeTypes.INPUT])
    nodes_pos = {}
    dist_in = 0

    input_label = font.render("Input layer", 1, (0, 0, 0))
    output_label = font.render("Output layer", 1, (0, 0, 0))
    hidden_layer = font.render("Hidden", 1, (0, 0, 0))

    screen.blit(input_label, (800 / 2 - input_label.get_width() / 2, 15))
    screen.blit(output_label, (800 / 2 - output_label.get_width() / 2, 700))
    screen.blit(hidden_layer, (25, 350))

    for node in gen.nodes:
        if node.node_type == NodeTypes.INPUT:
            pos = (round(800 / in_len + dist_in), 100)
            nodes_pos[node.key] = pos
            pygame.draw.circle(screen, (0, 255, 0), pos, circle_size)
            dist_in += circle_size * 2 * in_len

        if node.node_type == NodeTypes.OUTPUT:
            pos = (800 / 2, 600)
            nodes_pos[node.key] = pos
            pygame.draw.circle(screen, (255, 0, 0), pos, circle_size)

        if node.node_type == NodeTypes.HIDDEN:
            pos = (round(800 / in_len), 350)
            nodes_pos[node.key] = pos
            pygame.draw.circle(screen, (0, 0, 255), pos, circle_size)

    for cg in gen.connection_genes:
        pos_in = nodes_pos[cg.in_node.key]
        pos_out = nodes_pos[cg.out_node.key]

        pygame.draw.line(screen, (0, 0, 0), (pos_in[0], pos_in[1] + circle_size),
                         (pos_out[0], pos_out[1] - circle_size), 2)

    pygame.display.flip()

pygame.quit()
quit()
