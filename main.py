import neat

# import tetris
import os
from board import Board


def eval_genomes(genomes, config):
    board_list = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        board_list.append(Board(10, 20, genome, net))
    print(len(board_list))
    for board in board_list:
        output = board.net.activate(
            board.piece.x,
            board.piece.y,
            board.piece.id,
            board.piece.rotation,
            board.get_board().flatten(),
        )
        key = ["w", " ", "s", "d"][output.index(max(output))]
        board.update(key)


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
    winner = p.run(eval_genomes, 50)

    print("\nBest genome:\n{!s}".format(winner))
