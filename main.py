import neat
import numpy as np

import graphics

# import tetris
import os
from board import Board


# AI GEN
def find_first_rows(arr):
    if arr.size == 0:
        return np.array([], dtype=int)

    first_ones = np.argmax(arr == 1, axis=0)

    no_ones = ~np.any(arr == 1, axis=0)

    empty_columns = arr.shape[0] == 0

    invalid_columns = no_ones | empty_columns

    first_ones[invalid_columns] = -1

    return first_ones.tolist()


def eval_genomes(genomes, config):
    board_list = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        board_list.append(Board(10, 20, genome, net))
    render = graphics.Graphics()
    while len(board_list) > 0:
        for board in board_list:

            output = board.net.activate(
                [
                    board.piece.x,
                    board.piece.y,
                    board.piece.id,
                    board.piece.rotation,
                    board.rigid_std,
                    board.piece_level,
                ]
                + board.get_board().flatten().tolist()
            )
            key = ["w", " ", "a", "d"][output.index(max(output))]
            if not (board.update("s")):
                board_list.remove(board)
                continue
            if not (board.update(key)):
                board_list.remove(board)
        if len(board_list) == 0:
            break
        render.draw_board(board_list[0])


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    cfg = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    p = neat.Population(cfg)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(eval_genomes, 10)

    print("\nBest genome:\n{!s}".format(winner))
